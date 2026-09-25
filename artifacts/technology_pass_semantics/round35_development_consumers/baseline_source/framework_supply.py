"""Source-backed commercial facts for framework and recurring supply contracts."""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass, field
from typing import Any, Dict, Iterable, List, Sequence

from review_v2.clause_parser import ParsedClause
from review_v2.contract_facts import ContractFactGraph


FRAMEWORK_FACT_VERSION = "framework-supply-facts-1.0"


@dataclass(frozen=True)
class CommercialFact:
    value: Any = None
    exists: bool | None = None
    source_clause_ids: List[str] = field(default_factory=list)
    source_spans: List[str] = field(default_factory=list)
    confidence: str = "high"

    def to_public_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class FrameworkSupplyProfile:
    version: str
    transaction_structure: str
    product_category: str
    classification_score: int
    classification_signals: List[Dict[str, Any]]
    master_agreement: CommercialFact
    order_mechanism: CommercialFact
    dynamic_quantity: CommercialFact
    minimum_purchase_commitment: CommercialFact
    recurring_delivery: CommercialFact
    periodic_settlement: CommercialFact
    demand_forecast: CommercialFact
    forecast_binding: CommercialFact
    delivery_schedule: CommercialFact
    late_delivery_remedy: CommercialFact
    risk_transfer_rule: CommercialFact
    carrier_rule_applicability: CommercialFact
    payment_account: CommercialFact
    inspection_regime: CommercialFact
    receipt_is_final_acceptance: CommercialFact
    deemed_acceptance_scope: CommercialFact
    quality_remedy: CommercialFact
    quality_standard_hierarchy: CommercialFact
    dispute_resolution: CommercialFact
    price_mechanism: CommercialFact
    unilateral_price_adjustment: CommercialFact
    confirmed_order_price_protected: CommercialFact
    future_order_deadlock: CommercialFact
    termination_effect: CommercialFact
    document_precedence: CommercialFact
    order_amendment_cancellation: CommercialFact

    @property
    def is_framework(self) -> bool:
        return self.transaction_structure in {"FRAMEWORK_SUPPLY", "CALL_OFF_ORDER", "RECURRING_SUPPLY"}

    def to_public_dict(self) -> Dict[str, Any]:
        return asdict(self)


def _compact(value: str) -> str:
    return re.sub(r"\s+", "", value or "")


def _source(clauses: Sequence[ParsedClause], *terms: str, require_all: bool = False) -> tuple[List[str], List[str]]:
    rows = []
    for clause in clauses:
        compacted = _compact(clause.text)
        hit = all(term in compacted for term in terms) if require_all else any(term in compacted for term in terms)
        if hit:
            rows.append(clause)
    rows = rows[:12]
    return [row.clause_id for row in rows], [row.text for row in rows]


def _fact(clauses: Sequence[ParsedClause], value: Any, exists: bool | None, *terms: str, require_all: bool = False) -> CommercialFact:
    ids, spans = _source(clauses, *terms, require_all=require_all)
    return CommercialFact(value=value, exists=exists, source_clause_ids=ids, source_spans=spans)


def _signal(clauses: Sequence[ParsedClause], signal_type: str, terms: Iterable[str], weight: int) -> Dict[str, Any] | None:
    ids, _ = _source(clauses, *tuple(terms))
    return {
        "signal_type": signal_type,
        "weight": weight,
        "source_clause_ids": ids,
    } if ids else None


