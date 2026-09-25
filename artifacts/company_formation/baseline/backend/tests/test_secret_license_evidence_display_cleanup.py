"""Focused synthetic checks; intentionally do not rerun an accepted contract."""
import pytest

from review_v2.clause_parser import ParsedClause
from review_v2.engine import (
    _recommendation_action_for_element,
    _secret_loss_fee_subject,
    _technical_secret_transfer_proof_results,
)


def clause(key, title, text, section="正式合同条款"):
    return ParsedClause(key, title, title, text, section, 1)


def test_secret_identity_prefers_operative_scope_over_payment_document_reference():
    clauses = [
        clause("PAY", "付款", "支付价款时提交技术资料交付清单、技术秘密说明书、技术秘密清单。"),
        clause("RECITAL", "鉴于", "许可方拥有精密加工专有技术。"),
        clause("DEF", "定义", "技术资料是指载有技术参数、操作规程及控制程序的资料。"),
        clause("GRANT", "许可", "许可方提供精密加工专有技术，范围为生产线的控制及调试。"),
        clause("ANNEX", "技术资料范围附件", "技术资料交付清单：控制程序、工艺参数及操作手册。", "附件"),
        clause("WARRANTY", "权利保证", "许可方保证有权许可并提供上述专有技术。"),
    ]
    elements, evidence, _ = _technical_secret_transfer_proof_results(clauses)
    identity = next(row for row in elements if row["element_id"] == "technical_secret_identity_and_delivery_scope")
    assert identity["status"] == "COVERED"
    assert {"RECITAL", "DEF", "GRANT", "ANNEX"} <= set(identity["bound_evidence_ids"])
    assert "PAY" not in identity["bound_evidence_ids"]
    assert evidence[0]["clause_id"] != "PAY"
    warranty = next(row for row in evidence if row["clause_id"] == "WARRANTY")
    assert warranty["evidence_level"] == "CONTRACTUAL_REPRESENTATION"
    authority = next(row for row in elements if row["element_id"] == "disposition_authority")
    assert authority["status"] != "COVERED"


def test_payment_reference_remains_fallback_without_new_proof_inference():
    elements, evidence, _ = _technical_secret_transfer_proof_results([
        clause("PAY", "付款", "支付时提交技术资料交付清单。"),
    ])
    assert evidence[0]["clause_id"] == "PAY"
    assert elements[0]["status"] == "COVERED"


@pytest.mark.parametrize("text", [
    "许可价款为固定总价120万元，包含技术服务费，分三期支付。",
    "许可价款为固定总价120万元，技术指导已计入。本合同不采用提成费支付。",
    "合同总价包括技术服务。若后续采用提成支付，另行协商提成率。",
])
def test_fixed_fee_drafting_does_not_invent_royalties(text):
    fees = _secret_loss_fee_subject(text)
    action, _ = _recommendation_action_for_element({
        "element_id": "future_fee_after_secret_loss",
        "proposition": f"秘密性丧失后{fees}的停止、调减及结算规则。",
    })
    assert "提成" not in action
    assert "尚未支付的许可价款" in action
    assert "未履行服务对应价款" in action


def test_actual_royalty_and_mixed_payment_remain_in_drafting():
    fees = _secret_loss_fee_subject("入门费100万元。另按净销售额的3%支付提成费。")
    assert "尚未发生的提成费" in fees
    assert "尚未支付的许可价款" in fees
    assert "服务" not in fees
