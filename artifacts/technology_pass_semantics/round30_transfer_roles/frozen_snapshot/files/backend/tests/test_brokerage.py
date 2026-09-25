"""Tests for the brokerage-contract adjudication engine."""

from datetime import date

from adjudicate.brokerage_configs import get_brokerage_config
from adjudicate.brokerage_engine import adjudicate_brokerage


TODAY = date(2026, 7, 27)


def test_brokerage_config_declares_core_mapping_and_patches():
    config = get_brokerage_config("brokerage")

    assert config.key == "brokerage"
    assert config.fact_mapping["核心争议"].startswith("合同性质认定")
    assert config.enabled_patches == tuple(f"M{i}" for i in range(1, 16))
    assert config.patch_mount("M2").node_id == "bypass_order"


def test_brokerage_jurisdiction_question():
    output = adjudicate_brokerage("中介合同纠纷去哪里起诉？", today=TODAY)

    assert "被告住所地或者合同履行地" in output["conclusion"]
    assert "管辖程序" in output["triggered_patches"]


def test_m14_burden_of_proof_for_broker():
    output = adjudicate_brokerage("双方对中介义务履行争议，中介人主张已完成义务但无法举证。", today=TODAY)

    assert "中介人承担举证责任" in output["conclusion"]
    assert "应承担不利后果" in output["conclusion"]
    assert "中介合同纠纷的举证责任" in output["triggered_patches"]


def test_m1_classifies_brokerage_contract():
    output = adjudicate_brokerage("合同性质争议，一方只是介绍房源并提供媒介服务，不参与交易合同。", today=TODAY)

    assert "合同性质认定为中介合同" in output["conclusion"]
    assert "中介合同的性质认定" in output["triggered_patches"]


def test_m1_classifies_commission_agency_when_own_name_trade():
    output = adjudicate_brokerage("合同性质争议，一方以自己名义与第三人交易，代购代销。", today=TODAY)

    assert "更接近行纪合同" in output["conclusion"]


def test_m1_classifies_agency_when_principal_name_used():
    output = adjudicate_brokerage("合同性质争议，受托人以委托人名义处理委托事务。", today=TODAY)

    assert "更接近委托合同" in output["conclusion"]


def test_m8_oral_brokerage_contract_with_evidence():
    output = adjudicate_brokerage("双方没有书面合同，只有口头中介约定，但有聊天记录和看房记录证明。", today=TODAY)

    assert "口头中介协议成立" in output["conclusion"]
    assert "口头中介协议的效力" in output["triggered_patches"]


def test_m12_unreasonable_standard_clause_invalid():
    output = adjudicate_brokerage("中介合同存在格式条款，免除中介责任并加重委托人责任，委托人主张条款无效。", today=TODAY)

    assert "应认定无效" in output["conclusion"]
    assert "中介合同格式条款的效力" in output["triggered_patches"]


def test_m9_staff_scope_act_liability_belongs_to_broker():
    output = adjudicate_brokerage("中介工作人员以公司名义在工作期间承诺事项，引发争议。", today=TODAY)

    assert "责任由中介人承担" in output["conclusion"]
    assert "中介人工作人员行为的责任归属" in output["triggered_patches"]


def test_m11_principal_wrong_info_without_broker_fault():
    output = adjudicate_brokerage("房源信息由委托人提供，委托人提供信息有误，导致中介服务瑕疵。", today=TODAY)

    assert "委托人承担相应责任" in output["conclusion"]
    assert "委托人提供信息有误导致中介服务瑕疵" in output["triggered_patches"]


def test_m6_best_efforts_breach():
    output = adjudicate_brokerage("委托人主张中介未尽力，没有积极促成交易，服务不到位。", today=TODAY)

    assert "构成违约" in output["conclusion"]
    assert "中介人的尽力义务" in output["triggered_patches"]


def test_m2_bypass_order_established():
    output = adjudicate_brokerage("委托人接受中介服务并看房，利用中介提供的房源信息，绕开中介直接签约，中介主张跳单并要求支付中介费。", today=TODAY)

    assert "构成“跳单”" in output["conclusion"]
    assert "应向中介人支付报酬" in output["conclusion"]
    assert "“跳单”的认定标准" in output["triggered_patches"]


def test_m13_non_exclusive_other_broker_not_bypass():
    output = adjudicate_brokerage("非独家委托，委托人通过其他中介正当途径获取相同信息并支付了其他中介费，原中介主张跳单。", today=TODAY)

    assert "不构成“跳单”" in output["conclusion"]
    assert any("独家委托 vs 非独家委托" in patch for patch in output["triggered_patches"])


def test_m10_policy_failure_no_remuneration():
    output = adjudicate_brokerage("因限购和贷款政策变化导致交易未成，中介人要求支付中介费和必要费用。", today=TODAY)

    assert "不得请求报酬" in output["conclusion"]
    assert "可以请求必要费用" in output["conclusion"]
    assert "政策原因导致交易不成的责任" in output["triggered_patches"]


def test_m4_no_contract_necessary_expense_only():
    output = adjudicate_brokerage("中介人未促成合同成立，交易未成，但按约定请求必要费用交通费3000元。", today=TODAY)

    assert "不得请求支付报酬" in output["conclusion"]
    assert "可以请求支付必要费用" in output["conclusion"]
    assert "3000.00 元" in output["conclusion"]
    assert "未促成合同成立时的必要费用" in output["triggered_patches"]


def test_m3_contract_concluded_agreed_remuneration():
    output = adjudicate_brokerage("中介人促成合同成立，双方约定中介费5000元，中介人要求支付中介费。", today=TODAY)

    assert "报酬按约定确定" in output["conclusion"]
    assert "5000.00 元" in output["conclusion"]
    assert "报酬的计算与负担" in output["triggered_patches"]


def test_m3_media_service_both_parties_bear():
    output = adjudicate_brokerage("中介提供媒介服务促成合同成立，报酬约定不明，买卖双方平均负担中介费。", today=TODAY)

    assert "交易合同当事人平均负担" in output["conclusion"]


def test_m5_truthful_report_violation_with_loss():
    output = adjudicate_brokerage("委托人主张中介未如实报告，故意隐瞒房屋被查封的重要事实，损害委托人利益，造成损失8000元。", today=TODAY)

    assert "不可以请求支付报酬" in output["conclusion"]
    assert "应承担赔偿责任" in output["conclusion"]
    assert "8000.00 元" in output["conclusion"]
    assert "中介人如实报告义务的违反" in output["triggered_patches"]


def test_m7_paid_brokerage_termination_loss_scope():
    output = adjudicate_brokerage("有偿中介合同中，委托人解除中介合同，解除造成损失10000元。", today=TODAY)

    assert "中介合同解除有效" in output["conclusion"]
    assert "直接损失和可得利益" in output["conclusion"]
    assert "10000.00 元" in output["conclusion"]
    assert "中介合同解除" in output["triggered_patches"]


def test_m15_post_contract_obligation_breach():
    output = adjudicate_brokerage("中介合同终止后，一方违反后合同义务，泄露信息并拒绝协助。", today=TODAY)

    assert "已违反后合同义务" in output["conclusion"]
    assert "中介合同终止后的后合同义务" in output["triggered_patches"]
