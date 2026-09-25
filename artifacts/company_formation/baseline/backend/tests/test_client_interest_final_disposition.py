from __future__ import annotations

import re
from types import SimpleNamespace

from review_v2.engine import (
    DISPOSITION_MUST_CHANGE,
    DISPOSITION_OPTIONAL_IMPROVEMENT,
    DISPOSITION_SHOULD_CHANGE,
    NOT_RECOMMENDED_TO_SIGN,
    PROFESSIONAL_REVIEW_RECOMMENDED,
    SIGNABLE,
    SIGN_AFTER_MODIFICATION,
    SIGNABLE_WITH_OPTIONAL_IMPROVEMENTS,
    SIGNABLE_WITH_RECOMMENDED_IMPROVEMENTS,
    _build_signability_decision,
    review_contract_v2,
)
from review_v2.user_profile import UserRiskProfile


FRAMEWORK_SUPPLY_TEXT = (
    "长期供货合同。买方为甲方，卖方为乙方。双方建立两年长期供货合作，"
    "产品为工业端子和连接组件。买方每月发出书面采购订单，卖方确认后生效；"
    "本协议不约定最低采购数量，具体数量以买方实际下达并经卖方确认的订单为准。"
    "每月按照订单、送货单和实际收货数量对账结算。"
    "订单未另行约定时，卖方应在确认订单后七日内送货。"
    "买方无正当理由拒收的，应承担合理仓储费及二次运输费。"
    "一方侵害第三方合法权益的，由责任方负责处理、承担相应责任并赔偿损失。"
)


def _result(role: str):
    return review_contract_v2(
        FRAMEWORK_SUPPLY_TEXT,
        "sale",
        use_llm=False,
        profile=UserRiskProfile(user_identity=role),
    )


def _disposition_for_review(result: dict, review_id: str) -> dict:
    return next(
        row for row in result["final_dispositions"]
        if review_id in row["review_ids"]
    )


def _report_section(report: str, review_id: str) -> str:
    marker = f"（{review_id}）"
    if marker not in report:
        return ""
    section = report.split(marker, 1)[1]
    return section.split("\n## ", 1)[0]


def test_client_interest_mutation_changes_buyer_delay_acceptance_disposition():
    buyer = _result("买方 / 需方")
    seller = _result("卖方 / 供方")

    buyer_s0404 = _disposition_for_review(buyer, "S-04-04")
    seller_s0404 = _disposition_for_review(seller, "S-04-04")

    assert buyer["perspective_resolution"]["canonical_role"] == "BUYER"
    assert seller["perspective_resolution"]["canonical_role"] == "SELLER"
    assert buyer_s0404["client_effect"] == "ADVERSE"
    assert buyer_s0404["final_action"] in {"KEEP_CURRENT", "DO_NOT_ADD"}
    assert seller_s0404["final_action"] in {"SHOULD_CHANGE", "OPTIONAL_IMPROVEMENT", "MUST_CHANGE"}
    assert buyer_s0404["final_action"] != seller_s0404["final_action"]


def test_buyer_adverse_recommendation_blocked_but_ip_protection_retained():
    result = _result("买方 / 需方")
    s0404 = _disposition_for_review(result, "S-04-04")
    s1102 = _disposition_for_review(result, "S-11-02")

    assert result["client_interest_gate"]["gate_results"]["CLIENT_INTEREST_GATE"] == "PASS"
    assert s0404["blocked_recommendation_ids"]
    assert s0404["include_in_priority_changes"] is False
    assert s1102["final_action"] == "SHOULD_CHANGE"
    assert s1102["include_in_priority_changes"] is True


def test_risk_statistics_and_report_sections_use_final_disposition_single_source():
    result = _result("买方 / 需方")
    summary = result["final_disposition_summary"]
    gate = result["final_disposition_invariant_gate"]

    assert result["release_quality_gate"]["status"] == "REPORT_READY"
    assert gate["gate_results"]["RISK_STATISTICS_INVARIANT"] == "PASS"
    assert gate["gate_results"]["FINAL_DISPOSITION_INVARIANT"] == "PASS"
    assert gate["gate_results"]["FORMAL_RECOMMENDATION_FINAL_DISPOSITION_INVARIANT"] == "PASS"
    assert gate["gate_results"]["RECOMMENDATION_OWNERSHIP_INVARIANT"] == "PASS"
    assert summary["total"] == len(result["final_dispositions"])
    assert (
        summary["must_change"]
        + summary["should_change"]
        + summary["optional_improvement"]
        + summary["keep_current"]
        + summary["do_not_add"]
        + summary["manual_review"]
    ) == summary["total"]
    assert f"已识别但建议保持现状数：{summary['protected_no_change']}" in result["result"]


