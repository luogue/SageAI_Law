from __future__ import annotations

import asyncio
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

from routers.review_v2 import ReviewV2PdfInput, _build_docx, _build_pdf, review_v2_file  # noqa: E402


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


def write_json(path: Path, data: Any) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def export_payload(output: Dict[str, Any]) -> ReviewV2PdfInput:
    return ReviewV2PdfInput(
        filename=output.get("filename") or "contract_review.docx",
        contract_type_name=output.get("contract_type_name"),
        result=output.get("result"),
        risk_finding_summary=output.get("risk_finding_summary"),
        risk_findings=output.get("risk_findings"),
        recommendations=output.get("recommendations"),
        overall_assessment=output.get("overall_assessment"),
        release_quality_gate=output.get("release_quality_gate"),
        quality4_gate=output.get("quality4_gate"),
        items=output.get("items"),
    )


def count(text: str, needle: str) -> int:
    return (text or "").count(needle)


def number(value: Any) -> float | None:
    match = re.search(r"\d+(?:\.\d+)?", str(value))
    return float(match.group(0)) if match else None


def row(requirement: str, expected: Any, actual: Any, ok: bool, failure_stage: str) -> Dict[str, Any]:
    return {
        "requirement": requirement,
        "expected": expected,
        "actual": actual,
        "status": "PASS" if ok else "FAIL",
        "failure_stage": "" if ok else failure_stage,
    }


def hard_checks(lease: Dict[str, Any], sale: Dict[str, Any]) -> List[Dict[str, Any]]:
    by_id = {item["item_id"]: item for item in lease["items"]}
    facts = lease["contract_facts"]
    markdown = lease["result"]
    findings = lease["risk_findings"]
    cases = {case["remaining_days"]: case for case in by_id["HL-039"]["scenario_analysis"]["cases"]}
    early = next((finding for finding in findings if finding["risk_group"] == "early_termination_financial_exposure"), {})
    summary_total = sum(lease["risk_finding_summary"].get(key, 0) for key in ("重大风险", "中等风险", "低风险"))
    legal_trace = lease["observability"]["legal_freshness_trace"]

    return [
        row("HL-015 PASS", "通过", by_id["HL-015"]["coverage_status"], by_id["HL-015"]["coverage_status"] == "通过", "ReviewResult"),
        row("HL-030 N/A", "不适用", by_id["HL-030"]["coverage_status"], by_id["HL-030"]["coverage_status"] == "不适用", "Applicability"),
        row("payment due day = 5", 5, facts["rent"]["payment_due_day"], str(facts["rent"]["payment_due_day"]) == "5", "Fact Extraction"),
        row("monthly rent = 3852", 3852, facts["rent"]["monthly_amount"], number(facts["rent"]["monthly_amount"]) == 3852, "Fact Extraction"),
        row("remaining-term x2", "remaining_term_rent_multiplier", facts["early_termination"]["penalty_formula"]["type"], facts["early_termination"]["penalty_formula"]["type"] == "remaining_term_rent_multiplier", "Formula Parser"),
        row("30/90/180/300 correct", "7704/23112/46224/77040", [cases[days]["estimated_penalty"] for days in (30, 90, 180, 300)], [cases[days]["estimated_penalty"] for days in (30, 90, 180, 300)] == [7704, 23112, 46224, 77040], "Scenario Calculation"),
        row(
            "HL-040 protected",
            "not mortgage entailment",
            {"coverage": by_id["HL-040"]["coverage_status"], "entailment": by_id["HL-040"].get("semantic_entailment"), "evidence": by_id["HL-040"].get("evidence_clauses")},
            by_id["HL-040"]["coverage_status"] != "通过"
            and not any(
                any(term in ((clause.get("text") or "") + (clause.get("quote") or "")) for term in ("抵押", "贷款", "产权"))
                for clause in by_id["HL-040"].get("evidence_clauses", [])
            ),
            "Evidence Entailment",
        ),
        row("HL-043 reasonable severity", "not high", by_id["HL-043"]["risk_level"], by_id["HL-043"]["risk_level"] != "高", "Severity"),
        row("PASS old noise = 0", 0, count(markdown, "建议继续核对表述是否具体"), count(markdown, "建议继续核对表述是否具体") == 0, "Post-render Gate"),
        row("Top Risk Summary present", True, "核心风险摘要" in markdown, "核心风险摘要" in markdown, "Production Renderer"),
        row("Priority section present", True, "建议优先修改" in markdown, "建议优先修改" in markdown, "Production Renderer"),
        row("Optimization section present", True, "可选优化事项" in markdown, "可选优化事项" in markdown, "Production Renderer"),
        row("Covered section present", True, "已覆盖关键事项" in markdown, "已覆盖关键事项" in markdown, "Production Renderer"),
        row("Contract Law outdated detected", True, any(issue["status"] == "OUTDATED_REFERENCE" for issue in lease["legal_reference_issues"]), any(issue["status"] == "OUTDATED_REFERENCE" for issue in lease["legal_reference_issues"]), "Legal Freshness"),
        row("legal reference finding present", True, any(finding["risk_group"] == "legal_reference" and finding["title"] == "法律引用建议更新" for finding in findings), any(finding["risk_group"] == "legal_reference" and finding["title"] == "法律引用建议更新" for finding in findings), "Risk Aggregator"),
        row("manual review mismatch = 0", 0, count(markdown, "建议人工复核") if lease["overall_assessment"]["manual_review_count"] == 0 else "manual exists", lease["overall_assessment"]["manual_review_count"] != 0 or count(markdown, "建议人工复核") == 0, "Manual Review Aggregator"),
        row("risk preference text = 0", 0, count(markdown, "用户风险偏好已纳入后续优先级排序"), count(markdown, "用户风险偏好已纳入后续优先级排序") == 0, "Production Renderer"),
        row("LLM_PRIORITY = 0", 0, count(markdown, "LLM_PRIORITY"), count(markdown, "LLM_PRIORITY") == 0, "Production Renderer"),
        row("raw formula dict = 0", 0, count(markdown, "early_termination.penalty_formula") + count(markdown, "{'type'") + count(markdown, '{"type"'), count(markdown, "early_termination.penalty_formula") + count(markdown, "{'type'") + count(markdown, '{"type"') == 0, "Production Renderer"),
        row("internal RF ID = 0", 0, count(markdown, "RF-"), count(markdown, "RF-") == 0, "Production Renderer"),
        row("many-to-one finding works", True, set(early.get("source_review_ids", [])) >= {"HL-029", "HL-039"}, set(early.get("source_review_ids", [])) >= {"HL-029", "HL-039"}, "Risk Aggregator"),
        row("semantic aggregation separates HL-042", True, "HL-042" not in set(early.get("source_review_ids", [])), "HL-042" not in set(early.get("source_review_ids", [])), "Risk Aggregator"),
        row("risk statistics use unique findings", len(findings), summary_total, summary_total == len(findings), "Risk Aggregator"),
        row("rent regression pass", "REPORT_READY", lease["release_quality_gate"]["status"], lease["release_quality_gate"]["status"] == "REPORT_READY" and lease["quality4_gate"]["status"] == "REPORT_READY", "Production Integration"),
        row("cement regression pass", "REPORT_READY", sale["release_quality_gate"]["status"], sale["success"] and sale["release_quality_gate"]["status"] == "REPORT_READY", "Multi-contract Regression"),
        row("real production integration pass", True, bool(lease["filename"] and lease["extracted_text_length"] and legal_trace["called"]), bool(lease["filename"] and lease["extracted_text_length"] and legal_trace["called"]), "Production Entry"),
    ]


