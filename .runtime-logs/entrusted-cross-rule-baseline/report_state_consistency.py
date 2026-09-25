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


def report_state_consistency_failures(items, findings=()) -> list[dict]:
    """Return gate failures; accepting these errors is never a renderer choice.

    Both dataclass report objects and serialized API dictionaries are accepted
    so production and regression tests execute precisely the same invariant.
    """
    failures = []
    by_id = {str(_get(item, "item_id", "")): item for item in items}
    positives = {review_id: _positive_keys(item) for review_id, item in by_id.items()}
    for review_id, item in by_id.items():
        applicability = _get(item, "applicability", {}) or {}
        narrative = _get(item, "narrative_state", {}) or {}
        trace = _get(item, "decision_trace", {}) or {}
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
