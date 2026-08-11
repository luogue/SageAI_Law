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


def count(text: str, needle: str) -> int:
    return (text or "").count(needle)


def money_number(value: Any) -> float | None:
    match = re.search(r"\d+(?:\.\d+)?", str(value))
    return float(match.group(0)) if match else None


def row(requirement: str, expected: Any, actual: Any, ok: bool) -> Dict[str, Any]:
    return {"requirement": requirement, "expected": expected, "actual": actual, "status": "PASS" if ok else "FAIL"}


def p0_checks(lease: Dict[str, Any], sale: Dict[str, Any]) -> List[Dict[str, Any]]:
    by_id = {item["item_id"]: item for item in lease["items"]}
    findings = lease["risk_findings"]
    markdown = lease["result"]
    facts = lease["contract_facts"]
    cases = {case["remaining_days"]: case for case in by_id["HL-039"]["scenario_analysis"]["cases"]}
    pass_without_finding = [
        item for item in lease["items"]
        if item["coverage_status"] == "通过" and not item.get("related_risks")
    ]
    hl005_claims = [claim for claim in by_id["HL-005"].get("legal_references", []) if claim.get("article") == "第188条"]
    a_core_findings = [finding for finding in findings if finding["priority"] == "A_CORE"]
    engineering_terms = [
        "LLM_PRIORITY",
        "用户风险偏好已纳入后续优先级排序",
        "Scenario Engine",
        "统一事实图谱",
        "early_termination.penalty_formula",
        "RF-",
        "建议继续核对表述是否具体、附件是否完整、责任边界是否清楚",
    ]
    summary_total = sum(lease["risk_finding_summary"].get(key, 0) for key in ("重大风险", "中等风险", "低风险"))

    return [
        row("ReviewImportance separation", "HL-001 CORE and action NONE", {"review_importance": by_id["HL-001"]["review_importance"], "action_priority": by_id["HL-001"]["action_priority"]}, by_id["HL-001"]["review_importance"] == "CORE" and by_id["HL-001"]["action_priority"] == "NONE"),
        row("ActionPriority consistency", "PASS + no Finding => NONE", sorted({item["action_priority"] for item in pass_without_finding}), all(item["action_priority"] == "NONE" for item in pass_without_finding)),
        row("core risk count consistency", "no ambiguous core count; severity counts equal unique findings", {"has_core_risk_count_text": "核心风险数量" in markdown, "summary_total": summary_total, "finding_count": len(findings)}, "核心风险数量" not in markdown and summary_total == len(findings)),
        row("Legal Freshness", "OUTDATED_REFERENCE", [issue["status"] for issue in lease["legal_reference_issues"]], any(issue["status"] == "OUTDATED_REFERENCE" for issue in lease["legal_reference_issues"])),
        row("Citation Entailment", "HL-005 第188条 BACKGROUND_ONLY", [claim.get("support_type") for claim in hl005_claims], bool(hl005_claims) and all(claim.get("support_type") == "BACKGROUND_ONLY" for claim in hl005_claims)),
        row("Evidence source type", "source_document_type populated", sum(1 for item in lease["items"] for evidence in item.get("evidence_clauses", []) if evidence.get("source_document_type")), all(evidence.get("source_document_type") for item in lease["items"] for evidence in item.get("evidence_clauses", []))),
        row("sentence-level critical evidence", "all A_CORE findings have quote", [finding["title"] for finding in a_core_findings], all(any(evidence.get("quote") and evidence.get("sentence_index") for evidence in finding.get("evidence", [])) for finding in a_core_findings)),
        row("dynamic section numbering", "manual hidden => 完整审查明细 is 六", {"manual_count": lease["overall_assessment"]["manual_review_count"], "has_six": "## 六、完整审查明细" in markdown, "has_seven": "## 七、完整审查明细" in markdown}, lease["overall_assessment"]["manual_review_count"] == 0 and "## 六、完整审查明细" in markdown and "## 七、完整审查明细" not in markdown),
        row("PASS wording", "PASS no finding and PASS with finding separated", {"HL-001": by_id["HL-001"]["action_suggestion"], "HL-029": by_id["HL-029"]["action_suggestion"]}, by_id["HL-001"]["action_suggestion"] == "已覆盖，无需修改" and "关联风险" in by_id["HL-029"]["action_suggestion"]),
        row("manual review consistency", "0 false manual review text", count(markdown, "建议人工复核"), lease["overall_assessment"]["manual_review_count"] != 0 or count(markdown, "建议人工复核") == 0),
        row("engineering text zero", "all forbidden terms count 0", {term: count(markdown, term) for term in engineering_terms}, all(count(markdown, term) == 0 for term in engineering_terms)),
        row("rent regression", "facts and calculation locked", {"monthly": facts["rent"]["monthly_amount"], "due_day": facts["rent"]["payment_due_day"], "formula": facts["early_termination"]["penalty_formula"]["type"], "cases": [cases[d]["estimated_penalty"] for d in (30, 90, 180, 300)]}, money_number(facts["rent"]["monthly_amount"]) == 3852 and str(facts["rent"]["payment_due_day"]) == "5" and facts["early_termination"]["penalty_formula"]["type"] == "remaining_term_rent_multiplier" and [cases[d]["estimated_penalty"] for d in (30, 90, 180, 300)] == [7704, 23112, 46224, 77040]),
        row("cement regression", "sale release gate ready", (sale.get("release_quality_gate") or {}).get("status"), sale.get("success") and (sale.get("release_quality_gate") or {}).get("status") == "REPORT_READY"),
    ]


async def main() -> None:
    test_data = ROOT / "test_data"
    output_dir = ROOT / "output"
    output_dir.mkdir(exist_ok=True)

    lease = await run_file(next(test_data.glob("1*.docx")), "house_lease")
    sale = await run_file(next(test_data.glob("2*.docx")), "sale")
    checks = p0_checks(lease, sale)
    status = "PASS" if all(check["status"] == "PASS" for check in checks) else "FAIL"
    blind_status = "READY" if status == "PASS" else "NOT_READY"
    payload = {
        "status": status,
        "blind_benchmark_status": blind_status,
        "checks": checks,
        "notes": "Blind Benchmark is READY only as infrastructure/readiness. No blind pass is claimed without unseen contracts and private expert Gold.",
    }
    write_json(output_dir / "quality5_p0_acceptance.json", payload)
    lines = [
        "# Quality 5.0 P0 Acceptance",
        "",
        f"Status: {status}",
        f"Blind Benchmark Status: {blind_status}",
        "",
        "| Requirement | Expected | Actual | PASS/FAIL |",
        "| --- | --- | --- | --- |",
    ]
    for check in checks:
        lines.append(f"| {check['requirement']} | {check['expected']} | {check['actual']} | {check['status']} |")
    (output_dir / "quality5_p0_acceptance.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({"status": status, "blind_benchmark_status": blind_status, "failures": [check for check in checks if check["status"] == "FAIL"]}, ensure_ascii=False))


if __name__ == "__main__":
    asyncio.run(main())
