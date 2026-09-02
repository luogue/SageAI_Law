from pathlib import Path
from copy import deepcopy

import pytest
from docx import Document

from review_v2.engine import review_contract_v2
from review_v2 import engine as review_engine
from review_v2.technology_service_analysis import (
    analyze_improvement_license_facts,
    analyze_patent_license_consistency,
    analyze_payment_schedule,
    analyze_timeline,
    build_technology_fact_registry,
    classify_technology_transaction,
)
from review_v2.user_profile import UserRiskProfile
from routers.review_v2 import ReviewV2Result


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "test_data" / "25 专利实施许可合同.docx"


def _fixture_text() -> str:
    document = Document(str(FIXTURE))
    return "\n".join(paragraph.text for paragraph in document.paragraphs if paragraph.text.strip())


@pytest.fixture(scope="module")
def patent_license_text() -> str:
    return _fixture_text()


@pytest.fixture(scope="module")
def patent_license_review(patent_license_text: str) -> dict:
    return review_contract_v2(
        patent_license_text,
        "technology",
        include_low_risk=True,
        use_llm=False,
        profile=UserRiskProfile(user_identity="甲方/被许可方"),
    )


def test_payment_formula_uses_fixed_license_fee_and_all_payment_nodes(patent_license_text: str):
    payment = analyze_payment_schedule(patent_license_text)

    assert payment["status"] == "INCONSISTENT"
    assert payment["contract_total"] == 3_000_000
    assert payment["percentage_total"] == 110
    assert payment["amount_total"] == 3_300_000
    assert payment["amount_delta"] == 300_000
    assert payment["currency"] == "CNY"


def test_patent_license_cross_clause_consistency_facts_are_structured(patent_license_text: str):
    classification = classify_technology_transaction(patent_license_text)
    consistency = analyze_patent_license_consistency(patent_license_text)

    assert classification["primary_subtype"] == "TECHNOLOGY_LICENSE"
    assert classification["tertiary_subtype"] == "PATENT_LICENSE"
    assert consistency["exclusive_license_declared"] is True
    assert consistency["licensor_third_party_license_permission"] is True
    assert consistency["exclusive_license_conflict"] is True
    assert consistency["patent_type"] == "INVENTION"
    assert consistency["application_date"] == "2018-06-15"
    assert consistency["basic_patent_expiry_date"] == "2038-06-15"
    assert consistency["license_end_date"] == "2042-12-31"
    assert consistency["patent_term_compensation_present"] is False
    assert consistency["license_term_exceeds_basic_patent_term"] is True
    assert consistency["patent_protection_territories"] == ["CN_MAINLAND"]
    assert consistency["license_contains_foreign_territory"] is True
    assert consistency["license_territory_exceeds_patent_protection"] is True
    assert consistency["patent_invalidity_terminates_contract"] is True
    assert consistency["future_fixed_fee_continues_after_invalidity"] is True
    assert consistency["patent_invalidity_fee_conflict"] is True


def test_forced_free_improvement_transfer_is_not_treated_as_coverage_pass(patent_license_text: str):
    improvement = analyze_improvement_license_facts(patent_license_text)

    assert improvement["forced_free_improvement_transfer"] is True
    assert improvement["unreasonable_improvement_restriction"] is True
    assert improvement["arrangement_status"] == "ASYMMETRIC"


def test_license_start_before_signature_is_a_deterministic_timeline_conflict(patent_license_text: str):
    timeline = analyze_timeline(patent_license_text)

    assert timeline["license_start_date"] == "2026-10-10"
    assert timeline["contract_effective_date"] == "2026-10-20"
    assert timeline["primary_conflict_subject"] == "LICENSE_START"
    assert any(row["type"].startswith("LICENSE_BEFORE_") for row in timeline["conflicts"])


def test_third_party_claim_registry_preserves_notice_cost_direction_and_cap(patent_license_text: str):
    claim = build_technology_fact_registry(patent_license_text)["third_party_claim"]

    assert claim["notification_requirement"] is True
    assert claim["notification_deadline"] is True
    assert claim["attorney_fee_allocation"] is True
    assert claim["litigation_cost_allocation"] is True
    assert claim["claim_cost_bearer"] == "LICENSEE"
    assert claim["licensor_liability_cap"] is True
    assert claim["licensor_liability_cap_percentage"] == 20


