"""Tests for the utility-supply-contract adjudication engine."""

from datetime import date

from adjudicate.utility_supply_configs import get_utility_supply_config
from adjudicate.utility_supply_engine import adjudicate_utility_supply


TODAY = date(2026, 7, 27)


def test_utility_supply_config_declares_core_mapping_and_patches():
    config = get_utility_supply_config("utility_supply")

    assert config.key == "utility_supply"
    assert config.fact_mapping["核心争议"].startswith("供应质量是否达标")
    assert config.enabled_patches == tuple(f"U{i}" for i in range(1, 16))
    assert config.patch_mount("U6").node_id == "payment_dispute"


def test_utility_supply_jurisdiction_question():
    output = adjudicate_utility_supply("供用电合同纠纷去哪里起诉？", today=TODAY)

    assert "被告住所地或者合同履行地" in output["conclusion"]
    assert "管辖程序" in output["triggered_patches"]


def test_u1_water_supply_refers_to_power_supply_rules():
    output = adjudicate_utility_supply("供用水合同适用什么规则，是否参照适用供用电合同规定？", today=TODAY)

    assert "本案为供用水合同" in output["conclusion"]
    assert "参照适用供用电合同" in output["conclusion"]
    assert "合同类型的识别与参照适用" in output["triggered_patches"]


def test_u2_mandatory_contracting_breach():
    output = adjudicate_utility_supply("供电公司向社会公众供电，用户资料齐全且符合开户条件，但供电公司拒绝开户。", today=TODAY)

    assert "违反强制缔约义务" in output["conclusion"]
    assert "强制缔约义务" in output["triggered_patches"]


def test_u11_actual_supply_relation_without_written_contract():
    output = adjudicate_utility_supply("双方未签书面合同，但供电公司已经实际供电，用户一直使用并支付电费。", today=TODAY)

    assert "供用合同关系成立" in output["conclusion"]
    assert "未签订书面合同的供用关系认定" in output["triggered_patches"]


def test_u3_supply_quality_nonconform_liability_and_fee_reduction():
    output = adjudicate_utility_supply("供电质量不达标，电压不稳，不符合国家标准，造成用户损失2000元。", today=TODAY)

    assert "应承担赔偿责任" in output["conclusion"]
    assert "减免使用费" in output["conclusion"]
    assert "2000.00 元" in output["conclusion"]


def test_u4_interruption_without_prior_notice_liability():
    output = adjudicate_utility_supply("供电公司计划检修中断供电，但没有事先通知用户，造成损失1500元。", today=TODAY)

    assert "未履行中断供应的事先通知义务" in output["conclusion"]
    assert "1500.00 元" in output["conclusion"]
    assert "中断供应的通知义务" in output["triggered_patches"]


def test_u5_natural_disaster_without_timely_repair_liability():
    output = adjudicate_utility_supply("台风自然灾害导致断电，供电公司没有及时抢修，造成损失3000元。", today=TODAY)

    assert "未及时抢修" in output["conclusion"]
    assert "3000.00 元" in output["conclusion"]
    assert "自然灾害断电后的抢修义务" in output["triggered_patches"]


def test_u6_fee_suspension_legal_after_notice_period_and_procedure():
    output = adjudicate_utility_supply("用户拖欠电费，供电公司经催告后给予合理期限，用户仍未支付，供电公司按国家规定程序中止供电。", today=TODAY)

    assert "中止供应程序合法" in output["conclusion"]
    assert "欠费中止供应的法定程序" in output["triggered_patches"]


def test_u6_fee_suspension_illegal_without_notice():
    output = adjudicate_utility_supply("用户拖欠水费，自来水公司直接停水，没有催告，也没有给予合理期限。", today=TODAY)

    assert "中止供应程序不合法" in output["conclusion"]


def test_u7_illegal_use_causes_supplier_loss():
    output = adjudicate_utility_supply("用户窃电，属于违法用电，造成供应方损失5000元。", today=TODAY)

    assert "用户存在违规使用行为" in output["conclusion"]
    assert "5000.00 元" in output["conclusion"]
    assert "用户违规使用的责任" in output["triggered_patches"]


def test_u8_sub_supply_without_consent_breach():
    output = adjudicate_utility_supply("用户未经供应方同意，私自接给邻居用电，向第三方转供。", today=TODAY)

    assert "违规转供" in output["conclusion"]
    assert "承担违约责任" in output["conclusion"]
    assert "转供的处理" in output["triggered_patches"]


def test_u9_meter_error_overcharge_refund():
    output = adjudicate_utility_supply("双方发生计量争议，电表故障导致多收费用1000元。", today=TODAY)

    assert "按实际用量重新计算" in output["conclusion"]
    assert "多退" in output["conclusion"]
    assert "1000.00 元" in output["conclusion"]


def test_u10_facility_maintenance_user_side():
    output = adjudicate_utility_supply("供用设施损坏，双方有设施维护责任争议，损坏发生在产权分界处用户侧。", today=TODAY)

    assert "设施维护责任由用户承担" in output["conclusion"]
    assert "设施维护责任的认定" in output["triggered_patches"]


def test_u12_property_company_cutoff_illegal():
    output = adjudicate_utility_supply("物业公司以业主未交物业费为由断水断电，造成损失800元。", today=TODAY)

    assert "物业公司断水断电不合法" in output["conclusion"]
    assert "恢复供应并赔偿损失" in output["conclusion"]


def test_u13_heating_temperature_with_evidence_allows_fee_reduction():
    output = adjudicate_utility_supply("供暖温度不达标，用户拒交供暖费，并保留了投诉记录、维修记录和测温单。", today=TODAY)

    assert "供暖温度不达标主张成立" in output["conclusion"]
    assert "减免供暖费" in output["conclusion"]


def test_u13_heating_temperature_without_evidence_rejected():
    output = adjudicate_utility_supply("暖气不热，用户拒交供暖费，但没有测温证据，也没有投诉记录。", today=TODAY)

    assert "主张不成立" in output["conclusion"]


def test_u14_excessive_liquidated_damage_adjusted():
    output = adjudicate_utility_supply("用户欠费，供应方主张违约金5000元，用户请求调整，实际损失1000元。", today=TODAY)

    assert "违约金过高" in output["conclusion"]
    assert "应予以调减" in output["conclusion"]
    assert "违约金过高的调整" in output["triggered_patches"]


def test_u15_restore_time_commitment_breached():
    output = adjudicate_utility_supply("供电公司停电公告明确恢复供电时间，但超过承诺时间仍未恢复，违反承诺，造成损失2000元。", today=TODAY)

    assert "供应方已作出承诺且违反承诺" in output["conclusion"]
    assert "2000.00 元" in output["conclusion"]
    assert "供应方的承诺效力" in output["triggered_patches"]
