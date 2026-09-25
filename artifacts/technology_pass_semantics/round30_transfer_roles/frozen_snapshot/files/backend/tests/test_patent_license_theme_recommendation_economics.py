"""Final theme naming, compound adverse advice and monetary exposure stay factual."""
from copy import deepcopy
from pathlib import Path
import re
from types import SimpleNamespace

import pytest

from layers.input_layer import InputLayer
from review_v2.engine import (
    _adverse_element_recommendation_fragments, _assess_structured_economic_exposure,
    _evidence_constrained_recommendation, _exact_element_report_invariants,
    _user_visible_risk_themes, review_contract_v2,
)
from review_v2.user_profile import UserRiskProfile


@pytest.fixture(scope="module")
def result():
    path = next((Path(__file__).resolve().parents[2] / "test_data").glob("27*.docx"))
    text = InputLayer()._extract_from_docx_content(path.read_bytes())
    return review_contract_v2(text, "technology", use_llm=False, include_low_risk=True,
                              profile=UserRiskProfile(user_identity="甲方/被许可方"))


def review(result, key):
    return next(row for row in result["items"] if row["item_id"] == key)


def risk(result, key):
    return next(row for row in result["risk_findings"] if key in row["source_review_ids"])


def test_same_contract_baseline_counts_and_release_gate(result):
    assert result["risk_theme_count"] == 23
    assert result["rule_level_finding_count"] == 26
    assert result["risk_theme_severity_summary"] == {"major": 8, "medium": 9, "low": 6}
    assert result["final_overview_summary"] == {
        "major_risk": 8, "medium_risk": 9, "low_risk": 6, "priority_action": 7,
        "recommended_action": 10, "optional_action": 5,
        "manual_review": len(result["manual_review_items"]),
    }
    assert result["final_disposition_summary"]["actionable"] == 17
    assert result["release_quality_gate"]["status"] == "REPORT_READY"
    assert result["release_quality_gate"]["failures"] == []


def test_all_theme_regions_use_the_canonical_title(result):
    themes = result["risk_themes"]
    by_id = {row["finding_id"]: row for row in result["risk_findings"]}
    report = result["result"]
    detail = report.split("完整风险主题明细（聚合后）", 1)[1].split("完整审查明细", 1)[0]
    headings = re.findall(r"^### (.+)$", detail, re.MULTILINE)
    assert headings == [row["canonical_title"] for row in themes]
    for theme in themes:
        assert theme["title"] == theme["canonical_title"]
        for member in theme["member_finding_ids"]:
            assert by_id[member]["canonical_title"] == theme["canonical_title"]
        if theme["final_action"] in {"MUST_CHANGE", "SHOULD_CHANGE"}:
            assert "对应风险主题：" + theme["canonical_title"] in report
    assert "### 被许可方独立改进成果被强制无偿转归许可方" not in detail
    assert "### 重大过失仍适用责任上限的效力风险" not in detail
    # The source rule name remains available, but does not replace the theme.
    assert review(result, "GEN-LIAB-02")["title"] == "重大过失仍适用责任上限的效力风险"


def test_canonical_name_does_not_follow_later_source_label_changes(result):
    finding = SimpleNamespace(**deepcopy(risk(result, "GEN-LIAB-02")))
    title = finding.canonical_title
    finding.title = "来源规则的显示名称变化"
    assert _user_visible_risk_themes([finding])[0]["canonical_title"] == title


def test_all_confirmed_competition_restrictions_have_recommendation_fragments(result):
    item = review(result, "TC-02-01")
    finding = risk(result, "TC-02-01")
    adverse_ids = {row["element_id"] for row in item["coverage_elements"] if row["status"] == "ADVERSE"}
    fragments = finding["aggregation_signals"]["adverse_recommendation_fragments"]
    assert {row["element_id"] for row in fragments} == adverse_ids
    theme = next(row for row in result["risk_themes"] if finding["finding_id"] in row["member_finding_ids"])
    texts = (item["suggested_clause_example"], finding["recommendation"], theme["recommendation"])
    for text in texts:
        assert all(term in text for term in ("自主研发", "采购竞争来源替代技术", "独立改进成果", "继续5年"))
        assert all(row["text"] in text for row in fragments)


@pytest.mark.parametrize("new_id,years", [("OTHER-REVIEW", 2), ("GENERIC-RESTRICTION", 7)])
def test_compound_advice_is_semantic_not_rule_id_or_fixed_duration(result, new_id, years):
    item = SimpleNamespace(**deepcopy(review(result, "TC-02-01")))
    item.item_id = new_id
    for source in item.evidence_clauses:
        source["text"] = source["text"].replace("继续有效5年", f"继续有效{years}年")
    item.coverage_elements.reverse()
    advice = _evidence_constrained_recommendation(item, "仅修改一个条款的旧模板")
    assert all(term in advice for term in ("自主研发", "采购竞争来源替代技术", "独立改进成果", f"继续{years}年"))
    assert "继续5年" not in advice


