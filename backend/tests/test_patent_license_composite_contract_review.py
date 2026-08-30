from pathlib import Path

import pytest
from docx import Document

from review_v2.engine import review_contract_v2
from review_v2.technology_service_analysis import classify_technology_transaction
from review_v2.user_profile import UserRiskProfile


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "test_data" / "10、专利.docx"


def _fixture_text() -> str:
    document = Document(str(FIXTURE))
    return "\n".join(paragraph.text for paragraph in document.paragraphs if paragraph.text.strip())


@pytest.fixture(scope="module")
def composite_review() -> dict:
    return review_contract_v2(
        _fixture_text(),
        "technology",
        use_llm=False,
        profile=UserRiskProfile(user_identity="被许可方/付款方"),
    )


def test_patent_license_is_primary_and_commissioned_development_is_secondary_module():
    classification = classify_technology_transaction(_fixture_text())

    assert classification["primary_subtype"] == "TECHNOLOGY_LICENSE"
    assert classification["tertiary_subtype"] == "PATENT_LICENSE"
    assert classification["license_mode"] == "EXCLUSIVE"
    assert classification["secondary_modules"] == ["COMMISSIONED_DEVELOPMENT"]
    assert set(classification["ancillary_obligations"]) == {
        "TRAINING",
        "INSTALLATION_AND_COMMISSIONING",
        "TECHNICAL_GUIDANCE",
        "TECHNICAL_SUPPORT",
    }
    assert "TECHNICAL_CONSULTING" in classification["excluded_subtypes"]
    assert "TECHNICAL_SERVICE" in classification["excluded_subtypes"]
    assert "COOPERATIVE_DEVELOPMENT" in classification["excluded_subtypes"]


def test_composite_transaction_applicability_isolated_before_substantive_review(composite_review: dict):
    by_id = {row["item_id"]: row for row in composite_review["items"]}

    assert all(by_id[f"TC-08-0{index}"]["coverage_status"] == "不适用" for index in range(1, 5))
    assert all(by_id[f"TC-09-0{index}"]["coverage_status"] == "不适用" for index in range(1, 5))
    assert all(by_id[f"TC-06-0{index}"]["coverage_status"] == "不适用" for index in range(1, 5))
    assert by_id["TC-05-01"]["coverage_status"] == "不适用"
    assert by_id["TC-05-02"]["coverage_status"] == "不适用"
    assert by_id["TC-02-03"]["coverage_status"] == "不适用"
    assert by_id["TC-02-04"]["coverage_status"] == "不适用"

    non_applicable_ids = {
        row["item_id"] for row in composite_review["items"] if row["coverage_status"] == "不适用"
    }
    assert all(
        not non_applicable_ids.intersection(finding["source_review_ids"])
        for finding in composite_review["risk_findings"]
    )


def test_composite_contract_recovers_development_and_infringement_truth(composite_review: dict):
    by_id = {row["item_id"]: row for row in composite_review["items"]}

    assert by_id["TC-04-02"]["coverage_status"] == "通过"
    assert by_id["TC-04-02"]["coverage_presence"] == "PRESENT"
    assert "开发费用" in by_id["TC-04-02"]["reasoning_summary"]

    assert by_id["TC-04-04"]["coverage_status"] == "风险条款"
    assert by_id["TC-04-04"]["risk_status"] == "ADVERSE"
    assert "开发费不退" in by_id["TC-04-04"]["reasoning_summary"]

    assert by_id["TC-12-01"]["coverage_status"] == "风险条款"
    assert by_id["TC-12-01"]["issue_type"] == "DEFAULT_LAW_DEVIATION"
    assert "被许可方承担" in by_id["TC-12-01"]["reasoning_summary"]

    assert by_id["TC-12-02"]["coverage_status"] == "部分覆盖"
    assert by_id["TC-12-02"]["coverage_presence"] == "PARTIAL"
    element_statuses = {element["element_id"]: element["status"] for element in by_id["TC-12-02"]["coverage_elements"]}
    assert element_statuses["claim_notice_and_participation"] == "COVERED"
    assert element_statuses["defense_and_settlement_control"] == "MISSING"
    assert element_statuses["defense_cost_allocation"] == "MISSING"
    assert element_statuses["continuity_and_replacement_remedy"] == "MISSING"

    assert by_id["TC-12-04"]["coverage_status"] == "风险条款"
    assert by_id["TC-12-04"]["risk_status"] == "ADVERSE"
    assert "责任上限" in by_id["TC-12-04"]["reasoning_summary"]


