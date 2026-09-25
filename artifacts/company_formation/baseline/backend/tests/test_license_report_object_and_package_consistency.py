"""Final packages and prose retain object-specific, source-bound element facts."""
from copy import deepcopy
from pathlib import Path
from types import SimpleNamespace

import pytest

from layers.input_layer import InputLayer
from review_v2.engine import (
    _exact_element_report_invariants, _operative_technology_clauses,
    _evidence_constrained_recommendation, review_contract_v2,
)
from review_v2.technology_service_analysis import (
    explicit_expense_items, extract_material_delivery_method_facts,
    extract_material_disposition_facts,
)
from review_v2.user_profile import UserRiskProfile


@pytest.fixture(scope="module")
def result():
    path = next((Path(__file__).resolve().parents[2] / "test_data").glob("27*.docx"))
    text = InputLayer()._extract_from_docx_content(path.read_bytes())
    return review_contract_v2(text, "technology", use_llm=False, include_low_risk=True,
                              profile=UserRiskProfile(user_identity="甲方/被许可方"))


def item(result, key):
    return next(row for row in result["items"] if row["item_id"] == key)


def finding(result, key):
    return next(row for row in result["risk_findings"] if key in row["source_review_ids"])


def elements(result, key):
    return {row["element_id"]: row for row in item(result, key)["coverage_elements"]}


def test_each_claim_element_has_its_own_exact_package_quote(result):
    review = item(result, "TC-12-02")
    package = finding(result, "TC-12-02")["evidence_bundle"]["items"]
    for element in review["coverage_elements"]:
        if element["status"] != "COVERED":
            continue
        for fact in element["supporting_evidence"]:
            assert any(row.get("quoted_text") == fact["quote"]
                       and row.get("clause_id") == fact["clause_id"]
                       and element["element_id"] in row.get("supporting_element_ids", [])
                       and "TC-12-02" in row.get("supporting_review_ids", []) for row in package)
    handling = [row for row in package if "licensee_claim_handling" in row.get("supporting_element_ids", [])]
    assert len(handling) == 1
    assert handling[0]["quoted_text"] == "被许可方应自行处理第三方索赔"
    assert result["release_quality_gate"]["status"] == "REPORT_READY"
    assert result["release_quality_gate"]["gate_results"]["EXACT_ELEMENT_REPORT_INVARIANT"] == "PASS"
    assert not result["review_evidence_element_gate"]["mismatches"]


def test_shared_clause_without_exact_handling_quote_is_rejected(result):
    review = SimpleNamespace(**deepcopy(item(result, "TC-12-02")))
    risk = SimpleNamespace(**deepcopy(finding(result, "TC-12-02")))
    risk.evidence_bundle["items"] = [row for row in risk.evidence_bundle["items"]
                                    if "licensee_claim_handling" not in row.get("supporting_element_ids", [])]
    assert any(row.get("clause_id") == "C0029" for row in risk.evidence_bundle["items"])
    errors = _exact_element_report_invariants([review], [risk])
    assert any(row["reason"] == "EXACT_QUOTE_NOT_IN_REPORT_PACKAGE"
               and row["element_id"] == "licensee_claim_handling" for row in errors)


@pytest.mark.parametrize("method", ["电子邮件", "加密网盘", "现场移动存储设备", "纸质", "安全文件服务器"])
def test_delivery_method_can_be_in_a_numbered_child_clause(method):
    text = f"第四条 技术资料\n1. 交付资料\n提供技术手册。\n2. 交付方式\n通过{method}交付。"
    rows = extract_material_delivery_method_facts(_operative_technology_clauses(text))
    assert len(rows) == 1
    assert rows[0]["quote"] == f"通过{method}交付"


def test_contact_email_is_not_a_technical_material_delivery_method():
    rows = extract_material_delivery_method_facts(_operative_technology_clauses(
        "第一条 通知\n双方通过电子邮件通知付款账户变更。\n第二条 发票\n电子发票通过电子邮件发送。"))
    assert rows == []


def test_material_method_covered_and_absence_advice_share_final_gaps(result):
    review = item(result, "TC-13-01")
    row = elements(result, "TC-13-01")["delivery_method"]
    assert row["status"] == "COVERED" and "C0008" in row["evidence_ids"]
    assert "delivery_method" not in review["decision_trace"]["final_missing_element_ids"]
    risk = finding(result, "TC-13-01")
    for evidence in risk["evidence_bundle"]["items"]:
        if evidence.get("source_type") == "SEARCH_AUDIT":
            assert "技术资料交付形式" not in evidence["quoted_text"]
    for text in (review["suggested_clause_example"], risk["recommendation"]):
        assert "技术资料交付形式" not in text
        assert "正文尚未明确" not in text
        assert "补充明确附件内容未" not in text
    assert "基础研发范围、主要开发模块和各方基本研发分工" not in review["risk_point_description"]


def test_only_actual_expense_heads_are_asserted(result):
    review = item(result, "TC-12-01")
    risk = finding(result, "TC-12-01")
    expected = {"律师费", "诉讼费", "鉴定费", "赔偿费", "和解费", "停产损失"}
    assert set(review["decision_trace"]["source_bound_specific_details"]["expense_items"]) == expected
    for text in (review["reasoning_summary"], review["risk_point_description"], risk["issue"]):
        assert "召回" not in text
        assert set(explicit_expense_items(text)) <= expected
    assert explicit_expense_items("由被许可方承担召回费用和鉴定费") == ["召回费用", "鉴定费"]


