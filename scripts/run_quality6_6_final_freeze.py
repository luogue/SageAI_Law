"""Quality 6.6 final patch acceptance and candidate freeze."""

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

from routers.review_v2 import ReviewV2PdfInput, _build_docx, review_v2_file


NARRATIVE_VERSION = "element-narrative-6.6-final"
SERIALIZER_VERSION = "production-debug-isolation-6.6-final"


class Upload:
    def __init__(self, path: Path):
        self.filename = path.name
        self.file = io.BytesIO(path.read_bytes())


async def review(path: Path, contract_type: str) -> Dict[str, Any]:
    return await review_v2_file(
        file=Upload(path), contract_type=contract_type, include_low_risk=True,
        use_llm=False, profile_json="{}", current_user={"id": "quality-6.6-final-audit"},
    )


def write(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")


def sha(value: Any) -> str:
    data = value if isinstance(value, bytes) else json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(data).hexdigest()


def export_docx(result: Dict[str, Any], filename: str) -> bytes:
    fields = ReviewV2PdfInput.model_fields
    values = {key: value for key, value in result.items() if key in fields}
    values["filename"] = filename
    payload = ReviewV2PdfInput(**values)
    return _build_docx(payload)


async def main() -> int:
    out = ROOT / "output" / "quality6_6"
    out.mkdir(parents=True, exist_ok=True)
    paths = {
        "SALE-HB-003": next((ROOT / "test_data").glob("6*.docx")),
        "SALE-HB-001": next((ROOT / "test_data").glob("2*.docx")),
        "SALE-HB-002": next((ROOT / "test_data").glob("5*.docx")),
        "RENTAL": next((ROOT / "test_data").glob("1*.docx")),
    }
    results: Dict[str, Dict[str, Any]] = {}
    for name, path in paths.items():
        results[name] = await review(path, "house_lease" if name == "RENTAL" else "sale")

    hb3 = results["SALE-HB-003"]
    by_id = {item["item_id"]: item for item in hb3["items"]}
    gates = hb3["release_quality_gate"].get("gate_results", {})
    agency = by_id["RE-01-06"]
    rights = by_id["RE-02-04"]
    payment = by_id["S-05-03"]
    findings_by_review = {review_id for finding in hb3["risk_findings"] for review_id in finding["source_review_ids"]}
    goods_terms = ("货交承运人", "试用买卖", "凭样品买卖", "包装和随附资料", "保修卡")
    export_bytes = export_docx(hb3, paths["SALE-HB-003"].name)

    requirements = {
        "PASS_EVIDENCE_PROVENANCE_GATE": gates.get("PASS_EVIDENCE_PROVENANCE_GATE") == "PASS" and bool(rights["review_evidence_provenance"].get("evidence_ids")) and rights["evidence_location"] != "未召回正式条款",
        "PARTIAL_ELEMENT_NARRATIVE_GATE": gates.get("PARTIAL_ELEMENT_NARRATIVE_GATE") == "PASS" and (payment["coverage_status"] != "部分覆盖" or bool(payment.get("narrative_state"))),
        "PRODUCTION_INTERNAL_TOKEN_GATE": gates.get("PRODUCTION_INTERNAL_TOKEN_GATE") == "PASS" and hb3["observability"]["production_token_scan"]["count"] == 0,
        "APPLICABILITY_PRECONDITION_GATE": gates.get("APPLICABILITY_PRECONDITION_GATE") == "PASS" and agency["applicability"]["status"] == "NOT_APPLICABLE" and "RE-01-06" not in findings_by_review,
        "SHARED_CLAIM_CONSISTENCY_GATE": gates.get("SHARED_CLAIM_CONSISTENCY_GATE") == "PASS" and rights["coverage_status"] == "通过",
        "FINDING_PRECONDITION_GATE": gates.get("FINDING_PRECONDITION_GATE") == "PASS",
        "REPORT_CONTEXT_GATE": gates.get("REPORT_CONTEXT_GATE") == "PASS" and hb3["report_context"]["scenario_label"] == "二手住宅房地产买卖",
        "NARRATIVE_TRUTH_GATE": gates.get("NARRATIVE_TRUTH_GATE") == "PASS",
        "SALE_HB_001": results["SALE-HB-001"]["release_quality_gate"]["status"] == "REPORT_READY",
        "SALE_HB_002": results["SALE-HB-002"]["release_quality_gate"]["status"] == "REPORT_READY",
        "SALE_HB_003": hb3["release_quality_gate"]["status"] == "REPORT_READY",
        "RENTAL_REGRESSION": results["RENTAL"]["release_quality_gate"]["status"] == "REPORT_READY",
        "REAL_PRODUCTION_INTEGRATION": all(result["success"] for result in results.values()) and export_bytes.startswith(b"PK") and len(export_bytes) > 1000,
        "GOODS_REVIEW_ISOLATION": not any(term in hb3["result"] for term in goods_terms),
    }

    claim_debug = {
        "review_id": rights["item_id"],
        "coverage": rights["coverage_status"],
        "claim_ids": rights["review_evidence_provenance"].get("claim_ids", []),
        "claim_source_clause_ids": sorted({clause_id for element in rights["coverage_elements"] for clause_id in element.get("source_clause_ids", [])}),
        "aggregated_review_evidence": rights["review_evidence_provenance"],
        "display_locations": rights["evidence_location"].split("；") if rights["evidence_location"] else [],
    }
    partial_debug = [
        {
            "review_id": item["item_id"],
            "coverage_status": item["coverage_status"],
            "covered_elements": item.get("narrative_state", {}).get("covered_elements", []),
            "missing_elements": item.get("narrative_state", {}).get("missing_elements", []),
            "generated_issue": item.get("narrative_state", {}).get("issue", ""),
            "generated_consequence": item.get("narrative_state", {}).get("consequence", ""),
            "generated_recommendation": item.get("narrative_state", {}).get("recommendation", ""),
        }
        for item in hb3["items"]
        if item["coverage_status"] == "部分覆盖"
    ]
    write(out / "claim_provenance_debug.json", claim_debug)
    write(out / "partial_narrative_debug.json", partial_debug)
    write(out / "production_token_scan.json", hb3["observability"]["production_token_scan"])
    write(out / "final_regression_summary.json", {
        "requirements": {key: "PASS" if value else "FAIL" for key, value in requirements.items()},
        "release": {name: result["release_quality_gate"]["status"] for name, result in results.items()},
        "contexts": {name: result["contract_context"] for name, result in results.items()},
        "export": {"format": "docx", "valid_zip": export_bytes.startswith(b"PK"), "bytes": len(export_bytes)},
    })
    (out / "6_6_final_patch_root_cause.md").write_text(
        "# Quality 6.6 Final Patch Root Cause\n\n"
        "## PASS evidence provenance\n\n"
        "`backend/review_v2/engine.py::_coverage_elements_for_item` preserved only evidence IDs for Canonical Claim elements. The active path `_apply_coverage_evidence_gate -> _format_markdown_v2` therefore depended on a separate evidence list. Coverage elements now retain claim, clause, span and location provenance; `_aggregate_review_provenance` unions and deduplicates it before rendering.\n\n"
        "## PARTIAL narrative fidelity\n\n"
        "`backend/review_v2/engine.py::_apply_element_level_narratives` previously rewrote text only when a small forbidden-phrase list matched. The active path could leave issue, consequence and recommendation describing covered elements as missing. `_build_narrative_state` now derives all four production fields from the same element states.\n\n"
        "## Production debug isolation\n\n"
        "`backend/review_v2/engine.py::_professional_item_conclusion` and `_display_legal_consequence` consumed Applicability `reason`, which was the machine explanation. Applicability now exposes `machine_reason` and `user_reason`; production serializers consume only `user_reason`, followed by `PRODUCTION_INTERNAL_TOKEN_GATE`. Debug output retains the machine state.\n",
        encoding="utf-8",
    )

    versions = {
        "system_version": "contract-review-quality-6.6",
        "git_commit": subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True, capture_output=True).stdout.strip(),
        "model_version": hb3["system_metadata"].get("model_version", "deterministic_pipeline"),
        "prompt_version": hb3["system_metadata"].get("prompt_version", "current"),
        "parser_version": hb3["document_integrity"].get("parser_version", "current"),
        "classification_version": "hierarchical-domain-resolution-6.5",
        "fact_schema_version": hb3["contract_facts"].get("version", "contract-fact-graph-1.0"),
        "claim_schema_version": hb3["contract_facts"]["canonical_claims"]["version"],
        "domain_pack_version": hb3["contract_context"]["domain_attributes"]["domain_pack"],
        "review_ontology_version": "real-estate-sale-review-6.6",
        "retrieval_version": "fact-first-recall-6.4",
        "narrative_version": NARRATIVE_VERSION,
        "serializer_version": SERIALIZER_VERSION,
        "benchmark_version": "known-regression-6.6-final",
    }
    candidate_hash = sha({"versions": versions, "requirements": requirements, "sources": {name: sha(path.read_bytes()) for name, path in paths.items()}})
    passed = all(requirements.values())
    manifest = {
        **versions,
        "candidate_hash": candidate_hash,
        "status": "PASS" if passed else "FAIL",
        "created_at": datetime.now().isoformat(),
        "requirements": {key: "PASS" if value else "FAIL" for key, value in requirements.items()},
        "sale_hb_003_frozen": passed,
        "candidate_frozen": passed,
        "next_blind_status": "READY" if passed else "NOT_READY",
        "next_blind": "SALE-BLIND-004",
    }
    write(out / "candidate_manifest.json", manifest)
    print(json.dumps(manifest, ensure_ascii=False, indent=2))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
