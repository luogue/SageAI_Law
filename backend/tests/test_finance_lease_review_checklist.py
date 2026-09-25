"""Structural tests for the finance-lease review checklist."""

from review_v2.engine import review_contract_v2
from review_v2.finance_lease_contract_checklist import get_finance_lease_checklist
from review_v2.house_lease_checklist import ReviewCheckpoint


def test_finance_lease_review_checklist_has_45_points_and_15_modules():
    checklist = get_finance_lease_checklist()
    module_ids = {checkpoint.item_id.rsplit("-", 1)[0] for checkpoint in checklist}

    assert len(checklist) == 45
    assert checklist[0].item_id == "FL-01-01"
    assert checklist[-1].item_id == "FL-15-03"
    assert module_ids == {f"FL-{index:02d}" for index in range(1, 16)}
    assert all(isinstance(checkpoint, ReviewCheckpoint) for checkpoint in checklist)


def test_finance_lease_review_checklist_fields_are_complete():
    checklist = get_finance_lease_checklist()

    for checkpoint in checklist:
        assert checkpoint.item_id.startswith("FL-")
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


def test_finance_lease_review_checklist_has_risk_levels_and_forbidden_items():
    checklist = get_finance_lease_checklist()
    risk_levels = {checkpoint.risk_level for checkpoint in checklist}
    kinds = {checkpoint.kind for checkpoint in checklist}

    assert risk_levels == {"高", "中", "低"}
    assert kinds == {"required", "forbidden"}


def test_finance_lease_review_checklist_covers_required_special_rules():
    checklist = get_finance_lease_checklist()
    by_node = {checkpoint.node_id: checkpoint for checkpoint in checklist}

    expected_nodes = {
        "finance_lease_nature",
        "finance_lease_dual_attribute",
        "not_finance_lease_structure",
        "real_asset_existence",
        "fake_asset_invalid",
        "lessee_select_seller_asset",
        "lessor_no_unauthorized_change",
        "seller_delivery_to_lessee",
        "lessee_refusal_conditions",
        "lessor_defect_warranty_exemption",
        "lessor_defect_exception",
        "lessee_claim_against_seller",
        "rent_composition_cost_profit",
        "lessee_risk_loss_burden",
        "rent_remedy_choice",
        "request_both_remedies",
        "ownership_registration",
        "end_ownership_agreed",
        "value_settlement_rule",
        "sale_leaseback_identification",
    }

    assert expected_nodes <= set(by_node)
    assert "第735条" in by_node["finance_lease_nature"].legal_basis
    assert "第737条" in by_node["fake_asset_invalid"].legal_basis
    assert "第739条" in by_node["lessee_select_seller_asset"].legal_basis
    assert "第740条" in by_node["lessee_refusal_conditions"].legal_basis
    assert "第747条" in by_node["lessor_defect_warranty_exemption"].legal_basis
    assert "第741条" in by_node["lessee_claim_against_seller"].legal_basis
    assert "第746条" in by_node["rent_composition_cost_profit"].legal_basis
    assert "第751条" in by_node["lessee_risk_loss_burden"].legal_basis
    assert "第752条" in by_node["rent_remedy_choice"].legal_basis
    assert "第745条" in by_node["ownership_registration"].legal_basis
    assert "第757条" in by_node["end_ownership_agreed"].legal_basis
    assert "第758条" in by_node["value_settlement_rule"].legal_basis
    assert "第2条" in by_node["sale_leaseback_identification"].legal_basis


def test_finance_lease_review_checklist_has_template_blank_criteria():
    checklist = get_finance_lease_checklist()

    assert any("__" in checkpoint.suggested_clause for checkpoint in checklist)
    assert all(
        "空白" in checkpoint.partial_criteria
        or "未勾选" in checkpoint.partial_criteria
        or checkpoint.kind == "forbidden"
        for checkpoint in checklist
    )


def test_review_v2_can_load_finance_lease_checklist():
    output = review_contract_v2(
        "出租人根据承租人选择向出卖人购买设备并出租给承租人使用，承租人按租金支付表支付租金，期满支付象征性价款后取得设备所有权。",
        "finance_lease",
        use_llm=False,
    )

    assert output["success"] is True
    assert output["contract_type"] == "finance_lease"
    assert output["contract_type_name"] == "融资租赁合同"
    assert output["all_items_count"] == 45
    assert len(output["items"]) == 45
    assert sum(output["coverage_summary"].values()) == 45
    assert output["coverage_summary"].get("不适用", 0) >= 3
