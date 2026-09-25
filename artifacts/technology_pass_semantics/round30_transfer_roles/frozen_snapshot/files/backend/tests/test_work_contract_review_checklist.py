"""Structural tests for the work-contract review checklist."""

from review_v2.engine import COVERAGE_NOT_APPLICABLE, ISSUE_NOT_APPLICABLE, review_contract_v2
from review_v2.house_lease_checklist import ReviewCheckpoint
from review_v2.work_contract_checklist import get_work_contract_checklist


def test_work_contract_review_checklist_has_44_points_and_11_modules():
    checklist = get_work_contract_checklist()
    module_ids = {checkpoint.item_id.rsplit("-", 1)[0] for checkpoint in checklist}

    assert len(checklist) == 44
    assert checklist[0].item_id == "W-01-01"
    assert checklist[-1].item_id == "W-11-04"
    assert module_ids == {f"W-{index:02d}" for index in range(1, 12)}
    assert all(isinstance(checkpoint, ReviewCheckpoint) for checkpoint in checklist)


def test_work_contract_review_checklist_fields_are_complete():
    checklist = get_work_contract_checklist()

    for checkpoint in checklist:
        assert checkpoint.item_id.startswith("W-")
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


def test_work_contract_review_checklist_has_risk_levels_and_forbidden_items():
    checklist = get_work_contract_checklist()
    risk_levels = {checkpoint.risk_level for checkpoint in checklist}
    kinds = {checkpoint.kind for checkpoint in checklist}

    assert risk_levels == {"高", "中", "低"}
    assert kinds == {"required", "forbidden"}


def test_work_contract_review_checklist_covers_required_special_rules():
    checklist = get_work_contract_checklist()
    by_node = {checkpoint.node_id: checkpoint for checkpoint in checklist}

    expected_nodes = {
        "work_personal_completion_main_work",
        "work_main_subcontract_consent",
        "work_auxiliary_subcontract_liability",
        "work_customer_assistance_scope",
        "work_customer_material_inspection_notice",
        "work_material_result_custody",
        "work_quality_standard",
        "work_defect_repair",
        "work_defect_remake",
        "work_reduce_remuneration",
        "work_defect_compensation",
        "work_customer_arbitrary_termination_before_completion",
        "work_contractor_lien_condition",
    }

    assert expected_nodes <= set(by_node)
    assert "第772条" in by_node["work_personal_completion_main_work"].legal_basis
    assert "第773条" in by_node["work_auxiliary_subcontract_liability"].legal_basis
    assert "第778条" in by_node["work_customer_assistance_scope"].legal_basis
    assert "第775条" in by_node["work_customer_material_inspection_notice"].legal_basis
    assert "第784条" in by_node["work_material_result_custody"].legal_basis
    assert "第781条" in by_node["work_quality_standard"].legal_basis
    assert "第781条" in by_node["work_defect_repair"].legal_basis
    assert "第787条" in by_node["work_customer_arbitrary_termination_before_completion"].legal_basis
    assert "第783条" in by_node["work_contractor_lien_condition"].legal_basis


def test_work_contract_review_checklist_has_template_blank_criteria():
    checklist = get_work_contract_checklist()

    assert any("__" in checkpoint.suggested_clause for checkpoint in checklist)
    assert all(
        "空白" in checkpoint.partial_criteria
        or "未勾选" in checkpoint.partial_criteria
        or checkpoint.kind == "forbidden"
        for checkpoint in checklist
    )


def test_review_v2_can_load_work_contract_checklist():
    output = review_contract_v2(
        "定作人委托承揽人按照图纸加工设备零件，承揽人以自己的设备和技术完成主要工作，交付后按样品和技术规范验收。",
        "work_contract",
        use_llm=False,
    )

    assert output["success"] is True
    assert output["contract_type"] == "work_contract"
    assert output["contract_type_name"] == "承揽合同"
    assert output["all_items_count"] == 44
    assert len(output["items"]) == 44
    assert (
        output["summary"]["高"] + output["summary"]["中"] + output["summary"]["低"]
        == 44 - output["coverage_summary"].get(COVERAGE_NOT_APPLICABLE, 0)
    )


def test_work_special_scenario_points_are_not_applicable_when_absent():
    output = review_contract_v2(
        "定作人委托承揽人加工一批非标零件。承揽人以自己的设备、技术和劳力完成主要工作，质量标准和验收期限由双方另行确认。合同未涉及转包、分包或凭样品制作。",
        "work_contract",
        use_llm=False,
    )
    by_id = {item["item_id"]: item for item in output["items"]}

    for item_id in ("W-03-02", "W-03-03", "W-03-04", "W-11-02"):
        assert by_id[item_id]["coverage_status"] == COVERAGE_NOT_APPLICABLE
        assert by_id[item_id]["issue_type"] == ISSUE_NOT_APPLICABLE
        assert by_id[item_id]["risk_level"] == COVERAGE_NOT_APPLICABLE


def test_work_generic_notice_does_not_cover_assistance_urge_or_termination_notice():
    output = review_contract_v2(
        "承揽人应按照定作人要求完成定制展柜。双方联系地址用于一般通知。质量不合格的，承揽人应修理、重作或赔偿损失。",
        "work_contract",
        use_llm=False,
    )
    by_id = {item["item_id"]: item for item in output["items"]}

    assert by_id["W-04-03"]["coverage_status"] == "缺失"
    assert by_id["W-09-04"]["coverage_status"] == "缺失"
