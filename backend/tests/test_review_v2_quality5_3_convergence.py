from __future__ import annotations

from review_v2.engine import (
    ReviewItemResult,
    _system_confidence_for_item,
    review_contract_v2,
)


LEASE_TEXT = (
    "上海市房屋租赁合同。出租人为甲方，承租人为乙方，本合同用于住宅居住。"
    "房屋坐落上海市浦东新区测试路1号，产证编号沪房地浦字2020第081234号。"
    "租金为每月3852元，每月5日前支付至甲方账户。"
    "乙方欠租超过7日经甲方催告后仍不支付的，甲方有权解除合同。"
    "乙方提前退租的，应按剩余租期租金2倍向甲方支付违约金。"
    "双方协商不成的，依法向房屋所在地浦东新区人民法院起诉。"
)


def _by_id(output):
    return {item["item_id"]: item for item in output["items"]}


def test_fact_confidence_not_lowered_by_legal_uncertainty():
    output = review_contract_v2(LEASE_TEXT, "house_lease", use_llm=False)
    by_id = _by_id(output)

    for review_id in ("HL-001", "HL-003", "HL-015", "HL-049"):
        item = by_id[review_id]
        bundle = item["system_confidence"]["confidence_bundle"]
        assert item["system_confidence"]["level"] == "high"
        assert bundle["fact_confidence"] in {"high", "medium"}
        assert "legal" in bundle["ignored_components"]
        assert bundle["legal_confidence"] in {"low", "medium", "not_applicable"}


def test_missing_and_negative_search_can_have_calibrated_confidence():
    output = review_contract_v2(LEASE_TEXT, "house_lease", use_llm=False)
    hl042 = _by_id(output)["HL-042"]
    bundle = hl042["system_confidence"]["confidence_bundle"]

    assert hl042["coverage_status"] == "缺失"
    assert hl042["decision_trace"]["negative_evidence"]["result"] == "NOT_FOUND"
    assert bundle["evidence_confidence"] in {"high", "medium"}
    assert hl042["system_confidence"]["level"] in {"high", "medium"}
    assert "legal" in bundle["ignored_components"]


def test_formula_and_calculation_confidence_are_independent_from_legal():
    item = ReviewItemResult(
        item_id="T-FORMULA-001",
        node_id="penalty_adjustment",
        title="扣款和违约金调减",
        risk_level="高",
        status="部分覆盖",
        risk_point_description="提前退租违约金以剩余租期租金为基数。",
        suggested_clause_example="建议设置金额上限。",
        legal_basis_index="",
        legal_consequence_if_missing="",
        applicable_if="存在提前退租",
        matched_terms=[],
        coverage_status="部分覆盖",
        issue_type="条款缺陷",
        evidence_clauses=[{"text": "提前退租按剩余租期租金2倍支付违约金。"}],
        evidence_location="测试条款",
        reasoning_summary="测试",
        fact_dependencies=["early_termination.penalty_formula"],
        scenario_analysis={
            "formula": {"type": "remaining_term_rent_multiplier", "base": "remaining_term_rent", "multiplier": 2},
            "cases": [{"remaining_days": 30, "estimated_penalty": 7704}],
        },
        legal_references=[{"claim_type": "STATUTORY_RULE", "support_type": "UNCERTAIN", "support_scope": "", "confidence": "low"}],
    )
    confidence = _system_confidence_for_item(item)
    bundle = confidence["confidence_bundle"]

    assert bundle["formula_confidence"] == "high"
    assert bundle["calculation_confidence"] == "high"
    assert "formula" in bundle["required_components"]
    assert "calculation" in bundle["required_components"]
    assert "legal" in bundle["ignored_components"]


