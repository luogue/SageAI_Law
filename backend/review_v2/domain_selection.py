"""Resolve conflicts between a user-selected contract type and document evidence."""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Sequence, Tuple

from review_v2.clause_parser import ParsedClause
from review_v2.domain_resolution import DomainResolution, resolve_contract_domain
from review_v2.technology_service_analysis import classify_technology_transaction


@dataclass(frozen=True)
class DomainSelectionEvidence:
    signal_type: str
    signal: str
    target_family: str
    weight: int
    source_clause_ids: List[str]


@dataclass(frozen=True)
class DomainSelectionResolution:
    selected_contract_type: str
    document_domain: Dict[str, Any]
    compatibility: str
    resolution: str
    selected_domain: str
    rejected_domain: str
    confidence: str
    reasons: List[str]
    classification_evidence: List[DomainSelectionEvidence] = field(default_factory=list)
    classification_context: Dict[str, Any] = field(default_factory=dict)

    def to_public_dict(self) -> Dict[str, Any]:
        return asdict(self)


_LEASE_SIGNALS: Tuple[Tuple[str, Tuple[str, ...], int], ...] = (
    ("lease_title", ("房屋租赁合同", "住宅租赁合同", "租赁合同"), 8),
    ("lease_parties", ("出租人", "承租人"), 5),
    ("rent_obligation", ("月租金", "租金支付", "支付租金"), 3),
    ("lease_term", ("租赁期限", "租期", "退租"), 3),
    ("lease_deposit", ("租赁押金", "押金退还", "退还押金"), 2),
)

_SALE_SIGNALS: Tuple[Tuple[str, Tuple[str, ...], int], ...] = (
    ("sale_title", ("买卖合同", "供货合同", "采购合同", "框架采购"), 8),
    ("sale_parties", ("出卖人", "买受人", "供方", "需方", "供应商", "采购方"), 5),
    ("framework_structure", ("长期供货", "采购订单", "框架协议", "分批供货"), 5),
    ("goods_identity", ("产品名称", "货物名称", "设备", "材料", "规格型号", "供货数量"), 4),
    ("goods_purchase_obligation", ("购买", "采购", "销售", "供货"), 4),
    ("goods_performance", ("交货地点", "交货期限", "交货", "货款", "支付货款", "验收合格", "对账结算"), 3),
)

_SERVICE_SIGNALS: Tuple[Tuple[str, Tuple[str, ...], int], ...] = (
    ("service_obligation", ("提供服务", "服务内容", "服务范围", "委托乙方服务", "乙方提供"), 5),
    ("service_fee", ("服务费", "服务费用", "咨询费", "技术服务费", "服务报酬"), 5),
    ("service_scope", ("工作范围", "服务项目", "服务清单", "服务标准"), 3),
    ("service_term", ("服务期限", "服务期间", "服务周期", "服务时间"), 2),
    ("service_acceptance", ("服务成果", "成果验收", "验收标准", "验收期限"), 2),
    ("service_title_hint", ("服务合同", "咨询服务", "技术服务"), 1),
)

_TECHNOLOGY_SUBTYPES = {
    "COOPERATIVE_DEVELOPMENT",
    "ENTRUSTED_DEVELOPMENT",
    "TECHNOLOGY_TRANSFER",
    "TECHNOLOGY_LICENSE",
    "TECHNICAL_CONSULTING",
    "TECHNICAL_SERVICE",
}


