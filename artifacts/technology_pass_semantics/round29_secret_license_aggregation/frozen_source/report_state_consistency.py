"""Read-only invariants for final applicability, requirement and report state.

The evaluator remains the state authority. This module neither repairs a
projection nor infers coverage from related text: it rejects contradictions
between explicitly identified atomic requirements in the final projections.
"""
import json
import re
from typing import Any, Iterable

from review_v2.element_resolution import unresolved_requirements
from review_v2.requirement_keys import canonical_requirement_key
from review_v2.underlying_issue import group_duplicate_underlying_issues


def _get(row: Any, field: str, default=None):
    return row.get(field, default) if isinstance(row, dict) else getattr(row, field, default)


def _status(value: Any) -> str:
    value = str(value or "").strip().upper().replace("-", "_").replace(" ", "_")
    return {"不适用": "NOT_APPLICABLE", "N/A": "NOT_APPLICABLE", "NA": "NOT_APPLICABLE",
            "已覆盖": "COVERED", "通过": "COVERED", "PASS": "COVERED",
            "部分覆盖": "PARTIALLY_COVERED", "PARTIAL": "PARTIALLY_COVERED",
            "缺失": "MISSING", "完全缺失": "MISSING"}.get(value, value)


def _rows(value: Any):
    if isinstance(value, dict):
        yield value
        for entry in value.values():
            yield from _rows(entry)
    elif isinstance(value, (list, tuple)):
        for entry in value:
            yield from _rows(entry)


def _key(row: Any) -> str:
    if isinstance(row, str):
        return str(canonical_requirement_key(row))
    return str(canonical_requirement_key(row.get("element_id") or row.get("requirement_id")
                                        or row.get("requirement_key") or ""))


def _keys(rows: Iterable[Any]) -> set[str]:
    return {key for row in rows if (key := _key(row))}


def _direct_source(row: dict) -> bool:
    if str(row.get("source_type") or "").upper() in {"SEARCH_AUDIT", "ABSENCE_SEARCH"}:
        return False
    if "ABSENCE" in str(row.get("evidence_role") or "").upper():
        return False
    return bool(row.get("quote") or row.get("quoted_text") or row.get("text"))


def _positive_keys(item: Any) -> set[str]:
    # Partial coverage has a genuinely absent residual. It must not be treated
    # as full positive support simply because the parent has a source quote.
    sources = list(_get(item, "evidence_clauses", []) or [])
    result = set()
    for element in _get(item, "coverage_elements", []) or []:
        if _status(element.get("status")) != "COVERED":
            continue
        direct = any(_direct_source(row) for row in element.get("supporting_evidence", []))
        ids = set(element.get("bound_evidence_ids") or element.get("evidence_ids") or
                  element.get("supporting_evidence_ids") or [])
        if not direct and ids:
            direct = any(_direct_source(row) and (row.get("clause_id") in ids or
                         row.get("evidence_id") in ids) for row in sources)
        if direct:
            result.add(_key(element))
    return result


def _absent(row: dict) -> set[str]:
    search = row.get("element_search") or {}
    result = _status(row.get("result") or row.get("search_status") or search.get("result"))
    is_audit = str(row.get("source_type") or "").upper() in {"SEARCH_AUDIT", "ABSENCE_SEARCH"}
    if result not in {"NOT_FOUND", "ABSENT", "MISSING"} and not (is_audit and not result):
        return set()
    values = row.get("searched_absent_element_ids") or row.get("searched_absent_elements") or []
    if isinstance(values, str):
        values = [values]
    keys = _keys(values)
    if _key(row):
        keys.add(_key(row))
    if _key(search):
        keys.add(_key(search))
    return keys


def _asserts_not_applicable(text: Any) -> bool:
    for sentence in re.split(r"[。；;\n]", str(text or "")):
        if re.search(r"^(?:审查判断\s*[:：]\s*)?(?:本项|本规则|该规则|本事项)?\s*(?:不适用|无需适用)(?:[，,：:\s]|$)", sentence.strip()):
            return True
    return False


