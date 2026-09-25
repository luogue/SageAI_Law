from pathlib import Path

import pytest

from review_v2.clause_parser import parse_contract_clauses
from review_v2.consulting_element_facts import elements as consulting_elements
from review_v2.penalty_base import analyze
from review_v2.technology_service_elements import elements


TEXT = (Path(__file__).parent / "fixtures" / "round42_consulting.txt").read_text(encoding="utf8")
CLAUSES = parse_contract_clauses(TEXT)


def indexed(rows):
    return {row["element_id"]: row for row in rows}


def test_consulting_aliases_project_to_public_atomic_facts():
    subject = indexed(consulting_elements("consulting_subject", CLAUSES))
    quality = indexed(consulting_elements("consulting_quality", CLAUSES))
    decision = indexed(consulting_elements("consulting_decision", CLAUSES))
    inputs = indexed(consulting_elements("consulting_inputs", CLAUSES))
    assert subject["consulting_project"]["status"] == "COVERED"
    assert subject["consulting_scope"]["canonical_alias_of"] == "consulting_quality.consulting_scope"
    assert quality["report_contents"]["status"] == "COVERED"
    assert quality["acceptance_standard"]["status"] == "COVERED"
    assert decision["qualified_consulting_decision_risk"]["status"] == "COVERED"
    truth = inputs["truthfulness_completeness"]
    assert truth["status"] == "PARTIALLY_COVERED"
    components = indexed(truth["component_coverage"])
    assert components["material_truthfulness"]["status"] == "COVERED"
    assert components["material_completeness"]["status"] == "MISSING"


def test_confidentiality_and_exit_use_article_scoped_propositions():
    controls = indexed(elements("confidentiality_controls", CLAUSES))
    disclosure = indexed(elements("confidentiality_disclosure", CLAUSES))
    assert controls["confidential_information_scope"]["status"] == "COVERED"
    assert controls["purpose_limitation"]["status"] == "COVERED"
    for key in ("public_information_exception", "lawful_third_party_source_exception",
                "independent_development_exception", "compelled_disclosure_exception",
                "prior_notice_when_legally_permitted"):
        assert disclosure[key]["status"] == "COVERED", key
    exit_rows = indexed(elements("material_exit", CLAUSES))
    disposition = exit_rows["termination_return_or_delete"]
    assert disposition["status"] == "COVERED"
    components = indexed(disposition["component_coverage"])
    for key in ("service_end_disposition_trigger", "original_data_return", "original_data_deletion",
                "identifiable_copy_deletion", "retention_exception"):
        assert components[key]["status"] == "COVERED", key
    assert exit_rows["processing_deadline"]["status"] == "MISSING"
    assert exit_rows["confidential_backup_deletion"]["status"] == "MISSING"


def test_consulting_fee_total_is_a_determinable_penalty_base():
    rows = analyze(TEXT)
    total = next(row for row in rows if row["base"] == "技术咨询费总额")
    assert total["status"] == "DETERMINABLE"
    assert any("680,000元" in definition for definition in total["definitions"])


@pytest.mark.parametrize("party", ["甲方", "乙方"])
def test_round42_final_projection_is_exact(party):
    from review_v2.engine import review_contract_v2
    from review_v2.user_profile import UserRiskProfile

    report = review_contract_v2(TEXT, "technology", use_llm=False,
                                profile=UserRiskProfile(user_identity=party))
    assert report["release_quality_gate"]["status"] == "REPORT_READY", report["release_quality_gate"]["failures"]
    gates = report["release_quality_gate"]["gate_results"]
    assert gates["REVIEW_EVIDENCE_ELEMENT_MISMATCH"] == "PASS"
    assert gates["EXACT_ELEMENT_REPORT_INVARIANT"] == "PASS"
    items = {item["item_id"]: item for item in report["items"]}
    for rule_id in ("TC-01-01", "TC-01-02"):
        component = indexed(items[rule_id]["coverage_elements"])["transaction_consulting_performance"]
        assert component["status"] == "COVERED"
        assert component["evidence_ids"]
