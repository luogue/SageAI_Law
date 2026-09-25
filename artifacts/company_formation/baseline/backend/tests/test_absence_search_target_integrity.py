"""Missing evidence requires a concrete query, including partially covered rules."""
from copy import deepcopy

import pytest

from review_v2 import engine


def review(elements=()):
    return engine.ReviewItemResult(
        item_id="TC-10-02", node_id="test", title="改进成果分享", risk_level="低",
        status="部分覆盖", coverage_status="部分覆盖", issue_type="PARTIAL",
        risk_point_description="", suggested_clause_example="", legal_basis_index="",
        legal_consequence_if_missing="", applicable_if="适用", matched_terms=[],
        evidence_clauses=[], evidence_location="", reasoning_summary="",
        applicability={"status": "APPLICABLE"}, coverage_elements=deepcopy(list(elements)),
    )


def finding():
    return engine.RiskFinding(
        finding_id="test-finding", risk_group="improvement_sharing_license", title="分享许可",
        severity="LOW", priority="C_OPTIMIZATION", source_review_ids=["TC-10-02"],
        facts=[], evidence=[],
    )


INVALID_TARGETS = [
    [], [""], ["   "], ["。；，：、..."], ["___"], ["未明确"], ["部分覆盖"],
    ["已有原则安排但具体条件不完整"], ["优先许可或另行协商机制已有原则安排，具体许可条件尚不完整。"],
    ["已约定"], ["已经明确"], ["已完成"], ["未检索"], ["PASS"], ["PARTIAL"],
]


@pytest.mark.parametrize("targets", INVALID_TARGETS)
def test_no_empty_punctuation_or_status_only_query_is_absence_evidence(targets):
    row = {"element_id": "test", "status": "PARTIALLY_COVERED", "residual_gap": "尚需完善",
           "search_targets": targets, "proposition": "已有原则安排但具体条件不完整"}
    assert engine._objective_fact_search_targets(row) == []
    item = review([row])
    clauses = engine._operative_technology_clauses("第十条 改进成果\n双方享有优先许可权。")
    audit = engine._search_final_element(item, row, clauses)
    assert audit["result"] == "INVALID_SEARCH_TARGET"
    evidence, diagnostic = engine._absence_proposition_evidence(
        risk_group="test", searched_scope=["合同正文"], required_elements=targets,
    )
    assert evidence == {}
    assert diagnostic["search_status"] == "INVALID_SEARCH_TARGET"
    assert diagnostic["missing_elements"] == []


@pytest.mark.parametrize("targets", INVALID_TARGETS)
@pytest.mark.parametrize("owner", ["review", "operation", "finding", "alias", "nested", "diagnostic"])
def test_release_gate_blocks_invalid_absence_even_without_a_finding(targets, owner):
    item, risk = review(), finding()
    audit = {"source_type": "SEARCH_AUDIT", "search_targets": targets, "result": "NOT_FOUND",
             "query_patterns": ["query"], "searched_document_hash": "document"}
    risks = [risk]
    if owner == "review":
        item.evidence_clauses = [audit]
        risks = []
    elif owner == "operation":
        item.decision_trace["element_absence_searches"] = [audit]
    elif owner == "finding":
        risk.evidence_bundle = {"items": [audit]}
    elif owner == "alias":
        risk.evidence_bundle = {"evidence_items": [audit]}
    elif owner == "nested":
        risk.evidence_bundle = {"items": [{"source_type": "SEARCH_AUDIT",
                                          "search_targets": ["改进成果许可期限"], "element_search": audit}]}
    else:
        risk.evidence_bundle = {"absence_evidence": {"search_status": "FOUND",
                                                     "invalid_search_target": True, "search_targets": targets}}
    failures = engine._exact_element_report_invariants([item], risks)
    assert "INVALID_ABSENCE_SEARCH_TARGET" in {row["reason"] for row in failures}
    assert engine._release_quality_gate([item], risks, "审查报告")["status"] == "BLOCKED"


def test_real_objective_fact_targets_and_prohibited_fact_search_remain_valid():
    targets = ["改进成果许可费或定价机制", "改进成果许可地域", "改进成果许可期限",
               "改进成果商业使用边界", "改进成果分许可条件", "限制自主研发的条款"]
    assert engine._objective_fact_search_targets({"search_targets": targets}) == targets
    item = review()
    item.evidence_clauses = [{"source_type": "SEARCH_AUDIT", "search_targets": targets}]
    assert engine._absence_search_target_failures([item], []) == []


