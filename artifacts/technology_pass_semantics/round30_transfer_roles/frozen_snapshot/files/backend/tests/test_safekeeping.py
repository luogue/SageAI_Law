"""Tests for the safekeeping-contract adjudication engine."""

from datetime import date

from adjudicate.safekeeping_configs import get_safekeeping_config
from adjudicate.safekeeping_engine import adjudicate_safekeeping


def test_safekeeping_config_declares_core_mapping_and_patches():
    config = get_safekeeping_config("deposit")

    assert config.key == "deposit"
    assert config.fact_mapping["合同主体"] == "保管人/寄存人"
    assert config.fact_mapping["核心义务"] == "保管并返还原物（保管人不得使用）"
    assert config.fact_mapping["归责原则"] == "有偿=一般过失；无偿=故意或重大过失"
    assert set(config.reused_modules) == {"管辖", "适格被告", "合同效力", "违约金调减", "诉讼时效"}

    patch_ids = {mount.patch_id for mount in config.patch_mounts}
    assert patch_ids == {"S1", "S2", "S3", "S4", "S5", "S6", "S7", "S8", "S9", "S10"}
    for mount in config.patch_mounts:
        assert mount.node_id
        assert mount.mount_mode
        assert mount.patch_name
        assert mount.trigger_condition
        assert mount.legal_basis
        assert mount.logic
        assert mount.output_format


def test_safekeeping_jurisdiction_question_uses_general_contract_points():
    output = adjudicate_safekeeping(
        "保管合同纠纷去哪里起诉？",
        today=date(2026, 7, 27),
    )

    assert output["conclusion"] == "保管合同纠纷一般由被告住所地或者合同履行地人民法院处理；合同有有效管辖约定的，按约定处理"
    assert output["triggered_patches"] == ["管辖程序"]
    assert output["facts"]["asks_jurisdiction"] is True


def test_s1_classifies_venue_only_storage_as_site_lease():
    output = adjudicate_safekeeping(
        "合同名为保管合同，但实际是租用仓位自行存放物品，保管人不负责看管，双方对合同性质有争议。",
        today=date(2026, 7, 27),
    )

    assert output["triggered_patches"] == ["保管合同与租赁合同/场地租赁合同的定性"]
    assert output["conclusion"] == "合同性质认定为场地租赁合同，不适用本保管合同裁判引擎。"
    assert output["facts"]["venue_only"] is True


def test_s1_designated_restaurant_storage_is_safekeeping():
    output = adjudicate_safekeeping(
        "顾客在饭店就餐时将物品存放在指定柜台，保管人专人看管，物品丢失。",
        today=date(2026, 7, 27),
    )

    assert output["triggered_patches"] == ["保管合同与租赁合同/场地租赁合同的定性"]
    assert output["conclusion"] == "合同性质认定为保管合同，适用保管合同裁判规则。"
    assert output["facts"]["designated_place_activity"] is True


def test_s2_paid_safekeeping_general_negligence_requires_compensation():
    output = adjudicate_safekeeping(
        "有偿保管期间保管物丢失，保管人未尽妥善保管义务，物品价值10000元。",
        today=date(2026, 7, 27),
    )

    assert output["triggered_patches"] == ["有偿保管与无偿保管的责任标准"]
    assert output["conclusion"] == "保管合同为有偿保管，保管人未尽妥善保管义务，赔偿责任成立。赔偿金额按保管物实际损失或市场价值计算，为10000.00 元。"
    assert output["facts"]["paid_safekeeping"] is True
    assert output["facts"]["actual_loss"] == 10000


def test_s2_unpaid_safekeeping_without_intent_or_gross_negligence_is_exempt():
    output = adjudicate_safekeeping(
        "无偿保管期间保管物丢失，保管人证明自己没有故意或重大过失。",
        today=date(2026, 7, 27),
    )

    assert output["triggered_patches"] == ["有偿保管与无偿保管的责任标准"]
    assert output["conclusion"] == "保管合同为无偿保管，保管人已证明自己没有故意或重大过失，不承担赔偿责任。"
    assert output["facts"]["custodian_proves_no_intent_gross"] is True


def test_s3_unauthorized_transfer_safekeeping_requires_compensation():
    output = adjudicate_safekeeping(
        "保管人未经约定将保管物转交第三人保管，造成损失3000元。",
        today=date(2026, 7, 27),
    )

    assert output["triggered_patches"] == ["保管人擅自转保管"]
    assert output["conclusion"] == "保管人擅自转保管构成违约；造成损失的，应承担赔偿责任 3000.00 元。"
    assert output["facts"]["transfer_to_third"] is True


