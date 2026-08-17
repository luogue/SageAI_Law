from __future__ import annotations

import asyncio
import hashlib
import io
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List


ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"
if str(BACKEND) not in sys.path:
    sys.path.insert(0, str(BACKEND))

from routers.review_v2 import review_v2_file  # noqa: E402


class UploadFile:
    def __init__(self, path: Path):
        self.filename = path.name
        self.file = io.BytesIO(path.read_bytes())


async def run_file(path: Path, contract_type: str) -> Dict[str, Any]:
    return await review_v2_file(
        file=UploadFile(path),
        contract_type=contract_type,
        include_low_risk=True,
        use_llm=False,
        profile_json="{}",
        current_user={"id": 1},
    )


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def by_id(report: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    return {item["item_id"]: item for item in report.get("items", [])}


def number(value: Any) -> float | None:
    match = re.search(r"\d+(?:\.\d+)?", str(value))
    return float(match.group(0)) if match else None


def row(requirement: str, expected: Any, actual: Any, ok: bool) -> Dict[str, Any]:
    return {"requirement": requirement, "expected": expected, "actual": actual, "status": "PASS" if ok else "FAIL"}


def finding_for(report: Dict[str, Any], review_id: str) -> Dict[str, Any]:
    return next(finding for finding in report.get("risk_findings", []) if review_id in finding.get("source_review_ids", []))


def p0_checks(lease: Dict[str, Any], sale: Dict[str, Any]) -> List[Dict[str, Any]]:
    items = by_id(lease)
    facts = lease["contract_facts"]
    markdown = lease["result"]
    confidence_distribution = lease["observability"]["confidence_distribution"]
    confidence_rows = lease["observability"]["confidence_debug_report"]
    coverage_rows = lease["observability"]["coverage_element_debug_report"]
    provenance_rows = lease["observability"]["recommendation_provenance_debug_report"]
    narrative_rows = lease["observability"]["narrative_state_debug_report"]
    hl007 = items["HL-007"]
    hl008 = items["HL-008"]
    hl013 = items["HL-013"]
    hl037 = items["HL-037"]
    hl039 = items["HL-039"]
    hl040 = items["HL-040"]
    hl042 = items["HL-042"]
    hl043 = items["HL-043"]
    early = finding_for(lease, "HL-039")
    cases = {case["remaining_days"]: case for case in hl039["scenario_analysis"]["cases"]}
    forbidden_engineering = ("LLM_PRIORITY", "DIRECT_SUPPORT", "PARTIAL_SUPPORT", "BACKGROUND_ONLY", "RF-", "Scenario Engine", "Fact Graph", "统一事实图谱", "系统确定性")
    missing_bad_sections = []
    for item in lease["items"]:
        if item["coverage_status"] != "缺失":
            continue
        marker = f"（{item['item_id']}）"
        if marker not in markdown:
            continue
        section = markdown.split(marker, 1)[1].split("---", 1)[0]
        if any(term in section for term in ("已出现", "尚未完整覆盖", "已覆盖部分内容")):
            missing_bad_sections.append(item["item_id"])
    partial_without_element = [
        item["item_id"]
        for item in lease["items"]
        if item["coverage_status"] == "部分覆盖"
        and not any(element.get("status") in {"COVERED", "PARTIALLY_COVERED"} for element in item.get("coverage_elements", []))
    ]
    statutory_components = [row_ for row_ in provenance_rows if row_.get("source_type") in {"STATUTORY_RULE", "STATUTORY_DEFAULT"}]
    drafting_components = [row_ for row_ in provenance_rows if row_.get("source_type") in {"DRAFTING_CHOICE", "RISK_MITIGATION", "PRACTICAL_GUIDANCE"}]

    return [
        row("Confidence Calibration Gate", "not 50/50 HIGH, no forced distribution", confidence_distribution, confidence_distribution.get("high", 0) < 50 and sum(confidence_distribution.values()) == 50),
        row("Confidence Bundle verifier component", "all rows include verifier and reason", confidence_rows[:3], len(confidence_rows) == 50 and all("verifier" in row_["required_components"] and row_.get("reason") for row_ in confidence_rows)),
        row("Weak related evidence blocked", "HL-007 missing, no expiry renewal coverage", hl007["coverage_elements"], hl007["coverage_status"] == "缺失" and all(element["status"] == "MISSING" for element in hl007["coverage_elements"])),
        row("Default Law separated from Contract Coverage", "HL-007 clear default does not lift coverage", {"coverage": hl007["coverage_status"], "default": hl007["decision_trace"].get("default_law_status"), "priority": hl007["action_priority"]}, hl007["coverage_status"] == "缺失" and hl007["decision_trace"].get("default_law_status") == "CLEAR_DEFAULT" and hl007["action_priority"] == "C_OPTIMIZATION"),
        row("PARTIAL requires element evidence", "no partial without covered element", partial_without_element, not partial_without_element),
        row("Weak partial not HIGH", "HL-043 partial has medium confidence", hl043["system_confidence"], hl043["coverage_status"] == "部分覆盖" and hl043["system_confidence"]["level"] == "medium"),
        row("MISSING can be calibrated HIGH", "HL-042 missing + negative search high/medium", hl042["system_confidence"], hl042["coverage_status"] == "缺失" and hl042["decision_trace"]["negative_evidence"]["result"] == "NOT_FOUND" and hl042["system_confidence"]["level"] in {"high", "medium"}),
        row("Repair cost weak evidence rejected", "HL-037 no penalty article and no weak pass", {"coverage": hl037["coverage_status"], "claims": hl037["legal_references"]}, hl037["coverage_status"] == "缺失" and all(claim.get("article") != "第585条" for claim in hl037["legal_references"])),
        row("Legal/Drafting Provenance Gate", "statutory and drafting components separated", provenance_rows[:6], bool(statutory_components) and bool(drafting_components) and lease["observability"]["recommendation_provenance_gate"]["status"] == "PASS"),
        row("30-day drafting not statutory", "no legal 30-day wording", {"法定30": "法定30" in markdown, "强制30": "强制30" in markdown}, "法定30" not in markdown and "强制30" not in markdown),
        row("No cross-claim citation propagation", "HL-008 no Article 732 direct", hl008["legal_references"], all(claim.get("article") != "第732条" and not claim.get("authority_links") for claim in hl008["legal_references"])),
        row("Rental hard regression", "facts/fixed gates/formula/scenarios", {"rent": facts["rent"], "HL015": items["HL-015"]["coverage_status"], "HL030": items["HL-030"]["coverage_status"], "cases": [cases[d]["estimated_penalty"] for d in (30, 90, 180, 300)]}, number(facts["rent"]["monthly_amount"]) == 3852 and str(facts["rent"]["payment_due_day"]) == "5" and items["HL-015"]["coverage_status"] == "通过" and items["HL-030"]["coverage_status"] == "不适用" and facts["early_termination"]["penalty_formula"]["type"] == "remaining_term_rent_multiplier" and [number(cases[d]["estimated_penalty"]) for d in (30, 90, 180, 300)] == [7704, 23112, 46224, 77040]),
        row("Early termination priority frozen", "EconomicImpact HIGH + A_CORE", {"impact": hl039["economic_impact"], "item": hl039["action_priority"], "finding": early["priority"]}, hl039["economic_impact"] == "high" and hl039["action_priority"] == "A_CORE" and early["priority"] == "A_CORE"),
        row("HL-040 semantic protection", "not pass", hl040["coverage_status"], hl040["coverage_status"] != "通过"),
        row("HL-043 not over-upgraded", "not high risk", hl043["risk_level"], hl043["risk_level"] != "高"),
        row("Legal Freshness pass", "outdated Contract Law detected", lease["legal_reference_issues"], any(issue.get("status") == "OUTDATED_REFERENCE" for issue in lease["legal_reference_issues"])),
        row("Narrative invariants pass", "missing safe and no repeated low-prob sentence", {"missing_bad_sections": missing_bad_sections}, not missing_bad_sections and all(item["status"] == "PASS" for item in narrative_rows) and "该项属于低概率完善项。该项属于低概率完善项" not in markdown),
        row("Production internal fields zero", "internal terms hidden", {term: markdown.count(term) for term in forbidden_engineering}, all(term not in markdown for term in forbidden_engineering)),
        row("Manual review invariant", "0 count means no text", lease["overall_assessment"], lease["overall_assessment"]["manual_review_count"] != 0 or "建议人工复核" not in markdown),
        row("Cement Regression", "sale release gate ready", sale.get("release_quality_gate"), sale.get("success") and (sale.get("release_quality_gate") or {}).get("status") == "REPORT_READY"),
        row("Real Production Integration", "quality gates ready and debug tables present", lease.get("quality4_gate"), lease.get("quality4_gate", {}).get("status") == "REPORT_READY" and bool(coverage_rows) and bool(provenance_rows)),
    ]


ROOT_CAUSE_ROWS = [
    {
        "Problem": "50/50 HIGH confidence",
        "Root Cause": "The 5.3 confidence aggregator treated not_checked or UNCERTAIN evidence as strong evidence, and averaging could keep final HIGH even when a required verifier component was LOW.",
        "File": "backend/review_v2/engine.py",
        "Function": "_confidence_bundle_for_item",
        "Fix": "Evidence confidence now distinguishes UNCERTAIN/RELATED evidence, adds verifier_confidence, and caps final confidence at MEDIUM when a required component is LOW.",
    },
    {
        "Problem": "Weak/related evidence contributing to PARTIAL",
        "Root Cause": "Coverage was previously produced before element-level entailment; strict evidence gating only covered a few review IDs.",
        "File": "backend/review_v2/engine.py",
        "Function": "_apply_coverage_evidence_gate",
        "Fix": "CoverageElementResult verifies required elements; RELATED_BUT_NOT_SUPPORTING contributes zero coverage and may downgrade PASS/PARTIAL to MISSING.",
    },
    {
        "Problem": "Statutory rule and drafting choice losing provenance",
        "Root Cause": "Recommendations aggregated natural-language advice without preserving source_type and legal claim lineage through rendering.",
        "File": "backend/review_v2/engine.py",
        "Function": "_recommendation_components_for_finding / _recommendation_component_lines",
        "Fix": "Recommendations now expose structured components with source_type, legal_claim_ids, statutory_basis and drafting_reason; production renders legal rules and drafting choices separately.",
    },
]


def frozen_snapshot(path: Path, report: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "source_file": str(path),
        "source_sha256": sha256(path),
        "system_version": (report.get("system_metadata") or {}).get("system_version"),
        "model_version": (report.get("system_metadata") or {}).get("model_version"),
        "prompt_version": (report.get("system_metadata") or {}).get("prompt_version"),
        "rule_version": (report.get("system_metadata") or {}).get("rule_version"),
        "ontology_version": (report.get("system_metadata") or {}).get("ontology_version"),
        "legal_dataset_version": (report.get("system_metadata") or {}).get("legal_dataset_version"),
        "canonical_facts": report.get("contract_facts"),
        "review_results": report.get("items"),
        "coverage_element_results": report.get("observability", {}).get("coverage_element_debug_report"),
        "risk_findings": report.get("risk_findings"),
        "recommendations": report.get("recommendations"),
        "legal_claims": report.get("legal_citation_claims"),
        "confidence_bundles": report.get("observability", {}).get("confidence_debug_report"),
        "final_markdown": report.get("result"),
    }


def markdown_table(rows: List[Dict[str, Any]], columns: List[str]) -> List[str]:
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join("---" for _ in columns) + " |"]
    for item in rows:
        lines.append("| " + " | ".join(str(item.get(column, "")).replace("\n", " ") for column in columns) + " |")
    return lines


