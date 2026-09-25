"""Resolve applicability prerequisites before evaluating conditional evidence."""

from typing import Any, Dict, Optional, Sequence


def conditional_element(
    element_id: str,
    required_fact: str,
    prerequisite: Optional[bool],
    supporting_evidence: Sequence[Dict[str, Any]],
    *,
    prerequisite_fact: str,
    verification_instruction: str,
) -> Dict[str, Any]:
    if prerequisite is None:
        status = "CONDITION_UNRESOLVED"
    elif not prerequisite:
        status = "NOT_APPLICABLE"
    else:
        status = "COVERED" if supporting_evidence else "MISSING"
    return {
        "element_id": element_id,
        "status": status,
        "proposition": (
            verification_instruction if prerequisite is None
            else f"{required_fact}不适用。" if not prerequisite
            else f"{required_fact}已有独立文件。" if supporting_evidence
            else required_fact
        ),
        "required_fact": required_fact,
        "conditional_element": True,
        "prerequisite_status": "UNKNOWN" if prerequisite is None else "TRUE" if prerequisite else "FALSE",
        "prerequisite_fact": prerequisite_fact,
        "verification_instruction": verification_instruction if prerequisite is None else "",
        "risk_relevant": prerequisite is True,
        "bound_evidence_ids": [
            str(row.get("evidence_id") or row.get("clause_id") or "")
            for row in supporting_evidence
            if prerequisite is True and (row.get("evidence_id") or row.get("clause_id"))
        ],
    }


def is_actionable_element(element: Dict[str, Any]) -> bool:
    """Unknown prerequisites create verification tasks, never drafting gaps."""
    return bool(
        element.get("status") in {"MISSING", "PARTIALLY_COVERED", "ADVERSE", "CONFLICTING", "REQUIRES_CHANGE", "UNCERTAIN"}
        and element.get("risk_relevant") is not False
        and not element.get("internal_meta")
        and element.get("user_visible") is not False
        and (not element.get("conditional_element") or element.get("prerequisite_status") == "TRUE")
    )


def conditional_element_failures(elements: Sequence[Dict[str, Any]]) -> list[Dict[str, Any]]:
    failures = []
    for element in elements:
        if not element.get("conditional_element"):
            continue
        prerequisite = element.get("prerequisite_status", "UNKNOWN")
        allowed = {
            "FALSE": {"NOT_APPLICABLE"},
            "UNKNOWN": {"CONDITION_UNRESOLVED", "INSUFFICIENT_CONTEXT"},
            "TRUE": {"COVERED", "MISSING", "PARTIALLY_COVERED", "UNCERTAIN", "REFERENCED_BUT_NOT_PROVIDED"},
        }.get(prerequisite, set())
        if element.get("status") not in allowed:
            failures.append({
                "element_id": element.get("element_id"),
                "prerequisite_status": prerequisite,
                "status": element.get("status"),
                "reason": "CONDITIONAL_ELEMENT_PRECONDITION_STATE_CONFLICT",
            })
    return failures


def unresolved_requirements(elements: Sequence[Dict[str, Any]]) -> list[Dict[str, Any]]:
    """Single projection of incomplete positive requirements, never just absent ones."""
    result = {}
    for row in elements:
        if is_actionable_element(row) and row.get("status") not in {"ADVERSE", "CONFLICTING"}:
            # Party-specific residuals remain distinct even when the rule uses
            # a shared element ID. Repeated proof rules share the same residual.
            key = (row.get("element_id"), row.get("residual_gap") or row.get("required_fact") or "")
            result.setdefault(key, dict(row))
    return list(result.values())


def party_requirement_states(element: Dict[str, Any]) -> list[Dict[str, Any]]:
    """Project each actor's actual state, never the multi-actor rollup state.

    The parent element can be PARTIALLY_COVERED because a different actor has
    no duty. That does not make an evidence-bound actor's own duty incomplete.
    Keep parent IDs for rule aggregation; actor identity owns display semantics.
    """
    result = []
    for party in element.get("party_coverage", []):
        label = str(party.get("required_fact") or "").strip("。；; ")
        if not label:
            continue
        result.append({
            "element_id": element.get("element_id"),
            "obligated_party": party.get("obligated_party"),
            "status": party.get("status"),
            "required_fact": label,
            "proposition": str(party.get("proposition") or label).strip("。；; "),
            "supporting_evidence": list(party.get("supporting_evidence") or []),
        })
    return result
