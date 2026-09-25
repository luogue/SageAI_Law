"""Tests for the warehouse-contract adjudication engine."""

from datetime import date

from adjudicate.warehouse_configs import get_warehouse_config
from adjudicate.warehouse_engine import adjudicate_warehouse


TODAY = date(2026, 7, 27)


def test_warehouse_config_declares_core_mapping_and_patches():
    config = get_warehouse_config("warehouse")

    assert config.key == "warehouse"
    assert config.fact_mapping["核心争议"].startswith("仓储物是否毁损灭失")
    assert config.enabled_patches == tuple(f"W{i}" for i in range(1, 16))
    assert config.patch_mount("W4").node_id == "damage_cause"


def test_warehouse_jurisdiction_question():
    output = adjudicate_warehouse("仓储合同纠纷去哪里起诉？", today=TODAY)

    assert "被告住所地或者合同履行地" in output["conclusion"]
    assert "管辖程序" in output["triggered_patches"]


def test_w1_classifies_warehouse_contract():
    output = adjudicate_warehouse("双方对合同性质争议，保管人以仓储为业，属于仓储营业公司，双方意思表示一致。", today=TODAY)

    assert "合同性质认定为仓储合同" in output["conclusion"]
    assert "仓储合同与保管合同的区分认定" in output["triggered_patches"]


def test_w1_classifies_general_safekeeping():
    output = adjudicate_warehouse("双方对合同性质争议，保管人只是亲友临时保管，不是仓储营业人。", today=TODAY)

    assert "合同性质认定为保管合同" in output["conclusion"]


def test_qualification_issue_routes_to_actual_safekeeping_relation():
    output = adjudicate_warehouse("仓储合同中保管人未取得仓储资质，并非仓储营业人。", today=TODAY)

    assert "不宜按仓储合同处理" in output["conclusion"]


def test_w2_receipt_transfer_valid_with_endorsement_and_keeper_seal():
    output = adjudicate_warehouse("仓单转让，仓单上背书，并经保管人盖章。", today=TODAY)

    assert "仓单转让有效" in output["conclusion"]
    assert "仓单的转让与质押效力" in output["triggered_patches"]


def test_w2_receipt_transfer_invalid_without_formalities():
    output = adjudicate_warehouse("仓单转让，但没有背书，也未经保管人签名盖章。", today=TODAY)

    assert "暂未取得对保管人的提货权" in output["conclusion"]


def test_w11_receipt_holder_identity_for_multiple_claimants():
    output = adjudicate_warehouse("多人主张提取仓储物，其中甲为合法持有仓单的仓单持有人。", today=TODAY)

    assert "合法仓单持有人有权提取仓储物" in output["conclusion"]
    assert "仓单持有人身份的认定" in output["triggered_patches"]


def test_w3_acceptance_notice_failure_causes_liability():
    output = adjudicate_warehouse("入库验收后发现质量不符，保管人未及时通知存货人。", today=TODAY)

    assert "应承担相应赔偿责任" in output["conclusion"]
    assert "保管人验收义务与责任" in output["triggered_patches"]


def test_w6_dangerous_goods_without_explanation():
    output = adjudicate_warehouse("仓储物为易燃危险物品，存货人隐瞒危险性质，未提供资料。", today=TODAY)

    assert "保管人可以拒收仓储物" in output["conclusion"]
    assert "危险物品/易变质物品的说明义务" in output["triggered_patches"]


def test_w4_exemption_for_bad_packaging():
    output = adjudicate_warehouse("仓储物在储存期内毁损灭失，保管人主张系包装不符合约定造成，货值30000元。", today=TODAY)

    assert "保管人不承担赔偿责任" in output["conclusion"]
    assert "保管人免责事由" in output["triggered_patches"]


def test_w4_improper_custody_liability():
    output = adjudicate_warehouse("仓储物在储存期内损坏，原因是仓库漏水、保管人保管不善，损失20000元。", today=TODAY)

    assert "保管人承担赔偿责任" in output["conclusion"]
    assert "20000.00 元" in output["conclusion"]


def test_w12_partial_damage_compensation_and_return():
    output = adjudicate_warehouse("仓储物部分毁损，一部分货物损失价值10000元，剩余部分完好。", today=TODAY)

    assert "未毁损部分应予返还" in output["conclusion"]
    assert "仓储物部分毁损/灭失的处理" in output["triggered_patches"]


def test_w15_value_depreciation_by_improper_custody():
    output = adjudicate_warehouse("仓储物未毁损但价值减损，因保管人保管不善导致贬值，损失价值8000元。", today=TODAY)

    assert "保管人应赔偿" in output["conclusion"]
    assert "仓储物价值减损的认定" in output["triggered_patches"]


def test_w13_notice_failure_for_deterioration():
    output = adjudicate_warehouse("保管人发现仓储物变质，但未及时通知存货人，导致损失扩大。", today=TODAY)

    assert "对扩大损失承担赔偿责任" in output["conclusion"]
    assert "保管人未尽通知义务的责任" in output["triggered_patches"]


def test_w7_emergency_disposal():
    output = adjudicate_warehouse("仓储物发现变质，危及其他仓储物安全，情况紧急，保管人紧急处置。", today=TODAY)

    assert "紧急处置权成立" in output["conclusion"]
    assert "保管人紧急处置权" in output["triggered_patches"]


def test_w8_early_retrieval_no_fee_reduction():
    output = adjudicate_warehouse("存货人提前提取仓储物，仓储费5000元，要求减收仓储费。", today=TODAY)

    assert "仓储费不减收" in output["conclusion"]
    assert "5000.00 元" in output["conclusion"]


def test_w5_overdue_retrieval_storage_fee_and_deposit():
    output = adjudicate_warehouse("储存期限届满，存货人逾期未提取，保管人已催告，要求加收仓储费3000元。", today=TODAY)

    assert "应加收仓储费" in output["conclusion"]
    assert "提存仓储物" in output["conclusion"]
    assert "逾期提取的加收费与提存规则" in output["triggered_patches"]


def test_w9_unclear_storage_period_allows_retrieval_with_preparation_time():
    output = adjudicate_warehouse("双方未约定储存期限，期限约定不明，存货人要求随时提取。", today=TODAY)

    assert "双方均可随时主张提取" in output["conclusion"]
    assert "必要的准备时间" in output["conclusion"]


def test_storage_fee_lien():
    output = adjudicate_warehouse("存货人欠付仓储费6000元，保管人主张对仓储物行使留置权。", today=TODAY)

    assert "可以依法行使留置权" in output["conclusion"]
    assert "6000.00 元" in output["conclusion"]


def test_w10_termination_with_statutory_reason():
    output = adjudicate_warehouse("存货人要求解除仓储合同，保管人拒绝履行，经催告仍未履行，合同目的不能实现。", today=TODAY)

    assert "仓储合同解除成立" in output["conclusion"]
    assert "仓储合同解除" in output["triggered_patches"]


def test_w14_depositor_assignment_valid():
    output = adjudicate_warehouse("存货人将仓储物转让给第三人，转让手续齐备，受让人提货。", today=TODAY)

    assert "受让人承继存货人的权利义务" in output["conclusion"]
    assert "存货人变更/转让后的权利义务" in output["triggered_patches"]
