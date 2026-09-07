"""Compatibility tests for Word document extraction."""

import asyncio
import io
from pathlib import Path

from docx import Document
from layers.input_layer import InputLayer
from review_v2.clause_parser import parse_contract_clauses
from review_v2.engine import review_contract_v2
from routers.review_v2 import ReviewV2PdfInput, _build_docx, review_v2_file


class _UploadFile:
    def __init__(self, filename: str, content: bytes):
        self.filename = filename
        self.file = io.BytesIO(content)


HOUSE_LEASE_FIXTURE = Path(__file__).resolve().parents[2] / "test_data" / "1、租房合同.docx"


def test_extracts_legacy_word_file_renamed_as_docx():
    fixture = HOUSE_LEASE_FIXTURE
    upload = _UploadFile(fixture.name, fixture.read_bytes())

    text = InputLayer().extract_text_from_file(upload)

    assert len(text) > 100
    assert "上海市房屋租赁合同" in text
    assert "出租方" in text
    assert "承租方" in text
    assert "月租金的2倍" in text
    assert "产证编号" in text


def test_real_house_lease_review_uses_structured_clauses_and_practical_ratings():
    fixture = HOUSE_LEASE_FIXTURE
    upload = _UploadFile(fixture.name, fixture.read_bytes())
    text = InputLayer().extract_text_from_file(upload)

    clauses = parse_contract_clauses(text)
    assert any(clause.location == "九、第6项" and "逾期不支付租金累计超过 1 个月" in clause.text for clause in clauses)
    assert any(clause.location == "十、（六）" and "提前退租天数的租金的2倍" in clause.text for clause in clauses)

    output = review_contract_v2(text, "house_lease", include_low_risk=True, use_llm=False)
    by_id = {item["item_id"]: item for item in output["items"]}

    assert output["summary"]["高"] <= 2
    assert by_id["HL-005"]["coverage_status"] == "通过"
    assert by_id["HL-015"]["coverage_status"] == "通过"
    assert by_id["HL-010"]["risk_level"] == "中"
    assert by_id["HL-039"]["risk_level"] in {"中", "低"}
    assert by_id["HL-029"]["coverage_status"] == "通过"
    assert by_id["HL-030"]["coverage_status"] == "不适用"
    assert by_id["HL-031"]["coverage_status"] == "通过"
    assert by_id["HL-035"]["risk_level"] == "低"
    assert by_id["HL-035"]["coverage_status"] == "部分覆盖"
    assert "附件三" in by_id["HL-035"]["evidence_location"] or "家电" in by_id["HL-035"]["evidence_location"]
    assert "备案" not in by_id["HL-035"]["evidence_location"]
    assert "房地产经纪" not in by_id["HL-002"]["evidence_location"]


