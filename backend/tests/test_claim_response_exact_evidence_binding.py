"""Inbound claim facts must have their own event, actor and source binding."""
from copy import deepcopy
from pathlib import Path

import pytest
from docx import Document

from review_v2.engine import (
    ReviewItemResult, _apply_technology_transaction_evidence_consistency,
    _review_evidence_element_gate, _apply_review_evidence_ownership,
    _set_multi_element_state, review_contract_v2,
)
from review_v2.technology_service_analysis import build_technology_fact_registry, classify_technology_transaction
from review_v2.user_profile import UserRiskProfile


def review():
    return ReviewItemResult(
        item_id="SYNTHETIC", node_id="test", title="事实绑定", risk_level="中",
        status="部分覆盖", coverage_status="部分覆盖", issue_type="PARTIAL",
        risk_point_description="", suggested_clause_example="", legal_basis_index="",
        legal_consequence_if_missing="", applicable_if="本项适用", matched_terms=[],
        evidence_clauses=[{"clause_id": "E1", "text": "甲方负责办理登记。", "source_type": "SOURCE_CLAUSE"}],
        evidence_location="第一条", reasoning_summary="", applicability={"status": "APPLICABLE"},
    )


ADVERSE_CLAIM = """第一条 第三方主张
如第三方主张被许可方按约实施合同技术侵犯其知识产权：
被许可方应自行处理第三方索赔；
许可方根据实际情况提供必要技术协助；
相关律师费、诉讼费、赔偿费均由被许可方承担。
"""
NOISE = """第二条 分许可
被许可方完成第三方分许可后30日内通知许可方。
第三条 资料交付
被许可方收到材料后5个工作日内应通知许可方是否验收合格。
第四条 专利维权
任何一方发现第三方侵犯合同专利，应当通知另一方。
是否提起诉讼及和解由许可方单独决定。
第五条 无效
专利全部无效后，已付款不退，未付款继续支付。
第六条 不可抗力
受影响方应在10日内通知对方。
"""


def registry(text):
    return build_technology_fact_registry(text)["third_party_claim"]


def project(text):
    item = review()
    item.item_id, item.title = "TC-12-02", "第三方权利主张处理"
    text = "技术秘密许可合同。许可方许可被许可方使用技术秘密，许可费100万元。\n" + text
    _apply_technology_transaction_evidence_consistency([item], text, classify_technology_transaction(text))
    _apply_review_evidence_ownership([item])
    return item


def test_adverse_presence_does_not_invent_protective_procedures():
    facts = registry(ADVERSE_CLAIM + NOISE)
    assert facts["licensee_claim_handling"] and facts["claim_assistance"]
    assert facts["claim_cost_allocation"] and facts["third_party_compensation_allocation"]
    assert not any(facts[key] for key in (
        "claim_handling", "notification_requirement", "notification_deadline",
        "defense_control", "lawyer_selection", "settlement_authority", "refund_remedy",
    ))
    item = project(ADVERSE_CLAIM + NOISE)
    elements = {row["element_id"]: row for row in item.coverage_elements}
    for key in ("notification_requirement", "notification_deadline", "licensor_participation"):
        assert elements[key]["status"] == "MISSING"
        assert not elements[key]["evidence_ids"]
    for key in ("licensee_claim_handling", "defense_cost_allocation", "damages_allocation"):
        assert elements[key]["status"] == "COVERED"
        assert elements[key]["direction"] == "ADVERSE"
    assert "有限技术协助" in elements["licensor_assistance"]["proposition"]
    assert "约定工作日内" not in item.reasoning_summary
    assert not _review_evidence_element_gate([item])["mismatches"]


@pytest.mark.parametrize("provider,recipient", [
    ("许可方", "被许可方"), ("许可人", "被许可人"),
    ("卖方", "买方"), ("让与方", "受让方"),
])
@pytest.mark.parametrize("days", ["5个工作日", "十日", "48小时"])
def test_direct_notice_deadline_handler_and_costs_remain_recalled(provider, recipient, days):
    text = (f"第一条 第三方权利主张\n{recipient}收到第三方权利主张后应在{days}内书面通知{provider}。"
            f"{provider}负责与第三方交涉处理，承担合理律师费、诉讼费及依法应承担的赔偿责任。")
    f = registry(text)
    assert all(f[key] for key in ("notification_requirement", "notification_deadline", "claim_handling", "claim_cost_allocation", "third_party_compensation_allocation"))
    assert not f["licensee_claim_handling"]
    rows = f["response_element_evidence"]
    assert all(row["value"] == days + "内" for row in rows["notification_deadline"])
    assert all(row["actor"] == "LICENSOR" for row in rows["claim_handling"])


@pytest.mark.parametrize("provider,recipient", [("甲方", "乙方"), ("乙方", "甲方")])
def test_declared_party_roles_not_fixed_party_letters(provider, recipient):
    text = (f"许可方（{provider}）：企业一；被许可方（{recipient}）：企业二。\n"
            f"第一条 第三方权利主张\n如第三方指控{recipient}侵权，{recipient}应自行处理索赔；"
            f"{provider}仅提供必要技术协助。")
    f = registry(text)
    assert f["licensee_claim_handling"]
    assert f["claim_assistance"]
    assert not f["claim_handling"]


