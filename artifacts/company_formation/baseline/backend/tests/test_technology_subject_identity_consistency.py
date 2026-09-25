"""Asset identity consumes source-backed fields, not incidental delivery terms."""
from copy import deepcopy
from dataclasses import replace
from pathlib import Path

import pytest

from layers.input_layer import InputLayer
from review_v2 import engine
from review_v2.clause_parser import ParsedClause, parse_contract_clauses
from review_v2.contract_facts import extract_contract_fact_graph, resolve_patent_subject_identity
from review_v2.user_profile import UserRiskProfile


ROOT = Path(__file__).resolve().parents[2]


def fixture_text(number):
    return InputLayer()._extract_from_docx_content(next((ROOT / "test_data").glob(f"{number}*.docx")).read_bytes())


@pytest.fixture(scope="module")
def current():
    return engine.review_contract_v2(fixture_text(45), "technology", use_llm=False,
                                    profile=UserRiskProfile(user_identity="甲方/受让方"))


def subject(result):
    return next(row for row in result["items"] if row["item_id"] == "TC-01-03")


def assert_consistent_identity(result):
    item = subject(result)
    assert item["coverage_status"] == "通过"
    assert item["coverage_presence"] == "PRESENT"
    assert {row["status"] for row in item["coverage_elements"]} == {"COVERED"}
    assert item["narrative_state"]["missing_elements"] == []
    assert item["narrative_state"]["partial_elements"] == []
    assert not item["narrative_state"]["finding_exists"]
    assert item["decision_trace"]["recommendation_display_state"]["user_message"] == "已覆盖，无需修改。"
    assert not any("TC-01-03" in row["source_rule_ids"] for row in result["risk_themes"])
    evidence_ids = {row.get("evidence_id") or row["clause_id"] for row in item["evidence_clauses"]}
    for element in item["coverage_elements"]:
        assert element["evidence_ids"] and set(element["evidence_ids"]) <= evidence_ids
    assert not item["decision_trace"].get("specialized_search_audit")
    assert result["release_quality_gate"]["gate_results"]["PARTIAL_ELEMENT_NARRATIVE_GATE"] == "PASS"


def test_current_application_identity_uses_basic_information_and_definition(current):
    assert_consistent_identity(current)
    item = subject(current)
    rows = item["evidence_clauses"]
    assert rows[0]["location"] == "第十七条第1项"
    assert {"全文", "第一条第3项", "第一条第4项", "第一条第5项"} <= {row["location"] for row in rows}
    assert not any("支付" in row["quote"] or "第三方" in row["quote"] for row in rows)
    assert all(row["supporting_element_ids"] == ["technology_subject_identity"] for row in rows)
    assert any("全部申请权利" in row["quote"] for row in rows)
    assert item["narrative_state"]["judgment"].count("202511234567.8") == 1
    # Identity sufficiency does not fabricate independent ownership proof.
    proof = next(row for row in current["items"] if row["item_id"] == "TC-13-02")
    assert proof["coverage_status"] == "部分覆盖"


@pytest.mark.parametrize("stale_status", ["部分覆盖", "缺失"])
def test_direct_identity_overrides_stale_semantic_absence(monkeypatch, current, stale_status):
    original = engine.judge_checkpoints_with_llm

    def wrong_semantic_result(checkpoints, clauses, **kwargs):
        results = original(checkpoints, clauses, **{**kwargs, "use_llm": False})
        if "TC-01-03" in results:
            incidental = next(row for row in clauses if "具体支付方式" in row.text)
            results["TC-01-03"] = replace(
                results["TC-01-03"], coverage_status=stale_status, risk_level="高",
                status="缺失或不明确", issue_type="完全缺失", judge_source="llm_semantic",
                reasoning_summary="技术标的无法直接识别。", risk_point_description="技术标的身份尚未覆盖。",
                evidence_clauses=[incidental.to_public_dict()], evidence_location=incidental.location,
            )
        return results

    monkeypatch.setattr(engine, "judge_checkpoints_with_llm", wrong_semantic_result)
    result = engine.review_contract_v2(fixture_text(45), "technology", use_llm=False,
                                       profile=UserRiskProfile(user_identity="甲方/受让方"))
    assert_consistent_identity(result)
    assert result["risk_theme_summary"] == current["risk_theme_summary"]
    assert result["risk_theme_severity_summary"] == current["risk_theme_severity_summary"]


