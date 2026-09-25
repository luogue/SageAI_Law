"""Atomic coverage and review aggregation must not depend on a contract fixture."""
from copy import deepcopy
from types import SimpleNamespace

import pytest

from review_v2 import engine
from review_v2.clause_parser import ParsedClause


def item(rows, **overrides):
    values = dict(item_id="TEST-01", title="权属核验", risk_group="proof", risk_level="低",
                  coverage_elements=rows, coverage_status="部分覆盖", needs_manual_review=False,
                  decision_trace={}, action_suggestion="", suggested_clause_example="",
                  applicability={"status": "APPLICABLE", "applicable": True},
                  evidence_clauses=[{"clause_id": "SOURCE", "text": "合同明确约定本项责任。"}],
                  risk_point_description="保护不完整", reasoning_summary="保护不完整",
                  legal_consequence_if_missing="保护不完整")
    values.update(overrides)
    return SimpleNamespace(**values)


def test_final_required_coverage_resolves_stale_partial_and_gate_detects_regression():
    review = item([{"element_id": "required", "status": "COVERED", "proposition": "责任已明确",
                    "evidence_ids": ["SOURCE"]},
                   {"element_id": "optional", "status": "MISSING", "risk_relevant": False}],
                  decision_trace={"deterministic_semantic_risk": True, "specialized_multi_element_state": True})
    assert engine._exact_element_report_invariants([review], []) == [
        {"review_id": "TEST-01", "reason": "PARTIAL_WITHOUT_UNRESOLVED_ELEMENT"}]
    assert engine._reconcile_item_element_precedence(review) == []
    assert review.coverage_status == "通过"
    assert review.legal_consequence_if_missing == ""
    assert engine._exact_element_report_invariants([review], []) == []


@pytest.mark.parametrize("status", ["MISSING", "PARTIALLY_COVERED", "ADVERSE", "CONFLICTING"])
def test_real_remaining_gap_or_adverse_fact_does_not_become_pass(status):
    review = item([{"element_id": "required", "status": "COVERED", "evidence_ids": ["SOURCE"]},
                   {"element_id": "remaining", "status": status, "proposition": "具体通知期限"}])
    engine._reconcile_item_element_precedence(review)
    assert review.coverage_status != "通过"


@pytest.mark.parametrize("text,covered", [
    ("甲方曾向远川科技有限公司授予普通实施许可，许可期限至2032年6月30日，许可地域为广东省。",
     {"existing_license_disclosure", "existing_license_counterparty", "existing_license_term", "existing_license_territory"}),
    ("此前已向远川科技有限公司授予普通许可。", {"existing_license_disclosure", "existing_license_counterparty"}),
    ("本合同技术用于自有测试项目。", {"test_use_arrangement"}),
    ("技术由双方合作企业联合研发。", set()),
    ("本合同许可期限为三年，许可地域为广东省。", set()),
    ("此前接触过技术的合作企业均未与卖方签署完整的技术秘密许可合同。", set()),
    ("乙方曾向合作企业提供部分控制参数进行测试。", {"other_third_party_use_arrangement"}),
])
def test_disclosure_children_have_independent_positive_evidence(text, covered):
    clauses = [ParsedClause("SOURCE", "第四条", "既有使用", text, "正式合同条款", 1)]
    rows, evidence = engine._existing_technology_use_disclosure_results(clauses)
    assert {row["element_id"] for row in rows if row["status"] == "COVERED"} == covered
    assert all(row["bound_evidence_ids"] == ["SOURCE"] for row in rows if row["status"] == "COVERED")
    review = item(rows)
    for row in rows:
        audit = engine._search_final_element(review, row, clauses)
        assert (audit["result"] == "FOUND") == (row["element_id"] in covered)


def test_positive_atomic_evidence_precedes_duplicate_absence():
    review = item([{"element_id": "existing_license_disclosure", "status": "COVERED", "evidence_ids": ["SOURCE"]},
                   {"element_id": "existing_license_disclosure", "status": "MISSING"}])
    assert engine._reconcile_item_element_precedence(review) == []
    assert len(review.coverage_elements) == 1
    assert review.coverage_elements[0]["status"] == "COVERED"


def test_conditional_manual_topics_merge_sources_not_different_prerequisites():
    rows = [{"element_id": "component_license", "status": "CONDITION_UNRESOLVED",
             "prerequisite_fact": "contains_open_source", "verification_instruction": "核验是否包含开源组件；如有，核验许可证。"},
            {"element_id": "staff", "status": "CONDITION_UNRESOLVED",
             "prerequisite_fact": "employee_created", "verification_instruction": "核验员工成果归属。"}]
    first = item(deepcopy(rows), item_id="PROOF-A")
    second = item(deepcopy(rows[::-1]), item_id="PROOF-B")
    second.coverage_elements[1]["verification_instruction"] = "人工复核：核验是否包含开源组件;如有,核验许可证。"
    distinct = item(deepcopy(rows), item_id="PROOF-C")
    distinct.coverage_elements[0]["prerequisite_fact"] = "contains_third_party_code"
    records = engine._manual_review_records([first, second, distinct])
    assert len(records) == 2
    assert records[0]["source_rules"] == ["PROOF-A", "PROOF-B"]
    assert records[1]["source_rules"] == ["PROOF-C"]
    assert set(records[0]["conditional_element_ids"]) == {"component_license", "staff"}
