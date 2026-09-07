from pathlib import Path

import pytest

from layers.input_layer import InputLayer
from review_v2.clause_parser import parse_contract_clauses
from review_v2.engine import review_contract_v2
from review_v2.user_profile import UserRiskProfile


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "test_data" / "37 专利技术许可合同.docx"


def _review(text: str) -> dict:
    return review_contract_v2(
        text,
        "technology",
        include_low_risk=True,
        use_llm=False,
        profile=UserRiskProfile(user_identity="甲方/被许可方"),
    )


@pytest.fixture(scope="module")
def contract_text() -> str:
    return InputLayer()._extract_from_docx_content(FIXTURE.read_bytes())


@pytest.fixture(scope="module")
def review(contract_text: str) -> dict:
    return _review(contract_text)


def test_annex_subheadings_keep_appendix_lineage(contract_text: str):
    clauses = parse_contract_clauses(contract_text)
    by_id = {clause.clause_id: clause for clause in clauses}

    assert by_id["C0057"].source_type == "APPENDIX"
    assert by_id["C0058"].source_type == "APPENDIX"
    assert by_id["C0060"].source_type == "APPENDIX"


def test_patent_identity_and_support_reuse_direct_source_facts(review: dict):
    by_id = {row["item_id"]: row for row in review["items"]}
    subject = by_id["TC-01-03"]
    support = by_id["TC-07-04"]

    assert subject["coverage_status"] == "通过"
    assert {row["clause_id"] for row in subject["evidence_clauses"]} == {"C0003", "C0057"}
    assert subject["coverage_elements"][0]["status"] == "COVERED"

    assert support["coverage_status"] == "部分覆盖"
    support_elements = {row["element_id"]: row for row in support["coverage_elements"]}
    assert support_elements["on_demand_technical_service"]["status"] == "COVERED"
    assert support_elements["patent_fee_and_validity_maintenance"]["status"] == "COVERED"
    assert support_elements["patent_status_change_notice"]["status"] == "COVERED"
    assert support_elements["technical_service_execution_details"]["status"] == "MISSING"
    assert {row["clause_id"] for row in support["evidence_clauses"]} == {"C0015", "C0035", "C0036"}
    assert "发生实施障碍或技术问题后" in support["legal_consequence_if_missing"]
    assert "第三方提出权利主张" not in support["legal_consequence_if_missing"]

    support_finding = next(
        row for row in review["risk_findings"]
        if row["risk_group"] == "licensor_support_and_patent_maintenance"
    )
    assert "许可方是否负有协助义务" in support_finding["consequence"]
    assert "第三方提出权利主张" not in support_finding["consequence"]


def test_follow_on_improvement_clauses_are_recalled_and_split_by_element(review: dict):
    by_id = {row["item_id"]: row for row in review["items"]}

    assert by_id["TC-10-01"]["coverage_status"] == "通过"
    assert by_id["TC-10-02"]["coverage_status"] == "部分覆盖"
    assert by_id["TC-10-03"]["coverage_status"] == "部分覆盖"
    assert by_id["TC-10-04"]["coverage_status"] == "通过"
    for review_id in ("TC-10-01", "TC-10-02", "TC-10-03", "TC-10-04"):
        assert {row["clause_id"] for row in by_id[review_id]["evidence_clauses"]} == {"C0030", "C0031"}

    sharing = {row["element_id"]: row for row in by_id["TC-10-02"]["coverage_elements"]}
    assert sharing["reciprocal_free_use"]["status"] == "COVERED"
    assert sharing["license_duration"]["status"] == "COVERED"
    assert sharing["license_territory"]["status"] == "MISSING"

    notice = {row["element_id"]: row for row in by_id["TC-10-03"]["coverage_elements"]}
    assert notice["improvement_material_delivery"]["status"] == "COVERED"
    assert notice["improvement_notice_deadline"]["status"] == "MISSING"


