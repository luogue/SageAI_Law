from pathlib import Path

from docx import Document

from review_v2.clause_parser import parse_contract_clauses
from review_v2.engine import (
    FinalDisposition,
    Recommendation,
    ReviewItemResult,
    RiskFinding,
    _report_integrity_gate,
    review_contract_v2,
)
from review_v2.user_profile import UserRiskProfile


FIXTURE = Path(__file__).resolve().parents[2] / "test_data" / "8、技术服务.docx"


def _text() -> str:
    document = Document(str(FIXTURE))
    return "\n".join(paragraph.text for paragraph in document.paragraphs if paragraph.text.strip())


def _review() -> dict:
    return review_contract_v2(
        _text(),
        "technology",
        use_llm=False,
        profile=UserRiskProfile(
            user_identity="乙方/技术服务提供方",
            contract_scenario="高校科研数据治理技术服务",
        ),
    )


def _integrity_inputs(output: dict):
    return (
        [ReviewItemResult(**row) for row in output["items"]],
        [RiskFinding(**row) for row in output["risk_findings"]],
        [Recommendation(**row) for row in output["recommendations"]],
        [FinalDisposition(**row) for row in output["final_dispositions"]],
    )


def test_clause_parser_keeps_body_appendix_references_and_signature_page_separate():
    clauses = parse_contract_clauses(_text())
    personal_data = next(row for row in clauses if "数据可能包括师生姓名" in row.text)
    signature = next(row for row in clauses if "签订时间" in row.text)
    effective_condition = next(row for row in clauses if "签字并加盖合同专用章" in row.text)

    assert personal_data.source_type == "BODY"
    assert personal_data.location == "三、（一）"
    assert personal_data.heading_path == ["三、资料的提供", "（一）甲方需要提供的相关资料"]
    assert signature.source_type == "SIGNATURE_PAGE"
    assert signature.location == "签署页"
    assert signature.heading_path[0] == "签署页"
    assert effective_condition.location == "十六、（一）"


def test_same_evidence_span_supports_multiple_claims_without_duplicate_rendering():
    output = _review()
    findings = {row["risk_group"]: row for row in output["risk_findings"]}

    liability = findings["technical_uncapped_cumulative_liability"]["evidence_bundle"]
    combined = next(
        row for row in liability["items"]
        if {"technical_uncapped_cumulative_liability:penalty", "technical_uncapped_cumulative_liability:refund"}
        <= set(row["supports_claim_ids"])
    )
    assert "赔偿" in combined["quoted_text"]
    assert len(combined["supports_claim_ids"]) >= 3
    keys = [
        (row["clause_node_id"], row["start_offset"], row["end_offset"], row["quoted_text_hash"])
        for row in liability["items"]
    ]
    assert len(keys) == len(set(keys))
    assert liability["pre_dedup_item_count"] > liability["post_dedup_item_count"]
    assert sum(row["quoted_text"] == combined["quoted_text"] for row in liability["items"]) == 1

    privacy = findings["personal_information_processing_gap"]["evidence_bundle"]
    assert len(privacy["items"]) == 1
    assert len(privacy["items"][0]["supports_claim_ids"]) == 2

    termination = findings["technical_unilateral_termination_change"]["evidence_bundle"]
    shared = next(row for row in termination["items"] if "提前5个工作日" in row["quoted_text"])
    assert len(shared["supports_claim_ids"]) == 2


def test_material_objection_evidence_uses_review_deadline_not_delay_notice():
    finding = next(
        row for row in _review()["risk_findings"]
        if row["risk_group"] == "short_data_objection_deemed_acceptance"
    )
    bundle = finding["evidence_bundle"]
    by_type = {row["fact_type"]: row for row in bundle["items"]}
    assert "接收后3个工作日内" in by_type["material_review_deadline"]["quoted_text"]
    assert by_type["material_review_deadline"]["clause_number"] == "六、（三）"
    assert "影响发生后3个工作日" not in " ".join(row["quoted_text"] for row in bundle["items"])
    assert "12个" in by_type["large_or_complex_material_scope"]["quoted_text"]
    assert "数据源" in by_type["large_or_complex_material_scope"]["quoted_text"]


def test_timeline_effective_date_has_condition_and_signature_sources():
    finding = next(row for row in _review()["risk_findings"] if row["risk_group"] == "technical_timeline_conflict")
    bundle = finding["evidence_bundle"]
    derived = next(row for row in bundle["derived_facts"] if row["fact_type"] == "contract_effective_date")
    assert len(derived["source_node_ids"]) == 2
    assert any(row["source_type"] == "SIGNATURE_PAGE" for row in bundle["items"])
    assert any(row["clause_number"] == "十六、（一）" for row in bundle["items"])
    assert not any(row["clause_number"] == "十六、（五）" and "签订时间" in row["quoted_text"] for row in bundle["items"])


