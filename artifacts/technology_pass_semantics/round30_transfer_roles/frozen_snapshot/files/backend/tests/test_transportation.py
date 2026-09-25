"""Tests for the transportation-contract adjudication engine."""

from datetime import date

from adjudicate.transport_configs import get_transport_config
from adjudicate.transport_engine import adjudicate_transportation


def test_transportation_config_declares_core_mapping_and_patches():
    config = get_transport_config("transportation")

    assert config.key == "transportation"
    assert config.fact_mapping["合同主体"] == "承运人/托运人/收货人"
    assert config.fact_mapping["核心义务"] == "安全、按时运输货物"
    assert config.fact_mapping["归责原则"] == "严格责任（举证责任倒置）"
    assert set(config.reused_modules) == {"管辖", "适格被告", "合同效力", "违约金调减"}

    patch_ids = {mount.patch_id for mount in config.patch_mounts}
    assert patch_ids == {"T1", "T2", "T3", "T4", "T5", "T6", "T7", "T8"}
    for mount in config.patch_mounts:
        assert mount.node_id
        assert mount.mount_mode
        assert mount.patch_name
        assert mount.trigger_condition
        assert mount.legal_basis
        assert mount.logic
        assert mount.output_format


def test_transport_jurisdiction_question_uses_transport_connection_points():
    output = adjudicate_transportation(
        "运输合同纠纷去哪里起诉？",
        today=date(2026, 7, 27),
    )

    assert output["conclusion"] == "运输合同纠纷可由运输始发地、目的地或者被告住所地人民法院处理"
    assert output["triggered_patches"] == ["管辖程序"]
    assert output["facts"]["asks_jurisdiction"] is True


def test_pure_third_party_tort_is_diverted_at_entry():
    output = adjudicate_transportation(
        "路人侵权损坏了货物，货主要求赔偿。",
        today=date(2026, 7, 27),
    )

    assert output["conclusion"] == "本案涉及侵权责任，非运输合同纠纷，不适用本运输合同裁判引擎"
    assert output["facts"]["third_party_tort"] is True


def test_t4_shipper_change_before_delivery_requires_compensation():
    output = adjudicate_transportation(
        "货物尚未交付收货人，托运人要求变更到达地，承运人产生空驶费500元。",
        today=date(2026, 7, 27),
    )

    assert output["conclusion"] == "托运人变更/解除有效，应赔偿承运人损失 500.00 元。"
    assert output["triggered_patches"] == ["托运人变更/解除的赔偿"]
    assert output["facts"]["carrier_loss"] == 500


def test_t5_carrier_lien_for_unpaid_freight():
    output = adjudicate_transportation(
        "托运人未支付运费800元，承运人留置相应货物。",
        today=date(2026, 7, 27),
    )

    assert output["conclusion"] == "承运人留置权成立，承运人可留置与欠费相应的运输货物。"
    assert output["triggered_patches"] == ["承运人留置权"]
    assert output["facts"]["unpaid_freight"] is True


def test_t6_lien_requires_same_legal_relationship():
    output = adjudicate_transportation(
        "托运人拖欠此前运费，承运人扣押当前批次货物，但欠费与当前运输属于多笔独立业务。",
        today=date(2026, 7, 27),
    )

    assert output["triggered_patches"] == ["承运人留置权", "留置权的同一法律关系限制"]
    assert output["conclusion"] == "欠付运费与当前货物不属于同一法律关系，承运人留置权不成立；承运人擅自扣货构成违约，造成损失的应承担赔偿责任。"
    assert output["facts"]["different_legal_relationship"] is True


def test_t7_contract_can_exclude_carrier_lien():
    output = adjudicate_transportation(
        "运输合同明确约定承运人不得留置货物，但托运人未支付运费，承运人仍扣货。",
        today=date(2026, 7, 27),
    )

    assert output["triggered_patches"] == ["承运人留置权", "合同排除留置权的效力"]
    assert output["conclusion"] == "合同明确排除留置权，承运人扣货构成违约；造成托运人损失的，承运人应承担赔偿责任。"
    assert output["facts"]["lien_excluded_by_contract"] is True


