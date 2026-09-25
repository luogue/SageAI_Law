from pathlib import Path
import re
import pytest
from layers.input_layer import InputLayer
from review_v2.engine import review_contract_v2
from review_v2.user_profile import UserRiskProfile
from review_v2.clause_parser import parse_contract_clauses
from review_v2.technology_service_analysis import extract_claim_response_facts, classify_technology_transaction
from review_v2.engine import _operative_technology_clauses
from review_v2 import engine
from dataclasses import fields
from copy import deepcopy


@pytest.fixture(scope="module")
def result():
    path = next((Path(__file__).resolve().parents[2] / "test_data").glob("46*.docx"))
    text = InputLayer()._extract_from_docx_content(path.read_bytes())
    return review_contract_v2(text, "technology", use_llm=False, profile=UserRiskProfile(user_identity="甲方/被许可方"))


def test_structured_license_result(result):
    by_id = {row["item_id"]: row for row in result["items"]}
    elements = lambda key: {e["element_id"]: e for e in by_id[key]["coverage_elements"]}
    for key in ("notification_requirement", "notification_deadline"):
        row = elements("TC-12-02")[key]
        assert row["status"] == "COVERED"
        assert any("3个工作日" in source["quote"] for source in row["supporting_evidence"])
    assert by_id["TC-10-02"]["coverage_status"] == "部分覆盖"
    for key in ("reciprocal_free_use", "improvement_sublicense", "priority_license"):
        assert elements("TC-10-02")[key]["status"] == "COVERED"
    assert elements("TC-10-02")["license_duration"]["status"] == "MISSING"
    assert elements("TC-13-01")["major_document_types"]["status"] == "COVERED"
    for key in ("TC-09-02", "TC-13-03"):
        assert by_id[key]["coverage_status"] != "不适用"
    for key in ("TC-06-01", "TC-06-02", "TC-06-03", "TC-06-04"):
        assert by_id[key]["coverage_status"] == "不适用"
    assert "再许可" in by_id["TC-07-01"]["suggested_clause_example"]
    liability = elements("TC-12-01")["licensor_legal_economic_liability"]
    assert "合理法律费用" not in liability["proposition"]
    assert elements("TC-12-01")["specific_cost_and_compensation_scope"]["status"] == "MISSING"
    assert result["release_quality_gate"]["status"] == "REPORT_READY", result["release_quality_gate"]["failures"]


def test_atomic_support_incident_and_acceptance_states(result):
    items = {row["item_id"]: row for row in result["items"]}
    def elements(key):
        return {e["element_id"]: e for e in items[key]["coverage_elements"]}
    support = elements("TC-07-04")
    assert items["TC-07-04"]["coverage_status"] == "部分覆盖"
    assert support["on_demand_technical_service"]["status"] == "COVERED"
    for key in (
        "technical_service_scope", "technical_service_content", "patent_fee_and_validity_maintenance",
        "patent_status_change_notice", "technical_service_response_deadline",
    ):
        assert support[key]["status"] == "MISSING"
    service = elements("TC-09-01")
    assert items["TC-09-01"]["coverage_status"] == "部分覆盖"
    assert service["service_existence"]["status"] == "COVERED"
    assert service["service_period"]["status"] == "COVERED"
    assert service["training_people"]["status"] == "COVERED"
    assert service["training_place"]["status"] == "COVERED"
    assert service["service_scope"]["status"] == "MISSING"
    assert service["service_content"]["status"] == "MISSING"
    breach = elements("TC-11-04")
    assert items["TC-11-04"]["coverage_status"] == "部分覆盖"
    assert "confidentiality_obligation_reference" in breach
    assert "confidentiality_obligation" not in breach
    assert breach["breach_damage_liability"]["status"] == "COVERED"
    for key in ("stop_disclosure", "stop_use", "mitigation_obligation", "incident_notification"):
        assert breach[key]["status"] == "MISSING"
    assert not any("合同明确约定保密义务" in e["proposition"] for e in breach.values() if e["status"] == "MISSING")
    assert elements("TC-13-01")["receipt_confirmation"]["status"] == "MISSING"
    material = elements("TC-13-01")
    contaminated_ids = {"C0018", "C0019"}
    for key in ("technical_material_scope", "delivery_obligation", "delivery_quantity"):
        assert not (set(material[key]["evidence_ids"]) & contaminated_ids)
    acceptance = elements("TC-09-02")
    for key in ("reinspection_procedure", "reinspection_deadline"):
        assert acceptance[key]["status"] == "COVERED"
        assert acceptance[key]["evidence_ids"]
    for key in ("rectification_party", "rectification_measures", "rectification_procedure"):
        assert acceptance[key]["status"] == "MISSING"
    assert "再次验收" not in items["TC-09-02"]["suggested_clause_example"]
    assert "其他合同" in items["TC-09-02"]["applicable_if"]
    assert "退款" not in items["TC-09-02"]["reasoning_summary"]
    assert "模型训练" not in items["TC-07-04"]["reasoning_summary"]
    assert "响应时间" in items["TC-07-04"]["suggested_clause_example"]
    claim = elements("TC-12-02")
    assert claim["liability_responsible_party"]["status"] == "COVERED"
    assert "相应法律责任" in claim["liability_responsible_party"]["proposition"]
    assert claim["defense_cost_allocation"]["status"] == "MISSING"
    assert claim["damages_scope"]["status"] == "MISSING"


