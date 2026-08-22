"""Evaluate proposed changes from the resolved reviewed-party perspective."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import re
from typing import Any, Dict, Iterable, List, Sequence, Tuple


RECOMMENDATION_ENGINE_VERSION = "recommendation-impact-6.7-freeze-1.0"


@dataclass(frozen=True)
class RecommendationImpact:
    recommendation_id: str
    target_finding_ids: List[str]
    user_role: str
    current_protection: List[str]
    proposed_change: str
    current_rights: List[str]
    current_obligations: List[str]
    current_risks: List[str]
    proposed_rights: List[str]
    proposed_obligations: List[str]
    proposed_risks: List[str]
    current_effective_rights: List[str]
    current_effective_obligations: List[str]
    proposed_effective_rights: List[str]
    proposed_effective_obligations: List[str]
    authority_ids: List[str]
    improves: bool
    weakens: bool
    improves_protection: bool
    weakens_protection: bool
    narrows_remedy: bool
    increases_liability: bool
    accelerates_obligation: bool
    shifts_risk_to_user: bool
    expands_counterparty_rights: bool
    introduces_new_limit: bool
    shortens_user_right_period: bool
    introduces_cap: bool
    introduces_exclusion: bool
    potentially_weakens_protection: bool
    tradeoff: bool
    tradeoff_exists: bool
    net_effect: str
    confidence: str
    legal_requirement_strength: str
    effect_on_client: str
    effect_on_counterparty: str
    default_rule_available: bool
    dispute_reduction_value: str
    recommendation_disposition: str
    decision_reason: str
    reason: str
    gate_result: str

    def to_public_dict(self) -> Dict[str, Any]:
        return asdict(self)


def evaluate_recommendations(
    recommendations: Sequence[Any],
    findings: Sequence[Any],
    items: Sequence[Any],
    user_role: str,
) -> Tuple[List[Any], List[RecommendationImpact], Dict[str, Any]]:
    findings_by_id = {finding.finding_id: finding for finding in findings}
    items_by_id = {item.item_id: item for item in items}
    accepted: List[Any] = []
    impacts: List[RecommendationImpact] = []
    for recommendation in recommendations:
        target_findings = [findings_by_id[fid] for fid in recommendation.target_finding_ids if fid in findings_by_id]
        source_items = [items_by_id[rid] for finding in target_findings for rid in finding.source_review_ids if rid in items_by_id]
        current_protection = list(dict.fromkeys(
            [element.get("proposition") for item in source_items for element in item.coverage_elements if element.get("status") == "COVERED" and element.get("proposition")]
            + [((item.decision_trace or {}).get("effective_gap") or {}).get("statutory_protection_scope") for item in source_items]
        ))
        current_protection = [value for value in current_protection if value]
        current_risks = list(dict.fromkeys(
            value
            for item in source_items
            for value in (((item.decision_trace or {}).get("effective_gap") or {}).get("still_unprotected_elements") or [])
            if value
        ))
        authority_ids = list(dict.fromkeys(
            authority_id
            for item in source_items
            for authority_id in (((item.decision_trace or {}).get("effective_gap") or {}).get("authority_ids") or [])
            if authority_id
        ))
        proposed = recommendation.proposed_change or recommendation.suggested_text or ""
        groups = {finding.risk_group for finding in target_findings}
        source_nodes = {str(getattr(item, "node_id", "") or "") for item in source_items}
        buyer = user_role == "BUYER"
        service_provider = user_role == "SERVICE_PROVIDER"
        strengths = {
            str((getattr(item, "decision_trace", {}) or {}).get("legal_requirement_strength") or "RISK_CONTROL")
            for item in source_items
        }
        strength_rank = {"MANDATORY": 0, "RISK_CONTROL": 1, "DEFAULT_RULE": 2, "OPTIONAL": 3}
        legal_strength = min(strengths or {"RISK_CONTROL"}, key=lambda value: strength_rank.get(value, 9))
        optional_only = bool(strengths) and strengths <= {"OPTIONAL", "DEFAULT_RULE"}
        default_rule_available = legal_strength == "DEFAULT_RULE" or any(
            str(((getattr(item, "decision_trace", {}) or {}).get("default_law_status") or "")).upper()
            in {"CLEAR_DEFAULT", "PARTIAL_DEFAULT"}
            for item in source_items
        )
        remedy_context = any(
            any(token in value.lower() for token in ("damage", "loss", "remedy", "compensation", "expectation"))
            for value in groups | source_nodes
        ) or any(any(token in value for token in ("赔偿", "损失", "可得利益", "补救")) for value in current_protection)
        statutory_mirror = bool(re.search(r"(?:依照|按照|与).{0,12}(?:现行法律|法定规则|民法典|第\d+条).{0,30}(?:不增加|不扩大|不提前|不缩窄|保持)", proposed))
        remedy_limit = buyer and remedy_context and not statutory_mirror and bool(
            re.search(r"可预见(?:性)?|可证明(?:性)?|赔偿上限|责任上限|限制|排除|封顶|仅限|不得主张|视为放弃", proposed)
        )
        accelerates_obligation = buyer and bool(re.search(r"(?:发货|装运|交付第一承运人|第一承运人).{0,16}(?:即|起|时).{0,12}(?:承担|转移|支付)", proposed))
        risk_shift = buyer and (
            (any("送达买方指定地点" in value for value in current_protection) and "第一承运人" in proposed)
            or bool(re.search(r"(?:发货|装运|第一承运人).{0,20}(?:风险转移|买方承担风险)", proposed))
            or bool(re.search(r"买方.{0,16}(?:迟延受领|拒收|未提货).{0,24}风险转移", proposed))
            or bool(re.search(r"(?:迟延受领|拒收|未提货).{0,24}(?:风险转移至买方|买方承担风险)", proposed))
        )
        liability_increase = buyer and not statutory_mirror and bool(
            re.search(r"买方.{0,20}(?:承担|负责|赔偿|支付|风险转移)", proposed)
        )
        counterparty_expansion = buyer and bool(re.search(r"(?:卖方|供方).{0,12}(?:有权单方|可单方|有权随时)", proposed))
        shortens_right_period = buyer and bool(re.search(r"(?:缩短|仅限).{0,12}(?:期限|期间)|(?:期限|期间).{0,12}(?:缩短|仅限)", proposed))
        introduces_cap = buyer and bool(re.search(r"(?:赔偿|责任|损失).{0,12}(?:上限|封顶|最高不超过)", proposed))
        introduces_exclusion = buyer and bool(re.search(r"(?:排除|免责|不予赔偿|不得主张|视为放弃)", proposed))
        optional_consumer_benefit = service_provider and optional_only and bool(
            re.search(r"(?:消费者|服务接受方|学员|用户).{0,18}(?:有权|可以|申请|解除|退费|退款|赔偿|补救)", proposed)
            or re.search(r"(?:服务方|服务提供方|经营者).{0,18}(?:应|须|承担|退还|退款|退费|赔偿|补偿)", proposed)
        )
        dispute_reduction_value = "high" if legal_strength in {"MANDATORY", "RISK_CONTROL"} else "medium" if default_rule_available else "low"
        weakens = remedy_limit or risk_shift or liability_increase or accelerates_obligation or counterparty_expansion or shortens_right_period or optional_consumer_benefit
        tradeoff = bool(re.search(r"(?:作为交换|相应换取|谈判取舍|在对方).{0,20}(?:同意|提供|承担)", proposed))
        blocked = weakens and not tradeoff
        if blocked and optional_consumer_benefit:
            reason = "The proposed service-provider change is only an optional consumer benefit and would expand the reviewed party's obligations without a mandatory or risk-control basis."
        elif blocked:
            reason = "The proposed change narrows or shifts an existing contractual/statutory protection without an explicit negotiated return."
        elif service_provider and legal_strength == "MANDATORY":
            reason = "The proposed service-provider change reflects a mandatory consumer-protection or format-clause obligation; client interest cannot filter it out."
        elif service_provider and legal_strength == "RISK_CONTROL":
            reason = "The proposed service-provider change clarifies notice, settlement, cure, evidence, or liability boundaries and reduces dispute cost without creating unbounded new liability."
        elif service_provider and default_rule_available:
            reason = "A default legal rule is available; the proposed wording is acceptable only to clarify process and preserve reasonable deductions or defenses."
        else:
            reason = "The proposed change does not silently reduce the reviewed party's current protection."
        effect_on_client = "ADVERSE" if blocked else "FAVORABLE" if legal_strength in {"MANDATORY", "RISK_CONTROL"} else "NEUTRAL"
        effect_on_counterparty = (
            "EXPANDS_RIGHTS"
            if optional_consumer_benefit or any(term in proposed for term in ("消费者", "服务接受方", "学员", "用户"))
            else "NEUTRAL"
        )
        recommendation_disposition = "BLOCK" if blocked else "ALLOW"
        impact = RecommendationImpact(
            recommendation_id=recommendation.recommendation_id,
            target_finding_ids=list(recommendation.target_finding_ids), user_role=user_role,
            current_protection=current_protection, proposed_change=proposed,
            current_rights=current_protection if buyer else [], current_obligations=[], current_risks=current_risks,
            proposed_rights=[], proposed_obligations=[proposed] if liability_increase or accelerates_obligation or optional_consumer_benefit else [],
            proposed_risks=[proposed] if weakens else [],
            current_effective_rights=current_protection if buyer else [], current_effective_obligations=[],
            proposed_effective_rights=current_protection if buyer and not weakens else [],
            proposed_effective_obligations=[proposed] if liability_increase or accelerates_obligation or optional_consumer_benefit else [],
            authority_ids=authority_ids, improves=not weakens, weakens=weakens,
            improves_protection=not weakens, weakens_protection=weakens, narrows_remedy=remedy_limit,
            increases_liability=liability_increase or optional_consumer_benefit, accelerates_obligation=accelerates_obligation,
            shifts_risk_to_user=risk_shift, expands_counterparty_rights=counterparty_expansion,
            introduces_new_limit=remedy_limit, shortens_user_right_period=shortens_right_period,
            introduces_cap=introduces_cap, introduces_exclusion=introduces_exclusion,
            potentially_weakens_protection=weakens, tradeoff=tradeoff, tradeoff_exists=tradeoff,
            net_effect="DEGRADES" if weakens else "IMPROVES_OR_NEUTRAL", confidence="high",
            legal_requirement_strength=legal_strength,
            effect_on_client=effect_on_client,
            effect_on_counterparty=effect_on_counterparty,
            default_rule_available=default_rule_available,
            dispute_reduction_value=dispute_reduction_value,
            recommendation_disposition=recommendation_disposition,
            decision_reason=reason,
            reason=reason, gate_result="BLOCKED" if blocked else "PASS",
        )
        impacts.append(impact)
        recommendation.status = "BLOCKED_NON_DEGRADATION" if blocked else "ACTIVE"
        recommendation.perspective = user_role
        recommendation.impact = impact.to_public_dict()
        if not blocked:
            accepted.append(recommendation)
    active_adverse = [impact for impact in impacts if impact.weakens and impact.gate_result != "BLOCKED"]
    gate = {
        "status": "REPORT_READY" if not active_adverse else "BLOCKED",
        "failures": [] if not active_adverse else [{
            "requirement": "RECOMMENDATION_NON_DEGRADATION_GATE", "failure_stage": "Recommendation Impact",
            "root_cause": "An adverse recommendation reached production without an explicit negotiated tradeoff.",
            "responsible_function": "evaluate_recommendations", "current_status": "FAIL",
        }],
        "gate_results": {"RECOMMENDATION_NON_DEGRADATION_GATE": "PASS" if not active_adverse else "FAIL"},
        "blocked_recommendation_ids": [impact.recommendation_id for impact in impacts if impact.gate_result == "BLOCKED"],
        "adverse_recommendation_count": len(active_adverse),
    }
    return accepted, impacts, gate