async def main() -> None:
    test_data = ROOT / "test_data"
    output_dir = ROOT / "output"
    lease_path = next(test_data.glob("1*.docx"))
    sale_path = next(test_data.glob("2*.docx"))
    lease = await run_file(lease_path, "house_lease")
    sale = await run_file(sale_path, "sale")
    checks = p0_checks(lease, sale)
    status = "PASS" if all(check["status"] == "PASS" for check in checks) else "FAIL"
    payload = {
        "status": status,
        "P0_FINAL_CONVERGENCE": status == "PASS",
        "RENTAL_REGRESSION_FROZEN": status == "PASS",
        "BLIND_BENCHMARK_READY": status == "PASS",
        "confidence_distribution": lease["observability"]["confidence_distribution"],
        "checks": checks,
        "root_cause_report": ROOT_CAUSE_ROWS,
        "confidence_debug_report": lease["observability"]["confidence_debug_report"],
        "coverage_element_debug_report": lease["observability"]["coverage_element_debug_report"],
        "legal_drafting_provenance_report": lease["observability"]["recommendation_provenance_debug_report"],
        "legal_citation_debug_report": lease["observability"]["legal_claim_debug_report"],
        "narrative_state_debug_report": lease["observability"]["narrative_state_debug_report"],
        "notes": "Confidence distribution is observed only; it is not used to force calibration buckets.",
    }
    write_json(output_dir / "quality5_4_p0_acceptance.json", payload)
    write_json(output_dir / "frozen_regression_snapshot_quality5_4.json", frozen_snapshot(lease_path, lease))

    lines = [
        "# Contract Review Quality 5.4 P0 Acceptance",
        "",
        f"Status: {status}",
        f"P0_FINAL_CONVERGENCE = {status}",
        f"RENTAL_REGRESSION_FROZEN = {str(status == 'PASS').lower()}",
        f"BLIND_BENCHMARK_READY = {str(status == 'PASS').lower()}",
        f"Confidence Distribution = {lease['observability']['confidence_distribution']}",
        "",
        "## Final Acceptance Table",
        "",
        *markdown_table(checks, ["requirement", "expected", "actual", "status"]),
        "",
        "## Root Cause Report",
        "",
        *markdown_table(ROOT_CAUSE_ROWS, ["Problem", "Root Cause", "File", "Function", "Fix"]),
        "",
        "## Confidence Debug Table",
        "",
        *markdown_table(payload["confidence_debug_report"], ["review_id", "coverage", "parser", "fact", "evidence", "applicability", "legal", "formula", "calculation", "verifier", "final", "reason"]),
        "",
        "## Coverage Element Table",
        "",
        *markdown_table(payload["coverage_element_debug_report"], ["review_id", "coverage", "element_id", "proposition", "evidence_ids", "entailment", "element_status"]),
        "",
        "## Legal / Drafting Provenance Table",
        "",
        *markdown_table(payload["legal_drafting_provenance_report"], ["component", "source_type", "legal_claim_ids", "authority", "supported_scope"]),
    ]
    (output_dir / "quality5_4_p0_acceptance.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({"status": status, "blind_benchmark_ready": status == "PASS", "confidence_distribution": payload["confidence_distribution"], "failures": [check for check in checks if check["status"] == "FAIL"]}, ensure_ascii=False))


if __name__ == "__main__":
    asyncio.run(main())
