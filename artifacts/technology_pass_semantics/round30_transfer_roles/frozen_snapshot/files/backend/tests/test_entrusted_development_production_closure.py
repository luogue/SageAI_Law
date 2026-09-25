"""Uploaded entrusted-development contract through the production report API."""
import json
from pathlib import Path
from dataclasses import fields
from copy import deepcopy

import pytest
from fastapi.testclient import TestClient
from main import app
from auth.routes import get_current_user
from review_v2 import engine

CURRENT = Path(__file__).resolve().parents[2] / "test_data" / "47 技术开发（委托）合同.docx"


@pytest.fixture(scope="module")
def report():
    previous = app.dependency_overrides.get(get_current_user)
    app.dependency_overrides[get_current_user] = lambda: {"id": 1, "phone": "test"}
    try:
        with TestClient(app) as client:
            response = client.post("/review-v2/file", files={"file": (CURRENT.name, CURRENT.read_bytes(),
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document")},
                data={"contract_type": "technology", "include_low_risk": "true", "use_llm": "false",
                      "profile_json": json.dumps({"user_identity": "甲方/委托方"}, ensure_ascii=False)})
    finally:
        if previous is None:
            app.dependency_overrides.pop(get_current_user, None)
        else:
            app.dependency_overrides[get_current_user] = previous
    assert response.status_code == 200, response.text
    return response.json()


def item(report, rule):
    return next(row for row in report["items"] if row["item_id"] == rule)


def test_primary_and_ancillary_routing(report):
    assert report["contract_context"]["canonical_classification"]["contract_subtype"] == "ENTRUSTED_DEVELOPMENT"
    for rule in ("TC-04-01", "TC-04-02", "TC-04-03", "TC-04-04", "TC-09-01"):
        assert item(report, rule)["applicability"]["status"] == "APPLICABLE", item(report, rule)
    for rule in ("TC-05-01", "TC-05-02"):
        assert item(report, rule)["applicability"]["status"] == "NOT_APPLICABLE"


def test_exit_atoms_and_all_report_layers_share_state(report):
    review = item(report, "TC-05-04")
    assert review["coverage_status"] == "部分覆盖"
    rows = {e["element_id"]: e for e in review["coverage_elements"]}
    covered = {"development_delay_liability", "payment_delay_liability", "development_termination_mechanism"}
    assert set(rows) == set(engine.DEVELOPMENT_EXIT_REQUIREMENTS)
    assert {key for key, row in rows.items() if row["status"] == "COVERED"} == covered
    missing = set(rows) - covered
    assert all(rows[key]["status"] == "MISSING" for key in missing)
    assert all(rows[key]["supporting_evidence"] for key in covered)
    assert set(review["decision_trace"]["final_missing_element_ids"]) == missing
    searches = review["decision_trace"]["element_absence_searches"]
    assert {row["element_id"] for row in searches if row["result"] == "NOT_FOUND"} == missing
    finding = next(f for f in report["risk_findings"] if "TC-05-04" in f["source_review_ids"])
    assert {e["element_id"] for e in finding["final_missing_elements"]} == missing
    absent = {key for e in finding["evidence_bundle"]["items"] if e.get("source_type") == "SEARCH_AUDIT"
              for key in e.get("searched_absent_element_ids", [])}
    assert absent == missing
    assert not covered.intersection(review["decision_trace"]["recommendation_element_projection"]["missing_element_ids"])
    consequence = review["legal_consequence_if_missing"]
    assert all(rows[key]["required_fact"] in consequence for key in missing)
    assert all(rows[key]["required_fact"] not in consequence for key in covered)
    assert consequence == review["narrative_state"]["consequence"]
    assert "合作方退出、迟延投入" not in consequence


def test_release_gate_passes_without_skipping_consistency(report):
    gate = report["release_quality_gate"]
    assert gate["status"] in {"PASSED", "REPORT_READY"}, gate
    assert not gate.get("blocking_reasons"), gate


def test_newly_active_development_branch_consumes_actual_claim_evidence(report):
    review = item(report, "TC-12-02")
    rows = {e["element_id"]: e for e in review["coverage_elements"]}
    for key in ("notification_requirement", "notification_deadline", "liability_responsible_party",
                "licensor_participation", "legal_cost_allocation", "settlement_consultation"):
        assert rows[key]["status"] == "COVERED", rows[key]
        assert rows[key]["supporting_evidence"]
    assert "5个工作日" in rows["notification_deadline"]["proposition"]
    assert "开发方" in rows["liability_responsible_party"]["proposition"]
    assert rows["damages_scope"]["status"] == "MISSING"
    nature = item(report, "TC-01-01")
    assert all(e["supporting_evidence"] for e in nature["coverage_elements"])
    assert "合同以软件研发、需求确认" not in report["result"]


def test_positive_development_fact_cannot_be_mutated_to_absent(report):
    raw = item(report, "TC-05-04")
    review = engine.ReviewItemResult(**{key: deepcopy(value) for key, value in raw.items()
                                      if key in {f.name for f in fields(engine.ReviewItemResult)}})
    row = next(e for e in review.coverage_elements if e["element_id"] == "development_delay_liability")
    row["status"] = "MISSING"
    assert engine._release_quality_gate([review], [], report["result"])["status"] == "BLOCKED"
