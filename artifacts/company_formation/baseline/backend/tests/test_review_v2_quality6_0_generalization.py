from review_v2.engine import review_contract_v2
from review_v2.quality4 import build_contract_context, default_law_status
from review_v2.domain_packs import get_domain_pack


def _by_id(output):
    return {item["item_id"]: item for item in output["items"]}


def _sale_price_case(price_clause: str):
    return review_contract_v2(
        f"""
        水泥买卖合同
        甲方为出卖人，乙方为买受人。
        第一条 标的物为普通硅酸盐水泥。{price_clause}
        第二条 甲方负责运输，乙方签收后确认收货。
        第三条 乙方应在签收后十日内支付货款。
        """,
        "sale",
        use_llm=False,
    )


def test_quality6_contract_context_is_domain_isolated_across_types():
    lease = build_contract_context("house_lease", {"rent": {"monthly_amount": "3852", "payment_cycle": "月付"}, "lease_term": {"text": "一年"}}, contract_text="房屋租赁合同")
    sale = build_contract_context("sale", {}, contract_text="水泥买卖合同，单价420元/吨")
    service = build_contract_context("service", {}, contract_text="服务合同")
    sale_again = build_contract_context("sale", {}, contract_text="货物买卖合同")

    assert lease.usage_scenario == "residential_living"
    assert lease.deposit is None
    assert sale.usage_scenario == "GENERAL_GOODS_SALE"
    assert sale.transaction_purpose == "goods_sale"
    assert sale.domain_attributes["lease_fields_used"] is False
    assert "residential" not in sale.usage_scenario.lower()
    assert service.domain_attributes["lease_fields_used"] is False
    assert sale_again.usage_scenario == "GENERAL_GOODS_SALE"


def test_quality6_sale_domain_pack_default_law_and_economic_keys_are_isolated():
    sale_pack = get_domain_pack("sale")
    lease_pack = get_domain_pack("house_lease")

    assert sale_pack.version == "domain-pack-sale-1.0"
    assert lease_pack.version == "domain-pack-house-lease-1.0"
    assert default_law_status("sale_risk_transfer_delivery") == "PARTIAL_DEFAULT"
    assert default_law_status("sale_quality_liability") == "PARTIAL_DEFAULT"
    assert "contract_value_ratio" in sale_pack.economic_ratio_keys
    assert "delay_loss_ratio" in sale_pack.economic_ratio_keys


def test_quality6_sale_unilateral_price_mutations_do_not_false_positive():
    cases = {
        "fixed": _sale_price_case("单价固定为420元/吨，合同期内不因市场行情变化而调整。"),
        "mutual": _sale_price_case("价格如需变更，应由双方协商一致并签署书面补充协议。"),
        "index": _sale_price_case("价格按照公开市场指数公式自动计算，指数来源为行业公开报价，双方均可核验。"),
    }

    for name, output in cases.items():
        item = _by_id(output)["S-02-05"]
        assert item["coverage_status"] != "风险条款", {
            "case": name,
            "coverage": item["coverage_status"],
            "reason": item["reasoning_summary"],
            "evidence": item["evidence_clauses"],
        }
        assert not any("S-02-05" in finding.get("source_review_ids", []) for finding in output["risk_findings"]), name
        assert (output["release_quality_gate"] or {}).get("status") == "REPORT_READY"


def test_quality6_sale_unilateral_price_true_positive_requires_supporting_evidence():
    output = _sale_price_case("若因市场行情变化，单价确需调整的，甲方可向乙方发出书面通知予以调整。")
    item = _by_id(output)["S-02-05"]
    finding = next(finding for finding in output["risk_findings"] if "S-02-05" in finding.get("source_review_ids", []))

    assert item["coverage_status"] == "风险条款"
    assert any(evidence.get("entailment_status") == "SUPPORTS" for evidence in item["evidence_clauses"])
    assert any(evidence.get("entailment_status") == "SUPPORTS" for evidence in finding["supporting_evidence"])


def test_quality6_sale_historical_blind_regression_context_and_gates():
    output = review_contract_v2(
        """
        水泥买卖合同
        有关货物的名称、规格、单价详见如下表格：硅酸盐水泥P.O42.5，单价420元/吨。
        若因市场行情变化，单价确需调整的，甲方可向乙方发出书面通知予以调整。
        乙方应在签收后十日内支付货款。
        """,
        "sale",
        use_llm=False,
    )

    context = output["contract_context"]
    assert context["contract_type"] == "sale"
    assert context["domain_attributes"]["domain_pack"] == "domain-pack-sale-1.0"
    assert context["domain_attributes"]["lease_fields_used"] is False
    assert output["observability"]["context_consistency_gate"]["status"] == "PASS"
    assert output["benchmark_metrics"]["unsupported_positive_finding_rate"] == 0
    assert output["system_metadata"]["cross_type_generalization_stage"] == "CONVERGED"
    assert output["system_metadata"]["sale_historical_blind_001"] == "FROZEN_REGRESSION"
    assert output["system_metadata"]["next_blind_status"] == "READY"
