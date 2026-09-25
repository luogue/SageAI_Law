"""Structural tests for the guarantee-contract review checklist."""

from pathlib import Path

from docx import Document

from review_v2.engine import COVERAGE_NOT_APPLICABLE, review_contract_v2
from review_v2.guarantee_contract_checklist import get_guarantee_checklist
from review_v2.house_lease_checklist import ReviewCheckpoint


def test_guarantee_review_checklist_has_48_points_and_12_modules():
    checklist = get_guarantee_checklist()
    module_ids = {checkpoint.item_id.rsplit("-", 1)[0] for checkpoint in checklist}

    assert len(checklist) == 48
    assert checklist[0].item_id == "GUA-01-01"
    assert checklist[-1].item_id == "GUA-12-04"
    assert module_ids == {f"GUA-{index:02d}" for index in range(1, 13)}
    assert all(isinstance(checkpoint, ReviewCheckpoint) for checkpoint in checklist)


def test_guarantee_review_checklist_fields_are_complete():
    checklist = get_guarantee_checklist()

    for checkpoint in checklist:
        assert checkpoint.item_id.startswith("GUA-")
        assert checkpoint.node_id
        assert checkpoint.title
        assert checkpoint.kind in {"required", "forbidden"}
        assert checkpoint.risk_level in {"高", "中", "低"}
        assert checkpoint.terms
        assert checkpoint.risk_point_missing
        assert checkpoint.risk_point_present
        assert checkpoint.suggested_clause
        assert checkpoint.legal_basis
        assert checkpoint.legal_consequence_if_missing
        assert checkpoint.applicable_if
        assert checkpoint.semantic_question
        assert checkpoint.evidence_scope
        assert checkpoint.pass_criteria
        assert checkpoint.partial_criteria


def test_guarantee_review_checklist_has_risk_levels_and_forbidden_items():
    checklist = get_guarantee_checklist()
    risk_levels = {checkpoint.risk_level for checkpoint in checklist}
    kinds = {checkpoint.kind for checkpoint in checklist}

    assert risk_levels == {"高", "中", "低"}
    assert kinds == {"required", "forbidden"}


def test_guarantee_review_checklist_covers_required_special_rules():
    checklist = get_guarantee_checklist()
    by_node = {checkpoint.node_id: checkpoint for checkpoint in checklist}

    expected_nodes = {
        "guarantor_identity_capacity",
        "state_org_guarantor_forbidden",
        "public_nonprofit_guarantor_forbidden",
        "company_guarantor_authority",
        "written_guarantee_contract",
        "main_contract_validity_review",
        "independent_guarantee_clause_invalid",
        "guarantee_type_joint_or_general",
        "joint_guarantee_explicit_wording",
        "unclear_guarantee_type_clause",
        "guarantee_period_agreed",
        "guarantee_until_paid_unclear",
        "period_same_or_earlier_invalid",
        "prior_lawsuit_defense_rule",
        "waiver_prior_lawsuit_written",
        "guarantee_scope_agreed",
        "main_contract_change_consent",
        "assignment_notice_to_guarantor",
        "debt_transfer_guarantor_consent",
        "guarantee_share_agreed",
        "guarantor_recourse_right",
        "company_guarantee_resolution",
        "maximum_guarantee_period",
        "post_period_signature_new_guarantee",
    }

    assert expected_nodes <= set(by_node)
    assert "第683条" in by_node["state_org_guarantor_forbidden"].legal_basis
    assert "第685条" in by_node["written_guarantee_contract"].legal_basis
    assert "第682条" in by_node["main_contract_validity_review"].legal_basis
    assert "第686条" in by_node["guarantee_type_joint_or_general"].legal_basis
    assert "第692条" in by_node["guarantee_period_agreed"].legal_basis
    assert "第687条" in by_node["prior_lawsuit_defense_rule"].legal_basis
    assert "第691条" in by_node["guarantee_scope_agreed"].legal_basis
    assert "第695条" in by_node["main_contract_change_consent"].legal_basis
    assert "第696条" in by_node["assignment_notice_to_guarantor"].legal_basis
    assert "第697条" in by_node["debt_transfer_guarantor_consent"].legal_basis
    assert "第699条" in by_node["guarantee_share_agreed"].legal_basis
    assert "第700条" in by_node["guarantor_recourse_right"].legal_basis
    assert "第7条" in by_node["company_guarantee_resolution"].legal_basis
    assert "第30条" in by_node["maximum_guarantee_period"].legal_basis


def test_guarantee_review_checklist_has_template_blank_criteria():
    checklist = get_guarantee_checklist()

    assert any("__" in checkpoint.suggested_clause for checkpoint in checklist)
    assert all(
        "空白" in checkpoint.partial_criteria
        or "未勾选" in checkpoint.partial_criteria
        or checkpoint.kind == "forbidden"
        for checkpoint in checklist
    )


def test_review_v2_can_load_guarantee_checklist():
    output = review_contract_v2(
        "保证人为借款合同项下债务提供连带责任保证，保证范围包括本金、利息、违约金和实现债权费用，保证期间为主债务到期之日起两年。",
        "guarantee",
        use_llm=False,
    )

    assert output["success"] is True
    assert output["contract_type"] == "guarantee"
    assert output["contract_type_name"] == "保证合同"
    assert output["all_items_count"] == 48
    assert len(output["items"]) == 48
    assert (
        output["summary"]["高"]
        + output["summary"]["中"]
        + output["summary"]["低"]
        + output["coverage_summary"].get(COVERAGE_NOT_APPLICABLE, 0)
        == 48
    )


def test_guarantee_simple_fixture_filters_special_guarantee_points():
    # Keep this routing test independent of local, untracked fixture filenames.
    text = "保证合同。债权人甲公司、债务人乙公司、保证人王某。保证人承担一般保证责任，保证期间为主债务到期之日起两年。"
    output = review_contract_v2(text, "guarantee", use_llm=False)
    by_id = {item["item_id"]: item for item in output["items"]}

    assert by_id["GUA-12-02"]["coverage_status"] == COVERAGE_NOT_APPLICABLE
    assert by_id["GUA-12-02"]["risk_level"] == COVERAGE_NOT_APPLICABLE
    assert by_id["GUA-12-03"]["coverage_status"] == COVERAGE_NOT_APPLICABLE
    assert by_id["GUA-12-03"]["risk_level"] == COVERAGE_NOT_APPLICABLE
    assert by_id["GUA-10-02"]["coverage_status"] == COVERAGE_NOT_APPLICABLE
    assert by_id["GUA-10-02"]["risk_level"] == COVERAGE_NOT_APPLICABLE
    assert by_id["GUA-10-03"]["coverage_status"] == COVERAGE_NOT_APPLICABLE
    assert by_id["GUA-10-03"]["risk_level"] == COVERAGE_NOT_APPLICABLE
    assert by_id["GUA-04-01"]["coverage_status"] == "通过"
    assert by_id["GUA-04-02"]["coverage_status"] == COVERAGE_NOT_APPLICABLE
    assert by_id["GUA-04-04"]["coverage_status"] == COVERAGE_NOT_APPLICABLE
    assert sum(output["coverage_summary"].values()) == 48
