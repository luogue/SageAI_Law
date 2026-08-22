"""Resolve conflicts between a user-selected contract type and document evidence."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Sequence, Tuple

from review_v2.clause_parser import ParsedClause
from review_v2.domain_resolution import DomainResolution, resolve_contract_domain


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


def _family_for_contract_type(contract_type: str) -> str:
    value = (contract_type or "").strip().lower()
    if value in {"sale", "买卖合同"}:
        return "SALE"
    if value in {"lease", "house_lease", "房屋租赁合同"}:
        return "HOUSE_LEASE"
    if value in {"service", "服务合同"}:
        return "SERVICE"
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


def _classify_document_family(text: str, clauses: Sequence[ParsedClause]) -> tuple[str, str, List[DomainSelectionEvidence], Dict[str, int]]:
    lease_score, lease_evidence = _collect_family_evidence(text, clauses, "HOUSE_LEASE", _LEASE_SIGNALS)
    sale_score, sale_evidence = _collect_family_evidence(text, clauses, "SALE", _SALE_SIGNALS)
    service_score, service_evidence = _collect_family_evidence(text, clauses, "SERVICE", _SERVICE_SIGNALS)
    scores = {"SALE": sale_score, "HOUSE_LEASE": lease_score, "SERVICE": service_score}
    winner = max(scores, key=lambda key: scores[key])
    winner_score = scores[winner]
    runner_up = max((score for key, score in scores.items() if key != winner), default=0)
    margin = winner_score - runner_up
    evidence_by_family = {"SALE": sale_evidence, "HOUSE_LEASE": lease_evidence, "SERVICE": service_evidence}
    winner_evidence = evidence_by_family[winner]
    if winner_score >= 8 and margin >= 4 and len(winner_evidence) >= 2:
        confidence = "high"
    elif winner_score >= 5 and margin >= 2:
        confidence = "medium"
    else:
        return "UNCERTAIN", "low", lease_evidence + sale_evidence + service_evidence, scores
    return winner, confidence, lease_evidence + sale_evidence + service_evidence, scores


def resolve_domain_selection(
    selected_contract_type: str,
    text: str,
    clauses: Sequence[ParsedClause],
) -> tuple[DomainSelectionResolution, DomainResolution, str]:
    """Return the public resolution, detailed document domain, and routed registry type."""
    selected_family = _family_for_contract_type(selected_contract_type)
    document_family, confidence, evidence, scores = _classify_document_family(text, clauses)

    comparable = selected_family in {"SALE", "HOUSE_LEASE", "SERVICE"}
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

    routed_type = "sale" if routed_family == "SALE" else "house_lease" if routed_family == "HOUSE_LEASE" else "service" if routed_family == "SERVICE" else selected_contract_type
    document_type = "sale" if document_family == "SALE" else "house_lease" if document_family == "HOUSE_LEASE" else "service" if document_family == "SERVICE" else routed_type
    document_domain = resolve_contract_domain(document_type, text, clauses)
    reasons = [
        f"document family scores: SALE={scores['SALE']}, HOUSE_LEASE={scores['HOUSE_LEASE']}, SERVICE={scores['SERVICE']}",
        f"document family={document_family}, confidence={confidence}",
    ]
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
    )
    routed_domain = resolve_contract_domain(routed_type, text, clauses)
    return resolution_result, routed_domain, routed_type


def domain_selection_consistency_gate(
    resolution: DomainSelectionResolution,
    review_ids: Sequence[str],
) -> Dict[str, Any]:
    resolved = resolution.selected_domain
    if resolved == "SALE":
        wrong_ids = [item_id for item_id in review_ids if item_id.startswith(("HL-", "SVC-"))]
    elif resolved == "HOUSE_LEASE":
        wrong_ids = [item_id for item_id in review_ids if item_id.startswith(("S-", "FS-", "RE-", "SVC-"))]
    elif resolved == "SERVICE":
        wrong_ids = [item_id for item_id in review_ids if item_id.startswith(("S-", "FS-", "RE-", "HL-"))]
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
    return {
        "status": "BLOCKED" if failures else "REPORT_READY",
        "gate": "DOMAIN_SELECTION_CONSISTENCY_GATE",
        "gate_status": "FAIL" if failures else "PASS",
        "wrong_domain_review_count": len(wrong_ids),
        "wrong_domain_review_ids": wrong_ids,
        "failures": failures,
    }