def test_real_production_report_contract_review(monkeypatch, tmp_path):
    fixture = HOUSE_LEASE_FIXTURE
    upload = _UploadFile(fixture.name, fixture.read_bytes())

    import review_v2.engine as engine_module

    original_judge = engine_module.judge_checkpoints_with_llm
    observed = {"checkpoint_ids": []}

    def tracking_judge(checkpoints, clauses, use_llm=True):
        observed["checkpoint_ids"] = [checkpoint.item_id for checkpoint in checkpoints]
        return original_judge(checkpoints, clauses, use_llm=use_llm)

    monkeypatch.setattr(engine_module, "judge_checkpoints_with_llm", tracking_judge)

    output = asyncio.run(
        review_v2_file(
            file=upload,
            contract_type="house_lease",
            include_low_risk=True,
            use_llm=False,
            profile_json="{}",
            current_user={"id": 1},
        )
    )
    by_id = {item["item_id"]: item for item in output["items"]}
    facts = output["contract_facts"]
    markdown = output["result"]
    findings = output["risk_findings"]
    assessment = output["overall_assessment"]

    assert output["contract_review_trace_id"].startswith("CR-")
    assert output["observability"]["production_call_graph"][0].endswith("ContractReviewV2.vue:runReview")
    assert any(row["final_output"] == "Markdown" for row in output["observability"]["final_output_ownership_matrix"])
    assert output["observability"]["legal_freshness_trace"]["called"] is True
    assert by_id["HL-015"]["review_trace_id"].startswith(output["contract_review_trace_id"])
    assert facts["rent"]["payment_due_day"] == "5"
    assert facts["rent"]["payment_cycle"] == "monthly"
    assert facts["termination"]["rent_default"]["exists"] is True
    assert facts["termination"]["rent_default"]["threshold_value"] == 1
    assert facts["termination"]["rent_default"]["threshold_unit"] == "month"
    assert by_id["HL-015"]["coverage_status"] != "缺失"
    assert by_id["HL-015"]["claims"][0]["value"] is True
    assert by_id["HL-017"]["coverage_status"] == "通过"
    assert facts["early_termination"]["exists"] is True
    assert by_id["HL-030"]["applicability"]["applicable"] is False
    assert by_id["HL-030"]["coverage_status"] == "不适用"
    assert by_id["HL-030"]["risk_level"] == "none"
    assert output["coverage_summary"]["不适用"] >= 1
    assert "HL-030" not in observed["checkpoint_ids"]
    assert facts["early_termination"]["penalty_formula"]["type"] == "remaining_term_rent_multiplier"
    cases = {case["remaining_days"]: case for case in by_id["HL-039"]["scenario_analysis"]["cases"]}
    assert set(cases) == {30, 90, 180, 300}
    assert cases[30]["estimated_penalty"] == 7704
    assert cases[90]["estimated_penalty"] == 23112
    assert cases[180]["estimated_penalty"] == 46224
    assert cases[300]["estimated_penalty"] == 77040
    assert "2倍月租金/租金天数通常不属于明显过高" not in by_id["HL-039"]["reasoning_summary"]
    assert "2倍月租金/租金天数通常不属于明显过高" not in markdown
    assert by_id["HL-043"]["risk_level"] != "高"
    assert by_id["HL-040"]["coverage_status"] != "通过"
    assert not any(
        any(term in ((clause.get("text") or "") + (clause.get("quote") or "")) for term in ("抵押", "贷款", "产权"))
        for clause in by_id["HL-040"].get("evidence_clauses", [])
    )
    assert output["quality_gate"]["passed"] is True
    assert "## 15. 欠租重大违约标准（HL-015）" in markdown
    assert "## 30. 无提前退租条款时的协商机制（HL-030）" in markdown
    assert "覆盖状态：不适用" in markdown
    assert "原始风险等级" not in markdown
    assert "风险等级：" not in markdown
    assert "核心风险摘要" in markdown
    assert "建议优先修改" in markdown
    assert "可选优化事项" in markdown
    assert "已覆盖关键事项" in markdown
    assert "用户风险偏好已纳入后续优先级排序" not in markdown
    assert "LLM_PRIORITY" not in markdown
    assert "Scenario Engine" not in markdown
    assert "Fact Graph" not in markdown
    assert "early_termination.penalty_formula" not in markdown
    assert "RF-" not in markdown
    if assessment["manual_review_count"] == 0:
        assert "建议人工复核" not in markdown
    assert any(issue["status"] == "OUTDATED_REFERENCE" for issue in output["legal_reference_issues"])
    assert any(finding["risk_group"] == "legal_reference" and finding["title"] == "法律引用建议更新" for finding in findings)
    assert output["risk_finding_summary"]["重大风险"] + output["risk_finding_summary"]["中等风险"] + output["risk_finding_summary"]["低风险"] == len(findings)
    early_finding = next(finding for finding in findings if finding["risk_group"] == "early_termination_financial_exposure")
    assert set(early_finding["source_review_ids"]) >= {"HL-029", "HL-039"}
    assert "HL-042" not in early_finding["source_review_ids"]
    assert "## 39. 扣款和违约金调减（HL-039）" in markdown
    assert "不是普通固定倍数违约金" in markdown
    assert "## 43. 押金返还期限（HL-043）" in markdown
    assert "关联风险发现：提前退租违约金经济风险" in markdown
    assert "RF-EARLY-TERM-001" not in markdown
    assert "rule_fallback" not in markdown
    assert output["release_quality_gate"]["status"] == "REPORT_READY"
    assert output["quality4_gate"]["status"] == "REPORT_READY"
    assert "## 49. 租金支付规则（HL-049）" in markdown
    payload = ReviewV2PdfInput(
        filename=output["filename"],
        contract_type_name=output["contract_type_name"],
        result=output["result"],
        risk_finding_summary=output["risk_finding_summary"],
        risk_findings=output["risk_findings"],
        recommendations=output["recommendations"],
        overall_assessment=output["overall_assessment"],
        release_quality_gate=output["release_quality_gate"],
        quality4_gate=output["quality4_gate"],
        items=output["items"],
    )
    docx_path = tmp_path / "production_report.docx"
    docx_path.write_bytes(_build_docx(payload))
    exported = "\n".join(paragraph.text for paragraph in Document(str(docx_path)).paragraphs)
    assert "核心风险摘要" in exported
    assert "建议优先修改" in exported
    assert "合同审查报告（第二版）" not in exported
    assert "风险发现统计" not in exported