def test_every_final_risk_has_bundle_and_missing_risk_has_absence_evidence():
    output = _review()
    findings = {row["risk_group"]: row for row in output["risk_findings"]}
    assert all((row.get("evidence_bundle") or {}).get("bundle_id") for row in findings.values())

    legal = findings["legal_reference"]["evidence_bundle"]
    assert {row["source_type"] for row in legal["items"]} == {"BODY", "LEGAL_AUTHORITY"}
    assert set(legal["required_claim_ids"]) <= set(legal["supported_claim_ids"])

    provenance = findings["technology_ip_rights_provenance"]["evidence_bundle"]
    absence = provenance["absence_evidence"]
    assert absence["searched_scope"]
    assert absence["required_elements"]
    assert absence["missing_elements"]
    assert absence["related_trigger_clause_ids"]
    assert any(row["evidence_role"] == "MISSING_ELEMENT_CONTEXT" for row in provenance["items"])


def test_covered_reviews_that_contribute_to_risk_are_not_keep():
    output = _review()
    items = {row["item_id"]: row for row in output["items"]}
    for review_id in ("TC-10-01", "TC-10-02"):
        item = items[review_id]
        assert item["coverage_status"] == "不适用"
        assert not item["related_risks"]

    for review_id in ("TC-11-03",):
        item = items[review_id]
        assert item["coverage_status"] == "通过"
        assert item["related_risks"]
        assert item["risk_status"] == "LINKED_ADVERSE_RISK"
        assert item["recommended_action"] == "MODIFY_WITH_LINKED_RISK"
        assert "无需修改" not in item["action_suggestion"]
        assert item["review_risk_links"]

    safe = next(
        row for row in output["items"]
        if row["coverage_status"] == "通过" and not row["related_risks"]
    )
    assert safe["recommended_action"] == "KEEP"
    assert "无需修改" in safe["action_suggestion"]


def test_gate_blocks_duplicate_span_and_missing_final_bundle():
    output = _review()
    items, findings, recommendations, dispositions = _integrity_inputs(output)
    liability = next(row for row in findings if row.risk_group == "technical_uncapped_cumulative_liability")
    liability.evidence_bundle["items"].append(dict(liability.evidence_bundle["items"][0]))
    legal = next(row for row in findings if row.risk_group == "legal_reference")
    legal.evidence_bundle = {}
    gate = _report_integrity_gate(items, findings, recommendations, dispositions, output["result"])
    requirements = {row["requirement"] for row in gate["failures"]}
    assert {"EVIDENCE_ITEM_UNIQUENESS_GATE", "FINAL_RISK_EVIDENCE_BUNDLE_GATE"} <= requirements


def test_gate_blocks_missing_absence_evidence_and_invalid_clause_node():
    output = _review()
    items, findings, recommendations, dispositions = _integrity_inputs(output)
    provenance = next(row for row in findings if row.risk_group == "technology_ip_rights_provenance")
    provenance.evidence_bundle["absence_evidence"] = {}
    privacy = next(row for row in findings if row.risk_group == "personal_information_processing_gap")
    privacy.evidence_bundle["items"][0]["source_type"] = "APPENDIX"
    gate = _report_integrity_gate(items, findings, recommendations, dispositions, output["result"])
    requirements = {row["requirement"] for row in gate["failures"]}
    assert {"MISSING_RISK_ABSENCE_EVIDENCE_GATE", "CLAUSE_NODE_CONSISTENCY_GATE"} <= requirements


def test_gate_blocks_material_deadline_fact_role_mismatch():
    output = _review()
    items, findings, recommendations, dispositions = _integrity_inputs(output)
    objection = next(row for row in findings if row.risk_group == "short_data_objection_deemed_acceptance")
    deadline = next(row for row in objection.evidence_bundle["items"] if row["fact_type"] == "material_review_deadline")
    deadline["fact_type"] = "PROJECT_DELAY_NOTICE_DEADLINE"
    deadline["fact_types"] = ["PROJECT_DELAY_NOTICE_DEADLINE"]
    gate = _report_integrity_gate(items, findings, recommendations, dispositions, output["result"])
    assert any(row["requirement"] == "EVIDENCE_FACT_ROLE_GATE" for row in gate["failures"])


def test_gate_blocks_linked_covered_review_that_reverts_to_keep():
    output = _review()
    items, findings, recommendations, dispositions = _integrity_inputs(output)
    linked = next(row for row in items if row.coverage_status == "通过" and row.review_risk_links)
    linked.recommended_action = "KEEP"
    linked.action_suggestion = "已覆盖，无需修改。"
    linked.decision_trace["recommendation_display_state"]["user_message"] = "已覆盖，无需修改。"
    gate = _report_integrity_gate(items, findings, recommendations, dispositions, output["result"])
    assert any(row["requirement"] == "COVERAGE_RISK_ACTION_CONSISTENCY_GATE" for row in gate["failures"])