@pytest.mark.parametrize("receipt,covered", [
    ("合同产品验收合格后双方签署产品验收确认单。", False),
    ("双方应签署技术资料交接确认单。", True),
    ("被许可方应对交付的技术资料进行书面验收确认。", True),
])
def test_receipt_requires_material_object(receipt, covered):
    path = next((Path(__file__).resolve().parents[2] / "test_data").glob("46*.docx"))
    text = InputLayer()._extract_from_docx_content(path.read_bytes())
    report = review_contract_v2(text + "\n【交付确认】\n" + receipt, "technology", use_llm=False,
                                profile=UserRiskProfile(user_identity="甲方/被许可方"))
    item = next(i for i in report["items"] if i["item_id"] == "TC-13-01")
    element = next(e for e in item["coverage_elements"] if e["element_id"] == "receipt_confirmation")
    assert element["status"] == ("COVERED" if covered else "MISSING")
    if covered:
        assert element["evidence_ids"]


@pytest.mark.parametrize("separator", ["", "\n"])
@pytest.mark.parametrize("days", ["3个工作日内", "七日内", "12小时内"])
def test_notice_field_label_and_value_share_direct_evidence(separator, days):
    text = "【侵权处理】\n被许可方收到第三方侵权主张后的通知期限：" + separator + days
    facts = extract_claim_response_facts(parse_contract_clauses(text), r"(?:许可方|卖方)", r"(?:被许可方|买方)")
    assert facts["notification_requirement"]
    assert facts["notification_deadline"][0]["value"] == days


@pytest.mark.parametrize("value", ["待定", "未约定", "另行协商"])
def test_blank_notice_field_is_not_covered(value):
    facts = extract_claim_response_facts(parse_contract_clauses("【侵权处理】\n被许可方收到第三方侵权主张后的通知期限：" + value), r"(?:许可方|卖方)", r"(?:被许可方|买方)")
    assert not facts.get("notification_deadline")


def test_a_neighbouring_payment_deadline_does_not_fill_a_notice_field():
    text = "【侵权处理】\n被许可方收到第三方侵权主张后的通知期限：\n未约定\n付款期限：\n3个工作日内"
    facts = extract_claim_response_facts(parse_contract_clauses(text), "许可方", "被许可方")
    assert not facts.get("notification_deadline")


@pytest.mark.parametrize("numbered", [True, False])
def test_short_material_list_is_not_discarded_as_a_heading(numbered):
    lines = ["专利说明书", "权利要求书", "说明书附图"]
    if numbered:
        lines = [f"{n}. {s}" for n, s in enumerate(lines, 1)]
    clauses = _operative_technology_clauses("【技术资料交付】\n技术资料包括：\n" + "\n".join(lines))
    assert all(name in "\n".join(c.text for c in clauses) for name in ["专利说明书", "权利要求书", "说明书附图"])


