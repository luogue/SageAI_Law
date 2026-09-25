from pathlib import Path

from docx import Document

from review_v2.engine import review_contract_v2
from review_v2.technology_service_analysis import build_technology_fact_registry
from review_v2.user_profile import UserRiskProfile


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "test_data" / "27 专利实施许可（含后续开发）合同.docx"


def _claim_contract(*cap_clauses: str) -> str:
    return "\n".join([
        "甲方（被许可方）获得乙方（许可方）授予的专利实施许可。",
        (
            "被许可方因实施许可专利收到第三方知识产权主张时，应通知许可方；"
            "律师费、诉讼费、和解费、第三方赔偿及停产损失均由被许可方承担。"
        ),
        *cap_clauses,
    ])


def _cap_facts(text: str) -> dict:
    return build_technology_fact_registry(text)["third_party_claim"]


def test_neither_party_has_liability_cap():
    facts = _cap_facts(_claim_contract())

    assert facts["licensor_liability_cap"] is False
    assert facts["licensee_liability_cap"] is False
    assert facts["liability_cap_balance"] == "NO_CAPS"
    assert facts["liability_cap_imbalance"] is False
    assert facts["licensee_open_ended_infringement_liability"] is True


def test_only_licensor_has_liability_cap():
    facts = _cap_facts(_claim_contract(
        "许可方累计承担的全部赔偿责任，不超过被许可方已支付许可费的20%。"
    ))

    assert facts["licensor_liability_cap_percentage"] == 20
    assert facts["licensee_liability_cap"] is False
    assert facts["liability_cap_balance"] == "LICENSOR_ONLY"
    assert facts["liability_cap_imbalance"] is True


def test_only_licensee_has_liability_cap():
    facts = _cap_facts(_claim_contract(
        "被许可方累计承担的侵权赔偿责任，不超过合同总价的50%。"
    ))

    assert facts["licensor_liability_cap"] is False
    assert facts["licensee_liability_cap_percentage"] == 50
    assert facts["liability_cap_balance"] == "LICENSEE_ONLY"
    assert facts["liability_cap_imbalance"] is False
    assert facts["licensee_open_ended_infringement_liability"] is False


def test_both_parties_have_reasonably_balanced_caps():
    facts = _cap_facts(_claim_contract(
        "许可方累计承担的赔偿责任，不超过合同总价的50%。",
        "被许可方累计承担的侵权赔偿责任，不超过合同总价的50%。",
    ))

    assert facts["licensor_liability_cap_percentage"] == 50
    assert facts["licensee_liability_cap_percentage"] == 50
    assert facts["liability_cap_balance"] == "BOTH_BALANCED"
    assert facts["liability_cap_imbalance"] is False


def test_both_parties_have_materially_asymmetric_caps():
    facts = _cap_facts(_claim_contract(
        "许可方赔偿责任仍以被许可方已支付许可费的20%为上限。",
        "被许可方累计承担的侵权赔偿责任，不超过合同总价的100%。",
    ))

    assert facts["licensor_liability_cap_percentage"] == 20
    assert facts["licensee_liability_cap_percentage"] == 100
    assert facts["liability_cap_balance"] == "BOTH_ASYMMETRIC"
    assert facts["liability_cap_imbalance"] is True


def test_current_contract_reports_asymmetric_caps_instead_of_missing_cap():
    document = Document(str(FIXTURE))
    contract_text = "\n".join(
        paragraph.text for paragraph in document.paragraphs if paragraph.text.strip()
    )
    review = review_contract_v2(
        contract_text,
        "technology",
        include_low_risk=True,
        use_llm=False,
        profile=UserRiskProfile(user_identity="甲方/被许可方"),
    )
    item = next(row for row in review["items"] if row["item_id"] == "TC-12-04")
    elements = {row["element_id"]: row for row in item["coverage_elements"]}

    assert item["title"] == "侵权赔偿和责任上限"
    assert item["risk_level"] == "高"
    assert "双方责任范围及责任上限明显不对等" in item["risk_point_description"]
    assert "未设置责任上限" not in item["risk_point_description"]
    assert "重新平衡双方责任上限" in item["suggested_clause_example"]
    assert "故意、重大过失、未披露既有权利瑕疵" in item["suggested_clause_example"]
    assert elements["licensor_liability_cap"]["status"] == "ADVERSE"
    assert elements["licensee_liability_cap"]["status"] == "MISSING"
    assert elements["mutual_liability_cap"]["status"] == "ADVERSE"
    assert elements["liability_cap_exceptions"]["status"] == "MISSING"
