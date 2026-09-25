"""Conservative identity for duplicate, element-modeled contractual issues.

This module only describes/groups existing final states.  It neither changes
coverage nor uses rule IDs, titles or broad text similarity to merge risks.
An incomplete scope or an unmodeled independent adverse fact fails closed.
"""
from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import fields, is_dataclass
import hashlib
import json
import re
import unicodedata
from typing import Any

from review_v2.requirement_keys import canonical_requirement_key


SIGNATURE_VERSION = "underlying-issue-v1"
_UNKNOWN = {"", "unknown", "unspecified", "uncertain", "none", "null", "n/a", "na", "未明确", "未知", "待确认"}
_STATUSES = {
    "PARTIAL": "PARTIALLY_COVERED", "部分覆盖": "PARTIALLY_COVERED",
    "缺失": "MISSING", "完全缺失": "MISSING", "未覆盖": "MISSING",
    "PASS": "COVERED", "通过": "COVERED", "已覆盖": "COVERED",
    "N/A": "NOT_APPLICABLE", "不适用": "NOT_APPLICABLE",
}
_UNRESOLVED = {"MISSING", "PARTIALLY_COVERED", "ADVERSE", "CONFLICTING", "REQUIRES_CHANGE"}
_INDETERMINATE = {"UNKNOWN", "UNCERTAIN", "CONDITION_UNRESOLVED", "INSUFFICIENT_CONTEXT", "REFERENCED_BUT_NOT_PROVIDED", "NEEDS_EXTERNAL_VERIFICATION", "MANUAL_REVIEW"}
_COMPOSITE_KEYS = {"core_contract_arrangement", "general_requirement", "contract_arrangement"}
_SET_CONTENT_FIELDS = {"search_targets", "target_keys", "element_keys", "requirement_keys", "target_ids", "element_ids", "requirement_ids"}
_WHOLE_RECOMMENDATION_FIELDS = {
    "recommendation", "formal_recommendation", "suggested_clause_example", "action_suggestion",
    "建议", "正式建议", "处理建议",
}


def _mapping(value: Any) -> dict[str, Any]:
    if isinstance(value, Mapping):
        return dict(value)
    if is_dataclass(value) and not isinstance(value, type):
        return {field.name: getattr(value, field.name) for field in fields(value)}
    return {}


def _status(row):
    value = str(row.get("status") or row.get("requirement_status") or "").strip().upper()
    return _STATUSES.get(value, value)


def _string(value):
    return unicodedata.normalize("NFKC", str(value)).strip()


