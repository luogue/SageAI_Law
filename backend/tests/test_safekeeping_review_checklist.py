"""Structural tests for the safekeeping-contract review checklist."""

from review_v2.engine import review_contract_v2
from review_v2.house_lease_checklist import ReviewCheckpoint
from review_v2.safekeeping_contract_checklist import get_safekeeping_checklist


def test_safekeeping_review_checklist_has_48_points_and_12_modules():
    checklist = get_safekeeping_checklist()
    module_ids = {checkpoint.item_id.rsplit("-", 1)[0] for checkpoint in checklist}

    assert len(checklist) == 48
    assert checklist[0].item_id == "D-01-01"
    assert checklist[-1].item_id == "D-12-04"
    assert module_ids == {f"D-{index:02d}" for index in range(1, 13)}
    assert all(isinstance(checkpoint, ReviewCheckpoint) for checkpoint in checklist)


def test_safekeeping_review_checklist_fields_are_complete():
    checklist = get_safekeeping_checklist()

    for checkpoint in checklist:
        assert checkpoint.item_id.startswith("D-")
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


def test_safekeeping_review_checklist_has_risk_levels_and_forbidden_items():
    checklist = get_safekeeping_checklist()
    risk_levels = {checkpoint.risk_level for checkpoint in checklist}
    kinds = {checkpoint.kind for checkpoint in checklist}

    assert risk_levels == {"高", "中", "低"}
    assert kinds == {"required", "forbidden"}


def test_safekeeping_review_checklist_covers_required_special_rules():
    checklist = get_safekeeping_checklist()
    by_node = {checkpoint.node_id: checkpoint for checkpoint in checklist}

    expected_nodes = {
        "safekeeping_delivery_establishment",
        "safekeeping_fee_paid_or_unpaid",
        "safekeeping_paid_general_negligence",
        "safekeeping_unpaid_intent_gross",
        "safekeeping_depositor_disclosure",
        "safekeeping_valuable_declaration",
        "safekeeping_undeclared_valuable_consequence",
        "safekeeping_consumptive_type",
        "safekeeping_lien_condition",
        "safekeeping_depositor_anytime_retrieval",
    }

    assert expected_nodes <= set(by_node)
    assert "第890条" in by_node["safekeeping_delivery_establishment"].legal_basis
    assert "第889条" in by_node["safekeeping_fee_paid_or_unpaid"].legal_basis
    assert "第897条" in by_node["safekeeping_paid_general_negligence"].legal_basis
    assert "第897条" in by_node["safekeeping_unpaid_intent_gross"].legal_basis
    assert "第893条" in by_node["safekeeping_depositor_disclosure"].legal_basis
    assert "第898条" in by_node["safekeeping_valuable_declaration"].legal_basis
    assert "第901条" in by_node["safekeeping_consumptive_type"].legal_basis
    assert "第903条" in by_node["safekeeping_lien_condition"].legal_basis
    assert "第899条" in by_node["safekeeping_depositor_anytime_retrieval"].legal_basis


def test_safekeeping_review_checklist_has_template_blank_criteria():
    checklist = get_safekeeping_checklist()

    assert any("__" in checkpoint.suggested_clause for checkpoint in checklist)
    assert all(
        "空白" in checkpoint.partial_criteria
        or "未勾选" in checkpoint.partial_criteria
        or checkpoint.kind == "forbidden"
        for checkpoint in checklist
    )


def test_review_v2_can_load_safekeeping_contract_checklist():
    output = review_contract_v2(
        "寄存人将名表一块交给保管人保管，保管人出具寄存单，双方约定保管费每月100元，寄存人可随时领取。",
        "deposit",
        use_llm=False,
    )

    assert output["success"] is True
    assert output["contract_type"] == "deposit"
    assert output["contract_type_name"] == "保管合同"
    assert output["all_items_count"] == 48
    assert len(output["items"]) == 48
    assert output["summary"]["高"] + output["summary"]["中"] + output["summary"]["低"] == 48
