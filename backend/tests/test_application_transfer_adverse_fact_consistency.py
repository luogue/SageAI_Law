"""Role/polarity and exact fact consumption, with source and absence controls."""
from copy import deepcopy
from pathlib import Path
from types import SimpleNamespace

import pytest

from layers.input_layer import InputLayer
from review_v2 import engine
from review_v2.technology_service_analysis import analyze_payment_schedule, build_technology_fact_registry
from review_v2.user_profile import UserRiskProfile


@pytest.fixture(scope="module")
def text():
    path = next((Path(__file__).resolve().parents[2] / "test_data").glob("45*.docx"))
    return InputLayer()._extract_from_docx_content(path.read_bytes())


@pytest.fixture(scope="module")
def result(text):
    return engine.review_contract_v2(text, "technology", use_llm=False,
                                    profile=UserRiskProfile(user_identity="甲方/受让方"))


def item(result, key):
    return next(row for row in result["items"] if row["item_id"] == key)


def elements(row):
    return {e["element_id"]: e for e in row["coverage_elements"]}


def test_current_gate_and_identity_stay_ready(result):
    assert result["release_quality_gate"]["status"] == "REPORT_READY", result["release_quality_gate"]["failures"]
    assert not result["release_quality_gate"]["failures"]
    assert item(result, "TC-01-03")["coverage_status"] == "通过"


def test_claim_cost_actor_is_not_changed_by_provider_cap(text, result):
    registry = build_technology_fact_registry(text)["third_party_claim"]
    assert registry["claim_cost_bearer"] == "LICENSEE"
    liability = item(result, "TC-12-01")
    assert liability["coverage_status"] == "风险条款"
    assert elements(liability)["licensee_infringement_costs"]["status"] == "ADVERSE"
    assert "让与方对权利来源瑕疵承担法律费用及赔偿责任" not in str(liability["narrative_state"])
    claim = item(result, "TC-12-02")
    for key in ("defense_cost_allocation", "damages_allocation", "licensee_claim_handling"):
        element = elements(claim)[key]
        assert element["status"] == "COVERED" and element["direction"] == "ADVERSE"
        assert element["supporting_evidence"] and element["evidence_ids"]
        assert all(source["quote"] in text for source in element["supporting_evidence"])
    for key in ("notification_requirement", "notification_deadline", "licensor_participation"):
        assert elements(claim)[key]["status"] == "MISSING"


def test_existing_license_does_not_cover_sibling_encumbrances(result):
    for rule in ("TC-03-04", "TC-13-02"):
        rows = elements(item(result, rule))
        assert rows["application_existing_license_disclosure"]["status"] == "COVERED"
        for key in ("coownership", "pledge", "seizure", "other_restrictions"):
            assert rows[f"application_{key}_disclosure"]["status"] == "MISSING"
        assert "application_encumbrance_disclosure" not in rows
    for key in ("coownership", "pledge", "seizure", "other_restrictions"):
        assert elements(item(result, "TC-06-03"))[f"application_{key}_disclosure"]["status"] == "MISSING"


@pytest.mark.parametrize("label", ["专利申请权转让价款总额", "专利权转让价款", "合同总价"])
@pytest.mark.parametrize("base", [2400000, 3600000])
def test_payment_base_is_not_subtype_or_amount_specific(label, base):
    text = f"{label}：人民币{base:,}元。\n具体支付方式：\n"
    for index, pct in enumerate((50, 40, 20), 1):
        text += f"（{index}）第{index}阶段完成后支付{pct}%，即人民币{base*pct//100:,}元；\n"
    payment = analyze_payment_schedule(text)
    assert payment["contract_total"] == base
    assert payment["percentage_total"] == 110
    assert payment["amount_total"] == base * 110 // 100
    assert payment["amount_delta"] == base // 10


def test_all_confirmed_high_liability_facts_reach_narrative(result):
    payment = item(result, "GEN-PAY-01")["risk_point_description"]
    assert all(value in payment for value in ("110%", "3,300,000", "300,000"))
    penalty = item(result, "GEN-LIAB-03")["risk_point_description"]
    assert "500万元" in penalty and "0.5%" in penalty