def test_full_review_projects_cross_clause_risks_without_stale_missing_facts(patent_license_review: dict):
    by_id = {row["item_id"]: row for row in patent_license_review["items"]}

    assert patent_license_review["release_quality_gate"]["status"] == "REPORT_READY"
    assert by_id["TC-02-01"]["coverage_status"] == "风险条款"
    assert by_id["TC-07-01"]["coverage_status"] == "风险条款"
    assert "排他许可" in by_id["TC-07-01"]["risk_point_description"]
    assert "2038-06-15" in by_id["TC-07-01"]["risk_point_description"]
    assert "境外" in by_id["TC-07-01"]["risk_point_description"]
    assert by_id["TC-07-02"]["coverage_status"] == "风险条款"
    assert "仍继续支付" in by_id["TC-07-02"]["title"]
    assert all(by_id[item_id]["coverage_status"] == "风险条款" for item_id in ("TC-10-01", "TC-10-02", "TC-10-04"))

    claim_elements = {row["element_id"]: row for row in by_id["TC-12-02"]["coverage_elements"]}
    assert claim_elements["notification_requirement"]["status"] == "COVERED"
    assert claim_elements["notification_deadline"]["status"] == "COVERED"
    assert claim_elements["defense_cost_allocation"]["status"] == "COVERED"
    assert claim_elements["damages_allocation"]["status"] == "COVERED"
    assert "通知义务仍需" not in by_id["TC-12-02"]["risk_point_description"]
    assert "通知义务、通知期限" in by_id["TC-12-02"]["risk_point_description"]
    assert "已有约定" in by_id["TC-12-02"]["risk_point_description"]
    assert "费用承担不明" not in by_id["TC-12-02"]["legal_consequence_if_missing"]
    assert "第三方索赔抗辩控制权" in by_id["TC-12-02"]["legal_consequence_if_missing"]
    assert "相关合同要素" not in by_id["TC-12-02"]["legal_consequence_if_missing"]
    assert "替代技术或绕开侵权方案" in by_id["TC-12-02"]["legal_consequence_if_missing"]

    cap_elements = {row["element_id"]: row for row in by_id["TC-12-04"]["coverage_elements"]}
    assert cap_elements["licensor_liability_cap"]["status"] == "ADVERSE"
    assert "20%" in cap_elements["licensor_liability_cap"]["proposition"]


def test_material_acceptance_and_payment_rendering_are_grounded(patent_license_review: dict):
    by_id = {row["item_id"]: row for row in patent_license_review["items"]}
    material = by_id["TC-13-01"]
    elements = {row["element_id"]: row for row in material["coverage_elements"]}

    assert elements["receipt_confirmation"]["status"] == "COVERED"
    assert elements["delivery_quantity"]["status"] == "MISSING"
    assert not any(
        "本合同一式" in str(evidence.get("raw_text") or evidence.get("text") or "")
        for evidence in material["evidence_clauses"]
    )
    assert {str(evidence.get("clause_number") or evidence.get("location") or "") for evidence in material["evidence_clauses"]} <= {"第五条", "附件"}

    payment = by_id["GEN-PAY-01"]
    assert payment["risk_level"] == "高"
    assert payment["recommended_action"] == "MUST_FIX"
    assert "110%" in payment["risk_point_description"]
    assert "3,300,000元" in payment["risk_point_description"]
    assert "3,000,000元" in payment["risk_point_description"]
    assert "300,000元" in payment["risk_point_description"]
    assert "合同总价元" not in patent_license_review["result"]


def test_payment_formula_finding_requires_current_document_bound_inputs(
    monkeypatch: pytest.MonkeyPatch,
    patent_license_text: str,
):
    stale_payment = deepcopy(analyze_payment_schedule(patent_license_text))
    for fact in [
        *(stale_payment.get("contract_total_candidates") or []),
        *(stale_payment.get("nodes") or []),
    ]:
        fact["source_document"] = "different-contract-document-hash"

    monkeypatch.setattr(review_engine, "analyze_payment_schedule", lambda _text: stale_payment)
    items = review_engine._apply_technology_relationship_risk_layer([], patent_license_text)

    assert not any(item.item_id == "GEN-PAY-01" for item in items)


def test_payment_formula_finding_rejects_an_unbound_contract_total(
    monkeypatch: pytest.MonkeyPatch,
    patent_license_text: str,
):
    unbound_payment = deepcopy(analyze_payment_schedule(patent_license_text))
    unbound_payment["contract_total_candidates"] = []
    unbound_payment["contract_total_evidence"] = {}

    monkeypatch.setattr(review_engine, "analyze_payment_schedule", lambda _text: unbound_payment)
    items = review_engine._apply_technology_relationship_risk_layer([], patent_license_text)

    assert not any(item.item_id == "GEN-PAY-01" for item in items)