@pytest.mark.parametrize("notice", [
    "被许可方无需通知许可方。", "双方未明确5个工作日内通知许可方的义务。",
    "许可方应在5日内通知被许可方。", "通知期限由双方另行协商。",
])
def test_negative_unspecified_or_reversed_notice_is_not_covered(notice):
    f = registry("第一条 第三方索赔\n如第三方主张被许可方侵权，" + notice)
    assert not f["notification_requirement"]
    assert not f["notification_deadline"]


def test_handler_switch_is_not_a_role_reversal():
    f = registry("第一条 索赔\n被许可方收到第三方索赔后由许可方负责处理并承担合理法律费用。")
    assert f["claim_handling"]
    assert not f["licensee_claim_handling"]


def test_assistance_in_handling_is_not_full_handling():
    f = registry("第一条 第三方索赔\n第三方主张被许可方侵权时，许可方应协助处理索赔。")
    assert f["claim_assistance"]
    assert not f["claim_handling"]


def test_no_heading_only_or_outbound_enforcement_cover():
    assert not registry("第一条 第三方指控\n第二条 专利维权\n第三方侵犯合同专利，应及时通知许可方。")["response_element_evidence"]


def test_gate_rejects_borrowed_fact_even_when_source_clause_id_matches():
    item = project(ADVERSE_CLAIM)
    element = next(row for row in item.coverage_elements if row["element_id"] == "notification_requirement")
    assistance = next(row for row in item.coverage_elements if row["element_id"] == "licensor_assistance")
    element.update({"status": "COVERED", "evidence_ids": assistance["evidence_ids"],
                    "source_clause_ids": assistance["source_clause_ids"],
                    "supporting_evidence": deepcopy(assistance["supporting_evidence"])})
    _apply_review_evidence_ownership([item])
    gate = _review_evidence_element_gate([item])
    assert gate["status"] == "BLOCKED"
    assert "notification_requirement" in {row["element_id"] for row in gate["mismatches"]}


def test_unquoted_assertion_cannot_become_covered():
    item = review()
    _set_multi_element_state(item, [{"element_id": "notice", "status": "COVERED", "proposition": "通知许可方",
        "bound_evidence_ids": ["E1"], "supporting_evidence": [{"clause_id": "E1", "quote": "应通知许可方"}]}], item.evidence_clauses)
    assert item.coverage_elements[0]["status"] == "UNCERTAIN"
    assert not item.coverage_elements[0]["evidence_ids"]


def test_file_upload_response_keeps_exact_element_evidence():
    import asyncio
    from fastapi import UploadFile
    from routers.review_v2 import ReviewV2Result, review_v2_file
    path = next((Path(__file__).resolve().parents[2] / "test_data").glob("27*.docx"))
    with path.open("rb") as source:
        response = asyncio.run(review_v2_file(file=UploadFile(filename=path.name, file=source),
            contract_type="technology", include_low_risk=True, use_llm=False,
            profile_json='{"user_identity":"甲方/被许可方"}', current_user={}))
    payload = ReviewV2Result(**response).model_dump()
    assert payload["release_quality_gate"]["status"] == "REPORT_READY"
    assert response["review_evidence_element_gate"]["mismatches"] == []
    item = next(row for row in payload["items"] if row["item_id"] == "TC-12-02")
    assert item["issue_type"] == "PARTIAL"
    assert all(row.get("supporting_evidence") for row in item["coverage_elements"] if row["status"] == "COVERED")


def test_current_patent_license_report_and_release_gate():
    fixture = next((Path(__file__).resolve().parents[2] / "test_data").glob("27*.docx"))
    text = "\n".join(p.text for p in Document(fixture).paragraphs)
    result = review_contract_v2(text, "technology", use_llm=False, include_low_risk=True,
                                profile=UserRiskProfile(user_identity="被许可方"))
    item = next(row for row in result["items"] if row["item_id"] == "TC-12-02")
    assert item["coverage_status"] == "部分覆盖"
    assert item["issue_type"] == "PARTIAL"
    rows = {row["element_id"]: row for row in item["coverage_elements"]}
    for key in ("notification_requirement", "notification_deadline", "licensor_participation", "defense_control", "lawyer_selection", "settlement_authority", "settlement_non_prejudice", "license_cure"):
        assert rows[key]["status"] == "MISSING"
        assert not rows[key]["evidence_ids"]
    for row in rows.values():
        if row["status"] == "COVERED":
            assert row["supporting_evidence"]
            assert all(fact["location"] == "第十条第1项" for fact in row["supporting_evidence"])
    assert result["release_quality_gate"]["status"] == "REPORT_READY"
    assert not result["release_quality_gate"]["failures"]
    assert not result["review_evidence_element_gate"]["mismatches"]
    for key in ("reasoning_summary", "risk_point_description", "suggested_clause_example"):
        assert "约定工作日内" not in item[key]
        assert "许可方负责与第三方交涉处理。" not in item[key]
    liability = next(row for row in result["items"] if row["item_id"] == "TC-12-01")
    assert liability["issue_type"] == "DEFAULT_LAW_DEVIATION"
    assert any(row["status"] == "ADVERSE" for row in liability["coverage_elements"])
