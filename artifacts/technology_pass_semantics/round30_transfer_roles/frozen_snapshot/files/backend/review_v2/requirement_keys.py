"""Canonical identifiers for modeled requirements, separate from event types."""
import re
from typing import Any, Iterable

from review_v2.requirement_entailment import SECRET_IDENTITY_REQUIREMENT
from review_v2.technology_service_analysis import CLAIM_RESPONSE_ELEMENT_FACT_KEYS


MODELED_REQUIREMENT_KEYS = frozenset({
    SECRET_IDENTITY_REQUIREMENT, *CLAIM_RESPONSE_ELEMENT_FACT_KEYS,
    *CLAIM_RESPONSE_ELEMENT_FACT_KEYS.values(),
})

# These are established event/proposition types, not requirement identifiers.
# Some happen to share a spelling with a coverage element. Keep their separate
# type namespace intact; only element-ID fields use the requirement spelling.
EVENT_FACT_TYPES = frozenset({
    "INFRINGING_IMPLEMENTATION_TRIGGER", "LICENSEE_LOSS_ALLOCATION", "LICENSOR_ASSISTANCE_ONLY",
    "THIRD_PARTY_CLAIM_TRIGGER", "LICENSOR_CLAIM_HANDLING", "LICENSOR_LEGAL_ECONOMIC_LIABILITY",
    "FAULT_SPECIFIC_LOSS_ALLOCATION", "OPEN_ENDED_LOSS_SCOPE", "ABSENCE_EVIDENCE",
    "DEVELOPMENT_FEE", "RESULT_OWNERSHIP", "RESTRICTED_USE_LICENSE", "POST_TERMINATION_EXPIRY",
    "RECIPIENT_IMPROVEMENT_COOWNERSHIP", "RECIPIENT_IMPROVEMENT_DISPOSAL_VETO",
    "PROVIDER_FREE_IMPROVEMENT_USE", "PROVIDER_INDEPENDENT_IMPROVEMENT_OWNERSHIP",
    "LICENSEE_FREE_PERPETUAL_GRANTBACK", "LICENSOR_NEGOTIATED_IMPROVEMENT_LICENSE",
    "LICENSEE_IMPROVEMENT_OWNERSHIP_TRANSFER", "FREE_TRANSFER_OBLIGATION", "POST_TERMINATION_USE_CONTROL",
    "EXISTING_CLAIM_COST_ALLOCATION", "EXPLICIT_LICENSOR_LIABILITY_CAP",
    "PARTY_A_COMPARABLE_LIABILITY", "PARTY_B_COMPARABLE_LIABILITY", "LIABILITY_RATIO_COMPARISON",
    "ARBITRATION_PATH", "ORDINARY_LITIGATION_PATH", "RESTRICTION_SCOPE_AND_TERM", "HIGH_RESTRICTIVE_PENALTY",
    "UNAPPROVED_COMPONENT_SELECTION", "EXPLICIT_GOVERNANCE_ABSENCE", "COMPONENT_RISK_ALLOCATION",
})


def _key_shape(value: str) -> str:
    # Snake case, dashed/spaced labels and camel case are identifier spellings,
    # not different contractual requirements. Resolve only against the registry.
    value = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1_\2", value.strip())
    value = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", value)
    return re.sub(r"[\s_.-]+", "_", value).casefold()


def _identifier(value: Any) -> bool:
    return isinstance(value, str) and bool(re.fullmatch(r"[A-Za-z][A-Za-z0-9\s_.-]*", value.strip()))


def requirement_key_registry(known_requirements: Iterable[str] = ()) -> dict[str, str]:
    keys = {*MODELED_REQUIREMENT_KEYS, *(str(key) for key in known_requirements if key)}
    # The evaluator's lower-case identifier is the authoritative spelling.
    # Case variants supplied by a cached projection must not replace it.
    ordered = sorted(keys, key=lambda key: (key not in MODELED_REQUIREMENT_KEYS, key != key.lower(), key))
    registry = {}
    for key in ordered:
        registry.setdefault(_key_shape(key), _key_shape(key) if _identifier(key) else key)
    return registry