def extract_framework_supply_profile(text: str, clauses: Sequence[ParsedClause]) -> FrameworkSupplyProfile:
    compacted = _compact(text)
    signals = [
        _signal(clauses, "master_relationship", ("框架协议", "长期供货合同", "长期供应合同", "长期供货关系", "长期提供产品"), 4),
        _signal(clauses, "confirmed_order_performance", ("采购订单", "订单为准", "确认订单", "经甲方确认的订单", "经乙方确认的订单"), 4),
        _signal(clauses, "dynamic_quantity", ("不约定最低采购数量", "实际生产需求", "实际下达", "实际供货数量结算", "预计采购数量"), 3),
        _signal(clauses, "recurring_settlement", ("结算周期", "每月对账", "月度对账", "上一个结算周期", "滚动需求预测"), 3),
        _signal(clauses, "term_relationship", ("合作期限为", "供货期限自", "协议期限为", "合同期限为两年", "合同期限为2年"), 2),
    ]
    classification_signals = [row for row in signals if row]
    if "采购订单" in compacted and any(term in compacted for term in ("确认后生效", "供应商确认后", "供方确认后", "卖方确认后")):
        ids, _ = _source(clauses, "采购订单")
        if not any(row["signal_type"] == "confirmed_order_performance" for row in classification_signals):
            classification_signals.append({"signal_type": "confirmed_order_performance", "weight": 4, "source_clause_ids": ids})
    if "每月" in compacted and "对账" in compacted:
        ids, _ = _source(clauses, "对账")
        if not any(row["signal_type"] == "recurring_settlement" for row in classification_signals):
            classification_signals.append({"signal_type": "recurring_settlement", "weight": 3, "source_clause_ids": ids})
    signal_types = {row["signal_type"] for row in classification_signals}
    score = sum(row["weight"] for row in classification_signals)
    is_framework = (
        {"master_relationship", "confirmed_order_performance"}.issubset(signal_types)
        and len(signal_types) >= 3
    ) or {"confirmed_order_performance", "dynamic_quantity", "recurring_settlement"}.issubset(signal_types) \
        or {"confirmed_order_performance", "recurring_settlement", "term_relationship"}.issubset(signal_types)
    structure = "FRAMEWORK_SUPPLY" if is_framework else "SINGLE_TRANSACTION"

    product_category = "GENERAL_GOODS"
    product_body = "".join(
        clause.text for clause in clauses
        if any(term in clause.text for term in ("标的要求", "产品名称", "具体包括", "产品及价格清单"))
    )
    if any(term in compacted for term in ("连接器", "端子", "配套组件", "工业零部件", "密封圈", "锁止件")):
        product_category = "INDUSTRIAL_COMPONENTS"
    elif any(term in product_body for term in ("机器设备", "成套设备", "生产设备", "设备名称")):
        product_category = "EQUIPMENT"

    minimum_false = any(term in compacted for term in ("不约定最低采购数量", "无最低采购数量", "不承担最低采购", "不构成最低采购"))
    minimum_true = bool(re.search(r"(?:最低|最少|保底)(?:采购|购买|订购)[^。；]{0,20}\d+", compacted)) and not minimum_false
    forecast_exists = "预测" in compacted
    forecast_nonbinding = any(term in compacted for term in ("预测仅供", "仅供甲方安排", "仅供乙方安排", "才构成双方具有约束力", "不构成最低采购"))
    forecast_firm = any(term in compacted for term in ("锁定预测", "具有约束力的预测", "预测数量应当采购", "坚定预测", "预测具有约束力", "首月预测具有约束力"))

    order_exists = "采购订单" in compacted and any(term in compacted for term in ("确认订单", "订单为准", "经甲方确认", "经乙方确认", "正式采购订单"))
    dynamic = any(term in compacted for term in ("实际生产需求", "实际下达", "实际供货数量结算", "预计采购数量")) and order_exists
    periodic = any(term in compacted for term in ("结算周期", "每月对账", "月度对账", "自然月为一个结算周期"))
    destination = any(term in compacted for term in (
        "送货至乙方指定地点", "送达乙方指定地点", "送货至甲方指定地点", "送达甲方指定地点",
        "送货至买方指定", "送达买方指定", "送货至需方指定", "送达需方指定",
    ))
    buyer_transport = any(term in compacted for term in ("买方负责运输", "买受人负责运输", "需方负责运输", "交付第一承运人", "货交第一承运人"))
    risk_exists = "风险转移" in compacted or ("毁损" in compacted and "灭失" in compacted and "风险" in compacted)
    account_exists = any(term in compacted for term in ("收款账户", "账户名称", "开户行")) and "账号" in compacted
    inspection_exists = "检验期限" in compacted or bool(re.search(r"(?:到货|收货|签收)[^。；]{0,24}\d+个?工作日[^。；]{0,20}(?:检验|异议)", compacted))
    receipt_not_final = any(term in compacted for term in ("不视为对产品内在质量", "不表示乙方质量检验已经完成", "不表示甲方质量检验已经完成", "仅代表完成数量", "签收仅确认数量", "签收只确认数量"))
    deemed_limited = "视为" in compacted and any(term in compacted for term in ("明显瑕疵", "数量、型号、外观", "隐蔽瑕疵"))
    quality_remedy = "质量不符合" in compacted and sum(term in compacted for term in ("退货", "换货", "返修", "维修", "退还对应货款", "赔偿")) >= 2
    standard_hierarchy = any(term in compacted for term in ("标准之间存在不一致", "最后书面确认的技术规格", "强制性标准")) and any(term in compacted for term in ("为准", "不得低于", "优先"))
    dispute = "仲裁委员会" in compacted or "人民法院" in compacted
    price_exists = "价格调整" in compacted or "调价" in compacted
    unilateral = any(term in compacted for term in ("供应方有权单方调整价格", "供应商有权单方调整价格", "甲方有权单方调整价格", "乙方有权单方调整价格", "提前通知后调整价格")) or bool(re.search(r"(?:供应方|供应商|甲方|乙方)[^。；]{0,18}(?:通知|提前)[^。；]{0,12}(?:单方)?调整价格", compacted))
    bilateral = price_exists and any(term in compacted for term in ("协商确定新的价格", "双方书面确认新价格", "价格调整协议")) and not unilateral
    confirmed_protected = any(term in compacted for term in ("不得单方提高已经确认采购订单的价格", "已经确认的订单仍应按原约定履行", "已确认订单价格不变", "新价格仅适用于未来订单", "新价格适用于尚未确认的订单"))
    deadlock = any(term in compacted for term in ("停止接受新的采购订单", "暂停接受新的采购订单", "未来订单")) and "无法达成" in compacted
    termination_survival = any(term in compacted for term in ("已确认的采购订单", "已经确认的采购订单", "已经下达并经", "订单的继续履行")) and any(term in compacted for term in ("终止", "届满", "继续履行"))
    precedence = "文件效力顺序" in compacted or ("内容不一致" in compacted and "顺序确定效力" in compacted)
    conditional_override = "特别变更" in compacted and "授权人员书面确认" in compacted
    cancellation = any(term in compacted for term in ("取消订单", "不得无正当理由单方取消", "订单变更"))
    delivery_schedule = order_exists and ("订单未特别约定" in compacted or bool(re.search(r"确认订单后[^。；]{0,20}\d+个?(?:自然日|工作日|日|天)内", compacted)))
    late_remedy = "逾期交货" in compacted and any(term in compacted for term in ("拒收", "取消该批订单", "违约金", "替代采购差价"))

    profile = FrameworkSupplyProfile(
        version=FRAMEWORK_FACT_VERSION,
        transaction_structure=structure,
        product_category=product_category,
        classification_score=score,
        classification_signals=classification_signals,
        master_agreement=_fact(clauses, is_framework, is_framework, "长期供货合同", "长期供货关系", "长期提供产品", "框架协议"),
        order_mechanism=_fact(clauses, "FORMAL_ORDER_PLUS_CONFIRMATION" if order_exists else None, order_exists, "采购订单", "确认订单", "正式采购订单"),
        dynamic_quantity=_fact(clauses, dynamic, dynamic, "实际生产需求", "实际下达", "实际供货数量结算", "预计采购数量"),
        minimum_purchase_commitment=_fact(clauses, True if minimum_true else False if minimum_false else None, minimum_true if minimum_true else False if minimum_false else None, "最低采购数量", "最低采购责任", "保底采购"),
        recurring_delivery=_fact(clauses, is_framework and order_exists, is_framework and order_exists, "长期提供产品", "采购订单", "交付批次"),
        periodic_settlement=_fact(clauses, periodic, periodic, "结算周期", "每月对账", "月度对账", "上一个结算周期"),
        demand_forecast=_fact(clauses, "ROLLING_FORECAST" if forecast_exists else None, forecast_exists, "滚动需求预测", "预测"),
        forecast_binding=_fact(clauses, True if forecast_firm else False if forecast_nonbinding else None, True if forecast_firm else False if forecast_nonbinding else None, "预测仅供", "具有约束力", "才构成双方具有约束力", "坚定预测"),
        delivery_schedule=_fact(clauses, "ORDER_SPECIFIC_WITH_DEFAULT_LEAD_TIME" if delivery_schedule else None, delivery_schedule, "订单未特别约定", "确认订单后", "指定的时间交货"),
        late_delivery_remedy=_fact(clauses, "MULTI_STEP_REMEDY" if late_remedy else None, late_remedy, "逾期交货", "拒收相应逾期产品", "取消该批订单", "替代采购差价"),
        risk_transfer_rule=_fact(clauses, "DESTINATION_RECEIPT" if destination and risk_exists else "CARRIER_HANDOVER" if buyer_transport and risk_exists else None, risk_exists, "风险转移", "毁损、灭失等风险", "毁损、灭失风险"),
        carrier_rule_applicability=_fact(clauses, True if buyer_transport else False if destination else None, True if buyer_transport else False if destination else None, "第一承运人", "负责运输", "送货至", "送达"),
        payment_account=_fact(clauses, "SPECIFIED_WITH_CHANGE_NOTICE" if account_exists else None, account_exists, "账户信息", "收款账户", "开户行", "账号"),
        inspection_regime=_fact(clauses, "VISIBLE_AND_LATENT_SEPARATED" if inspection_exists and "隐蔽瑕疵" in compacted else "INSPECTION_PERIOD" if inspection_exists else None, inspection_exists, "检验期限", "到货初步检验期限", "隐蔽瑕疵"),
        receipt_is_final_acceptance=_fact(clauses, False if receipt_not_final else None, False if receipt_not_final else None, "不视为对产品内在质量", "不表示乙方质量检验已经完成", "不表示甲方质量检验已经完成"),
        deemed_acceptance_scope=_fact(clauses, "VISIBLE_ONLY_LATENT_RESERVED" if deemed_limited else None, deemed_limited, "视为该批产品", "隐蔽瑕疵", "明显瑕疵异议"),
        quality_remedy=_fact(clauses, "RETURN_REPLACE_REPAIR_REFUND_DAMAGES" if quality_remedy else None, quality_remedy, "质量不符合", "退货", "换货", "返修", "退还对应货款"),
        quality_standard_hierarchy=_fact(clauses, "LATEST_WRITTEN_SPEC_WITH_MANDATORY_FLOOR" if standard_hierarchy else None, standard_hierarchy, "标准之间存在不一致", "最后书面确认的技术规格", "强制性国家标准"),
        dispute_resolution=_fact(clauses, "ARBITRATION" if "仲裁委员会" in compacted else "LITIGATION" if "人民法院" in compacted else None, dispute, "仲裁委员会", "人民法院"),
        price_mechanism=_fact(clauses, "BILATERAL_ADJUSTMENT" if bilateral else "UNILATERAL_ADJUSTMENT" if unilateral else "FIXED_OR_UNSPECIFIED", price_exists, "价格调整", "协商确定新的价格", "单方调整价格"),
        unilateral_price_adjustment=_fact(clauses, unilateral, unilateral, "单方调整价格", "提前通知后调整价格"),
        confirmed_order_price_protected=_fact(clauses, confirmed_protected, confirmed_protected, "不得单方提高已经确认", "已经确认的订单仍应按原约定履行", "已确认订单价格不变"),
        future_order_deadlock=_fact(clauses, "SUSPEND_NEW_ORDERS" if deadlock else None, deadlock, "停止接受新的采购订单", "暂停接受新的采购订单", "无法达成新的价格"),
        termination_effect=_fact(clauses, "CONFIRMED_ORDERS_SURVIVE" if termination_survival else None, termination_survival, "继续履行通知发出前已经确认", "订单的继续履行", "已确认的采购订单"),
        document_precedence=_fact(clauses, "CONDITIONAL_ORDER_OVERRIDE" if precedence and conditional_override else "ORDERED_PRECEDENCE" if precedence else None, precedence, "文件效力顺序", "顺序确定效力", "特别变更"),
        order_amendment_cancellation=_fact(clauses, "CONSENT_OR_COST_PROTECTION" if cancellation else None, cancellation, "取消订单", "订单变更", "不得无正当理由单方取消"),
    )
    return profile