def consumer_service_context(text: str, technology_classification: Dict[str, Any] | None = None) -> Dict[str, Any]:
    """Classify consumer/prepaid service context independently from incidental service words."""
    compact = re.sub(r"\s+", "", text or "")
    technology = technology_classification or classify_technology_transaction(text)
    primary_type = str(technology.get("primary_contract_type") or "")
    technology_development = primary_type in {"commissioned_development", "cooperative_development"}
    training_signals = [term for term in ("培训", "课程", "课时", "授课", "学员", "上课") if term in compact]
    prepaid_signals = [term for term in ("预付费", "预付款", "会员卡", "储值", "充值", "课包", "剩余课时") if term in compact]
    consumer_signals = [term for term in ("消费者", "学员", "会员", "家长", "个人客户") if term in compact]
    training_economic_signals = [
        term for term in ("培训费", "课程费", "课时费", "课程包", "培训项目", "服务费")
        if term in compact
    ]
    is_training_primary = bool(training_signals and training_economic_signals and not technology_development)
    is_prepaid_service = bool(prepaid_signals and (training_signals or "服务" in compact) and not technology_development)
    is_consumer_transaction = bool(consumer_signals and (training_signals or "服务" in compact) and not technology_development)
    return {
        "is_consumer_transaction": is_consumer_transaction,
        "is_prepaid_service": is_prepaid_service,
        "is_training_primary_transaction": is_training_primary,
        "consumer_signals": consumer_signals,
        "prepaid_signals": prepaid_signals,
        "training_signals": training_signals,
        "gate_status": "APPLICABLE" if any((is_consumer_transaction, is_prepaid_service, is_training_primary)) else "NOT_APPLICABLE",
    }


def _family_for_contract_type(contract_type: str) -> str:
    value = (contract_type or "").strip().lower()
    if value in {"sale", "买卖合同"}:
        return "SALE"
    if value in {"lease", "house_lease", "房屋租赁合同"}:
        return "HOUSE_LEASE"
    if value in {"service", "服务合同"}:
        return "SERVICE"
    if value in {"technology", "技术合同"}:
        return "TECHNOLOGY"
    return value.upper()


def _collect_family_evidence(
    text: str,
    clauses: Sequence[ParsedClause],
    family: str,
    definitions: Sequence[Tuple[str, Tuple[str, ...], int]],
) -> tuple[int, List[DomainSelectionEvidence]]:
    score = 0
    evidence: List[DomainSelectionEvidence] = []
    for signal_type, terms, weight in definitions:
        hits = [term for term in terms if term in text]
        if signal_type in {"lease_parties", "sale_parties"}:
            distinct_roles = {term for term in hits}
            if len(distinct_roles) < 2:
                continue
        if not hits:
            continue
        source_ids = [clause.clause_id for clause in clauses if any(term in clause.text for term in hits)][:8]
        evidence.append(DomainSelectionEvidence(signal_type, "、".join(hits[:3]), family, weight, source_ids))
        score += weight
    return score, evidence


def _technology_family_evidence(
    text: str,
    clauses: Sequence[ParsedClause],
) -> tuple[int, List[DomainSelectionEvidence], Dict[str, Any]]:
    classification = classify_technology_transaction(text)
    subtype = str(classification.get("primary_subtype") or "")
    confidence = str(classification.get("confidence") or "low")
    raw_score = int(classification.get("classification_score") or 0)
    if subtype not in _TECHNOLOGY_SUBTYPES or confidence == "low":
        return 0, [], classification

    reasons = [str(value) for value in classification.get("classification_evidence") or []]
    if not reasons:
        reasons = [str(value) for value in classification.get("evidence_node_ids") or []]
    source_ids = [clause.clause_id for clause in clauses if any(
        term in clause.text
        for term in ("委托", "开发", "研发", "源代码", "API", "专利", "许可", "技术服务", "技术咨询")
    )][:12]
    score = max(6, raw_score)
    evidence = [DomainSelectionEvidence(
        signal_type=f"technology_{subtype.lower()}",
        signal="、".join(reasons[:8]) or subtype,
        target_family="TECHNOLOGY",
        weight=score,
        source_clause_ids=source_ids,
    )]
    return score, evidence, classification