def canonical_requirement_key(value: Any, known_requirements: Iterable[str] = ()) -> Any:
    if not isinstance(value, str):
        return value
    registry = requirement_key_registry(known_requirements)
    # Registered element aliases (including dotted spellings) remain flat.
    # An otherwise qualified FactStore address is already a different kind
    # of identifier: consumers must not flatten it on a second pass.
    if _key_shape(value) in registry:
        return registry[_key_shape(value)]
    if re.fullmatch(r"[A-Za-z][A-Za-z0-9_-]*(?:\.[A-Za-z][A-Za-z0-9_-]*)+", value.strip()):
        from review_v2.contract_facts import canonical_fact_key
        return canonical_fact_key(value)
    return _key_shape(value) if _identifier(value) else value


def canonical_requirement_fact_type(value: Any, known_requirements: Iterable[str] = ()) -> Any:
    if isinstance(value, str) and value in EVENT_FACT_TYPES:
        return value
    # An unknown event is not a requirement just because its spelling looks
    # like an identifier. Only the requirement registry can cross this boundary.
    if isinstance(value, str):
        return requirement_key_registry(known_requirements).get(_key_shape(value), value)
    return value


def canonical_requirement_claim_id(value: Any, known_requirements: Iterable[str] = ()) -> Any:
    return _canonical_claim_id(value, requirement_key_registry(known_requirements))


def _canonical_claim_id(value: Any, registry: dict[str, str]) -> Any:
    if not isinstance(value, str):
        return value
    if value in EVENT_FACT_TYPES:
        return value
    if _key_shape(value) in registry:
        return registry[_key_shape(value)]
    # Claim namespaces and review IDs retain their spelling. Only a known
    # requirement suffix is normalized, e.g. risk:KEY or TC-03-04-KEY.
    for boundary in (match.end() for match in re.finditer(r"[:/]", value)):
        if value[boundary:] in EVENT_FACT_TYPES:
            return value
        suffix = registry.get(_key_shape(value[boundary:]))
        if suffix:
            return value[:boundary] + suffix
    for boundary in (match.end() for match in re.finditer(r"-", value)):
        if value[boundary:] in EVENT_FACT_TYPES:
            return value
        suffix = registry.get(_key_shape(value[boundary:]))
        if suffix:
            return value[:boundary] + suffix
    return value


_KEY_FIELDS = frozenset({
    "fact_type", "fact_types", "supports", "element_id", "element_ids",
    "supporting_element_ids", "supported_element_ids", "searched_absent_element_ids",
    "covered_element_ids", "missing_element_ids", "recommendation_element_ids",
    "required_fact_key", "source_fact_key", "required_fact_type", "canonical_fact_keys",
    "required_fact_types", "covered_fact_types", "missing_fact_types", "missing_element_types",
    "required_element_ids", "source_element_ids", "final_missing_element_ids",
    "review_evidence_supports_element_ids", "residual_element_ids", "resolves_element_ids",
    "requirement_id", "requirement_ids", "requirement_key", "requirement_keys",
    "canonical_requirement_key", "searched_absent_elements", "final_adverse_element_ids",
    "core_missing_element_ids", "adverse_element_ids", "unresolved_element_ids",
})
_FACT_TYPE_FIELDS = frozenset({
    "fact_type", "fact_types", "supports", "required_fact_type", "required_fact_types",
    "covered_fact_types", "missing_fact_types", "missing_element_types",
})
_FACT_KEY_FIELDS = frozenset({"required_fact_key", "source_fact_key", "canonical_fact_keys"})
_CLAIM_FIELDS = frozenset({
    "claim_id", "claim_ids", "supports_claim_ids", "required_claim_ids",
    "supported_claim_ids", "unsupported_claim_ids", "required_claim",
})
_REQUIREMENT_COLLECTION_FIELDS = frozenset({
    "coverage_elements", "covered_elements", "missing_elements", "unresolved_requirements",
    "final_missing_elements", "final_adverse_elements", "recommendation_elements",
    "evidence_support", "element_support", "requirements",
})
_REQUIREMENT_MAP_FIELDS = frozenset({
    "direct_fact_bindings", "direct_element_fact_keys", "element_status_by_id",
    "requirement_status_by_id", "requirement_evidence", "element_evidence",
})