def test_dependency_aware_confidence_and_fact_conflict_lower_only_fact_component():
    item = ReviewItemResult(
        item_id="T-CONF-001",
        node_id="rent_payment",
        title="租金支付规则",
        risk_level="低",
        status="通过",
        risk_point_description="合同明确租金支付日期。",
        suggested_clause_example="",
        legal_basis_index="",
        legal_consequence_if_missing="",
        applicable_if="始终适用",
        matched_terms=[],
        coverage_status="通过",
        issue_type="通过",
        evidence_clauses=[{"text": "每月5日前支付租金。"}],
        evidence_location="测试条款",
        reasoning_summary="测试",
        fact_dependencies=["rent.payment_due_day"],
        decision_trace={"fact_conflict": True},
    )

    confidence = _system_confidence_for_item(item)
    assert confidence["fact_confidence"] == "low"
    assert confidence["legal_confidence"] == "not_applicable"
    assert "fact" in confidence["confidence_bundle"]["limiting_factors"]


def test_claim_level_scope_no_death_or_repair_citation_propagation():
    output = review_contract_v2(LEASE_TEXT, "house_lease", use_llm=False)
    by_id = _by_id(output)

    hl007_claims = by_id["HL-007"]["legal_references"]
    hl008_claims = by_id["HL-008"]["legal_references"]
    hl037_claims = by_id["HL-037"]["legal_references"]

    assert any(claim["article"] == "第732条" and claim["support_type"] == "DIRECT_SUPPORT" and claim["support_scope"] for claim in hl007_claims)
    for item in output["items"]:
        for claim in item["legal_references"]:
            if claim["support_type"] == "DIRECT_SUPPORT":
                assert claim["authority"]
                assert claim["support_scope"]
    assert all(claim["article"] != "第732条" for claim in hl008_claims)
    assert all(not claim["authority_links"] for claim in hl008_claims)
    assert all(claim["article"] != "第585条" for claim in hl037_claims)


def test_30_day_notice_is_drafting_choice_not_statutory_requirement():
    output = review_contract_v2(LEASE_TEXT, "house_lease", use_llm=False)
    hl013_claims = _by_id(output)["HL-013"]["legal_references"]

    assert any(claim["article"] == "第730条" and "合理期限" in claim["support_scope"] for claim in hl013_claims)
    drafting = [claim for claim in hl013_claims if claim["claim_type"] == "DRAFTING_RECOMMENDATION"]
    assert drafting and all(not claim["authority_links"] for claim in drafting)
    assert "法定30" not in output["result"]
    assert "强制30" not in output["result"]


def test_narrative_state_invariant_and_debug_reports():
    output = review_contract_v2(LEASE_TEXT, "house_lease", use_llm=False)

    assert len(output["observability"]["confidence_debug_report"]) == 50
    assert output["observability"]["legal_claim_debug_report"]
    assert all(row["status"] == "PASS" for row in output["observability"]["narrative_state_debug_report"])
    assert "系统确定性" not in output["result"]
    assert "判断可靠度" in output["result"]
    for item in output["items"]:
        if item["coverage_status"] == "缺失":
            detail = output["result"].split(f"（{item['item_id']}）", 1)
            if len(detail) > 1:
                section = detail[1].split("---", 1)[0]
                assert "已出现" not in section
                assert "尚未完整覆盖" not in section


def test_no_forced_confidence_distribution_and_non_rental_fact_confidence():
    lease = review_contract_v2(LEASE_TEXT, "house_lease", use_llm=False)
    sale = review_contract_v2(
        "买卖合同。标的物为水泥，价款10000元，交货后7日内验收，质量不合格的出卖人负责更换。",
        "sale",
        use_llm=False,
    )
    levels = [item["system_confidence"]["level"] for item in lease["items"]]

    assert len(set(levels)) <= 3
    assert not (levels.count("high") == 15 and levels.count("medium") == 20 and levels.count("low") == 15)
    assert any(item["system_confidence"]["level"] in {"high", "medium"} for item in sale["items"])
    assert "confidence_metrics" in lease["benchmark_metrics"]
