from __future__ import annotations

from review_v2.engine import (
    ReviewItemResult,
    _apply_element_level_narratives,
    _element_identity_contradictions,
    review_contract_v2,
)
from review_v2.report_context import build_report_context


def _item(*, coverage: str, elements: list[dict]) -> ReviewItemResult:
    return ReviewItemResult(
        item_id="MUT-01",
        node_id="mutation_review",
        title="变异审查项",
        risk_level="低",
        status="待处理",
        risk_point_description="",
        suggested_clause_example="",
        legal_basis_index="",
        legal_consequence_if_missing="",
        applicable_if="",
        matched_terms=[],
        coverage_status=coverage,
        issue_type="",
        evidence_clauses=[{"clause_id": "C1", "text": "书面通知", "location": "第一条"}] if coverage == "部分覆盖" else [],
        evidence_location="",
        reasoning_summary="",
        applicability={"status": "APPLICABLE", "applicable": True},
        coverage_elements=elements,
    )


def test_report_context_display_priority_is_transaction_aware():
    common = {
        "contract_family": "SALE",
        "subject_matter": "GOODS",
        "transaction_structure": "SINGLE_TRANSACTION",
        "contract_subtype": "GENERAL_GOODS_SALE",
    }
    single = build_report_context(common).to_public_dict()
    framework = build_report_context({
        **common,
        "transaction_structure": "FRAMEWORK_SUPPLY",
        "contract_subtype": "FRAMEWORK_SUPPLY",
    }).to_public_dict()
    real_estate = build_report_context({
        **common,
        "subject_matter": "REAL_ESTATE",
        "contract_subtype": "RESIDENTIAL_SECONDARY_REAL_ESTATE_SALE",
    }).to_public_dict()

    assert single["usage_scenario_label"] == "商品买卖"
    assert framework["usage_scenario_label"] == "长期供货 / 框架采购"
    assert framework["report_title"] == "长期供货合同审查报告"
    assert real_estate["usage_scenario_label"] == "二手住宅房地产买卖"


def test_element_identity_gate_blocks_same_element_in_two_truth_buckets():
    item = _item(
        coverage="部分覆盖",
        elements=[
            {"element_id": "notice", "proposition": "书面通知", "status": "COVERED", "evidence_ids": ["E1"]},
            {"element_id": "notice", "proposition": "书面通知", "status": "MISSING", "evidence_ids": []},
        ],
    )
    assert _element_identity_contradictions([item]) == [
        {"review_id": "MUT-01", "element_ids": ["notice"]}
    ]


def test_narrative_state_uses_element_truth_without_independent_inference():
    missing = _apply_element_level_narratives([
        _item(
            coverage="缺失",
            elements=[{"element_id": "cure", "proposition": "补救期限", "status": "MISSING", "evidence_ids": []}],
        )
    ])[0]
    partial = _apply_element_level_narratives([
        _item(
            coverage="部分覆盖",
            elements=[
                {"element_id": "notice", "proposition": "通知", "status": "COVERED", "evidence_ids": ["E1"]},
                {"element_id": "cure", "proposition": "补救期限", "status": "MISSING", "evidence_ids": []},
            ],
        )
    ])[0]

    assert "已覆盖" not in missing.narrative_state["judgment"]
    assert "已覆盖：通知" in partial.narrative_state["judgment"]
    assert "尚未覆盖：补救期限" in partial.narrative_state["judgment"]


def test_framework_common_reviews_share_claims_and_product_applicability():
    text = (
        "双方建立两年长期供货合作，产品为工业端子和连接组件。"
        "买方每月发出书面采购订单，卖方确认后生效；本协议不约定最低采购数量，"
        "具体数量以买方实际下达并经卖方确认的订单为准，按件计量；"
        "每月按照订单、送货单和实际收货数量对账结算。"
        "订单未另行约定时，卖方应在确认订单后七日内送货。"
        "买方无正当理由拒收的，应承担合理仓储费及二次运输费。"
        "一方侵害第三方合法权益的，由责任方负责处理、承担相应责任并赔偿损失。"
    )
    result = review_contract_v2(text, "sale", use_llm=False)
    by_id = {item["item_id"]: item for item in result["items"]}
    by_node = {item["node_id"]: item for item in result["items"]}

    assert result["contract_context"]["transaction_structure"] == "FRAMEWORK_SUPPLY"
    assert by_node["sale_subject_quantity_unit"]["coverage_status"] == "通过"
    assert by_node["sale_delivery_time"]["coverage_status"] == "通过"
    assert by_id["S-04-04"]["coverage_status"] == "部分覆盖"
    assert by_id["S-11-02"]["coverage_status"] == "部分覆盖"
    assert by_id["S-12-03"]["coverage_status"] == "不适用"
    rights_findings = [
        finding for finding in result["risk_findings"]
        if set(finding["source_review_ids"]) & {"S-11-01", "S-11-03", "S-11-04"}
    ]
    assert len(rights_findings) == 1


def test_complex_equipment_activates_manual_review():
    result = review_contract_v2(
        "买方购买自动化生产设备一套，卖方负责现场安装、调试和试运行，并提供操作培训。总价十万元，验收后付款。",
        "sale",
        use_llm=False,
    )
    by_id = {item["item_id"]: item for item in result["items"]}
    assert by_id["S-12-03"]["applicability"]["status"] == "APPLICABLE"
    assert by_id["S-12-03"]["coverage_status"] != "不适用"
