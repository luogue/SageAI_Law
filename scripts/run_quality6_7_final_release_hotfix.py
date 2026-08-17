"""Production acceptance for Contract Review Quality 6.7 Final Release Hotfix."""

from __future__ import annotations

import asyncio
import hashlib
import io
import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "backend"))

from routers.review_v2 import ReviewV2PdfInput, _build_docx, review_v2_file


class Upload:
    def __init__(self, path: Path):
        self.filename = path.name
        self.file = io.BytesIO(path.read_bytes())


async def review(path: Path, contract_type: str) -> Dict[str, Any]:
    return await review_v2_file(
        file=Upload(path), contract_type=contract_type, include_low_risk=True,
        use_llm=False, profile_json="{}", current_user={"id": "quality-6.7-final-release-hotfix"},
    )


def write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")


def digest(value: Any) -> str:
    raw = value if isinstance(value, bytes) else json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), default=str,
    ).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def export_docx(result: Dict[str, Any], filename: str) -> bytes:
    fields = ReviewV2PdfInput.model_fields
    payload = {key: value for key, value in result.items() if key in fields}
    payload["filename"] = filename
    return _build_docx(ReviewV2PdfInput(**payload))


def git_commit() -> str:
    completed = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True, check=False,
    )
    return completed.stdout.strip() or "UNCOMMITTED"