def test_removing_an_adverse_fact_removes_its_recommendation(result):
    item = SimpleNamespace(**deepcopy(review(result, "TC-02-01")))
    target = next(row for row in item.coverage_elements if row["element_id"] == "external_competing_technology_access_restriction")
    target.update(status="NOT_APPLICABLE", evidence_ids=[])
    advice = _evidence_constrained_recommendation(item, "旧模板")
    assert "采购竞争来源" not in advice
    assert "自主研发" in advice


def test_missing_one_material_adverse_action_fails_invariant(result):
    item = SimpleNamespace(**deepcopy(review(result, "TC-02-01")))
    finding = SimpleNamespace(**deepcopy(risk(result, "TC-02-01")))
    finding.recommendation = "建议仅删除改进成果无偿转归。"
    failures = _exact_element_report_invariants([item], [finding])
    assert {row["element_id"] for row in failures if row["reason"] == "ADVERSE_ELEMENT_RECOMMENDATION_OMITTED"} == {
        row["element_id"] for row in _adverse_element_recommendation_fragments(item)
    }


@pytest.mark.parametrize("amount,total,expected", [(5_000_000, 4_800_000, "high"), (600, 1000, "high"),
                                                   (200, 1000, "medium"), (10, 1000, "low"), (600, None, "medium")])
def test_fixed_penalty_ratio_is_consumed_without_fixture_thresholds(amount, total, expected):
    result = _assess_structured_economic_exposure([{"amount": amount, "source_text": "固定金额违约金"}], total, [])
    assert result["level"] == expected
    assert result["fixed_amount"] == amount
    assert result["ultimate_loss_quantified"] is False


@pytest.mark.parametrize("rate,cap,expected", [(0.5, None, "high"), (0.1, None, "medium"),
                                               (0.01, None, "low"), (0.5, 2, "low")])
def test_daily_rate_and_its_own_cap(rate, cap, expected):
    result = _assess_structured_economic_exposure(
        [{"rate_percent_per_day": rate, "bound_cumulative_cap_percent": cap}], 1000, [])
    assert result["level"] == expected
    assert result["computations"][0]["percentage_of_applicable_base"] == pytest.approx(min(rate * 30, cap) if cap is not None else rate * 30)
    assert result["computations"][0]["not_actual_loss_or_assumed_contract_total_base"] is True


def test_daily_cap_does_not_reduce_an_independent_fixed_penalty():
    result = _assess_structured_economic_exposure([
        {"rate_percent_per_day": 0.5, "bound_cumulative_cap_percent": 2}, {"amount": 800},
    ], 1000, [])
    assert result["level"] == "high"


@pytest.mark.parametrize("fact,expected", [("第三方赔偿及停产损失由当前审查方承担", "medium"),
                                            ("已支付开发费用不退还", "medium"),
                                            ("专利无效后继续支付未到期许可费", "medium"),
                                            ("当前审查方承担无限责任", "high")])
def test_unquantified_express_monetary_exposure_not_low(fact, expected):
    assert _assess_structured_economic_exposure([], None, [{"proposition": fact}])["level"] == expected


def test_no_fact_is_unknown_not_automatically_low():
    assert _assess_structured_economic_exposure([], None, [])["level"] == "unknown"


def test_economic_dimensions_are_consistent_without_severity_escalation(result):
    item = review(result, "GEN-LIAB-03")
    finding = risk(result, "GEN-LIAB-03")
    assert item["economic_impact"] == finding["economic_impact"]["level"] == "high"
    detail = finding["economic_impact"]
    assert detail["fixed_amount"] == detail["direct_amount"] == 5_000_000
    assert detail["fixed_amount_percentage_of_contract"] == pytest.approx(104.1666667)
    assert detail["has_direct_financial_exposure"] and detail["time_amplifying"]
    assert detail["max_daily_rate_percent"] == 0.5
    assert finding["severity"] == "MEDIUM"
    assert risk(result, "TC-12-01")["economic_impact"]["level"] in {"medium", "high"}
    assert risk(result, "TC-07-02")["economic_impact"]["level"] in {"medium", "high"}


def test_route_payment_and_partial_facts_do_not_regress(result):
    context = str(result["report_context"])
    assert "专利实施许可" in context and "委托开发" in context
    payment = review(result, "GEN-PAY-01")["reasoning_summary"]
    assert all(term in payment for term in ("110%", "120%", "5,460,000", "660,000"))
    material = review(result, "TC-13-01")
    method = next(row for row in material["coverage_elements"] if row["element_id"] == "delivery_method")
    assert method["status"] == "COVERED"
    assert "交付形式" not in material["suggested_clause_example"]
    assert "召回费用" not in review(result, "TC-12-01")["risk_point_description"]
