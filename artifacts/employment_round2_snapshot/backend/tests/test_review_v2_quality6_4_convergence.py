import json

from review_v2.clause_parser import parse_contract_clauses
from review_v2.blind_runner import run_blind_benchmark
from review_v2.engine import (
    COVERAGE_NOT_APPLICABLE,
    PRIORITY_A_CORE,
    PRIORITY_B_PRACTICAL,
    ReviewItemResult,
    _apply_risk_dimensions,
    _narrative_state_debug_report,
    _overall_assessment,
    _priority_assessment_for_item,
    review_contract_v2,
)


def _items(output):
    return {item["item_id"]: item for item in output["items"]}


def test_default_law_preserves_contract_coverage_and_changes_residual_gap():
    output = review_contract_v2(
        "买卖合同。甲方为买方，乙方为卖方。产品A共10台，总价10000元，卖方送货至买方仓库。",
        "sale",
        use_llm=False,
    )
    item = _items(output)["S-04-01"]
    gap = item["decision_trace"]["effective_gap"]
    assert item["coverage_status"] == "缺失"
    assert gap["default_law_status"] == "CLEAR_DEFAULT"
    assert gap["default_protection"]
    assert "默认规则" in gap["residual_risk"]


def test_template_guidance_is_not_operative_force_majeure_evidence():
    guidance_text = """
        特别提示
        遇不可抗力，双方宜及时通知并提供证明。
        订立合同双方
        甲方：买方；乙方：卖方。
        第一条 产品A共10台。
        """
    body_text = """
        特别提示
        遇不可抗力，双方宜及时通知并提供证明。
        订立合同双方
        甲方：买方；乙方：卖方。
        第一条 产品A共10台。
        第十条 因不可抗力不能履行的，受影响方应及时书面通知并提供证明。
        """
    guidance_only = parse_contract_clauses(guidance_text)
    with_body = parse_contract_clauses(body_text)
    assert any(clause.block_type == "TEMPLATE_GUIDANCE" for clause in guidance_only)
    assert any(clause.block_type == "OPERATIVE_CLAUSE" and "第十条" in clause.text for clause in with_body)
    first = _items(review_contract_v2(guidance_text, "sale", use_llm=False))["S-00-06"]
    second = _items(review_contract_v2(body_text, "sale", use_llm=False))["S-00-06"]
    assert first["coverage_status"] == "缺失"
    assert second["coverage_status"] != "缺失"
    assert all(evidence["evidence_block_type"] == "OPERATIVE_CLAUSE" for evidence in second["evidence_clauses"])


def test_short_document_preserves_normal_unicode_guidance_block():
    clauses = parse_contract_clauses(
        "特别提示\n双方宜约定不可抗力通知。\n订立合同双方\n甲方：买方；乙方：卖方。"
    )
    assert any(clause.block_type == "TEMPLATE_GUIDANCE" for clause in clauses)
    assert any(clause.block_type == "OPERATIVE_CLAUSE" for clause in clauses)


def test_format_terms_applicability_requires_trigger_evidence():
    public_template = review_contract_v2(
        "政府发布的公开示范文本，双方协商填写并可协商修改。买卖合同。甲方为买方，乙方为卖方。",
        "sale",
        use_llm=False,
    )
    supplier_terms = review_contract_v2(
        "买卖合同。本合同由卖方提供、不可修改并用于重复使用；卖方不承担任何质量责任。甲方为买方，乙方为卖方。",
        "sale",
        use_llm=False,
    )
    public_item = _items(public_template)["S-00-07"]
    supplied_item = _items(supplier_terms)["S-00-07"]
    assert public_item["coverage_status"] == COVERAGE_NOT_APPLICABLE
    assert public_item["applicability"]["status"] == "NOT_APPLICABLE"
    assert supplied_item["applicability"]["status"] == "APPLICABLE"
    assert supplied_item["applicability"]["trigger_evidence"]
    assert supplied_item["applicability"]["confidence"] == "high"


