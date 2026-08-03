"""Tests for the technology-contract adjudication engine."""

from datetime import date

from adjudicate.technology_configs import get_technology_config
from adjudicate.technology_engine import adjudicate_technology


TODAY = date(2026, 7, 27)


def test_technology_config_declares_core_mapping_and_patches():
    config = get_technology_config("technology")

    assert config.key == "technology"
    assert config.fact_mapping["核心争议"].startswith("合同类型认定")
    assert config.enabled_patches == tuple(f"T{i}" for i in range(1, 16))
    assert config.patch_mount("T10").node_id == "contract_termination"


def test_technology_jurisdiction_question():
    output = adjudicate_technology("技术合同纠纷去哪里起诉？", today=TODAY)

    assert "被告住所地或者合同履行地" in output["conclusion"]
    assert "管辖程序" in output["triggered_patches"]


def test_t14_research_org_authorized_liability():
    output = adjudicate_technology("课题组签订合同，科研组织不具有民事主体资格，但经授权订立。", today=TODAY)

    assert "责任由授权组织承担" in output["conclusion"]
    assert "不具有民事主体资格的科研组织订立合同的责任承担" in output["triggered_patches"]


def test_t1_classifies_development_contract():
    output = adjudicate_technology("双方对技术合同类型存在争议，合同标的是研究开发新技术和新产品。", today=TODAY)

    assert "合同性质认定为技术开发合同" in output["conclusion"]
    assert "技术合同类型认定" in output["triggered_patches"]


def test_t1_excludes_work_or_construction_relation():
    output = adjudicate_technology("合同性质争议，名为技术服务，但实为承揽合同，加工定作成果。", today=TODAY)

    assert "不宜按技术合同处理" in output["conclusion"]


def test_t15_technology_import_export_special_rules():
    output = adjudicate_technology("本案为技术进出口合同，涉及进口技术许可。", today=TODAY)

    assert "优先适用技术进出口相关法律法规" in output["conclusion"]
    assert "技术进出口合同的特殊规定" in output["triggered_patches"]


def test_t13_fraud_contract_revocable():
    output = adjudicate_technology("一方以现有技术冒充委托开发标的，欺诈订立技术合同并重复收费。", today=TODAY)

    assert "受损害方可以请求撤销合同" in output["conclusion"]
    assert "欺诈订立技术合同的撤销" in output["triggered_patches"]


def test_t11_good_faith_use_after_trade_secret_invalid():
    output = adjudicate_technology("侵害他人技术秘密的技术合同无效，受让方善意取得该技术秘密，应支付合理使用费20000元。", today=TODAY)

    assert "善意取得方可以继续在原范围内使用技术秘密" in output["conclusion"]
    assert "20000.00 元" in output["conclusion"]


def test_t3_illegal_monopoly_invalid():
    output = adjudicate_technology("技术合同限制新的研究开发，并限制从其他渠道吸收技术，构成非法垄断技术。", today=TODAY)

    assert "合同构成非法垄断技术，无效" in output["conclusion"]
    assert "非法垄断技术的认定" in output["triggered_patches"]


def test_t2_duty_achievement_belongs_to_unit():
    output = adjudicate_technology("双方有技术成果权属争议，该成果属于职务技术成果，系履行岗位职责完成。", today=TODAY)

    assert "权属归单位" in output["conclusion"]
    assert "职务技术成果 vs 非职务技术成果的认定" in output["triggered_patches"]


def test_t10_termination_after_30_days():
    output = adjudicate_technology("一方迟延履行主要债务，另一方经催告后超过30日仍未履行，主张解除技术合同。", today=TODAY)

    assert "另一方可以解除合同" in output["conclusion"]
    assert "技术合同解除的催告期限" in output["triggered_patches"]


def test_t4_development_failure_reasonable_sharing():
    output = adjudicate_technology("技术开发合同研发失败，合同没有风险分担约定，双方对损失分担有争议。", today=TODAY)

    assert "风险由各方根据投入、过错等因素合理分担" in output["conclusion"]
    assert "技术开发合同的风险分担" in output["triggered_patches"]


def test_t5_commissioned_development_patent_application_right():
    output = adjudicate_technology("委托开发完成发明创造，双方未约定专利申请权归属。", today=TODAY)

    assert "专利申请权归研究开发人" in output["conclusion"]
    assert "委托开发成果的专利申请权归属" in output["triggered_patches"]


def test_t6_technical_secret_result_shared_without_agreement():
    output = adjudicate_technology("合作开发完成技术秘密成果，双方没有约定成果归属。", today=TODAY)

    assert "双方均有使用和转让的权利" in output["conclusion"]
    assert "技术秘密成果的使用权/转让权归属" in output["triggered_patches"]


def test_t7_license_infringement_by_licensor_when_used_as_agreed():
    output = adjudicate_technology("技术许可合同中，被许可人按约定实施专利，结果侵犯第三人专利。", today=TODAY)

    assert "侵权责任由让与人或许可人承担" in output["conclusion"]
    assert "技术许可合同侵权责任的承担" in output["triggered_patches"]


def test_t12_followup_improvement_belongs_to_improver():
    output = adjudicate_technology("一方完成后续改进成果，合同没有分享约定，另一方主张分享。", today=TODAY)

    assert "后续改进成果归改进方" in output["conclusion"]
    assert "他方无权分享" in output["conclusion"]


def test_licensor_breach_returns_fee():
    output = adjudicate_technology("技术许可合同中，许可人未按约定许可技术，未交付技术资料。", today=TODAY)

    assert "返还部分或全部使用费" in output["conclusion"]


def test_licensee_unpaid_fee_breach():
    output = adjudicate_technology("被许可人未支付使用费，拖欠使用费。", today=TODAY)

    assert "被许可人应补交使用费并支付违约金" in output["conclusion"]


def test_t8_consulting_decision_risk_by_client():
    output = adjudicate_technology("技术咨询合同中，咨询报告符合约定，委托人按咨询报告决策造成损失。", today=TODAY)

    assert "由委托人承担" in output["conclusion"]
    assert "技术咨询合同决策风险承担" in output["triggered_patches"]


def test_t9_new_result_belongs_to_trustee():
    output = adjudicate_technology("技术服务合同履行过程中产生新的技术成果，受托人利用委托人提供的技术资料和工作条件完成。", today=TODAY)

    assert "新技术成果归受托人所有" in output["conclusion"]
    assert "技术咨询/服务合同的新技术成果归属" in output["triggered_patches"]
