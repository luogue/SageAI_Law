from __future__ import annotations

from review_v2.engine import (
    PRIORITY_A_CORE,
    PRIORITY_B_PRACTICAL,
    PRIORITY_C_OPTIMIZATION,
    ReviewItemResult,
    _action_priority_for_item,
)
from review_v2.engine import review_contract_v2


LEASE_TEXT = (
    "上海市房屋租赁合同。签订日期：2024年1月1日。"
    "根据《中华人民共和国合同法》及有关规定，双方订立本合同。"
    "第一条 房屋坐落于上海市浦东新区，产证编号沪房地浦字第123号。"
    "第五条 月租金为3852元，支付方式为银行转账，【每月5日前】☑【________】。"
    "第六条 押金为人民币6000元，合同终止时结清费用后无息返还。"
    "第九条 乙方欠租超过7日经甲方催告后仍不支付的，甲方有权解除合同。"
    "第十条 乙方提前退租的，应按剩余租期租金2倍支付违约金。"
    "第十一条 双方协商不成的，向浦东新区人民法院起诉。"
)


def _by_id(output):
    return {item["item_id"]: item for item in output["items"]}


def _priority_rank(priority: str) -> int:
    return {PRIORITY_A_CORE: 0, PRIORITY_B_PRACTICAL: 1, PRIORITY_C_OPTIMIZATION: 2, "NONE": 3}.get(priority, 4)


def test_priority_normalized_economic_exposure_promotes_time_amplified_tenant_risk():
    output = review_contract_v2(LEASE_TEXT, "house_lease", use_llm=False)
    by_id = _by_id(output)
    hl039 = by_id["HL-039"]
    early = next(finding for finding in output["risk_findings"] if finding["risk_group"] == "early_termination_financial_exposure")

    assert hl039["action_priority"] == PRIORITY_A_CORE
    assert early["priority"] == PRIORITY_A_CORE
    assert early["economic_impact"]["monthly_payment_multiple"] >= 20
    assert early["economic_impact"]["time_amplifying"] is True
    assessment = hl039["decision_trace"]["priority_assessment"]
    assert assessment["input"]["severity"] in {"MEDIUM", "HIGH"}
    assert "monthly_multiple" in assessment["reason"]
    assert "time_amplifying" in assessment["reason"]


def test_priority_counterfactual_penalty_size_and_time_amplification_change_priority():
    base = dict(
        item_id="T-001",
        node_id="penalty_adjustment",
        title="违约金校准",
        risk_level="中",
        status="风险条款",
        risk_point_description="违约金可能偏高。",
        suggested_clause_example="建议设置上限。",
        legal_basis_index="《中华人民共和国民法典》第585条",
        legal_consequence_if_missing="可能形成过高经济负担。",
        applicable_if="存在违约金",
        matched_terms=[],
        coverage_status="风险条款",
        issue_type="风险条款",
        evidence_clauses=[{"text": "提前退租违约金。", "location": "第十条"}],
        evidence_location="第十条",
        reasoning_summary="测试",
        risk_severity="MEDIUM",
        risk_group="early_termination_financial_exposure",
    )
    low = ReviewItemResult(**base)
    low.economic_impact = "low"
    low.economic_impact_detail = {"estimated_max_loss": 3852, "monthly_payment_multiple": 1, "level": "low", "time_amplifying": False}

    high = ReviewItemResult(**base)
    high.economic_impact = "critical"
    high.economic_impact_detail = {"estimated_max_loss": 77040, "monthly_payment_multiple": 20, "level": "critical", "time_amplifying": True}
    high.scenario_analysis = {"monthly_rent": 3852, "formula": {"base": "remaining_term_rent", "party": "tenant", "beneficiary": "landlord"}}

    assert _priority_rank(_action_priority_for_item(high)) < _priority_rank(_action_priority_for_item(low))
    assert _action_priority_for_item(high) == PRIORITY_A_CORE


def test_claim_level_entailment_and_production_hides_debug_enums():
    output = review_contract_v2(LEASE_TEXT, "house_lease", use_llm=False)
    by_id = _by_id(output)

    hl013_claims = by_id["HL-013"]["legal_references"]
    assert any(claim["claim_type"] == "LEGAL_EFFECT" and claim["article"] == "第734条" and claim["support_type"] == "DIRECT_SUPPORT" for claim in hl013_claims)
    assert any(claim["claim_type"] == "PROCEDURE" and claim["article"] == "第730条" and claim["support_type"] == "DIRECT_SUPPORT" for claim in hl013_claims)
    assert any(claim["claim_type"] == "DRAFTING_RECOMMENDATION" and not claim["authority_links"] for claim in hl013_claims)

    hl012_claims = by_id["HL-012"]["legal_references"]
    assert any(claim["article"] == "第725条" and claim["support_type"] == "DIRECT_SUPPORT" for claim in hl012_claims)
    assert any(claim["claim_type"] == "DRAFTING_RECOMMENDATION" and not claim["authority_links"] for claim in hl012_claims)

    hl005_188 = [claim for claim in by_id["HL-005"]["legal_references"] if claim["article"] == "第188条"]
    assert hl005_188 and all(claim["support_type"] == "BACKGROUND_ONLY" for claim in hl005_188)

    report = output["result"]
    for token in ("DIRECT_SUPPORT", "PARTIAL_SUPPORT", "BACKGROUND_ONLY", "NOT_SUPPORT", "CONTRADICTS"):
        assert token not in report


def test_hl042_not_merged_with_early_termination_and_missing_evidence_is_negative():
    output = review_contract_v2(LEASE_TEXT, "house_lease", use_llm=False)
    by_review = {
        review_id: finding
        for finding in output["risk_findings"]
        for review_id in finding.get("source_review_ids", [])
    }
    assert by_review["HL-039"]["risk_group"] == "early_termination_financial_exposure"
    assert by_review["HL-042"]["risk_group"] == "deposit_offset_order"
    assert by_review["HL-042"]["finding_id"] != by_review["HL-039"]["finding_id"]

    report = output["result"]
    assert "原文片段：无正式条款证据" not in report
    assert "依据来源：合同文件" not in report
    assert "未在合同正文及附件中定位到对应安排" in report
