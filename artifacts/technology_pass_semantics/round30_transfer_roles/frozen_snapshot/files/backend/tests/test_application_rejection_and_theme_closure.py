"""Rejection is application-specific; aggregate prose follows adverse elements."""
from pathlib import Path
from dataclasses import fields
from copy import deepcopy

import pytest

from layers.input_layer import InputLayer
from review_v2 import engine
from review_v2.technology_patent_transfer_analysis import extract_application_rejection_facts
from review_v2.user_profile import UserRiskProfile


@pytest.fixture(scope="module")
def current():
    path = next((Path(__file__).resolve().parents[2] / "test_data").glob("45*.docx"))
    text = InputLayer()._extract_from_docx_content(path.read_bytes())
    return engine.review_contract_v2(text, "technology", use_llm=False,
                                     profile=UserRiskProfile(user_identity="甲方/受让方"))


def get_item(result, key):
    return next(row for row in result["items"] if row["item_id"] == key)


def theme(result, key):
    return next(row for row in result["risk_themes"] if key in row["source_rule_ids"])


def test_rejection_risk_has_its_own_complete_evidence_and_action(current):
    row = get_item(current, "TECH-SHARED-APP-REJECTION-01")
    assert row["risk_severity"] == "MEDIUM"
    assert theme(current, row["item_id"])["final_action"] == "SHOULD_CHANGE"
    facts = row["decision_trace"]["application_rejection_facts"]
    assert all(facts[key] for key in (
        "application_rejection_trigger", "rejection_paid_fees_nonrefundable", "rejection_unpaid_fees_continue",
        "rejection_termination_prohibited", "rejection_narrow_fault_exception", "rejection_concealment_refund",
    ))
    assert not facts.get("rejection_differentiated_outcomes")
    assert not facts.get("rejection_independent_value_settlement")
    assert not facts.get("rejection_concealment_damages")
    assert not facts.get("rejection_termination_right")
    elements = {e["element_id"]: e for e in row["coverage_elements"]}
    assert elements["rejection_termination_right"]["status"] == "ADVERSE"
    for e in elements.values():
        if e["status"] != "MISSING":
            assert e["evidence_ids"] and e["supporting_evidence"]
    assert "已履行部分不预设一律退款" in theme(current, row["item_id"])["recommendation"]


def test_coownership_is_not_ownership_transfer_in_any_report_projection(current):
    row = theme(current, "TC-10-04")
    expected = "后续改进成果共有、处分限制与无偿使用的不对等安排"
    assert row["title"] == row["canonical_title"] == expected
    assert row["severity"] == "MEDIUM" and row["final_action"] == "SHOULD_CHANGE"
    assert "无偿转归" not in row["recommendation"]
    assert all(term in row["recommendation"] for term in ("共有", "权利比例", "处分", "对价", "永久免费"))
    assert "改进成果无偿转归及权利限制" not in current["result"]
    assert "删除独立改进成果无偿转归" not in current["result"]
    assert len([row for row in current["risk_themes"] if "TC-10-04" in row["source_rule_ids"]]) == 1
    for key in ("TC-10-01", "TC-10-02", "TC-10-04"):
        item = get_item(current, key)
        assert item["risk_severity"] == "MEDIUM"
        assert item["decision_trace"]["final_fact_severity_refresh"]["source"] == "FINAL_ELEMENT_STATES"


def test_competition_narrative_consumes_all_three_adverse_facts(current):
    row = get_item(current, "TC-02-01")
    for text in (row["risk_point_description"], row["narrative_state"]["judgment"], theme(current, row["item_id"])["issue"]):
        assert "自行研发" in text
        assert "竞争来源" in text and "购买" in text
        assert "终止后" in text and "5年" in text
    statuses = {e["element_id"]: e["status"] for e in row["coverage_elements"]}
    for key in ("independent_competing_research_restriction", "external_competing_technology_access_restriction", "post_termination_competition_restriction"):
        assert statuses[key] == "ADVERSE"