def test_template_expense_expansion_blocks_invariant(result):
    review = SimpleNamespace(**deepcopy(item(result, "TC-12-01")))
    review.risk_point_description += "被许可方承担召回费用。"
    errors = _exact_element_report_invariants([review], [])
    assert any(row["reason"] == "UNSUPPORTED_FACTUAL_EXPENSE_ITEMS" and "召回费用" in row["details"] for row in errors)


def test_data_retention_is_not_project_copy_retention(result):
    rows = elements(result, "TC-11-03")
    assert rows["technical_material_return_destroy"]["status"] == "COVERED"
    assert rows["secret_material_return_destroy"]["status"] == "COVERED"
    assert rows["counterparty_data_retention"]["status"] == "COVERED"
    facts = rows["counterparty_data_retention"]["supporting_evidence"]
    assert all(row["actor"] == "许可方" and row["object_type"] == "counterparty_data" for row in facts)
    assert all("生产数据" in row["antecedent_quote"] for row in facts)
    assert "retained_copy_arrangement" not in rows
    assert rows["copy_return_destroy"]["status"] == "MISSING"
    assert rows["backup_return_destroy"]["status"] == "MISSING"
    review = item(result, "TC-11-03")
    assert "复制件可以继续保存" not in review["reasoning_summary"]
    assert review["coverage_status"] == "部分覆盖"


def test_copy_data_and_original_objects_do_not_cross_bind():
    text = ("第一条 处置\n合同终止后，各方应返还原始资料，但项目形成的复制件可以继续保存。\n"
            "第二条 数据\n许可方对被许可方提供的生产数据承担保密义务。合同终止后许可方可继续保存相关数据。")
    facts = extract_material_disposition_facts(_operative_technology_clauses(text))
    assert facts["original_material_disposal"] and facts["copy_retention"] and facts["counterparty_data_retention"]
    assert not facts.get("original_material_retention")
    assert not facts.get("copy_disposal")
    assert not facts.get("backup_retention")
    assert {row["clause_id"] for row in facts["copy_retention"]}.isdisjoint(row["clause_id"] for row in facts["counterparty_data_retention"])


def test_positive_retention_controls_are_not_missing():
    facts = extract_material_disposition_facts(_operative_technology_clauses(
        "第一条 处置\n合同终止后甲方可以继续保存复制件三年。复制件仅限授权人员访问。期限届满后删除复制件并出具删除确认。"))
    assert all(facts.get("copy_" + suffix) for suffix in ("period", "access_control", "deletion_or_destroy", "confirmation"))


@pytest.mark.parametrize("other_controls", [
    "备份仅限授权人员访问。期限届满后删除备份并出具删除确认。",
    "乙方应将复制件仅限授权人员访问。期限届满后删除复制件并出具删除确认。",
])
def test_retention_controls_cannot_borrow_another_object_or_actor(other_controls):
    facts = extract_material_disposition_facts(_operative_technology_clauses(
        "第一条 处置\n合同终止后甲方可以继续保存复制件。" + other_controls))
    assert facts["copy_retention"]
    assert not any(facts.get("copy_" + suffix) for suffix in ("access_control", "deletion_or_destroy", "confirmation"))


def test_prohibited_retention_is_not_positive_retention():
    facts = extract_material_disposition_facts(_operative_technology_clauses(
        "第一条 处置\n合同终止后甲方不得继续保存复制件。"))
    assert not facts.get("copy_retention")


def test_positive_fact_cannot_be_overwritten_with_missing(result):
    review = SimpleNamespace(**deepcopy(item(result, "TC-13-01")))
    method = next(row for row in review.coverage_elements if row["element_id"] == "delivery_method")
    method.update(status="MISSING", supporting_evidence=[])
    assert any(row["reason"] == "MISSING_WITH_DIRECT_FACT" for row in _exact_element_report_invariants([review], []))


def test_covered_and_missing_duplicates_are_rejected(result):
    review = SimpleNamespace(**deepcopy(item(result, "TC-12-02")))
    review.coverage_elements.append({"element_id": "licensee_claim_handling", "status": "MISSING"})
    assert any(row["reason"] == "ELEMENT_STATUS_CONFLICT" for row in _exact_element_report_invariants([review], []))


def test_recommendation_uses_only_final_unresolved_elements(result):
    review = SimpleNamespace(**deepcopy(item(result, "TC-13-01")))
    advice = _evidence_constrained_recommendation(review, "补充技术资料交付形式；补充正文研发范围。")
    assert "交付形式" not in advice and "正文研发范围" not in advice
    assert "交付数量" in advice


@pytest.mark.parametrize("key", ["TC-12-02", "TC-13-01", "TC-11-03"])
def test_recommendation_quality_rewrite_preserves_final_element_projection(result, key):
    review = SimpleNamespace(**deepcopy(item(result, key)))
    risk = finding(result, key)
    assert risk["recommendation"] == _evidence_constrained_recommendation(review, "过期模板")
    assert "同时列明责任主体、办理期限和违约后果" not in risk["recommendation"]


def test_later_recommendation_expansion_is_rejected(result):
    risk = SimpleNamespace(**deepcopy(finding(result, "TC-13-01")))
    risk.recommendation += "补充已覆盖的技术资料交付形式。"
    assert any(row["reason"] == "FINAL_ELEMENT_RECOMMENDATION_OVERRIDDEN"
               for row in _exact_element_report_invariants([], [risk]))
