"""Structural tests for the commission-agency-contract review checklist."""

from review_v2.commission_agency_contract_checklist import get_commission_agency_checklist
from review_v2.engine import review_contract_v2
from review_v2.house_lease_checklist import ReviewCheckpoint


def test_commission_agency_review_checklist_has_44_points_and_11_modules():
    checklist = get_commission_agency_checklist()
    module_ids = {checkpoint.item_id.rsplit("-", 1)[0] for checkpoint in checklist}

    assert len(checklist) == 44
    assert checklist[0].item_id == "CA-01-01"
    assert checklist[-1].item_id == "CA-11-04"
    assert module_ids == {f"CA-{index:02d}" for index in range(1, 12)}
    assert all(isinstance(checkpoint, ReviewCheckpoint) for checkpoint in checklist)


def test_commission_agency_review_checklist_fields_are_complete():
    checklist = get_commission_agency_checklist()

    for checkpoint in checklist:
        assert checkpoint.item_id.startswith("CA-")
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


def test_commission_agency_review_checklist_has_risk_levels_and_forbidden_items():
    checklist = get_commission_agency_checklist()
    risk_levels = {checkpoint.risk_level for checkpoint in checklist}
    kinds = {checkpoint.kind for checkpoint in checklist}

    assert risk_levels == {"高", "中", "低"}
    assert kinds == {"required", "forbidden"}


def test_commission_agency_review_checklist_covers_required_special_rules():
    checklist = get_commission_agency_checklist()
    by_node = {checkpoint.node_id: checkpoint for checkpoint in checklist}

    expected_nodes = {
        "commission_agency_contract_nature",
        "own_name_trade",
        "not_agency_or_brokerage",
        "oral_contract_evidence",
        "commission_agent_identity_separation",
        "commission_affair_scope",
        "commission_goods_description",
        "commission_agent_custody_duty",
        "commission_agent_follow_instruction",
        "commission_agent_expense_burden",
        "commission_agent_deliver_result",
        "principal_pay_remuneration",
        "principal_receive_or_retrieve_goods",
        "price_instruction_rule",
        "price_difference_compensation",
        "positive_price_difference_ownership",
        "intervention_right_condition",
        "intervention_remuneration",
        "third_party_default_liability",
        "exclude_commission_agent_third_party_default",
        "malicious_collusion_with_third_party",
        "commission_lien_right",
        "lien_exclusion_or_scope",
        "commission_deposit_right",
        "defective_goods_disposal",
        "perishable_goods_emergency_disposal",
        "termination_right_reference_mandate",
        "termination_loss_scope",
        "sub_entrustment_rule",
    }

    assert expected_nodes <= set(by_node)
    assert "第951条" in by_node["commission_agency_contract_nature"].legal_basis
    assert "第958条" in by_node["own_name_trade"].legal_basis
    assert "第953条" in by_node["commission_agent_custody_duty"].legal_basis
    assert "第952条" in by_node["commission_agent_expense_burden"].legal_basis
    assert "第959条" in by_node["principal_pay_remuneration"].legal_basis
    assert "第955条" in by_node["price_instruction_rule"].legal_basis
    assert "第956条" in by_node["intervention_right_condition"].legal_basis
    assert "第958条" in by_node["third_party_default_liability"].legal_basis
    assert "第957条" in by_node["commission_deposit_right"].legal_basis
    assert "第954条" in by_node["defective_goods_disposal"].legal_basis
    assert "第933条" in by_node["termination_right_reference_mandate"].legal_basis
    assert "第923条" in by_node["sub_entrustment_rule"].legal_basis


def test_commission_agency_review_checklist_has_template_blank_criteria():
    checklist = get_commission_agency_checklist()

    assert any("__" in checkpoint.suggested_clause for checkpoint in checklist)
    assert all(
        "空白" in checkpoint.partial_criteria
        or "未勾选" in checkpoint.partial_criteria
        or checkpoint.kind == "forbidden"
        for checkpoint in checklist
    )


def test_review_v2_can_load_commission_agency_checklist():
    output = review_contract_v2(
        "委托人委托行纪人以自己名义代销商品，行纪人按指定价格与第三人交易，完成交易后交付价款并收取佣金。",
        "commission_agency",
        use_llm=False,
    )

    assert output["success"] is True
    assert output["contract_type"] == "commission_agency"
    assert output["contract_type_name"] == "行纪合同"
    assert output["all_items_count"] == 44
    assert len(output["items"]) == 44
    assert output["summary"]["高"] + output["summary"]["中"] + output["summary"]["低"] == 44
