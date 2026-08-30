from pathlib import Path
import re

from docx import Document

from review_v2.clause_parser import parse_contract_clauses
from review_v2.engine import review_contract_v2
from review_v2.engine import (
    FinalDisposition,
    Recommendation,
    ReviewItemResult,
    RiskFinding,
    _report_integrity_gate,
)
from review_v2.technology_service_analysis import analyze_technical_service_risks
from review_v2.user_profile import UserRiskProfile


FIXTURE = Path(__file__).resolve().parents[2] / "test_data" / "8、技术服务.docx"
CORE_GROUPS = {
    "technical_acceptance_payment_control",
    "technical_background_ip_overtransfer",
    "technical_uncapped_cumulative_liability",
    "technical_unilateral_termination_change",
    "personal_information_processing_gap",
    "payment_formula_inconsistency",
}


def _text() -> str:
    document = Document(str(FIXTURE))
    return "\n".join(paragraph.text for paragraph in document.paragraphs if paragraph.text.strip())


def _review() -> dict:
    return review_contract_v2(
        _text(), "technology", use_llm=False,
        profile=UserRiskProfile(user_identity="乙方/技术服务提供方", contract_scenario="高校科研数据治理技术服务"),
    )


def test_clause_parent_is_not_replaced_by_cross_reference_item_number():
    text = "第十二条 违约责任\n（二）乙方违约责任\n乙方违反第八条第（二）款第8项的，应承担责任；多项责任同时适用且不设最高限额。"
    clause = next(row for row in parse_contract_clauses(text) if "不设最高限额" in row.text)
    assert clause.location.startswith("第十二条（二）")
    assert clause.article_number == "第十二条"
    assert clause.heading_path[0].startswith("第十二条")
    assert clause.heading_path[-1].startswith("（二）")
    assert clause.node_id == clause.clause_id


def test_core_findings_have_complete_fact_typed_evidence_bundles():
    output = _review()
    findings = {row["risk_group"]: row for row in output["risk_findings"]}
    assert CORE_GROUPS <= set(findings)
    for group in CORE_GROUPS:
        bundle = findings[group]["evidence_bundle"]
        assert bundle["entailment_status"] == "PASSED"
        assert not bundle["missing_fact_types"]
        assert bundle["items"]
        assert all(row["quoted_text"] and row["clause_node_id"] for row in bundle["items"])

    acceptance_types = set(findings["technical_acceptance_payment_control"]["evidence_bundle"]["covered_fact_types"])
    assert {"quantitative_acceptance", "subjective_acceptance_override", "no_deemed_acceptance", "unlimited_rectification", "payment_depends_on_acceptance"} <= acceptance_types
    ip_quotes = " ".join(row["quoted_text"] for row in findings["technical_background_ip_overtransfer"]["evidence_bundle"]["items"])
    assert "重复数据较多" not in ip_quotes
    assert "已有" in ip_quotes and "通用算法" in ip_quotes and "甲方所有" in ip_quotes


def test_core_recommendations_are_bound_by_finding_id_and_semantics():
    output = _review()
    recs = {risk_id: rec for rec in output["recommendations"] for risk_id in rec["target_finding_ids"]}
    findings = {row["risk_group"]: row for row in output["risk_findings"]}
    payment = recs[findings["payment_formula_inconsistency"]["finding_id"]]
    liability = recs[findings["technical_uncapped_cumulative_liability"]["finding_id"]]
    assert any(term in payment["suggested_text"] for term in ("付款节点", "比例合计", "质保金"))
    assert not any(term in payment["suggested_text"] for term in ("责任上限", "实际损失"))
    assert "责任上限" in liability["suggested_text"]
    assert payment["rule_code"] == "payment_formula_inconsistency"
    assert liability["rule_code"] == "technical_uncapped_cumulative_liability"


def test_personal_information_trigger_ignores_contact_only_contracts():
    contact_only = "合同通知联系人张三，联系电话13800000000，通知邮箱test@example.com，签署页地址为成都市。"
    assert analyze_technical_service_risks(contact_only)["personal_information_processing_gap"]["present"] is False


def test_report_uses_final_findings_and_quality_gate_checks_integrity():
    output = _review()
    report = output["result"]
    assert output["release_quality_gate"]["status"] == "REPORT_READY"
    assert output["report_integrity_gate"]["status"] == "REPORT_READY"
    assert output["report_integrity_gate"]["gate_results"]["EVIDENCE_BUNDLE_ENTAILMENT_GATE"] == "PASS"
    assert output["report_integrity_gate"]["gate_results"]["RECOMMENDATION_SEMANTIC_BINDING_GATE"] == "PASS"
    for finding in output["risk_findings"]:
        assert finding["title"] in report
    assert report.count("**可选优化**") == output["final_disposition_summary"]["optional_improvement"]
    assert "合同已明确约定" in report
    assert "风险条款" in report