def test_t3_continuous_transport_keeps_signing_carrier_on_the_hook():
    output = adjudicate_transportation(
        "货物多式联运，签约承运人转包给区段承运人，运输途中货物损坏。",
        today=date(2026, 7, 27),
    )

    assert output["conclusion"] == "签约承运人承担全程责任，可向区段承运人追偿。"
    assert output["triggered_patches"] == ["连续运输/多式联运责任划分"]
    assert output["facts"]["continuous_transport"] is True


def test_t8_unknown_multimodal_segment_uses_maritime_limit():
    output = adjudicate_transportation(
        "货物多式联运运输途中损坏，无法查明区段，货值10000元。",
        today=date(2026, 7, 27),
    )

    assert output["triggered_patches"] == ["多式联运区段不明时的责任"]
    assert output["conclusion"] == "货损区段无法查明，适用《海商法》赔偿责任限额；不同运输方式赔偿标准差异较大，需补充运输单证、货物件数和重量。"
    assert output["facts"]["unknown_transport_segment"] is True


def test_t1_strict_liability_when_carrier_cannot_prove_exemption():
    output = adjudicate_transportation(
        "托运人将货物交给承运人，货物在运输过程中损坏，承运人无法证明免责事由，货值10000元。",
        today=date(2026, 7, 27),
    )

    assert output["triggered_patches"] == ["承运人严格责任 + 举证责任倒置"]
    assert "承运人未能证明免责事由" in output["conclusion"]
    assert "10000.00 元" in output["conclusion"]
    assert output["facts"]["market_price"] == 10000


def test_t1_exempts_carrier_when_exemption_and_causation_are_proven():
    output = adjudicate_transportation(
        "货物交给承运人后在运输过程中因洪水灭失，承运人证明洪水导致货损，与货损有因果关系。",
        today=date(2026, 7, 27),
    )

    assert output["conclusion"] == "承运人已证明货损系不可抗力造成，且该事由与货损之间存在因果关系，承运人免责。"
    assert output["triggered_patches"] == ["承运人严格责任 + 举证责任倒置"]
    assert output["facts"]["force_majeure"] is True


def test_t2_ignores_unexplained_valuation_clause_and_uses_market_price():
    output = adjudicate_transportation(
        "货物交给承运人后运输途中灭失，合同有限额赔偿500元但承运人未提示说明，货值10000元。",
        today=date(2026, 7, 27),
    )

    assert output["triggered_patches"] == ["承运人严格责任 + 举证责任倒置", "保价条款效力审查"]
    assert "保价条款无效，赔偿金额为 10000.00 元" in output["conclusion"]
    assert output["facts"]["carrier_no_explanation"] is True


def test_delay_delivery_uses_general_breach_rule():
    output = adjudicate_transportation(
        "承运人超过约定期限迟延送达，造成延迟损失2000元。",
        today=date(2026, 7, 27),
    )

    assert output["conclusion"] == "承运人构成延迟交付违约，应赔偿因此造成的损失 2000.00 元。"
    assert output["path"][-1] == "延迟交付"
    assert output["facts"]["delay_loss"] == 2000


def test_shipper_inaccurate_information_is_pre_entity_fault():
    output = adjudicate_transportation(
        "托运人瞒报危险品导致货损。",
        today=date(2026, 7, 27),
    )

    assert output["conclusion"] == "托运人未准确告知货物运输必要信息，应对因此造成的损失承担相应责任。"
    assert output["path"][-1] == "托运人义务审查"
    assert output["facts"]["shipper_info_inaccurate"] is True


def test_damage_before_loading_is_outside_carrier_responsibility_period():
    output = adjudicate_transportation(
        "货物在装货前已经破损，托运人要求承运人赔偿。",
        today=date(2026, 7, 27),
    )

    assert output["conclusion"] == "货损未发生在承运人责任期间内，承运人不承担赔偿责任。"
    assert output["path"][-1] == "责任期间"
