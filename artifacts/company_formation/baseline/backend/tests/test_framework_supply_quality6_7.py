from __future__ import annotations

from review_v2.clause_parser import parse_contract_clauses
from review_v2.domain_resolution import resolve_contract_domain
from review_v2.framework_supply import extract_framework_supply_profile


def profile(text: str):
    clauses = parse_contract_clauses(text)
    return extract_framework_supply_profile(text, clauses)


FRAMEWORK_BASE = (
    "本协议合作期限为两年。买方按月发出书面采购订单，供应商确认后生效。"
    "每月根据订单、送货单和实际收货数量对账结算。"
)


def test_single_fixed_sale_is_not_framework():
    value = profile("买方一次性购买设备十台，总价十万元，签约后三日交付。")
    assert value.transaction_structure == "SINGLE_TRANSACTION"


def test_two_year_monthly_orders_is_framework():
    assert profile(FRAMEWORK_BASE).transaction_structure == "FRAMEWORK_SUPPLY"


def test_minimum_purchase_true():
    value = profile(FRAMEWORK_BASE + "买方每年最低采购10000件。")
    assert value.minimum_purchase_commitment.value is True


def test_explicit_no_minimum_is_false_not_missing():
    value = profile(FRAMEWORK_BASE + "本协议不约定最低采购数量。")
    assert value.minimum_purchase_commitment.value is False
    assert value.minimum_purchase_commitment.exists is False


def test_planning_forecast_is_non_binding():
    value = profile(FRAMEWORK_BASE + "预测仅供供应商安排产能，正式采购订单经确认后才构成有约束力的采购义务。")
    assert value.demand_forecast.exists is True
    assert value.forecast_binding.value is False


def test_firm_forecast_is_binding():
    value = profile(FRAMEWORK_BASE + "首月预测具有约束力，之后月份预测仅供参考。")
    assert value.forecast_binding.value is True


def test_bilateral_price_adjustment():
    value = profile(FRAMEWORK_BASE + "铜价变化超过10%时任一方可申请价格调整，双方协商确定新的价格并书面确认。")
    assert value.price_mechanism.value == "BILATERAL_ADJUSTMENT"
    assert value.unilateral_price_adjustment.value is False


def test_unilateral_price_notice_is_risk_fact():
    value = profile(FRAMEWORK_BASE + "供应商提前7日通知后可单方调整价格。")
    assert value.price_mechanism.value == "UNILATERAL_ADJUSTMENT"
    assert value.unilateral_price_adjustment.value is True


def test_new_price_only_for_future_orders_protects_confirmed_orders():
    value = profile(FRAMEWORK_BASE + "新价格仅适用于未来订单，已确认订单价格不变。")
    assert value.confirmed_order_price_protected.value is True


def test_destination_delivery_disables_carrier_rule():
    value = profile(FRAMEWORK_BASE + "供应商送货至买方指定仓库，仓库签收后风险转移。")
    assert value.carrier_rule_applicability.value is False
    assert value.risk_transfer_rule.value == "DESTINATION_RECEIPT"


def test_buyer_transport_enables_carrier_rule():
    value = profile(FRAMEWORK_BASE + "买方负责运输，货物交付第一承运人后风险转移。")
    assert value.carrier_rule_applicability.value is True


def test_receipt_quantity_is_not_final_acceptance():
    value = profile(FRAMEWORK_BASE + "签收仅确认数量，质量检验期限另为10日，签收不表示质量检验完成。")
    assert value.receipt_is_final_acceptance.value is False


def test_latent_defect_regime_is_preserved():
    value = profile(FRAMEWORK_BASE + "到货初步检验期限为5个工作日，隐蔽瑕疵可在质量保证期内提出。")
    assert value.inspection_regime.value == "VISIBLE_AND_LATENT_SEPARATED"


def test_confirmed_orders_survive_termination():
    value = profile(FRAMEWORK_BASE + "任一方可提前60日终止，但通知前已经确认的采购订单继续履行。")
    assert value.termination_effect.value == "CONFIRMED_ORDERS_SURVIVE"


def test_conditional_order_override():
    value = profile(FRAMEWORK_BASE + "文件效力顺序为补充协议、正文、附件、订单；订单特别变更须经双方授权人员书面确认。")
    assert value.document_precedence.value == "CONDITIONAL_ORDER_OVERRIDE"


def test_one_long_term_or_order_word_is_insufficient():
    assert profile("双方愿意长期合作，本次购买材料100件。期限七日。").transaction_structure == "SINGLE_TRANSACTION"
    assert profile("买方发出一个订单购买设备一台，卖方确认。").transaction_structure == "SINGLE_TRANSACTION"


def test_company_name_does_not_turn_components_into_equipment():
    text = FRAMEWORK_BASE + "买方为某新能源设备有限公司，标的要求为工业连接器、端子和配套组件。"
    clauses = parse_contract_clauses(text)
    resolution = resolve_contract_domain("sale", text, clauses)
    assert resolution.subject_matter == "GOODS"
    assert resolution.product_category == "INDUSTRIAL_COMPONENTS"
    assert resolution.contract_subtype == "FRAMEWORK_SUPPLY"
