"""Structural tests for the warehouse-contract review checklist."""

from review_v2.engine import review_contract_v2
from review_v2.house_lease_checklist import ReviewCheckpoint
from review_v2.warehouse_contract_checklist import get_warehouse_checklist


def test_warehouse_review_checklist_has_40_points_and_10_modules():
    checklist = get_warehouse_checklist()
    module_ids = {checkpoint.item_id.rsplit("-", 1)[0] for checkpoint in checklist}

    assert len(checklist) == 40
    assert checklist[0].item_id == "WH-01-01"
    assert checklist[-1].item_id == "WH-10-04"
    assert module_ids == {f"WH-{index:02d}" for index in range(1, 11)}
    assert all(isinstance(checkpoint, ReviewCheckpoint) for checkpoint in checklist)


def test_warehouse_review_checklist_fields_are_complete():
    checklist = get_warehouse_checklist()

    for checkpoint in checklist:
        assert checkpoint.item_id.startswith("WH-")
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


def test_warehouse_review_checklist_has_risk_levels_and_forbidden_items():
    checklist = get_warehouse_checklist()
    risk_levels = {checkpoint.risk_level for checkpoint in checklist}
    kinds = {checkpoint.kind for checkpoint in checklist}

    assert risk_levels == {"高", "中", "低"}
    assert kinds == {"required", "forbidden"}


def test_warehouse_review_checklist_covers_required_special_rules():
    checklist = get_warehouse_checklist()
    by_node = {checkpoint.node_id: checkpoint for checkpoint in checklist}

    expected_nodes = {
        "warehouse_contract_nature",
        "warehouse_business_qualification",
        "warehouse_consensual_contract",
        "warehouse_goods_description",
        "warehouse_packaging_mark",
        "acceptance_check_standard",
        "acceptance_notice_nonconform",
        "after_acceptance_liability",
        "warehouse_receipt_issue",
        "warehouse_receipt_content",
        "warehouse_receipt_transfer_pledge",
        "receipt_holder_identity",
        "storage_period_agreed",
        "unclear_storage_period_rule",
        "early_retrieval_no_fee_reduction",
        "storage_fee_amount",
        "keeper_proper_custody",
        "inspection_sampling_right",
        "deterioration_notice_obligation",
        "emergency_disposal_right",
        "dangerous_goods_disclosure",
        "keeper_refuse_or_measures",
        "damage_liability_in_storage",
        "keeper_exemption_reasons",
        "warehouse_lien_right",
        "deposit_goods_rule",
    }

    assert expected_nodes <= set(by_node)
    assert "第904条" in by_node["warehouse_contract_nature"].legal_basis
    assert "第905条" in by_node["warehouse_consensual_contract"].legal_basis
    assert "第906条" in by_node["dangerous_goods_disclosure"].legal_basis
    assert "第907条" in by_node["acceptance_check_standard"].legal_basis
    assert "第908条" in by_node["warehouse_receipt_content"].legal_basis
    assert "第910条" in by_node["warehouse_receipt_transfer_pledge"].legal_basis
    assert "第911条" in by_node["inspection_sampling_right"].legal_basis
    assert "第912条" in by_node["deterioration_notice_obligation"].legal_basis
    assert "第913条" in by_node["emergency_disposal_right"].legal_basis
    assert "第914条" in by_node["unclear_storage_period_rule"].legal_basis
    assert "第915条" in by_node["early_retrieval_no_fee_reduction"].legal_basis
    assert "第916条" in by_node["deposit_goods_rule"].legal_basis
    assert "第917条" in by_node["keeper_exemption_reasons"].legal_basis
    assert "第903条" in by_node["warehouse_lien_right"].legal_basis


def test_warehouse_review_checklist_has_template_blank_criteria():
    checklist = get_warehouse_checklist()

    assert any("__" in checkpoint.suggested_clause for checkpoint in checklist)
    assert all(
        "空白" in checkpoint.partial_criteria
        or "未勾选" in checkpoint.partial_criteria
        or checkpoint.kind == "forbidden"
        for checkpoint in checklist
    )


def test_review_v2_can_load_warehouse_checklist():
    output = review_contract_v2(
        "保管人作为仓储公司为存货人储存货物，出具仓单和入库单，仓储费按月支付，存货人到期凭仓单提取仓储物。",
        "warehouse",
        use_llm=False,
    )

    assert output["success"] is True
    assert output["contract_type"] == "warehouse"
    assert output["contract_type_name"] == "仓储合同"
    assert output["all_items_count"] == 40
    assert len(output["items"]) == 40
    assert output["summary"]["高"] + output["summary"]["中"] + output["summary"]["低"] == 40
