from pathlib import Path

import pytest
from docx import Document

from review_v2.engine import review_contract_v2
from review_v2.technology_service_analysis import (
    analyze_patent_license_consistency,
    analyze_payment_schedule,
    classify_technology_transaction,
)
from review_v2.user_profile import UserRiskProfile


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "test_data" / "27 专利实施许可（含后续开发）合同.docx"


@pytest.fixture(scope="module")
def contract_text() -> str:
    document = Document(str(FIXTURE))
    return "\n".join(paragraph.text for paragraph in document.paragraphs if paragraph.text.strip())


@pytest.fixture(scope="module")
def review(contract_text: str) -> dict:
    return review_contract_v2(
        contract_text,
        "technology",
        include_low_risk=True,
        use_llm=False,
        profile=UserRiskProfile(user_identity="甲方/被许可方"),
    )


def test_patent_license_route_and_cross_clause_conflicts(contract_text: str):
    classification = classify_technology_transaction(contract_text)
    consistency = analyze_patent_license_consistency(contract_text)

    assert classification["primary_subtype"] == "TECHNOLOGY_LICENSE"
    assert classification["tertiary_subtype"] == "PATENT_LICENSE"
    assert "COMMISSIONED_DEVELOPMENT" in classification["secondary_modules"]
    assert consistency["exclusive_license_declared"] is True
    assert consistency["licensor_third_party_license_permission"] is True
    assert consistency["exclusive_license_conflict"] is True
    assert consistency["exclusive_license_downgrade_present"] is True
    assert consistency["exclusive_license_unilateral_downgrade"] is True
    assert consistency["downgrade_trigger_defined"] is True
    assert consistency["downgrade_notice_present"] is False
    assert consistency["downgrade_cure_period_present"] is False
    assert consistency["downgrade_consideration_adjustment_present"] is False
    assert consistency["patent_invalidity_occurs"] is True
    assert consistency["contract_continues_after_patent_invalidity"] is True
    assert consistency["future_fixed_fee_continues_after_invalidity"] is True
    assert consistency["royalty_continues_after_invalidity"] is True
    assert consistency["termination_prohibited_after_invalidity"] is True
    assert consistency["patent_invalidity_fee_conflict"] is True


def test_payment_formula_is_partitioned_by_price_base(contract_text: str):
    payment = analyze_payment_schedule(contract_text)
    groups = {row["label"]: row for row in payment["payment_groups"]}

    assert payment["status"] == "INCONSISTENT"
    assert payment["contract_total"] == 4_800_000
    assert payment["percentage_total"] is None
    assert payment["amount_total"] == 5_460_000
    assert payment["amount_delta"] == 660_000

    patent_fee = groups["专利许可费"]
    assert patent_fee["base_amount"] == 3_000_000
    assert patent_fee["percentages"] == [60, 30, 20]
    assert patent_fee["percentage_total"] == 110
    assert patent_fee["amount_total"] == 3_300_000
    assert patent_fee["amount_delta"] == 300_000

    development_fee = groups["后续技术开发费"]
    assert development_fee["base_amount"] == 1_800_000
    assert development_fee["percentages"] == [50, 40, 30]
    assert development_fee["percentage_total"] == 120
    assert development_fee["amount_total"] == 2_160_000
    assert development_fee["amount_delta"] == 360_000


def test_license_scope_invalidity_notice_and_competition_results(review: dict):
    by_id = {row["item_id"]: row for row in review["items"]}

    assert by_id["TC-07-01"]["coverage_status"] == "风险条款"
    assert "排他许可" in by_id["TC-07-01"]["risk_point_description"]
    assert "单方将排他许可降级为普通许可" in by_id["TC-07-01"]["risk_point_description"]
    assert "按专利类型、申请日" not in by_id["TC-07-01"]["suggested_clause_example"]
    assert "按各法域" not in by_id["TC-07-01"]["suggested_clause_example"]
    assert by_id["TC-07-02"]["coverage_status"] == "风险条款"
    assert "专利无效" in by_id["TC-07-02"]["title"]
    assert "继续支付" in by_id["TC-07-02"]["risk_point_description"]

    notice = by_id["TC-10-03"]
    notice_elements = {row["element_id"]: row for row in notice["coverage_elements"]}
    assert notice["coverage_status"] == "部分覆盖"
    assert notice["needs_manual_review"] is False
    assert notice_elements["improvement_notice_trigger"]["status"] == "COVERED"
    assert notice_elements["improvement_notice_deadline"]["status"] == "COVERED"
    assert notice_elements["improvement_notice_content"]["status"] == "COVERED"
    assert notice_elements["improvement_notice_form"]["status"] == "MISSING"

    competition = by_id["TC-02-01"]
    adverse_elements = {
        row["element_id"] for row in competition["coverage_elements"] if row["status"] == "ADVERSE"
    }
    assert {
        "independent_competing_research_restriction",
        "external_competing_technology_access_restriction",
        "substitute_solution_restriction",
        "forced_free_improvement_transfer",
        "post_termination_competition_restriction",
    } <= adverse_elements


