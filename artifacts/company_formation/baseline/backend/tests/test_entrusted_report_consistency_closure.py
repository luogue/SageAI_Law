"""Current entrusted contract through the unchanged production upload/report API."""
from copy import deepcopy

from tests.test_entrusted_development_production_closure import report, item
from review_v2.report_state_consistency import report_state_consistency_failures
from review_v2.requirement_keys import canonical_requirement_key


def elements(report, rule):
    return {row["element_id"]: row for row in item(report, rule)["coverage_elements"]}


def test_patent_rights_positive_evidence_precedes_absence(report):
    rows = elements(report, "TC-04-03")
    covered = {"patent_application_right_ownership", "patent_right_after_grant", "inventor_authorship"}
    for key in covered:
        assert rows[key]["status"] == "COVERED", rows[key]
        assert rows[key]["supporting_evidence"]
    for key in ("application_filing_control", "document_signature_cooperation", "registration_cooperation"):
        assert rows[key]["status"] == "PARTIALLY_COVERED"
        assert rows[key]["residual_gap"]
    searches = item(report, "TC-04-03")["decision_trace"]["element_absence_searches"]
    assert not covered & {row["element_id"] for row in searches if row["result"] == "NOT_FOUND"}


def test_risk_loss_allocation_is_not_payment_settlement(report):
    rows = elements(report, "TC-04-04")
    assert rows["no_fault_technical_risk_allocation"]["status"] == "COVERED"
    assert "50%" in str(rows["no_fault_technical_risk_allocation"]["supporting_evidence"])
    for key in ("failed_development_incurred_cost_settlement", "paid_fee_refund", "unpaid_fee_obligation",
                "failed_project_stage_result_disposition", "failed_project_source_code_disposition", "failed_project_material_disposition"):
        assert rows[key]["status"] == "MISSING", rows[key]


def test_confidentiality_fields_and_survival_period_are_consumed(report):
    review = item(report, "TC-11-02")
    assert review["coverage_status"] == "部分覆盖"
    rows = elements(report, "TC-11-02")
    assert {key for key, row in rows.items() if row["status"] == "MISSING"} == {"confidentiality_exceptions"}
    assert all(row["status"] == "COVERED" for key, row in rows.items() if key != "confidentiality_exceptions")
    assert "5年" in str(rows["confidentiality_duration"]["supporting_evidence"])
    for key, row in rows.items():
        if key == "confidentiality_exceptions":
            continue
        parties = {entry["obligated_party"]: entry for entry in row["party_coverage"]}
        assert set(parties) == {"甲方", "乙方"}, row
        assert all(entry["status"] == "COVERED" for entry in parties.values())
        for entry in parties.values():
            assert entry["required_fact"] in " ".join(review["narrative_state"]["covered_elements"])


def test_ancillary_support_and_priority_license_enter_substantive_review(report):
    service = item(report, "TC-09-01")
    assert service["applicability"]["status"] == "APPLICABLE"
    assert service["coverage_status"] == "通过"
    assert "第十九条" in service["evidence_location"]
    sharing = item(report, "TC-10-02")
    assert sharing["coverage_status"] == "部分覆盖"
    rows = elements(report, "TC-10-02")
    assert rows["priority_license"]["status"] == "COVERED"
    assert set(sharing["decision_trace"]["final_missing_element_ids"]) == {
        "license_fee", "license_territory", "license_duration", "commercial_use", "improvement_sublicense",
    }


def test_non_applicable_remedy_coordination_cannot_remain_partial(report):
    review = item(report, "TC-12-04")
    assert review["applicability"]["status"] == "NOT_APPLICABLE"
    assert review["coverage_status"] == "不适用"
    assert review["narrative_state"]["coverage_status"] == "不适用"
    assert not review["decision_trace"].get("final_missing_element_ids")
    assert all("TC-12-04" not in finding["source_review_ids"] for finding in report["risk_findings"])


