"""Tests for the property-management adjudication engine."""

from datetime import date

from adjudicate.property_configs import get_property_config
from adjudicate.property_engine import adjudicate_property_management


def test_property_management_config_declares_core_mapping_and_patches():
    config = get_property_config("property_management")

    assert config.key == "property_management"
    assert config.fact_mapping["合同签订主体"] == "建设单位/业主委员会"
    assert config.fact_mapping["履约主体"] == "全体业主"
    assert set(config.reused_modules) == {"管辖", "适格被告", "合同效力", "违约金调减"}

    patch_ids = {mount.patch_id for mount in config.patch_mounts}
    assert patch_ids == {"M1", "M2", "M3", "M4", "M5", "M6", "M7"}
    for mount in config.patch_mounts:
        assert mount.node_id
        assert mount.mount_mode
        assert mount.patch_name
        assert mount.trigger_condition
        assert mount.legal_basis
        assert mount.logic
        assert mount.output_format


def test_property_jurisdiction_question_uses_real_estate_location():
    output = adjudicate_property_management(
        "物业服务合同纠纷应该去哪里起诉？",
        today=date(2026, 7, 27),
    )

    assert output["conclusion"] == "物业服务合同纠纷由不动产所在地人民法院处理，即房屋所在地人民法院"
    assert "管辖程序" in output["triggered_patches"]


def test_owner_not_signed_defense_is_not_supported():
    output = adjudicate_property_management(
        "物业起诉业主追缴物业费，业主说合同不是我签的，物业合同是业委会签的。",
        today=date(2026, 7, 27),
    )

    assert "不是我签" in output["conclusion"]
    assert "抗辩不成立" in output["conclusion"]
    assert "诉讼时效逐期计算" in output["triggered_patches"]


def test_property_fee_limitation_is_calculated_by_each_period():
    output = adjudicate_property_management(
        "物业起诉追缴2020年1月至2021年12月、2024年1月至2024年6月物业费，未提出服务瑕疵。",
        today=date(2026, 7, 27),
    )

    assert output["triggered_patches"] == ["诉讼时效逐期计算"]
    assert "2020年1月—2021年12月已超时效，不支持" in output["conclusion"]
    assert "2024年1月—2024年6月未超时效，支持" in output["conclusion"]


def test_illegal_collection_method_does_not_eliminate_fee_obligation():
    output = adjudicate_property_management(
        "业主欠物业费，物业公司停水停电并停用门禁卡催缴。",
        today=date(2026, 7, 27),
    )

    assert "催收方式合法性审查" in output["triggered_patches"]
    assert output["conclusion"] == "催收方式违法，物业不得以该方式催费，但物业费本体仍需缴纳。"


def test_dismissal_requires_owner_meeting_procedure():
    output = adjudicate_property_management(
        "业主主张已经解聘物业公司，但没有业主大会表决，只是部分业主决定更换物业。",
        today=date(2026, 7, 27),
    )

    assert output["triggered_patches"] == ["解聘程序合法性审查"]
    assert output["conclusion"] == "解聘程序不合法，解聘无效。未经业主大会依法表决或程序违法的，不能产生解聘物业公司的效力。"


def test_general_service_defect_can_reduce_property_fee():
    output = adjudicate_property_management(
        "业主拖欠物业费，抗辩物业多处服务不达标，多处公共区域脏乱，保洁经常不到位。",
        today=date(2026, 7, 27),
    )

    assert "物业费应缴金额" in output["path"]
    assert "瑕疵程度判断" in output["path"]
    assert "10%-30%" in output["conclusion"]


def test_non_property_responsibility_defect_does_not_reduce_fee():
    output = adjudicate_property_management(
        "业主以外墙漏水拒交物业费，称房屋主体结构存在问题。",
        today=date(2026, 7, 27),
    )

    assert output["conclusion"].startswith("该瑕疵不属于物业责任，不支持以此减免物业费")


def test_no_living_or_no_acceptance_defense_fails():
    output = adjudicate_property_management(
        "业主房屋空置一直没住，所以拒交物业费。",
        today=date(2026, 7, 27),
    )

    assert output["conclusion"] == "该抗辩不成立；物业已面向小区公共区域和全体业主提供服务的，业主应缴纳物业费；物业费诉讼时效应逐期计算，需补充欠费起止月份及催缴情形。"


def test_public_income_belongs_to_all_owners():
    output = adjudicate_property_management(
        "小区电梯广告产生公共收益5000元，物业主张可以扣除管理成本1000元。",
        today=date(2026, 7, 27),
    )

    assert output["triggered_patches"] == ["公共收益归属"]
    assert output["conclusion"] == "公共收益归全体业主共有，物业应返还 4000.00 元或抵扣物业费。"


def test_m5_factual_property_service_relationship_requires_fee_payment():
    output = adjudicate_property_management(
        "业主未签物业合同，但物业公司实际提供保洁安保设施维护，业主长期接受服务未提出异议，物业起诉追缴物业费。",
        today=date(2026, 7, 27),
    )

    assert output["triggered_patches"] == ["诉讼时效逐期计算", "事实物业服务关系"]
    assert output["conclusion"].startswith("双方形成事实上的物业服务合同关系，业主仍应支付物业费")


def test_m6_refusal_to_exit_blocks_post_termination_fee():
    output = adjudicate_property_management(
        "物业服务合同已终止，原物业公司拒不退场，并要求支付合同终止后的物业费。",
        today=date(2026, 7, 27),
    )

    assert output["triggered_patches"] == ["诉讼时效逐期计算", "合同终止后交接僵局"]
    assert output["conclusion"] == "原物业公司拒不退场，合同终止后的物业费不予支持；拒不移交资料造成业主损失的，原物业公司应承担赔偿责任。"


def test_m7_property_company_has_no_claim_to_cancel_owner_meeting_dismissal():
    output = adjudicate_property_management(
        "业主大会表决通过解聘物业公司，物业公司起诉撤销解聘决定。",
        today=date(2026, 7, 27),
    )

    assert output["triggered_patches"] == ["物业公司对业主大会解聘决定无诉权"]
    assert output["conclusion"] == "物业公司无权起诉要求撤销业主大会解聘决定，法院驳回起诉。"
