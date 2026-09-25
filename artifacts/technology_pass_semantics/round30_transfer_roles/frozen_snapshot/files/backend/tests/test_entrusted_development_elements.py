"""Independent fact states for entrusted patent rights and no-fault failure."""
from review_v2.clause_parser import parse_contract_clauses
from review_v2.entrusted_development_elements import (
    entrusted_patent_application_elements, development_failure_elements,
    entrusted_development_element_family,
)


def patent(text):
    return {row["element_id"]: row for row in entrusted_patent_application_elements(parse_contract_clauses(text))}


def failure(text):
    return {row["element_id"]: row for row in development_failure_elements(parse_contract_clauses(text))}


def test_express_application_entitlement_and_authorship_are_not_absence():
    rows = patent("第一条 成果权利\n甲方享有申请专利的权利。乙方应配合甲方办理专利申请及相关手续。专利授权后，专利权归甲方所有。实际完成研究开发的人员依法享有发明人署名权。")
    for key in ("patent_application_right_ownership", "patent_right_after_grant", "inventor_authorship"):
        assert rows[key]["status"] == "COVERED", rows[key]
        assert rows[key]["supporting_evidence"]
    for key in ("document_signature_cooperation", "registration_cooperation"):
        assert rows[key]["status"] == "PARTIALLY_COVERED", rows[key]
    for key in ("application_filing_control", "filing_cost_allocation", "inventor_confirmation"):
        assert rows[key]["status"] == "MISSING"
        assert not rows[key]["supporting_evidence"]


def test_application_ownership_cannot_prove_post_grant_ownership():
    rows = patent("第一条 专利申请\n受托方拥有专利申请权。")
    assert rows["patent_application_right_ownership"]["status"] == "COVERED"
    assert rows["patent_right_after_grant"]["status"] == "MISSING"
    assert rows["document_signature_cooperation"]["status"] == "MISSING"


def test_joint_ownership_only_covers_ownership_not_application_procedure():
    rows = patent("第十条 知识产权\n专利申请权及相关知识产权归甲乙双方共同所有。")
    assert rows["patent_application_right_ownership"]["status"] == "COVERED"
    for key, row in rows.items():
        if key != "patent_application_right_ownership":
            assert row["status"] == "MISSING", row
            assert row["supporting_evidence"] == []
            assert row["bound_evidence_ids"] == []
    resolved = entrusted_development_element_family("application_filing_control", parse_contract_clauses(
        "第十条 知识产权\n专利申请权及相关知识产权归甲乙双方共同所有。"))
    assert resolved["status"] == "MISSING"


def test_real_deferred_application_decision_has_partial_positive_support():
    rows = patent("第一条 专利申请\n是否申请专利的决定由双方另行协商。")
    assert rows["application_filing_control"]["status"] == "PARTIALLY_COVERED"
    assert rows["application_filing_control"]["supporting_evidence"]
    assert rows["patent_application_right_ownership"]["status"] == "MISSING"


def test_names_or_signature_right_do_not_prove_inventor_confirmation():
    rows = patent("第一条 完成人\n发明人张某和李某享有发明人署名权。")
    assert rows["inventor_authorship"]["status"] == "COVERED"
    assert rows["inventor_confirmation"]["status"] == "MISSING"


def test_specific_procedures_do_not_need_broad_composite_wording():
    rows = patent("第一条 专利申请\n是否申请专利由委托方决定。受托方应签署专利申请文件及请求书。受托方应提供专利申请、登记及权利取得所需全部材料。专利申请费用由委托方承担。发明人名单由双方按照实际创造贡献共同书面确认。")
    for key in ("application_filing_control", "document_signature_cooperation", "registration_cooperation", "filing_cost_allocation", "inventor_confirmation"):
        assert rows[key]["status"] == "COVERED", rows[key]
    assert rows["patent_application_right_ownership"]["status"] == "MISSING"


def test_explicit_no_agreement_and_unrelated_paperwork_do_not_cover_patent():
    rows = patent("第一条 付款\n乙方配合甲方签署付款文件并提供发票。\n第二条 专利申请\n专利申请费用承担尚未明确。未约定专利申请文件签署配合。")
    assert all(row["status"] == "MISSING" for row in rows.values()), rows


