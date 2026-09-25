"""Atomic attribution facts and final no-gap report state, without fixture wording."""
import pytest
from copy import deepcopy

from review_v2.contract_facts import extract_contract_fact_graph
from review_v2.engine import (
    ReviewItemResult,
    _apply_default_law_narratives,
    _apply_technology_shared_fact_consistency,
    _build_narrative_state,
    _creator_reward_recommendation,
    _finding_recommendation,
    _operative_technology_clauses,
    _partial_core_covered_without_gap,
)


def review():
    return ReviewItemResult(
        item_id="SYNTHETIC", node_id="synthetic", title="测试保护事项",
        risk_level="低", status="部分覆盖", coverage_status="部分覆盖", issue_type="PARTIAL",
        risk_point_description="合同已明确覆盖本项要求。", suggested_clause_example="",
        legal_basis_index="", legal_consequence_if_missing="旧模板声称合同未明确约定。",
        applicable_if="本事项适用", matched_terms=[], evidence_clauses=[], evidence_location="",
        reasoning_summary="合同已覆盖核心要求。", applicability={"status": "APPLICABLE"},
        coverage_elements=[{"element_id": "core", "status": "COVERED", "proposition": "核心义务已覆盖。"}],
        decision_trace={"final_missing_element_ids": []},
    )


@pytest.mark.parametrize("field", [
    "发明人/设计人：张明、李华。", "发明人姓名：陈晓。", "完成人：\n王宁、赵敏。",
])
def test_named_creator_is_covered_independently_of_rewards(field):
    text = "第一条 技术标的\n发明名称：自动检测装置。\n" + field
    clauses = _operative_technology_clauses(text)
    graph = extract_contract_fact_graph(clauses)
    assert graph.matching(["creator_named_identity"])
    row = review()
    row.item_id = "TC-03-03"
    _apply_technology_shared_fact_consistency([row], text, {}, graph)
    elements = {e["element_id"]: e for e in row.coverage_elements}
    assert elements["creator_named_identity"]["status"] == "COVERED"
    assert elements["creator_named_identity"]["evidence_ids"]
    assert {k for k, e in elements.items() if e["status"] == "MISSING"} == {"creator_reward_arrangement"}
    assert row.coverage_status == "部分覆盖"
    assert row.risk_level == "低"
    assert row.action_priority == "C"


@pytest.mark.parametrize("field", [
    "发明人/设计人：____。", "完成人：待定。", "发明人姓名：请填写姓名。",
    "发明人姓名：\n申请号：202600001。", "本项目发明人为自然人。",
])
def test_unfilled_or_generic_creator_reference_is_not_named_identity(field):
    graph = extract_contract_fact_graph(_operative_technology_clauses("第一条 技术标的\n" + field))
    assert not graph.matching(["creator_named_identity"])


def test_final_empty_gap_set_does_not_reuse_stale_missing_prose():
    row = review()
    row.decision_trace["explicit_missing_elements"] = ["合同已明确覆盖本项要求"]
    narrative = _build_narrative_state(row)
    assert narrative["missing_elements"] == []
    assert narrative["partial_elements"] == []
    assert narrative["issue"] == narrative["consequence"] == narrative["recommendation"] == ""
    assert narrative["finding_exists"] is False
    assert narrative["judgment"] == "合同已覆盖本项核心要求，未发现需要独立修改的实质性缺口。"
    assert _apply_default_law_narratives([row])[0]["generated_narrative"] == ""


@pytest.mark.parametrize("status", ["MISSING", "PARTIALLY_COVERED", "ADVERSE", "REFERENCED_BUT_NOT_PROVIDED"])
def test_real_gap_or_adverse_element_is_not_suppressed_even_with_stale_empty_ids(status):
    row = review()
    row.coverage_elements.append({"element_id": "notice", "status": status, "proposition": "通知期限"})
    assert not _partial_core_covered_without_gap(row)


def test_no_action_does_not_hide_a_genuine_remaining_gap():
    row = review()
    row.coverage_elements.append({"element_id": "notice", "status": "MISSING", "proposition": "通知期限"})
    row.decision_trace["final_missing_element_ids"] = ["notice"]
    row.decision_trace["recommendation_display_state"] = {"has_active_recommendation": False}
    narrative = _build_narrative_state(row)
    assert "通知期限" in narrative["issue"]
    assert "核心义务已覆盖" not in narrative["issue"]


@pytest.mark.parametrize("flag", ["manual", "semantic", "no_final_state"])
def test_uncertain_or_unfinalized_state_is_not_silently_treated_as_covered(flag):
    row = review()
    if flag == "manual":
        row.needs_manual_review = True
    elif flag == "semantic":
        row.decision_trace["deterministic_semantic_risk"] = True
    else:
        row.decision_trace.pop("final_missing_element_ids")
    assert not _partial_core_covered_without_gap(row)


@pytest.mark.parametrize("proposition", [
    "完成人奖励、报酬或内部激励安排尚未明确（可选核验）。",
    "内部激励安排待核对。",
])
def test_creator_dedicated_copy_bypasses_missing_text_composition(monkeypatch, proposition):
    row = review()
    row.item_id = "TC-03-03"
    row.coverage_elements.append({
        "element_id": "creator_reward_arrangement", "status": "MISSING", "proposition": proposition,
    })
    row.decision_trace["final_missing_element_ids"] = ["creator_reward_arrangement"]
    expected = "建议视需要核验让与方是否已依法落实完成人奖励、报酬或内部激励安排。"
    before = deepcopy(row.to_public_dict())

    def forbidden_composition(*args, **kwargs):
        raise AssertionError("Creator reward advice must not be composed from missing text")

    monkeypatch.setattr("review_v2.engine._recommendation_from_missing_elements", forbidden_composition)
    assert _creator_reward_recommendation(row) == expected
    assert _finding_recommendation("creator_attribution", row) == expected
    assert _build_narrative_state(row)["recommendation"] == expected
    for key in ("coverage_status", "risk_level", "issue_type", "applicability", "coverage_elements", "evidence_clauses"):
        assert row.to_public_dict()[key] == before[key]
    row.item_id = "UNRELATED"
    assert _creator_reward_recommendation(row) == ""
