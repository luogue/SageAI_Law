"""Primary research commissions must retain their ancillary support module."""

from pathlib import Path

import pytest

from layers.input_layer import InputLayer
from review_v2.clause_parser import parse_contract_clauses
from review_v2.domain_selection import resolve_domain_selection
from review_v2.technology_service_analysis import (
    analyze_primary_transaction,
    classify_technology_transaction,
)


ROOT = Path(__file__).resolve().parents[2]


def _fixture_text() -> str:
    fixture = next((ROOT / "test_data").glob("47 *.docx"))
    return InputLayer()._extract_from_docx_content(fixture.read_bytes())


def _form_contract() -> str:
    return """合同编号：RESEARCH-OTHER
委托方（甲方）：星河材料公司
受托方（乙方）：明光研究公司
第一条 研究开发要求
技术目标：研发一种耐腐蚀复合材料及配套制备工艺。
第二条 研究开发计划
乙方应在生效后二十日内提交研究开发计划，列明试验、验证和阶段里程碑。
第三条 研究开发经费及报酬
总额：人民币720000元，按阶段支付，试制完成后支付尾款。
第四条 成果交付
乙方完成试验并向甲方交付全部研究开发成果，包括样品和制备工艺文件。
第五条 技术指导及培训
乙方在成果交付后提供六个月技术支持，包括系统部署、参数配置和技术人员培训。
合同总价已包含上述技术服务费用。
"""


def test_real_form_contract_uses_research_performance_as_primary_transaction():
    text = _fixture_text()
    classification = classify_technology_transaction(text)

    assert classification["primary_subtype"] == "ENTRUSTED_DEVELOPMENT"
    assert classification["primary_contract_type"] == "commissioned_development"
    assert classification["transaction_structure"] == "B2B_ENTRUSTED_DEVELOPMENT"
    assert classification["scenario"] == "ENTRUSTED_DEVELOPMENT"
    assert classification["primary_transaction_model"]["type"] == "ENTRUSTED_DEVELOPMENT"
    assert classification["primary_transaction_model"]["development_semantics"]["is_primary_commission"]
    assert classification["secondary_modules"] == ["TECHNICAL_SERVICE"]
    assert set(classification["active_transaction_types"]) == {
        "ENTRUSTED_DEVELOPMENT", "TECHNICAL_SERVICE",
    }
    assert "COMMISSIONED_DEVELOPMENT" not in classification["secondary_modules"]

    service = classification["structured_facts"]["technical_service"]
    assert service["content"] is True
    assert service["included_in_main_price"] is True
    assert "系统部署" in service["activities"]
    assert "模型训练" not in service["activities"]
    assert set(classification["ancillary_obligations"]) >= {
        "TECHNICAL_SUPPORT", "TRAINING",
    }
    assert any(
        "研究开发经费" in quote
        for quote in classification["classification_evidence_details"]["consideration_nature"]
    )


def test_real_form_contract_overrides_selected_service_domain():
    text = _fixture_text()
    resolution, _, routed_type = resolve_domain_selection(
        "service", text, parse_contract_clauses(text),
    )

    assert routed_type == "technology"
    assert resolution.document_domain["primary_subtype"] == "ENTRUSTED_DEVELOPMENT"
    assert resolution.document_domain["primary_contract_type"] == "commissioned_development"


def test_form_research_structure_is_not_tied_to_a_project_name_amount_or_title():
    text = _form_contract()
    classification = classify_technology_transaction(text)
    primary = analyze_primary_transaction(text)

    assert classification["primary_subtype"] == "ENTRUSTED_DEVELOPMENT"
    assert primary["type"] == "ENTRUSTED_DEVELOPMENT"
    assert primary["dominant_family"] == "TECHNOLOGY"
    assert primary["primary_consideration"] == ["research funding and development remuneration"]


@pytest.mark.parametrize("title", [
    "技术开发（委托）合同", "技术开发(委托)合同", "技术开发合同（委托）",
])
def test_parenthesized_entrusted_development_title_is_recognized(title):
    classification = classify_technology_transaction(title + "\n" + _form_contract())

    assert classification["title_transaction_type"] == "ENTRUSTED_DEVELOPMENT"
    assert classification["primary_subtype"] == "ENTRUSTED_DEVELOPMENT"
    assert classification["contract_type_conflict"]["exists"] is False


def test_removing_ancillary_support_does_not_change_research_primary_type():
    classification = classify_technology_transaction(_form_contract().split("第五条")[0])

    assert classification["primary_subtype"] == "ENTRUSTED_DEVELOPMENT"
    assert "TECHNICAL_SERVICE" not in classification["secondary_modules"]


def test_ordinary_technical_service_does_not_become_research_from_development_words():
    text = """技术服务合同
委托方（甲方）：设备公司
受托方（乙方）：技术公司
第一条 技术服务内容
乙方负责现有系统部署、模型训练、参数优化和技术人员培训，提交测试报告。
甲方支付技术服务费用300000元。
第二条 服务边界
本合同不承担研究开发工作，不交付研发成果。
甲方可提供历史研究开发计划、研发目标和研究开发经费预算供乙方了解已有技术。
"""
    classification = classify_technology_transaction(text)

    assert classification["primary_subtype"] == "TECHNICAL_SERVICE"
    assert classification["primary_transaction_model"]["development_semantics"]["is_primary_commission"] is False
    assert "COMMISSIONED_DEVELOPMENT" not in classification["secondary_modules"]


def test_reference_to_research_without_developer_obligation_does_not_trigger_core():
    text = _form_contract().replace(
        "乙方应在生效后二十日内提交研究开发计划，列明试验、验证和阶段里程碑。",
        "研究开发计划由甲方自行制订，乙方不承担研究开发工作。",
    ).replace(
        "乙方完成试验并向甲方交付全部研究开发成果，包括样品和制备工艺文件。",
        "交付全部研究开发成果的安排仅供参考，乙方不承担成果形成义务。",
    )

    assert analyze_primary_transaction(text)["development_semantics"]["is_primary_commission"] is False