@pytest.mark.parametrize("number", [27, 43, 44])
def test_patent_license_granted_transfer_and_application_transfer(number):
    result = engine.review_contract_v2(fixture_text(number), "technology", use_llm=False)
    assert_consistent_identity(result)
    assert result["release_quality_gate"]["status"] == "REPORT_READY"


@pytest.mark.parametrize("number", [26, 38, 41])
def test_secret_transactions_do_not_acquire_patent_identifier_requirements(number):
    result = engine.review_contract_v2(fixture_text(number), "technology", use_llm=False)
    item = subject(result)
    assert item["coverage_status"] == "通过"
    assert not item["decision_trace"].get("shared_patent_identity_facts")
    assert not any("TC-01-03" in row["source_rule_ids"] for row in result["risk_themes"])


def graph_for(*texts):
    return extract_contract_fact_graph([
        ParsedClause(f"S-{index}", f"第{index}条", "", text, "正式合同条款", 1)
        for index, text in enumerate(texts, 1)
    ])


@pytest.mark.parametrize("name_label", ["专利名称", "发明名称", "发明创造名称", "项目名称"])
@pytest.mark.parametrize("number_label", ["专利号", "专利编号", "专利申请号", "申请号"])
def test_name_and_unique_identifier_are_sufficient_without_grant_proof(name_label, number_label):
    graph = graph_for(f"{name_label}：柔性传感装置", f"{number_label}：202410987654.3")
    identity = resolve_patent_subject_identity(graph)
    assert identity["satisfied"]
    assert identity["asset_count"] == 1
    assert all(fact.source_clause_ids and fact.source_spans for fact in identity["facts"])
    assert not graph.facts.get("technology.patent.authorization_date")


@pytest.mark.parametrize("texts", [
    ("项目名称：____", "专利申请号：202410987654.3"),
    ("发明名称：柔性传感装置", "专利申请号：________"),
    ("付款后交付技术资料，承担第三方责任。",),
    ("项目名称：柔性传感装置", "参考申请号：202410987654.3、申请号：202420123456.1"),
    ("发明名称：柔性传感装置", "发明名称：光学识别装置", "申请号：202410987654.3"),
])
def test_incomplete_or_unassociated_facts_are_not_promoted_to_identity(texts):
    assert not resolve_patent_subject_identity(graph_for(*texts))["satisfied"]


def test_multiple_assets_require_individual_name_identifier_pairs():
    identity = resolve_patent_subject_identity(graph_for(
        "发明名称：柔性传感装置；申请号：202410987654.3",
        "发明名称：光学识别装置；申请号：202420123456.1",
    ))
    assert identity["satisfied"] and identity["asset_count"] == 2


def test_applicant_remains_distinct_from_granted_patent_owner():
    graph = graph_for("项目名称：柔性传感装置", "专利申请号：202410987654.3", "专利申请人：示例研发有限公司")
    assert graph.facts["technology.patent.applicant"][0].value == "示例研发有限公司"
    assert not graph.facts.get("technology.patent.owner")


def test_unbound_structured_fields_cannot_create_coverage(current):
    item = engine.ReviewItemResult(**deepcopy(subject(current)))
    item.coverage_status = "缺失"
    graph = graph_for("项目名称：柔性传感装置", "申请号：202410987654.3")
    # Facts from another parsed document must not bind to the current document.
    engine._apply_patent_subject_identity([item], parse_contract_clauses("第一条 本次转让费用支付。"),
                                        {"tertiary_subtype": "PATENT_APPLICATION_RIGHT_TRANSFER"}, graph)
    assert item.coverage_status == "缺失"