def test_material_unresolved_set_is_identical_in_all_projections(report):
    review = item(report, "TC-13-01")
    expected = set(review["decision_trace"]["final_missing_element_ids"])
    finding = next(row for row in report["risk_findings"] if "TC-13-01" in row["source_review_ids"])
    assert {row["element_id"] for row in finding["final_missing_elements"]} == expected
    assert set(review["decision_trace"]["recommendation_element_projection"]["missing_element_ids"]) == expected
    for row in finding["final_missing_elements"]:
        label = row.get("residual_gap") or row.get("required_fact") or row["proposition"]
        assert label.strip("。") in finding["issue"]
        assert label.strip("。") in finding["recommendation"]


def test_real_release_gate_and_new_invariants_reject_mutated_reports(report):
    assert report["release_quality_gate"]["status"] == "REPORT_READY", report["release_quality_gate"]
    assert not report_state_consistency_failures(report["items"], report["risk_findings"])
    changed = deepcopy(item(report, "TC-12-04"))
    changed["coverage_status"] = "部分覆盖"
    assert any(row["reason"] == "NOT_APPLICABLE_NARRATIVE_STATE_CONFLICT"
               for row in report_state_consistency_failures([changed]))
    changed = deepcopy(item(report, "TC-04-03"))
    changed["decision_trace"]["element_absence_searches"].append({
        "element_id": "PATENT_APPLICATION_RIGHT_OWNERSHIP", "result": "NOT_FOUND",
    })
    assert any(row["reason"] == "POSITIVE_REQUIREMENT_WITH_ABSENCE_SEARCH"
               for row in report_state_consistency_failures([changed]))
    finding = deepcopy(next(row for row in report["risk_findings"] if "TC-13-01" in row["source_review_ids"]))
    finding["final_missing_elements"] = finding["final_missing_elements"][:1]
    assert any(row["reason"] == "REPORT_UNRESOLVED_REQUIREMENTS_MISMATCH"
               for row in report_state_consistency_failures(report["items"], [finding]))


def test_final_requirement_keys_and_support_aliases_are_canonical(report):
    def visit(value):
        if isinstance(value, dict):
            for field, data in value.items():
                if field in {"element_id", "required_fact_key", "source_fact_key", "requirement_key", "requirement_id"}:
                    assert data == canonical_requirement_key(data), (field, data)
                elif field in {"supporting_element_ids", "searched_absent_element_ids", "element_ids"}:
                    assert data == list(dict.fromkeys(canonical_requirement_key(key) for key in data)), (field, data)
                yield from visit(data)
        elif isinstance(value, list):
            for row in value:
                yield from visit(row)
    list(visit(report["items"]))
    list(visit([finding["evidence_bundle"] for finding in report["risk_findings"]]))


def test_atomic_consequences_cannot_reintroduce_old_composite_absence(report):
    for rule in ("TC-04-03", "TC-04-04", "TC-11-02", "TC-10-02"):
        review = item(report, rule)
        rows = elements(report, rule)
        expected = set(review["decision_trace"]["final_missing_element_ids"])
        assert set(review["decision_trace"]["consequence_element_ids"]) == expected
        consequence = review["legal_consequence_if_missing"]
        assert consequence == review["narrative_state"]["consequence"]
        assert all((rows[key].get("residual_gap") or rows[key]["required_fact"]).strip("。") in consequence
                   for key in expected)
        assert all((rows[key].get("residual_gap") or rows[key]["required_fact"]).strip("。") in review["reasoning_summary"]
                   for key in expected)
        assert "未约定无过错技术风险导致研发失败时的责任分配" not in consequence
        assert "如未专项明确专利申请权" not in consequence
    patent = item(report, "TC-04-03")
    assert "已覆盖" in patent["reasoning_summary"]
    assert "甲方享有申请专利的权利" in patent["reasoning_summary"]
