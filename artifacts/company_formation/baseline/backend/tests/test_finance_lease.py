"""Tests for the finance-lease adjudication engine."""

from datetime import date

from adjudicate.finance_lease_configs import get_finance_lease_config
from adjudicate.finance_lease_engine import adjudicate_finance_lease


TODAY = date(2026, 7, 27)


def test_finance_lease_config_declares_core_mapping_and_patches():
    config = get_finance_lease_config("finance_lease")

    assert config.key == "finance_lease"
    assert config.fact_mapping["核心争议"].startswith("是否构成融资租赁法律关系")
    assert config.enabled_patches == tuple(f"F{i}" for i in range(1, 16))
    assert config.patch_mount("F4").node_id == "rent_remedy_choice"


def test_finance_lease_jurisdiction_question():
    output = adjudicate_finance_lease("融资租赁合同纠纷去哪里起诉？", today=TODAY)

    assert "被告住所地或者合同履行地" in output["conclusion"]
    assert "管辖程序" in output["triggered_patches"]


def test_f1_non_finance_lease_by_substance():
    output = adjudicate_finance_lease("双方对合同性质争议，名为融资租赁，但实为借款，只有融资没有融物。", today=TODAY)

    assert "不构成融资租赁法律关系" in output["conclusion"]
    assert "融资租赁法律关系认定" in output["triggered_patches"]


def test_f8_sale_leaseback_is_not_denied_only_for_same_person():
    output = adjudicate_finance_lease("本案为售后回租，承租人和出卖人是同一人，租赁物真实存在。", today=TODAY)

    assert "售后回租构成融资租赁法律关系" in output["conclusion"]
    assert "售后回租认定" in output["triggered_patches"]


def test_f2_fake_asset_invalidates_contract():
    output = adjudicate_finance_lease("融资租赁交易中租赁物不存在，是虚构租赁物。", today=TODAY)

    assert "融资租赁合同无效" in output["conclusion"]
    assert "虚构租赁物合同无效" in output["triggered_patches"]


def test_f15_invalid_contract_returns_asset_to_lessor_without_agreement():
    output = adjudicate_finance_lease("融资租赁合同无效，双方没有合同无效后租赁物归属约定。", today=TODAY)

    assert "租赁物应返还出租人" in output["conclusion"]
    assert "合同无效时租赁物归属" in output["triggered_patches"]


def test_admin_license_issue_does_not_automatically_invalidate_contract():
    output = adjudicate_finance_lease("承租人没有行政许可，经营使用需行政许可，出租人主张融资租赁合同无效。", today=TODAY)

    assert "不当然导致融资租赁合同无效" in output["conclusion"]


def test_delivery_refusal_is_supported_for_serious_nonconformity():
    output = adjudicate_finance_lease("出卖人交付的租赁物严重不符合约定，承租人拒绝受领并及时通知出租人。", today=TODAY)

    assert "承租人拒绝受领成立" in output["conclusion"]


def test_f3_lessor_no_quality_liability_when_lessee_selected_asset():
    output = adjudicate_finance_lease("租赁物有质量瑕疵，但承租人自行选择出卖人和租赁物。", today=TODAY)

    assert "出租人不承担租赁物质量瑕疵担保责任" in output["conclusion"]
    assert "出租人瑕疵担保责任例外" in output["triggered_patches"]


def test_f3_lessor_has_quality_liability_when_intervening_choice():
    output = adjudicate_finance_lease("租赁物质量瑕疵，出租人干预选择并决定选择出卖人。", today=TODAY)

    assert "出租人应承担租赁物质量瑕疵担保责任" in output["conclusion"]


def test_f12_wrongful_repossession():
    output = adjudicate_finance_lease("出租人无正当理由收回租赁物，妨碍承租人占有使用。", today=TODAY)

    assert "出租人构成妨碍" in output["conclusion"]
    assert "出租人妨碍占有使用责任" in output["triggered_patches"]


def test_f14_third_party_damage_during_lessee_possession():
    output = adjudicate_finance_lease("租赁物在承租人占有期间造成第三人损害。", today=TODAY)

    assert "出租人不承担责任" in output["conclusion"]
    assert "租赁物致人损害责任" in output["triggered_patches"]


def test_f10_sale_contract_invalid_with_lessee_choice():
    output = adjudicate_finance_lease("买卖合同无效导致融资租赁合同解除，租赁物由承租人选择。", today=TODAY)

    assert "出租人有权向承租人主张赔偿损失" in output["conclusion"]
    assert "买卖合同无效导致解除的处理" in output["triggered_patches"]


def test_f11_repurchase_guarantee_with_conditions():
    output = adjudicate_finance_lease("融资租赁交易存在出卖人回购担保，回购条件成就，回购人公司决议齐备。", today=TODAY)

    assert "回购人应履行回购义务" in output["conclusion"]
    assert "回购担保认定与处理" in output["triggered_patches"]


def test_f13_contract_assignment_continues():
    output = adjudicate_finance_lease("出租人转让融资租赁合同项下权利，受让方请求解除合同。", today=TODAY)

    assert "合同继续有效" in output["conclusion"]
    assert "融资租赁合同转让影响" in output["triggered_patches"]


def test_f4_lessor_cannot_choose_both_rent_and_repossession():
    output = adjudicate_finance_lease(
        "承租人欠付租金，经催告后仍未支付，出租人同时请求全部租金和解除合同收回租赁物。",
        today=TODAY,
    )

    assert "不能同时获得" in output["conclusion"]
    assert "承租人违约时出租人救济方式选择" in output["triggered_patches"]


def test_f9_termination_loss_after_repossession():
    output = adjudicate_finance_lease(
        "承租人欠付租金2期，经催告后仍未支付，出租人解除合同收回租赁物并主张损失赔偿，全部未付租金及其他费用100000元，收回租赁物价值70000元。",
        today=TODAY,
    )

    assert "30000.00 元" in output["conclusion"]
    assert "解除收回后的损失赔偿计算" in output["triggered_patches"]


def test_f5_asset_loss_by_lessee_fault_keeps_rent_obligation():
    output = adjudicate_finance_lease("租赁物在承租人占有期间毁损灭失，因承租人保管不善造成。", today=TODAY)

    assert "继续支付租金" in output["conclusion"]
    assert "租赁物毁损灭失后租金义务" in output["triggered_patches"]


def test_f6_unregistered_ownership_cannot_defeat_good_faith_third_party():
    output = adjudicate_finance_lease("承租人擅自处分租赁物，所有权未登记，第三人善意取得。", today=TODAY)

    assert "不得以未登记的所有权对抗善意第三人" in output["conclusion"]
    assert "所有权登记与善意取得" in output["triggered_patches"]


def test_term_end_symbolic_price_transfers_ownership_to_lessee():
    output = adjudicate_finance_lease("合同约定租赁期满归承租人所有，承租人支付一元象征性价款后过户。", today=TODAY)

    assert "租赁物所有权归承租人" in output["conclusion"]


def test_f7_value_settlement_refunds_surplus():
    output = adjudicate_finance_lease(
        "期满归承租人，承租人已支付大部分租金但无力支付剩余租金，出租人收回租赁物。租赁物价值80000元，欠付租金及其他费用50000元。",
        today=TODAY,
    )

    assert "出租人应返还" in output["conclusion"]
    assert "30000.00 元" in output["conclusion"]
    assert "租赁物收回后的价值清算" in output["triggered_patches"]
