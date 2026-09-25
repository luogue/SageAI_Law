from copy import deepcopy
from types import SimpleNamespace

import pytest

from review_v2 import engine
from backend.tests.test_application_transfer_element_report_consistency import review


def test_partial_issue_and_advice_only_use_the_residual_gap():
    item = review([
        {"element_id": "shortfall", "status": "COVERED", "proposition": "不足部分继续赔偿已有约定", "evidence_ids": ["E1"]},
        {"element_id": "offset", "status": "PARTIALLY_COVERED",
         "proposition": "事项已有部分约定，但完整性仍不足",
         "residual_gap": "同一损失的抵扣规则及适用顺序"},
    ])
    state = engine._build_narrative_state(item)
    assert "已有部分约定" not in state["issue"]
    assert "不足部分继续赔偿" not in state["issue"]
    assert "抵扣规则" in state["issue"]
    assert "已有部分约定" not in state["recommendation"]
    assert "抵扣规则" in state["recommendation"]


def test_positive_preface_is_removed_from_a_residual_label():
    assert engine._uncovered_element_label({"proposition": "赔偿已有约定，但抵扣规则尚未明确"}) == "抵扣规则尚未明确"


@pytest.mark.parametrize("transaction,source,target", [
    ("TECHNOLOGY_TRANSFER", "被许可方", "受让方"),
    ("TECHNOLOGY_LICENSE", "受让方", "被许可方"),
])
def test_generated_search_and_elements_follow_transaction_but_quotes_do_not(transaction, source, target):
    text = f"取得{source}书面同意"
    item = review([{"element_id": "consent", "status": "MISSING", "proposition": text}])
    item.applicable_if = "受让人或被许可人按约实施"
    item.evidence_clauses = [
        {"source_type": "SOURCE_CLAUSE", "quote": text},
        {"source_type": "SEARCH_AUDIT", "quote": "未找到：" + text},
    ]
    item.decision_trace["specialized_search_audit"] = {"missing_elements": [text]}
    finding = SimpleNamespace(title=text, issue=text, consequence=text, recommendation=text,
                              evidence_bundle={"items": deepcopy(item.evidence_clauses),
                                               "absence_search": {"targets": [text]}})
    engine._normalize_technology_transaction_terminology([item], [finding], {"primary_subtype": transaction})
    assert target in item.coverage_elements[0]["proposition"]
    assert target in item.evidence_clauses[1]["quote"]
    assert target in str(finding.evidence_bundle["absence_search"])
    assert item.evidence_clauses[0]["quote"] == text
    assert item.applicable_if == "受让人或被许可人按约实施"


def test_shortfall_arrangement_is_covered_separately_from_remaining_coordination():
    item = review()
    item.item_id = "TC-12-04"
    text = "第一条 第三方知识产权责任\n乙方提供的技术侵犯第三方知识产权时，乙方负责处理并赔偿损失。\n第二条 违约责任\n任何一方违反本合同义务应承担违约金及赔偿责任。违约金不足以弥补损失的，不足部分继续赔偿。"
    engine._apply_technical_service_semantic_rules([item], text)
    rows = {row["element_id"]: row for row in item.coverage_elements}
    assert rows["penalty_shortfall_compensation"]["status"] == "COVERED"
    assert rows["special_general_liability_coordination"]["status"] == "MISSING"
    assert "不足部分" not in rows["special_general_liability_coordination"]["proposition"]
