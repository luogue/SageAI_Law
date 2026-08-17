"""Production-entry acceptance and freeze artifacts for Quality 6.7 Final Freeze Patch."""

from __future__ import annotations

import asyncio
import hashlib
import io
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "backend"))

from routers.review_v2 import review_v2_file


class Upload:
    def __init__(self, path: Path):
        self.filename = path.name
        self.file = io.BytesIO(path.read_bytes())


async def review(path: Path, contract_type: str) -> Dict[str, Any]:
    return await review_v2_file(
        file=Upload(path), contract_type=contract_type, include_low_risk=True,
        use_llm=False, profile_json="{}", current_user={"id": "quality-6.7-final-freeze"},
    )


def write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")


def digest(value: Any) -> str:
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), default=str).encode()
    return hashlib.sha256(raw).hexdigest()


async def main() -> int:
    output = ROOT / "output" / "quality6_7_final_freeze"
    output.mkdir(parents=True, exist_ok=True)
    paths = {
        "SALE_HB_001": next((ROOT / "test_data").glob("2*.docx")),
        "SALE_HB_002": next((ROOT / "test_data").glob("5*.docx")),
        "SALE_HB_003": next((ROOT / "test_data").glob("6*.docx")),
        "SALE_HB_004": next((ROOT / "test_data").glob("7*.docx")),
        "RENTAL_REGRESSION": next((ROOT / "test_data").glob("1*.docx")),
    }
    results = {
        name: await review(path, "house_lease" if name == "SALE_HB_004" else "sale" if name != "RENTAL_REGRESSION" else "sale")
        for name, path in paths.items()
    }
    hb4 = results["SALE_HB_004"]
    report = hb4["result"]
    gates = hb4["release_quality_gate"].get("gate_results", {})
    internal_scan = hb4["observability"]["production_token_scan"]
    polarity = hb4["observability"]["production_fact_polarity_debug"]
    rec_gate = hb4["observability"]["recommendation_non_degradation_gate"]
    narrative = hb4["observability"]["narrative_state_debug_report"]
    wrong_perspective = sum(report.count(token) for token in ("租客", "承租人", "出租人"))
    narrative_contradictions = sum(1 for row in narrative if row.get("status") != "PASS")
    element_contradictions = sum(len(row.get("element_identity_conflicts") or []) for row in narrative)

    cases = {}
    for name, result in results.items():
        case_gates = result["release_quality_gate"].get("gate_results", {})
        ids = [item["item_id"] for item in result["items"]]
        cases[name] = {
            "status": "PASS" if result["release_quality_gate"]["status"] == "REPORT_READY" else "FAIL",
            "report_ready": result["release_quality_gate"]["status"] == "REPORT_READY",
            "resolved_domain": result["domain_selection_resolution"]["selected_domain"],
            "perspective": result["perspective_resolution"],
            "wrong_domain_review_count": result["domain_selection_consistency_gate"]["wrong_domain_review_count"],
            "review_counts": {"HL": sum(x.startswith("HL-") for x in ids), "S": sum(x.startswith("S-") for x in ids), "FS": sum(x.startswith("FS-") for x in ids)},
            "gates": case_gates,
        }

    required_gates = (
        "PERSPECTIVE_DOMAIN_CONSISTENCY_GATE", "REPORT_TRANSACTION_TRUTH_GATE",
        "PRODUCTION_INTERNAL_TOKEN_GATE", "PRODUCTION_FACT_POLARITY_GATE",
        "DEFAULT_LAW_EFFECTIVE_GAP_GATE", "RECOMMENDATION_NON_DEGRADATION_GATE",
        "COMMON_REVIEW_SATISFACTION_GATE", "ELEMENT_IDENTITY_CONTRADICTION_GATE",
        "PRODUCT_APPLICABILITY_GATE", "SHARED_CLAIM_REUSE_GATE",
        "FINDING_INDEPENDENCE_GATE", "NARRATIVE_TRUTH_GATE",
    )
    acceptance = {
        gate: gates.get(gate) == "PASS" for gate in required_gates
    }
    acceptance.update({name: row["status"] == "PASS" for name, row in cases.items()})
    acceptance.update({
        "WRONG_PERSPECTIVE_TOKEN_COUNT": wrong_perspective,
        "INTERNAL_TOKEN_COUNT": internal_scan.get("count", 0),
        "FACT_POLARITY_CONTRADICTION_COUNT": polarity.get("contradiction_count", 0),
        "NARRATIVE_CONTRADICTION_COUNT": narrative_contradictions,
        "ELEMENT_IDENTITY_CONTRADICTION_COUNT": element_contradictions,
        "ADVERSE_RECOMMENDATION_COUNT": rec_gate.get("adverse_recommendation_count", 0),
        "REAL_PRODUCTION_INTEGRATION": all(row["report_ready"] for row in cases.values()),
    })
    frozen = all(value is True for key, value in acceptance.items() if not key.endswith("_COUNT")) and all(
        acceptance[key] == 0 for key in acceptance if key.endswith("_COUNT")
    )
    git_commit = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip()
    metadata = hb4["system_metadata"]
    manifest = {
        "system_version": metadata["system_version"], "git_commit": git_commit,
        "model_version": metadata["model_version"], "prompt_version": metadata["prompt_version"],
        "parser_version": metadata["parser_version"], "classification_version": "domain-selection-consistency-1.0",
        "perspective_resolver_version": metadata["perspective_resolver_version"],
        "fact_graph_version": metadata["fact_graph_version"],
        "claim_graph_version": hb4["contract_facts"]["canonical_claims"]["version"],
        "domain_pack_version": metadata["domain_pack_version"], "review_registry_version": "review-registry-6.7",
        "legal_dataset_version": metadata["legal_dataset_version"], "default_law_engine_version": metadata["default_law_version"],
        "effective_gap_engine_version": metadata["effective_gap_engine_version"],
        "recommendation_engine_version": metadata["recommendation_engine_version"],
        "production_serializer_version": metadata["production_serializer_version"],
        "benchmark_version": metadata["benchmark_version"], "generated_at": datetime.now().isoformat(),
    }
    manifest["candidate_hash"] = digest({"manifest": manifest, "acceptance": acceptance, "cases": cases})

    write_json(output / "perspective_resolution_debug.json", hb4["perspective_resolution"])
    write_json(output / "production_humanization_debug.json", hb4["observability"]["production_humanization_debug"])
    write_json(output / "production_token_scan.json", internal_scan)
    write_json(output / "production_fact_polarity_debug.json", polarity)
    write_json(output / "default_law_effective_gap_debug.json", hb4["observability"]["default_law_debug_table"])
    write_json(output / "recommendation_impact_debug.json", hb4["observability"]["recommendation_impact_debug"])
    write_json(output / "sale_hb_004_freeze_regression.json", {"case": cases["SALE_HB_004"], "acceptance": acceptance})
    write_json(output / "final_regression_summary.json", {"acceptance": acceptance, "cases": cases, "manifest": manifest, "frozen": frozen})
    (output / "6_7_final_freeze_root_cause.md").write_text(
        "# Quality 6.7 Final Freeze Root Cause\n\n"
        "Perspective was inferred independently by profile, context, item, and renderer code, allowing a carried lease role to be merged with a resolved sale role. "
        "Commercial fact keys were also used directly as coverage propositions, so machine identifiers reached production narrative. "
        "The patch establishes resolved perspective as SSOT, maps structured fact values to deterministic user meaning, validates fact polarity, records Default Law to Effective Gap state, and blocks adverse recommendations before serialization.\n",
        encoding="utf-8",
    )
    print(json.dumps({"frozen": frozen, "candidate_hash": manifest["candidate_hash"], "acceptance": acceptance}, ensure_ascii=False, indent=2))
    return 0 if frozen else 1


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
