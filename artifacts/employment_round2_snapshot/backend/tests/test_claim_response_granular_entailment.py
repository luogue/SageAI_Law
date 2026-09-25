"""Broad claim duties cannot prove a narrower procedure or expense category."""
from copy import deepcopy
from pathlib import Path

import pytest

from layers.input_layer import InputLayer
from review_v2 import engine
from review_v2.technology_service_analysis import (
    build_technology_fact_registry, claim_requirement_entailment,
    claim_response_entailment_failures,
)


CONTEXT = "第一条 第三方主张\n如第三方指控买方按约实施技术侵犯其知识产权，买方应在5个工作日内通知卖方。"
BROAD = "卖方负责与第三方进行交涉并承担由此产生的合理法律费用和依法应承担的赔偿责任。双方进行和解时应事先协商。"
DETAILS = ("administrative_handling", "litigation_handling", "attorney_fee", "litigation_cost", "direct_damage",
           "defense_cost_allocation", "damages_allocation", "damages_scope")


def item():
    return engine.ReviewItemResult(
        item_id="TC-12-02", node_id="test", title="第三方权利主张处理", risk_level="中",
        status="部分覆盖", coverage_status="部分覆盖", issue_type="PARTIAL",
        risk_point_description="", suggested_clause_example="", legal_basis_index="",
        legal_consequence_if_missing="", applicable_if="适用", matched_terms=[],
        evidence_clauses=[], evidence_location="", reasoning_summary="",
        applicability={"status": "APPLICABLE"},
    )


def project(text):
    review = item()
    clauses = engine._operative_technology_clauses(text)
    registry = build_technology_fact_registry(text)["third_party_claim"]
    engine._apply_exact_claim_response(review, clauses, registry)
    return review, clauses, registry


@pytest.fixture(scope="module")
def current():
    path = next((Path(__file__).resolve().parents[2] / "test_data").glob("38*.docx"))
    text = InputLayer()._extract_from_docx_content(path.read_bytes())
    return project(text)


def test_current_contract_preserves_broad_facts_without_specific_expansion(current):
    review, clauses, registry = current
    rows = {row["element_id"]: row for row in review.coverage_elements}
    for key in ("notification_requirement", "notification_deadline", "claim_handling",
                "legal_cost_allocation", "liability_responsible_party", "settlement_consultation"):
        assert rows[key]["status"] == "COVERED", rows[key]
        assert rows[key]["supporting_evidence"]
    assert "5个工作日" in rows["notification_deadline"]["proposition"]
    assert "赔偿责任承担主体" in rows["liability_responsible_party"]["proposition"]
    for key in DETAILS:
        assert rows[key]["status"] == "MISSING", rows[key]
        assert not rows[key]["supporting_evidence"]
    facts = registry["response_element_evidence"]
    assert facts["third_party_compensation_allocation"]
    assert facts["claim_cost_allocation"]
    assert not claim_response_entailment_failures(review.coverage_elements, clauses)


@pytest.mark.parametrize("key", DETAILS)
def test_broad_quote_does_not_entail_specific_requirement(key):
    assert claim_requirement_entailment(key, BROAD, CONTEXT + BROAD) is False


@pytest.mark.parametrize("key,statement", [
    ("administrative_handling", "卖方负责第三方主张的行政处理。"),
    ("litigation_handling", "卖方负责第三方诉讼并应诉。"),
    ("attorney_fee", "卖方承担合理律师费。"),
    ("litigation_cost", "卖方承担诉讼费。"),
    ("direct_damage", "卖方承担买方的直接经济损失。"),
    ("defense_cost_allocation", "卖方承担合理抗辩费用。"),
    ("damages_allocation", "赔偿费均由卖方承担。"),
    ("damages_scope", "卖方承担买方的直接经济损失及停产损失。"),
])
def test_specific_requirement_requires_its_own_explicit_quote(key, statement):
    assert claim_requirement_entailment(key, statement, CONTEXT + statement) is True
    review, clauses, _ = project(CONTEXT + statement)
    row = next(row for row in review.coverage_elements if row["element_id"] == key)
    assert row["status"] == "COVERED", row
    assert not claim_response_entailment_failures(review.coverage_elements, clauses)


