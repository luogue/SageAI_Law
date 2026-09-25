"""A requirement has one support identity across evidence projections."""
from copy import deepcopy

import pytest

from review_v2 import engine
from review_v2.requirement_entailment import SECRET_IDENTITY_REQUIREMENT as KEY
from review_v2.requirement_keys import (
    EVENT_FACT_TYPES, canonical_requirement_claim_id, canonical_requirement_fact_type,
    canonical_requirement_key, normalize_requirement_supports,
)


def finding():
    return engine.RiskFinding(
        finding_id="test", risk_group="technology_ip_rights_provenance", title="标的证明",
        severity="LOW", priority="C_OPTIMIZATION", source_review_ids=["TC-03-04"],
        facts=[], evidence=[], covered_element_ids=[KEY],
    )


def review():
    return engine.ReviewItemResult(
        item_id="TC-03-04", node_id="test", title="标的证明", risk_level="无",
        status="已覆盖", coverage_status="已覆盖", issue_type="PASS",
        risk_point_description="", suggested_clause_example="", legal_basis_index="",
        legal_consequence_if_missing="", applicable_if="适用", matched_terms=[],
        evidence_clauses=[], evidence_location="", reasoning_summary="",
    )


ALIASES = [KEY, KEY.upper(), KEY.replace("_", "-"), KEY.replace("_", " "),
           KEY.replace("_", "."), "technicalSecretIdentityAndDeliveryScope", f" {KEY.upper()} "]


@pytest.mark.parametrize("alias", ALIASES)
def test_modeled_requirement_spelling_has_one_canonical_key(alias):
    assert canonical_requirement_key(alias) == KEY
    for prefix in ("", "risk:", "TC-03-04-", "review/"):
        assert canonical_requirement_claim_id(prefix + alias) == prefix + KEY


def test_source_text_and_unknown_external_types_are_untouched():
    payload = {
        "fact_type": "UNMODELED_EXTERNAL_EVENT", "fact_types": ["UNMODELED_EXTERNAL_EVENT"],
        "claim_id": "GROUP:UNMODELED_EXTERNAL_EVENT", "clause_id": KEY.upper(),
        "quoted_text": KEY.upper(), "proposition": KEY.replace("_", " "),
    }
    assert normalize_requirement_supports(payload) == payload


@pytest.mark.parametrize("event", sorted(EVENT_FACT_TYPES))
def test_known_event_types_remain_distinct_from_requirement_id_namespace(event):
    known = [event.lower()]
    assert canonical_requirement_key(event, known) == event.lower()
    assert canonical_requirement_fact_type(event, known) == event
    assert canonical_requirement_claim_id("GROUP:" + event, known) == "GROUP:" + event
    normalized = normalize_requirement_supports({
        "fact_type": event, "fact_types": [event], "supports": event,
        "supporting_element_ids": [event, event.lower()],
    }, known)
    assert normalized["fact_types"] == [event]
    assert normalized["supporting_element_ids"] == [event.lower()]


def test_all_support_aliases_and_cached_requirement_keys_are_deduplicated():
    original = {
        "fact_type": KEY.upper(), "fact_types": ALIASES, "supports": ALIASES,
        "supporting_element_ids": ALIASES, "element_ids": ALIASES,
        "required_fact_types": ALIASES, "covered_fact_types": ALIASES,
        "covered_element_ids": ALIASES, "missing_element_ids": ALIASES,
        "review_evidence_supports_element_ids": ALIASES,
        "claim_id": "proof:" + KEY.upper(),
        "supports_claim_ids": ["proof:" + value for value in ALIASES],
        "required_claim_ids": ["proof:" + value for value in ALIASES],
        "direct_element_fact_keys": {KEY.upper(): KEY.upper()},
        "direct_fact_bindings": {KEY: [{"quote": "原文"}], KEY.upper(): [{"quote": "原文"}]},
    }
    snapshot = deepcopy(original)
    result = normalize_requirement_supports(original)
    for field in ("fact_types", "supports", "supporting_element_ids", "element_ids",
                  "required_fact_types", "covered_fact_types", "covered_element_ids",
                  "missing_element_ids", "review_evidence_supports_element_ids"):
        assert result[field] == [KEY]
    assert result["fact_type"] == KEY
    assert result["claim_id"] == "proof:" + KEY
    assert result["supports_claim_ids"] == ["proof:" + KEY]
    assert result["required_claim_ids"] == ["proof:" + KEY]
    assert result["direct_element_fact_keys"] == {KEY: KEY}
    assert result["direct_fact_bindings"] == {KEY: [{"quote": "原文"}]}
    assert original == snapshot
    assert normalize_requirement_supports(result) == result