async def main() -> int:
    output = ROOT / "output" / "quality6_7_final_release_hotfix"
    output.mkdir(parents=True, exist_ok=True)
    paths = {
        "SALE_HB_001": next((ROOT / "test_data").glob("2*.docx")),
        "SALE_HB_002": next((ROOT / "test_data").glob("5*.docx")),
        "SALE_HB_003": next((ROOT / "test_data").glob("6*.docx")),
        "SALE_HB_004": next((ROOT / "test_data").glob("7*.docx")),
        "RENTAL_REGRESSION": next((ROOT / "test_data").glob("1*.docx")),
    }
    results = {
        name: await review(path, "house_lease" if name == "SALE_HB_004" else "sale")
        for name, path in paths.items()
    }
    hb4 = results["SALE_HB_004"]
    report = hb4["result"]
    release_gates = hb4["release_quality_gate"].get("gate_results", {})
    observability = hb4["observability"]
    recommendation_renderer = observability["recommendation_cross_renderer_debug"]
    recommendation_impact = observability["recommendation_non_degradation_gate"]
    legal_authority = hb4["legal_authority_gate"]
    default_law_provenance = hb4["default_law_provenance_gate"]
    default_law_narrative = hb4["default_law_narrative_truth_gate"]
    shared_claim = hb4["cross_review_shared_claim_gate"]
    cross_review = observability["cross_review_consistency_debug"]
    items = {item["item_id"]: item for item in hb4["items"]}

    export_bytes = export_docx(hb4, paths["SALE_HB_004"].name)
    (output / "sale_hb_004_report.docx").write_bytes(export_bytes)

    gate_names = (
        "RECOMMENDATION_SINGLE_SOURCE_GATE", "RECOMMENDATION_CROSS_RENDERER_CONSISTENCY_GATE",
        "RECOMMENDATION_NON_DEGRADATION_GATE", "LEGAL_AUTHORITY_DEDUP_GATE",
        "LEGAL_AUTHORITY_SELECTION_GATE", "CITATION_ENTAILMENT_GATE",
        "DEFAULT_LAW_EFFECTIVE_GAP_GATE", "DEFAULT_LAW_PROVENANCE_GATE",
        "DEFAULT_LAW_NARRATIVE_TRUTH_GATE", "CROSS_REVIEW_SHARED_CLAIM_GATE",
        "FALSE_RISK_EXISTENCE_GATE", "PERSPECTIVE_DOMAIN_CONSISTENCY_GATE",
        "REPORT_TRANSACTION_TRUTH_GATE", "PRODUCTION_INTERNAL_TOKEN_GATE",
        "PRODUCTION_FACT_POLARITY_GATE", "COMMON_REVIEW_SATISFACTION_GATE",
        "ELEMENT_IDENTITY_CONTRADICTION_GATE", "PRODUCT_APPLICABILITY_GATE",
        "SHARED_CLAIM_REUSE_GATE", "FINDING_INDEPENDENCE_GATE", "NARRATIVE_TRUTH_GATE",
    )
    acceptance = {name: release_gates.get(name) == "PASS" for name in gate_names}
    for name, result in results.items():
        acceptance[name] = result["release_quality_gate"]["status"] == "REPORT_READY"
    acceptance["REAL_PRODUCTION_INTEGRATION"] = (
        all(result.get("success") for result in results.values())
        and export_bytes.startswith(b"PK") and len(export_bytes) > 1000
    )

    counts = {
        "RECOMMENDATION_DUAL_SOURCE_COUNT": recommendation_renderer.get("dual_source_count", 0),
        "RECOMMENDATION_CROSS_RENDERER_MISMATCH_COUNT": recommendation_renderer.get("cross_renderer_mismatch_count", 0),
        "ADVERSE_RECOMMENDATION_COUNT": recommendation_impact.get("adverse_recommendation_count", 0),
        "LEGAL_AUTHORITY_DUPLICATE_COUNT": legal_authority.get("duplicate_count", 0),
        "LEGAL_PROVENANCE_BREAK_COUNT": default_law_provenance.get("break_count", 0),
        "MATERIAL_CITATION_NOT_SUPPORT_COUNT": legal_authority.get("material_citation_not_support_count", 0),
        "DEFAULT_LAW_NARRATIVE_CONTRADICTION_COUNT": default_law_narrative.get("contradiction_count", 0),
        "CROSS_REVIEW_SHARED_CLAIM_CONTRADICTION_COUNT": shared_claim.get("contradiction_count", 0),
        "NARRATIVE_CONTRADICTION_COUNT": sum(
            1 for row in observability["narrative_state_debug_report"] if row.get("status") != "PASS"
        ),
    }
    wrong_perspective_tokens = sum(report.count(token) for token in ("租客", "承租人", "出租人"))
    hb4_invariants = (
        hb4["contract_context"].get("contract_family") == "SALE"
        and hb4["contract_context"].get("subject_matter") == "GOODS"
        and hb4["contract_context"].get("transaction_structure") == "FRAMEWORK_SUPPLY"
        and hb4["perspective_resolution"].get("canonical_role") == "BUYER"
        and hb4["domain_selection_consistency_gate"].get("wrong_domain_review_count") == 0
        and wrong_perspective_tokens == 0
        and observability["production_token_scan"].get("count", 0) == 0
        and observability["production_fact_polarity_debug"].get("contradiction_count", 0) == 0
        and items["S-12-04"]["coverage_status"] in {"通过", "部分覆盖"}
        and items["FS-14"]["coverage_status"] in {"通过", "部分覆盖"}
    )
    frozen = all(acceptance.values()) and all(value == 0 for value in counts.values()) and hb4_invariants

    source_paths = (
        ROOT / "backend/review_v2/engine.py",
        ROOT / "backend/review_v2/quality4.py",
        ROOT / "backend/review_v2/recommendation_impact.py",
        ROOT / "backend/review_v2/ARCHITECTURE_NOTES.md",
        ROOT / "backend/tests/test_quality6_7_final_release_hotfix.py",
        ROOT / "scripts/run_quality6_7_final_release_hotfix.py",
    )
    source_hashes = {str(path.relative_to(ROOT)): digest(path.read_bytes()) for path in source_paths}
    case_summary = {
        name: {
            "report_ready": result["release_quality_gate"]["status"] == "REPORT_READY",
            "domain": result["contract_context"].get("contract_family"),
            "subject": result["contract_context"].get("subject_matter"),
            "structure": result["contract_context"].get("transaction_structure"),
            "perspective": result["perspective_resolution"].get("canonical_role"),
        }
        for name, result in results.items()
    }
    manifest = {
        "system_version": "contract-review-quality-6.7-final-release-hotfix",
        "git_commit": git_commit(), "model_version": "qwen-doubao-cloud-fallback",
        "prompt_version": "quality-6.7-final-release-hotfix",
        "parser_version": "frozen-6.7", "domain_version": "frozen-6.7",
        "perspective_version": "frozen-6.7", "fact_graph_version": "frozen-6.7",
        "claim_graph_version": "frozen-6.7", "review_registry_version": "frozen-6.7",
        "domain_pack_version": "frozen-6.7", "legal_dataset_version": "quality4-current",
        "legal_entailment_version": "proposition-entailment-6.7",
        "default_law_version": "default-law-6.7", "effective_gap_version": "effective-gap-6.7",
        "recommendation_engine_version": "recommendation-impact-6.7",
        "renderer_version": "recommendation-ssot-6.7", "regression_version": "final-release-hotfix-1",
    }
    candidate_hash = digest({
        "manifest": manifest, "source_hashes": source_hashes,
        "acceptance": acceptance, "counts": counts, "cases": case_summary,
    })
    manifest["candidate_hash"] = candidate_hash

    legal_entailment_rows = [
        entailment
        for row in legal_authority.get("rows", [])
        for entailment in row.get("entailment", [])
    ]
    write_json(output / "recommendation_ssot_debug.json", observability["recommendation_ssot_debug"])
    write_json(output / "recommendation_cross_renderer_debug.json", recommendation_renderer)
    write_json(output / "recommendation_non_degradation_debug.json", {
        "gate": recommendation_impact,
        "impacts": observability["recommendation_impact_debug"],
    })
    write_json(output / "legal_authority_dedup_debug.json", {
        "gate_results": legal_authority["gate_results"],
        "candidate_duplicate_count": legal_authority.get("candidate_duplicate_count", 0),
        "production_duplicate_count": legal_authority.get("duplicate_count", 0),
        "rows": legal_authority.get("rows", []),
    })
    write_json(output / "legal_authority_selection_debug.json", legal_authority.get("rows", []))
    write_json(output / "legal_proposition_entailment_debug.json", legal_entailment_rows)
    write_json(output / "default_law_narrative_debug.json", default_law_narrative)
    write_json(output / "sale_hb_004_final_release_regression.json", {
        "report_ready": hb4["release_quality_gate"]["status"] == "REPORT_READY",
        "domain": "SALE / GOODS / FRAMEWORK_SUPPLY", "perspective": "BUYER",
        "wrong_domain_review_count": hb4["domain_selection_consistency_gate"].get("wrong_domain_review_count"),
        "wrong_perspective_token_count": wrong_perspective_tokens,
        "internal_token_count": observability["production_token_scan"].get("count", 0),
        "fact_polarity_contradiction_count": observability["production_fact_polarity_debug"].get("contradiction_count", 0),
        "cross_review_shared_claim_contradiction_count": shared_claim.get("contradiction_count", 0),
        "s_12_04": items["S-12-04"]["coverage_status"], "fs_14": items["FS-14"]["coverage_status"],
        "acceptance": acceptance, "counts": counts,
    })
    write_json(output / "final_regression_summary.json", {
        "contract_review_6_7": "PASS" if frozen else "FAIL", "acceptance": acceptance,
        "counts": counts, "cases": case_summary, "candidate_manifest": manifest,
        "source_hashes": source_hashes, "sale_hb_004_frozen": frozen,
        "candidate_frozen": frozen, "candidate_hash": candidate_hash,
        "next_blind_status": "READY" if frozen else "NOT_READY", "next_blind": "SALE-BLIND-005",
    })
    (output / "6_7_final_release_hotfix_root_cause.md").write_text(
        "# Quality 6.7 Final Release Hotfix Root Cause\n\n"
        "Production recommendation prose had two owners: the Recommendation pipeline and the detail renderer's "
        "missing-element narrative. A recommendation blocked by non-degradation could therefore reappear in detail. "
        "Legal references were also assembled from Review and Default Law paths without structured best-authority "
        "selection, while citation validity was evaluated at Review rather than proposition level. Finally, Default "
        "Law could influence risk without a user-facing distinction between contractual coverage and statutory fallback.\n\n"
        "The hotfix makes FinalRecommendationSet the only production recommendation source, selects and deduplicates "
        "authorities by structured identity and proposition entailment, and renders Effective Gap as contract state, "
        "statutory fallback, and residual exposure. Domain, Fact, Claim, Coverage, and Framework Supply remain frozen.\n",
        encoding="utf-8",
    )

    lines = ["CONTRACT_REVIEW_6_7 = " + ("PASS" if frozen else "FAIL"), ""]
    lines.extend(f"{name} = {'PASS' if acceptance[name] else 'FAIL'}" for name in gate_names)
    lines.append("")
    lines.extend(f"{name} = {'PASS' if acceptance[name] else 'FAIL'}" for name in (*paths.keys(), "REAL_PRODUCTION_INTEGRATION"))
    lines.append("")
    lines.extend(f"{name} = {value}" for name, value in counts.items())
    lines.extend([
        "", f"SALE_HB_004_FROZEN = {str(frozen).lower()}",
        f"CANDIDATE_FROZEN = {str(frozen).lower()}", f"CANDIDATE_HASH = {candidate_hash}", "",
        f"NEXT_BLIND_STATUS = {'READY' if frozen else 'NOT_READY'}", "NEXT_BLIND = SALE-BLIND-005",
    ])
    print("\n".join(lines))
    return 0 if frozen else 1


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