@pytest.mark.parametrize("statement", [
    "卖方承担合理法律费用，但不包括律师费和诉讼费。",
    "卖方承担不含律师费和诉讼费的合理法律费用。",
])
def test_excluded_cost_categories_cannot_be_borrowed(statement):
    _, _, registry = project(CONTEXT + statement)
    facts = registry["response_element_evidence"]
    assert facts["legal_cost_allocation"]
    assert not facts.get("attorney_fee")
    assert not facts.get("litigation_cost")
    assert claim_requirement_entailment("attorney_fee", statement, CONTEXT + statement) is False


def test_specific_expenses_do_not_cross_borrow_the_other_actors_allocation():
    text = CONTEXT + "律师费由卖方承担，诉讼费由买方承担。"
    review, clauses, registry = project(text)
    facts = registry["response_element_evidence"]
    assert {row["actor"] for row in facts["attorney_fee"]} == {"LICENSOR"}
    assert {row["actor"] for row in facts["litigation_cost"]} == {"LICENSEE"}
    lawyer = next(row for row in review.coverage_elements if row["element_id"] == "attorney_fee")
    lawyer["supporting_evidence"][0]["actor"] = "LICENSEE"
    assert "CLAIM_RESPONSE_SOURCE_BINDING_MISMATCH" in {
        row["reason"] for row in claim_response_entailment_failures(review.coverage_elements, clauses)
    }


@pytest.mark.parametrize("key", DETAILS)
def test_corrupt_mapping_and_fact_metadata_cannot_override_source_entailment(current, key):
    original, clauses, _ = current
    review = deepcopy(original)
    row = next(row for row in review.coverage_elements if row["element_id"] == key)
    broad = next(row for row in review.coverage_elements if row["element_id"] == "legal_cost_allocation")
    row.update(status="COVERED", source_fact_key=broad["source_fact_key"],
               supporting_evidence=deepcopy(broad["supporting_evidence"]), evidence_ids=broad["evidence_ids"])
    review.decision_trace["direct_element_fact_keys"][key] = broad["source_fact_key"]
    review.decision_trace["direct_fact_bindings"][key] = deepcopy(broad["supporting_evidence"])
    failures = claim_response_entailment_failures(review.coverage_elements, clauses)
    assert any(row["element_id"] == key and row["reason"] == "CLAIM_RESPONSE_FACT_NOT_ENTAILED" for row in failures)


def test_unrelated_contract_dispute_costs_do_not_cover_inbound_claim_detail():
    text = CONTEXT + BROAD + "\n第二条 合同争议\n双方因本合同发生诉讼的，败诉方承担律师费及诉讼费。"
    _, _, registry = project(text)
    assert not registry["response_element_evidence"].get("attorney_fee")
    assert not registry["response_element_evidence"].get("litigation_cost")


def test_payable_litigation_cost_is_not_an_obligation_to_conduct_litigation():
    _, _, registry = project(CONTEXT + "卖方应承担诉讼费用。")
    assert registry["response_element_evidence"].get("litigation_cost")
    assert not registry["response_element_evidence"].get("litigation_handling")


def test_covered_source_binding_cannot_be_removed(current):
    review, clauses, _ = deepcopy(current)
    row = next(row for row in review.coverage_elements if row["element_id"] == "legal_cost_allocation")
    row["supporting_evidence"] = []
    assert any(row["element_id"] == "legal_cost_allocation"
               and row["reason"] == "CLAIM_RESPONSE_SOURCE_BINDING_MISMATCH"
               for row in claim_response_entailment_failures(review.coverage_elements, clauses))