def _scoped_fact_identity(row: dict):
    """A matching name alone never proves two rules discuss the same fact.

    Evaluators supply scope, actor and object identity. Inapplicable dimensions
    should use an explicit value (for example CONTRACT_PARTIES), not an empty
    wildcard that could conflate different actors or materials.
    """
    identity = row.get("fact_identity") or row.get("shared_fact_identity") or {}
    key = identity.get("canonical_fact_key") or identity.get("fact_key") or row.get("canonical_fact_key")
    scope = identity.get("scope") or identity.get("scope_id") or row.get("fact_scope")
    party = identity.get("party") or identity.get("party_id") or row.get("obligated_party")
    target = identity.get("object") or identity.get("object_id") or row.get("fact_object")
    if not all(isinstance(value, str) and value.strip() for value in (key, scope, party, target)):
        return None
    return (str(canonical_requirement_key(key)), scope.strip(), party.strip(), target.strip())


def _cross_rule_fact_failures(items):
    states = {}
    for item in items:
        review_id = str(_get(item, "item_id", ""))
        if _status(_get(item, "coverage_status")) == "NOT_APPLICABLE":
            continue
        direct_keys = _positive_keys(item)
        for element in _get(item, "coverage_elements", []) or []:
            identity = _scoped_fact_identity(element)
            if identity is None or _status(element.get("status")) not in {"COVERED", "MISSING"}:
                continue
            if element.get("conditional_element") and _status(element.get("prerequisite_status")) != "TRUE":
                continue
            states.setdefault(identity, []).append((review_id, _key(element), _status(element["status"]),
                                                   _key(element) in direct_keys))
    failures = []
    for identity, values in states.items():
        covered = {review_id for review_id, _, status, direct in values if status == "COVERED" and direct}
        missing = {review_id for review_id, _, status, _ in values if status == "MISSING"}
        if covered and missing and len(covered | missing) > 1:
            failures.append({"reason": "CROSS_RULE_SCOPED_FACT_STATUS_CONFLICT",
                             "canonical_fact_key": identity[0], "scope": identity[1], "party": identity[2],
                             "object": identity[3], "covered_reviews": sorted(covered),
                             "missing_reviews": sorted(missing)})
    return failures


def _manual_review_required(item: Any) -> bool:
    manual = {"MANUAL_REVIEW", "HUMAN_REVIEW", "NEEDS_MANUAL_REVIEW", "NEEDS_EXTERNAL_VERIFICATION",
              "人工复核", "需人工复核", "人工核验"}
    if _get(item, "needs_manual_review") is True:
        return True
    return any(_status(_get(item, field)) in manual for field in (
        "status", "issue_type", "recommended_action", "action_priority", "review_priority",
    ))


def _confirmed_secret_domains(trace: dict):
    """Consume established applicability facts, not source-text keyword guesses."""
    result = {}
    family = trace.get("confidentiality_applicability") or {}
    technical_ids = family.get("technical_secret_clause_ids") or []
    if family.get("technical_secret_positive_fact") is True and technical_ids:
        result["technical_secret"] = technical_ids
        result["confidential_material"] = technical_ids
    scope_ids = family.get("confidentiality_scope_clause_ids") or []
    if family.get("confidentiality_scope_positive_fact") is True and scope_ids:
        result["confidential_material"] = scope_ids
    material = trace.get("secret_material_applicability") or {}
    if _status(material.get("status")) in {"CONFIRMED", "COVERED"} and material.get("source_clause_ids"):
        result["confidential_material"] = material["source_clause_ids"]
    return result