def test_acceptance_and_ip_proof_attachment_are_partial_without_manual_review(review: dict):
    by_id = {row["item_id"]: row for row in review["items"]}

    acceptance = by_id["TC-13-03"]
    acceptance_elements = {row["element_id"]: row for row in acceptance["coverage_elements"]}
    assert acceptance["coverage_status"] == "部分覆盖"
    assert acceptance["action_priority"] == "C_OPTIMIZATION"
    assert acceptance["needs_manual_review"] is False
    assert acceptance_elements["acceptance_test_scene"]["status"] == "COVERED"
    assert acceptance_elements["acceptance_test_attachment_arrangement"]["status"] == "COVERED"
    assert acceptance_elements["quantitative_metrics"]["status"] == "MISSING"
    assert acceptance_elements["retest_mechanism"]["status"] == "MISSING"

    for review_id in ("TC-03-04", "TC-13-02"):
        proof = by_id[review_id]
        proof_elements = {row["element_id"]: row for row in proof["coverage_elements"]}
        assert proof["coverage_status"] == "部分覆盖"
        assert proof_elements["patent_certificate_or_register_attachment"]["status"] == "COVERED"
        assert proof_elements["patent_legal_status_and_annual_fee"]["status"] == "MISSING"
        assert proof_elements["license_encumbrance_and_conflict_disclosure"]["status"] == "MISSING"
        assert proof_elements["patent_proof_attachment_content_verification"]["status"] == "MISSING"
        assert "缺失权属证明附件" not in proof["risk_point_description"]


def test_unilateral_acceptance_and_confidentiality_asymmetry_are_distinct_risks(review: dict):
    by_id = {row["item_id"]: row for row in review["items"]}

    acceptance = by_id["TC-04-01"]
    assert acceptance["coverage_status"] == "风险条款"
    assert acceptance["risk_level"] == "中"
    assert "由对方单方决定" in acceptance["title"]
    assert "双方在测试前书面确认" in acceptance["suggested_clause_example"]
    assert any("TC-04-01" in theme["source_rule_ids"] for theme in review["risk_themes"])

    confidentiality = by_id["TC-11-02"]
    assert confidentiality["coverage_status"] == "风险条款"
    assert confidentiality["risk_level"] == "中"
    assert "保密期限及合同终止后数据使用权限明显不对等" in confidentiality["title"]
    assert "脱敏或匿名化" in confidentiality["suggested_clause_example"]
    assert by_id["TC-11-03"]["coverage_status"] == "通过"


def test_not_applicable_secret_rule_acknowledges_existing_secret_facts(review: dict):
    item = next(row for row in review["items"] if row["item_id"] == "TC-12-03")
    assert item["coverage_status"] == "不适用"
    assert "已明确技术秘密范围" in item["applicability"]["reason"]
    assert "未形成以技术秘密秘密性为独立对价基础" in item["applicability"]["reason"]
    assert "未形成可识别的技术秘密范围" not in item["applicability"]["reason"]


def test_final_evidence_bundles_never_render_blank_support_items(review: dict):
    for finding in review["risk_findings"]:
        for evidence in (finding.get("evidence_bundle") or {}).get("items", []):
            assert str(
                evidence.get("quoted_text")
                or evidence.get("quote")
                or evidence.get("text")
                or ""
            ).strip()
    assert "[支持：LICENSOR_ASSISTANCE_ONLY]：；" not in review["result"]
    assert "[支持：EXISTING_NOTICE_AND_DEADLINE]：；" not in review["result"]


def test_full_report_uses_grouped_calculation_and_aggregated_risk_themes(review: dict):
    report = review["result"]
    payment = next(row for row in review["items"] if row["item_id"] == "GEN-PAY-01")

    assert "专利许可费的节点比例合计为110%" in payment["risk_point_description"]
    assert "后续技术开发费的节点比例合计为120%" in payment["risk_point_description"]
    assert "5,460,000元" in payment["risk_point_description"]
    assert "4,800,000元相差660,000元" in payment["risk_point_description"]
    assert "230%" not in report

    improvement_themes = [
        theme for theme in review["risk_themes"]
        if {"TC-02-01", "TC-10-01"} <= set(theme["source_rule_ids"])
    ]
    assert len(improvement_themes) == 1
    assert {"TC-02-01", "TC-10-01", "TC-10-02", "TC-10-04"} <= set(
        improvement_themes[0]["source_rule_ids"]
    )
    assert improvement_themes[0]["underlying_finding_count"] == 2
    assert review["finding_count"] == 18
    assert review["risk_theme_count"] == 17
    assert review["manual_review_summary"]["manual_review_count"] == 0
    assert review["release_quality_gate"]["status"] == "REPORT_READY"