def test_license_and_confidentiality_reviews_stay_covered_and_report_context_is_specific(composite_review: dict):
    by_id = {row["item_id"]: row for row in composite_review["items"]}

    assert all(by_id[f"TC-07-0{index}"]["coverage_status"] == "通过" for index in range(1, 5))
    assert all(by_id[f"TC-11-0{index}"]["coverage_status"] == "通过" for index in range(1, 5))
    assert composite_review["report_context"]["contract_type_label"] == "技术合同—技术许可合同—专利实施许可（含委托开发模块）"
    assert composite_review["contract_context"]["user_role"] == "patent_licensee"
    assert composite_review["contract_context"]["counterparty_role"] == "patent_licensor"
    assert composite_review["release_quality_gate"]["status"] == "REPORT_READY"


def test_composite_gap_reviews_use_contract_specific_states_and_evidence(composite_review: dict):
    by_id = {row["item_id"]: row for row in composite_review["items"]}

    assert by_id["TC-05-04"]["coverage_status"] == "部分覆盖"
    assert "阶段成果" in by_id["TC-05-04"]["reasoning_summary"]
    assert by_id["TC-05-04"]["evidence_clauses"]

    assert by_id["TC-10-03"]["coverage_status"] == "缺失"
    assert "改进成果形成后的专项通知义务" in by_id["TC-10-03"]["reasoning_summary"]

    assert by_id["TC-10-04"]["coverage_status"] == "风险条款"
    assert by_id["TC-10-04"]["risk_status"] == "ADVERSE"
    assert "不可转让" in by_id["TC-10-04"]["reasoning_summary"]
    assert by_id["TC-10-04"]["evidence_clauses"]

    assert by_id["TC-13-03"]["coverage_status"] == "部分覆盖"
    assert "98.5%" in by_id["TC-13-03"]["reasoning_summary"]
    assert "独立附件" in by_id["TC-13-03"]["reasoning_summary"]


def test_final_disposition_is_the_single_report_action_source(composite_review: dict):
    report = composite_review["result"]
    dispositions = composite_review["final_dispositions"]
    visible = [row for row in dispositions if row["report_visibility"] == "VISIBLE"]
    recommended = [row for row in visible if row["final_action"] in {"MUST_CHANGE", "SHOULD_CHANGE"}]
    optional = [row for row in visible if row["final_action"] == "OPTIONAL_IMPROVEMENT"]

    assert composite_review["report_view_model"]["recommended_total"] == len(recommended)
    assert composite_review["report_view_model"]["optional_total"] == len(optional)
    assert composite_review["report_disposition_projection_gate"]["status"] == "REPORT_READY"
    assert all(row["recommendation"].strip() for row in recommended + optional)

    priority_section = report.split("、建议修改事项", 1)[1].split("\n## ", 1)[0]
    optional_section = report.split("、可选优化事项", 1)[1].split("\n## ", 1)[0]
    assert sum(line.startswith("- **") for line in priority_section.splitlines()) == len(recommended)
    assert sum(line.startswith("- **") for line in optional_section.splitlines()) == len(optional)
    assert all(row["risk_title"] in priority_section for row in recommended)
    assert all(row["risk_title"] in optional_section for row in optional)
    assert "暂无需要单独提示的可优化事项" not in optional_section
    assert "正式建议：\n" not in report
    assert "明确合同明确" not in report

    ownership = next(row for row in dispositions if row["risk_title"] == "权属证明附件")
    assert ownership["final_action"] == "SHOULD_CHANGE"
    assert "**权属证明附件**：建议处理。" in report