def test_valid_payment_formula_finding_has_a_complete_evidence_precondition(patent_license_review: dict):
    payment = next(row for row in patent_license_review["items"] if row["item_id"] == "GEN-PAY-01")
    trace = payment["decision_trace"]
    bundle = trace["evidence_bundle"]

    assert trace["payment_calculation_precondition"]["status"] == "PASSED"
    assert bundle["entailment_status"] == "PASSED"
    assert bundle["missing_fact_types"] == []
    assert bundle["unsupported_claim_ids"] == []
    assert {"contract_total", "payment_node_1", "payment_node_2", "payment_node_3"} <= set(
        bundle["covered_fact_types"]
    )


def test_improvement_presence_and_adverse_direction_are_kept_separate(patent_license_review: dict):
    by_id = {row["item_id"]: row for row in patent_license_review["items"]}

    ownership = {row["element_id"]: row for row in by_id["TC-10-01"]["coverage_elements"]}
    boundary = {row["element_id"]: row for row in by_id["TC-10-04"]["coverage_elements"]}
    assert ownership["improvement_ownership_written"]["status"] == "COVERED"
    assert ownership["licensee_independent_improvement_ownership"]["status"] == "ADVERSE"
    assert ownership["licensee_independent_improvement_ownership"]["presence_status"] == "COVERED"
    assert ownership["licensee_independent_improvement_ownership"]["direction"] == "ADVERSE"
    assert boundary["improvement_restriction_written"]["status"] == "COVERED"
    assert boundary["forced_free_ownership_transfer"]["status"] == "ADVERSE"
    assert not any(row["status"] == "MISSING" for row in ownership.values())


def test_third_party_claim_atomic_states_do_not_relabel_existing_terms_as_missing(patent_license_review: dict):
    claim = next(row for row in patent_license_review["items"] if row["item_id"] == "TC-12-02")
    elements = {row["element_id"]: row for row in claim["coverage_elements"]}

    assert elements["notification_requirement"]["status"] == "COVERED"
    assert elements["notification_deadline"]["status"] == "COVERED"
    assert elements["licensor_participation"]["status"] == "COVERED"
    assert elements["defense_cost_allocation"]["status"] == "COVERED"
    assert elements["defense_cost_allocation"]["direction"] == "ADVERSE"
    assert elements["damages_allocation"]["status"] == "COVERED"
    assert elements["damages_allocation"]["direction"] == "ADVERSE"
    assert elements["defense_control"]["status"] == "MISSING"
    assert elements["lawyer_selection"]["status"] == "MISSING"
    assert elements["settlement_authority"]["status"] == "MISSING"
    assert "通知义务" in claim["risk_point_description"]
    assert "已有约定" in claim["risk_point_description"]


def test_technical_material_recommendation_is_generated_from_missing_elements(patent_license_review: dict):
    material = next(row for row in patent_license_review["items"] if row["item_id"] == "TC-13-01")
    recommendation = material["suggested_clause_example"]
    trace = material["decision_trace"]["recommendation_element_status_source"]

    assert set(trace["missing_element_ids"]) == {"delivery_quantity", "file_version", "file_identifier"}
    assert "技术资料交付数量" in recommendation
    assert "最终交付文件版本号" in recommendation
    assert "最终交付文件编号" in recommendation
    assert "数量及签收机制" not in recommendation
    assert "无需重复" not in recommendation


def test_final_report_consumes_the_same_element_truth_as_review_items(patent_license_review: dict):
    report = patent_license_review["result"]

    assert "合同总价元" not in report
    assert "未明确通知期限、抗辩控制" not in report
    assert "未登记的处理责任" not in report
    assert "被许可方独立改进成果归属尚未覆盖" not in report
    assert "被许可方独立改进成果归属已有约定" not in report
    assert "不要重复扩写已经明确的资料类型、交付方式、数量及签收机制" not in report
    assert "与合同总价3,000,000元相差300,000元" in report
    assert "被许可方独立形成的改进成果及知识产权被要求无偿转归许可方" in report
    assert "建议补充或明确：技术资料交付数量、最终交付文件版本号、最终交付文件编号" in report

    for finding in patent_license_review["risk_findings"]:
        assert not (set(finding.get("covered_element_ids") or []) & set(finding.get("missing_element_ids") or []))

    claim_finding = next(
        finding for finding in patent_license_review["risk_findings"]
        if finding.get("risk_group") == "third_party_claim_defense"
    )
    assert "费用承担不明" not in claim_finding["consequence"]
    assert "如通知、抗辩控制" not in claim_finding["consequence"]

    material_finding = next(
        finding for finding in patent_license_review["risk_findings"]
        if finding.get("risk_group") == "technical_material_attachment"
    )
    material_quotes = "\n".join(
        str(row.get("quoted_text") or "")
        for row in (material_finding.get("evidence_bundle") or {}).get("items", [])
    )
    assert "本合同一式" not in material_quotes
    assert "技术资料" in material_quotes