def _report_confirmed_secret_domains(items):
    """Share established contract prerequisites without keyword re-extraction.

    The proving rule owns the source trace. Dependent rules need not duplicate
    that trace, and absence of a local copy cannot negate the shared fact.
    """
    confirmed = {}
    for item in items:
        review_id = str(_get(item, "item_id", ""))
        trace = _get(item, "decision_trace", {}) or {}
        for domain, sources in _confirmed_secret_domains(trace).items():
            record = confirmed.setdefault(domain, {"source_clause_ids": [], "source_review_ids": []})
            for source in sources:
                if source not in record["source_clause_ids"]:
                    record["source_clause_ids"].append(source)
            if review_id and review_id not in record["source_review_ids"]:
                record["source_review_ids"].append(review_id)
    return confirmed


def _denied_secret_domains(reason: Any):
    # A reason saying no *newly developed secret result* does not deny that
    # confidential background data exists. Nor does a permitted public-data
    # exception negate secret material elsewhere in the same contract.
    denied = set()
    for sentence in re.split(r"[。；;\n]", str(reason or "")):
        if re.search(r"如果|若|如无|除非|即使|并非|不能据此|不代表", sentence):
            continue
        # In “未形成以技术秘密为对价基础的收费安排”, the absent
        # object is the fee arrangement, not the embedded basis. Preserve
        # genuine “未形成技术秘密范围” denials for the same strict check.
        sentence = re.sub(r'以[^，,；;。]{1,45}为[^，,；;。]{0,16}(?:基础|标的|条件|前提)',
                          '该基础', sentence)
        for domain, subject in (
            ("technical_secret", r"技术秘密(?!成果|许可|转让|交易)|非公开技术信息"),
            ("confidential_material", r"保密(?:资料|材料|信息|范围)|涉密资料"),
        ):
            if re.search(r"(?:不|未)(?:存在|涉及|包含|提供|交付|形成).{0,8}(?:" + subject + r")|"
                         r"(?:尚未|未能|无法|不能|未)(?:明确|确认|识别|查明).{0,16}(?:" + subject + r")", sentence):
                denied.add(domain)
    return denied


_TRANSACTION_LABELS = {
    "委托开发": {"ENTRUSTED_DEVELOPMENT"}, "合作开发": {"COOPERATIVE_DEVELOPMENT"},
    "技术开发": {"ENTRUSTED_DEVELOPMENT", "COOPERATIVE_DEVELOPMENT"},
    "技术转让": {"TECHNOLOGY_TRANSFER"}, "技术许可": {"TECHNOLOGY_LICENSE"},
    "技术咨询": {"TECHNICAL_CONSULTING"}, "技术服务": {"TECHNICAL_SERVICE"},
}


def _active_transaction_types(context: dict):
    aliases = {"COMMISSIONED_DEVELOPMENT": "ENTRUSTED_DEVELOPMENT", "TECHNOLOGY_CONSULTING": "TECHNICAL_CONSULTING"}
    values = [context.get("primary_subtype"), context.get("contract_subtype"),
              *(context.get("active_transaction_types") or []), *(context.get("secondary_modules") or []),
              *(context.get("active_scenes") or []), *(context.get("activated_modules") or [])]
    return {aliases.get(_status(value), _status(value)) for value in values if value}


def _declared_transaction_types(text: str) -> set[str]:
    declared = {scene for label, scenes in _TRANSACTION_LABELS.items() if label in text for scene in scenes}
    # Chinese coordinated type names commonly share their leading modifier:
    # “技术转让或许可” declares both technology transfer and technology license.
    # Only expand adjacent type names in that list, not later references to a
    # licensee, fees, or another rule's subject matter.
    type_word = r"(?:开发|转让|许可|咨询|服务)"
    coordinated = (r"技术" + type_word + r"(?:合同)?(?:\s*(?:或|和|与|及|、|/|／)\s*"
                   r"(?:技术)?" + type_word + r"(?:合同)?)+")
    for match in re.finditer(coordinated, text):
        for word in re.findall(type_word, match.group()):
            declared.update(_TRANSACTION_LABELS["技术" + word])
    return declared