def test_bundle_deduplication_merges_case_aliases_before_aggregate_counts():
    risk = finding()
    rows = [engine._external_bundle_item(
        risk_group=risk.risk_group, fact_type=alias, evidence_role="EXACT_ELEMENT_SOURCE",
        quoted_text="技术秘密内容：坐标转换算法和核心源代码。", source_type="BODY",
        claim_id=risk.risk_group + ":" + alias,
    ) for alias in ALIASES]
    for row, alias in zip(rows, ALIASES):
        row["element_ids"] = [alias]
        row["supporting_element_ids"] = [alias]
    engine._assign_final_evidence_bundle(risk, rows)
    bundle = risk.evidence_bundle
    assert bundle["post_dedup_item_count"] == 1
    assert bundle["required_fact_types"] == bundle["covered_fact_types"] == [KEY]
    assert len(bundle["supported_claim_ids"]) == 1
    for collection in ("items", "evidence_items"):
        assert len(bundle[collection]) == 1
        row = bundle[collection][0]
        assert row["fact_type"] == row["supports"] == KEY
        assert row["fact_types"] == row["element_ids"] == row["supporting_element_ids"] == [KEY]
        assert len(row["supports_claim_ids"]) == 1


def test_dynamic_coverage_registry_is_applied_to_all_final_projections():
    item, risk = review(), finding()
    key = "current_modeled_requirement"
    item.coverage_elements = [{"element_id": key, "source_fact_key": key,
                               "supporting_evidence": [{"fact_type": key.upper()}]}]
    item.evidence_clauses = [{"fact_types": [key, key.upper()], "element_ids": [key.upper()]}]
    item.review_evidence_supports_element_ids = [key, key.upper()]
    item.decision_trace = {"direct_element_fact_keys": {key.upper(): key.upper()},
                           "direct_fact_bindings": {key.upper(): [{"quote": "原文"}]}}
    risk.evidence_bundle = {"items": [{"fact_types": [key, key.upper()]}],
                            "evidence_items": [{"supports": [key.upper(), key]}],
                            "required_claim_ids": ["GROUP:" + key.upper(), "GROUP:" + key]}
    risk.covered_element_ids = [key, key.upper()]
    engine._canonicalize_requirement_evidence([item], [risk])
    assert item.evidence_clauses == [{"fact_types": [key], "element_ids": [key]}]
    assert item.review_evidence_supports_element_ids == [key]
    assert item.decision_trace["direct_element_fact_keys"] == {key: key}
    assert set(item.decision_trace["direct_fact_bindings"]) == {key}
    assert risk.covered_element_ids == [key]
    assert risk.evidence_bundle["items"][0]["fact_types"] == [key]
    assert risk.evidence_bundle["evidence_items"][0]["supports"] == [key]
    assert risk.evidence_bundle["required_claim_ids"] == ["GROUP:" + key]


def test_normalization_does_not_turn_invalid_source_into_support():
    item, risk = review(), finding()
    risk.evidence_bundle = {"items": [{
        "fact_type": KEY.replace("_", "-"),
        "quoted_text": "买方未经许可不得向第三方提供技术秘密。",
    }]}
    engine._canonicalize_requirement_evidence([item], [risk])
    failures = engine._exact_element_report_invariants([item], [risk])
    assert any(row["reason"] == "REQUIREMENT_NOT_ENTAILED_BY_SOURCE" for row in failures)


@pytest.mark.parametrize("key", ["claim_trigger", "technical_secret_result_ownership", "source_algorithm_document_delivery"])
def test_any_modeled_requirement_uses_one_format_without_a_static_allowlist(key):
    assert canonical_requirement_key(key.upper()) == key
    assert canonical_requirement_key(" ".join(key.split("_"))) == key
    payload = {"coverage_elements": [{"requirement_key": key.upper(), "status": "COVERED"},
                                     {"requirement_key": key, "status": "COVERED"}],
               "evidence_bundle": {"items": [{"fact_types": [key.upper(), key],
                                              "supporting_element_ids": [key.upper(), key]}]},
               "requirement_status_by_id": {key.upper(): "COVERED"}}
    normalized = normalize_requirement_supports(payload)
    assert normalized["coverage_elements"] == [{"requirement_key": key, "status": "COVERED"}]
    assert normalized["evidence_bundle"]["items"][0]["fact_types"] == [key]
    assert normalized["evidence_bundle"]["items"][0]["supporting_element_ids"] == [key]
    assert normalized["requirement_status_by_id"] == {key: "COVERED"}
    assert normalize_requirement_supports(normalized) == normalized


def test_normalization_preserves_conflicting_state_rows_for_quality_gate():
    normalized = normalize_requirement_supports({"coverage_elements": [
        {"element_id": "NEW_REQUIREMENT", "status": "COVERED"},
        {"element_id": "newRequirement", "status": "MISSING"},
    ]})
    assert normalized["coverage_elements"] == [
        {"element_id": "new_requirement", "status": "COVERED"},
        {"element_id": "new_requirement", "status": "MISSING"},
    ]