def test_user_visible_themes_merge_the_same_improvement_fact_without_losing_findings(
    patent_license_review: dict,
):
    themes = patent_license_review["risk_themes"]
    improvement_theme = next(
        theme for theme in themes
        if theme["risk_fingerprint"]["risk_object"] == "IMPROVEMENT_RESULT_RIGHTS"
        and theme["risk_fingerprint"]["core_fact"] == "FORCED_FREE_TRANSFER_AND_USE_RESTRICTION"
    )

    assert patent_license_review["finding_count"] == 13
    assert len(patent_license_review["risk_findings"]) == 13
    assert patent_license_review["risk_theme_count"] == 13
    assert improvement_theme["title"] == "改进成果无偿转归及权利限制"
    assert improvement_theme["member_finding_ids"] == ["RF-001", "RF-005"]
    assert improvement_theme["source_rule_ids"] == ["TC-02-01", "TC-10-01", "TC-10-02", "TC-10-04"]
    assert improvement_theme["evidence_ids"]
    assert "C0008" in improvement_theme["evidence_ids"]
    assert {row["finding_id"] for row in improvement_theme["child_findings"]} == {"RF-001", "RF-005"}
    assert improvement_theme["severity"] == "HIGH"
    assert improvement_theme["underlying_finding_count"] == 2


def test_distinct_legal_exposures_remain_independent_user_visible_themes(
    patent_license_review: dict,
):
    themes = patent_license_review["risk_themes"]
    theme_by_rule = {
        rule_id: theme
        for theme in themes
        for rule_id in theme["source_rule_ids"]
    }

    assert theme_by_rule["GEN-PAY-01"]["theme_id"] != theme_by_rule["TC-07-02"]["theme_id"]
    assert theme_by_rule["TC-12-01"]["theme_id"] != theme_by_rule["TC-12-02"]["theme_id"]
    assert theme_by_rule["TC-12-02"]["theme_id"] != theme_by_rule["TC-12-04"]["theme_id"]
    assert all(
        len(theme_by_rule[rule_id]["member_finding_ids"]) == 1
        for rule_id in ("GEN-PAY-01", "TC-07-02", "TC-12-01", "TC-12-02", "TC-12-04")
    )


def test_report_statistics_and_summary_use_the_aggregated_theme_projection(
    patent_license_review: dict,
):
    report = patent_license_review["result"]
    theme_summary = patent_license_review["risk_theme_summary"]
    core_summary = report.split("核心风险摘要", 1)[1].split("建议优先修改", 1)[0]

    assert theme_summary == {
        "total": 13,
        "must_change": 1,
        "should_change": 10,
        "optional_improvement": 2,
        "manual_review": 0,
    }
    assert patent_license_review["risk_theme_severity_summary"] == {
        "major": 6,
        "medium": 5,
        "low": 2,
    }
    assert "风险主题数（聚合后）：13" in report
    assert "底层审查发现数：13" in report
    assert "重大风险数量：6" in report
    assert "中等风险数量：5" in report
    assert "低风险数量：2" in report
    assert "需要真正修改的风险数：11" in report
    assert core_summary.count("改进成果无偿转归及权利限制") == 1
    assert "非法限制技术进步和发展" not in core_summary
    assert "被许可方独立改进成果被强制无偿转归许可方" not in core_summary
    assert patent_license_review["release_quality_gate"]["status"] == "REPORT_READY"


def test_file_api_response_schema_preserves_user_visible_risk_themes(
    patent_license_review: dict,
):
    public_response = ReviewV2Result(**patent_license_review).model_dump()

    assert public_response["risk_theme_count"] == 13
    assert public_response["finding_count"] == 13
    assert public_response["risk_theme_summary"]["should_change"] == 10
    assert public_response["risk_theme_severity_summary"] == {
        "major": 6,
        "medium": 5,
        "low": 2,
    }
    assert any(
        theme["title"] == "改进成果无偿转归及权利限制"
        and theme["member_finding_ids"] == ["RF-001", "RF-005"]
        for theme in public_response["risk_themes"]
    )