def test_improvement_existence_does_not_mean_fair_scope(result):
    for key in ("TC-10-01", "TC-10-02", "TC-10-04"):
        row = item(result, key)
        assert row["coverage_status"] == "风险条款"
        assert len(elements(row)) == 4
        assert all(e["evidence_ids"] for e in row["coverage_elements"])
    themes = [row for row in result["risk_themes"] if any(k in row["source_rule_ids"] for k in ("TC-10-01", "TC-10-02", "TC-10-04"))]
    assert len(themes) == 1


def test_generic_transfer_period_is_not_called_service(result):
    assert "服务开始" not in item(result, "TECH-SHARED-03")["risk_point_description"]


def test_missing_asymmetric_limb_does_not_manufacture_four_fact_conclusion(text):
    text = text.replace("卖方无需支付任何费用即可永久免费使用相关改进成果。", "使用改进成果的范围、期限和费用由双方另行公平协商。")
    result = engine.review_contract_v2(text, "technology", use_llm=False)
    assert not item(result, "TC-10-04")["decision_trace"].get("asymmetric_improvement_facts")


@pytest.mark.parametrize("actor, expected", [("买方", "LICENSEE"), ("卖方", "LICENSOR")])
def test_sentence_actor_controls_cost_allocation(actor, expected):
    text = f"技术转让合同。\n第六条 第三方权利\n卖方保证有权转让技术。第三方向买方提出侵权主张时，由{actor}承担律师费、诉讼费及赔偿费。卖方赔偿最高不超过价款10%。"
    facts = build_technology_fact_registry(text)["third_party_claim"]["response_element_evidence"]
    assert {row["actor"] for row in facts["claim_cost_allocation"]} == {expected}
    assert not facts.get("notification_requirement") and not facts.get("notification_deadline")


def test_negotiation_is_not_a_current_cost_or_damages_allocation():
    text = "第六条 第三方权利。第三方指控买方侵权时双方协商。律师费、诉讼费、赔偿责任及停产损失，由双方届时另行协商承担。"
    facts = build_technology_fact_registry(text)["third_party_claim"]["response_element_evidence"]
    assert facts["claim_trigger"]
    assert not facts.get("claim_cost_allocation")
    assert not facts.get("third_party_compensation_allocation")


def test_single_pledge_representation_never_covers_all_warranty_siblings(text):
    text = text.replace("卖方保证其有权转让本专利申请权", "卖方保证本专利申请权不存在质押。卖方保证其有权转让本专利申请权")
    result = engine.review_contract_v2(text, "technology", use_llm=False)
    for rule in ("TC-03-04", "TC-06-03", "TC-13-02"):
        rows = elements(item(result, rule))
        assert rows["application_pledge_disclosure"]["status"] == "COVERED"
        for key in ("coownership", "seizure", "other_restrictions"):
            assert rows[f"application_{key}_disclosure"]["status"] == "MISSING"


@pytest.mark.parametrize("fact_type", [
    "RECIPIENT_IMPROVEMENT_COOWNERSHIP", "RECIPIENT_IMPROVEMENT_DISPOSAL_VETO",
    "PROVIDER_FREE_IMPROVEMENT_USE", "PROVIDER_INDEPENDENT_IMPROVEMENT_OWNERSHIP",
])
def test_asymmetric_branch_gate_requires_every_independent_limb(result, fact_type):
    rows = deepcopy(result["risk_findings"])
    finding = next(row for row in rows if row["risk_group"] == "improvement_no_unlawful_restriction")
    bundle = finding["evidence_bundle"]
    original = bundle["items"]
    bundle["items"] = [row for row in original if fact_type not in (row.get("fact_types") or [row.get("fact_type")])]
    assert len(bundle["items"]) < len(original)
    audit = engine._technical_evidence_proposition_audit([SimpleNamespace(**row) for row in rows])
    assert audit["status"] == "FAIL"
