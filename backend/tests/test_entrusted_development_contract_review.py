import asyncio
import io
import json
from pathlib import Path

import pytest
from docx import Document

from review_v2.engine import _normalize_missing_element_for_recommendation, review_contract_v2
from review_v2.user_profile import UserRiskProfile
from routers.review_v2 import ReviewV2Result, review_v2_file


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = next((ROOT / "test_data").glob("12*.docx"))


class _UploadFile:
    def __init__(self, filename: str, content: bytes):
        self.filename = filename
        self.file = io.BytesIO(content)


def _fixture_text() -> str:
    document = Document(FIXTURE)
    blocks = [paragraph.text for paragraph in document.paragraphs if paragraph.text.strip()]
    for table in document.tables:
        blocks.extend(
            " | ".join(cell.text.strip() for cell in row.cells)
            for row in table.rows
        )
    return "\n".join(blocks)


@pytest.fixture(scope="module")
def party_a_review():
    return review_contract_v2(
        _fixture_text(),
        "technology",
        use_llm=False,
        profile=UserRiskProfile(user_identity="甲方"),
    )


def _by_id(review):
    return {item["item_id"]: item for item in review["items"]}


def test_entrusted_classification_is_canonical_across_report_and_execution(party_a_review):
    canonical = party_a_review["contract_context"]["canonical_classification"]
    report = party_a_review["report_context"]

    assert canonical["contract_family"] == "TECHNOLOGY"
    assert canonical["contract_category"] == "TECHNOLOGY_DEVELOPMENT"
    assert canonical["contract_subtype"] == "ENTRUSTED_DEVELOPMENT"
    assert canonical["transaction_structure"] == "B2B_ENTRUSTED_DEVELOPMENT"
    assert party_a_review["contract_context"]["contract_subtype"] == canonical["contract_subtype"]
    assert party_a_review["contract_context"]["transaction_structure"] == canonical["transaction_structure"]
    assert report["contract_subtype"] == canonical["contract_subtype"]
    assert report["transaction_structure"] == canonical["transaction_structure"]
    assert report["scenario_label"] == "委托开发"
    assert report["contract_type_label"] == "技术合同—技术开发合同—委托开发合同"


def test_entrusted_party_roles_follow_identity_and_subtype(party_a_review):
    party_a = party_a_review["perspective_resolution"]
    assert party_a["review_party_identity"] == "PARTY_A"
    assert party_a["canonical_role"] == "COMMISSIONING_PARTY"
    assert party_a["display_role"] == "甲方 / 委托方"
    assert "专利权受让方" not in party_a["display_role"]

    party_b_review = review_contract_v2(
        _fixture_text(),
        "technology",
        use_llm=False,
        profile=UserRiskProfile(user_identity="乙方"),
    )
    party_b = party_b_review["perspective_resolution"]
    assert party_b["review_party_identity"] == "PARTY_B"
    assert party_b["canonical_role"] == "DEVELOPMENT_CONTRACTOR"
    assert party_b["display_role"] == "乙方 / 开发方"


def test_entrusted_rule_states_and_partial_elements_are_consistent(party_a_review):
    items = _by_id(party_a_review)
    expected = {
        "TC-01-01": "通过",
        "TC-01-04": "不适用",
        "TC-04-01": "通过",
        "TC-04-02": "通过",
        "TC-04-03": "部分覆盖",
        "TC-04-04": "部分覆盖",
        "TC-05-04": "部分覆盖",
        "TC-12-02": "部分覆盖",
        "TC-12-04": "部分覆盖",
        "TC-13-01": "通过",
        "TC-13-03": "部分覆盖",
    }
    assert {review_id: items[review_id]["coverage_status"] for review_id in expected} == expected

    for review_id in ("TC-04-03", "TC-04-04", "TC-05-04", "TC-12-02", "TC-12-04"):
        statuses = {element["status"] for element in items[review_id]["coverage_elements"]}
        assert "COVERED" in statuses
        assert "MISSING" in statuses
        audit = items[review_id]["decision_trace"]["specialized_search_audit"]
        assert audit["searched_full_document"] is True
        assert audit["searched_aliases"]
        assert audit["missing_elements"]
        narrative = " ".join(
            str(items[review_id].get(key) or "")
            for key in ("reasoning_summary", "risk_point_description")
        )
        assert "适用范围、履行标准和责任安排" not in narrative


