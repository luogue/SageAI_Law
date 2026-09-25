"""Three-valued, request-local rule prerequisites, evaluated before retrieval.

Resolvers provide facts; rule definitions declare keys. Identity, industry,
transaction and numeric predicates all use the same TRUE/FALSE/UNKNOWN gate.
An absent fact is unknown, never proof that a contractual obligation is missing.
"""


def resolve_prerequisites(checkpoint, facts):
    keys = getattr(checkpoint, "prerequisite_facts", ())
    if not keys:
        return None
    required = [facts.get(key, {"value": None, "label": key}) for key in keys]
    values = [fact.get("value") for fact in required]
    applicable = False if any(v is False for v in values) else True if all(v is True for v in values) else None
    if applicable is None:
        reason = "；".join(f.get("verification_instruction") or f"请核验{f.get('label', key)}"
                          for key, f in zip(keys, required) if f.get("value") is None)
    elif applicable:
        reason = "已确认适用前提：" + "、".join(f.get("label", k) for k, f in zip(keys, required))
    else:
        reason = "材料明确不满足适用前提：" + "、".join(f.get("label", k) for k, f in zip(keys, required) if f.get("value") is False)
    return dict(applicable=applicable, status="APPLICABLE" if applicable is True else "not_applicable" if applicable is False else "INSUFFICIENT_CONTEXT",
                reason=reason, user_reason=reason, machine_reason=reason,
                condition=checkpoint.applicable_if, depends_on=list(keys),
                trigger_facts=[dict(key=k, **f) for k, f in zip(keys, required)],
                trigger_evidence=[e for f in required for e in f.get("evidence", [])])


def prerequisite_status_failures(items):
    failures = []
    for item in items:
        get = item.get if isinstance(item, dict) else lambda k, d=None: getattr(item, k, d)
        applicability = get("applicability", {}) or {}
        if not applicability.get("trigger_facts") or not applicability.get("depends_on"):
            continue
        # Only gate declared fact predicates, not unrelated legacy metadata.
        facts = [f for f in applicability["trigger_facts"] if isinstance(f, dict) and "value" in f]
        if not facts:
            continue
        expected = False if any(f["value"] is False for f in facts) else True if all(f["value"] is True for f in facts) else None
        status = get("coverage_status")
        if ((expected is None and status != "INSUFFICIENT_CONTEXT")
                or (expected is False and status not in {"不适用", "NOT_APPLICABLE"})):
            failures.append(dict(requirement="APPLICABILITY_FIRST", current_status="FAIL",
                                 root_cause="身份或场景前提未成立，不得进入实质覆盖/缺失判断。", source_rules=[get("item_id")]))
    return failures