@pytest.mark.parametrize("field", ["target", "required_elements", "missing_elements"])
@pytest.mark.parametrize("value", ["。", "", "已有原则安排但具体条件不完整"])
def test_valid_targets_cannot_hide_an_invalid_explicit_target_field(field, value):
    item = review()
    item.evidence_clauses = [{"source_type": "SEARCH_AUDIT", "search_targets": ["通知期限"], field: value}]
    assert engine._absence_search_target_failures([item], [])
    assert engine._release_quality_gate([item], [], "审查报告")["status"] == "BLOCKED"


def test_partial_principle_expands_to_real_fields_without_a_second_actionable_gap():
    item = review()
    text = ("专利实施许可合同\n甲方（被许可方）与乙方（许可方）约定许可专利技术。\n"
            "第十条 改进成果\n甲方改进成果归甲方，乙方使用需另行协商；"
            "乙方改进成果归乙方，甲方享有优先许可权。")
    classification = {"primary_subtype": "TECHNOLOGY_LICENSE", "tertiary_subtype": "PATENT_LICENSE"}
    engine._apply_technology_transaction_evidence_consistency([item], text, classification)
    elements = {row["element_id"]: row for row in item.coverage_elements}
    principle = elements["priority_or_negotiated_license"]
    expected = ["改进成果许可费或定价机制", "改进成果许可地域", "改进成果许可期限",
                "改进成果商业使用边界", "改进成果分许可条件"]
    assert principle["status"] == "PARTIALLY_COVERED"
    assert principle["search_targets"] == expected
    assert principle["residual_gap"] == "、".join(expected)
    assert not engine.is_actionable_element(principle)
    assert elements["license_fee"]["status"] == "MISSING"
    assert engine._missing_search_targets(engine.unresolved_requirements(item.coverage_elements)) == expected
    engine._resolve_final_element_searches([item], engine._operative_technology_clauses(text))
    audits = item.decision_trace["element_absence_searches"]
    assert {row["element_id"] for row in audits} == {
        "license_fee", "license_territory", "license_duration", "commercial_use_and_sublicense",
    }
    assert engine._absence_search_target_failures([item], []) == []


def test_covered_child_field_cannot_remain_in_parent_absence_targets():
    item = review([
        {"element_id": "priority_or_negotiated_license", "status": "PARTIALLY_COVERED",
         "risk_relevant": False, "proposition": "许可原则已有约定但具体条件不完整",
         "residual_gap": "许可地域及期限", "search_targets": ["改进成果许可地域", "改进成果许可期限"],
         "evidence_ids": ["E1"]},
        {"element_id": "license_territory", "status": "COVERED", "proposition": "中国境内使用改进成果",
         "search_targets": ["改进成果许可地域"], "evidence_ids": ["E1"]},
        {"element_id": "license_duration", "status": "MISSING", "proposition": "改进成果许可期限",
         "search_targets": ["改进成果许可期限"]},
    ])
    item.evidence_clauses = [{"clause_id": "E1", "text": "甲方在中国境内使用改进成果。"}]
    engine._resolve_final_element_searches([item], engine._operative_technology_clauses("第十条\n甲方在中国境内使用改进成果。"))
    assert item.coverage_elements[0]["search_targets"] == ["改进成果许可期限"]
    assert "地域" not in item.coverage_elements[0]["residual_gap"]
    assert {row["element_id"] for row in item.decision_trace["element_absence_searches"]} == {"license_duration"}


def test_partial_missing_absence_binding_is_rejected():
    item = review([{"element_id": "notice", "status": "PARTIALLY_COVERED", "proposition": "已有通知义务",
                    "residual_gap": "通知期限", "search_targets": ["通知期限"]}])
    risk = finding()
    risk.aggregation_signals = {"recommendation_element_policy": "FINAL_UNRESOLVED_ELEMENTS"}
    risk.final_missing_elements = [{**item.coverage_elements[0], "source_review_id": item.item_id}]
    risk.evidence_bundle = {"items": [], "unresolved_requirements": risk.final_missing_elements}
    failures = engine._exact_element_report_invariants([item], [risk])
    assert "FINAL_MISSING_WITHOUT_ELEMENT_ABSENCE_SEARCH" in {row["reason"] for row in failures}
