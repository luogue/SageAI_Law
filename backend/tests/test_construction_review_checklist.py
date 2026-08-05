"""Structural tests for the construction-contract review checklist."""

from pathlib import Path

from docx import Document

from review_v2.construction_contract_checklist import get_construction_checklist
from review_v2.engine import COVERAGE_NOT_APPLICABLE, review_contract_v2
from review_v2.house_lease_checklist import ReviewCheckpoint


def test_construction_review_checklist_has_52_points_and_13_modules():
    checklist = get_construction_checklist()
    module_ids = {checkpoint.item_id.rsplit("-", 1)[0] for checkpoint in checklist}

    assert len(checklist) == 52
    assert checklist[0].item_id == "CE-01-01"
    assert checklist[-1].item_id == "CE-13-04"
    assert module_ids == {f"CE-{index:02d}" for index in range(1, 14)}
    assert all(isinstance(checkpoint, ReviewCheckpoint) for checkpoint in checklist)


def test_construction_review_checklist_fields_are_complete():
    checklist = get_construction_checklist()

    for checkpoint in checklist:
        assert checkpoint.item_id.startswith("CE-")
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
        assert checkpoint.applicable_if


def test_construction_review_checklist_has_risk_levels_and_forbidden_items():
    checklist = get_construction_checklist()
    risk_levels = {checkpoint.risk_level for checkpoint in checklist}
    kinds = {checkpoint.kind for checkpoint in checklist}

    assert risk_levels == {"高", "中", "低"}
    assert kinds == {"required", "forbidden"}


def test_construction_review_checklist_covers_required_special_rules():
    checklist = get_construction_checklist()
    by_node = {checkpoint.node_id: checkpoint for checkpoint in checklist}

    expected_nodes = {
        "construction_contract_nature",
        "construction_survey_design_work_type",
        "contractor_qualification_match",
        "qualification_before_completion",
        "affiliation_qualification_lending",
        "mandatory_tender_review",
        "valid_bid_award_document",
        "tender_illegal_invalid",
        "planning_permit_obtained",
        "planning_obtained_before_suit",
        "prohibit_total_subcontract",
        "subcontract_to_qualified_party",
        "no_re_subcontract",
        "labor_subcontract_qualification",
        "black_white_contract_check",
        "substantive_terms_consistency",
        "start_date_identification",
        "completion_date_identification",
        "period_extension_conditions",
        "quality_standard_acceptance",
        "hidden_work_inspection",
        "quality_deposit_return_period",
        "project_price_pricing_method",
        "settlement_procedure",
        "project_price_interest",
        "invalid_contract_price_compensation",
        "priority_payment_right",
        "priority_claim_18_months",
        "priority_no_waiver_worker_interest",
        "actual_constructor_identification",
        "direct_sue_employer_limit",
        "subrogation_claim",
        "employer_material_fund_site_obligation",
        "stoppage_loss_claim",
        "employer_assistance_breach_termination",
        "contract_termination_settlement",
    }

    assert expected_nodes <= set(by_node)
    assert "第788条" in by_node["construction_contract_nature"].legal_basis
    assert "第794条" in by_node["construction_survey_design_work_type"].legal_basis
    assert "第1条" in by_node["contractor_qualification_match"].legal_basis
    assert "第7条" in by_node["affiliation_qualification_lending"].legal_basis
    assert "第2条" in by_node["black_white_contract_check"].legal_basis
    assert "第3条" in by_node["planning_permit_obtained"].legal_basis
    assert "第791条" in by_node["prohibit_total_subcontract"].legal_basis
    assert "第8条" in by_node["start_date_identification"].legal_basis
    assert "第9条" in by_node["completion_date_identification"].legal_basis
    assert "第798条" in by_node["hidden_work_inspection"].legal_basis
    assert "第17条" in by_node["quality_deposit_return_period"].legal_basis
    assert "第793条" in by_node["invalid_contract_price_compensation"].legal_basis
    assert "第807条" in by_node["priority_payment_right"].legal_basis
    assert "第41条" in by_node["priority_claim_18_months"].legal_basis
    assert "第43条" in by_node["direct_sue_employer_limit"].legal_basis
    assert "第803条" in by_node["employer_material_fund_site_obligation"].legal_basis
    assert "第804条" in by_node["stoppage_loss_claim"].legal_basis
    assert "第806条" in by_node["contract_termination_settlement"].legal_basis


def test_construction_review_checklist_has_template_blank_criteria():
    checklist = get_construction_checklist()

    assert any("__" in checkpoint.suggested_clause for checkpoint in checklist)
    assert all(
        "空白" in checkpoint.partial_criteria
        or "未勾选" in checkpoint.partial_criteria
        or checkpoint.kind == "forbidden"
        for checkpoint in checklist
    )


def test_review_v2_can_load_construction_checklist():
    output = review_contract_v2(
        "发包人与承包人签订建设工程施工合同，承包人具备施工资质，工程价款按工程量清单结算，竣工验收合格后支付。",
        "construction",
        use_llm=False,
    )

    assert output["success"] is True
    assert output["contract_type"] == "construction"
    assert output["contract_type_name"] == "建设工程合同"
    assert output["all_items_count"] == 52
    assert len(output["items"]) == 52
    assert (
        output["summary"]["高"]
        + output["summary"]["中"]
        + output["summary"]["低"]
        + output["coverage_summary"].get(COVERAGE_NOT_APPLICABLE, 0)
        == 52
    )


def test_construction_fixture_corrections_for_subcontract_and_tender_points():
    fixtures_dir = Path(__file__).resolve().parents[2] / "test_data"
    fixture = next(path for path in fixtures_dir.glob("*.docx") if path.name.startswith("测试合同8"))
    document = Document(fixture)
    contract_text = "\n".join(paragraph.text for paragraph in document.paragraphs if paragraph.text.strip())

    output = review_contract_v2(contract_text, "construction", use_llm=False)
    by_id = {item["item_id"]: item for item in output["items"]}

    assert by_id["CE-05-01"]["risk_level"] == "低"
    assert by_id["CE-05-01"]["coverage_status"] == "通过"
    assert by_id["CE-05-03"]["risk_level"] == "低"
    assert by_id["CE-05-03"]["coverage_status"] == "通过"

    assert by_id["CE-01-01"]["risk_level"] == "中"
    assert by_id["CE-01-01"]["coverage_status"] == "部分覆盖"
    assert by_id["CE-01-01"]["issue_type"] == "模板空白"

    assert by_id["CE-03-02"]["coverage_status"] == COVERAGE_NOT_APPLICABLE

    assert by_id["CE-03-04"]["risk_level"] == "中"
    assert by_id["CE-03-04"]["coverage_status"] == "部分覆盖"
    assert by_id["CE-03-04"]["issue_type"] == "模板空白"
