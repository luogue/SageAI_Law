from copy import deepcopy
from dataclasses import fields
from pathlib import Path
from types import SimpleNamespace

import pytest

from layers.input_layer import InputLayer
from review_v2 import engine
from review_v2.narrative_evidence import narrative_evidence_gate
from review_v2.technology_service_analysis import analyze_timeline
from review_v2.user_profile import UserRiskProfile


@pytest.fixture(scope="module")
def current():
    source = next((Path(__file__).resolve().parents[2] / "test_data").glob("45*.docx"))
    text = InputLayer()._extract_from_docx_content(source.read_bytes())
    return engine.review_contract_v2(text, "technology", use_llm=False,
                                     profile=UserRiskProfile(user_identity="甲方/受让方"))


def models(result):
    items = [engine.ReviewItemResult(**{f.name: row[f.name] for f in fields(engine.ReviewItemResult) if f.name in row})
             for row in deepcopy(result["items"])]
    findings = [engine.RiskFinding(**{f.name: row[f.name] for f in fields(engine.RiskFinding) if f.name in row})
                for row in deepcopy(result["risk_findings"])]
    return items, findings


def test_current_facts_publish_their_exact_sources(current):
    assert current["release_quality_gate"]["status"] == "REPORT_READY", current["release_quality_gate"]["failures"]
    assert current["narrative_evidence_gate"]["status"] == "REPORT_READY"
    for rule, marker in (("TC-11-02", "仅限本合同有效期内"), ("GEN-LIAB-03", "违反技术使用、转让或保密义务")):
        finding = next(f for f in current["risk_findings"] if rule in f["source_review_ids"])
        rows = [row for row in finding["evidence_bundle"]["items"] if marker in row.get("quoted_text", "")]
        assert rows and any(row.get("supporting_element_ids") for row in rows)


@pytest.mark.parametrize("marker", ["仅限本合同有效期内", "违反技术使用、转让或保密义务"])
def test_removing_one_material_source_blocks_not_rescued_by_other_clauses(current, marker):
    items, findings = models(current)
    for finding in findings:
        finding.evidence_bundle["items"] = [row for row in finding.evidence_bundle.get("items", [])
                                            if marker not in row.get("quoted_text", "")]
    gate = narrative_evidence_gate(items, findings)
    assert gate["status"] == "BLOCKED"
    assert gate["failures"][0]["requirement"] == "NARRATIVE_EVIDENCE_GATE"


@pytest.mark.parametrize("field", ["risk_point_description", "reasoning_summary", "narrative_state", "finding_issue"])
def test_invented_material_fact_in_any_projection_blocks(current, field):
    items, findings = models(current)
    item = next(row for row in items if row.item_id == "GEN-LIAB-03")
    invented = "买方违反设备采购义务时，应支付700万元违约金。"
    if field == "narrative_state":
        item.narrative_state["judgment"] += invented
    elif field == "finding_issue":
        next(row for row in findings if item.item_id in row.source_review_ids).issue += invented
    else:
        setattr(item, field, getattr(item, field) + invented)
    assert narrative_evidence_gate(items, findings)["status"] == "BLOCKED"


def test_gate_is_element_generic_not_rule_id_specific():
    item = SimpleNamespace(item_id="UNRELATED-RULE", coverage_elements=[{
        "element_id": "arbitrary_obligation", "status": "ADVERSE", "proposition": "一方承担责任",
        "supporting_evidence": [{"clause_id": "c1", "quote": "一方承担责任"}],
    }], risk_point_description="一方承担责任", reasoning_summary="", narrative_state={})
    finding = SimpleNamespace(finding_id="f1", source_review_ids=[item.item_id], issue=item.risk_point_description,
                              evidence_bundle={"items": []})
    assert narrative_evidence_gate([item], [finding])["status"] == "BLOCKED"


def test_renderer_cannot_add_any_unregistered_independent_fact(current):
    items, findings = models(current)
    report = current["result"] + "\n- 风险说明：受让方必须将全部客户移交让与方。\n"
    assert narrative_evidence_gate(items, findings, report)["status"] == "BLOCKED"


def test_same_amount_with_an_invented_trigger_is_not_supported(current):
    items, findings = models(current)
    finding = next(f for f in findings if "GEN-LIAB-03" in f.source_review_ids)
    finding.issue += "买方违反设备采购义务时，应支付500万元违约金。"
    assert narrative_evidence_gate(items, findings)["status"] == "BLOCKED"


def test_time_narrative_cannot_replace_validity_with_performance(current):
    items, findings = models(current)
    finding = next(f for f in findings if "TECH-SHARED-03" in f.source_review_ids)
    finding.issue = "履行义务早于合同生效日。"
    assert narrative_evidence_gate(items, findings)["status"] == "BLOCKED"


def test_four_dates_are_not_aliases():
    text = "有效期限：2026年10月10日至2034年10月9日\n签署日期：2026年10月20日\n本合同自专利申请权转让登记之日起生效。"
    timeline = analyze_timeline(text)
    assert timeline["validity_start_date"] == "2026-10-10"
    assert timeline["signing_date"] == "2026-10-20"
    assert timeline["effective_date"] is None
    assert timeline["performance_start_date"] is None
    assert timeline["service_end_date"] is None
    assert timeline["effective_date_basis"] == "REGISTRATION_CONDITION"
    assert timeline["conflict_types"] == ["VALIDITY_BEFORE_SIGNING"]


def test_explicit_performance_and_effective_date_remain_distinct():
    timeline = analyze_timeline("有效期限：2026年10月10日至2034年10月9日\n签署日期：2026年10月20日\n"
                                "服务期限：2026年11月1日至2027年11月1日\n合同生效日期：2026年10月25日。")
    assert timeline["performance_start_date"] == "2026-11-01"
    assert timeline["effective_date"] == "2026-10-25"
    assert timeline["signing_date"] == "2026-10-20"
    assert timeline["validity_start_date"] == "2026-10-10"


def test_signing_is_effective_only_with_direct_condition():
    assert analyze_timeline("签署日期：2026年10月20日")["effective_date"] is None
    assert analyze_timeline("签署日期：2026年10月20日\n本合同自双方签字盖章之日起生效。")["effective_date"] == "2026-10-20"


def test_current_timeline_has_no_invented_performance_or_effect(current):
    row = next(row for row in current["items"] if row["item_id"] == "TECH-SHARED-03")
    assert "有效期限起始日早于签署日" in row["risk_point_description"]
    assert "履行义务早于合同生效日" not in current["result"]
    finding = next(f for f in current["risk_findings"] if row["item_id"] in f["source_review_ids"])
    assert "validity_start_date" in finding["evidence_bundle"]["covered_fact_types"]
    assert "performance_start_date" not in finding["evidence_bundle"]["covered_fact_types"]