def test_s4_unauthorized_use_requires_compensation():
    output = adjudicate_safekeeping(
        "保管人未经约定擅自使用保管物，造成损坏损失2000元。",
        today=date(2026, 7, 27),
    )

    assert output["triggered_patches"] == ["保管人擅自使用保管物"]
    assert output["conclusion"] == "保管人擅自使用保管物构成违约；造成保管物损耗或损坏的，应承担赔偿责任 2000.00 元。"
    assert output["facts"]["custodian_used_item"] is True


def test_s5_undeclared_valuable_is_compensated_as_ordinary_item():
    output = adjudicate_safekeeping(
        "寄存人寄存名表等贵重物品未向保管人声明，保管期间丢失，实际价值50000元。",
        today=date(2026, 7, 27),
    )

    assert output["triggered_patches"] == ["贵重物品未声明"]
    assert output["conclusion"] == "寄存人未声明贵重物品，若保管人赔偿责任成立，赔偿范围按一般物品价值计算；保管人是否承担责任仍需结合有偿、无偿及保管过错审查。"
    assert output["facts"]["undeclared_valuable"] is True


def test_s6_consumptive_safekeeping_returns_same_kind_quantity_quality():
    output = adjudicate_safekeeping(
        "双方约定消费保管货币10000元，保管人到期应返还相同种类和数量的货币。",
        today=date(2026, 7, 27),
    )

    assert output["triggered_patches"] == ["消费保管"]
    assert output["conclusion"] == "属于消费保管，保管人应返还相同种类、数量、品质的货币或物品，而非必须返还原物。"
    assert output["facts"]["consumptive_safekeeping"] is True


def test_s7_custodian_lien_for_unpaid_fee():
    output = adjudicate_safekeeping(
        "寄存人未支付保管费800元，保管人留置保管物。",
        today=date(2026, 7, 27),
    )

    assert output["triggered_patches"] == ["保管人留置权"]
    assert output["conclusion"] == "保管人留置权成立，保管人可以留置与欠费相当的保管物；欠付费用为800.00 元。"
    assert output["facts"]["unpaid_fee"] is True


def test_s8_depositor_may_retrieve_at_any_time():
    output = adjudicate_safekeeping(
        "寄存人提前领取保管物，保管人拒绝返还。",
        today=date(2026, 7, 27),
    )

    assert output["triggered_patches"] == ["寄存人随时领取权"]
    assert output["conclusion"] == "寄存人有权随时领取，保管人应返还保管物及孳息；有偿保管费按实际保管期间结算。"
    assert output["facts"]["depositor_requests_return"] is True


def test_s9_item_nature_loss_without_disclosure_exempts_custodian():
    output = adjudicate_safekeeping(
        "寄存易腐物品但未告知特殊保管需求，保管物因自身性质变质。",
        today=date(2026, 7, 27),
    )

    assert output["triggered_patches"] == ["保管物自身性质导致的损失"]
    assert output["conclusion"] == "保管物自身性质导致损失，寄存人未履行告知义务，保管人不承担赔偿责任；保管人因此受损的，寄存人还应承担赔偿责任。"
    assert output["facts"]["depositor_not_disclosed"] is True


def test_s10_overdue_retrieval_after_period_expiry_shifts_extra_fee():
    output = adjudicate_safekeeping(
        "保管期限届满后寄存人逾期未领取，保管人催告后仍不领取，额外保管费500元。",
        today=date(2026, 7, 27),
    )

    assert output["triggered_patches"] == ["保管合同终止后的逾期领取"]
    assert output["conclusion"] == "保管期限已届满，寄存人应在合理期限内领取；逾期产生的额外保管费用由寄存人承担 500.00 元。"
    assert output["facts"]["depositor_overdue_retrieval"] is True


def test_damage_before_delivery_is_outside_custodian_responsibility_period():
    output = adjudicate_safekeeping(
        "保管物交付前已经损坏，寄存人要求保管人赔偿。",
        today=date(2026, 7, 27),
    )

    assert output["conclusion"] == "损失未发生在保管期间，保管人不承担保管合同项下的赔偿责任。"
    assert output["path"][-1] == "责任期间"
