"""Structural tests for the service-contract review checklist."""

from review_v2.engine import review_contract_v2
from review_v2.house_lease_checklist import ReviewCheckpoint
from review_v2.service_contract_checklist import get_service_checklist


def test_service_review_checklist_has_48_points_and_12_modules():
    checklist = get_service_checklist()
    module_ids = {checkpoint.item_id.rsplit("-", 1)[0] for checkpoint in checklist}

    assert len(checklist) == 48
    assert checklist[0].item_id == "SVC-01-01"
    assert checklist[-1].item_id == "SVC-12-04"
    assert module_ids == {f"SVC-{index:02d}" for index in range(1, 13)}
    assert all(isinstance(checkpoint, ReviewCheckpoint) for checkpoint in checklist)


def test_service_review_checklist_fields_are_complete():
    checklist = get_service_checklist()

    for checkpoint in checklist:
        assert checkpoint.item_id.startswith("SVC-")
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
        assert checkpoint.semantic_question
        assert checkpoint.evidence_scope
        assert checkpoint.pass_criteria
        assert checkpoint.partial_criteria


def test_service_review_checklist_has_risk_levels_and_forbidden_items():
    checklist = get_service_checklist()
    risk_levels = {checkpoint.risk_level for checkpoint in checklist}
    kinds = {checkpoint.kind for checkpoint in checklist}

    assert risk_levels == {"高", "中", "低"}
    assert kinds == {"required", "forbidden"}


def test_service_review_checklist_covers_required_special_rules():
    checklist = get_service_checklist()
    by_node = {checkpoint.node_id: checkpoint for checkpoint in checklist}

    expected_nodes = {
        "service_contract_type_identification",
        "provider_legal_qualification",
        "service_content_standard",
        "service_quality_standard",
        "prepaid_consumption_identification",
        "prepaid_refund_condition_process",
        "format_no_refund_clause",
        "format_clause_prompt_explain",
        "health_change_termination",
        "waive_legal_termination_right",
        "provider_change_requires_consent",
        "provider_unilateral_change_right",
        "platform_terms_change_consent",
        "service_nonperformance_remedy",
        "service_quality_nonconform_remedy",
        "operator_closure_refund",
        "consumer_personal_reason_termination",
        "consumer_excessive_penalty_clause",
        "punitive_damages_closure",
        "termination_refund_calculation",
    }

    assert expected_nodes <= set(by_node)
    assert "第53条" in by_node["prepaid_refund_condition_process"].legal_basis
    assert "第497条" in by_node["format_no_refund_clause"].legal_basis
    assert "第13条" in by_node["health_change_termination"].legal_basis
    assert "第509条" in by_node["provider_change_requires_consent"].legal_basis
    assert "第23条" in by_node["punitive_damages_closure"].legal_basis
    assert "第496条" in by_node["platform_terms_change_consent"].legal_basis
    assert "第577条" in by_node["service_quality_nonconform_remedy"].legal_basis
    assert "第585条" in by_node["consumer_excessive_penalty_clause"].legal_basis


def test_service_review_checklist_has_template_blank_criteria():
    checklist = get_service_checklist()

    assert any("__" in checkpoint.suggested_clause for checkpoint in checklist)
    assert all(
        "空白" in checkpoint.partial_criteria
        or "未勾选" in checkpoint.partial_criteria
        or checkpoint.kind == "forbidden"
        for checkpoint in checklist
    )


def test_review_v2_can_load_service_checklist():
    output = review_contract_v2(
        "甲方向乙方提供培训服务，乙方预付课程费12000元，服务期限一年，未提供课程的按剩余课时退费。",
        "service",
        use_llm=False,
    )

    assert output["success"] is True
    assert output["contract_type"] == "service"
    assert output["contract_type_name"] == "服务合同"
    assert output["all_items_count"] == 48
    assert len(output["items"]) == 48
    assert output["summary"]["高"] + output["summary"]["中"] + output["summary"]["低"] == 48