def _classify_document_family(
    text: str,
    clauses: Sequence[ParsedClause],
) -> tuple[str, str, List[DomainSelectionEvidence], Dict[str, int], Dict[str, Any]]:
    lease_score, lease_evidence = _collect_family_evidence(text, clauses, "HOUSE_LEASE", _LEASE_SIGNALS)
    sale_score, sale_evidence = _collect_family_evidence(text, clauses, "SALE", _SALE_SIGNALS)
    service_score, service_evidence = _collect_family_evidence(text, clauses, "SERVICE", _SERVICE_SIGNALS)
    technology_score, technology_evidence, technology_classification = _technology_family_evidence(text, clauses)
    scores = {
        "SALE": sale_score,
        "HOUSE_LEASE": lease_score,
        "SERVICE": service_score,
        "TECHNOLOGY": technology_score,
    }
    winner = max(scores, key=lambda key: scores[key])
    winner_score = scores[winner]
    runner_up = max((score for key, score in scores.items() if key != winner), default=0)
    margin = winner_score - runner_up
    evidence_by_family = {
        "SALE": sale_evidence,
        "HOUSE_LEASE": lease_evidence,
        "SERVICE": service_evidence,
        "TECHNOLOGY": technology_evidence,
    }
    winner_evidence = evidence_by_family[winner]
    if winner == "TECHNOLOGY" and technology_classification.get("confidence") == "high" and margin >= 4:
        confidence = "high"
    elif winner_score >= 8 and margin >= 4 and len(winner_evidence) >= 2:
        confidence = "high"
    elif winner_score >= 5 and margin >= 2:
        confidence = "medium"
    else:
        return "UNCERTAIN", "low", lease_evidence + sale_evidence + service_evidence + technology_evidence, scores, technology_classification
    return winner, confidence, lease_evidence + sale_evidence + service_evidence + technology_evidence, scores, technology_classification


def resolve_domain_selection(
    selected_contract_type: str,
    text: str,
    clauses: Sequence[ParsedClause],
) -> tuple[DomainSelectionResolution, DomainResolution, str]:
    """Return the public resolution, detailed document domain, and routed registry type."""
    selected_family = _family_for_contract_type(selected_contract_type)
    document_family, confidence, evidence, scores, technology_classification = _classify_document_family(text, clauses)

    comparable = selected_family in {"SALE", "HOUSE_LEASE", "SERVICE", "TECHNOLOGY"}
    if document_family == "UNCERTAIN" or not comparable:
        routed_family = selected_family
        resolution = "USER_SELECTION_ACCEPTED"
        compatibility = "UNCERTAIN" if comparable else "NOT_COMPARABLE"
        rejected = ""
    elif document_family == selected_family:
        routed_family = selected_family
        resolution = "AGREE"
        compatibility = "COMPATIBLE"
        rejected = ""
    elif confidence == "high":
        routed_family = document_family
        resolution = "DOCUMENT_OVERRIDE"
        compatibility = "CONFLICT"
        rejected = selected_family
    else:
        routed_family = selected_family
        resolution = "UNCERTAIN_CONFLICT"
        compatibility = "CONFLICT"
        rejected = document_family

    family_types = {"SALE": "sale", "HOUSE_LEASE": "house_lease", "SERVICE": "service", "TECHNOLOGY": "technology"}
    routed_type = family_types.get(routed_family, selected_contract_type)
    document_type = family_types.get(document_family, routed_type)
    document_domain = resolve_contract_domain(document_type, text, clauses)
    reasons = [
        "document family scores: " + ", ".join(f"{family}={score}" for family, score in scores.items()),
        f"document family={document_family}, confidence={confidence}",
    ]
    primary_transaction = dict(technology_classification.get("primary_transaction") or {}) if document_family == "TECHNOLOGY" else {"type": document_type}
    ancillary_obligations = list(technology_classification.get("ancillary_obligations") or []) if document_family == "TECHNOLOGY" else []
    post_delivery_obligations = [
        obligation for obligation in ancillary_obligations
        if obligation in {"TRAINING", "TECHNICAL_SUPPORT", "TECHNICAL_GUIDANCE", "INSTALLATION_AND_COMMISSIONING"}
    ]
    consumer_context = consumer_service_context(text, technology_classification)
    classification_context = {
        "primary_transaction": primary_transaction,
        "secondary_transactions": list(technology_classification.get("secondary_transactions") or []),
        "ancillary_obligations": ancillary_obligations,
        "post_delivery_obligations": post_delivery_obligations,
        "consumer_service_context": consumer_context,
        "candidate_scores": scores,
        "technology_candidate_scores": dict(technology_classification.get("candidate_scores") or {}),
        "primary_transaction_reason": (
            "New technical result creation and development-performance facts control; training/support are ancillary obligations."
            if document_family == "TECHNOLOGY" and str(technology_classification.get("primary_contract_type") or "") in {"commissioned_development", "cooperative_development"}
            else "The highest-confidence family evidence controls before Review Registry loading."
        ),
    }
    if resolution == "DOCUMENT_OVERRIDE":
        reasons.append("High-confidence document evidence overrides the incompatible user selection before Review Registry loading.")
    elif resolution == "UNCERTAIN_CONFLICT":
        reasons.append("Conflicting document evidence is not strong enough for an automatic override.")
    else:
        reasons.append("The user selection remains a compatible or uncontested routing prior.")
    public_document = document_domain.to_public_dict()
    public_document["family"] = document_family
    public_document["classification_confidence"] = confidence
    public_document["classification_scores"] = scores
    public_document["primary_contract_type"] = technology_classification.get("primary_contract_type") if document_family == "TECHNOLOGY" else document_type
    public_document["primary_subtype"] = technology_classification.get("primary_subtype") if document_family == "TECHNOLOGY" else document_domain.contract_subtype
    resolution_result = DomainSelectionResolution(
        selected_contract_type=selected_contract_type,
        document_domain=public_document,
        compatibility=compatibility,
        resolution=resolution,
        selected_domain=routed_family,
        rejected_domain=rejected,
        confidence=confidence,
        reasons=reasons,
        classification_evidence=evidence,
        classification_context=classification_context,
    )
    routed_domain = resolve_contract_domain(routed_type, text, clauses)
    return resolution_result, routed_domain, routed_type


