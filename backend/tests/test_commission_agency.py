"""Tests for the commission-agency-contract adjudication engine."""

from datetime import date

from adjudicate.commission_agency_configs import get_commission_agency_config
from adjudicate.commission_agency_engine import adjudicate_commission_agency


TODAY = date(2026, 7, 27)


def test_commission_agency_config_declares_core_mapping_and_patches():
    config = get_commission_agency_config("commission_agency")

    assert config.key == "commission_agency"
    assert config.fact_mapping["核心争议"].startswith("合同性质认定")
    assert config.enabled_patches == tuple(f"J{i}" for i in range(1, 16))
    assert config.patch_mount("J4").node_id == "third_party_default"


def test_commission_agency_jurisdiction_question():
    output = adjudicate_commission_agency("行纪合同纠纷去哪里起诉？", today=TODAY)

    assert "被告住所地或者合同履行地" in output["conclusion"]
    assert "管辖程序" in output["triggered_patches"]


def test_j1_classifies_commission_agency_contract():
    output = adjudicate_commission_agency("双方有合同性质争议，行纪人以自己名义为委托人从事代销贸易活动。", today=TODAY)

    assert "合同性质认定为行纪合同" in output["conclusion"]
    assert "行纪合同的性质认定" in output["triggered_patches"]


def test_j1_classifies_agency_contract_when_principal_name_used():
    output = adjudicate_commission_agency("合同性质争议，受托人以委托人名义与第三人交易。", today=TODAY)

    assert "更接近委托合同" in output["conclusion"]


def test_j1_classifies_intermediary_contract():
    output = adjudicate_commission_agency("合同性质争议，乙方只是报告订约机会并提供媒介服务。", today=TODAY)

    assert "更接近中介合同" in output["conclusion"]


def test_j15_oral_contract_with_evidence_established():
    output = adjudicate_commission_agency("双方没有书面合同，仅口头约定行纪事务，但有聊天记录和交易记录证明。", today=TODAY)

    assert "行纪合同成立" in output["conclusion"]
    assert "行纪合同未采用书面形式" in output["triggered_patches"]


def test_j14_identity_confusion_claim_not_established():
    output = adjudicate_commission_agency("行纪人身份混同，无法区分身份，不能证明委托物属于行纪事务。", today=TODAY)

    assert "主张不成立" in output["conclusion"]
    assert "行纪人身份混同的处理" in output["triggered_patches"]


def test_j8_improper_custody_liability():
    output = adjudicate_commission_agency("委托物在行纪人占有期间毁损，因行纪人保管不善造成损失8000元。", today=TODAY)

    assert "应承担赔偿责任" in output["conclusion"]
    assert "8000.00 元" in output["conclusion"]
    assert "行纪人妥善保管义务" in output["triggered_patches"]


def test_j9_expense_burden_without_agreement():
    output = adjudicate_commission_agency("行纪人要求报销处理事务费用3000元，合同没有费用另有约定。", today=TODAY)

    assert "由行纪人自行负担" in output["conclusion"]
    assert "行纪人费用负担" in output["triggered_patches"]


def test_j12_sub_entrustment_without_consent_full_liability():
    output = adjudicate_commission_agency("行纪人转委托，交给第三人处理，未取得委托人同意。", today=TODAY)

    assert "承担全部责任" in output["conclusion"]
    assert "行纪合同与转委托" in output["triggered_patches"]


def test_j10_malicious_collusion_full_liability():
    output = adjudicate_commission_agency("行纪人与第三人恶意串通，损害委托人利益，造成损失5000元。", today=TODAY)

    assert "承担全部赔偿责任" in output["conclusion"]
    assert "恶意串通" in output["triggered_patches"][0]


def test_j4_third_party_default_compensation():
    output = adjudicate_commission_agency("行纪人与第三人订立合同后，第三人不履行付款义务，致使委托人受损，损失6000元。", today=TODAY)

    assert "行纪人应向委托人承担赔偿责任" in output["conclusion"]
    assert "6000.00 元" in output["conclusion"]
    assert "行纪人对第三人违约的责任承担" in output["triggered_patches"]


def test_j2_low_sell_with_difference_compensation():
    output = adjudicate_commission_agency("委托人有指定价格，行纪人低于指定价格卖出，未经委托人同意，但愿意补偿差额。", today=TODAY)

    assert "补偿差额" in output["conclusion"]
    assert "交易对委托人发生效力" in output["conclusion"]
    assert "行纪人违反价格指示的处理" in output["triggered_patches"]


def test_j2_high_sell_benefit_belongs_to_principal():
    output = adjudicate_commission_agency("委托人指定价格出售，行纪人高于指定价格卖出，合同没有差价约定。", today=TODAY)

    assert "利益归委托人" in output["conclusion"]


def test_j3_intervention_right_for_market_priced_goods():
    output = adjudicate_commission_agency("行纪人主张介入权，自行买入市场定价商品，委托人没有相反意思表示。", today=TODAY)

    assert "介入权成立" in output["conclusion"]
    assert "仍可请求委托人支付报酬" in output["conclusion"]


def test_j7_perishable_goods_disposal_when_cannot_contact():
    output = adjudicate_commission_agency("委托物容易腐烂变质，行纪人无法联系委托人，只能合理处分委托物。", today=TODAY)

    assert "处分委托物合规" in output["conclusion"]
    assert "所得应转交委托人" in output["conclusion"]


def test_j6_deposit_right_after_urge_and_refusal():
    output = adjudicate_commission_agency("行纪人按约定买入委托物，经催告，委托人无正当理由拒收，行纪人主张提存。", today=TODAY)

    assert "提存权成立" in output["conclusion"]
    assert "行纪人提存权的行使" in output["triggered_patches"]


def test_j11_unclear_remuneration_determined_by_court():
    output = adjudicate_commission_agency("行纪人已经完成委托事务，双方未约定报酬，行纪人请求支付佣金。", today=TODAY)

    assert "酌情确定" in output["conclusion"]
    assert "行纪合同报酬的确定" in output["triggered_patches"]


def test_j5_lien_right_for_unpaid_remuneration():
    output = adjudicate_commission_agency("行纪人已经完成委托事务，委托人逾期不支付报酬，行纪人主张留置委托物。", today=TODAY)

    assert "留置权成立" in output["conclusion"]
    assert "行纪人留置权的行使" in output["triggered_patches"]


def test_j13_paid_commission_termination_loss_scope():
    output = adjudicate_commission_agency("有偿行纪合同中，委托人主张解除合同，解除造成损失10000元。", today=TODAY)

    assert "直接损失和合同履行后可以获得的利益" in output["conclusion"]
    assert "10000.00 元" in output["conclusion"]
    assert "行纪合同的任意解除权" in output["triggered_patches"]