def test_material_schedule_and_handover_confirmation_are_positive_facts(review: dict):
    item = next(row for row in review["items"] if row["item_id"] == "TC-13-01")
    elements = {row["element_id"]: row for row in item["coverage_elements"]}

    assert item["coverage_status"] == "部分覆盖"
    assert elements["closed_attachment_schedule"]["status"] == "COVERED"
    assert elements["receipt_confirmation"]["status"] == "COVERED"
    assert elements["delivery_quantity"]["status"] == "MISSING"
    assert elements["file_version"]["status"] == "MISSING"
    assert elements["file_identifier"]["status"] == "MISSING"
    assert {row["clause_id"] for row in item["evidence_clauses"]} == {"C0056", "C0058", "C0060"}
    assert "未形成最终附件级文件清单" not in item["reasoning_summary"]
    assert "未明确技术资料签收" not in item["reasoning_summary"]

    finding = next(row for row in review["risk_findings"] if row["risk_group"] == "technical_material_attachment")
    direct_evidence = [
        row for row in finding["evidence_bundle"]["items"]
        if row["source_type"] != "SEARCH_AUDIT"
    ]
    assert {row["clause_id"] for row in direct_evidence} >= {"C0058", "C0060"}
    assert any("MATERIAL_ATTACHMENT_SCHEDULE" in row["fact_types"] for row in direct_evidence)
    assert any("MATERIAL_RECEIPT_CONFIRMATION" in row["fact_types"] for row in direct_evidence)
    assert all("交付方式和数量" not in row["proposition"] for row in direct_evidence)


def test_patent_proof_search_audit_uses_atomic_positive_fact_names(review: dict):
    by_id = {row["item_id"]: row for row in review["items"]}
    expected_keys = {
        "patent_name", "patent_number", "patent_owner", "application_date",
        "authorization_date", "co_owner", "existing_license", "pledge", "seizure",
        "annual_fee_status",
    }
    for review_id in ("TC-03-04", "TC-13-02"):
        item = by_id[review_id]
        elements = {row["element_id"]: row for row in item["coverage_elements"]}
        objective = item["decision_trace"]["objective_patent_fact_search"]
        assert item["coverage_status"] == "部分覆盖"
        assert elements["patent_identity_in_contract"]["status"] == "COVERED"
        assert {row["fact_key"] for row in objective["facts"]} == expected_keys
        assert next(row for row in objective["facts"] if row["fact_key"] == "patent_name")["found"] is True
        assert next(row for row in objective["facts"] if row["fact_key"] == "annual_fee_status")["found"] is False

    finding = next(
        row for row in review["risk_findings"]
        if set(row["source_review_ids"]) == {"TC-03-04", "TC-13-02"}
    )
    audit = next(
        row for row in finding["evidence_bundle"]["items"]
        if row["source_type"] == "SEARCH_AUDIT"
    )
    assert audit["search_targets"] == [
        "上游授权书", "再许可授权书", "共有权人同意文件",
        "共同专利权人信息", "既有许可披露", "专利质押登记", "专利查封保全",
        "专利证书正文", "专利登记簿副本",
    ]
    assert all(term not in audit["quoted_text"] for term in ("已在合同中明确", "尚无法核验", "完整性不足"))


def test_patent_proof_partial_summary_lists_only_unresolved_gaps(review: dict):
    by_id = {row["item_id"]: row for row in review["items"]}

    for review_id in ("TC-03-04", "TC-13-02"):
        item = by_id[review_id]
        assert item["coverage_status"] == "部分覆盖"
        assert "正文已约定许可方按时缴纳" not in item["reasoning_summary"]
        assert "权利负担已披露" not in item["reasoning_summary"]
        assert "专利现时有效状态及年费缴纳状态证明" in item["reasoning_summary"]
        assert "权利负担披露材料" in item["reasoning_summary"]


def test_infringement_remedy_coordination_ignores_unrelated_payment_penalty(review: dict):
    item = next(row for row in review["items"] if row["item_id"] == "TC-12-04")

    assert item["coverage_status"] == "不适用"
    assert item["evidence_clauses"] == []
    assert "同一侵权损失" in item["reasoning_summary"]
    assert "退还专利资料" not in item["reasoning_summary"]
    assert "提成费" not in item["reasoning_summary"]