def test_pass_review_not_polluted_by_linked_risk_and_basis_evidence_are_clean():
    result = _result("买方 / 需方")
    items = {item["item_id"]: item for item in result["items"]}
    report = result["result"]

    if "S-11-04" in items and items["S-11-04"]["coverage_status"] == "通过":
        state = items["S-11-04"]["decision_trace"]["recommendation_display_state"]
        section = _report_section(report, "S-11-04")
        assert items["S-11-04"]["action_priority"] == "NONE"
        assert "无需修改" in items["S-11-04"]["action_suggestion"]
        assert state["formal_recommendations"] == []
        assert state["recommendation_owners"] == ["RISK"]
        assert "【正式建议】" not in section

    assert "法律依据】：合同管理实务建议" not in report
    assert "未召回正式条款" not in report
    assert "”对应的核心安排" not in report
    assert "当前未匹配到足够直接的现行具体条文" not in report
    assert "合同正文及附件中未找到对应约定；未在合同正文及附件中定位到对应安排" not in report
    assert "最终动作：" not in report
    assert "合同已明确约定合同已约定" not in report
    assert "合同已明确约定已明确约定" not in report
    assert "缺失：缺失：" not in report
    assert "已覆盖：已覆盖：" not in report
    assert "建议建议" not in report
    assert "无无需" not in report
    assert "。。" not in report
    assert "；；" not in report
    assert result["report_text_validation_gate"]["broken_template_text_count"] == 0
    evidence_statuses = {
        item.get("citation", {}).get("evidence_status")
        for item in result["items"]
        if item.get("citation")
    }
    assert "NOT_FOUND" not in evidence_statuses
    assert evidence_statuses & {"NO_SUPPORTING_CLAUSE", "NO_ADVERSE_CLAUSE_FOUND", "FOUND_SUPPORTING_CLAUSE"}


def test_risk_owned_recommendations_are_not_review_detail_formal_recommendations():
    result = _result("买方 / 需方")
    risk_owned = [
        row for row in result["final_dispositions"]
        if row["risk_id"] == "RF-GOODS-RIGHTS-001"
    ]

    assert risk_owned
    assert all(row["recommendation_owner"] == "RISK" for row in risk_owned)
    assert all(row["formal_recommendation"] is None for row in risk_owned)
    assert result["recommendation_cross_renderer_consistency_gate"]["gate_results"][
        "RECOMMENDATION_CROSS_RENDERER_CONSISTENCY_GATE"
    ] == "PASS"


def test_uncertain_applicability_becomes_insufficient_context_not_not_applicable():
    result = _result("买方 / 需方")
    items = {item["item_id"]: item for item in result["items"]}

    assert items["S-00-07"]["coverage_status"] == "INSUFFICIENT_CONTEXT"
    assert items["S-00-07"]["needs_manual_review"] is True
    assert items["S-00-07"]["applicability"]["status"] == "INSUFFICIENT_CONTEXT"
    assert "人工复核" in items["S-00-07"]["action_suggestion"]

    assert items["S-12-03"]["coverage_status"] == "不适用"
    assert items["S-12-03"]["needs_manual_review"] is False


def test_manual_review_count_and_section_use_same_source():
    result = _result("买方 / 需方")
    report = result["result"]
    manual_items = result["manual_review_items"]
    manual_section = report.split("人工复核事项", 1)[1].split("---", 1)[0]

    assert result["manual_review_summary"]["manual_review_count"] == len(manual_items) == 1
    assert result["overall_assessment"]["manual_review_count"] == len(manual_items)
    assert f"人工复核项：{len(manual_items)}" in report
    assert manual_section.count("S-00-07") == len(manual_items)


