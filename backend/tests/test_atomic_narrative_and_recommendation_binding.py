from copy import deepcopy
from dataclasses import fields
from types import SimpleNamespace

import pytest

from review_v2 import engine
from review_v2.narrative_evidence import narrative_evidence_gate
from backend.tests.test_narrative_source_and_date_semantics import current


def identity_case(proposition, attribution=False):
    rows = [{"evidence_id": "e1", "clause_id": "c1", "quoted_text": "发明人/设计人：张三",
             "source_type": "SOURCE_CLAUSE", "supporting_review_ids": ["ANY"],
             "supporting_element_ids": ["identity"]}]
    if attribution:
        rows.append(dict(rows[0], evidence_id="e2", clause_id="c2", quoted_text="张三享有研发成果署名权。"))
    item = SimpleNamespace(item_id="ANY", coverage_elements=[{
        "element_id": "identity", "status": "COVERED", "proposition": proposition,
        "supporting_evidence": [{"clause_id": r["clause_id"], "quote": r["quoted_text"]} for r in rows],
    }], risk_point_description=proposition, reasoning_summary=proposition, narrative_state={})
    finding = SimpleNamespace(finding_id="f", source_review_ids=["ANY"], issue=proposition,
                              evidence_bundle={"items": rows})
    return item, finding


@pytest.mark.parametrize("separator", ["，", "；", "。"])
def test_identity_does_not_support_a_second_attribution_assertion(separator):
    item, finding = identity_case("合同已列明发明人姓名" + separator + "合同署名已有明确记载。")
    gate = narrative_evidence_gate([item], [finding])
    assert gate["status"] == "BLOCKED"
    atoms = [r for r in gate["claims"] if r["field"] == "atomic_element_proposition"]
    assert any(r["predicate"] == "creator_identity" and r["supporting_evidence_ids"] for r in atoms)
    assert any(r["predicate"] == "creator_attribution" and not r["supporting_evidence_ids"] for r in atoms)


def test_each_independent_fact_can_have_its_own_direct_source():
    item, finding = identity_case("合同已列明发明人姓名，合同署名已有明确记载。", True)
    assert narrative_evidence_gate([item], [finding])["status"] == "REPORT_READY"


def test_current_names_and_document_advice_are_not_expanded(current):
    assert current["release_quality_gate"]["status"] == "REPORT_READY", current["release_quality_gate"]["failures"]
    by_id = {row["item_id"]: row for row in current["items"]}
    assert "署名已有" not in str(by_id["TC-03-03"]["coverage_elements"])
    for rule in ("TC-03-04", "TC-13-02"):
        item = by_id[rule]
        assert "登记" not in item["suggested_clause_example"]
        assert "受理通知书" in item["suggested_clause_example"]
        assert "审查" in item["suggested_clause_example"]


@pytest.mark.parametrize("mutation", ["covered_id", "new_id", "new_text", "rendered_text"])
def test_recommendation_gate_rejects_covered_or_unregistered_actions(current, mutation):
    def load(cls, key):
        return [cls(**{f.name: row[f.name] for f in fields(cls) if f.name in row})
                for row in deepcopy(current[key])]
    findings = load(engine.RiskFinding, "risk_findings")
    recs = load(engine.Recommendation, "recommendations")
    dispositions = load(engine.FinalDisposition, "final_dispositions")
    finding = next(f for f in findings if "TC-03-04" in f.source_review_ids)
    rec = next(r for r in recs if finding.finding_id in r.source_finding_ids)
    fragment = rec.fragments[0]
    if mutation == "covered_id":
        fragment["source_element_ids"] = ["application_transfer_registration_documents"]
    elif mutation == "new_id":
        fragment["source_element_ids"] = ["invented_requirement"]
    elif mutation == "new_text":
        fragment["text"] += "；补充专利申请权转让登记文件和配合义务"
    else:
        rec.suggested_text += "另应补充登记文件和配合义务。"
    audit = engine._recommendation_truth_binding_audit(recs, findings, dispositions)
    assert engine._recommendation_truth_binding_gate(audit)["status"] == "BLOCKED"