def test_same_loss_gate_is_generic_not_fixture_specific():
    unrelated = _review(
        "专利实施许可合同。许可方许可被许可方实施发明专利。"
        "如第三方指控许可专利侵权，许可方负责交涉并承担由此产生的一切法律和经济责任。"
        "被许可方逾期支付许可费的，每日按应付未付金额万分之五支付违约金。"
    )
    linked = _review(
        "专利实施许可合同。许可方许可被许可方实施发明专利。"
        "如第三方指控许可专利侵权，许可方负责交涉并承担由此产生的一切法律和经济责任。"
        "任何一方违反本合同任何义务并造成对方损失的，应赔偿全部实际损失。"
    )

    unrelated_item = next(row for row in unrelated["items"] if row["item_id"] == "TC-12-04")
    linked_item = next(row for row in linked["items"] if row["item_id"] == "TC-12-04")
    assert unrelated_item["coverage_status"] == "不适用"
    assert linked_item["coverage_status"] != "不适用"


def test_scope_pass_lists_the_actual_patent_license_coverage(review: dict):
    item = next(row for row in review["items"] if row["item_id"] == "TC-07-01")
    elements = {row["element_id"]: row for row in item["coverage_elements"]}

    assert item["coverage_status"] == "通过"
    assert all(elements[key]["status"] == "COVERED" for key in (
        "licensed_patent_subject", "permitted_implementation_acts", "license_territory",
        "license_term", "license_type", "transfer_or_sublicense_boundary",
    ))
    for label in ("许可标的", "实施方式", "许可地域", "许可期限", "许可类型", "许可权转让或再许可边界"):
        assert label in item["risk_point_description"]
    assert "合同已覆盖技术许可范围要求" not in item["risk_point_description"]


def test_audit_confidentiality_does_not_cover_general_technical_secret_rules(review: dict):
    by_id = {row["item_id"]: row for row in review["items"]}

    for review_id in ("TC-11-01", "TC-11-02"):
        item = by_id[review_id]
        assert item["coverage_status"] == "INSUFFICIENT_CONTEXT"
        assert item["risk_level"] == "低"
        assert item["risk_severity"] == "NONE"
        assert item["needs_manual_review"] is True
        assert item["evidence_clauses"] == []
        assert item["decision_trace"]["audit_confidentiality_scope_filter"]["audit_clause_does_not_cover_general_technical_secret"] is True
        trigger = item["decision_trace"]["technical_secret_applicability"]
        assert trigger["technical_secret_positive_fact"] is False
        assert trigger["public_patent_material_is_not_secret_fact"] is True
        assert trigger["commercial_secret_distinguished_from_technical_secret"] is True
        audit = item["decision_trace"]["specialized_search_audit"]
        assert audit["query_semantics"] == "POSITIVE_REQUIRED_FACT"
        assert all("未找到" not in target for target in audit["required_positive_facts"])


def test_major_risks_and_action_counts_share_the_final_result(review: dict):
    overview = review["final_overview_summary"]
    findings = review["risk_findings"]
    dispositions = review["final_dispositions"]

    assert overview["major_risk"] == sum(row["severity"] in {"HIGH", "CRITICAL"} for row in findings)
    assert overview["priority_action"] == sum(row["final_action"] == "MUST_CHANGE" for row in dispositions)
    assert overview["major_risk"] == 0
    assert overview["priority_action"] == 0
    assert overview["manual_review"] == review["manual_review_summary"]["manual_review_count"] == 5
    high_findings = [row for row in findings if row["severity"] in {"HIGH", "CRITICAL"}]
    assert all(row["priority"] == "A_CORE" for row in high_findings)
    assert review["final_disposition_invariant_gate"]["status"] == "REPORT_READY"
    assert review["release_quality_gate"]["status"] == "REPORT_READY"


