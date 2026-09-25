from pathlib import Path

import pytest

from review_v2.clause_parser import parse_contract_clauses
from review_v2.consulting_element_facts import elements as consulting_elements
from review_v2.confidentiality_remedies import canonical_confidentiality_remedies
from review_v2.engine import review_contract_v2
from review_v2.technology_service_elements import elements as technology_elements
from review_v2.user_profile import UserRiskProfile


TEXT = (Path(__file__).parent / "fixtures" / "round44_consulting_projection.txt").read_text(encoding="utf-8")


def states(rows):
    return {row["element_id"]: row for row in rows}


def test_consulting_canonical_facts_cover_cross_sentence_and_reference_forms():
    clauses = parse_contract_clauses(TEXT)
    expected = {
        "consulting_subject": {"consulting_project", "consulting_scope"},
        "consulting_quality": {"consulting_scope", "report_contents"},
        "consulting_decision": {"qualified_consulting_decision_risk", "consultant_fault_exception"},
        "consulting_inputs": {"cooperation_conditions", "truthfulness_completeness"},
        "consulting_remedy": {"defect_trigger", "correction_period", "correction_remedy"},
    }
    for family, keys in expected.items():
        rows = states(consulting_elements(family, clauses))
        assert all(rows[key]["status"] == "COVERED" for key in keys)
        assert all(rows[key]["supporting_evidence"] for key in keys)


def test_confidentiality_canonical_facts_cover_lists_survival_exit_and_incident():
    clauses = parse_contract_clauses(TEXT)
    controls = states(technology_elements("confidentiality_controls", clauses))
    for key in {
        "confidential_information_scope", "confidentiality_obligation",
        "need_to_know_personnel", "purpose_limitation",
        "third_party_disclosure_restriction", "copying_restriction", "security_measures",
    }:
        assert controls[key]["status"] == "COVERED"
    disclosure = states(technology_elements("confidentiality_disclosure", clauses))
    for key in {
        "post_termination_confidentiality", "public_information_exception",
        "lawful_third_party_source_exception", "independent_development_exception",
        "compelled_disclosure_exception", "prior_notice_when_legally_permitted",
    }:
        assert disclosure[key]["status"] == "COVERED"
    exit_rows = states(technology_elements("material_exit", clauses))
    for key in {
        "termination_return_or_delete", "processing_deadline",
        "retained_backup_use_restriction", "confidential_copy_deletion",
        "confidential_backup_deletion", "confidential_disposal_confirmation",
    }:
        assert exit_rows[key]["status"] == "COVERED"
    remedies = states(canonical_confidentiality_remedies(clauses))
    for key in {
        "breach_damage_liability", "stop_disclosure", "stop_use",
        "mitigation_obligation", "incident_notification",
    }:
        assert remedies[key]["status"] == "COVERED"


@pytest.mark.parametrize("party", ["甲方", "乙方"])
def test_final_projection_removes_stale_missing_audits(party):
    result = review_contract_v2(
        TEXT, "technology", use_llm=False, include_low_risk=True,
        profile=UserRiskProfile(user_identity=party),
    )
    assert result["release_quality_gate"]["status"] == "REPORT_READY"
    target = {
        "TC-01-03", "TC-08-01", "TC-08-02", "TC-08-03", "TC-08-04",
        "TC-11-01", "TC-11-02", "TC-11-03", "TC-11-04",
    }
    for item in result["items"]:
        if item["item_id"] not in target:
            continue
        covered = {
            row["element_id"] for row in item.get("coverage_elements", [])
            if row.get("status") == "COVERED"
        }
        missing_audits = {
            row["element_id"] for row in item.get("decision_trace", {}).get("element_absence_searches", [])
            if row.get("result") == "NOT_FOUND"
        }
        assert covered.isdisjoint(missing_audits)

