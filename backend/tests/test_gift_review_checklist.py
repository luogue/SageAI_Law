"""Structural tests for the gift-contract review checklist."""

from review_v2.engine import review_contract_v2
from review_v2.gift_contract_checklist import get_gift_checklist
from review_v2.house_lease_checklist import ReviewCheckpoint


def test_gift_review_checklist_has_48_points_and_12_modules():
    checklist = get_gift_checklist()
    module_ids = {checkpoint.item_id.rsplit("-", 1)[0] for checkpoint in checklist}

    assert len(checklist) == 48
    assert checklist[0].item_id == "G-01-01"
    assert checklist[-1].item_id == "G-12-04"
    assert module_ids == {f"G-{index:02d}" for index in range(1, 13)}
    assert all(isinstance(checkpoint, ReviewCheckpoint) for checkpoint in checklist)


def test_gift_review_checklist_fields_are_complete():
    checklist = get_gift_checklist()

    for checkpoint in checklist:
        assert checkpoint.item_id.startswith("G-")
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


def test_gift_review_checklist_has_risk_levels_and_forbidden_items():
    checklist = get_gift_checklist()
    risk_levels = {checkpoint.risk_level for checkpoint in checklist}
    kinds = {checkpoint.kind for checkpoint in checklist}

    assert risk_levels == {"高", "中", "低"}
    assert kinds == {"required", "forbidden"}


def test_gift_review_checklist_covers_required_special_rules():
    checklist = get_gift_checklist()
    by_node = {checkpoint.node_id: checkpoint for checkpoint in checklist}

    expected_nodes = {
        "gift_gratuitous_intent",
        "gift_arbitrary_revocation_before_transfer",
        "gift_irrevocable_exceptions",
        "gift_statutory_revocation_one_year",
        "gift_heir_revocation_six_months",
        "gift_poverty_defense_condition",
        "gift_compulsory_delivery_notarized",
        "gift_donor_fault_damage",
        "gift_obligation_attached_defect_warranty",
        "gift_return_after_revocation",
    }

    assert expected_nodes <= set(by_node)
    assert "第657条" in by_node["gift_gratuitous_intent"].legal_basis
    assert "第658条" in by_node["gift_arbitrary_revocation_before_transfer"].legal_basis
    assert "第663条" in by_node["gift_statutory_revocation_one_year"].legal_basis
    assert "第664条" in by_node["gift_heir_revocation_six_months"].legal_basis
    assert "第666条" in by_node["gift_poverty_defense_condition"].legal_basis
    assert "第660条" in by_node["gift_compulsory_delivery_notarized"].legal_basis
    assert "第662条" in by_node["gift_obligation_attached_defect_warranty"].legal_basis
    assert "第665条" in by_node["gift_return_after_revocation"].legal_basis


def test_gift_review_checklist_has_template_blank_criteria():
    checklist = get_gift_checklist()

    assert any("__" in checkpoint.suggested_clause for checkpoint in checklist)
    assert all(
        "空白" in checkpoint.partial_criteria
        or "未勾选" in checkpoint.partial_criteria
        or checkpoint.kind == "forbidden"
        for checkpoint in checklist
    )


def test_review_v2_can_load_gift_contract_checklist():
    output = review_contract_v2(
        "赠与人自愿将名下车辆一辆无偿赠与受赠人，受赠人表示接受赠与。双方约定办理过户登记。",
        "gift",
        use_llm=False,
    )

    assert output["success"] is True
    assert output["contract_type"] == "gift"
    assert output["contract_type_name"] == "赠与合同"
    assert output["all_items_count"] == 48
    assert len(output["items"]) == 48
    assert output["summary"]["高"] + output["summary"]["中"] + output["summary"]["低"] == 48
