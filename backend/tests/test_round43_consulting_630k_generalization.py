from pathlib import Path

import pytest

from review_v2.clause_parser import parse_contract_clauses
from review_v2.confidentiality_remedies import confidentiality_remedy_elements
from review_v2.consulting_element_facts import elements as consulting_elements
from review_v2.engine import review_contract_v2
from review_v2.penalty_base import analyze as analyze_penalty
from review_v2.technology_service_elements import elements as service_elements
from review_v2.user_profile import UserRiskProfile


TEXT = (Path(__file__).parent / "fixtures" / "round43_consulting_630k.txt").read_text(encoding="utf8")
CLAUSES = parse_contract_clauses(TEXT)


def indexed(rows):
    return {row["element_id"]: row for row in rows}


def test_consulting_atoms_cover_project_quality_inputs_remedy_and_lump_sum_fee():
    subject = indexed(consulting_elements("consulting_subject", CLAUSES))
    quality = indexed(consulting_elements("consulting_quality", CLAUSES))
    inputs = indexed(consulting_elements("consulting_inputs", CLAUSES))
    remedy = indexed(consulting_elements("consulting_remedy", CLAUSES))
    payment = indexed(consulting_elements("consulting_payment", CLAUSES))

    assert subject["consulting_project"]["status"] == "COVERED"
    for key in ("report_contents", "delivery_form", "acceptance_standard"):
        assert quality[key]["status"] == "COVERED"
        assert quality[key]["supporting_evidence"]
    assert inputs["truthfulness_completeness"]["status"] == "COVERED"
    assert all(row["status"] == "COVERED" for row in inputs["truthfulness_completeness"]["component_coverage"])
    assert remedy["defect_trigger"]["status"] == "COVERED"
    assert payment["consulting_fee_total"]["status"] == "COVERED"
    assert "630,000.00" in payment["consulting_fee_total"]["supporting_evidence"][0]["quote"]


def test_confidentiality_and_material_exit_atoms_keep_only_real_gaps():
    controls = indexed(service_elements("confidentiality_controls", CLAUSES))
    disclosure = indexed(service_elements("confidentiality_disclosure", CLAUSES))
    exit_rows = indexed(service_elements("material_exit", CLAUSES))
    remedies = indexed(confidentiality_remedy_elements(CLAUSES))

    for key in ("confidentiality_obligation", "third_party_disclosure_restriction", "security_measures"):
        assert controls[key]["status"] == "COVERED"
    assert disclosure["post_termination_confidentiality"]["status"] == "COVERED"
    for key in ("termination_return_or_delete", "processing_deadline", "retained_backup_use_restriction",
                "confidential_copy_deletion", "confidential_backup_deletion", "confidential_disposal_confirmation"):
        assert exit_rows[key]["status"] == "COVERED", key
    assert exit_rows["confidential_material_destruction"]["status"] == "MISSING"
    for key in ("breach_damage_liability", "stop_disclosure", "stop_use", "mitigation_obligation"):
        assert remedies[key]["status"] == "COVERED", key
    assert remedies["incident_notification"]["status"] == "MISSING"


def test_claim_applicability_and_penalty_base_reuse_verified_facts():
    claims = indexed(service_elements("service_claims", CLAUSES))
    for key in ("third_party_claim_trigger", "notification_requirement", "necessary_assistance"):
        assert claims[key]["status"] == "COVERED", key
    assert claims["claim_handling_responsibility"]["status"] == "MISSING"

    formula = next(row for row in analyze_penalty(TEXT) if row["base"] == "本合同咨询服务总价")
    assert formula["status"] == "DETERMINABLE"
    assert any("630,000.00" in definition for definition in formula["definitions"])


@pytest.mark.parametrize("party", ["甲方", "乙方"])
def test_final_projection_is_exact_and_report_ready_for_both_stances(party):
    report = review_contract_v2(
        TEXT, "technology", use_llm=False,
        profile=UserRiskProfile(user_identity=party),
    )
    assert report["release_quality_gate"]["status"] == "REPORT_READY", report["release_quality_gate"]["failures"]
    gates = report["release_quality_gate"]["gate_results"]
    assert gates["REVIEW_EVIDENCE_ELEMENT_MISMATCH"] == "PASS"
    assert gates["EXACT_ELEMENT_REPORT_INVARIANT"] == "PASS"

    items = {row["item_id"]: row for row in report["items"]}
    assert items["TC-01-04"]["coverage_presence"] == "NOT_APPLICABLE"
    assert items["TC-08-05"]["coverage_status"] == "通过"
    assert items["COMMON-20-01"]["coverage_status"] == "通过"
    assert items["TC-11-03"]["coverage_status"] == "部分覆盖"
    assert items["TC-11-04"]["coverage_status"] == "部分覆盖"
    assert items["TC-12-02"]["coverage_status"] == "部分覆盖"
    for rule_id in ("TC-01-03", "TC-08-01", "TC-08-03", "TC-08-04", "TC-08-05", "TC-11-01", "TC-11-02"):
        covered = [row for row in items[rule_id]["coverage_elements"] if row["status"] == "COVERED"]
        assert covered
        for component in covered:
            assert component.get("supporting_evidence_ids") or component.get("evidence_ids")

