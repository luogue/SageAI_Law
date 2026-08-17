"""Canonical factual claims shared by multiple reviews.

Review results do not own objective facts. Facts and source clauses establish
one claim state that every consuming review must interpret consistently.
"""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass, field, replace
from typing import Any, Callable, Dict, List, Sequence

from review_v2.clause_parser import ParsedClause, formal_evidence_clauses
from review_v2.contract_facts import ContractFactGraph


CLAIM_SCHEMA_VERSION = "canonical-claim-schema-1.0"


@dataclass(frozen=True)
class CanonicalClaim:
    claim_id: str
    subject: str
    predicate: str
    object: Any
    qualifier: str
    polarity: str
    status: str
    fact_ids: List[str]
    evidence_ids: List[str]
    source_clause_ids: List[str]
    source_spans: List[str]
    source_locations: List[str]
    extraction_method: str
    normalization: str
    confidence: str
    consumer_review_ids: List[str] = field(default_factory=list)

    def to_public_dict(self) -> Dict[str, Any]:
        return asdict(self)


def _clauses_with(clauses: Sequence[ParsedClause], terms: Sequence[str]) -> List[ParsedClause]:
    return [clause for clause in formal_evidence_clauses(list(clauses)) if any(term in clause.text for term in terms)]


def _claim(claim_id: str, subject: str, predicate: str, value: Any, clauses: Sequence[ParsedClause], terms: Sequence[str], consumers: Sequence[str], confidence: str = "high") -> CanonicalClaim:
    sources = _clauses_with(clauses, terms)
    return CanonicalClaim(
        claim_id=claim_id, subject=subject, predicate=predicate, object=value, qualifier="contract_disclosure",
        polarity="NEGATIVE" if value is False else "POSITIVE", status="ASSERTED" if sources else "UNKNOWN",
        fact_ids=[], evidence_ids=[f"CCE-{clause.clause_id}" for clause in sources],
        source_clause_ids=[clause.clause_id for clause in sources], source_spans=[clause.text for clause in sources],
        source_locations=[clause.location for clause in sources],
        extraction_method="domain_claim_rule", normalization="boolean_or_explicit_value", confidence=confidence if sources else "low",
        consumer_review_ids=list(consumers),
    )


def _claim_where(
    claim_id: str,
    subject: str,
    predicate: str,
    clauses: Sequence[ParsedClause],
    consumers: Sequence[str],
    matcher: Callable[[str], bool],
    *,
    confidence: str = "high",
) -> CanonicalClaim:
    sources = [
        clause for clause in formal_evidence_clauses(list(clauses))
        if matcher(clause.text.replace("\n", ""))
    ]
    return CanonicalClaim(
        claim_id=claim_id,
        subject=subject,
        predicate=predicate,
        object=True if sources else None,
        qualifier="contract_clause",
        polarity="POSITIVE",
        status="ASSERTED" if sources else "UNKNOWN",
        fact_ids=[],
        evidence_ids=[f"CCE-{clause.clause_id}" for clause in sources],
        source_clause_ids=[clause.clause_id for clause in sources],
        source_spans=[clause.text for clause in sources],
        source_locations=[clause.location for clause in sources],
        extraction_method="shared_claim_rule",
        normalization="semantic_predicate",
        confidence=confidence if sources else "low",
        consumer_review_ids=list(consumers),
    )


