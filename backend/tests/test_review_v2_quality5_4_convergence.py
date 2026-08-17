from __future__ import annotations

from review_v2.engine import ReviewItemResult, _system_confidence_for_item, review_contract_v2


LEASE_TEXT = (
    "上海市房屋租赁合同。出租人为甲方，承租人为乙方，本合同用于住宅居住。"
    "房屋坐落上海市浦东新区测试路1号，产证编号沪房地浦字2020第081234号。"
    "租金为每月3852元，每月5日前支付至甲方账户。"
    "租赁期满后，乙方需要继续承租的，应提前1个月向甲方提出续租要求。"
    "乙方提前退租的，应按剩余租期租金2倍向甲方支付违约金。"
    "租赁关系终止时，保证金除抵充合同约定由乙方承担的费用外，剩余部分无息返还乙方。"
    "双方协商不成的，依法向房屋所在地浦东新区人民法院起诉。"
)


def _by_id(output):
    return {item["item_id"]: item for item in output["items"]}


def test_confidence_not_all_high_and_debug_explains_required_components():
    output = review_contract_v2(LEASE_TEXT, "house_lease", use_llm=False)
    distribution = output["observability"]["confidence_distribution"]
    confidence_rows = output["observability"]["confidence_debug_report"]

    assert distribution.get("high", 0) < 50
    assert distribution.get("medium", 0) >= 1
    assert len(confidence_rows) == 50
    assert all("verifier" in row["required_components"] for row in confidence_rows)
    assert all(row.get("reason") for row in confidence_rows)


def test_weak_related_evidence_does_not_create_tenant_death_partial_coverage():
    output = review_contract_v2(LEASE_TEXT, "house_lease", use_llm=False)
    hl007 = _by_id(output)["HL-007"]

    assert hl007["coverage_status"] == "缺失"
    assert hl007["decision_trace"]["default_law_status"] == "CLEAR_DEFAULT"
    assert hl007["action_priority"] == "C_OPTIMIZATION"
    assert all(element["status"] == "MISSING" for element in hl007["coverage_elements"])


def test_real_partial_requires_element_level_support_and_can_be_medium_confidence():
    item = ReviewItemResult(
        item_id="T-PARTIAL-001",
        node_id="deposit_return_deadline",
        title="押金返还期限",
        risk_level="中",
        status="部分覆盖",
        risk_point_description="合同有押金返还安排但无期限。",
        suggested_clause_example="",
        legal_basis_index="",
        legal_consequence_if_missing="",
        applicable_if="始终适用",
        matched_terms=[],
        coverage_status="部分覆盖",
        issue_type="条款缺陷",
        evidence_clauses=[{"text": "剩余保证金无息返还乙方。", "entailment_status": "PARTIAL_SUPPORT"}],
        evidence_location="测试条款",
        reasoning_summary="测试",
        coverage_elements=[
            {"element_id": "deposit_return", "status": "PARTIALLY_COVERED", "entailment": "PARTIAL_SUPPORT", "verifier_confidence": "medium"},
            {"element_id": "return_deadline", "status": "UNCERTAIN", "entailment": "UNCERTAIN", "verifier_confidence": "low"},
        ],
    )
    confidence = _system_confidence_for_item(item)

    assert confidence["level"] == "medium"
    assert "verifier" in confidence["confidence_bundle"]["limiting_factors"]


def test_missing_with_negative_search_can_remain_high_confidence():
    output = review_contract_v2(LEASE_TEXT, "house_lease", use_llm=False)
    hl042 = _by_id(output)["HL-042"]

    assert hl042["coverage_status"] == "缺失"
    assert hl042["decision_trace"]["negative_evidence"]["result"] == "NOT_FOUND"
    assert hl042["system_confidence"]["level"] == "high"


def test_required_component_low_caps_final_confidence():
    item = ReviewItemResult(
        item_id="T-WEAK-001",
        node_id="deposit_return_deadline",
        title="押金返还期限",
        risk_level="中",
        status="部分覆盖",
        risk_point_description="合同只有押金金额，没有返还期限。",
        suggested_clause_example="",
        legal_basis_index="",
        legal_consequence_if_missing="",
        applicable_if="始终适用",
        matched_terms=[],
        coverage_status="部分覆盖",
        issue_type="条款缺陷",
        evidence_clauses=[{"text": "乙方支付保证金3852元。", "entailment_status": "UNCERTAIN"}],
        evidence_location="测试条款",
        reasoning_summary="测试",
        coverage_elements=[
            {
                "element_id": "return_deadline",
                "status": "UNCERTAIN",
                "entailment": "UNCERTAIN",
                "verifier_confidence": "low",
            }
        ],
    )

    confidence = _system_confidence_for_item(item)
    assert confidence["level"] != "high"
    assert "verifier" in confidence["confidence_bundle"]["limiting_factors"]


def test_recommendation_provenance_separates_statutory_rule_and_drafting_choice():
    output = review_contract_v2(LEASE_TEXT, "house_lease", use_llm=False)
    provenance = output["observability"]["recommendation_provenance_debug_report"]
    source_types = {row["source_type"] for row in provenance}

    assert "STATUTORY_RULE" in source_types or "STATUTORY_DEFAULT" in source_types
    assert "DRAFTING_CHOICE" in source_types or "RISK_MITIGATION" in source_types
    assert output["observability"]["recommendation_provenance_gate"]["status"] == "PASS"
    assert "法定30" not in output["result"]
    assert "DIRECT_SUPPORT" not in output["result"]
