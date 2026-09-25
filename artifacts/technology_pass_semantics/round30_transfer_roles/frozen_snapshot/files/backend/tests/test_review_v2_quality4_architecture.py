from review_v2.benchmark import GoldContract, run_regression_benchmark
from review_v2.engine import review_contract_v2
from review_v2.quality4 import validate_formula_ast


LEASE_TEXT = (
    "上海市房屋租赁合同。签订日期：2026年8月1日。"
    "根据《中华人民共和国合同法》及有关规定，双方订立本合同。"
    "第一条 房屋坐落于上海市浦东新区，产权清晰。"
    "第五条 月租金为3852元，支付方式为银行转账，每月5日前支付。"
    "第九条 乙方逾期不支付租金累计超过1个月的，甲方有权解除合同。"
    "第十条 乙方中途擅自退租的，应按剩余租期租金的2倍支付违约金。"
    "第十一条 双方协商不成的，向浦东新区人民法院起诉。"
)


def test_quality4_public_review_result_has_no_review_level_severity():
    output = review_contract_v2(LEASE_TEXT, "house_lease", use_llm=False)

    first = output["review_results_4_0"][0]
    assert "risk_level" not in first
    assert "severity" not in first
    assert {"review_id", "applicable", "coverage_status", "priority", "facts", "evidence", "related_finding_ids", "confidence"} <= set(first)
    assert all("severity" in finding for finding in output["risk_findings"])
    assert output["release_quality_gate"]["status"] == "REPORT_READY"
    assert output["quality4_gate"]["status"] == "REPORT_READY"


def test_quality4_risk_ontology_aggregation_and_recommendation_are_finding_driven():
    output = review_contract_v2(LEASE_TEXT, "house_lease", use_llm=False)

    by_review = {
        source: finding
        for finding in output["risk_findings"]
        for source in finding.get("source_review_ids", [])
    }
    early_findings = {by_review[item_id]["finding_id"] for item_id in ["HL-029", "HL-039"] if item_id in by_review}
    assert len(early_findings) == 1

    early = next(finding for finding in output["risk_findings"] if finding["finding_id"] in early_findings)
    assert early["risk_category"] == "termination"
    assert "HL-042" not in early["source_review_ids"]
    assert early["aggregation_signals"]["source_review_count"] >= 2
    assert early["severity_reason"]["dominant_factor"]

    recommendation_ids = set(early["recommendation_ids"])
    recs = [rec for rec in output["recommendations"] if rec["recommendation_id"] in recommendation_ids]
    assert recs
    assert early["finding_id"] in recs[0]["target_finding_ids"]
    assert recs[0]["type"] in {"MODIFY", "VERIFY", "OPTIONAL", "ADD"}


def test_quality4_context_legal_freshness_and_formula_validation_are_structured():
    output = review_contract_v2(LEASE_TEXT, "house_lease", use_llm=False)
    by_id = {item["item_id"]: item for item in output["items"]}

    assert output["contract_context"]["contract_type"] == "house_lease"
    assert output["contract_context"]["payment_frequency"] == "monthly"
    assert any(issue["status"] == "OUTDATED_REFERENCE" for issue in output["legal_reference_issues"])
    assert output["legal_authority_validation"]["results"][0]["entailment"] in {"PARTIAL", "SUPPORTS"}
    assert by_id["HL-039"]["decision_trace"]["formula_validation"]["status"] == "PASS"
    assert by_id["HL-039"]["decision_trace"]["calculation_provenance"]["units"]["currency"] == "CNY"


def test_quality4_benchmark_exposes_full_metric_shell_and_gold_metadata():
    result = run_regression_benchmark(
        [
            GoldContract(
                "reg-lease-quality4-001",
                "house_lease",
                LEASE_TEXT,
                {"release_quality_gate": "REPORT_READY", "formula_type": "remaining_term_rent_multiplier"},
                "regression",
                "MEDIUM",
                perspective="tenant",
                annotator="annotator-a",
                reviewer="reviewer-b",
                legal_version="cn-civil-code-2026-08-11",
            )
        ],
        lambda text, contract_type: review_contract_v2(text, contract_type, use_llm=False),
    )

    assert result["sample_status"] == "INSUFFICIENT SAMPLE SIZE"
    assert result["metrics"]["critical_fact_recall"] is None
    assert result["metrics"]["legal_citation_entailment_accuracy"] is None
    assert result["metrics"]["per_risk_category"] == {}
    assert "CONFIDENCE_OVERCLAIM" in result["failure_taxonomy"]
    assert result["cases"][0]["gold_metadata"]["annotator"] == "annotator-a"


def test_quality4_formula_ast_validator_blocks_unknown_or_directionless_formula():
    assert validate_formula_ast({"type": "daily_percentage", "rate": 0.005, "direction": "tenant_to_landlord"})["status"] == "PASS"
    assert validate_formula_ast({"type": "unknown_formula", "direction": "tenant_to_landlord"})["status"] == "BLOCK"
    assert validate_formula_ast({"type": "monthly_rent_multiplier", "multiplier": 2, "direction": "unspecified"})["status"] == "BLOCK"
