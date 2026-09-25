"""Cross-review claim extraction and consistency checks for review v2."""

from __future__ import annotations

from typing import Any, Dict, Iterable, List


def _evidence_text(item: Any) -> str:
    return " ".join(clause.get("text", "") for clause in (getattr(item, "evidence_clauses", None) or []))


def claim_for_review(item: Any) -> List[Dict[str, Any]]:
    """Project selected review results into machine-checkable claims."""

    claims: List[Dict[str, Any]] = []
    item_id = getattr(item, "item_id", "")
    node_id = getattr(item, "node_id", "")
    coverage = getattr(item, "coverage_status", "")
    evidence_text = _evidence_text(item)
    fact_dependencies = list(getattr(item, "fact_dependencies", None) or [])

    if node_id == "rent_arrears_breach" or item_id == "HL-015":
        claims.append(
            {
                "concept": "tenant_rent_default_threshold",
                "predicate": "exists",
                "value": coverage != "缺失",
                "source_item_id": item_id,
                "evidence_priority": "fact" if any("termination.tenant.rent_default" in dep for dep in fact_dependencies) else "review",
                "evidence": fact_dependencies or evidence_text[:120],
            }
        )

    if node_id == "agreed_termination" or item_id == "HL-017":
        has_rent_default = any(term in evidence_text for term in ("欠租", "逾期不支付租金", "拖欠租金"))
        if has_rent_default:
            claims.append(
                {
                    "concept": "tenant_rent_default_threshold",
                    "predicate": "exists",
                    "value": True,
                    "source_item_id": item_id,
                    "evidence_priority": "review",
                    "evidence": evidence_text[:120],
                }
            )

    if node_id == "early_termination_missing_consultation" or item_id == "HL-030":
        claims.append(
            {
                "concept": "early_termination_mechanism_missing",
                "predicate": "applicable",
                "value": coverage != "不适用",
                "source_item_id": item_id,
                "evidence_priority": "applicability",
                "evidence": getattr(item, "applicability", {}) or getattr(item, "reasoning_summary", ""),
            }
        )

    if node_id == "early_surrender_rule" or item_id == "HL-029":
        claims.append(
            {
                "concept": "early_termination_mechanism",
                "predicate": "exists",
                "value": coverage != "缺失",
                "source_item_id": item_id,
                "evidence_priority": "fact" if any("early_termination" in dep for dep in fact_dependencies) else "review",
                "evidence": fact_dependencies or evidence_text[:120],
            }
        )

    return claims


def apply_claims(items: Iterable[Any]) -> None:
    for item in items:
        item.claims = claim_for_review(item)


def verify_consistency(items: Iterable[Any]) -> List[Dict[str, Any]]:
    claims: Dict[tuple[str, str], List[Dict[str, Any]]] = {}
    for item in items:
        for claim in getattr(item, "claims", None) or claim_for_review(item):
            claims.setdefault((claim["concept"], claim["predicate"]), []).append(claim)

    conflicts: List[Dict[str, Any]] = []
    for (concept, predicate), grouped in claims.items():
        values = {claim.get("value") for claim in grouped}
        if len(values) <= 1:
            continue
        conflicts.append(
            {
                "type": "cross_review_claim_conflict",
                "concept": concept,
                "predicate": predicate,
                "claims": grouped,
                "recommended_action": "human_review",
            }
        )
    return conflicts