def test_final_evidence_matches_each_adverse_proposition(composite_review: dict):
    findings = {row["risk_group"]: row for row in composite_review["risk_findings"]}

    infringement = findings["license_infringement_responsibility"]["evidence_bundle"]["items"]
    infringement_by_type = {row["fact_type"]: row for row in infringement}
    assert "均由被许可方承担" in infringement_by_type["LICENSEE_LOSS_ALLOCATION"]["quoted_text"]
    assert all(term in infringement_by_type["LICENSEE_LOSS_ALLOCATION"]["quoted_text"] for term in (
        "停产损失", "产品召回损失", "对第三方的赔偿", "律师费", "诉讼费",
    ))
    assert "许可方仅承担协助义务" in infringement_by_type["LICENSOR_ASSISTANCE_ONLY"]["quoted_text"]

    uncapped = findings["license_infringement_uncapped_indemnity"]["evidence_bundle"]
    assert any(row["fact_type"] == "OPEN_ENDED_LOSS_SCOPE" for row in uncapped["items"])
    assert any(row["source_type"] == "SEARCH_AUDIT" and "责任总额上限" in row["quoted_text"] for row in uncapped["items"])

    improvement = findings["improvement_no_unlawful_restriction"]["evidence_bundle"]["items"]
    assert all(row["support_strength"] == "DIRECT" for row in improvement)
    assert not any(str(row["clause_number"]).startswith("第一条") for row in improvement)
    improvement_text = "\n".join(row["quoted_text"] for row in improvement)
    assert all(term in improvement_text for term in (
        "120万元", "全部归许可方", "不可转让", "不可分许可", "使用权同时终止",
    ))

    audit = composite_review["report_integrity_gate"]["evidence_proposition_audit"]
    assert audit["status"] == "PASS"
    assert audit["checked_risk_count"] == 10
    dispute_audit = next(
        row for row in audit["rows"]
        if row["risk_group"] == "dispute_resolution_choice_conflict"
    )
    assert dispute_audit["status"] == "PASS"
    assert len(dispute_audit["direct_contract_evidence_ids"]) >= 2
    assert all(row["direct_evidence_ids"] for row in audit["rows"])


def test_ip_proof_linked_reviews_share_one_canonical_partial_state(composite_review: dict):
    by_id = {row["item_id"]: row for row in composite_review["items"]}
    provenance = next(
        row for row in composite_review["risk_findings"]
        if row["risk_group"] == "technology_ip_rights_provenance"
    )

    assert provenance["issue_type"] == "PARTIAL"
    assert provenance["severity"] == "MEDIUM"
    assert set(provenance["source_review_ids"]) == {"TC-03-04", "TC-13-02"}
    for review_id in ("TC-03-04", "TC-13-02"):
        assert by_id[review_id]["coverage_status"] == "部分覆盖"
        assert by_id[review_id]["issue_type"] == "PARTIAL"
        assert by_id[review_id]["decision_trace"]["canonical_risk_state"]["risk_id"] == provenance["finding_id"]
    assert composite_review["report_integrity_gate"]["gate_results"]["CANONICAL_RISK_COVERAGE_INVARIANT"] == "PASS"


def test_pass_evidence_is_bound_to_coverage_propositions(composite_review: dict):
    by_id = {row["item_id"]: row for row in composite_review["items"]}
    secret_result = by_id["TC-05-03"]

    assert secret_result["coverage_status"] == "通过"
    assert secret_result["issue_type"] == "通过"
    assert secret_result["evidence_clauses"]
    primary = secret_result["evidence_clauses"][0]
    assert primary["support_type"] == "DIRECT"
    assert primary["location"] == "第八条第7项"
    assert all(term in primary["quote"] for term in ("使用权", "不可转让", "不可分许可"))
    assert "一式六份" not in primary["quote"]
    assert "签字、盖章之日起生效" not in primary["quote"]

    audit = composite_review["report_integrity_gate"]["pass_evidence_proposition_audit"]
    assert audit["status"] == "PASS"
    # The count may change when a formerly generic PASS is correctly split into
    # an ancillary PARTIAL review; the invariant is that every remaining PASS
    # was audited and none failed.
    assert audit["checked_pass_count"] >= 19
    assert not audit["failures"]
    assert composite_review["report_integrity_gate"]["gate_results"]["PASS_EVIDENCE_PROPOSITION_MATCH_GATE"] == "PASS"
