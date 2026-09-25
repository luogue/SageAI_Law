from pathlib import Path

import pytest

from review_v2.clause_parser import parse_contract_clauses
from review_v2.consulting_element_facts import elements
from review_v2.engine import review_contract_v2
from review_v2.penalty_base import analyze as analyze_penalty
from review_v2.user_profile import UserRiskProfile


TEXT = (Path(__file__).parent / "fixtures" / "round43_consulting_generalization.txt").read_text(encoding="utf8")


def _atoms(family):
    return {row["element_id"]: row for row in elements(family, parse_contract_clauses(TEXT))}


def test_consulting_atoms_share_verified_cross_clause_sources():
    payment = _atoms("consulting_payment")
    quality = _atoms("consulting_quality")
    remedy = _atoms("consulting_remedy")
    inputs = _atoms("consulting_inputs")

    assert payment["consulting_fee_total"]["status"] == "COVERED"
    assert "480,000" in payment["consulting_fee_total"]["supporting_evidence"][0]["quote"]
    for key in ("delivery_form", "acceptance_standard"):
        assert quality[key]["status"] == "COVERED" and quality[key]["supporting_evidence"]
    for key in ("defect_trigger", "correction_period", "correction_remedy"):
        assert remedy[key]["status"] == "COVERED" and remedy[key]["supporting_evidence"]
    assert inputs["cooperation_conditions"]["status"] == "COVERED"
    assert inputs["truthfulness_completeness"]["status"] == "MISSING"


def test_penalty_base_reuses_verified_consulting_total():
    row = next(row for row in analyze_penalty(TEXT) if row["base"] == "合同总咨询费")
    assert row["status"] == "DETERMINABLE"
    assert any("480,000" in definition for definition in row["definitions"])


@pytest.mark.parametrize("identity", ["甲方/委托方", "乙方/咨询方"])
def test_final_projection_reuses_the_same_consulting_atoms(identity):
    report = review_contract_v2(
        TEXT, "technology", use_llm=False,
        profile=UserRiskProfile(user_identity=identity),
    )
    items = {row["item_id"]: row for row in report["items"]}
    expected = {
        "TC-08-05": ("consulting_fee_total",),
        "TC-08-01": ("delivery_form", "acceptance_standard"),
        "TC-08-04": ("defect_trigger", "correction_period", "correction_remedy"),
        "TC-08-03": ("cooperation_conditions",),
    }
    for rule_id, keys in expected.items():
        components = {row["element_id"]: row for row in items[rule_id]["coverage_elements"]}
        for key in keys:
            component = components[key]
            assert component["status"] == "COVERED"
            assert component["source_fact_key"]
            assert component["supporting_evidence_ids"]
            direct = [row for row in items[rule_id]["evidence_clauses"]
                      if key in row.get("supporting_element_ids", [])]
            assert direct and all(row["support_type"] == "DIRECT" for row in direct)
    inputs = {row["element_id"]: row for row in items["TC-08-03"]["coverage_elements"]}
    assert inputs["truthfulness_completeness"]["status"] == "MISSING"
    assert items["COMMON-20-01"]["coverage_status"] == "通过"
    # The deterministic unit path can expose unrelated legacy common-rule
    # diagnostics.  The target exact-binding invariants must themselves pass;
    # production Gate status is exercised through the real endpoint acceptance.
    gates = report["release_quality_gate"]["gate_results"]
    assert gates["REVIEW_EVIDENCE_ELEMENT_MISMATCH"] == "PASS"
    assert gates["RISK_EVIDENCE_MISMATCH"] == "PASS"
