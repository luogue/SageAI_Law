from __future__ import annotations

from review_v2.benchmark import FAILURE_TAXONOMY, run_regression_benchmark
from review_v2.engine import (
    PRIORITY_C_OPTIMIZATION,
    ReviewItemResult,
    _action_priority_for_item,
    review_contract_v2,
)


BASE_LEASE_TEXT = (
    "上海市房屋租赁合同。出租人为甲方，承租人为乙方，本合同用于住宅居住。"
    "租金为每月3852元，每月5日前支付。"
    "乙方欠租超过7日经甲方催告后仍不支付的，甲方有权解除合同。"
    "乙方提前退租的，应按剩余租期租金2倍向甲方支付违约金。"
)


def _by_id(output):
    return {item["item_id"]: item for item in output["items"]}


def test_evidence_entailment_hl042_rejects_early_termination_penalty():
    output = review_contract_v2(
        BASE_LEASE_TEXT
        + "押金为6000元，合同终止结清费用后无息返还。"
        + "乙方中途擅自退租的，应支付违约金；甲方可从租赁保证金中抵扣，不足部分由乙方另行支付。",
        "house_lease",
        use_llm=False,
    )
    hl042 = _by_id(output)["HL-042"]

    assert hl042["coverage_status"] == "缺失"
    assert hl042["risk_group"] == "deposit_offset_order"
    assert hl042["evidence_clauses"] == []
    assert hl042["decision_trace"]["negative_evidence"]["result"] == "NOT_FOUND"
    rejected = hl042["decision_trace"]["negative_evidence"]["rejected_candidates"]
    assert all(candidate["entailment_status"] not in {"SUPPORTS", "PARTIAL_SUPPORT"} for candidate in rejected)
    finding = next(finding for finding in output["risk_findings"] if "HL-042" in finding.get("source_review_ids", []))
    assert finding["risk_group"] == "deposit_offset_order"


def test_evidence_entailment_hl042_accepts_real_deposit_offset_partial():
    text = BASE_LEASE_TEXT + "押金可抵扣未付租金、水电费、维修费，抵扣后余额返还。"
    output = review_contract_v2(text, "house_lease", use_llm=False)
    hl042 = _by_id(output)["HL-042"]

    assert hl042["coverage_status"] in {"部分覆盖", "通过"}
    evidence_text = "".join(evidence.get("quote") or evidence.get("text") or "" for evidence in hl042["evidence_clauses"])
    assert "押金" in evidence_text
    assert any(term in evidence_text for term in ("抵扣", "扣除", "扣款"))
    assert "提前退租" not in evidence_text
    assert any(evidence.get("entailment_status") in {"SUPPORTS", "PARTIAL_SUPPORT"} for evidence in hl042["evidence_clauses"])


def test_legal_claim_recall_tenant_death_direct_authority_and_clean_report():
    output = review_contract_v2(BASE_LEASE_TEXT, "house_lease", use_llm=False)
    hl007 = _by_id(output)["HL-007"]
    claims = hl007["legal_references"]

    assert any(
        claim.get("claim_type") == "RIGHT"
        and claim.get("article") == "第732条"
        and claim.get("support_type") == "DIRECT_SUPPORT"
        and claim.get("authority_id") == "CN-CIVIL-CODE-732"
        and claim.get("citation_existence_status") == "FOUND"
        for claim in claims
    )
    assert "《中华人民共和国民法典》第732条" in output["result"]
    assert "DIRECT_SUPPORT" not in output["result"]
    assert "【法律依据】：法律依据：" not in output["result"]
    assert "【法律依据】：依据：" not in output["result"]


def test_default_law_priority_lowers_low_probability_clear_default_issue():
    output = review_contract_v2(BASE_LEASE_TEXT, "house_lease", use_llm=False)
    hl007 = _by_id(output)["HL-007"]

    assert hl007["decision_trace"]["default_law_status"] == "CLEAR_DEFAULT"
    assert hl007["decision_trace"]["priority_assessment"]["priority"] == PRIORITY_C_OPTIMIZATION
    assert "clear_default_law_protection" in hl007["decision_trace"]["priority_assessment"]["reason"]

    base = dict(
        item_id="T-DEFAULT",
        node_id="tenant_death_successor",
        title="出租人死亡或权利承继",
        risk_level="中",
        status="缺失",
        risk_point_description="合同未约定出租人死亡后的权利义务承继安排。",
        suggested_clause_example="建议补充权利证明和收款账户变更流程。",
        legal_basis_index="《中华人民共和国民法典》第725条",
        legal_consequence_if_missing="可能造成通知和付款衔接争议。",
        applicable_if="房屋租赁",
        matched_terms=[],
        coverage_status="缺失",
        issue_type="缺失",
        evidence_clauses=[],
        evidence_location="",
        reasoning_summary="测试",
        risk_severity="LOW",
        risk_group="tenant_death_successor",
        economic_impact="medium",
        economic_impact_detail={"monthly_payment_multiple": 12, "level": "medium", "time_amplifying": False},
        decision_trace={
            "default_law_status": "CLEAR_DEFAULT",
            "effective_gap": {
                "statutory_default": "CLEAR_DEFAULT",
                "default_strength": "strong",
                "residual_operational_risk": "low",
                "residual_legal_risk": "low",
                "contract_override_risk": "low",
            },
        },
    )
    protected = ReviewItemResult(**base)
    unprotected = ReviewItemResult(**{**base, "decision_trace": {"default_law_status": "UNCERTAIN_DEFAULT", "effective_gap": {"statutory_default": "UNCERTAIN_DEFAULT"}}})

    assert _action_priority_for_item(protected) == PRIORITY_C_OPTIMIZATION
    assert _action_priority_for_item(unprotected) != PRIORITY_C_OPTIMIZATION


def test_benchmark_metrics_taxonomy_includes_evidence_legal_5_2():
    output = review_contract_v2(BASE_LEASE_TEXT, "house_lease", use_llm=False)
    metrics = output["benchmark_metrics"]
    for key in (
        "evidence_entailment_accuracy",
        "evidence_direction_accuracy",
        "evidence_source_accuracy",
        "direct_authority_recall",
    ):
        assert key in metrics

    result = run_regression_benchmark([], lambda text, contract_type: output)
    for failure_type in (
        "EVIDENCE_RELATED_NOT_SUPPORTING",
        "EVIDENCE_WRONG_CLAIM",
        "LEGAL_CITATION_MISS",
        "LEGAL_DRAFTING_AS_STATUTORY",
        "LEGAL_DEFAULT_PROTECTION_MISS",
    ):
        assert failure_type in FAILURE_TAXONOMY
        assert failure_type in result["failure_taxonomy"]
