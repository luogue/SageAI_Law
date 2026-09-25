from collections import Counter
from copy import deepcopy
from pathlib import Path
from types import SimpleNamespace
from dataclasses import replace
import re
from docx import Document

import pytest

from review_v2.clause_parser import parse_contract_clauses
from review_v2.construction_coverage import PROFILES, extract, coverage_failures, supports
from review_v2.report_statistics import statistics_gate
from review_v2.engine import review_contract_v2

TEXT = "\n".join(p.text for p in Document(Path(__file__).resolve().parents[2] / "test_data/50 建设工程.docx").paragraphs if p.text.strip())
TARGETS = ("CE-12-02", "CE-12-03", "CE-12-04", "CE-13-01", "CE-11-03", "CE-13-03", "CE-13-04")


@pytest.fixture(scope="module")
def report():
    return review_contract_v2(TEXT, "construction", use_llm=False)


def test_all_52_statuses_and_manual_counts_close(report):
    assert len(report["items"]) == report["all_items_count"] == 52
    assert Counter(r["coverage_status"] for r in report["items"]) == report["coverage_summary"]
    assert sum(report["coverage_summary"].values()) == 52
    assert report["coverage_summary"]["待核验"] == 6
    assert report["coverage_summary"]["法律提示"] == 7
    assert report["manual_review_summary"]["manual_review_count"] == 6
    assert len(report["manual_review_items"]) == report["final_overview_summary"]["manual_review"] == 6
    assert statistics_gate(report)["status"] == "REPORT_READY"
    assert report["release_quality_gate"]["status"] == "REPORT_READY"


def test_http_response_schema_preserves_statistics_audit(report):
    from routers.review_v2 import ReviewV2Result
    response = ReviewV2Result(**report).model_dump()
    assert len(response["all_rule_statuses"]) == 52
    assert response["statistics_consistency_gate"]["status"] == "REPORT_READY"
    assert response["coverage_summary"] == report["coverage_summary"]


@pytest.mark.parametrize("key", TARGETS)
def test_epc_cross_clause_coverage(report, key):
    item = next(r for r in report["items"] if r["item_id"] == key)
    assert item["coverage_status"] in ({"通过", "部分覆盖"} if key == "CE-13-03" else {"通过"})
    assert item["evidence_clauses"]
    assert all(re.sub(r"\s+", "", r["text"]) in re.sub(r"\s+", "", TEXT) for r in item["evidence_clauses"])
    assert not coverage_failures([SimpleNamespace(**item)])


def test_consistency_pass_uses_actual_promise_not_quality_dispute(report):
    item = next(r for r in report["items"] if r["item_id"] == "CE-06-02")
    assert item["coverage_status"] == "通过"
    assert all("背离" in r["text"] or "一致" in r["text"] for r in item["evidence_clauses"])
    assert all(not r["location"].endswith("8.5") for r in item["evidence_clauses"])


def test_every_positive_pass_is_semantically_verified_and_source_bound(report):
    assert not coverage_failures([SimpleNamespace(**r) for r in report["items"]])


@pytest.mark.parametrize("mutation", ["location", "text", "missing", "partial"])
def test_pass_evidence_mutation_is_blocked(report, mutation):
    item = deepcopy(next(r for r in report["items"] if r["item_id"] == "CE-13-01"))
    if mutation == "location":
        item["evidence_clauses"][0]["location"] = "第二部分 通用条款 / 8.5"
    elif mutation == "text":
        item["evidence_clauses"][0]["text"] = "施工质量争议由鉴定机构解决。"
    elif mutation == "missing":
        item["evidence_clauses"] = []
    else:
        item["evidence_clauses"] = [{"clause_id": "C1", "text": "合同文件包括图纸。", "location": "1"}]
    assert coverage_failures([SimpleNamespace(**item)])


@pytest.mark.parametrize("field", ["coverage", "manual", "severity", "total", "rendered", "action"])
def test_summary_mutation_blocks_release(report, field):
    result = deepcopy(report)
    if field == "coverage":
        result["coverage_summary"].pop("法律提示")
    elif field == "manual":
        result["final_overview_summary"]["manual_review"] = 0
    elif field == "severity":
        result["risk_finding_summary"]["重大风险"] += 1
    elif field == "total":
        result["all_items_count"] = 41
    elif field == "action":
        result["final_overview_summary"]["priority_action"] += 1
    else:
        result["result"] = result["result"].replace("- 待核验：6 项", "- 待核验：0 项")
    assert statistics_gate(result)["status"] == "BLOCKED"


def test_user_reported_31_10_4_7_closes_without_hiding_states():
    states = ["通过"] * 31 + ["缺失"] * 10 + ["待核验"] * 4 + ["法律提示"] * 7
    rows = [{"item_id": str(i), "coverage_status": state, "risk_level": "低"} for i, state in enumerate(states)]
    manual = [{"item_id": str(i), "source_rules": [str(i)]} for i in range(41, 45)]
    result = {"items": rows, "all_items_count": 52, "coverage_summary": dict(Counter(states)),
              "summary": {"高": 0, "中": 0, "低": 52}, "manual_review_items": manual,
              "manual_review_summary": {"manual_review_count": 4},
              "risk_finding_summary": {"重大风险": 0, "中等风险": 0, "低风险": 0, "人工复核": 4},
              "final_overview_summary": {"major_risk": 0, "medium_risk": 0, "low_risk": 0, "manual_review": 4}}
    assert statistics_gate(result)["status"] == "REPORT_READY"


def test_relocated_clause_and_unrelated_neighbour_do_not_change_coverage():
    text = "第九十九条 文件组成\n合同文件包括标准、规范和技术要求，以及图纸。\n第一百条 质量争议\n施工质量争议应提交鉴定。"
    rows = extract("drawing_technical_spec_attachment", parse_contract_clauses(text))
    assert rows and all("质量争议" not in r["text"] for r in rows)
    assert all(any(supports(e, r["text"]) for r in rows) for e in PROFILES["drawing_technical_spec_attachment"])
    assert not extract("substantive_terms_consistency", parse_contract_clauses(text))


def test_model_missing_verdicts_cannot_override_full_corpus_evidence(monkeypatch):
    import review_v2.engine as engine
    original = engine.judge_checkpoints_with_llm

    def wrong_model(checkpoints, clauses, **kwargs):
        judgments = original(checkpoints, clauses, use_llm=False)
        for key in TARGETS:
            row = judgments.get(key)
            if row:
                judgments[key] = replace(row, coverage_status="缺失", evidence_clauses=[], evidence_location="")
        return judgments

    monkeypatch.setattr(engine, "judge_checkpoints_with_llm", wrong_model)
    result = engine.review_contract_v2(TEXT, "construction", use_llm=True)
    assert all(r["coverage_status"] in ({"通过", "部分覆盖"} if r["item_id"] == "CE-13-03" else {"通过"}) for r in result["items"] if r["item_id"] in TARGETS)
