"""Structural tests for the agency-contract review checklist."""

from review_v2.agency_contract_checklist import get_agency_checklist
from review_v2.engine import COVERAGE_NOT_APPLICABLE, ISSUE_NOT_APPLICABLE, review_contract_v2
from review_v2.house_lease_checklist import ReviewCheckpoint


def test_agency_review_checklist_has_42_points_and_14_modules():
    checklist = get_agency_checklist()
    module_ids = {checkpoint.item_id.rsplit("-", 1)[0] for checkpoint in checklist}

    assert len(checklist) == 42
    assert checklist[0].item_id == "A-01-01"
    assert checklist[-1].item_id == "A-14-03"
    assert module_ids == {f"A-{index:02d}" for index in range(1, 15)}
    assert all(isinstance(checkpoint, ReviewCheckpoint) for checkpoint in checklist)


def test_agency_review_checklist_fields_are_complete():
    checklist = get_agency_checklist()

    for checkpoint in checklist:
        assert checkpoint.item_id.startswith("A-")
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


def test_agency_review_checklist_has_risk_levels_and_forbidden_items():
    checklist = get_agency_checklist()
    risk_levels = {checkpoint.risk_level for checkpoint in checklist}
    kinds = {checkpoint.kind for checkpoint in checklist}

    assert risk_levels == {"高", "中", "低"}
    assert kinds == {"required", "forbidden"}


def test_agency_review_checklist_covers_required_special_rules():
    checklist = get_agency_checklist()
    by_node = {checkpoint.node_id: checkpoint for checkpoint in checklist}

    expected_nodes = {
        "agency_contract_type_identification",
        "agency_special_or_general_mandate",
        "agency_paid_or_unpaid",
        "agency_obey_instruction",
        "agency_report_obligation",
        "agency_property_transfer",
        "agency_paid_fault_standard",
        "agency_unpaid_intent_gross_standard",
        "agency_over_authority_liability",
        "agency_sub_entrustment_consent",
        "agency_sub_entrustment_liability",
        "agency_self_agency_consent",
        "agency_both_side_agency_consent",
        "agency_undisclosed_principal_intervention",
        "agency_third_party_choice_right",
        "agency_arbitrary_termination",
        "agency_termination_compensation_scope",
    }

    assert expected_nodes <= set(by_node)
    assert "第919条" in by_node["agency_contract_type_identification"].legal_basis
    assert "第920条" in by_node["agency_special_or_general_mandate"].legal_basis
    assert "第923条" in by_node["agency_sub_entrustment_liability"].legal_basis
    assert "第168条" in by_node["agency_self_agency_consent"].legal_basis
    assert "第926条" in by_node["agency_undisclosed_principal_intervention"].legal_basis
    assert "第926条" in by_node["agency_third_party_choice_right"].legal_basis
    assert "第929条" in by_node["agency_paid_fault_standard"].legal_basis
    assert "第933条" in by_node["agency_termination_compensation_scope"].legal_basis


def test_agency_review_checklist_has_template_blank_criteria():
    checklist = get_agency_checklist()

    assert any("__" in checkpoint.suggested_clause for checkpoint in checklist)
    assert all(
        "空白" in checkpoint.partial_criteria
        or "未勾选" in checkpoint.partial_criteria
        or checkpoint.kind == "forbidden"
        for checkpoint in checklist
    )


def test_review_v2_can_load_agency_checklist():
    output = review_contract_v2(
        "委托人委托受托人代办公司登记事务，受托人应按委托人指示处理事务并定期报告进展，取得的文件和财产应转交委托人。",
        "agency",
        use_llm=False,
    )

    assert output["success"] is True
    assert output["contract_type"] == "agency"
    assert output["contract_type_name"] == "委托合同"
    assert output["all_items_count"] == 42
    assert len(output["items"]) == 42
    assert (
        output["summary"]["高"] + output["summary"]["中"] + output["summary"]["低"]
        == 42 - output["coverage_summary"].get(COVERAGE_NOT_APPLICABLE, 0)
    )


def test_agency_special_scenario_points_are_not_applicable_when_absent():
    output = review_contract_v2(
        "委托人委托受托人代办公司登记事项。受托人应按委托人指示处理事务、定期报告进展并移交取得的文件和财产。本合同不涉及转委托、隐名委托、自己代理或双方代理。",
        "agency",
        use_llm=False,
    )
    by_id = {item["item_id"]: item for item in output["items"]}

    for item_id in (
        "A-08-01",
        "A-08-02",
        "A-08-03",
        "A-09-01",
        "A-09-02",
        "A-09-03",
        "A-10-01",
        "A-10-02",
        "A-10-03",
        "A-11-01",
        "A-11-02",
        "A-11-03",
    ):
        assert by_id[item_id]["coverage_status"] == COVERAGE_NOT_APPLICABLE
        assert by_id[item_id]["issue_type"] == ISSUE_NOT_APPLICABLE
        assert by_id[item_id]["risk_level"] == COVERAGE_NOT_APPLICABLE


def test_agency_generic_notice_does_not_cover_arbitrary_termination():
    output = review_contract_v2(
        "委托人委托受托人代办工商登记。双方确认联系地址用于一般通知。受托人应按指示处理事务并报告结果。",
        "agency",
        use_llm=False,
    )
    by_id = {item["item_id"]: item for item in output["items"]}

    assert by_id["A-12-01"]["coverage_status"] == "缺失"
