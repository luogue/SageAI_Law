"""Structural tests for the loan-contract review checklist."""

from review_v2.engine import review_contract_v2
from review_v2.house_lease_checklist import ReviewCheckpoint
from review_v2.loan_contract_checklist import get_loan_checklist


def test_loan_review_checklist_has_48_points_and_12_modules():
    checklist = get_loan_checklist()
    module_ids = {checkpoint.item_id.rsplit("-", 1)[0] for checkpoint in checklist}

    assert len(checklist) == 48
    assert checklist[0].item_id == "L-01-01"
    assert checklist[-1].item_id == "L-12-04"
    assert module_ids == {f"L-{index:02d}" for index in range(1, 13)}
    assert all(isinstance(checkpoint, ReviewCheckpoint) for checkpoint in checklist)


def test_loan_review_checklist_fields_are_complete():
    checklist = get_loan_checklist()

    for checkpoint in checklist:
        assert checkpoint.item_id.startswith("L-")
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


def test_loan_review_checklist_has_risk_levels_and_forbidden_items():
    checklist = get_loan_checklist()
    risk_levels = {checkpoint.risk_level for checkpoint in checklist}
    kinds = {checkpoint.kind for checkpoint in checklist}

    assert risk_levels == {"高", "中", "低"}
    assert kinds == {"required", "forbidden"}


def test_loan_review_checklist_covers_required_special_rules():
    checklist = get_loan_checklist()
    by_node = {checkpoint.node_id: checkpoint for checkpoint in checklist}

    expected_nodes = {
        "loan_financial_private_distinction",
        "loan_relending_bank_loan_invalid",
        "loan_professional_lender_invalid",
        "loan_illegal_purpose_known_invalid",
        "loan_principal_amount",
        "loan_actual_disbursement_evidence",
        "loan_deducted_interest_forbidden",
        "loan_interest_lpr_cap",
        "loan_hidden_fee_over_cap",
        "loan_repayment_offset_order",
        "loan_early_repayment_right",
        "loan_extension_request",
        "loan_guarantee_type_joint_or_general",
        "loan_guarantee_period",
        "loan_old_for_new_guarantor_notice",
        "loan_spousal_joint_intent",
        "loan_collection_ack_limitation_interruption",
        "loan_notice_service_method",
    }

    assert expected_nodes <= set(by_node)
    assert "第667条" in by_node["loan_financial_private_distinction"].legal_basis
    assert "第670条" in by_node["loan_deducted_interest_forbidden"].legal_basis
    assert "第25条" in by_node["loan_interest_lpr_cap"].legal_basis
    assert "第29条" in by_node["loan_interest_lpr_cap"].legal_basis
    assert "第561条" in by_node["loan_repayment_offset_order"].legal_basis
    assert "第677条" in by_node["loan_early_repayment_right"].legal_basis
    assert "第678条" in by_node["loan_extension_request"].legal_basis
    assert "第686条" in by_node["loan_guarantee_type_joint_or_general"].legal_basis
    assert "第195条" in by_node["loan_collection_ack_limitation_interruption"].legal_basis


def test_loan_review_checklist_has_template_blank_criteria():
    checklist = get_loan_checklist()

    assert any("__" in checkpoint.suggested_clause for checkpoint in checklist)
    assert all(
        "空白" in checkpoint.partial_criteria
        or "未勾选" in checkpoint.partial_criteria
        or checkpoint.kind == "forbidden"
        for checkpoint in checklist
    )


def test_review_v2_can_load_loan_checklist():
    output = review_contract_v2(
        "借款人向出借人借款人民币100000元，年利率10%，借款期限一年，到期一次性还本付息。",
        "loan",
        use_llm=False,
    )

    assert output["success"] is True
    assert output["contract_type"] == "loan"
    assert output["contract_type_name"] == "借款合同"
    assert output["all_items_count"] == 48
    assert len(output["items"]) == 48
    assert sum(output["summary"].values()) + output["coverage_summary"].get("不适用", 0) == 48
