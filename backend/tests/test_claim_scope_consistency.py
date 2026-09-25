from types import SimpleNamespace

import pytest

from review_v2.claim_scope_consistency import (
    SCOPE_REQUIREMENTS, liability_scope_elements, liability_scope_consistency_failures,
)
from review_v2.technology_service_analysis import build_technology_fact_registry


def registry(text):
    return build_technology_fact_registry(text)["third_party_claim"]


BROAD = "第三方提出侵权主张时，卖方负责与第三方交涉并承担合理法律费用和依法应承担的赔偿责任。"


def review(review_id, facts, rows, judgment=""):
    return SimpleNamespace(item_id=review_id, decision_trace={"fact_registry": {"third_party_claim": facts}},
                           coverage_elements=rows, reasoning_summary=judgment, risk_point_description="",
                           narrative_state={}, evidence_clauses=[])


def test_principle_responsibility_cannot_prove_concrete_scope():
    facts = registry(BROAD)
    assert facts["response_element_evidence"]["legal_cost_allocation"]
    assert facts["response_element_evidence"]["liability_responsible_party"]
    rows = liability_scope_elements(facts, reviewed_in="scope-review")
    assert {row["element_id"] for row in rows} == set(SCOPE_REQUIREMENTS)
    assert all(row["status"] == "MISSING" and not row["supporting_evidence"] for row in rows)


def test_concrete_scope_still_consumes_direct_evidence():
    facts = registry("第三方提出侵权主张时，卖方承担律师费、诉讼费及直接经济损失。")
    assert all(row["status"] == "COVERED" and row["supporting_evidence"]
               for row in liability_scope_elements(facts))


@pytest.mark.parametrize("status", ["MISSING", "PARTIALLY_COVERED"])
def test_cross_rule_scope_conflict_blocks(status):
    facts = registry(BROAD)
    a = review("direction-review", facts, [{"element_id": "specific_cost_and_compensation_scope", "status": "COVERED"}])
    b = review("procedure-review", facts, [{"element_id": "damages_scope", "status": status}])
    errors = liability_scope_consistency_failures([a, b])
    assert any(e["reason"] == "CROSS_RULE_LIABILITY_SCOPE_CONTRADICTION" for e in errors)


def test_narrative_cannot_claim_scope_coverage_from_principle():
    facts = registry(BROAD)
    item = review("direction-review", facts, [], "合理法律费用及依法应承担的赔偿责任范围已有明确约定。")
    assert any(e["reason"] == "CONCRETE_LIABILITY_SCOPE_NARRATIVE_WITHOUT_DIRECT_FACT"
               for e in liability_scope_consistency_failures([item]))


def test_principle_and_unresolved_scope_are_consistent():
    facts = registry(BROAD)
    items = [review(name, facts, liability_scope_elements(facts), "责任承担已有原则安排；具体赔偿范围仍需完善。")
             for name in ("direction-review", "procedure-review")]
    assert liability_scope_consistency_failures(items) == []


@pytest.mark.parametrize("judgment", [
    "现有条款不能证明赔偿责任具体范围已有明确约定。",
    "未能认定赔偿范围明确。",
    "应将赔偿范围明确到费用和损失项目。",
    "建议明确赔偿责任具体范围。",
])
def test_negative_assessment_or_drafting_is_not_a_coverage_assertion(judgment):
    item = review("direction-review", registry(BROAD), [], judgment)
    assert liability_scope_consistency_failures([item]) == []


def test_negation_in_another_atomic_clause_cannot_excuse_scope_inflation():
    item = review("direction-review", registry(BROAD), [],
                  "未能认定律师费范围明确；赔偿责任具体范围已有明确约定。")
    assert liability_scope_consistency_failures([item])