def applicability_description_failures(items, transaction_context=None):
    """Validate explanation against activated scenes; never route from prose.

    An open-ended mixed-obligation description is not an exclusive type list.
    Without an established transaction context this invariant makes no guess.
    """
    active = _active_transaction_types(transaction_context or {})
    if not active:
        for item in items:
            trace = _get(item, "decision_trace", {}) or {}
            # The legal-basis router records the same established classification
            # on every applicable technology item. Some late atomic projections
            # retain it without the classifier-only trace on the nature rule.
            for field in ("classification_context", "global_subtype_applicability_gate", "subtransaction_activation",
                          "legal_basis_applicability"):
                active.update(_active_transaction_types(trace.get(field) or {}))
    if not active:
        return []
    failures = []
    for item in items:
        applicability = _get(item, "applicability", {}) or {}
        if applicability.get("applicable") is False or _status(applicability.get("status")) == "NOT_APPLICABLE":
            continue
        if not (applicability.get("applicable") is True or _status(applicability.get("status")) in {"APPLICABLE", "CONDITIONALLY_APPLICABLE"}):
            continue
        text = str(_get(item, "applicable_if", "") or "")
        if not re.match(r"^(?:仅|主要)?适用于", text):
            continue
        if re.search(r"其他合同|其他.{0,12}场景|混合(?:合同|交易|履约)|附随|独立.{0,12}义务", text):
            continue
        declared = _declared_transaction_types(text)
        if declared and not declared.intersection(active):
            failures.append({"review_id": _get(item, "item_id", ""),
                             "reason": "APPLICABILITY_DESCRIPTION_EXCLUDES_ACTIVE_TRANSACTION",
                             "declared_transaction_types": sorted(declared), "active_transaction_types": sorted(active)})
    return failures


