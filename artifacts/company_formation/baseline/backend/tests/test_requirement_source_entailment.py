"""Related clauses must not inherit an unrelated identity requirement tag."""
from copy import deepcopy

import pytest

from review_v2 import engine
from review_v2.clause_parser import ParsedClause
from review_v2.requirement_entailment import SECRET_IDENTITY_REQUIREMENT, technical_secret_identity_support


RELATED_NOT_SUPPORTING = [
    "买方违反许可范围及禁止擅自向第三方提供技术秘密的约定，应停止违约行为并赔偿可证明损失。",
    "未经卖方同意，买方不得向第三方转让、许可或提供本项技术秘密。",
    "卖方曾向某公司授予本项技术秘密的普通实施许可。",
    "买方为生产目的复制和使用相关技术资料及源代码。",
    "卖方保证其有权许可并提供上述专有技术。",
    "技术秘密内容尚未明确。",
    "许可方应提供技术秘密。",
    "许可方须提供本合同所需的技术秘密。",
]


@pytest.mark.parametrize("text", RELATED_NOT_SUPPORTING)
def test_mention_of_technology_is_not_identity_or_delivery_scope(text):
    assert not technical_secret_identity_support(text)


@pytest.mark.parametrize("text", [
    "技术秘密名称：柔性加工误差补偿技术。",
    "许可方拥有精密加工专有技术。",
    "技术秘密的内容：包括坐标转换算法、控制参数及核心源代码。",
    "技术资料是指载有技术参数、操作规程及控制程序的资料。",
    "许可方提供精密加工专有技术，范围为生产线的控制及调试。",
    "技术资料交付清单：控制程序、工艺参数及操作手册。",
])
def test_direct_definition_scope_and_delivery_list_remain_supporting(text):
    assert technical_secret_identity_support(text)


def test_identity_binding_uses_actual_scope_not_breach_or_historical_licence():
    clauses = [ParsedClause("scope", "第一条", "标的", "技术秘密内容：包括坐标转换算法和核心源代码。", "正式合同条款", 1)]
    clauses += [ParsedClause(str(i), "第十条", "其他安排", text, "正式合同条款", 1)
                for i, text in enumerate(RELATED_NOT_SUPPORTING)]
    elements, evidence, _ = engine._technical_secret_transfer_proof_results(clauses)
    identity = next(e for e in elements if e["element_id"] == SECRET_IDENTITY_REQUIREMENT)
    assert identity["status"] == "COVERED"
    assert identity["bound_evidence_ids"] == ["scope"]
    assert {f["clause_id"] for f in identity["supporting_evidence"]} == {"scope"}


@pytest.mark.parametrize("owner", ["element", "review", "items", "evidence_items", "tag", "bound_id"])
def test_release_gate_rejects_bad_support_edge_even_with_good_neighbour(owner):
    from tests.test_absence_search_target_integrity import review, finding
    item, risk = review(), finding()
    item.item_id = "TC-03-04"
    risk.source_review_ids = [item.item_id]
    good = {"clause_id": "good", "text": "技术秘密内容：包括坐标转换算法及核心源代码。",
            "supporting_element_ids": [SECRET_IDENTITY_REQUIREMENT]}
    bad = {"clause_id": "bad", "text": RELATED_NOT_SUPPORTING[0],
           "supporting_element_ids": [SECRET_IDENTITY_REQUIREMENT]}
    item.evidence_clauses = [good]
    if owner == "element":
        item.coverage_elements = [{"element_id": SECRET_IDENTITY_REQUIREMENT, "status": "COVERED",
                                   "proposition": "标的已明确", "supporting_evidence": [
                                       {"clause_id": "bad", "quote": bad["text"]}]}]
    elif owner == "review":
        item.evidence_clauses.append(bad)
    elif owner == "bound_id":
        item.evidence_clauses.append({"clause_id": "bad", "text": bad["text"]})
        item.coverage_elements = [{"element_id": SECRET_IDENTITY_REQUIREMENT, "status": "COVERED",
                                   "proposition": "标的已明确", "supporting_evidence_ids": ["bad"]}]
    elif owner == "tag":
        risk.evidence_bundle = {"items": [{"clause_id": "bad", "quote": bad["text"],
                                           "fact_type": SECRET_IDENTITY_REQUIREMENT.upper()}]}
    else:
        risk.evidence_bundle = {owner: [deepcopy(good), bad]}
    errors = engine._exact_element_report_invariants([item], [risk])
    assert any(e["reason"] == "REQUIREMENT_NOT_ENTAILED_BY_SOURCE" for e in errors)
    assert engine._release_quality_gate([item], [risk], "报告")["status"] == "BLOCKED"
