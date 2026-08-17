"""Production acceptance and freeze artifacts for Quality 6.7 Final Freeze Hotfix."""

from __future__ import annotations

import asyncio
import hashlib
import io
import json
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
        use_llm=False, profile_json="{}", current_user={"id": "quality-6.7-freeze-hotfix"},
    )


def write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")


def digest(value: Any) -> str:
    raw = value if isinstance(value, bytes) else json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), default=str).encode()
    return hashlib.sha256(raw).hexdigest()


def export_docx(result: Dict[str, Any], filename: str) -> bytes:
    fields = ReviewV2PdfInput.model_fields
    payload = {key: value for key, value in result.items() if key in fields}
    payload["filename"] = filename
    return _build_docx(ReviewV2PdfInput(**payload))


async def main() -> int:
    output = ROOT / "output" / "quality6_7_freeze_hotfix"
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
    gates = hb4["release_quality_gate"].get("gate_results", {})
    cross_debug = hb4["observability"]["cross_review_consistency_debug"]
    shared_debug = hb4["observability"]["shared_claim_consumer_debug"]
    document_precedence = next(row for row in shared_debug if row["claim_id"] == "document.precedence")
    law_debug = hb4["observability"]["default_law_provenance_debug"]
    recommendation_debug = hb4["observability"]["recommendation_impact_debug"]
    items = {item["item_id"]: item for item in hb4["items"]}

    cross_count = sum(len(row.get("contradictions") or []) for row in shared_debug)
    legal_break_count = law_debug.get("break_count", 0)
    adverse_count = hb4["recommendation_non_degradation_gate"].get("adverse_recommendation_count", 0)
    wrong_perspective_count = sum(report.count(token) for token in ("租客", "承租人", "出租人"))
    internal_count = hb4["observability"]["production_token_scan"].get("count", 0)
    polarity_count = hb4["observability"]["production_fact_polarity_debug"].get("contradiction_count", 0)
    narrative_count = sum(1 for row in hb4["observability"]["narrative_state_debug_report"] if row.get("status") != "PASS")
    identity_count = len(cross_debug.get("element_identity_contradictions") or [])
    export_bytes = export_docx(hb4, paths["SALE_HB_004"].name)

    gate_names = (
        "CROSS_REVIEW_SHARED_CLAIM_GATE", "SHARED_CLAIM_REUSE_GATE", "FALSE_RISK_EXISTENCE_GATE",
        "DEFAULT_LAW_EFFECTIVE_GAP_GATE", "DEFAULT_LAW_PROVENANCE_GATE", "RECOMMENDATION_NON_DEGRADATION_GATE",
        "PERSPECTIVE_DOMAIN_CONSISTENCY_GATE", "REPORT_TRANSACTION_TRUTH_GATE", "PRODUCTION_INTERNAL_TOKEN_GATE",
        "PRODUCTION_FACT_POLARITY_GATE", "COMMON_REVIEW_SATISFACTION_GATE", "ELEMENT_IDENTITY_CONTRADICTION_GATE",
        "PRODUCT_APPLICABILITY_GATE", "FINDING_INDEPENDENCE_GATE", "NARRATIVE_TRUTH_GATE",
    )
    acceptance = {name: gates.get(name) == "PASS" for name in gate_names}
    for name, result in results.items():
        acceptance[name] = result["release_quality_gate"]["status"] == "REPORT_READY"
    acceptance["REAL_PRODUCTION_INTEGRATION"] = (
        all(result.get("success") for result in results.values())
        and export_bytes.startswith(b"PK") and len(export_bytes) > 1000
    )
    counts = {
        "CROSS_REVIEW_SHARED_CLAIM_CONTRADICTION_COUNT": cross_count,
        "LEGAL_PROVENANCE_BREAK_COUNT": legal_break_count,
        "ADVERSE_RECOMMENDATION_COUNT": adverse_count,
        "WRONG_PERSPECTIVE_TOKEN_COUNT": wrong_perspective_count,
        "INTERNAL_TOKEN_COUNT": internal_count,
        "FACT_POLARITY_CONTRADICTION_COUNT": polarity_count,
        "NARRATIVE_CONTRADICTION_COUNT": narrative_count,
        "ELEMENT_IDENTITY_CONTRADICTION_COUNT": identity_count,
    }
    hb4_invariants = (
        hb4["contract_context"]["contract_family"] == "SALE"
        and hb4["contract_context"]["subject_matter"] == "GOODS"
        and hb4["contract_context"]["transaction_structure"] == "FRAMEWORK_SUPPLY"
        and hb4["perspective_resolution"]["canonical_role"] == "BUYER"
        and hb4["domain_selection_consistency_gate"]["wrong_domain_review_count"] == 0
        and document_precedence["consumer_reviews"] == ["S-12-04", "FS-14"]
        and all(element.get("claim_id") == "document.precedence" for review_id in ("S-12-04", "FS-14") for element in items[review_id]["coverage_elements"])
    )
    frozen = all(acceptance.values()) and all(value == 0 for value in counts.values()) and hb4_invariants

    source_hashes = {
        str(path.relative_to(ROOT)): digest(path.read_bytes())
        for path in (
            ROOT / "backend/review_v2/canonical_claims.py",
            ROOT / "backend/review_v2/engine.py",
            ROOT / "backend/review_v2/quality4.py",
            ROOT / "backend/review_v2/recommendation_impact.py",
        )
    }
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
    candidate_hash = digest({"source_hashes": source_hashes, "acceptance": acceptance, "counts": counts, "cases": case_summary})

    effective_protection = [
        {
            "recommendation_id": row["recommendation_id"],
            "user_role": row["user_role"],
            "current_contract_position": row["current_protection"],
            "current_statutory_position": row["current_rights"],
            "effective_current_position": row["current_rights"],
            "proposed_position": row["proposed_change"],
            "net_effect": row["net_effect"],
        }
        for row in recommendation_debug
    ]
    write_json(output / "shared_claim_consumer_debug.json", shared_debug)
    write_json(output / "cross_review_consistency_debug.json", cross_debug)
    write_json(output / "document_precedence_debug.json", {
        "first_broken_layer": "Claim Construction / Evidence Assembly",
        "root_cause": "The precedence list was split after an annex-labelled line, so Common and Framework reviews consumed incomplete evidence paths.",
        "claim": document_precedence,
        "review_results": {review_id: items[review_id] for review_id in ("S-12-04", "FS-14")},
    })
    write_json(output / "default_law_provenance_debug.json", law_debug)
    write_json(output / "effective_protection_debug.json", effective_protection)
    write_json(output / "recommendation_effect_debug.json", recommendation_debug)
    write_json(output / "sale_hb_004_freeze_hotfix.json", {
        "report_ready": hb4["release_quality_gate"]["status"] == "REPORT_READY",
        "domain_selection": hb4["domain_selection_resolution"], "perspective": hb4["perspective_resolution"],
        "acceptance": acceptance, "counts": counts,
    })
    write_json(output / "final_regression_summary.json", {
        "contract_review_6_7": "PASS" if frozen else "FAIL", "acceptance": acceptance,
        "counts": counts, "cases": case_summary, "source_hashes": source_hashes,
        "sale_hb_004_frozen": frozen, "candidate_frozen": frozen,
        "candidate_hash": candidate_hash, "next_blind_status": "READY" if frozen else "NOT_READY",
        "next_blind": "SALE-BLIND-005",
    })
    (output / "6_7_freeze_hotfix_root_cause.md").write_text(
        "# Quality 6.7 Final Freeze Hotfix Root Cause\n\n"
        "The document-precedence list crossed a parser block boundary created by an annex-labelled list item. "
        "FS-14 consumed the Commercial Fact path while S-12-04 independently assembled incomplete evidence. "
        "The hotfix constructs one canonical document.precedence Claim, binds both reviews to semantic child elements, "
        "validates Default Law authority freshness before risk reduction, propagates relied-on authorities into production, "
        "and withholds recommendations that degrade the buyer's effective protection.\n",
        encoding="utf-8",
    )

    lines = ["CONTRACT_REVIEW_6_7 = " + ("PASS" if frozen else "FAIL"), ""]
    lines.extend(f"{name} = {'PASS' if acceptance[name] else 'FAIL'}" for name in gate_names)
    lines.append("")
    lines.extend(f"{name} = {'PASS' if acceptance[name] else 'FAIL'}" for name in (*paths.keys(), "REAL_PRODUCTION_INTEGRATION"))
    lines.append("")
    lines.extend(f"{name} = {value}" for name, value in counts.items())
    lines.extend(["", f"SALE_HB_004_FROZEN = {str(frozen).lower()}", f"CANDIDATE_FROZEN = {str(frozen).lower()}", "", f"CANDIDATE_HASH = {candidate_hash}", "", f"NEXT_BLIND_STATUS = {'READY' if frozen else 'NOT_READY'}", "NEXT_BLIND = SALE-BLIND-005"])
    print("\n".join(lines))
    return 0 if frozen else 1


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
