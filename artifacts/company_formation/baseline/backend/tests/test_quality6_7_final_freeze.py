from review_v2.clause_parser import parse_contract_clauses
from review_v2.domain_resolution import resolve_contract_domain
from review_v2.engine import _production_internal_token_gate, review_contract_v2
from review_v2.perspective_resolution import perspective_domain_consistency_gate, resolve_perspective
from review_v2.production_display import display_claim, production_fact_polarity_gate
from review_v2.recommendation_impact import evaluate_recommendations


FRAMEWORK = """
长期供货合同
甲方（采购方）与乙方（供应商）签订本框架采购合同。
本合同期限为两年，双方建立长期供货关系，不约定最低采购数量。
甲方根据实际生产需求下达正式采购订单，采购订单经乙方确认后生效，并确定每批产品名称、规格型号、预计采购数量和交货期限。
乙方应按确认订单分批供货，双方以自然月为一个结算周期并每月对账，按实际供货数量结算货款，交货地点以订单为准。
签收仅确认数量和外观，不等同于最终质量验收。
"""


def test_perspective_resolution_rejects_cross_domain_profile_role():
    resolution = resolve_perspective("个人租客/买方", "SALE", previous_context_role="LESSEE")
    assert resolution.canonical_role == "BUYER"
    assert resolution.display_role == "买方 / 需方"
    assert resolution.rejected_roles == ["LESSEE"]
    assert perspective_domain_consistency_gate(resolution)["status"] == "REPORT_READY"


def test_false_fact_polarity_survives_production_mapping():
    claim = display_claim("receipt_is_final_acceptance", {"value": False, "exists": True, "source_clause_ids": ["C1"]})
    assert "不等同于最终质量验收" in claim.user_statement
    assert "构成最终质量验收" not in claim.user_statement
    assert production_fact_polarity_gate([claim.to_public_dict()])["contradiction_count"] == 0


def test_framework_report_contains_human_meaning_not_internal_keys():
    result = review_contract_v2(FRAMEWORK, "house_lease", use_llm=False)
    assert result["perspective_resolution"]["canonical_role"] == "BUYER"
    assert "审查立场：买方 / 需方" in result["result"]
    assert "租客" not in result["result"]
    assert "dynamic_quantity" not in result["result"]
    assert "order_mechanism" not in result["result"]
    assert "统一商业事实图谱" not in result["result"]
    assert _production_internal_token_gate(result["result"])["count"] == 0


def test_default_law_effective_gap_keeps_contract_coverage_independent():
    text = "买卖合同。买受人无正当理由拒收时承担仓储费和二次运输费。"
    result = review_contract_v2(text, "sale", use_llm=False)
    item = next(row for row in result["items"] if row["node_id"] == "sale_risk_buyer_delay_acceptance")
    gap = item["decision_trace"]["effective_gap"]
    assert item["coverage_status"] in {"缺失", "部分覆盖"}
    assert gap["default_law_checked"] is True
    assert gap["effective_gap_valid"] is True
    assert "authority_ids" in gap
    assert "still_unprotected_elements" in gap


def test_adverse_buyer_recommendation_is_blocked_before_production():
    class Obj:
        def __init__(self, **values): self.__dict__.update(values)
    item = Obj(item_id="R1", coverage_elements=[{"status": "COVERED", "proposition": "货物送达买方指定地点后风险转移。"}], decision_trace={})
    finding = Obj(finding_id="F1", source_review_ids=["R1"], risk_group="delivery_risk")
    recommendation = Obj(recommendation_id="REC-1", target_finding_ids=["F1"], proposed_change="风险在货交第一承运人时转移。", suggested_text="")
    accepted, impacts, gate = evaluate_recommendations([recommendation], [finding], [item], "BUYER")
    assert accepted == []
    assert impacts[0].shifts_risk_to_user is True
    assert impacts[0].gate_result == "BLOCKED"
    assert gate["status"] == "REPORT_READY"