def _identity_value(value):
    if isinstance(value, Mapping):
        if not value:
            return None
        normalized = {str(canonical_requirement_key(_string(key))): _identity_value(entry) for key, entry in value.items()}
        if any(entry is None for entry in normalized.values()):
            return None
        return json.dumps(normalized, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    if not isinstance(value, (str, int, float)) or isinstance(value, bool):
        return None
    text = re.sub(r"\s+", "", _string(value)).casefold()
    if text in _UNKNOWN or re.search(r"(?:^|[:=])(?:unknown|unspecified|uncertain)(?:$|[:=])", text):
        return None
    return text


def _identity(row):
    identity = _mapping(row.get("fact_identity"))
    if identity:
        values = {field: identity.get(field) for field in ("canonical_fact_key", "scope", "party", "object")}
    else:
        # A title, rule ID or shared source clause is not a substitute for a
        # modeled atomic fact and its independently supplied scope and actor.
        if not row.get("source_fact_key") or row.get("atomic") is False:
            return None
        values = {
            "canonical_fact_key": row["source_fact_key"],
            "scope": row.get("scope") or row.get("fact_scope"),
            "party": row.get("obligated_party") or row.get("party") or row.get("actor"),
            "object": row.get("object_type") or row.get("object") or row.get("domain") or row.get("source_domain"),
        }
    if not isinstance(values["canonical_fact_key"], str):
        return None
    values["canonical_fact_key"] = canonical_requirement_key(values["canonical_fact_key"])
    if values["canonical_fact_key"] in _COMPOSITE_KEYS:
        return None
    # A fully scoped fact does not erase an explicitly modeled domain. Keep
    # both when supplied: material receipt and product acceptance can mention
    # identical actors/objects yet remain distinct obligations.
    for field in ("domain", "source_domain"):
        if field in identity or field in row:
            values[field] = canonical_requirement_key(identity.get(field, row.get(field)))
    normalized = {field: _identity_value(value) for field, value in values.items()}
    return normalized if all(value is not None for value in normalized.values()) else None


def _text_action(value):
    text = _string(value)
    text = re.sub(r"^(?:(?:建议|补充|补足|明确|完善|新增)\s*)+", "", text)
    if not text or re.search(r"已有(?:部分)?(?:约定|安排)|完整性仍不足|尚无法核验|仅部分明确", text):
        return None
    # Punctuation and rendering wrappers are immaterial; numbers, negations,
    # order words ('先/后') and substantive verbs are deliberately retained.
    text = re.sub(r"[\s，,；;。！？!?：:、‘’“”\"'（）()【】\[\]]", "", text).casefold()
    if not re.search(r"[a-z0-9\u4e00-\u9fff]", text):
        return None
    return text


def _normalized_content(value, *, identifier=False, unordered=False):
    if isinstance(value, str):
        return _identity_value(canonical_requirement_key(value)) if identifier else _text_action(value)
    if isinstance(value, Mapping):
        # Provenance and explanatory display labels cannot change an action's
        # identity. Other structured parameters (amount, period, remedy, etc.)
        # remain significant and are never silently dropped.
        ignored = {"source_review_id", "source_review_ids", "source_rule_id", "source_rule_ids", "evidence_ids", "supporting_evidence", "display_text"}
        entries = {}
        for key, entry in value.items():
            key = str(canonical_requirement_key(key))
            if key in ignored:
                continue
            normalized = _normalized_content(
                entry, identifier=key.endswith(("_key", "_keys")), unordered=key in _SET_CONTENT_FIELDS,
            )
            if normalized is None:
                return None
            entries[key] = normalized
        return json.dumps(entries, ensure_ascii=False, sort_keys=True, separators=(",", ":")) if entries else None
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes)):
        entries = [_normalized_content(entry, identifier=identifier) for entry in value]
        if not entries or any(entry is None for entry in entries):
            return None
        # A list of procedure steps or actions is ordered and may deliberately
        # repeat an operation. Only explicit target/search sets are unordered.
        return json.dumps(sorted(set(entries)) if unordered else entries, ensure_ascii=False, separators=(",", ":"))
    if isinstance(value, (int, float, bool)):
        return json.dumps(value)
    return None


def _actions(row):
    explicit = row.get("remediation_action") or row.get("recommendation_action")
    residual_key = next((key for key in ("residual_gap", "search_targets", "required_fact") if row.get(key)), None)
    residual = row.get(residual_key) if residual_key else None
    # Explicit actions must be preserved (e.g. delete vs retain, refund vs
    # continue payment); a common requirement cannot erase that difference.
    action = _normalized_content(explicit) if explicit else None
    residual = _normalized_content(residual, unordered=residual_key == "search_targets") if residual else None
    if explicit and action is None or residual is None:
        return None
    # The usual generated action merely prefixes a residual with '明确'. Its
    # presence in a finding but absence in the original review row is not a
    # new remedy. Concrete different actions remain significant.
    return {"remediation": action or residual, "residual": residual}


