"""Production freeze acceptance for Quality 6.7 Freeze Closure Patch."""

from __future__ import annotations

import asyncio
import json
import sys
from pathlib import Path
from typing import Any, Dict


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "backend"))

from scripts.run_quality6_7_final_release_hotfix import digest, export_docx, git_commit, review, write_json


async def main() -> int:
    output = ROOT / "output" / "quality6_7_freeze_closure"
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
    observability = hb4["observability"]
    release_gates = hb4["release_quality_gate"].get("gate_results", {})
    legal_default = hb4["legal_default_law_consistency_gate"]
    semantics = hb4["not_applicable_gap_gate"]
    recommendation_renderer = hb4["recommendation_single_source_gate"]
    recommendation_impact = hb4["recommendation_non_degradation_gate"]
    legal_authority = hb4["legal_authority_gate"]
    default_provenance = hb4["default_law_provenance_gate"]
    cross_review = hb4["cross_review_shared_claim_gate"]
    items = {item["item_id"]: item for item in hb4["items"]}

    export_bytes = export_docx(hb4, paths["SALE_HB_004"].name)
    (output / "sale_hb_004_report.docx").write_bytes(export_bytes)

    gate_names = (
        "LEGAL_DEFAULT_LAW_CONSISTENCY_GATE", "ATOMIC_LEGAL_ELEMENT_GATE",
        "NOT_APPLICABLE_NARRATIVE_GATE", "NOT_APPLICABLE_GAP_GATE",
        "REVIEW_POLARITY_NARRATIVE_GATE", "NEGATIVE_CHECK_PASS_GATE",
        "RECOMMENDATION_SINGLE_SOURCE_GATE", "RECOMMENDATION_CROSS_RENDERER_CONSISTENCY_GATE",
        "RECOMMENDATION_NON_DEGRADATION_GATE", "LEGAL_AUTHORITY_DEDUP_GATE",
        "LEGAL_AUTHORITY_SELECTION_GATE", "CITATION_ENTAILMENT_GATE", "DEFAULT_LAW_PROVENANCE_GATE",
        "CROSS_REVIEW_SHARED_CLAIM_GATE", "FALSE_RISK_EXISTENCE_GATE", "NARRATIVE_TRUTH_GATE",
    )
    acceptance = {name: release_gates.get(name) == "PASS" for name in gate_names}
    for name, result in results.items():
        acceptance[name] = result["release_quality_gate"]["status"] == "REPORT_READY"
    acceptance["REAL_PRODUCTION_INTEGRATION"] = (
        all(result.get("success") for result in results.values())
        and export_bytes.startswith(b"PK") and len(export_bytes) > 1000
    )

    counts = {
        "LEGAL_DEFAULT_LAW_CONTRADICTION_COUNT": legal_default.get("contradiction_count", 0),
        "COMPOSITE_LEGAL_ELEMENT_ERROR_COUNT": legal_default.get("composite_error_count", 0),
        "NOT_APPLICABLE_GAP_NARRATIVE_COUNT": semantics.get("not_applicable_gap_narrative_count", 0),
        "NOT_APPLICABLE_FINDING_COUNT": semantics.get("not_applicable_finding_count", 0),
        "NOT_APPLICABLE_RECOMMENDATION_COUNT": semantics.get("not_applicable_recommendation_count", 0),
        "NEGATIVE_REVIEW_POSITIVE_NARRATIVE_COUNT": semantics.get("negative_review_positive_narrative_count", 0),
        "NEGATIVE_CHECK_FALSE_PASS_COUNT": semantics.get("negative_check_false_pass_count", 0),
        "RECOMMENDATION_DUAL_SOURCE_COUNT": recommendation_renderer.get("dual_source_count", 0),
        "RECOMMENDATION_CROSS_RENDERER_MISMATCH_COUNT": recommendation_renderer.get("cross_renderer_mismatch_count", 0),
        "ADVERSE_RECOMMENDATION_COUNT": recommendation_impact.get("adverse_recommendation_count", 0),
        "LEGAL_AUTHORITY_DUPLICATE_COUNT": legal_authority.get("duplicate_count", 0),
        "LEGAL_PROVENANCE_BREAK_COUNT": default_provenance.get("break_count", 0),
        "MATERIAL_CITATION_NOT_SUPPORT_COUNT": legal_authority.get("material_citation_not_support_count", 0),
        "CROSS_REVIEW_SHARED_CLAIM_CONTRADICTION_COUNT": cross_review.get("contradiction_count", 0),
        "NARRATIVE_CONTRADICTION_COUNT": sum(
            1 for row in observability["narrative_state_debug_report"] if row.get("status") != "PASS"
        ),
    }
    hb4_invariants = (
        hb4["contract_context"].get("contract_family") == "SALE"
        and hb4["contract_context"].get("subject_matter") == "GOODS"
        and hb4["contract_context"].get("transaction_structure") == "FRAMEWORK_SUPPLY"
        and hb4["perspective_resolution"].get("canonical_role") == "BUYER"
        and items["S-12-04"]["coverage_status"] in {"通过", "部分覆盖"}
        and items["FS-14"]["coverage_status"] in {"通过", "部分覆盖"}
        and items["S-08-03"]["decision_trace"]["default_law_assessment"]["status"] == "PARTIAL_DEFAULT"
        and items["S-02-05"]["narrative_state"]["judgment"].startswith("未发现")
        and items["S-08-04"]["narrative_state"]["judgment"].startswith("未发现")
    )
    frozen = all(acceptance.values()) and all(value == 0 for value in counts.values()) and hb4_invariants

    source_paths = (
        ROOT / "backend/review_v2/engine.py", ROOT / "backend/review_v2/house_lease_checklist.py",
        ROOT / "backend/review_v2/sale_contract_checklist.py", ROOT / "backend/review_v2/common_sale.py",
        ROOT / "backend/review_v2/domain_packs.py", ROOT / "backend/review_v2/ARCHITECTURE_NOTES.md",
        ROOT / "backend/tests/test_quality6_7_freeze_closure.py",
        ROOT / "scripts/run_quality6_7_freeze_closure.py",
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
        "system_version": "contract-review-quality-6.7-freeze-closure",
        "git_commit": git_commit(), "model_version": "qwen-doubao-cloud-fallback",
        "prompt_version": "quality-6.7-freeze-closure",
        "parser_version": "frozen-6.7", "domain_version": "frozen-6.7",
        "perspective_version": "frozen-6.7", "fact_graph_version": "frozen-6.7",
        "claim_graph_version": "frozen-6.7", "review_registry_version": "frozen-6.7",
        "review_polarity_version": "review-polarity-6.7-closure-1",
        "legal_proposition_version": "resolved-legal-proposition-6.7-closure-1",
        "default_law_version": "default-law-6.7-closure-1",
        "narrative_semantics_version": "narrative-semantics-6.7-closure-1",
        "regression_version": "freeze-closure-1",
    }
    candidate_hash = digest({
        "manifest": manifest, "source_hashes": source_hashes,
        "acceptance": acceptance, "counts": counts, "cases": case_summary,
    })
    manifest["candidate_hash"] = candidate_hash

    write_json(output / "legal_default_consistency_debug.json", legal_default)
    write_json(output / "legal_element_decomposition_debug.json", legal_default.get("element_decomposition", []))
    write_json(output / "not_applicable_pipeline_debug.json", semantics.get("not_applicable_rows", []))
    write_json(output / "review_polarity_debug.json", semantics.get("polarity_rows", []))
    write_json(output / "negative_check_debug.json", [
        row.get("evidence_state") for row in semantics.get("polarity_rows", [])
    ])
    write_json(output / "narrative_semantics_debug.json", semantics)
    write_json(output / "sale_hb_004_freeze_closure.json", {
        "report_ready": hb4["release_quality_gate"]["status"] == "REPORT_READY",
        "acceptance": acceptance, "counts": counts, "hb4_invariants": hb4_invariants,
        "s_08_03": items["S-08-03"], "s_02_05": items["S-02-05"],
        "s_08_04": items["S-08-04"],
    })
    write_json(output / "final_regression_summary.json", {
        "contract_review_6_7": "PASS" if frozen else "FAIL", "acceptance": acceptance,
        "counts": counts, "cases": case_summary, "candidate_manifest": manifest,
        "source_hashes": source_hashes, "sale_hb_004_frozen": frozen,
        "candidate_frozen": frozen, "candidate_hash": candidate_hash,
        "next_blind_status": "READY" if frozen else "NOT_READY", "next_blind": "SALE-BLIND-005",
    })
    (output / "6_7_freeze_closure_root_cause.md").write_text(
        "# Quality 6.7 Freeze Closure Root Cause\n\n"
        "Default Law and Legal Authority previously evaluated related text through separate semantic paths. "
        "Composite coverage elements could therefore hide a supported legal boundary behind an unrelated evidentiary gap. "
        "NOT_APPLICABLE reviews also continued through the generic gap narrative, while PASS was rendered as contractual "
        "presence even for negative-clause checks.\n\n"
        "The closure patch records atomic legal elements and supplied element IDs on resolved default rules, stops the gap "
        "path at Applicability, and makes ReviewPolarity part of NarrativeState. Six fail-closed gates verify these truths "
        "before release without changing Domain, Fact, Claim, Finding aggregation, Severity, Priority, or Recommendation SSOT.\n",
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
        f"CANDIDATE_FROZEN = {str(frozen).lower()}", "", f"CANDIDATE_HASH = {candidate_hash}", "",
        f"NEXT_BLIND_STATUS = {'READY' if frozen else 'NOT_READY'}", "NEXT_BLIND = SALE-BLIND-005",
    ])
    print("\n".join(lines))
    return 0 if frozen else 1


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
