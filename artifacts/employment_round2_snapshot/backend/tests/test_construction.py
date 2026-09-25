"""Tests for the construction-contract adjudication engine."""

from datetime import date

from adjudicate.construction_configs import get_construction_config
from adjudicate.construction_engine import adjudicate_construction


TODAY = date(2026, 7, 27)


def test_construction_config_declares_core_mapping_and_patches():
    config = get_construction_config("construction")

    assert config.key == "construction"
    assert config.fact_mapping["核心争议"].startswith("合同是否有效")
    assert config.enabled_patches == tuple(f"C{i}" for i in range(1, 16))
    assert config.patch_mount("C5").node_id == "priority_payment"


def test_construction_jurisdiction_question():
    output = adjudicate_construction("建设工程合同纠纷去哪里起诉？", today=TODAY)

    assert "被告住所地或者合同履行地" in output["conclusion"]
    assert "管辖程序" in output["triggered_patches"]


def test_c11_survey_contract_uses_work_contract_rules():
    output = adjudicate_construction("本案为工程勘察合同，勘察人主张费用。", today=TODAY)

    assert "本案为勘察合同" in output["conclusion"]
    assert "勘察、设计合同纠纷的特殊处理" in output["triggered_patches"]


def test_c12_labor_subcontract_valid():
    output = adjudicate_construction("劳务分包合同，承包人具有劳务作业法定资质。", today=TODAY)

    assert "劳务分包合同有效" in output["conclusion"]
    assert "劳务分包合同的效力" in output["triggered_patches"]


def test_c3_black_white_contract_uses_bid_contract():
    output = adjudicate_construction("存在黑白合同，另行签订合同与中标合同工程价款不一致，实质性内容不一致。", today=TODAY)

    assert "应按中标合同确定权利义务" in output["conclusion"]
    assert "黑白合同的认定" in output["triggered_patches"]


def test_c4_affiliation_joint_liability():
    output = adjudicate_construction("无资质实际施工人借用资质挂靠施工，因出借资质造成损失20000元。", today=TODAY)

    assert "出借方与借用方对损失承担连带赔偿责任" in output["conclusion"]
    assert "出借资质（挂靠）的连带责任" in output["triggered_patches"]


def test_c1_invalid_contract_but_accepted_gets_discount_compensation():
    output = adjudicate_construction("建设工程施工合同无效，但工程竣工验收合格，承包人请求折价补偿工程价款100万元。", today=TODAY)

    assert "合同无效但工程验收合格" in output["conclusion"]
    assert "1000000.00 元" in output["conclusion"]
    assert "合同无效但工程合格的处理" in output["triggered_patches"]


def test_c2_invalid_contract_unaccepted_unrepairable_no_compensation():
    output = adjudicate_construction("施工合同无效，工程验收不合格，修复后仍不合格，不可修复。", today=TODAY)

    assert "承包人不可主张折价补偿" in output["conclusion"]
    assert "合同无效且工程不合格的处理" in output["triggered_patches"]


def test_c7_period_identification():
    output = adjudicate_construction("双方有工期争议，开工通知发出后不具备开工条件，发包人拖延验收，承包人提交竣工验收报告。", today=TODAY)

    assert "开工日期认定为开工条件具备之日" in output["conclusion"]
    assert "竣工日期认定为承包人提交竣工验收报告之日" in output["conclusion"]


def test_c13_unauthorized_use_sets_completion_date():
    output = adjudicate_construction("建设工程未经竣工验收，发包人擅自使用并转移占有。", today=TODAY)

    assert "竣工日期认定为转移占有之日" in output["conclusion"]
    assert "发包人擅自使用未验收工程的法律后果" in output["triggered_patches"]


def test_c14_hidden_work_inspection_delay():
    output = adjudicate_construction("隐蔽工程隐蔽前，承包人已通知发包人检查，但发包人未及时检查。", today=TODAY)

    assert "承包人可顺延工期并索赔损失" in output["conclusion"]
    assert "隐蔽工程检查" in output["triggered_patches"]


def test_c8_quality_deposit_return():
    output = adjudicate_construction("承包人请求返还工程质量保证金50000元，质保金返还期限届满。", today=TODAY)

    assert "工程质量保证金应返还" in output["conclusion"]
    assert "50000.00 元" in output["conclusion"]


def test_c10_project_price_interest():
    output = adjudicate_construction("发包人拖欠工程款，承包人主张工程款利息，未约定利率，按LPR，工程已实际交付，利息金额3000元。", today=TODAY)

    assert "工程款利息按LPR计算" in output["conclusion"]
    assert "工程实际交付之日" in output["conclusion"]


def test_c9_stoppage_loss_by_employer_breach():
    output = adjudicate_construction("发包人中途停建并未按约定提供资金，造成承包人停工窝工损失60000元。", today=TODAY)

    assert "发包人违约造成停工/窝工" in output["conclusion"]
    assert "60000.00 元" in output["conclusion"]


def test_c5_priority_payment_supported():
    output = adjudicate_construction("发包人拖欠工程款200万元，承包人已催告支付，在18个月内主张建设工程价款优先受偿权，工程质量合格。", today=TODAY)

    assert "承包人享有建设工程价款优先受偿权" in output["conclusion"]
    assert "优先于抵押权和其他债权" in output["conclusion"]


def test_c5_priority_payment_expired_after_18_months():
    output = adjudicate_construction("发包人欠付工程款，承包人主张优先受偿权，但已超过十八个月。", today=TODAY)

    assert "不再享有建设工程价款优先受偿权" in output["conclusion"]


def test_c6_actual_constructor_direct_sue_employer():
    output = adjudicate_construction("实际施工人直接起诉发包人，发包人欠付工程款80万元。", today=TODAY)

    assert "实际施工人可向发包人主张权利" in output["conclusion"]
    assert "800000.00 元" in output["conclusion"]


def test_c6_actual_constructor_subrogation():
    output = adjudicate_construction("实际施工人提起代位权诉讼，转包人怠于向发包人行使到期债权。", today=TODAY)

    assert "实际施工人可以提起代位权诉讼" in output["conclusion"]


def test_c15_employer_termination_for_illegal_subcontract():
    output = adjudicate_construction("发包人要求解除施工合同，承包人违法分包，已完工程质量合格。", today=TODAY)

    assert "发包人解除权成立" in output["conclusion"]
    assert "建设工程合同解除后的处理" in output["triggered_patches"]


def test_quality_defect_repair_rule():
    output = adjudicate_construction("工程存在质量问题，质量不符合约定，发包人要求无偿修理返工。", today=TODAY)

    assert "无偿修理、返工或者改建" in output["conclusion"]
