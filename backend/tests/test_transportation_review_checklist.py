"""Structural tests for the transportation-contract review checklist."""

from review_v2.engine import review_contract_v2
from review_v2.house_lease_checklist import ReviewCheckpoint
from review_v2.transportation_contract_checklist import get_transportation_checklist


def test_transportation_review_checklist_has_48_points_and_12_modules():
    checklist = get_transportation_checklist()
    module_ids = {checkpoint.item_id.rsplit("-", 1)[0] for checkpoint in checklist}

    assert len(checklist) == 48
    assert checklist[0].item_id == "T-01-01"
    assert checklist[-1].item_id == "T-12-04"
    assert module_ids == {f"T-{index:02d}" for index in range(1, 13)}
    assert all(isinstance(checkpoint, ReviewCheckpoint) for checkpoint in checklist)


def test_transportation_review_checklist_fields_are_complete():
    checklist = get_transportation_checklist()

    for checkpoint in checklist:
        assert checkpoint.item_id.startswith("T-")
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


def test_transportation_review_checklist_has_risk_levels_and_forbidden_items():
    checklist = get_transportation_checklist()
    risk_levels = {checkpoint.risk_level for checkpoint in checklist}
    kinds = {checkpoint.kind for checkpoint in checklist}

    assert risk_levels == {"高", "中", "低"}
    assert kinds == {"required", "forbidden"}


def test_transportation_review_checklist_covers_required_special_rules():
    checklist = get_transportation_checklist()
    by_node = {checkpoint.node_id: checkpoint for checkpoint in checklist}

    expected_nodes = {
        "transport_strict_liability",
        "transport_burden_of_proof",
        "transport_exemption_force_majeure",
        "transport_exemption_nature_reasonable_loss",
        "transport_exemption_shipper_consignee_fault",
        "transport_exemption_causation",
        "transport_compensation_agreed",
        "transport_compensation_market_price",
        "transport_declared_value_clause_prompt",
        "transport_invalid_limitation_clause",
        "transport_carrier_lien",
        "transport_lien_same_legal_relationship",
        "transport_lien_exclusion_clause",
        "transport_multimodal_contracting_carrier",
        "transport_unknown_segment_rule",
        "transport_shipper_change_before_delivery",
    }

    assert expected_nodes <= set(by_node)
    assert "第832条" in by_node["transport_strict_liability"].legal_basis
    assert "第832条" in by_node["transport_burden_of_proof"].legal_basis
    assert "第832条" in by_node["transport_exemption_force_majeure"].legal_basis
    assert "第833条" in by_node["transport_compensation_market_price"].legal_basis
    assert "第496条" in by_node["transport_declared_value_clause_prompt"].legal_basis
    assert "第836条" in by_node["transport_carrier_lien"].legal_basis
    assert "第448条" in by_node["transport_lien_same_legal_relationship"].legal_basis
    assert "第829条" in by_node["transport_shipper_change_before_delivery"].legal_basis


def test_transportation_review_checklist_has_template_blank_criteria():
    checklist = get_transportation_checklist()

    assert any("__" in checkpoint.suggested_clause for checkpoint in checklist)
    assert all(
        "空白" in checkpoint.partial_criteria
        or "未勾选" in checkpoint.partial_criteria
        or checkpoint.kind == "forbidden"
        for checkpoint in checklist
    )


def test_review_v2_can_load_transportation_checklist():
    output = review_contract_v2(
        "托运人委托承运人将货物从广州运输至上海，承运人应按时安全送达。货物名称、数量、重量以运单和交接清单为准。",
        "transportation",
        use_llm=False,
    )

    assert output["success"] is True
    assert output["contract_type"] == "transportation"
    assert output["contract_type_name"] == "运输合同"
    assert output["all_items_count"] == 48
    assert len(output["items"]) == 48
    assert output["summary"]["高"] + output["summary"]["中"] + output["summary"]["低"] == 48