def report_state_consistency_failures(items, findings=(), *, transaction_context=None) -> list[dict]:
    """Return gate failures; accepting these errors is never a renderer choice.

    Both dataclass report objects and serialized API dictionaries are accepted
    so production and regression tests execute precisely the same invariant.
    """
    findings = list(findings)
    failures = _cross_rule_fact_failures(items)
    failures.extend(applicability_description_failures(items, transaction_context))
    # Aggregation and its gate deliberately share one conservative atomic
    # signature. Related titles or a common clause alone do not make duplicates.
    for indices in group_duplicate_underlying_issues(findings):
        risk_ids, source_ids = set(), set()
        for index in indices:
            finding = findings[index]
            risk_id = _get(finding, "finding_id") or _get(finding, "risk_id")
            if risk_id:
                risk_ids.add(str(risk_id))
            for field in ("source_rule_ids", "source_review_ids"):
                source_ids.update(str(value) for value in (_get(finding, field, []) or []))
        failures.append({"reason": "DUPLICATE_UNDERLYING_ISSUE", "finding_indices": indices,
                         "risk_ids": sorted(risk_ids), "source_rule_ids": sorted(source_ids)})
    by_id = {str(_get(item, "item_id", "")): item for item in items}
    confirmed_prerequisites = _report_confirmed_secret_domains(items)
    positives = {review_id: _positive_keys(item) for review_id, item in by_id.items()}
    for review_id, item in by_id.items():
        applicability = _get(item, "applicability", {}) or {}
        narrative = _get(item, "narrative_state", {}) or {}
        trace = _get(item, "decision_trace", {}) or {}
        if trace.get("review_polarity") == "NEGATIVE_CLAUSE_CHECK" and _status(_get(item, "coverage_status")) == "COVERED":
            contaminated = [str(_get(f, "finding_id", "")) for f in findings
                            if review_id in (_get(f, "source_review_ids", []) or [])]
            gaps = unresolved_requirements(_get(item, "coverage_elements", []) or [])
            if contaminated or gaps:
                failures.append({"review_id": review_id, "reason": "NEGATIVE_PASS_AGGREGATION_CONTAMINATION",
                                 "finding_ids": contaminated, "missing_element_ids": sorted(_keys(gaps))})
        if trace.get("atomic_requirement_family") and _status(_get(item, "coverage_status")) == "PARTIALLY_COVERED":
            unresolved = unresolved_requirements(_get(item, "coverage_elements", []) or [])
            expected = _keys(unresolved)
            consequence_ids = _keys(trace.get("consequence_element_ids") or [])
            consequence = str(narrative.get("consequence") or "")
            omitted = [_key(row) for row in unresolved
                       if str(row.get("residual_gap") or row.get("required_fact") or "").strip("。；; ") not in consequence]
            if consequence_ids != expected or omitted or consequence != _get(item, "legal_consequence_if_missing", ""):
                failures.append({"review_id": review_id, "reason": "CONSEQUENCE_REQUIREMENTS_MISMATCH",
                                 "expected": sorted(expected), "actual": sorted(consequence_ids), "omitted": omitted})
            # A shared source quote must not collapse several distinct residual
            # requirements in the detail narrative while advice still lists them.
            for field, text in (("judgment", narrative.get("judgment")),
                                ("risk_point_description", _get(item, "risk_point_description"))):
                absent_labels = [_key(row) for row in unresolved
                                 if str(row.get("residual_gap") or row.get("required_fact") or "").strip("。；; ")
                                 not in str(text or "")]
                if absent_labels:
                    failures.append({"review_id": review_id, "reason": "DETAIL_UNRESOLVED_REQUIREMENTS_OMITTED",
                                     "projection": field, "omitted": absent_labels})
        verdicts = [narrative.get("judgment"), narrative.get("issue"),
                    _get(item, "reasoning_summary"), _get(item, "risk_point_description")]
        inapplicable = (applicability.get("applicable") is False or
                        _status(applicability.get("status")) == "NOT_APPLICABLE" or
                        any(_asserts_not_applicable(text) for text in verdicts))
        if inapplicable and _status(_get(item, "coverage_status")) != "NOT_APPLICABLE":
            failures.append({"review_id": review_id, "reason": "NOT_APPLICABLE_NARRATIVE_STATE_CONFLICT",
                             "coverage_status": _get(item, "coverage_status")})
        if _status(_get(item, "coverage_status")) == "COVERED" and _manual_review_required(item):
            failures.append({"review_id": review_id, "reason": "PASS_WITH_PENDING_MANUAL_REVIEW"})
        if inapplicable or _status(_get(item, "coverage_status")) == "NOT_APPLICABLE":
            confirmed = confirmed_prerequisites
            # Reason aliases are separate exported projections. A corrected
            # display reason cannot excuse a stale machine/user reason that
            # still denies the confirmed prerequisite.
            reason_texts = {f"applicability.{field}": applicability.get(field)
                            for field in ("reason", "machine_reason", "user_reason")}
            reason_texts.update({f"narrative.{index}": text for index, text in enumerate(verdicts)})
            denied_by = {}
            for field, text in reason_texts.items():
                for domain in _denied_secret_domains(text):
                    denied_by.setdefault(domain, []).append(field)
            denials = set(denied_by)
            for domain in sorted(denials & confirmed.keys()):
                failures.append({"review_id": review_id, "reason": "NA_REASON_DENIES_CONFIRMED_PREREQUISITE",
                                 "prerequisite_domain": domain, **confirmed[domain],
                                 "reason_fields": denied_by[domain]})
        for element in _get(item, "coverage_elements", []) or []:
            for party in element.get("party_coverage", []):
                if _status(party.get("status")) != "COVERED":
                    continue
                facts = party.get("supporting_evidence") or []
                if not facts or any(not _direct_source(fact) or fact.get("obligated_party") !=
                                    party.get("obligated_party") for fact in facts):
                    failures.append({"review_id": review_id, "element_id": _key(element),
                                     "obligated_party": party.get("obligated_party"),
                                     "reason": "COVERED_PARTY_WITHOUT_EXACT_SOURCE"})
        for row in _rows({"trace": _get(item, "decision_trace", {}),
                          "evidence": _get(item, "evidence_clauses", [])}):
            for key in sorted(_absent(row) & positives[review_id]):
                failures.append({"review_id": review_id, "element_id": key,
                                 "reason": "POSITIVE_REQUIREMENT_WITH_ABSENCE_SEARCH"})

    for finding in findings:
        finding_id = _get(finding, "finding_id", "")
        source_ids = list(_get(finding, "source_review_ids", []) or [])
        bundle = _get(finding, "evidence_bundle", {}) or {}
        for row in _rows(bundle):
            absent = _absent(row)
            if not absent:
                continue
            owners = row.get("supporting_review_ids") or ([row["review_id"]] if row.get("review_id") else source_ids)
            for review_id in owners:
                for key in sorted(absent & positives.get(review_id, set())):
                    failures.append({"risk_id": finding_id, "review_id": review_id, "element_id": key,
                                     "reason": "POSITIVE_REQUIREMENT_WITH_ABSENCE_SEARCH"})

        signals = _get(finding, "aggregation_signals", {}) or {}
        if signals.get("recommendation_element_policy") != "FINAL_UNRESOLVED_ELEMENTS":
            continue
        source_rows = [element for review_id in source_ids if review_id in by_id
                       for element in _get(by_id[review_id], "coverage_elements", []) or []]
        expected = _keys(row for row in unresolved_requirements(source_rows)
                         if _key(row) != "core_contract_arrangement")
        actual = _keys(_get(finding, "final_missing_elements", []) or [])
        projections = {"aggregate": actual}
        for name, owner, field in (
            ("aggregate_cache", signals, "unresolved_requirements"),
            ("evidence", bundle, "unresolved_requirements"),
        ):
            # A modeled finding must always project its residual set, including
            # an explicitly empty set; absence of a cache is not positive proof.
            if field in owner:
                projections[name] = _keys(owner[field] or [])
        for name, ids in (signals.get("unresolved_projection_element_ids") or {}).items():
            projections[name] = _keys(ids or [])
        for name, projected in projections.items():
            if projected != expected:
                failures.append({"risk_id": finding_id, "projection": name,
                                 "reason": "REPORT_UNRESOLVED_REQUIREMENTS_MISMATCH",
                                 "expected": sorted(expected), "actual": sorted(projected)})

        adverse = _keys(_get(finding, "final_adverse_elements", []) or [])
        recommendation = signals.get("recommendation_element_ids")
        if recommendation is not None:
            recommended = _keys(recommendation)
            if recommended != expected | adverse:
                failures.append({"risk_id": finding_id, "reason": "RECOMMENDATION_REQUIREMENTS_MISMATCH",
                                 "expected": sorted(expected | adverse), "actual": sorted(recommended)})
        for review_id in source_ids:
            item = by_id.get(review_id)
            if item is None:
                continue
            projection = (_get(item, "decision_trace", {}) or {}).get("recommendation_element_projection") or {}
            if "missing_element_ids" in projection:
                own = _keys(unresolved_requirements(_get(item, "coverage_elements", []) or []))
                if _keys(projection["missing_element_ids"]) != own:
                    failures.append({"risk_id": finding_id, "review_id": review_id,
                                     "reason": "DETAIL_RECOMMENDATION_REQUIREMENTS_MISMATCH"})
    # Evidence aliases, caches and the final bundle can report the same defect.
    unique = {}
    for failure in failures:
        unique.setdefault(json.dumps(failure, ensure_ascii=False, sort_keys=True), failure)
    return list(unique.values())