def test_secondary_cross_clause_risks_are_detected():
    groups = {row["risk_group"] for row in _review()["risk_findings"]}
    assert {
        "data_retention_warranty_conflict",
        "personal_injury_liability_exclusion",
        "short_data_objection_deemed_acceptance",
        "external_change_free_remediation",
    } <= groups


def _integrity_inputs(output: dict):
    return (
        [ReviewItemResult(**row) for row in output["items"]],
        [RiskFinding(**row) for row in output["risk_findings"]],
        [Recommendation(**row) for row in output["recommendations"]],
        [FinalDisposition(**row) for row in output["final_dispositions"]],
    )


def test_quality_gate_blocks_wrong_recommendation_binding():
    output = _review()
    items, findings, recommendations, dispositions = _integrity_inputs(output)
    payment = next(row for row in findings if row.risk_group == "payment_formula_inconsistency")
    recommendation = next(row for row in recommendations if payment.finding_id in row.target_finding_ids)
    recommendation.suggested_text = "建议设置累计责任上限并限定实际损失。"
    gate = _report_integrity_gate(items, findings, recommendations, dispositions, output["result"])
    assert gate["status"] == "BLOCKED"
    assert any(row["requirement"] == "RECOMMENDATION_SEMANTIC_BINDING_GATE" for row in gate["failures"])


def test_quality_gate_blocks_incomplete_evidence_bundle_and_missing_detail():
    output = _review()
    items, findings, recommendations, dispositions = _integrity_inputs(output)
    acceptance = next(row for row in findings if row.risk_group == "technical_acceptance_payment_control")
    acceptance.evidence_bundle["missing_fact_types"] = ["payment_depends_on_acceptance"]
    report_without_detail = output["result"].replace(acceptance.title, "")
    gate = _report_integrity_gate(items, findings, recommendations, dispositions, report_without_detail)
    requirements = {row["requirement"] for row in gate["failures"]}
    assert gate["status"] == "BLOCKED"
    assert "EVIDENCE_BUNDLE_ENTAILMENT_GATE" in requirements
    assert "SUMMARY_DETAIL_RISK_ID_GATE" in requirements


def test_quality_gate_blocks_semantically_invalid_evidence_and_claim_gap():
    output = _review()
    items, findings, recommendations, dispositions = _integrity_inputs(output)
    privacy = next(row for row in findings if row.risk_group == "personal_information_processing_gap")
    privacy.evidence_bundle["items"][0]["quoted_text"] = "通知联系人邮箱为notice@example.com。"
    privacy.evidence_bundle["supported_claim_ids"].remove(privacy.evidence_bundle["required_claim_ids"][0])
    gate = _report_integrity_gate(items, findings, recommendations, dispositions, output["result"])
    requirements = {row["requirement"] for row in gate["failures"]}
    assert {"EVIDENCE_FACT_ROLE_GATE", "CLAIM_EVIDENCE_COVERAGE_GATE"} <= requirements


def test_quality_gate_blocks_review_risk_bundle_projection_mismatch():
    output = _review()
    items, findings, recommendations, dispositions = _integrity_inputs(output)
    target = next(row for row in findings if row.evidence_bundle)
    for item in items:
        item.related_risks = [risk_id for risk_id in item.related_risks if risk_id != target.finding_id]
    gate = _report_integrity_gate(items, findings, recommendations, dispositions, output["result"])
    assert any(row["requirement"] == "SINGLE_EVIDENCE_SOURCE_GATE" for row in gate["failures"])


def test_quality_gate_blocks_issue_type_partial_and_applicability_conflicts():
    output = _review()
    items, findings, recommendations, dispositions = _integrity_inputs(output)
    payment = next(row for row in findings if row.risk_group == "payment_formula_inconsistency")
    payment.issue_type = "ADVERSE"
    privacy = next(row for row in findings if row.risk_group == "personal_information_processing_gap")
    privacy.evidence_bundle["missing_element_types"] = []
    not_applicable = next(row for row in items if str((row.applicability or {}).get("status")).upper() == "NOT_APPLICABLE")
    not_applicable.applicability["user_reason"] = "合同未触发“技术合同均适用”这一条件。"
    gate = _report_integrity_gate(items, findings, recommendations, dispositions, output["result"])
    requirements = {row["requirement"] for row in gate["failures"]}
    assert {
        "ISSUE_TYPE_CONSISTENCY_GATE",
        "PARTIAL_MISSING_ELEMENT_GATE",
        "APPLICABILITY_DISPLAY_CONSISTENCY_GATE",
    } <= requirements


def test_quality_gate_blocks_undisclosed_summary_truncation():
    output = _review()
    items, findings, recommendations, dispositions = _integrity_inputs(output)
    report = re.sub(r"> 以下展示优先级最高的\d+项，其余\d+项见完整风险明细。", "", output["result"])
    gate = _report_integrity_gate(items, findings, recommendations, dispositions, report)
    assert any(row["requirement"] == "SUMMARY_TRUNCATION_DISCLOSURE_GATE" for row in gate["failures"])