def test_entrusted_rule_evidence_covers_body_and_attachment_semantics(party_a_review):
    items = _by_id(party_a_review)

    expected_terms = {
        "TC-04-01": ("主要功能", "里程碑"),
        "TC-04-02": ("开发费用", "付款"),
        "TC-04-03": ("前景知识产权", "申请"),
        "TC-05-04": ("解除", "开发费用"),
        "TC-12-02": ("第三方", "许可"),
        "TC-13-01": ("源代码", "测试报告"),
        "TC-13-03": ("验收", "测试"),
    }
    for review_id, terms in expected_terms.items():
        evidence_text = " ".join(
            str(row.get("text") or row.get("quote") or "")
            for row in items[review_id]["evidence_clauses"]
        )
        assert all(term in evidence_text for term in terms)


def test_entrusted_report_is_generated_without_fatal_quality_gate(party_a_review):
    assert party_a_review["report_generation_decision"]["status"] == "GENERATED"
    assert party_a_review["report_generation_decision"]["report_generated"] is True
    assert party_a_review["report_generation_decision"]["fatal_rule_ids"] == []


def test_unsubstantiated_generic_missing_is_local_manual_review(party_a_review):
    generic_phrase = "适用范围、履行标准和责任安排"
    manual_items = []
    for item in party_a_review["items"]:
        if item["coverage_status"] == "缺失" and generic_phrase in item["risk_point_description"]:
            audit = item["decision_trace"].get("specialized_search_audit")
            assert audit and audit["searched_full_document"] is True
            assert audit["missing_elements"]
        if item["coverage_status"] == "INSUFFICIENT_CONTEXT":
            manual_items.append(item["item_id"])
            assert item["needs_manual_review"] is True
            assert item["decision_trace"]["missing_fallback_resolution"]["original_status"] == "MISSING"
            assert generic_phrase not in item["risk_point_description"]
    assert all(review_id for review_id in manual_items)


def test_acceptance_evidence_does_not_invent_third_party_testing(party_a_review):
    item = _by_id(party_a_review)["TC-13-03"]
    elements = {row["element_id"]: row for row in item["coverage_elements"]}

    assert item["coverage_status"] == "部分覆盖"
    assert elements["acceptance_metrics"]["status"] == "COVERED"
    assert elements["test_method_and_report"]["status"] == "COVERED"
    assert elements["acceptance_dispute_verification"]["status"] == "MISSING"
    assert elements["acceptance_dispute_verification"]["supporting_evidence_ids"] == []
    evidence_text = " ".join(str(row.get("quote") or row.get("text") or "") for row in item["evidence_clauses"])
    assert "第三方检测机构" not in evidence_text


def test_explicit_third_party_testing_clause_is_covered():
    text = _fixture_text() + "\n如双方对测试结果存在争议，共同委托有资质的第三方检测机构进行检测，检测结果作为验收依据。"
    review = review_contract_v2(
        text,
        "technology",
        use_llm=False,
        profile=UserRiskProfile(user_identity="甲方"),
    )
    item = _by_id(review)["TC-13-03"]
    element = next(row for row in item["coverage_elements"] if row["element_id"] == "acceptance_dispute_verification")

    assert item["coverage_status"] == "通过"
    assert element["status"] == "COVERED"
    assert element["supporting_evidence_ids"]


def test_post_termination_confidentiality_is_directly_covered(party_a_review):
    item = _by_id(party_a_review)["TC-11-02"]
    elements = {row["element_id"]: row for row in item["coverage_elements"]}

    assert item["coverage_status"] == "通过"
    assert elements["during_contract_confidentiality"]["status"] == "COVERED"
    assert elements["during_contract_confidentiality"]["supporting_evidence_ids"]
    assert elements["post_termination_confidentiality"]["status"] == "COVERED"
    assert elements["post_termination_confidentiality"]["supporting_evidence_ids"]
    assert elements["confidentiality_duration"]["status"] == "COVERED"
    assert elements["confidentiality_duration"]["supporting_evidence_ids"]
    evidence_text = " ".join(str(row.get("quote") or row.get("text") or "") for row in item["evidence_clauses"])
    assert "终止或解除之后仍需履行" in evidence_text


def test_recommendation_normalization_removes_negative_prefixes(party_a_review):
    assert _normalize_missing_element_for_recommendation("未专项明确专利申请权归属") == ("专项明确", "专利申请权归属")
    report = party_a_review["result"]
    assert "建议明确未专项明确" not in report
    assert "建议明确未明确" not in report
    assert "建议明确未约定" not in report