def test_risk_loss_split_does_not_imply_development_fee_settlement():
    rows = failure("第一条 研发失败及技术风险\n因现有技术水平和条件下难以克服的技术困难导致研发失败且双方均无过错的，由双方各承担50%的直接损失。")
    for key in ("no_fault_technical_risk_trigger", "no_fault_technical_risk_allocation"):
        assert rows[key]["status"] == "COVERED"
        assert "50%" in rows[key]["supporting_evidence"][0]["quote"]
    assert all(row["status"] == "MISSING" for key, row in rows.items() if key not in {"no_fault_technical_risk_trigger", "no_fault_technical_risk_allocation"})


def test_normal_delivery_and_payment_do_not_cover_failure_disposition():
    rows = failure("第一条 研发失败\n双方各分担无过错技术风险的损失。\n第二条 正常交付\n项目完成时乙方交付源代码、技术资料和阶段成果。甲方在验收合格后支付研发费用。")
    for key in ("paid_fee_refund", "unpaid_fee_obligation", "failed_project_stage_result_disposition", "failed_project_source_code_disposition", "failed_project_material_disposition"):
        assert rows[key]["status"] == "MISSING", rows[key]


def test_each_failure_financial_and_output_requirement_has_exact_source():
    rows = failure("第一条 研发失败\n研发失败时，已发生研发费用按实际完成工作结算。已支付款项扣除已完成部分后退还。未付款项不再支付。乙方应移交阶段成果。源代码由甲方继续使用。技术资料处置方式另行协商。")
    for key in ("failed_development_incurred_cost_settlement", "paid_fee_refund", "unpaid_fee_obligation", "failed_project_stage_result_disposition", "failed_project_source_code_disposition"):
        assert rows[key]["status"] == "COVERED", rows[key]
    assert rows["failed_project_material_disposition"]["status"] == "PARTIALLY_COVERED"
    assert "阶段成果" in rows["failed_project_stage_result_disposition"]["supporting_evidence"][0]["quote"]
    assert "源代码" not in rows["failed_project_stage_result_disposition"]["supporting_evidence"][0]["quote"]


def test_no_refund_is_existing_allocation_not_missing_or_assumed_refund():
    rows = failure("第一条 研发失败\n发生无过错技术风险导致研发失败时，已付款不予退还，剩余开发费继续支付。")
    assert rows["paid_fee_refund"]["status"] == "COVERED"
    assert "不予退还" in rows["paid_fee_refund"]["proposition"]
    assert rows["unpaid_fee_obligation"]["status"] == "COVERED"


def test_developer_fault_does_not_prove_no_fault_risk_loss_allocation():
    rows = failure("第一条 研发失败\n因乙方违约导致研发失败时，乙方承担全部损失并退还已支付研发费用。")
    assert rows["no_fault_technical_risk_trigger"]["status"] == "MISSING"
    assert rows["no_fault_technical_risk_allocation"]["status"] == "MISSING"


def test_partial_searches_objective_remaining_content_with_same_extractor():
    clauses = parse_contract_clauses("第一条 专利申请\n甲方享有申请专利的权利。乙方配合甲方办理专利申请。")
    covered = entrusted_development_element_family("PATENT_APPLICATION_RIGHT_OWNERSHIP", clauses)
    assert covered["status"] == "COVERED"
    partial = entrusted_development_element_family("document_signature_cooperation", clauses)
    assert partial["status"] == "PARTIALLY_COVERED"
    assert partial["search_targets"] == [partial["residual_gap"]]
    assert "签署" in partial["residual_gap"]
    assert all(term not in partial["residual_gap"] for term in ("已有", "不完整", "未明确"))
    assert entrusted_development_element_family("unknown_requirement", clauses) is None


def test_unrelated_prohibition_does_not_negate_positive_application_right():
    rows = patent("第一条 专利申请\n甲方享有申请专利的权利，乙方不得以自己名义申请专利。")
    assert rows["patent_application_right_ownership"]["status"] == "COVERED"
    assert rows["application_filing_control"]["status"] == "COVERED"


def test_negated_entitlement_or_cooperation_is_not_positive_support():
    rows = patent("第一条 专利申请\n乙方不享有申请专利的权利。乙方无需配合甲方办理专利申请。乙方无需签署专利申请文件。")
    for key in ("patent_application_right_ownership", "application_filing_control", "document_signature_cooperation", "registration_cooperation"):
        assert rows[key]["status"] != "COVERED", rows[key]
        assert not rows[key]["supporting_evidence"], rows[key]