def domain_selection_consistency_gate(
    resolution: DomainSelectionResolution,
    review_ids: Sequence[str],
    perspective: Dict[str, Any] | None = None,
) -> Dict[str, Any]:
    resolved = resolution.selected_domain
    if resolved == "SALE":
        wrong_ids = [item_id for item_id in review_ids if item_id.startswith(("HL-", "SVC-"))]
    elif resolved == "HOUSE_LEASE":
        wrong_ids = [item_id for item_id in review_ids if item_id.startswith(("S-", "FS-", "RE-", "SVC-"))]
    elif resolved == "SERVICE":
        wrong_ids = [item_id for item_id in review_ids if item_id.startswith(("S-", "FS-", "RE-", "HL-"))]
    elif resolved == "TECHNOLOGY":
        wrong_ids = [item_id for item_id in review_ids if item_id.startswith(("S-", "FS-", "RE-", "HL-", "SVC-"))]
    else:
        wrong_ids = []
    failures: List[Dict[str, str]] = []
    if resolution.resolution == "UNCERTAIN_CONFLICT":
        failures.append({
            "requirement": "DOMAIN_SELECTION_CONSISTENCY_GATE",
            "failure_stage": "Domain Selection",
            "root_cause": "User selection conflicts with document classification without enough confidence for automatic override.",
            "responsible_function": "resolve_domain_selection",
            "current_status": "FAIL",
        })
    if wrong_ids:
        failures.append({
            "requirement": "DOMAIN_SELECTION_CONSISTENCY_GATE",
            "failure_stage": "Review Registry",
            "root_cause": f"Resolved domain {resolved} loaded incompatible reviews: {', '.join(wrong_ids)}",
            "responsible_function": "get_checklist_for_resolution",
            "current_status": "FAIL",
        })
    primary_type = str(((resolution.classification_context.get("primary_transaction") or {}).get("type") or ""))
    role = str((perspective or {}).get("canonical_role") or "")
    if primary_type == "commissioned_development" and role and role not in {
        "COMMISSIONING_PARTY", "DEVELOPMENT_CONTRACTOR", "ENTRUSTED_DEVELOPMENT_PARTY",
    }:
        failures.append({
            "requirement": "PRIMARY_ROLE_CONSISTENCY_GATE",
            "failure_stage": "Perspective Resolution",
            "root_cause": f"Primary commissioned-development transaction is incompatible with role {role}.",
            "responsible_function": "resolve_perspective",
            "current_status": "FAIL",
        })
    return {
        "status": "BLOCKED" if failures else "REPORT_READY",
        "gate": "DOMAIN_SELECTION_CONSISTENCY_GATE",
        "gate_status": "FAIL" if failures else "PASS",
        "wrong_domain_review_count": len(wrong_ids),
        "wrong_domain_review_ids": wrong_ids,
        "failures": failures,
    }
