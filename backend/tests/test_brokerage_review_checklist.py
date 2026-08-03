"""Structural tests for the brokerage-contract review checklist."""

from review_v2.brokerage_contract_checklist import get_brokerage_checklist
from review_v2.engine import review_contract_v2
from review_v2.house_lease_checklist import ReviewCheckpoint


def test_brokerage_review_checklist_has_44_points_and_11_modules():
    checklist = get_brokerage_checklist()
    module_ids = {checkpoint.item_id.rsplit("-", 1)[0] for checkpoint in checklist}

    assert len(checklist) == 44
    assert checklist[0].item_id == "BR-01-01"
    assert checklist[-1].item_id == "BR-11-04"
    assert module_ids == {f"BR-{index:02d}" for index in range(1, 12)}
    assert all(isinstance(checkpoint, ReviewCheckpoint) for checkpoint in checklist)


def test_brokerage_review_checklist_fields_are_complete():
    checklist = get_brokerage_checklist()

    for checkpoint in checklist:
        assert checkpoint.item_id.startswith("BR-")
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


def test_brokerage_review_checklist_has_risk_levels_and_forbidden_items():
    checklist = get_brokerage_checklist()
    risk_levels = {checkpoint.risk_level for checkpoint in checklist}
    kinds = {checkpoint.kind for checkpoint in checklist}

    assert risk_levels == {"高", "中", "低"}
    assert kinds == {"required", "forbidden"}


def test_brokerage_review_checklist_covers_required_special_rules():
    checklist = get_brokerage_checklist()
    by_node = {checkpoint.node_id: checkpoint for checkpoint in checklist}

    expected_nodes = {
        "brokerage_contract_nature",
        "broker_not_party_to_deal",
        "brokerage_not_agency_or_commission",
        "oral_brokerage_evidence",
        "report_brokerage_scope",
        "media_brokerage_scope",
        "service_record_attachment",
        "truthful_report_obligation",
        "important_fact_disclosure",
        "best_efforts_obligation",
        "principal_pay_remuneration",
        "principal_information_accuracy",
        "remuneration_condition_concluded_contract",
        "remuneration_amount_method",
        "media_service_both_parties_bear",
        "bypass_order_three_elements",
        "accepted_service_evidence",
        "used_opportunity_evidence",
        "bypass_remuneration_liability",
        "nonexclusive_other_broker_exception",
        "original_broker_not_causal",
        "policy_failure_no_remuneration",
        "necessary_expense_when_no_contract",
        "broker_activity_expense_burden",
        "truthful_report_breach_consequence",
        "staff_scope_act_liability",
        "principal_wrong_info_allocation",
        "exclusive_entrustment_clause",
        "exclusive_bypass_consequence",
        "unreasonable_standard_clause",
        "burden_of_proof_rule",
        "termination_reference_mandate",
        "post_contract_obligation",
    }

    assert expected_nodes <= set(by_node)
    assert "第961条" in by_node["brokerage_contract_nature"].legal_basis
    assert "第962条" in by_node["truthful_report_obligation"].legal_basis
    assert "第963条" in by_node["remuneration_condition_concluded_contract"].legal_basis
    assert "第964条" in by_node["necessary_expense_when_no_contract"].legal_basis
    assert "第965条" in by_node["bypass_order_three_elements"].legal_basis
    assert "第966条" in by_node["termination_reference_mandate"].legal_basis
    assert "第933条" in by_node["termination_reference_mandate"].legal_basis
    assert "第496条" in by_node["unreasonable_standard_clause"].legal_basis
    assert "第497条" in by_node["unreasonable_standard_clause"].legal_basis
    assert "第558条" in by_node["post_contract_obligation"].legal_basis


def test_brokerage_review_checklist_has_template_blank_criteria():
    checklist = get_brokerage_checklist()

    assert any("__" in checkpoint.suggested_clause for checkpoint in checklist)
    assert all(
        "空白" in checkpoint.partial_criteria
        or "未勾选" in checkpoint.partial_criteria
        or checkpoint.kind == "forbidden"
        for checkpoint in checklist
    )


def test_review_v2_can_load_brokerage_checklist():
    output = review_contract_v2(
        "中介人向委托人报告房源信息并提供媒介服务，促成买卖合同成立，双方约定中介费和跳单责任。",
        "brokerage",
        use_llm=False,
    )

    assert output["success"] is True
    assert output["contract_type"] == "brokerage"
    assert output["contract_type_name"] == "中介合同"
    assert output["all_items_count"] == 44
    assert len(output["items"]) == 44
    assert output["summary"]["高"] + output["summary"]["中"] + output["summary"]["低"] == 44