def test_topic_evidence_does_not_pass_standard_precedence_element():
    topic_only = review_contract_v2(
        "买卖合同。第一条 产品质量执行国家标准GB-X及企业标准Q-Y。",
        "sale",
        use_llm=False,
    )
    precedence = review_contract_v2(
        "买卖合同。第一条 产品质量执行国家标准GB-X及企业标准Q-Y；标准冲突时以双方特别约定标准为准。",
        "sale",
        use_llm=False,
    )
    first = _items(topic_only)["S-06-01"]
    second = _items(precedence)["S-06-01"]
    first_elements = {row["element_id"]: row["status"] for row in first["coverage_elements"]}
    second_elements = {row["element_id"]: row["status"] for row in second["coverage_elements"]}
    assert first["coverage_status"] != "通过"
    assert first_elements["precedence_between_standards"] in {"MISSING", "UNCERTAIN"}
    assert second_elements["precedence_between_standards"] == "COVERED"


def test_narrative_priority_and_signability_are_structurally_explained():
    output = review_contract_v2(
        "买卖合同。甲方为买方，乙方为卖方。产品A共10台，合同总价10000元。",
        "sale",
        use_llm=False,
    )
    assert all(row["status"] == "PASS" for row in output["observability"]["narrative_state_debug_report"])
    priority = output["observability"]["pre_render_quality_gate"]["priority_consistency_verification"]
    assert priority["consistency"] == "CONSISTENT"
    decision = output["overall_assessment"]["signability_decision"]
    if output["risk_findings"]:
        assert decision["decision_finding_ids"]
        assert decision["reasons"]


def test_priority_mutation_default_law_can_mitigate_but_core_exposure_escalates():
    base = ReviewItemResult(
        item_id="MUT-01", node_id="sale_risk_transfer_delivery", title="风险转移", risk_level="高",
        status="缺失", risk_point_description="缺少约定", suggested_clause_example="", legal_basis_index="",
        legal_consequence_if_missing="责任不清", applicable_if="", matched_terms=[], coverage_status="缺失",
        issue_type="完全缺失", evidence_clauses=[], evidence_location="", reasoning_summary="缺失",
    )
    base.risk_group = "sale_risk_transfer_delivery"
    base.risk_severity = "HIGH"
    base.economic_impact = "low"
    base.decision_trace["default_law_status"] = "CLEAR_DEFAULT"
    base.decision_trace["effective_gap"] = {
        "default_strength": "strong", "residual_operational_risk": "low", "residual_legal_risk": "low"
    }
    mitigated = _priority_assessment_for_item(base)
    assert mitigated["priority"] in {PRIORITY_B_PRACTICAL, "C_OPTIMIZATION"}
    assert mitigated["decision"]["explanation"]

    base.node_id = "early_termination_financial_exposure"
    base.risk_group = "early_termination_financial_exposure"
    base.economic_impact = "critical"
    base.decision_trace["default_law_status"] = "NO_DEFAULT"
    base.decision_trace["effective_gap"] = {
        "default_strength": "none", "residual_operational_risk": "high", "residual_legal_risk": "high"
    }
    escalated = _priority_assessment_for_item(base)
    assert escalated["priority"] == PRIORITY_A_CORE


def test_blind_runner_locks_prediction_to_frozen_candidate(tmp_path):
    benchmark_root = tmp_path / "blind"
    contracts = benchmark_root / "contracts"
    contracts.mkdir(parents=True)
    (contracts / "SALE-BLIND-003.json").write_text(
        json.dumps({"contract_id": "SALE-BLIND-003", "contract_type": "sale", "text": "买卖合同。产品A。"}),
        encoding="utf-8",
    )
    manifest = tmp_path / "candidate_manifest.json"
    manifest.write_text(json.dumps({"candidate_hash": "candidate-6-4"}), encoding="utf-8")
    result = run_blind_benchmark(
        benchmark_root,
        tmp_path / "result",
        candidate_manifest_path=manifest,
        review_fn=lambda text, contract_type: {
            "contract_facts": {}, "items": [], "risk_findings": [], "recommendations": [], "result": "report"
        },
    )
    lock = result["summary"]["prediction_lock"]
    prediction_lock = lock["locks"]["SALE-BLIND-003"]
    assert lock["gold_loaded_during_prediction"] is False
    assert prediction_lock["candidate_hash"] == "candidate-6-4"
    assert prediction_lock["contract_hash"]
    assert prediction_lock["report_hash"]
    assert prediction_lock["structured_result_hash"]
    assert prediction_lock["locked"] is True
