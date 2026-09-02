from pathlib import Path

import pytest
from docx import Document

from review_v2.clause_parser import parse_contract_clauses
from review_v2.engine import (
    _analyze_clause_cross_reference_consistency,
    review_contract_v2,
)
from review_v2.technology_service_analysis import (
    analyze_improvement_license_facts,
    analyze_patent_license_consistency,
    analyze_payment_schedule,
    analyze_third_party_infringement_allocation,
)
from review_v2.user_profile import UserRiskProfile


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "test_data" / "30 专利实施许可（含后续开发）合同.docx"


@pytest.fixture(scope="module")
def contract_text() -> str:
    document = Document(str(FIXTURE))
    return "\n".join(row.text for row in document.paragraphs if row.text.strip())


@pytest.fixture(scope="module")
def review(contract_text: str) -> dict:
    return review_contract_v2(
        contract_text,
        "technology",
        include_low_risk=True,
        use_llm=False,
        profile=UserRiskProfile(user_identity="甲方/被许可方"),
    )


def test_total_components_and_installments_are_reconciled_independently(contract_text: str):
    payment = analyze_payment_schedule(contract_text)
    groups = {row["label"]: row for row in payment["payment_groups"]}

    assert payment["status"] == "INCONSISTENT"
    assert payment["contract_total"] == 5_000_000
    assert payment["component_total_sum"] == 5_500_000
    assert payment["component_total_delta"] == 500_000
    assert payment["amount_total"] == 6_000_000
    assert payment["amount_delta"] == 1_000_000
    assert groups["专利许可费"]["base_amount"] == 3_000_000
    assert groups["专利许可费"]["amount_total"] == 3_500_000
    assert groups["专利许可费"]["amount_delta"] == 500_000
    assert groups["后续技术开发费"]["amount_total"] == 2_500_000
    assert payment["payment_fact_count"] == 6


def test_patent_license_term_uses_explicit_expiry_without_mixing_development_term(contract_text: str):
    analysis = analyze_patent_license_consistency(contract_text)

    assert analysis["application_date"] == "2019-10-10"
    assert analysis["explicit_patent_expiry_date"] == "2039-10-09"
    assert analysis["license_end_date"] == "2042-10-09"
    assert analysis["patent_expiry_source"] == "CONTRACT_EXPLICIT"
    assert analysis["license_term_exceeds_basic_patent_term"] is True


def test_third_party_responsibility_follows_the_actual_party_allocation(contract_text: str, review: dict):
    allocation = analyze_third_party_infringement_allocation(contract_text)
    item = next(row for row in review["items"] if row["item_id"] == "TC-12-01")

    assert allocation["responsible_party"] == "LICENSEE"
    assert allocation["claim_cost_bearer"] == "LICENSEE"
    assert allocation["licensor_assistance_only"] is True
    assert item["coverage_status"] == "风险条款"
    assert "由被许可方自行处理" in item["risk_point_description"]
    assert "许可方仅提供必要协助" in item["risk_point_description"]
    assert "许可方负责处理并承担法律和经济责任" not in item["risk_point_description"]


def test_material_delivery_method_is_covered_but_version_and_schedule_gaps_remain(review: dict):
    item = next(row for row in review["items"] if row["item_id"] == "TC-13-01")
    elements = {row["element_id"]: row for row in item["coverage_elements"]}

    assert elements["delivery_method"]["status"] == "COVERED"
    assert elements["delivery_quantity"]["status"] == "MISSING"
    assert elements["closed_attachment_schedule"]["status"] == "MISSING"
    assert elements["file_version"]["status"] == "MISSING"
    assert "技术资料交付形式" not in item["risk_point_description"]


def test_third_party_disclosure_is_not_counterparty_improvement_notice(review: dict):
    item = next(row for row in review["items"] if row["item_id"] == "TC-10-03")

    assert item["coverage_status"] == "缺失"
    assert "改进成果形成后的专项通知义务" in item["reasoning_summary"] or "未约定改进成果" in item["risk_point_description"]


def test_free_transfer_of_independent_improvements_is_adverse(contract_text: str, review: dict):
    facts = analyze_improvement_license_facts(contract_text)
    item = next(row for row in review["items"] if row["item_id"] == "TC-10-04")

    assert facts["forced_free_improvement_transfer"] is True
    assert item["coverage_status"] == "风险条款"
    assert any(row["status"] == "ADVERSE" for row in item["coverage_elements"])
    assert "无偿" in item["risk_point_description"] or "无偿" in item["title"]