def test_low_materiality_manual_review_does_not_block_signability():
    result = _result("买方 / 需方")

    assert result["overall_assessment"]["signability_decision"]["level"] == SIGN_AFTER_MODIFICATION
    assert result["overall_assessment"]["signability"] == "建议修改后签署"
    assert result["manual_review_items"][0]["materiality"] in {"LOW", "MEDIUM"}
    assert result["overall_assessment"]["signability_decision"]["blocking_manual_review_item_ids"] == []


def test_high_materiality_manual_review_escalates_signability():
    decision = _build_signability_decision(
        findings=[],
        dispositions=[SimpleNamespace(final_action=DISPOSITION_SHOULD_CHANGE)],
        manual_review_records=[
            {
                "item_id": "AUTH-01",
                "title": "签字人授权真实性",
                "reason": "主体授权真实性无法确认。",
                "materiality": "HIGH",
                "blocking_signability": True,
            }
        ],
    )

    assert decision.level == PROFESSIONAL_REVIEW_RECOMMENDED
    assert decision.label == "建议专业法律复核后决定"
    assert decision.blocking_manual_review_item_ids == ["AUTH-01"]


def _signability_finding(*, severity: str, priority: str = "B_PRACTICAL", title: str = "合同风险"):
    return SimpleNamespace(
        finding_id=f"RF-{severity}-{priority}",
        priority=priority,
        severity=severity,
        needs_manual_review=False,
        confidence={"level": "high"},
        risk_group="contract_term_risk",
        title=title,
    )


def test_low_risk_should_change_is_recommended_improvement_not_signing_blocker():
    finding = _signability_finding(severity="LOW")
    decision = _build_signability_decision(
        findings=[finding],
        dispositions=[SimpleNamespace(final_action=DISPOSITION_SHOULD_CHANGE)],
        manual_review_records=[],
    )

    assert decision.level == SIGNABLE_WITH_RECOMMENDED_IMPROVEMENTS
    assert decision.label == "可以签署，建议进一步完善"


def test_optional_only_contract_remains_signable_with_optional_improvements():
    finding = _signability_finding(severity="LOW", priority="C_OPTIMIZATION")
    decision = _build_signability_decision(
        findings=[finding],
        dispositions=[SimpleNamespace(final_action=DISPOSITION_OPTIONAL_IMPROVEMENT)],
        manual_review_records=[],
    )

    assert decision.level == SIGNABLE_WITH_OPTIONAL_IMPROVEMENTS
    assert decision.label == "可以签署，可进一步优化"


def test_medium_risk_or_must_change_still_requires_modification_before_signing():
    medium = _signability_finding(severity="MEDIUM")
    medium_decision = _build_signability_decision(
        findings=[medium],
        dispositions=[SimpleNamespace(final_action=DISPOSITION_SHOULD_CHANGE)],
        manual_review_records=[],
    )
    low_must = _signability_finding(severity="LOW")
    must_decision = _build_signability_decision(
        findings=[low_must],
        dispositions=[SimpleNamespace(final_action=DISPOSITION_MUST_CHANGE)],
        manual_review_records=[],
    )

    assert medium_decision.level == SIGN_AFTER_MODIFICATION
    assert must_decision.level == SIGN_AFTER_MODIFICATION


def test_critical_validity_obstacle_remains_not_recommended_to_sign():
    finding = _signability_finding(
        severity="CRITICAL",
        priority="A_CORE",
        title="合同效力存在重大障碍",
    )
    decision = _build_signability_decision(
        findings=[finding],
        dispositions=[SimpleNamespace(final_action=DISPOSITION_MUST_CHANGE)],
        manual_review_records=[],
    )

    assert decision.level == NOT_RECOMMENDED_TO_SIGN
    assert decision.label == "当前不建议签署"


def test_no_risk_contract_remains_signable():
    decision = _build_signability_decision(
        findings=[],
        dispositions=[],
        manual_review_records=[],
    )

    assert decision.level == SIGNABLE
    assert decision.label == "可以签署"


def test_not_applicable_report_has_no_always_applicable_contradiction():
    result = _result("买方 / 需方")
    report = result["result"]

    assert not re.search(r"覆盖状态：不适用[\s\S]{0,240}【适用条件】：始终适用", report)
    assert "合同已明确约定合同" not in report
    assert "已明确约定合同已" not in report
    assert "合同已约定合同" not in report
    assert "已经明确已经" not in report