def test_major_missing_rules_have_transaction_specific_recommendations(review: dict):
    by_id = {row["item_id"]: row for row in review["items"]}
    over_scope = by_id["TC-07-03"]
    assert over_scope["risk_level"] == "低"
    assert over_scope["risk_direction"]["gate_result"] == "SUPPRESS_LICENSEE_ADVERSE_RISK"
    assert "不主动新增或扩大被许可方赔偿责任" in over_scope["suggested_clause_example"]
    assert all(
        row["risk_group"] not in {
            "license_over_scope_liability", "technical_secret_confidentiality", "confidentiality_period_and_scope",
        }
        for row in review["risk_findings"]
    )
    for review_id in ("TC-11-01", "TC-11-02"):
        assert by_id[review_id]["action_suggestion"].startswith("人工复核：请确认")
        assert "请确认请确认" not in by_id[review_id]["action_suggestion"]


def test_confidentiality_liability_inherits_unresolved_family_applicability(review: dict):
    item = next(row for row in review["items"] if row["item_id"] == "TC-11-04")
    elements = {row["element_id"]: row for row in item["coverage_elements"]}
    propagation = item["decision_trace"]["confidentiality_family_applicability_propagation"]

    assert item["coverage_status"] == "INSUFFICIENT_CONTEXT"
    assert item["coverage_presence"] == "UNCERTAIN"
    assert item["risk_severity"] == "NONE"
    assert item["applicability"]["status"] == "CONDITIONALLY_APPLICABLE"
    assert elements["confidentiality_breach_applicability"]["status"] == "UNCERTAIN"
    assert propagation["child_status"] == "INHERITED_INSUFFICIENT_CONTEXT"
    assert propagation["independent_evidence_ids"] == []


def test_third_party_claim_core_and_advanced_elements_are_separated(review: dict):
    item = next(row for row in review["items"] if row["item_id"] == "TC-12-02")
    elements = {row["element_id"]: row for row in item["coverage_elements"]}

    assert elements["licensor_participation"]["status"] == "COVERED"
    assert elements["licensor_participation"]["supporting_evidence"]
    # An umbrella legal/economic responsibility clause does not separately
    # enumerate the allocation of claim-handling and defence expenses.
    assert elements["damages_allocation"]["status"] == "COVERED"
    assert elements["defense_cost_allocation"]["status"] == "MISSING"
    assert elements["notification_requirement"]["status"] == "MISSING"
    assert elements["settlement_non_prejudice"]["status"] == "MISSING"
    assert elements["lawyer_selection"]["risk_relevant"] is False
    assert "律师选择" not in item["decision_trace"]["third_party_claim_element_tiers"]["necessary_protection_gaps"]
    assert "约定工作日内" not in item["reasoning_summary"]


def test_cross_border_patent_license_uses_ordered_import_analysis(review: dict):
    item = next(row for row in review["items"] if row["item_id"] == "TC-13-04")
    elements = {row["element_id"]: row for row in item["coverage_elements"]}
    evidence_ids = {row["clause_id"] for row in item["evidence_clauses"]}

    assert elements["cross_border_transaction_direction"]["status"] == "COVERED"
    assert elements["technology_import_characterization"]["status"] == "COVERED"
    assert elements["cross_border_transaction_type"]["status"] == "COVERED"
    assert elements["royalty_payment_method"]["status"] == "COVERED"
    assert {"C0019", "C0020"} <= evidence_ids
    trace = item["decision_trace"]["regulatory_reasoning_chain"]
    assert trace["steps"] == [
        "跨境方向", "技术进口或出口", "具体交易类型", "自由/限制/禁止属性", "对应管理路径",
    ]
    rendered = " ".join((item["reasoning_summary"], item["risk_point_description"], item["suggested_clause_example"]))
    assert "技术进口" in rendered
    assert "专利实施许可" in rendered
    assert "提成" in rendered
    assert "现行技术进出口目录" in rendered
    assert "境内委托方" not in rendered
    assert "技术咨询" not in rendered
    assert item["needs_manual_review"] is True
    assert item["decision_trace"]["external_verification"]["status"] == "NEEDS_EXTERNAL_VERIFICATION"
    assert review["final_overview_summary"]["manual_review"] >= 1
    disposition = next(row for row in review["final_dispositions"] if "TC-13-04" in row["review_ids"])
    assert disposition["final_action"] == "MANUAL_REVIEW"
    assert "《中国禁止进口限制进口技术目录》" in disposition["review_instruction"]