def _rows(value):
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes)):
        rows = [_mapping(row) for row in value]
        return rows if all(rows) else None
    data = _mapping(value)
    if not data:
        return None
    if any(data.get(field) for field in _WHOLE_RECOMMENDATION_FIELDS):
        signals = _mapping(data.get("aggregation_signals"))
        projection = _mapping(_mapping(data.get("decision_trace")).get("recommendation_element_projection"))
        policies = (
            data.get("policy"), data.get("recommendation_element_policy"),
            signals.get("policy"), signals.get("recommendation_element_policy"), projection.get("policy"),
        )
        if "FINAL_UNRESOLVED_ELEMENTS" not in policies:
            # An independently authored whole-rule suggestion may encode an
            # additional/different remedy not present in the atomic rows.
            # Production aggregation and the duplicate gate must both refuse
            # equivalence unless the same element-projection policy applies.
            return None
    if "final_missing_elements" in data or "final_adverse_elements" in data:
        rows = [*(data.get("final_missing_elements") or []), *(data.get("final_adverse_elements") or [])]
        # Never hide an independently modeled adverse fact just because a
        # stale final-missing projection omitted it.
        rows.extend(row for row in data.get("coverage_elements", []) if _status(_mapping(row)) in {"ADVERSE", "CONFLICTING"})
    elif "unresolved_requirements" in data:
        rows = list(data.get("unresolved_requirements") or [])
        rows.extend(data.get("adverse_elements") or [])
    else:
        rows = data.get("coverage_elements") or data.get("elements") or []
    normalized = [_mapping(row) for row in rows]
    if not all(normalized):
        return None
    # Conditional/manual uncertainty is not a certain drafting defect. Refuse
    # the whole merge when an actionable unresolved prerequisite remains.
    for raw in [*normalized, *data.get("coverage_elements", [])]:
        row = _mapping(raw)
        if row.get("risk_relevant") is False or row.get("internal_meta") or row.get("user_visible") is False:
            continue
        if _status(row) in _INDETERMINATE or (_status(row) != "NOT_APPLICABLE" and row.get("conditional_element") and row.get("prerequisite_status") != "TRUE"):
            return None
    return normalized


def underlying_issue_descriptor(value: Any) -> dict[str, Any] | None:
    """Describe a safely comparable item/finding or final atomic-element list.

    ``None`` means there is no actionable issue or not enough reliable metadata
    to aggregate it. Covered elements and rule-specific titles are ignored.
    """
    rows = _rows(value)
    if rows is None:
        return None
    requirements = {}
    titles = set()
    for row in rows:
        if row.get("risk_relevant") is False or row.get("internal_meta") or row.get("user_visible") is False:
            continue
        status = _status(row)
        if status in _INDETERMINATE or (status != "NOT_APPLICABLE" and row.get("conditional_element") and row.get("prerequisite_status") != "TRUE"):
            return None
        if status not in _UNRESOLVED:
            continue
        identity, actions = _identity(row), _actions(row)
        if identity is None or actions is None:
            return None
        if status in {"ADVERSE", "CONFLICTING"} and not any(row.get(key) for key in ("supporting_evidence", "evidence_ids", "supporting_evidence_ids", "bound_evidence_ids")):
            return None
        identity_token = json.dumps(identity, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        descriptor = {**identity, "status": status, **actions}
        previous = requirements.get(identity_token)
        if previous is not None and previous != descriptor:
            return None  # conflicting residual/action states for one atom
        requirements[identity_token] = descriptor
        if row.get("underlying_issue_title"):
            titles.add(_string(row["underlying_issue_title"]))
    if not requirements:
        return None
    result = {"version": SIGNATURE_VERSION, "requirements": [requirements[key] for key in sorted(requirements)]}
    if len(titles) == 1:
        result["display_title"] = next(iter(titles))
    return result


def underlying_issue_signature(value: Any) -> str | None:
    descriptor = underlying_issue_descriptor(value)
    if descriptor is None:
        return None
    payload = {key: descriptor[key] for key in ("version", "requirements")}
    canonical = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return SIGNATURE_VERSION + ":" + hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def group_duplicate_underlying_issues(values: Sequence[Any]) -> list[list[int]]:
    """Return only duplicate index groups; callers keep all source-rule IDs."""
    groups = {}
    for index, value in enumerate(values):
        signature = underlying_issue_signature(value)
        if signature is not None:
            groups.setdefault(signature, []).append(index)
    return [indices for indices in groups.values() if len(indices) > 1]