def _build_goods_claims(clauses: Sequence[ParsedClause]) -> Dict[str, CanonicalClaim]:
    definitions = (
        ("contract.termination.trigger", "contract", "termination_trigger", ["S-00-02"], lambda t: "解除" in t and any(x in t for x in ("严重违约", "合同目的无法实现", "不履行主要义务", "丧失履约能力"))),
        ("contract.termination.notice_or_demand", "contract", "termination_notice_or_demand", ["S-00-02"], lambda t: any(x in t for x in ("书面催告", "书面终止通知", "书面通知")) and any(x in t for x in ("解除", "终止", "补救"))),
        ("contract.termination.cure_period", "contract", "termination_cure_period", ["S-00-02"], lambda t: any(x in t for x in ("催告后", "补救措施", "履约保障")) and any(x in t for x in ("工作日内", "日内"))),
        ("contract.termination.right", "contract", "termination_right", ["S-00-02"], lambda t: any(x in t for x in ("有权解除合同", "有权解除本合同", "均可解除本合同"))),
        ("contract.termination.convenience_notice", "contract", "convenience_termination_notice", ["S-00-02"], lambda t: "提前终止" in t and "通知" in t),
        ("contract.termination.settlement", "contract", "termination_settlement", ["S-00-02"], lambda t: any(x in t for x in ("解除", "终止")) and any(x in t for x in ("结算", "结清", "返还"))),
        ("framework.confirmed_orders_survive", "framework_supply", "confirmed_orders_survive", ["S-00-02", "FS-13"], lambda t: "已经确认" in t and "订单" in t and any(x in t for x in ("继续履行", "仍应按原约定履行"))),
        ("contract.force_majeure.event", "contract", "force_majeure_event", ["S-00-06"], lambda t: "不可抗力" in t),
        ("contract.force_majeure.notice", "contract", "force_majeure_notice", ["S-00-06"], lambda t: "不可抗力" in t and "通知" in t),
        ("contract.force_majeure.evidence", "contract", "force_majeure_evidence", ["S-00-06"], lambda t: "不可抗力" in t and any(x in t for x in ("证明", "证据"))),
        ("contract.force_majeure.mitigation", "contract", "force_majeure_mitigation", ["S-00-06"], lambda t: "不可抗力" in t and any(x in t for x in ("调整履行方式", "部分履行", "减损"))),
        ("contract.force_majeure.suspension_or_extension", "contract", "force_majeure_extension", ["S-00-06"], lambda t: "不可抗力" in t and any(x in t for x in ("延期履行", "中止履行", "延长"))),
        ("contract.force_majeure.prolonged_termination", "contract", "force_majeure_prolonged_termination", ["S-00-06"], lambda t: "不可抗力" in t and "合同目的无法实现" in t and "解除" in t),
        ("contract.force_majeure.payment_settlement", "contract", "force_majeure_payment_settlement", ["S-00-06"], lambda t: "不可抗力" in t and any(x in t for x in ("结算", "已履行部分", "费用承担"))),
        ("damages.lost_profit_recognized", "damages", "lost_profit_recognized", ["S-08-03"], lambda t: any(x in t for x in ("可得利益损失", "可得的利益", "预期利益"))),
        ("damages.lost_profit_causation", "damages", "lost_profit_causation", ["S-08-03"], lambda t: any(x in t for x in ("可得利益", "预期利益")) and any(x in t for x in ("因违约造成", "因此造成", "因不履行"))),
        ("damages.lost_profit_foreseeability", "damages", "lost_profit_foreseeability", ["S-08-03"], lambda t: any(x in t for x in ("可得利益", "预期利益")) and any(x in t for x in ("可预见", "应当预见", "能够证明", "合理证明"))),
        ("damages.lost_profit_exclusion_or_cap", "damages", "lost_profit_exclusion_or_cap", ["S-08-03"], lambda t: any(x in t for x in ("可得利益", "预期利益")) and any(x in t for x in ("责任上限", "最高不超过", "不予赔偿", "排除"))),
        ("damages.lost_profit_recovery_scope", "damages", "lost_profit_recovery_scope", ["S-08-03"], lambda t: "损失包括" in t and any(x in t for x in ("可得利益", "预期利益"))),
        ("goods.buyer_refusal_liability", "buyer", "unreasonable_refusal_liability", ["S-04-04"], lambda t: "无正当理由" in t and any(x in t for x in ("拒绝接收", "拒收", "未提货")) and any(x in t for x in ("承担", "赔偿"))),
        ("goods.delay_acceptance_storage_cost", "buyer", "delay_acceptance_storage_cost", ["S-04-04"], lambda t: any(x in t for x in ("拒绝接收", "拒收", "未提货")) and any(x in t for x in ("仓储", "保管费"))),
        ("goods.delay_acceptance_retransport_cost", "buyer", "delay_acceptance_retransport_cost", ["S-04-04"], lambda t: any(x in t for x in ("拒绝接收", "拒收", "未提货")) and any(x in t for x in ("二次运输", "再次运输"))),
        ("goods.delay_acceptance_insurance_cost", "buyer", "delay_acceptance_insurance_cost", ["S-04-04"], lambda t: any(x in t for x in ("迟延受领", "拒绝接收", "未提货")) and "保险" in t),
        ("goods.delay_acceptance_risk_transfer", "buyer", "risk_transfer_on_delay", ["S-04-04"], lambda t: any(x in t for x in ("迟延受领", "拒绝接收", "未提货")) and "风险" in t and "转移" in t),
        ("goods.delay_acceptance_preservation_duty", "seller", "preservation_duty", ["S-04-04"], lambda t: any(x in t for x in ("迟延受领", "拒绝接收", "未提货")) and any(x in t for x in ("妥善保管", "保全货物", "保管义务"))),
        ("goods.non_infringement_warranty", "seller", "non_infringement_warranty", ["S-11-02"], lambda t: any(x in t for x in ("不侵犯第三方", "不侵害第三方", "无知识产权侵权"))),
        ("goods.third_party_claim_handling", "contract_party", "third_party_claim_handling", ["S-11-02", "S-11-04"], lambda t: "侵害第三方合法权益" in t and any(x in t for x in ("负责处理", "承担相应责任"))),
        ("goods.infringement_indemnity", "contract_party", "infringement_indemnity", ["S-11-02", "S-11-04"], lambda t: "侵害第三方合法权益" in t and any(x in t for x in ("赔偿责任", "赔偿损失"))),
        ("goods.embedded_software_right", "seller", "embedded_software_right", ["S-11-02"], lambda t: any(x in t for x in ("嵌入式软件", "随附软件")) and any(x in t for x in ("授权", "使用权", "许可"))),
        ("goods.technical_material_right", "seller", "technical_material_right", ["S-11-02"], lambda t: any(x in t for x in ("图纸", "技术资料")) and any(x in t for x in ("使用权", "授权", "许可"))),
        ("goods.brand_authorization", "seller", "brand_authorization", ["S-11-02"], lambda t: any(x in t for x in ("商标", "品牌")) and any(x in t for x in ("授权", "许可"))),
        ("goods.third_party_rights_free", "seller", "third_party_rights_free", ["S-11-01"], lambda t: any(x in t for x in ("无第三方权利", "不存在第三方权利", "无权利负担", "不存在权利瑕疵"))),
        ("goods.right_defect_disclosure", "seller", "right_defect_disclosure", ["S-11-03"], lambda t: any(x in t for x in ("权利瑕疵", "第三方权利", "权利负担")) and any(x in t for x in ("披露", "书面告知", "如实告知"))),
        ("goods.third_party_claim_remedy", "seller", "third_party_claim_remedy", ["S-11-04"], lambda t: "第三方" in t and any(x in t for x in ("负责处理", "排除妨碍", "赔偿责任", "赔偿损失"))),
        ("goods.title_warranty", "seller", "title_warranty", ["S-11-01", "S-11-03", "S-11-04"], lambda t: any(x in t for x in ("合法所有权", "有权处分", "享有所有权", "权属清晰"))),
        ("goods.packaging_standard", "seller", "packaging_standard", ["S-02-04"], lambda t: any(x in t for x in ("包装标准", "包装方式", "包装应当", "防潮包装", "防震包装"))),
        ("goods.packaging_cost_included", "seller", "packaging_cost_included", ["S-02-04"], lambda t: any(x in t for x in ("包含包装费", "含包装费", "包装费用"))),
        ("goods.documentation_delivery", "seller", "documentation_delivery", ["S-02-04"], lambda t: any(x in t for x in ("随附资料", "随货资料", "交付资料", "说明书", "合格证"))),
        ("goods.certificate_of_conformity", "seller", "certificate_of_conformity", ["S-12-02"], lambda t: any(x in t for x in ("合格证", "质量合格证明"))),
        ("goods.factory_test_report", "seller", "factory_test_report", ["S-12-02"], lambda t: any(x in t for x in ("出厂检验报告", "出厂检测报告"))),
        ("goods.third_party_test_report", "seller", "third_party_test_report", ["S-12-02"], lambda t: any(x in t for x in ("第三方检测报告", "第三方检验报告"))),
        ("goods.mandatory_certificate", "seller", "mandatory_certificate", ["S-12-02"], lambda t: any(x in t for x in ("强制认证证书", "CCC证书", "监管证书"))),
        ("goods.user_manual", "seller", "user_manual", ["S-12-03"], lambda t: any(x in t for x in ("使用说明书", "用户手册"))),
        ("goods.operation_manual", "seller", "operation_manual", ["S-12-03"], lambda t: any(x in t for x in ("操作手册", "操作说明"))),
        ("goods.maintenance_manual", "seller", "maintenance_manual", ["S-12-03"], lambda t: any(x in t for x in ("维护手册", "维修手册"))),
        ("goods.warranty_card", "seller", "warranty_card", ["S-12-03"], lambda t: "保修卡" in t),
    )
    claims = {
        claim_id: _claim_where(claim_id, subject, predicate, clauses, consumers, matcher)
        for claim_id, subject, predicate, consumers, matcher in definitions
    }
    precedence = _claim_where(
        "document.precedence", "contract_documents", "precedence", clauses,
        ["S-12-04", "FS-14"],
        lambda t: any(term in t for term in ("文件效力顺序", "内容不一致", "顺序确定效力", "优先适用"))
        and any(term in t for term in ("合同正文", "本合同正文", "附件", "采购订单", "补充协议")),
    )
    all_clauses = list(clauses)
    source_ids = set(precedence.source_clause_ids)
    anchor_indexes = [index for index, clause in enumerate(all_clauses) if clause.clause_id in source_ids]
    for clause in formal_evidence_clauses(all_clauses):
        compact = clause.text.replace("\n", "")
        if "本合同及其附件" in compact and "共同构成" in compact:
            source_ids.add(clause.clause_id)
    continuation_terms = ("附件", "采购订单", "订单", "特别变更", "授权人员书面确认", "授权人书面确认")
    for anchor_index in anchor_indexes:
        for clause in all_clauses[anchor_index + 1:]:
            if re.match(r"^（[一二三四五六七八九十]+）", clause.text.strip()):
                break
            if any(term in clause.text for term in continuation_terms):
                source_ids.add(clause.clause_id)
    sources = [clause for clause in all_clauses if clause.clause_id in source_ids]
    precedence = replace(
        precedence,
        status="ASSERTED" if sources else "UNKNOWN",
        evidence_ids=[f"CCE-{clause.clause_id}" for clause in sources],
        source_clause_ids=[clause.clause_id for clause in sources],
        source_spans=[clause.text for clause in sources],
        source_locations=[clause.location for clause in sources],
        confidence="high" if sources else "low",
    )
    combined = "".join(precedence.source_spans)
    semantic_elements = {
        "attachment_effect": "附件" in combined,
        "attachment_vs_main": "附件" in combined and any(term in combined for term in ("合同正文", "本合同正文", "正文")),
        "supplement_priority": "补充协议" in combined,
        "amendment_priority": any(term in combined for term in ("书面变更", "特别变更")),
        "order_priority": "采购订单" in combined or "订单" in combined,
        "conditional_override": any(term in combined for term in ("授权人员书面确认", "授权人书面确认", "特别变更")),
    }
    claims[precedence.claim_id] = replace(
        precedence,
        object={"hierarchy": semantic_elements, "ordered_document_hierarchy": precedence.status == "ASSERTED"},
        fact_ids=["commercial.document_precedence"],
        normalization="document_precedence_semantic_elements",
    )
    return claims