def add_framework_facts_to_graph(profile: FrameworkSupplyProfile, clauses: Sequence[ParsedClause], graph: ContractFactGraph) -> None:
    clauses_by_id = {clause.clause_id: clause for clause in clauses}
    for field_name, value in profile.to_public_dict().items():
        if not isinstance(value, dict) or "source_clause_ids" not in value:
            continue
        normalized = value.get("value") if value.get("value") is not None else value.get("exists")
        if normalized is None:
            continue
        for clause_id in value.get("source_clause_ids", []):
            clause = clauses_by_id.get(clause_id)
            if clause:
                graph.add(f"commercial.{field_name}", normalized, clause, normalized)


FRAMEWORK_REVIEW_FACT_PATHS: Dict[str, tuple[str, ...]] = {
    "framework_master_order_relationship": ("master_agreement", "order_mechanism"),
    "framework_order_formation_confirmation": ("order_mechanism",),
    "framework_dynamic_quantity": ("dynamic_quantity",),
    "framework_minimum_purchase": ("minimum_purchase_commitment",),
    "framework_forecast_order_distinction": ("demand_forecast", "forecast_binding", "order_mechanism"),
    "framework_periodic_settlement": ("periodic_settlement",),
    "framework_order_delivery_schedule": ("delivery_schedule",),
    "framework_order_amendment_cancellation": ("order_amendment_cancellation",),
    "framework_price_validity": ("price_mechanism",),
    "framework_price_adjustment_trigger": ("price_mechanism",),
    "framework_confirmed_order_price": ("confirmed_order_price_protected",),
    "framework_future_order_deadlock": ("future_order_deadlock",),
    "framework_termination_effect": ("termination_effect",),
    "framework_document_precedence": ("document_precedence",),
    "sale_subject_quantity_unit": ("dynamic_quantity", "order_mechanism"),
    "sale_delivery_time": ("delivery_schedule",),
    "sale_delivery_method": ("risk_transfer_rule", "receipt_is_final_acceptance"),
    "sale_delay_delivery_liability": ("late_delivery_remedy",),
    "sale_risk_transfer_delivery": ("risk_transfer_rule",),
    "sale_payment_method_account": ("payment_account",),
    "sale_quality_standard_basis": ("quality_standard_hierarchy",),
    "sale_quality_remedy": ("quality_remedy",),
    "sale_inspection_period": ("inspection_regime",),
    "sale_inspection_period_reasonable": ("inspection_regime",),
    "sale_visible_hidden_defects": ("inspection_regime", "receipt_is_final_acceptance"),
    "sale_deemed_acceptance": ("deemed_acceptance_scope",),
    "common_jurisdiction": ("dispute_resolution",),
}