def test_previous_facts_gate_and_counts_are_preserved(current):
    assert current["release_quality_gate"]["status"] == "REPORT_READY", current["release_quality_gate"]["failures"]
    assert get_item(current, "TC-01-03")["coverage_status"] == "通过"
    assert get_item(current, "TC-12-01")["coverage_status"] == "风险条款"
    claim = {e["element_id"]: e for e in get_item(current, "TC-12-02")["coverage_elements"]}
    assert claim["defense_cost_allocation"]["direction"] == "ADVERSE"
    assert claim["notification_deadline"]["status"] == "MISSING"
    assert all(term in get_item(current, "GEN-PAY-01")["risk_point_description"] for term in ("110%", "3,300,000", "300,000"))
    penalty = get_item(current, "GEN-LIAB-03")
    assert "500万元" in penalty["risk_point_description"] and "0.5%" in penalty["risk_point_description"]
    finding = next(row for row in current["risk_findings"] if "GEN-LIAB-03" in row["source_review_ids"])
    assert finding["economic_impact"]["percentage_of_contract"] == pytest.approx(166.6666667)
    assert current["risk_theme_summary"]["total"] == len(current["risk_themes"])


@pytest.mark.parametrize("scope", ["全部", "部分", "全部或部分"])
def test_rejection_keeps_all_actual_payment_limbs(scope):
    text = f"第八条 专利申请被驳回\n专利申请被{scope}驳回时，已经支付的价款不予退还；尚未支付的价款仍应继续支付；受让方不得解除合同。"
    clauses = engine._operative_technology_clauses(text)
    facts = extract_application_rejection_facts(clauses)
    assert facts["rejection_unpaid_fees_continue"] and facts["rejection_termination_prohibited"]
    assert all(source["quote"] in text for rows in facts.values() for source in rows)


@pytest.mark.parametrize("text", [
    "第八条 专利权全部被宣告无效，尚未支付的转让费继续支付。",
    "第八条 技术资料验收申请被驳回，尚未支付的价款继续支付。",
    "第八条 申请材料交付。专利申请文件已提供。第九条 退款申请被驳回后仍支付服务费。",
    "第八条 专利申请未被驳回，尚未支付的价款继续支付。",
])
def test_other_events_cannot_trigger_application_rejection(text):
    items = []
    engine._apply_application_rejection_review(items, engine._operative_technology_clauses(text))
    assert not items


@pytest.mark.parametrize("arrangement", [
    "已经支付的价款不退。",
    "受让方有权解除合同，尚未支付的价款无需继续支付。",
    "全部驳回则解除，部分驳回按剩余权利价值比例结算。技术资料的独立价值单独结算。",
])
def test_no_adverse_exit_or_future_payment_does_not_manufacture_risk(arrangement):
    clauses = engine._operative_technology_clauses("第八条 专利申请被驳回\n专利申请被驳回时，" + arrangement)
    items = []
    engine._apply_application_rejection_review(items, clauses)
    assert not items


def test_warranty_current_rejection_status_is_not_future_payment_policy():
    clauses = engine._operative_technology_clauses("第六条 申请状态\n本专利申请未被驳回。\n第七条 付款\n受让方继续支付技术服务价款。")
    items = []
    engine._apply_application_rejection_review(items, clauses)
    assert not items


def test_compound_advice_and_narrative_share_facts_without_rule_id_branch(current):
    source = deepcopy(get_item(current, "TC-02-01"))
    row = engine.ReviewItemResult(**{field.name: source[field.name] for field in fields(engine.ReviewItemResult) if field.name in source})
    row.item_id = "SYNTHETIC-ADVERSE-COMPOUND"
    raw = deepcopy(next(f for f in current["risk_findings"] if "TC-02-01" in f["source_review_ids"]))
    finding = engine.RiskFinding(**{field.name: raw[field.name] for field in fields(engine.RiskFinding) if field.name in raw})
    finding.source_review_ids = [row.item_id]
    finding.issue = "对竞争技术的限制在合同终止后继续有效5年。"
    engine._complete_adverse_finding_recommendations([finding], [row])
    fragments = finding.aggregation_signals["adverse_recommendation_fragments"]
    assert len(fragments) == 3
    assert all(fragment["evidence_ids"] and fragment["proposition"] in finding.issue for fragment in fragments)
    assert "自主研发" in finding.recommendation and "采购" in finding.recommendation
