from review_v2.engine import review_contract_v2


def _sale(price_clause: str, quality_clause: str = ""):
    return review_contract_v2(
        f"""
        买卖合同
        甲方为出卖人，乙方为买受人。
        第一条 产品A，单价420元/吨，数量500吨。{price_clause}
        第二条 甲方应于2026年9月1日前送货至乙方仓库，由乙方签收。
        第三条 乙方应在签收后十日内支付货款。
        第四条 产品应符合国家标准。{quality_clause}
        第五条 争议由合同履行地法院管辖。
        """,
        "sale",
        use_llm=False,
    )


def _by_id(output):
    return {item["item_id"]: item for item in output["items"]}


def test_positive_price_finding_requires_direct_support():
    cases = {
        "fixed": "单价固定为420元/吨。",
        "mutual": "价格调整须经双方书面协商一致。",
        "indexed": "价格按照上海地区公开水泥价格指数自动调整。",
    }
    for name, clause in cases.items():
        output = _sale(clause)
        assert not any(
            finding["risk_group"] == "sale_unilateral_price_adjustment"
            for finding in output["risk_findings"]
        ), name
        assert output["release_quality_gate"]["status"] == "REPORT_READY", name

    unilateral = _sale("卖方可根据市场行情自行调整价格。")
    finding = next(
        row for row in unilateral["risk_findings"]
        if row["risk_group"] == "sale_unilateral_price_adjustment"
    )
    assert finding["aggregation_signals"]["risk_claim"]["existence_type"] == "POSITIVE_EXISTENCE"
    assert {row["entailment_status"] for row in finding["supporting_evidence"]} == {"SUPPORTS"}


def test_price_clause_counterfactual_does_not_change_unrelated_reviews():
    fixed = _sale("单价固定为420元/吨。")
    unilateral = _sale("卖方可根据市场行情自行调整价格。")
    fixed_by_id = _by_id(fixed)
    unilateral_by_id = _by_id(unilateral)
    for review_id in ("S-00-04", "S-02-03", "S-03-02", "S-05-04"):
        assert fixed_by_id[review_id]["coverage_status"] == unilateral_by_id[review_id]["coverage_status"]


def test_sale_default_law_executes_without_changing_contract_coverage():
    output = _sale("")
    by_id = _by_id(output)
    for review_id in ("S-04-01", "S-04-02", "S-04-04"):
        item = by_id[review_id]
        assessment = item["decision_trace"]["default_law_assessment"]
        effective_gap = item["decision_trace"]["effective_gap"]
        assert assessment["executed"] is True
        assert assessment["default_law_relevant"] is True
        assert assessment["rule"]["authority_ids"]
        assert effective_gap["contract_coverage"] == item["coverage_status"]
        assert effective_gap["statutory_protection_scope"]
        assert effective_gap["remaining_gap"]


def test_partial_quality_remedy_narrative_uses_coverage_elements():
    output = _sale(
        "",
        "买受人发现质量问题应在10日内通知卖方，卖方负责更换或补发。",
    )
    item = _by_id(output)["S-06-03"]
    assert item["coverage_status"] == "部分覆盖"
    narrative = item["decision_trace"]["narrative_elements"]["result"]
    assert "已覆盖" in narrative
    assert "完全未约定" not in narrative
    assert "未约定质量异议处理机制" not in output["result"]
    assert output["observability"]["pre_render_quality_gate"]["gate_results"]["NARRATIVE_ELEMENT_CONSISTENCY_GATE"] == "PASS"


def test_quality6_2_debug_and_gate_surfaces_are_production_outputs():
    output = _sale("价格调整须经双方书面协商一致。")
    observability = output["observability"]
    assert observability["evidence_finding_debug_table"]
    assert observability["default_law_debug_table"]
    assert observability["confidence_debug_report"]
    assert observability["narrative_state_debug_report"]
    assert {
        "FINDING_EVIDENCE_GATE",
        "CROSS_LAYER_CONSISTENCY_GATE",
        "DEFAULT_LAW_COMPLETENESS_GATE",
        "NARRATIVE_ELEMENT_CONSISTENCY_GATE",
        "CONFIDENCE_VALIDATION_GATE",
    } <= set(observability["pre_render_quality_gate"]["gate_results"])


def test_sale_mutation_pack_and_profile_perspective():
    cases = {
        "sale_delivery_date_removed": _sale(""),
        "sale_risk_transfer_added": review_contract_v2(
            "买卖合同。产品A单价420元。标的物风险在交付前由出卖人承担，交付后由买受人承担。",
            "sale",
            use_llm=False,
        ),
        "sale_risk_transfer_removed": _sale(""),
        "sale_quality_remedy_partial": _sale("", "质量问题应在10日内通知，卖方负责更换。"),
        "sale_quality_remedy_full": _sale("", "质量问题应在10日内通知，可要求修理、更换、重作、退货、减少价款或赔偿损失。"),
        "sale_quality_remedy_none": _sale(""),
    }
    for name, output in cases.items():
        assert output["contract_context"]["user_perspective"] == "buyer", name
        assert all(item["decision_trace"]["user_perspective"] == "BUYER" for item in output["items"]), name
        assert output["release_quality_gate"]["status"] == "REPORT_READY", name


def test_positive_finding_gate_is_not_sale_only():
    for contract_type, text in (
        ("house_lease", "房屋租赁合同。出租人甲方，承租人乙方。月租金3000元。"),
        ("service", "服务合同。甲方提供咨询服务，乙方支付服务费。"),
    ):
        output = review_contract_v2(text, contract_type, use_llm=False)
        assert output["observability"]["pre_render_quality_gate"]["gate_results"]["FINDING_EVIDENCE_GATE"] == "PASS"
