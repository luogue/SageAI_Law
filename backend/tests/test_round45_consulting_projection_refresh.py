from pathlib import Path

import pytest

from review_v2.clause_parser import parse_contract_clauses
from review_v2.confidentiality_remedies import canonical_confidentiality_remedies
from review_v2.consulting_element_facts import elements as consulting_elements
from review_v2.engine import review_contract_v2
from review_v2.technology_service_elements import elements as technology_elements
from review_v2.user_profile import UserRiskProfile


TEXT = (Path(__file__).parent / "fixtures" / "round45_consulting_projection.txt").read_text(encoding="utf-8")


def indexed(rows):
    return {row["element_id"]: row for row in rows}


def test_consulting_lists_conditions_and_references_publish_shared_canonical_facts():
    clauses = parse_contract_clauses(TEXT)
    expected = {
        "consulting_subject": {"consulting_project", "consulting_scope"},
        "consulting_quality": {"consulting_scope", "report_contents", "acceptance_standard"},
        "consulting_decision": {"qualified_consulting_decision_risk", "consultant_fault_exception"},
        "consulting_inputs": {"truthfulness_completeness"},
        "consulting_remedy": {"defect_trigger", "correction_period", "correction_remedy"},
    }
    for family, keys in expected.items():
        rows = indexed(consulting_elements(family, clauses))
        assert all(rows[key]["status"] == "COVERED" for key in keys)
        assert all(rows[key]["supporting_evidence"] for key in keys)


def test_confidentiality_lists_publish_controls_exceptions_exit_and_incident_atoms():
    clauses = parse_contract_clauses(TEXT)
    controls = indexed(technology_elements("confidentiality_controls", clauses))
    assert controls["third_party_disclosure_restriction"]["status"] == "COVERED"
    assert controls["security_measures"]["status"] == "COVERED"
    disclosure = indexed(technology_elements("confidentiality_disclosure", clauses))
    assert disclosure["independent_development_exception"]["status"] == "COVERED"
    exit_rows = indexed(technology_elements("material_exit", clauses))
    for key in {
        "processing_deadline", "retained_backup_use_restriction",
        "confidential_copy_deletion", "confidential_backup_deletion",
        "confidential_disposal_confirmation",
    }:
        assert exit_rows[key]["status"] == "COVERED"
    assert exit_rows["confidential_material_destruction"]["status"] == "MISSING"
    remedies = indexed(canonical_confidentiality_remedies(clauses))
    for key in {"breach_damage_liability", "stop_disclosure", "stop_use", "mitigation_obligation", "incident_notification"}:
        assert remedies[key]["status"] == "COVERED"


def test_third_party_claim_remedy_chain_is_atomically_projected():
    clauses = parse_contract_clauses(TEXT)
    rows = indexed(technology_elements("service_claims", clauses))
    for key in {
        "third_party_claim_trigger", "claim_handling_responsibility",
        "provider_infringement_liability", "direct_damage", "defense_cost_allocation",
        "notification_requirement", "notification_deadline", "necessary_assistance",
        "termination_remedy", "refund_remedy", "settlement_authority",
        "replacement_remedy", "license_cure",
    }:
        assert rows[key]["status"] == "COVERED"
        assert rows[key]["supporting_evidence"]
    assert rows["defense_control"]["status"] == "PARTIALLY_COVERED"
    assert rows["lawyer_selection"]["status"] == "MISSING"


@pytest.mark.parametrize("party", ["甲方", "乙方"])
def test_final_snapshot_refreshes_missing_audits_from_verified_facts(party):
    result = review_contract_v2(
        TEXT, "technology", use_llm=False, include_low_risk=True,
        profile=UserRiskProfile(user_identity=party),
    )
    assert result["release_quality_gate"]["status"] == "REPORT_READY"
    targets = {
        "TC-01-03", "TC-08-01", "TC-08-02", "TC-08-03", "TC-08-04",
        "TC-11-01", "TC-11-02", "TC-11-03", "TC-11-04", "TC-12-02",
    }
    for item in result["items"]:
        if item["item_id"] not in targets:
            continue
        covered = {
            row["element_id"] for row in item.get("coverage_elements", [])
            if row.get("status") == "COVERED"
        }
        missing = {
            row["element_id"]
            for row in item.get("decision_trace", {}).get("element_absence_searches", [])
            if row.get("result") == "NOT_FOUND"
        }
        assert covered.isdisjoint(missing)