def test_cross_reference_subject_mismatch_is_bound_to_source_and_target(contract_text: str, review: dict):
    mismatches = _analyze_clause_cross_reference_consistency(parse_contract_clauses(contract_text))
    acceptance = next(row for row in review["items"] if row["item_id"] == "TC-13-03")

    assert [(row["expected_subject"], row["referenced_article"], row["target_subject"]) for row in mismatches] == [
        ("验收", 7, "保密")
    ]
    assert acceptance["decision_trace"]["cross_reference_consistency"]["status"] == "MISMATCH"
    assert "按照第七条约定执行" in acceptance["risk_point_description"]
    assert "实际属于保密事项" in acceptance["risk_point_description"]
    finding = next(row for row in review["risk_findings"] if "TC-13-03" in row["source_review_ids"])
    assert "按照第七条约定执行" in finding["issue"]
    assert "实际属于保密事项" in finding["issue"]
    assert "按照第七条约定执行" in review["result"]
    assert "实际属于保密事项" in review["result"]


def test_tc1303_positive_elements_have_element_specific_direct_evidence(review: dict):
    item = next(row for row in review["items"] if row["item_id"] == "TC-13-03")
    elements = {row["element_id"]: row for row in item["coverage_elements"]}
    evidence_by_clause = {
        str(row.get("clause_id") or row.get("evidence_id") or ""): row
        for row in item["evidence_clauses"]
    }

    assert elements["quantitative_metrics"]["status"] == "MISSING"
    assert elements["test_dataset"]["status"] == "PARTIALLY_COVERED"
    assert elements["test_dataset"]["evidence_ids"] == ["C0020"]
    assert elements["retest_mechanism"]["status"] == "COVERED"
    assert elements["retest_mechanism"]["evidence_ids"] == ["C0020"]
    for element in elements.values():
        if element["status"] not in {"COVERED", "PARTIALLY_COVERED", "CONFLICTING"}:
            continue
        assert element["evidence_ids"], element["element_id"]
        assert all(evidence_id in evidence_by_clause for evidence_id in element["evidence_ids"])


def test_tc1303_cross_reference_bundle_and_issue_type_are_consistent(review: dict):
    item = next(row for row in review["items"] if row["item_id"] == "TC-13-03")
    finding = next(row for row in review["risk_findings"] if "TC-13-03" in row["source_review_ids"])
    evidence = {row["fact_type"]: row for row in finding["evidence_bundle"]["items"]}

    assert item["issue_type"] == "CONFLICTING"
    assert finding["issue_type"] == "CONFLICTING"
    assert evidence["REFERENCE_SOURCE"]["clause_id"] == "C0010"
    assert "按照第七条约定执行" in evidence["REFERENCE_SOURCE"]["quoted_text"]
    assert evidence["REFERENCE_TARGET"]["clause_id"] == "C0011"
    assert "保密事项" in evidence["REFERENCE_TARGET"]["quoted_text"]
    assert len(evidence["SEMANTIC_CONFLICT"]["derived_from_evidence_ids"]) == 2
    assert "验收" in evidence["SEMANTIC_CONFLICT"]["quoted_text"]
    assert "保密" in evidence["SEMANTIC_CONFLICT"]["quoted_text"]


def test_tc1303_recommendation_does_not_invent_a_named_attachment(review: dict):
    finding = next(row for row in review["risk_findings"] if "TC-13-03" in row["source_review_ids"])

    assert "验收测试附件或专项测试方案" in finding["recommendation"]
    assert "《项目测试方案》" not in finding["recommendation"]
    assert "《项目测试方案》" not in review["result"]