def normalize_requirement_supports(payload: Any, known_requirements: Iterable[str] = ()) -> Any:
    """Copy a projection with stable, deduplicated requirement identifiers.

    Text, rule IDs, evidence IDs and unknown external FACT_TYPE values are not
    rewritten. Nested evidence aliases and caches use the same normalization.
    """
    discovered = set(known_requirements)
    from review_v2.contract_facts import canonical_fact_key

    def discover(value: Any) -> None:
        if isinstance(value, (list, tuple)):
            for entry in value:
                discover(entry)
        elif isinstance(value, dict):
            for field, entry in value.items():
                if field in _KEY_FIELDS - _FACT_TYPE_FIELDS - _FACT_KEY_FIELDS:
                    for candidate in entry if isinstance(entry, (list, tuple)) else [entry]:
                        if _identifier(candidate):
                            discovered.add(candidate)
                elif field in _REQUIREMENT_MAP_FIELDS and isinstance(entry, dict):
                    discovered.update(name for name in entry if _identifier(name))
                discover(entry)

    discover(payload)
    registry = requirement_key_registry(discovered)

    def key(value: Any) -> Any:
        return registry.get(_key_shape(value), _key_shape(value) if _identifier(value) else value) if isinstance(value, str) else value

    def claim(value: Any) -> Any:
        return _canonical_claim_id(value, registry)

    def fact_type(value: Any) -> Any:
        if isinstance(value, str) and value not in EVENT_FACT_TYPES:
            return registry.get(_key_shape(value), value)
        return value

    def values(value: Any, convert) -> Any:
        if isinstance(value, (list, tuple)):
            result = []
            for entry in value:
                normalized = convert(entry)
                if normalized not in result:
                    result.append(normalized)
            return result
        return convert(value)

    def visit(value: Any) -> Any:
        if isinstance(value, list):
            return [visit(entry) for entry in value]
        if not isinstance(value, dict):
            return value
        result = {}
        for field, entry in value.items():
            if field in _FACT_KEY_FIELDS:
                result[field] = values(entry, canonical_fact_key)
            elif field in _FACT_TYPE_FIELDS:
                result[field] = values(entry, fact_type)
            elif field in _KEY_FIELDS:
                result[field] = values(entry, key)
            elif field in _CLAIM_FIELDS:
                result[field] = values(entry, claim)
            elif field == "direct_element_fact_keys" and isinstance(entry, dict):
                result[field] = {key(name): canonical_fact_key(fact) for name, fact in entry.items()}
            elif field == "direct_fact_bindings" and isinstance(entry, dict):
                merged = {}
                for name, facts in entry.items():
                    canonical = canonical_fact_key(name)
                    retained = merged.setdefault(canonical, [])
                    for fact in facts:
                        normalized = visit(fact)
                        if normalized not in retained:
                            retained.append(normalized)
                result[field] = merged
            elif field in _REQUIREMENT_COLLECTION_FIELDS and isinstance(entry, list):
                normalized = []
                for row in entry:
                    converted = visit(row)
                    # Duplicate aliases of the same support are one support.
                    # Conflicting states/sources remain separate for the gate.
                    if converted not in normalized:
                        normalized.append(converted)
                result[field] = normalized
            elif field in _REQUIREMENT_MAP_FIELDS and isinstance(entry, dict):
                result[field] = {key(name): visit(row) for name, row in entry.items()}
            else:
                result[field] = visit(entry)
        return result

    return visit(payload)
