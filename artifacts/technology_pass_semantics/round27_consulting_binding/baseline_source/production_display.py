"""Deterministic semantic display mapping for structured commercial facts."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict, Iterable, List


PRODUCTION_SERIALIZER_VERSION = "production-semantic-display-6.7-freeze-1.0"


@dataclass(frozen=True)
class ProductionDisplayClaim:
    source_fact_ids: List[str]
    source_claim_ids: List[str]
    semantic_key: str
    status: str
    user_statement: str
    evidence_locations: List[str]
    confidence: str
    fact_value: Any
    polarity: str

    def to_public_dict(self) -> Dict[str, Any]:
        return asdict(self)


def _statement(key: str, value: Any, exists: Any) -> str:
    mapping = {
        "master_agreement": "合同确立了持续供货的框架合作关系。",
        "order_mechanism": "采购订单经供方确认后形成具体履约义务。",
        "dynamic_quantity": "具体采购数量以后续双方确认的采购订单和实际供货记录为准。",
        "late_delivery_remedy": "合同已约定迟延交付时的通知、拒收、取消订单或损失承担机制。",
        "risk_transfer_rule": "货物送达买方指定地点并完成约定签收后，货物风险转移。",
        "payment_account": "合同已明确约定收款银行、账户名称及账号。",
        "quality_standard_hierarchy": "合同已明确多个质量标准或技术文件发生冲突时的适用顺序。",
        "quality_remedy": "合同已约定质量不符合时的退换、修理或赔偿等补救方式。",
        "inspection_regime": "合同已约定收货检验、异议提出及质量复核安排。",
        "deemed_acceptance_scope": "合同已限定逾期未提出异议所产生的视为验收范围。",
        "price_mechanism": "价格调整须按照合同约定的条件和双方确认程序进行。",
        "confirmed_order_price_protected": "已确认订单的价格不因后续调价而被单方改变。",
        "termination_effect": "框架合同终止后，终止前已确认的订单仍按原约定继续履行。",
        "document_precedence": "合同已明确正文、附件、订单及书面变更文件之间的效力顺序。",
        "order_amendment_cancellation": "已确认订单的变更或取消须经协商，并保护已经发生的合理成本。",
        "periodic_settlement": "双方按照约定结算周期核对实际供货数量和货款。",
        "recurring_delivery": "合同约定在合作期内按订单分批持续交付。",
        "demand_forecast": "合同设置了采购需求预测或生产计划衔接机制。",
        "forecast_binding": "采购预测仅用于安排生产，不当然构成最低采购承诺。",
        "delivery_schedule": "合同已明确订单交付期限及迟延交付的通知要求。",
        "carrier_rule_applicability": "本交易由供方送达指定地点，不适用货交第一承运人的交付路径。",
        "receipt_is_final_acceptance": "签收仅代表约定范围内的收货确认，不等同于最终质量验收。",
        "minimum_purchase_commitment": "合同未约定最低采购数量，采购义务以确认订单为准。",
        "future_order_deadlock": "未来订单价格无法协商一致时，双方可暂停接受新订单。",
        "order_amendment_cancellation": "订单变更或取消须遵守协商及已发生合理成本保护机制。",
    }
    if key == "receipt_is_final_acceptance" and value is True:
        return "合同将签收约定为最终验收节点。"
    if key == "forecast_binding" and value is True:
        return "合同约定采购预测对后续采购安排具有约束力。"
    if key == "minimum_purchase_commitment" and value is True:
        return "合同约定了最低采购数量或最低采购承诺。"
    if key == "unilateral_price_adjustment":
        return "合同允许一方单方调整价格。" if value is True else "合同未赋予任何一方单方调整价格的权利。"
    return mapping.get(key, "合同已明确该项商业安排。" if exists else "合同未明确该项商业安排。")


def display_claim(fact_key: str, fact_row: Dict[str, Any]) -> ProductionDisplayClaim:
    value = fact_row.get("value")
    exists = fact_row.get("exists")
    statement = _statement(fact_key, value, exists)
    return ProductionDisplayClaim(
        source_fact_ids=[f"commercial.{fact_key}"], source_claim_ids=[], semantic_key=fact_key,
        status="CONFIRMED" if exists is not False else "ABSENT", user_statement=statement,
        evidence_locations=list(fact_row.get("source_clause_ids") or []),
        confidence=str(fact_row.get("confidence") or "high"), fact_value=value,
        polarity="NEGATIVE" if value is False else "POSITIVE",
    )


def display_claims(fact_names: Iterable[str], values: Dict[str, Dict[str, Any]]) -> List[ProductionDisplayClaim]:
    return [display_claim(name, values.get(name) or {}) for name in fact_names]


def production_fact_polarity_gate(claims: Iterable[Dict[str, Any]]) -> Dict[str, Any]:
    contradictions = []
    for claim in claims:
        value = claim.get("fact_value")
        statement = str(claim.get("user_statement") or "")
        if value is False and any(text in statement for text in ("构成最终质量验收", "具有约束力", "约定了最低采购", "允许一方单方")):
            contradictions.append(claim)
    return {
        "status": "REPORT_READY" if not contradictions else "BLOCKED",
        "failures": [] if not contradictions else [{
            "requirement": "PRODUCTION_FACT_POLARITY_GATE", "failure_stage": "Production Semantic Mapping",
            "root_cause": "A false structured fact was rendered as a positive affirmation.",
            "responsible_function": "display_claim", "current_status": "FAIL",
        }],
        "gate_results": {"PRODUCTION_FACT_POLARITY_GATE": "PASS" if not contradictions else "FAIL"},
        "contradictions": contradictions,
        "contradiction_count": len(contradictions),
    }