def test_primary_license_is_preserved_when_service_module_is_activated():
    text = "专利实施许可合同\n许可方授予被许可方普通实施许可，专利使用费100万元。\n【技术服务】\n培训人员：5人\n培训时间：2个工作日\n技术服务期限：资料交付后45日内"
    classification = classify_technology_transaction(text)
    assert classification["primary_subtype"] == "TECHNOLOGY_LICENSE"
    assert "TECHNICAL_SERVICE" in classification["secondary_modules"]


def test_required_recommendation_element_cannot_silently_disappear(result):
    def load(cls, key):
        return [cls(**{f.name: row[f.name] for f in fields(cls) if f.name in row}) for row in deepcopy(result[key])]
    findings = load(engine.RiskFinding, "risk_findings")
    dispositions = load(engine.FinalDisposition, "final_dispositions")
    recommendations = load(engine.Recommendation, "recommendations")
    finding = next(row for row in findings if "TC-07-01" in row.source_review_ids)
    recommendation = next(row for row in recommendations if finding.finding_id in row.source_finding_ids)
    recommendation.fragments = [row for row in recommendation.fragments if "transfer_or_sublicense_boundary" not in row["source_element_ids"]]
    audit = engine._recommendation_truth_binding_audit(recommendations, findings, dispositions)
    assert any(row.get("reason") == "CORE_RECOMMENDATION_ELEMENT_OMITTED" for row in audit["recommendation_element_leakage"])


def test_owner_licensor_and_sublicense_ban_make_authorization_documents_conditional():
    text = """
专利实施许可合同
甲方（被许可方）：智能制造有限公司
乙方（许可方）：先进技术研究院
乙方授予甲方在中华人民共和国境内实施本专利的普通许可。
专利名称：工业检测技术；专利号：ZL202610000099.9；专利权人：先进技术研究院；申请日：2025年1月1日；授权日：2026年2月1日。
未经乙方书面同意，甲方不得分许可、再许可或转许可给任何第三方。
"""
    report = review_contract_v2(text, "technology", use_llm=False,
                                profile=UserRiskProfile(user_identity="甲方/被许可方"))
    item = next(row for row in report["items"] if row["item_id"] == "TC-03-04")
    elements = {row["element_id"]: row for row in item["coverage_elements"]}
    missing_text = "\n".join(
        row["proposition"] for row in item["coverage_elements"] if row["status"] == "MISSING"
    )

    assert elements["licensor_authority_and_upstream_authorization"]["status"] == "COVERED"
    assert elements["upstream_authorization_file"]["status"] == "NOT_APPLICABLE"
    assert elements["sublicense_authorization_file"]["status"] == "NOT_APPLICABLE"
    assert "上游授权" not in missing_text
    assert "再许可权限证明文件" not in missing_text
    assert "上游授权" not in item["suggested_clause_example"]
    assert "再许可权限" not in item["suggested_clause_example"]


def test_recommendations_are_limited_to_final_missing_elements_and_are_actionable(result):
    items = {row["item_id"]: row for row in result["items"]}
    support = items["TC-07-04"]
    allowed = {
        "技术服务具体范围", "技术服务具体内容", "技术服务响应时间", "技术服务交付标准",
        "专利费用缴纳及有效性维持义务", "专利法律状态变化通知义务",
    }
    advice = support["suggested_clause_example"]
    for label in allowed:
        assert label in advice
    for extra in ("责任主体", "办理期限", "违约后果"):
        assert extra not in advice

    infringement = items["TC-12-01"]
    sentence = infringement["suggested_clause_example"]
    assert "律师费" in sentence and "诉讼费" in sentence and "鉴定费" in sentence
    assert "赔偿款" in sentence and "和解费用" in sentence
    assert "尚未细化" not in sentence
    assert "尚未明确" not in sentence
    assert not re.search(r"建议(?:补充)?明确[^。；]*尚未", sentence)
