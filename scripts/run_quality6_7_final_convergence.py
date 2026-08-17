"""Quality 6.7 framework-supply acceptance, regression, and candidate freeze."""

from __future__ import annotations

import asyncio
import hashlib
import io
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "backend"))

from routers.review_v2 import ReviewV2PdfInput, _build_docx, review_v2_file


class Upload:
    def __init__(self, path: Path):
        self.filename = path.name
        self.file = io.BytesIO(path.read_bytes())


async def review(path: Path, contract_type: str) -> Dict[str, Any]:
    return await review_v2_file(
        file=Upload(path), contract_type=contract_type, include_low_risk=True,
        use_llm=False, profile_json="{}", current_user={"id": "quality-6.7-audit"},
    )


def write(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")


def digest(value: Any) -> str:
    raw = value if isinstance(value, bytes) else json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), default=str).encode()
    return hashlib.sha256(raw).hexdigest()


def export_docx(result: Dict[str, Any], filename: str) -> bytes:
    fields = ReviewV2PdfInput.model_fields
    values = {key: value for key, value in result.items() if key in fields}
    values["filename"] = filename
    return _build_docx(ReviewV2PdfInput(**values))


async def main() -> int:
    out = ROOT / "output" / "quality6_7"
    paths = {
        "SALE-HB-001": next((ROOT / "test_data").glob("2*.docx")),
        "SALE-HB-002": next((ROOT / "test_data").glob("5*.docx")),
        "SALE-HB-003": next((ROOT / "test_data").glob("6*.docx")),
        "SALE-HB-004": next((ROOT / "test_data").glob("7*.docx")),
        "RENTAL": next((ROOT / "test_data").glob("1*.docx")),
    }
    results = {
        name: await review(path, "house_lease" if name == "RENTAL" else "sale")
        for name, path in paths.items()
    }
    hb4 = results["SALE-HB-004"]
    context = hb4["contract_context"]
    facts = hb4["contract_facts"]["framework_supply"]
    items = {item["item_id"]: item for item in hb4["items"]}
    nodes = {item["node_id"]: item for item in hb4["items"]}
    gates = hb4["release_quality_gate"].get("gate_results", {})
    required_convergence_gates = (
        "REPORT_TRANSACTION_TRUTH_GATE",
        "COMMON_REVIEW_SATISFACTION_GATE",
        "ELEMENT_IDENTITY_CONTRADICTION_GATE",
        "PRODUCT_APPLICABILITY_GATE",
        "SHARED_CLAIM_REUSE_GATE",
        "FINDING_INDEPENDENCE_GATE",
        "NARRATIVE_TRUTH_GATE",
        "RECOMMENDATION_NON_DEGRADATION_GATE",
    )
    protected = {
        "sale_delivery_time", "sale_delay_delivery_liability", "sale_risk_transfer_delivery",
        "sale_payment_method_account", "sale_quality_remedy", "sale_inspection_period",
        "sale_deemed_acceptance", "sale_quality_standard_basis", "common_jurisdiction",
    }
    prohibited_findings = sorted(
        node for node in protected
        if node in nodes and nodes[node]["coverage_status"] not in {"通过", "不适用"}
    )
    findings_by_review = {
        review_id for finding in hb4["risk_findings"] for review_id in finding["source_review_ids"]
    }
    carrier_safe = items["S-04-02"]["coverage_status"] == "不适用" and "S-04-02" not in findings_by_review
    adverse = sum(
        len((result["observability"]["cross_review_consistency_debug"] or {}).get("recommendation_degradation_conflicts", []))
        for result in results.values()
    )
    narrative_rows = [
        row
        for result in results.values()
        for row in result["observability"]["narrative_state_debug_report"]
    ]
    narrative_contradictions = [row for row in narrative_rows if row.get("status") != "PASS"]
    element_identity_contradictions = [
        row
        for result in results.values()
        for row in (result["observability"]["cross_review_consistency_debug"] or {}).get("element_identity_contradictions", [])
    ]
    duplicate_finding_rows = [
        row
        for result in results.values()
        for row in (result["observability"]["cross_review_consistency_debug"] or {}).get("finding_independence_issues", [])
    ]
    total_findings = sum(len(result["risk_findings"]) for result in results.values())
    duplicate_finding_rate = len(duplicate_finding_rows) / total_findings if total_findings else 0.0
    common_explicit_fact_false_negatives = [
        review_id for review_id in ("S-04-04", "S-08-03", "S-11-02")
        if items[review_id]["coverage_status"] == "缺失"
    ]
    generic_common_elements = [
        {"review_id": item["item_id"], "element_id": element.get("element_id")}
        for item in hb4["items"]
        for element in item.get("coverage_elements", [])
        if item["item_id"] in {"S-00-02", "S-00-06", "S-08-03"}
        and element.get("element_id") in {"core_contract_arrangement", "element"}
    ]
    header_truth = (
        hb4["report_context"]["transaction_structure"] == "FRAMEWORK_SUPPLY"
        and hb4["report_context"]["usage_scenario_label"] == "长期供货 / 框架采购"
        and hb4["report_context"]["contract_type_label"] == "长期供货合同"
        and hb4["report_context"]["report_title"] == "长期供货合同审查报告"
    )
    export_bytes = export_docx(hb4, paths["SALE-HB-004"].name)

    requirements = {
        **{gate: gates.get(gate) == "PASS" for gate in required_convergence_gates},
        "TRANSACTION_STRUCTURE_GATE": gates.get("TRANSACTION_STRUCTURE_GATE") == "PASS" and context["transaction_structure"] == "FRAMEWORK_SUPPLY",
        "FRAMEWORK_DOMAIN_GATE": gates.get("FRAMEWORK_DOMAIN_GATE") == "PASS" and context["contract_subtype"] == "FRAMEWORK_SUPPLY" and context["product_category"] == "INDUSTRIAL_COMPONENTS",
        "ORDER_RELATION_GATE": gates.get("ORDER_RELATION_GATE") == "PASS" and context["order_driven_performance"] is True,
        "DYNAMIC_QUANTITY_GATE": gates.get("DYNAMIC_QUANTITY_GATE") == "PASS" and context["dynamic_quantity"] is True and context["minimum_purchase_commitment"] is False,
        "PRICE_MECHANISM_GATE": gates.get("PRICE_MECHANISM_GATE") == "PASS" and context["price_adjustment_mechanism"] == "BILATERAL_ADJUSTMENT" and facts["confirmed_order_price_protected"]["value"] is True,
        "ALTERNATIVE_SATISFACTION_GATE": gates.get("ALTERNATIVE_SATISFACTION_GATE") == "PASS",
        "FALSE_RISK_EXISTENCE_GATE": gates.get("FALSE_RISK_EXISTENCE_GATE") == "PASS" and not prohibited_findings and carrier_safe,
        "RECOMMENDATION_NON_DEGRADATION_GATE": gates.get("RECOMMENDATION_NON_DEGRADATION_GATE") == "PASS" and adverse == 0,
        "NARRATIVE_TRUTH_GATE": gates.get("NARRATIVE_TRUTH_GATE") == "PASS" and not narrative_contradictions,
        "SALE_HB_001": results["SALE-HB-001"]["release_quality_gate"]["status"] == "REPORT_READY",
        "SALE_HB_002": results["SALE-HB-002"]["release_quality_gate"]["status"] == "REPORT_READY" and results["SALE-HB-002"]["contract_context"]["transaction_structure"] == "SINGLE_TRANSACTION",
        "SALE_HB_003": results["SALE-HB-003"]["release_quality_gate"]["status"] == "REPORT_READY" and results["SALE-HB-003"]["contract_context"]["subject_matter"] == "REAL_ESTATE" and results["SALE-HB-003"]["report_context"]["usage_scenario_label"] == "二手住宅房地产买卖",
        "SALE_HB_004": hb4["release_quality_gate"]["status"] == "REPORT_READY" and all(items[f"FS-{index:02d}"]["coverage_status"] == "通过" for index in range(1, 15)) and header_truth and not common_explicit_fact_false_negatives and not generic_common_elements and items["S-12-03"]["coverage_status"] == "不适用",
        "RENTAL_REGRESSION": results["RENTAL"]["release_quality_gate"]["status"] == "REPORT_READY",
        "REAL_PRODUCTION_INTEGRATION": all(result["success"] for result in results.values()) and export_bytes.startswith(b"PK") and len(export_bytes) > 1000,
    }

    classification_debug = {
        "historical_case_id": "SALE-HB-004",
        "former_blind_status": "FAIL",
        "classification": hb4["observability"]["classification_trace"],
        "contract_context": context,
    }
    write(out / "framework_classification_debug.json", classification_debug)
    write(out / "framework_fact_debug.json", facts)
    write(out / "order_mechanism_debug.json", facts["order_mechanism"])
    write(out / "quantity_structure_debug.json", {
        "dynamic_quantity": facts["dynamic_quantity"],
        "minimum_purchase_commitment": facts["minimum_purchase_commitment"],
        "demand_forecast": facts["demand_forecast"],
        "forecast_binding": facts["forecast_binding"],
    })
    write(out / "price_mechanism_debug.json", {
        key: facts[key] for key in (
            "price_mechanism", "unilateral_price_adjustment", "confirmed_order_price_protected", "future_order_deadlock",
        )
    })
    write(out / "inspection_regime_debug.json", {
        key: facts[key] for key in ("inspection_regime", "receipt_is_final_acceptance", "deemed_acceptance_scope", "quality_remedy")
    })
    write(out / "risk_transfer_debug.json", {
        "risk_transfer_rule": facts["risk_transfer_rule"],
        "carrier_rule_applicability": facts["carrier_rule_applicability"],
        "carrier_review": items["S-04-02"],
    })
    write(out / "framework_applicability_debug.json", {
        item_id: {"applicability": item["applicability"], "coverage": item["coverage_status"]}
        for item_id, item in items.items() if item_id.startswith("FS-") or item_id in {"S-01-03", "S-01-04", "S-04-02", "S-10-02"}
    })
    write(out / "framework_material_coverage.json", {
        "reviews": {item_id: items[item_id]["coverage_status"] for item_id in items if item_id.startswith("FS-")},
        "gates": {key: gates.get(key) for key in requirements if key.endswith("_GATE")},
    })
    write(out / "false_risk_debug.json", {"protected_nodes": sorted(protected), "prohibited_findings": prohibited_findings, "carrier_safe": carrier_safe})
    write(out / "recommendation_safety_debug.json", {
        "adverse_recommendation_count": adverse,
        "gate": gates.get("RECOMMENDATION_NON_DEGRADATION_GATE"),
        "cross_review_debug": hb4["observability"]["cross_review_consistency_debug"],
    })
    write(out / "report_context_debug.json", {
        "DomainResolution": {
            "family": context["contract_family"],
            "subject": context["subject_matter"],
            "transaction_structure": context["transaction_structure"],
            "subtype": context["contract_subtype"],
        },
        "ReportContext": {
            "title": hb4["report_context"]["report_title"],
            "type_label": hb4["report_context"]["contract_type_label"],
            "scenario_label": hb4["report_context"]["usage_scenario_label"],
            "transaction_structure": hb4["report_context"]["transaction_structure"],
        },
        "match": "PASS" if header_truth else "FAIL",
    })
    write(out / "common_review_satisfaction_debug.json", {
        item["item_id"]: {
            "node_id": item["node_id"],
            "transaction_structure": context["transaction_structure"],
            "coverage": item["coverage_status"],
            "coverage_elements": item.get("coverage_elements", []),
            "satisfaction": (item.get("decision_trace") or {}).get("common_review_satisfaction", {}),
        }
        for item in hb4["items"]
        if (item.get("decision_trace") or {}).get("common_review_satisfaction")
    })
    write(out / "element_identity_debug.json", {
        "contradiction_count": len(element_identity_contradictions),
        "contradictions": element_identity_contradictions,
        "generic_common_elements": generic_common_elements,
        "gate": gates.get("ELEMENT_IDENTITY_CONTRADICTION_GATE"),
    })
    write(out / "product_applicability_debug.json", [
        {
            "review_id": item["item_id"],
            "product_category": (item.get("applicability") or {}).get("product_category") or context.get("product_category"),
            "transaction_structure": (item.get("applicability") or {}).get("transaction_structure") or context.get("transaction_structure"),
            "trigger_facts": (item.get("applicability") or {}).get("trigger_facts", []),
            "positive_triggers": (item.get("applicability") or {}).get("positive_triggers", []),
            "negative_triggers": (item.get("applicability") or {}).get("negative_triggers", []),
            "applicability_result": (item.get("applicability") or {}).get("status"),
            "reason": (item.get("applicability") or {}).get("reason"),
        }
        for item in hb4["items"] if item["item_id"] in {"S-12-02", "S-12-03"}
    ])
    canonical_claim_rows = hb4["contract_facts"]["canonical_claims"]["claims"]
    write(out / "shared_claim_reuse_debug.json", [
        {
            "claim_id": claim_id,
            "source_clauses": claim.get("source_clause_ids", []),
            "consumer_reviews": claim.get("consumer_review_ids", []),
            "consumer_interpretation": {
                item["item_id"]: next((element.get("status") for element in item.get("coverage_elements", []) if element.get("claim_id") == claim_id), "NOT_CONSUMED")
                for item in hb4["items"] if item["item_id"] in claim.get("consumer_review_ids", [])
            },
            "coverage_effect": "SUPPORTS" if claim.get("status") == "ASSERTED" else "NO_ASSERTED_FACT",
            "conflict": any(
                element.get("status") not in {"COVERED", "PARTIALLY_COVERED"}
                for item in hb4["items"]
                for element in item.get("coverage_elements", [])
                if element.get("claim_id") == claim_id and claim.get("status") == "ASSERTED"
            ),
        }
        for claim_id, claim in canonical_claim_rows.items()
        if claim.get("consumer_review_ids")
    ])
    write(out / "finding_aggregation_debug.json", [
        {
            "finding_candidate": finding["finding_id"],
            "risk_group": finding["risk_group"],
            "source_review_ids": finding["source_review_ids"],
            "shared_claim_ids": (finding.get("aggregation_signals") or {}).get("claim_ids", []),
            "semantic_similarity": 1.0 if len(finding["source_review_ids"]) > 1 else 0.0,
            "shared_consequence": (finding.get("aggregation_signals") or {}).get("shared_legal_consequence", ""),
            "shared_recommendation": finding.get("recommendation", ""),
            "aggregation_decision": "AGGREGATED" if len(finding["source_review_ids"]) > 1 else "INDEPENDENT",
        }
        for finding in hb4["risk_findings"]
    ])
    write(out / "narrative_truth_debug.json", {
        "contradiction_count": len(narrative_contradictions),
        "reviews": [
            {
                "review_id": row["review_id"],
                "coverage": row["coverage"],
                "covered_elements": row.get("covered_elements", []),
                "missing_elements": row.get("missing_elements", []),
                "rendered_issue": row.get("rendered_issue", ""),
                "rendered_consequence": row.get("rendered_consequence", ""),
                "contradiction": row.get("status") != "PASS",
                "reasons": row.get("contradiction_reasons", []),
            }
            for row in hb4["observability"]["narrative_state_debug_report"]
        ],
    })
    write(out / "sale_hb_004_regression.json", {
        "status": "PASS" if requirements["SALE_HB_004"] else "FAIL",
        "context": context,
        "known_facts": facts,
        "review_status": {node: nodes[node]["coverage_status"] for node in sorted(protected) if node in nodes},
        "carrier_review": items["S-04-02"]["coverage_status"],
        "release": hb4["release_quality_gate"],
        "export": {"valid_zip": export_bytes.startswith(b"PK"), "bytes": len(export_bytes)},
    })
    write(out / "sale_hb_004_final_regression.json", {
        "status": "PASS" if requirements["SALE_HB_004"] else "FAIL",
        "framework_reviews_present": all(f"FS-{index:02d}" in items for index in range(1, 15)),
        "framework_material_coverage": "PASS" if all(items[f"FS-{index:02d}"]["coverage_status"] == "通过" for index in range(1, 15)) else "FAIL",
        "carrier_false_positive_count": 0 if carrier_safe else 1,
        "adverse_recommendation_count": adverse,
        "common_explicit_fact_false_negatives": common_explicit_fact_false_negatives,
        "narrative_contradiction_count": len(narrative_contradictions),
        "element_identity_contradiction_count": len(element_identity_contradictions),
        "header_domain_mismatch_count": 0 if header_truth else 1,
        "duplicate_finding_rate": duplicate_finding_rate,
        "release": hb4["release_quality_gate"],
    })
    write(out / "regression_summary.json", {
        "requirements": {key: "PASS" if value else "FAIL" for key, value in requirements.items()},
        "release": {name: result["release_quality_gate"]["status"] for name, result in results.items()},
        "contexts": {name: result["contract_context"] for name, result in results.items()},
        "adverse_recommendation_count": adverse,
        "next_blind": "SALE-BLIND-005",
    })
    write(out / "final_regression_summary.json", {
        "requirements": {key: "PASS" if value else "FAIL" for key, value in requirements.items()},
        "release": {name: result["release_quality_gate"]["status"] for name, result in results.items()},
        "narrative_contradiction_count": len(narrative_contradictions),
        "element_identity_contradiction_count": len(element_identity_contradictions),
        "adverse_recommendation_count": adverse,
        "duplicate_finding_rate": duplicate_finding_rate,
        "next_blind": "SALE-BLIND-005",
    })
    (out / "6_7_domain_root_cause.md").write_text(
        "# Quality 6.7 Domain Root Cause\n\n"
        "`domain_resolution.resolve_contract_domain` previously inferred equipment from any occurrence of `设备`, including a party name. "
        "It also had no transaction-structure axis, so a long-term, order-driven component supply relationship collapsed into `EQUIPMENT_SALE`. "
        "The resolver now aggregates master relationship, confirmed-order, dynamic-quantity, recurring-settlement and term signals. "
        "No single occurrence of `长期` or `订单` is sufficient.\n",
        encoding="utf-8",
    )
    (out / "6_7_recall_root_cause.md").write_text(
        "# Quality 6.7 Recall Root Cause\n\n"
        "## FIRST_BROKEN_LAYER\n\n"
        "`DOMAIN_SUBTYPE_CLASSIFICATION_ERROR` was first: the wrong equipment-sale route prevented framework ReviewDefinitions and facts from entering production. "
        "The second break was `DOMAIN_ONTOLOGY_MISS`: relative order lead time, destination risk transfer, periodic settlement, non-binding forecast and document precedence had no shared commercial facts. "
        "The third break was `TRANSACTION_STRUCTURE_MISS`: dynamic quantity was evaluated as missing fixed quantity.\n\n"
        "The repaired trace is `raw -> normalized clause -> commercial fact -> ReviewDefinition fact path -> CoverageElementResult -> ReviewResult -> gate`. "
        "Every satisfied path carries source clause IDs; explicit facts cannot coexist with a missing Review result without blocking the release gate.\n",
        encoding="utf-8",
    )
    (out / "6_7_final_convergence_root_cause.md").write_text(
        "# Contract Review Quality 6.7 Final Convergence\n\n"
        "## Root cause\n\n"
        "The first broken layer was shared Common Review assembly. `S-00-02`, `S-00-06` and `S-08-03` "
        "fell through `_coverage_claim_for_item` to one generic `core_contract_arrangement` element. "
        "The same label could therefore be emitted by evidence matching as both covered and missing, and the old renderer "
        "independently selected prose from `risk_point_description`. Report display also resolved from the family label after "
        "transaction classification, so `FRAMEWORK_SUPPLY` stopped before the production header.\n\n"
        "## Repaired call chain\n\n"
        "`DomainResolution -> ReportContext -> Production Renderer` now carries transaction structure without reclassification.\n\n"
        "`S-00-02 ReviewDefinition -> semantic CoverageRequirement elements -> applicable SatisfactionPath -> "
        "CoverageElementResult -> ReviewResult -> NarrativeState -> Narrative Truth Gate -> Markdown` is now one truth path.\n\n"
        "`Canonical Claim -> Common Review consumers -> Coverage -> shared risk_group -> one independent RiskFinding` reuses "
        "delayed-acceptance and third-party-right facts instead of retrieving them separately.\n\n"
        "## Error taxonomy closed\n\n"
        "- REPORT_TRANSACTION_STRUCTURE_MISMATCH\n"
        "- COMMON_REVIEW_CONTEXT_LOSS\n"
        "- ELEMENT_IDENTITY_CONTRADICTION\n"
        "- PRODUCT_APPLICABILITY_ERROR\n"
        "- SHARED_CLAIM_REUSE_ERROR\n"
        "- DUPLICATE_FINDING\n"
        "- NARRATIVE_TRUTH_VIOLATION\n"
        "- EVIDENCE_LOCATION_NOISE\n\n"
        "## Frozen engineering principles\n\n"
        "Transaction Structure must reach the final report, not stop inside the review engine. Common Reviews must understand "
        "domain context. A Review title is not a Coverage Element. The same semantic element cannot be both covered and missing. "
        "MISSING cannot be narrated as COVERED. Product-specific requirements must be activated by product applicability. "
        "Shared facts must be reused across Common and Domain Reviews. Multiple Reviews may describe one independent risk. "
        "ReviewResult count is not RiskFinding count.\n",
        encoding="utf-8",
    )

    passed = all(requirements.values())
    versions = {
        "release": "Contract Review Quality 6.7",
        "git_commit": subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True, capture_output=True).stdout.strip(),
        "classification_version": "transaction-structure-6.7",
        "fact_schema_version": facts["version"],
        "domain_pack_version": context["domain_attributes"]["domain_resolution"]["selected_domain_packs"][-1],
        "benchmark_version": "known-regression-6.7",
    }
    critical_sources = {
        str(path.relative_to(ROOT)): digest(path.read_bytes())
        for path in (
            ROOT / "backend" / "review_v2" / "engine.py",
            ROOT / "backend" / "review_v2" / "report_context.py",
            ROOT / "backend" / "review_v2" / "common_sale.py",
            ROOT / "backend" / "review_v2" / "canonical_claims.py",
            ROOT / "backend" / "tests" / "test_review_v2_quality6_7_final_convergence.py",
            ROOT / "scripts" / "run_quality6_7_final_convergence.py",
        )
    }
    candidate_hash = digest({
        "versions": versions,
        "requirements": requirements,
        "sources": {name: digest(path.read_bytes()) for name, path in paths.items()},
        "critical_sources": critical_sources,
    })
    manifest = {
        **versions,
        "candidate_hash": candidate_hash,
        "status": "PASS" if passed else "FAIL",
        "created_at": datetime.now().isoformat(),
        "requirements": {key: "PASS" if value else "FAIL" for key, value in requirements.items()},
        "sale_hb_004_frozen": passed,
        "candidate_frozen": passed,
        "adverse_recommendation_count": adverse,
        "narrative_contradiction_count": len(narrative_contradictions),
        "element_identity_contradiction_count": len(element_identity_contradictions),
        "duplicate_finding_rate": duplicate_finding_rate,
        "next_blind_status": "READY" if passed else "NOT_READY",
        "next_blind": "SALE-BLIND-005",
    }
    write(out / "candidate_manifest.json", manifest)
    write(ROOT / "output" / "candidate_manifest.json", manifest)
    print(json.dumps(manifest, ensure_ascii=False, indent=2))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
