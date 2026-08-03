"""Structural tests for the utility-supply-contract review checklist."""

from review_v2.engine import review_contract_v2
from review_v2.house_lease_checklist import ReviewCheckpoint
from review_v2.utility_supply_contract_checklist import get_utility_supply_checklist


def test_utility_supply_review_checklist_has_48_points_and_12_modules():
    checklist = get_utility_supply_checklist()
    module_ids = {checkpoint.item_id.rsplit("-", 1)[0] for checkpoint in checklist}

    assert len(checklist) == 48
    assert checklist[0].item_id == "US-01-01"
    assert checklist[-1].item_id == "US-12-04"
    assert module_ids == {f"US-{index:02d}" for index in range(1, 13)}
    assert all(isinstance(checkpoint, ReviewCheckpoint) for checkpoint in checklist)


def test_utility_supply_review_checklist_fields_are_complete():
    checklist = get_utility_supply_checklist()

    for checkpoint in checklist:
        assert checkpoint.item_id.startswith("US-")
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


def test_utility_supply_review_checklist_has_risk_levels_and_forbidden_items():
    checklist = get_utility_supply_checklist()
    risk_levels = {checkpoint.risk_level for checkpoint in checklist}
    kinds = {checkpoint.kind for checkpoint in checklist}

    assert risk_levels == {"高", "中", "低"}
    assert kinds == {"required", "forbidden"}


def test_utility_supply_review_checklist_covers_required_special_rules():
    checklist = get_utility_supply_checklist()
    by_node = {checkpoint.node_id: checkpoint for checkpoint in checklist}

    expected_nodes = {
        "utility_supply_contract_nature",
        "electricity_water_gas_heat_classification",
        "actual_supply_relation",
        "mandatory_contracting_obligation",
        "reasonable_access_conditions",
        "improper_refusal_clause",
        "national_supply_quality_standard",
        "contractual_supply_parameters",
        "quality_nonconform_remedy",
        "safe_continuous_supply_obligation",
        "planned_interruption_notice",
        "temporary_interruption_notice",
        "no_notice_interruption_clause",
        "natural_disaster_repair_obligation",
        "emergency_repair_time_limit",
        "user_fee_payment",
        "overdue_fee_liquidated_damage",
        "suspension_after_demand_period",
        "suspension_procedure_compliance",
        "safe_economical_planned_use",
        "illegal_use_prohibition",
        "sub_supply_without_consent",
        "property_boundary_point",
        "supplier_side_maintenance",
        "user_side_maintenance",
        "metering_device_rule",
        "billing_standard_method",
        "metering_dispute_handling",
        "contract_change_or_termination",
        "property_company_cutoff",
        "boundary_facility_diagram_attachment",
    }

    assert expected_nodes <= set(by_node)
    assert "第648条" in by_node["mandatory_contracting_obligation"].legal_basis
    assert "第650条" in by_node["property_boundary_point"].legal_basis
    assert "第651条" in by_node["national_supply_quality_standard"].legal_basis
    assert "第652条" in by_node["planned_interruption_notice"].legal_basis
    assert "第653条" in by_node["natural_disaster_repair_obligation"].legal_basis
    assert "第654条" in by_node["suspension_after_demand_period"].legal_basis
    assert "第655条" in by_node["safe_economical_planned_use"].legal_basis
    assert "第656条" in by_node["electricity_water_gas_heat_classification"].legal_basis
    assert "第585条" in by_node["overdue_fee_liquidated_damage"].legal_basis
    assert "第944条" in by_node["property_company_cutoff"].legal_basis


def test_utility_supply_review_checklist_has_template_blank_criteria():
    checklist = get_utility_supply_checklist()

    assert any("__" in checkpoint.suggested_clause for checkpoint in checklist)
    assert all(
        "空白" in checkpoint.partial_criteria
        or "未勾选" in checkpoint.partial_criteria
        or checkpoint.kind == "forbidden"
        for checkpoint in checklist
    )


def test_review_v2_can_load_utility_supply_checklist():
    output = review_contract_v2(
        "供电公司与用户签订供用电合同，约定用电地址、容量、电费计量方式、供电质量标准、欠费催告和中止供电程序。",
        "utility_supply",
        use_llm=False,
    )

    assert output["success"] is True
    assert output["contract_type"] == "utility_supply"
    assert output["contract_type_name"] == "供用电、水、气、热力合同"
    assert output["all_items_count"] == 48
    assert len(output["items"]) == 48
    assert output["summary"]["高"] + output["summary"]["中"] + output["summary"]["低"] == 48