def build_canonical_claims(text: str, clauses: Sequence[ParsedClause], graph: ContractFactGraph, subject_matter: str) -> Dict[str, CanonicalClaim]:
    claims: Dict[str, CanonicalClaim] = {}
    if subject_matter in {"GOODS", "EQUIPMENT", "UNCERTAIN"}:
        claims.update(_build_goods_claims(clauses))
    if subject_matter != "REAL_ESTATE":
        return claims
    consumers = ["RE-01-08", "RE-02-01", "RE-02-02", "RE-02-03", "RE-02-04", "RE-02-05"]
    definitions = (
        ("property.mortgage.disclosed", "property.mortgage", "disclosed", True, ("存在如下抵押", "存在抵押", "抵押权人", "无抵押")),
        ("property.judicial_seizure.disclosed", "property.judicial_seizure", "disclosed", True, ("司法查封",)),
        ("property.disposition_restriction.disclosed", "property.disposition_restriction", "disclosed", True, ("限制处分", "限售")),
        ("property.ownership_dispute.disclosed", "property.ownership_dispute", "disclosed", True, ("产权争议",)),
        ("property.coownership.disclosed", "property.coownership", "disclosed", True, ("登记共有情况", "未披露共有权", "单独所有")),
        ("property.lease.disclosed", "property.lease", "disclosed", True, ("租赁情况", "无租赁", "不存在出租情况", "未披露租赁关系")),
        ("seller.encumbrance_warranty.exists", "seller", "encumbrance_warranty", True, ("其他足以影响房地产正常转让的第三方权利", "其他影响正常转让的第三方权利", "不存在司法查封", "保证房地产不存在", "卖方保证无司法查封")),
    )
    for claim_id, subject, predicate, value, terms in definitions:
        claims[claim_id] = _claim(claim_id, subject, predicate, value, clauses, terms, consumers)
    agent_positive = ("委托代理人", "授权委托书", "代为签署", "代为办理", "代理签署", "代办过户")
    agent_negative = ("代理人：无", "委托代理人：无", "均本人签署", "本人签署")
    negative_sources = _clauses_with(clauses, agent_negative)
    positive_sources = [clause for clause in _clauses_with(clauses, agent_positive) if not any(term in clause.text for term in agent_negative)]
    agent_exists = True if positive_sources else False if negative_sources else False
    agent_sources = positive_sources or negative_sources
    claims["agent.exists"] = CanonicalClaim(
        claim_id="agent.exists", subject="contract_party", predicate="agent_exists", object=agent_exists,
        qualifier="signing_or_registration", polarity="POSITIVE" if agent_exists else "NEGATIVE",
        status="ASSERTED" if agent_sources else "ABSENT", fact_ids=[], evidence_ids=[f"CCE-{c.clause_id}" for c in agent_sources],
        source_clause_ids=[c.clause_id for c in agent_sources], source_spans=[c.text for c in agent_sources],
        source_locations=[c.location for c in agent_sources],
        extraction_method="agency_trigger_rule", normalization="boolean", confidence="high" if agent_sources else "medium",
        consumer_review_ids=["RE-01-06"],
    )
    return claims


def canonical_claims_public(claims: Dict[str, CanonicalClaim]) -> Dict[str, Any]:
    return {"version": CLAIM_SCHEMA_VERSION, "claims": {key: value.to_public_dict() for key, value in claims.items()}}