def test_tc0201_final_claims_do_not_exceed_direct_evidence(review: dict):
    item = next(row for row in review["items"] if row["item_id"] == "TC-02-01")
    finding = next(row for row in review["risk_findings"] if "TC-02-01" in row["source_review_ids"])
    elements = {row["element_id"]: row for row in item["coverage_elements"]}

    assert elements["forced_free_improvement_transfer"]["status"] == "ADVERSE"
    assert elements["forced_free_improvement_transfer"]["evidence_ids"] == ["C0019"]
    assert elements["independent_competing_research_restriction"]["status"] == "NOT_APPLICABLE"
    assert elements["external_competing_technology_access_restriction"]["status"] == "NOT_APPLICABLE"
    assert elements["substitute_solution_restriction"]["status"] == "NOT_APPLICABLE"
    assert elements["post_termination_competition_restriction"]["status"] == "NOT_APPLICABLE"
    assert "无偿转归许可方" in item["risk_point_description"]
    assert "禁止自行研发" not in item["risk_point_description"]
    assert "购买竞争" not in item["risk_point_description"]
    assert "替代方案" not in item["risk_point_description"]
    assert "禁止自行研发" not in finding["issue"]
    assert "购买竞争" not in finding["issue"]
    assert "替代方案" not in finding["issue"]
    direct_clause_ids = {
        row.get("clause_id")
        for row in finding["evidence_bundle"]["items"]
        if row.get("source_type") != "SEARCH_AUDIT" and row.get("clause_id")
    }
    assert direct_clause_ids == {"C0019"}


@pytest.mark.parametrize(
    "review_id, element_id",
    [
        ("TC-10-01", "licensee_independent_improvement_ownership"),
        ("TC-10-02", "licensee_improvement_ownership"),
        ("TC-10-04", "forced_free_ownership_transfer"),
    ],
)
def test_improvement_claims_bind_the_actual_forced_transfer_clause(review: dict, review_id: str, element_id: str):
    item = next(row for row in review["items"] if row["item_id"] == review_id)
    element = next(row for row in item["coverage_elements"] if row["element_id"] == element_id)
    source = next(row for row in item["evidence_clauses"] if row.get("clause_id") == "C0019")
    source_text = source.get("text") or source.get("quote") or ""

    assert element["status"] == "ADVERSE"
    assert element["evidence_ids"] == ["C0019"]
    assert "自行基于后续开发成果" in source_text
    assert "知识产权亦无偿归许可方所有" in source_text


def test_aggregated_improvement_finding_has_a_complete_direct_evidence_bundle(review: dict):
    finding = next(
        row for row in review["risk_findings"]
        if row["risk_group"] == "improvement_no_unlawful_restriction"
    )
    fact_types = {row["fact_type"] for row in finding["evidence_bundle"]["items"]}

    assert fact_types == {
        "LICENSEE_IMPROVEMENT_OWNERSHIP_TRANSFER",
        "FREE_TRANSFER_OBLIGATION",
    }
    assert finding["evidence_bundle"]["entailment_status"] == "PASSED"
    assert review["release_quality_gate"]["status"] == "REPORT_READY"


def test_payment_recommendation_only_mentions_observed_payment_structure(review: dict):
    finding = next(row for row in review["risk_findings"] if row["risk_group"] == "payment_formula_inconsistency")

    assert "合同总价、分项价款及各付款节点金额" in finding["recommendation"]
    assert "尾款" not in finding["recommendation"]
    assert "质保金" not in finding["recommendation"]


def test_operative_license_type_is_not_replaced_by_a_glossary_term(contract_text: str, review: dict):
    analysis = analyze_patent_license_consistency(contract_text)
    item = next(row for row in review["items"] if row["item_id"] == "TC-07-01")

    assert analysis["license_type"] == "SOLE_EXCLUSIVE"
    assert analysis["license_type_label"] == "独占实施许可"
    assert analysis["license_type_self_implementation_conflict"] is True
    assert analysis["license_type_third_party_permission_conflict"] is True
    assert "合同约定独占实施许可" in item["risk_point_description"]
    assert "许可方同时保留自行实施权" in item["risk_point_description"]
    assert "许可方仍可向部分第三方授予普通许可" in item["risk_point_description"]
    assert "合同约定排他实施许可" not in item["risk_point_description"]


def test_explicit_counterparty_improvement_notice_remains_recognizable():
    text = (
        "专利实施许可合同。许可方将其合法持有的专利实施权许可被许可方使用。"
        "被许可方形成改进成果后，应在30日内向许可方书面通知并提交完整技术方案和研发资料。"
    )
    review = review_contract_v2(
        text,
        "technology",
        include_low_risk=True,
        use_llm=False,
        profile=UserRiskProfile(user_identity="甲方/被许可方"),
    )
    item = next(row for row in review["items"] if row["item_id"] == "TC-10-03")
    assert item["coverage_status"] != "缺失"
