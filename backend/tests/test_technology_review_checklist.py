"""Structural tests for the technology-contract review checklist."""

from review_v2.engine import review_contract_v2
from review_v2.house_lease_checklist import ReviewCheckpoint
from review_v2.technology_contract_checklist import get_technology_checklist


def test_technology_review_checklist_has_52_points_and_13_modules():
    checklist = get_technology_checklist()
    module_ids = {checkpoint.item_id.rsplit("-", 1)[0] for checkpoint in checklist}

    assert len(checklist) == 52
    assert checklist[0].item_id == "TC-01-01"
    assert checklist[-1].item_id == "TC-13-04"
    assert module_ids == {f"TC-{index:02d}" for index in range(1, 14)}
    assert all(isinstance(checkpoint, ReviewCheckpoint) for checkpoint in checklist)


def test_technology_review_checklist_fields_are_complete():
    checklist = get_technology_checklist()

    for checkpoint in checklist:
        assert checkpoint.item_id.startswith("TC-")
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


def test_technology_review_checklist_has_risk_levels_and_forbidden_items():
    checklist = get_technology_checklist()
    risk_levels = {checkpoint.risk_level for checkpoint in checklist}
    kinds = {checkpoint.kind for checkpoint in checklist}

    assert risk_levels == {"高", "中", "低"}
    assert kinds == {"required", "forbidden"}


def test_technology_review_checklist_covers_required_special_rules():
    checklist = get_technology_checklist()
    by_node = {checkpoint.node_id: checkpoint for checkpoint in checklist}

    expected_nodes = {
        "technology_contract_nature",
        "technology_contract_type_classification",
        "illegal_monopoly_technology",
        "infringe_others_technology",
        "fraud_contract_existing_technology",
        "research_organization_authorization",
        "duty_achievement_ownership",
        "non_duty_achievement_ownership",
        "entrusted_development_scope",
        "entrusted_patent_application_right",
        "development_failure_risk",
        "cooperative_development_investment",
        "cooperative_patent_application_right",
        "technical_secret_result_rights",
        "technology_transfer_right_scope",
        "transfer_right_warranty",
        "technology_license_scope",
        "license_over_scope_liability",
        "consulting_decision_risk",
        "service_new_result_ownership",
        "followup_improvement_ownership",
        "improvement_no_unlawful_restriction",
        "technical_secret_confidentiality",
        "license_infringement_responsibility",
        "good_faith_secret_use_after_invalid",
        "technology_import_export_control",
    }

    assert expected_nodes <= set(by_node)
    assert "第843条" in by_node["technology_contract_nature"].legal_basis
    assert "第850条" in by_node["illegal_monopoly_technology"].legal_basis
    assert "第847条" in by_node["duty_achievement_ownership"].legal_basis
    assert "第848条" in by_node["non_duty_achievement_ownership"].legal_basis
    assert "第859条" in by_node["entrusted_patent_application_right"].legal_basis
    assert "第861条" in by_node["technical_secret_result_rights"].legal_basis
    assert "第874条" in by_node["license_infringement_responsibility"].legal_basis
    assert "第881条" in by_node["consulting_decision_risk"].legal_basis
    assert "第885条" in by_node["service_new_result_ownership"].legal_basis
    assert "第875条" in by_node["followup_improvement_ownership"].legal_basis
    assert "第877条" in by_node["technology_import_export_control"].legal_basis
    assert "第12条" in by_node["good_faith_secret_use_after_invalid"].legal_basis


def test_technology_review_checklist_has_template_blank_criteria():
    checklist = get_technology_checklist()

    assert any("__" in checkpoint.suggested_clause for checkpoint in checklist)
    assert all(
        "空白" in checkpoint.partial_criteria
        or "未勾选" in checkpoint.partial_criteria
        or checkpoint.kind == "forbidden"
        for checkpoint in checklist
    )


def test_review_v2_can_load_technology_checklist():
    output = review_contract_v2(
        "双方签订技术开发合同，委托研究开发新技术成果，约定交付技术资料、验收标准、研发经费和技术秘密保密义务。",
        "technology",
        use_llm=False,
    )

    assert output["success"] is True
    assert output["contract_type"] == "technology"
    assert output["contract_type_name"] == "技术合同"
    assert output["all_items_count"] == 52
    assert len(output["items"]) == 52
    assert output["summary"]["高"] + output["summary"]["中"] + output["summary"]["低"] == 52
