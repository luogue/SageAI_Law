"""Keep principle-level liability separate from evidenced expense/damage scope."""
import re

from review_v2.requirement_keys import canonical_requirement_key


SCOPE_REQUIREMENTS = {
    "defense_cost_scope": "第三方主张抗辩和程序费用的具体范围及承担",
    "damages_allocation": "第三方赔偿项目及分担规则",
    "damages_scope": "第三方赔偿责任具体范围",
}
SCOPE_ALIASES = {"defense_cost_allocation": "defense_cost_scope"}
UNRESOLVED = {"MISSING", "PARTIALLY_COVERED", "PARTIAL", "UNCERTAIN"}


def _asserts_concrete_scope_coverage(text):
    # Validate assertions, not quoted judgments that are expressly rejected or
    # actions asking the parties to clarify the missing scope. Polarity belongs
    # to the atomic clause; a negation elsewhere cannot excuse a later claim.
    for clause in re.split(r"[。；;，,\n]", text):
        for match in re.finditer(
            r"赔偿(?:责任)?(?:具体)?范围(?:已经|已有|已)?(?:明确|完整|充分)|"
            r"赔偿(?:责任)?(?:具体)?范围已有明确约定", clause,
        ):
            prefix = clause[:match.start()]
            if re.search(
                r"(?:不能|无法|未能|不得|不应|尚未|没有|未)(?:直接|据此|明确)?(?:证明|认定|确认|说明)|"
                r"建议|(?:应当?|需要|须|需)(?:进一步|补充|将|把|明确|约定)", prefix,
            ):
                continue
            return True
    return False


def liability_scope_elements(registry, *, reviewed_in=""):
    """Project the same atomic facts consumed by the detailed claims review.

    A reference to a companion review does not turn an unresolved requirement
    into coverage. It only avoids issuing the same scope recommendation twice.
    """
    facts = registry.get("response_element_evidence") or {}
    result = []
    for key, label in SCOPE_REQUIREMENTS.items():
        sources = facts.get(key, [])
        details = list(dict.fromkeys(value for row in sources for value in row.get("scope_items", [])))
        result.append({
            "element_id": key, "source_fact_key": key,
            "status": "COVERED" if sources else "MISSING",
            "required_fact": label,
            "proposition": label + ("已有约定" + ("：" + "、".join(details) if details else "") if sources else ""),
            "supporting_evidence": sources,
            "bound_evidence_ids": list(dict.fromkeys(row["clause_id"] for row in sources)),
            "risk_relevant": not bool(reviewed_in),
            "owned_by_review_id": reviewed_in,
        })
    return result


def scope_review_reference(elements):
    references = {}
    for row in elements:
        if row.get("source_fact_key") in SCOPE_REQUIREMENTS and row.get("owned_by_review_id") and row.get("status") in UNRESOLVED:
            references.setdefault(row["owned_by_review_id"], []).append(row["required_fact"])
    return "".join(
        f"{'、'.join(dict.fromkeys(labels))}仍需完善，详见 {review_id}。"
        for review_id, labels in references.items()
    )


def liability_scope_consistency_failures(items, findings=()):
    """Reject cross-rule scope contradictions and narrative-only scope inflation."""
    failures, states = [], {}
    for item in items:
        registry = (item.decision_trace.get("fact_registry") or {}).get("third_party_claim")
        if not registry:
            continue
        facts = registry.get("response_element_evidence") or {}
        # Source IDs identify the event being shared. Do not compare distinct
        # claim events merely because their requirement names are identical.
        event_sources = tuple(sorted({row.get("clause_id", "")
                                      for rows in facts.values() for row in rows}))
        for element in item.coverage_elements:
            key = canonical_requirement_key(
                str(element.get("source_fact_key") or element.get("element_id") or ""),
                [*SCOPE_REQUIREMENTS, *SCOPE_ALIASES, "specific_cost_and_compensation_scope"],
            )
            key = SCOPE_ALIASES.get(key, key)
            keys = list(SCOPE_REQUIREMENTS) if key == "specific_cost_and_compensation_scope" else [key]
            for canonical in keys:
                if canonical not in SCOPE_REQUIREMENTS:
                    continue
                status = element.get("status")
                states.setdefault((event_sources, canonical), []).append((item.item_id, status))
                if status == "COVERED" and not facts.get(canonical):
                    failures.append({"review_id": item.item_id, "element_id": canonical,
                                     "reason": "CONCRETE_LIABILITY_SCOPE_WITHOUT_DIRECT_FACT"})
        texts = [item.reasoning_summary or "", item.risk_point_description or "",
                 (item.narrative_state or {}).get("judgment", ""),
                 (item.narrative_state or {}).get("issue", ""),
                 *[row.get("proposition", "") for row in item.coverage_elements],
                 *[row.get("support_summary", "") for row in item.evidence_clauses],
                 *[finding.issue for finding in findings if item.item_id in finding.source_review_ids]]
        if not facts.get("damages_scope") and any(_asserts_concrete_scope_coverage(text) for text in texts):
            failures.append({"review_id": item.item_id, "element_id": "damages_scope",
                             "reason": "CONCRETE_LIABILITY_SCOPE_NARRATIVE_WITHOUT_DIRECT_FACT"})
    for (_, key), values in states.items():
        covered = {review for review, state in values if state == "COVERED"}
        unresolved = {review for review, state in values if state in UNRESOLVED}
        if covered and unresolved and len(covered | unresolved) > 1:
            failures.append({"element_id": key, "covered_reviews": sorted(covered),
                             "unresolved_reviews": sorted(unresolved),
                             "reason": "CROSS_RULE_LIABILITY_SCOPE_CONTRADICTION"})
    return failures