def test_gap_consequences_are_bound_to_actual_missing_elements(party_a_review):
    items = _by_id(party_a_review)
    patent = items["TC-04-03"]["narrative_state"]["consequence"]
    failure = items["TC-04-04"]["narrative_state"]["consequence"]
    exit_consequence = items["TC-05-04"]["narrative_state"]["consequence"]

    assert all(term in patent for term in ("申请主体", "文件签署", "权利登记"))
    assert "第三方提出权利主张" not in patent
    assert all(term in failure for term in ("研发费用", "阶段成果", "资料交接"))
    assert "风险转移、质量异议" not in failure
    assert all(term in exit_consequence for term in ("接管项目", "继续开发", "既有投入"))
    assert "付款期限、逾期责任" not in exit_consequence


def test_manual_review_and_insufficient_context_states_are_explained(party_a_review):
    missing_count = party_a_review["coverage_summary"].get("缺失", 0)
    insufficient = [item for item in party_a_review["items"] if item["coverage_status"] == "INSUFFICIENT_CONTEXT"]
    assert missing_count == sum(item["coverage_status"] == "缺失" for item in party_a_review["items"])
    for item in party_a_review["items"]:
        if item["coverage_status"] == "通过" and item["needs_manual_review"]:
            assert item["evidence_clauses"]
            assert item["quality_gate_failure_reason"]
        if item["coverage_status"] == "缺失" and item["decision_trace"].get("specialized_search_audit"):
            assert item["needs_manual_review"] is False
    for item in insufficient:
        assert item["issue_type"] == "人工复核"
        assert item["quality_gate_failure_reason"]


def test_production_file_api_renders_entrusted_development_snapshot():
    engine_output = asyncio.run(
        review_v2_file(
            file=_UploadFile(FIXTURE.name, FIXTURE.read_bytes()),
            contract_type="technology",
            include_low_risk=True,
            use_llm=False,
            profile_json=json.dumps({"user_identity": "甲方"}, ensure_ascii=False),
            current_user={"id": 1},
        )
    )
    output = ReviewV2Result.model_validate(engine_output).model_dump()
    items = _by_id(output)
    markdown = output["result"]
    ownership = {
        row["final_output"]: row
        for row in output["observability"]["final_output_ownership_matrix"]
    }

    assert output["filename"] == FIXTURE.name
    assert output["extracted_text_length"] > 1000
    assert output["report_generation_decision"]["report_generated"] is True
    assert output["release_quality_gate"]["status"] == "REPORT_READY"
    assert output["perspective_resolution"]["display_role"] == "甲方 / 委托方"
    assert "审查立场：甲方 / 委托方" in markdown

    expected_statuses = {
        "TC-04-01": "通过",
        "TC-04-02": "通过",
        "TC-04-03": "部分覆盖",
        "TC-04-04": "部分覆盖",
        "TC-05-04": "部分覆盖",
        "TC-12-02": "部分覆盖",
        "TC-12-04": "部分覆盖",
        "TC-13-01": "通过",
        "TC-13-03": "部分覆盖",
    }
    assert {review_id: items[review_id]["coverage_status"] for review_id in expected_statuses} == expected_statuses

    third_party = next(
        element
        for element in items["TC-13-03"]["coverage_elements"]
        if element["element_id"] == "acceptance_dispute_verification"
    )
    assert third_party["status"] == "MISSING"
    assert third_party["supporting_evidence_ids"] == []
    assert "第三方检测机制明确" not in markdown

    confidentiality = items["TC-11-02"]
    assert confidentiality["coverage_status"] == "通过"
    assert "终止或解除之后仍需履行" in " ".join(
        str(row.get("quote") or row.get("text") or "")
        for row in confidentiality["evidence_clauses"]
    )

    assert "建议明确未明确" not in markdown
    assert "建议明确未约定" not in markdown
    assert "建议明确未专项明确" not in markdown
    assert "建议补充明确合同尚未" not in markdown
    assert all(term in markdown for term in ("申请主体", "文件签署", "权利登记"))
    assert all(term in markdown for term in ("研发费用", "阶段成果", "资料交接"))
    assert all(term in markdown for term in ("接管项目", "继续开发", "既有投入"))

    assert ownership["正式建议"]["current_producer"].endswith("FinalDisposition.recommendation")
    assert ownership["缺失的法律后果"]["current_producer"].startswith("RiskFinding.consequence")
    assert output["manual_review_summary"]["manual_review_count"] == 0