async def main() -> None:
    output_dir = ROOT / "output"
    output_dir.mkdir(exist_ok=True)
    test_data = ROOT / "test_data"

    lease = await run_file(next(test_data.glob("1*.docx")), "house_lease")
    sale = await run_file(next(test_data.glob("2*.docx")), "sale")

    (output_dir / "production_closure_lease_report.md").write_text(lease["result"], encoding="utf-8")
    (output_dir / "production_closure_sale_report.md").write_text(sale["result"], encoding="utf-8")
    write_json(output_dir / "production_closure_lease_result.json", lease)
    write_json(output_dir / "production_closure_sale_result.json", sale)
    (output_dir / "production_closure_lease_report.docx").write_bytes(_build_docx(export_payload(lease)))
    (output_dir / "production_closure_lease_report.pdf").write_bytes(_build_pdf(export_payload(lease)))

    acceptance = {
        "status": "PASS",
        "production_entry": "backend/routers/review_v2.py:review_v2_file",
        "final_markdown_serializer": "backend/review_v2/engine.py:_format_markdown_v2",
        "export_renderer": "backend/routers/review_v2.py:_build_pdf/_build_docx",
        "checks": hard_checks(lease, sale),
        "production_call_graph": lease["observability"]["production_call_graph"],
        "final_output_ownership_matrix": lease["observability"]["final_output_ownership_matrix"],
        "risk_aggregation_debug_table": lease["observability"]["risk_aggregation_debug_table"],
        "legal_freshness_trace": lease["observability"]["legal_freshness_trace"],
    }
    if any(check["status"] == "FAIL" for check in acceptance["checks"]):
        acceptance["status"] = "FAIL"

    write_json(output_dir / "production_closure_acceptance.json", acceptance)
    lines = [
        "# Production Closure Acceptance",
        "",
        f"Status: {acceptance['status']}",
        "",
        "| Requirement | Expected | Actual | PASS/FAIL | Failure Stage |",
        "| --- | --- | --- | --- | --- |",
    ]
    for check in acceptance["checks"]:
        lines.append(f"| {check['requirement']} | {check['expected']} | {check['actual']} | {check['status']} | {check['failure_stage']} |")
    (output_dir / "production_closure_acceptance.md").write_text("\n".join(lines), encoding="utf-8")

    print(json.dumps({"status": acceptance["status"], "checks": len(acceptance["checks"]), "failures": [check for check in acceptance["checks"] if check["status"] == "FAIL"]}, ensure_ascii=False))


if __name__ == "__main__":
    asyncio.run(main())
