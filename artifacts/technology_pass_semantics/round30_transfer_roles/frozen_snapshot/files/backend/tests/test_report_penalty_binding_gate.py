from copy import deepcopy
from types import SimpleNamespace

import pytest

from review_v2.narrative_evidence import narrative_evidence_gate


def case(period="每迟延一天", rate="0.1%"):
    quote = f"若因乙方原因导致迟延交付，{period}，乙方应按照合同总金额的{rate}向甲方支付违约金。"
    element = {"element_id": "penalty_obligation_1", "status": "ADVERSE",
               "proposition": quote, "bound_evidence_ids": ["C3"],
               "supporting_evidence": [{"clause_id": "C3", "quote": quote}]}
    item = SimpleNamespace(item_id="GEN-LIAB-03", coverage_elements=[element],
                           risk_point_description=quote, reasoning_summary="违约金达到每日0.1%。",
                           narrative_state={}, decision_trace={})
    row = {"evidence_id": "EV-direct", "clause_id": "C3", "quoted_text": quote,
           "supporting_element_ids": ["penalty_obligation_1"],
           "supporting_review_ids": [item.item_id], "source_type": "BODY",
           "evidence_role": "EXACT_ELEMENT_SOURCE"}
    finding = SimpleNamespace(finding_id="RF-test", source_review_ids=[item.item_id],
                              issue=quote, evidence_bundle={"items": [row]})
    return item, finding


@pytest.mark.parametrize("period", ["每迟延一天", "每逾期一日", "每延期1天", "每日", "每天"])
def test_daily_equivalent_with_exact_published_binding(period):
    item, finding = case(period)
    before = deepcopy((vars(item), vars(finding)))
    result = narrative_evidence_gate([item], [finding])
    assert result["mismatch_count"] == 0, result
    assert result["status"] == "REPORT_READY"
    claim = next(c for c in result["claims"] if c["field"] == "review_judgment")
    assert claim["element_ids"] == ["penalty_obligation_1"]
    assert claim["supporting_evidence_ids"] == ["EV-direct"]
    assert before == (vars(item), vars(finding))


@pytest.mark.parametrize("fault", ["wrong_target", "wrong_owner", "search_audit", "wrong_period", "wrong_rate"])
def test_rejected_binding_contains_actual_tuple(fault):
    item, finding = case("每月" if fault == "wrong_period" else "每迟延一天",
                         "0.2%" if fault == "wrong_rate" else "0.1%")
    row = finding.evidence_bundle["items"][0]
    if fault == "wrong_target":
        row["supporting_element_ids"] = ["theme_trigger"]
    if fault == "wrong_owner":
        row["supporting_review_ids"] = ["COMMON-20-01"]
    if fault == "search_audit":
        row["source_type"] = "SEARCH_AUDIT"
    result = narrative_evidence_gate([item], [finding])
    assert result["status"] == "BLOCKED"
    assert result["mismatch_count"] > 0
    rejection = next(f for f in result["failures"][0]["details"] if f["binding_diagnostics"])
    diagnostic = rejection["binding_diagnostics"][0]
    assert diagnostic["rule_id"] == "GEN-LIAB-03"
    assert diagnostic["fact_key"] == "penalty_obligation_1"
    assert diagnostic["report_evidence_id"] == "EV-direct"
    assert diagnostic["reject_reason"]


def test_daily_word_in_another_sentence_does_not_prove_rate_period():
    item, finding = case("每月")
    row = finding.evidence_bundle["items"][0]
    row["quoted_text"] += "乙方每日报告工作进度。"
    item.coverage_elements[0]["supporting_evidence"][0]["quote"] = row["quoted_text"]
    result = narrative_evidence_gate([item], [finding])
    assert result["status"] == "BLOCKED"
