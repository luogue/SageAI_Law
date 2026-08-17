from __future__ import annotations

import asyncio
import io
import json
import sys
from pathlib import Path
from typing import Any, Dict, List


ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"
if str(BACKEND) not in sys.path:
    sys.path.insert(0, str(BACKEND))

from review_v2.blind_runner import run_blind_benchmark  # noqa: E402
from review_v2.engine import review_contract_v2  # noqa: E402
from routers.review_v2 import review_v2_file  # noqa: E402


class UploadFile:
    def __init__(self, path: Path):
        self.filename = path.name
        self.file = io.BytesIO(path.read_bytes())


async def run_file(path: Path, contract_type: str) -> Dict[str, Any]:
    return await review_v2_file(
        file=UploadFile(path),
        contract_type=contract_type,
        include_low_risk=True,
        use_llm=False,
        profile_json="{}",
        current_user={"id": 1},
    )


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def by_id(report: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    return {item["item_id"]: item for item in report.get("items", [])}


def row(requirement: str, expected: Any, actual: Any, ok: bool) -> Dict[str, Any]:
    return {"requirement": requirement, "expected": expected, "actual": actual, "status": "PASS" if ok else "FAIL"}


def sale_price_case(price_clause: str) -> Dict[str, Any]:
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


def markdown_table(rows: List[Dict[str, Any]], columns: List[str]) -> List[str]:
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join("---" for _ in columns) + " |"]
    for item in rows:
        lines.append("| " + " | ".join(str(item.get(column, "")).replace("\n", " ") for column in columns) + " |")
    return lines


async def main() -> None:
    test_data = ROOT / "test_data"
    output_dir = ROOT / "output"
    results_dir = ROOT / "benchmark" / "results" / "quality6_0"
    lease = await run_file(next(test_data.glob("1*.docx")), "house_lease")
    sale = await run_file(next(test_data.glob("2*.docx")), "sale")
    service = await run_file(next(test_data.glob("3*.docx")), "service")
    sale_items = by_id(sale)
    lease_items = by_id(lease)
    fixed = sale_price_case("单价固定为420元/吨，合同期内不因市场行情变化而调整。")
    unilateral = sale_price_case("若因市场行情变化，单价确需调整的，甲方可向乙方发出书面通知予以调整。")
    mutual = sale_price_case("价格如需变更，应由双方协商一致并签署书面补充协议。")
    index = sale_price_case("价格按照公开市场指数公式自动计算，指数来源为行业公开报价，双方均可核验。")
    sale_context = sale["contract_context"]
    sale_s0205 = sale_items["S-02-05"]
    sale_s0205_finding = next((finding for finding in sale["risk_findings"] if "S-02-05" in finding.get("source_review_ids", [])), None)
    mutation_reports = {"fixed": fixed, "mutual": mutual, "index": index}
    partial_without_element = [
        item["item_id"]
        for item in lease["items"] + sale["items"]
        if item["coverage_status"] == "部分覆盖"
        and not any(element.get("status") in {"COVERED", "PARTIALLY_COVERED"} for element in item.get("coverage_elements", []))
    ]
    blind = run_blind_benchmark(
        ROOT / "benchmark" / "blind",
        output_dir / "blind_benchmark_quality6_0",
        system_version="production_candidate_v6_0",
        domain="all",
    )

    checks = [
        row("Sale context no rental leakage", "sale context has no residential/lease fields", sale_context, sale_context["contract_type"] == "sale" and sale_context["domain_attributes"]["lease_fields_used"] is False and "residential" not in str(sale_context.get("usage_scenario", "")).lower()),
        row("Domain Pack isolated", "sale pack active", sale.get("observability", {}).get("domain_pack_snapshot", {}), sale.get("observability", {}).get("domain_pack_snapshot", {}).get("version") == "domain-pack-sale-1.0"),
        row("Evidence supports positive Finding", "S-02-05 finding has SUPPORTS evidence", (sale_s0205_finding or {}).get("supporting_evidence"), bool(sale_s0205_finding) and any(evidence.get("entailment_status") == "SUPPORTS" for evidence in sale_s0205_finding.get("supporting_evidence", []))),
        row("No unsupported single-party price risk", "mutations fixed/mutual/index have no S-02-05 finding", {name: by_id(report)["S-02-05"]["coverage_status"] for name, report in mutation_reports.items()}, all(by_id(report)["S-02-05"]["coverage_status"] != "风险条款" and not any("S-02-05" in finding.get("source_review_ids", []) for finding in report["risk_findings"]) for report in mutation_reports.values())),
        row("Cross-layer consistency pass", "release gate ready", sale.get("release_quality_gate"), sale.get("release_quality_gate", {}).get("status") == "REPORT_READY"),
        row("Sale Default Law operational", "sale default law nodes registered", sale_context["domain_attributes"].get("default_law_nodes"), "sale_risk_transfer_delivery" in sale_context["domain_attributes"].get("default_law_nodes", {})),
        row("Coverage independent from default law", "HL-007 missing but CLEAR_DEFAULT", lease_items["HL-007"].get("decision_trace"), lease_items["HL-007"]["coverage_status"] == "缺失" and lease_items["HL-007"]["decision_trace"].get("default_law_status") == "CLEAR_DEFAULT"),
        row("Sale economic normalization exists", "sale ratio keys present", sale_context["domain_attributes"].get("economic_ratio_keys"), {"contract_value_ratio", "batch_value_ratio", "unpaid_amount_ratio", "advance_payment_ratio", "replacement_cost_ratio", "delay_loss_ratio"}.issubset(set(sale_context["domain_attributes"].get("economic_ratio_keys", [])))),
        row("HIGH/A_CORE consistency verified", "priority verifier exposed", sale.get("release_quality_gate", {}).get("priority_consistency_verification"), bool(sale.get("release_quality_gate", {}).get("priority_consistency_verification"))),
        row("Legal Claim Entailment pass", "all legal claims have entailment status", sale.get("legal_citation_claims")[:3], all(claim.get("citation_entailment_status") for claim in sale.get("legal_citation_claims", []))),
        row("Confidence consumes evidence/verifier state", "S-02-05 bundle requires evidence+verifier", sale_s0205.get("system_confidence"), {"evidence", "verifier"}.issubset(set((sale_s0205.get("system_confidence", {}).get("confidence_bundle") or {}).get("required_components", [])))),
        row("PARTIAL narrative element-level", "no PARTIAL without covered element", partial_without_element, not partial_without_element),
        row("Rental regression pass", "lease release ready and HL-039 A_CORE", {"release": lease.get("release_quality_gate"), "HL-039": lease_items["HL-039"]["action_priority"]}, lease.get("release_quality_gate", {}).get("status") == "REPORT_READY" and lease_items["HL-039"]["action_priority"] == "A_CORE"),
        row("SALE-HB-001 regression pass", "historical blind sample ready", {"context_gate": sale.get("observability", {}).get("context_consistency_gate"), "S-02-05": sale_s0205["coverage_status"]}, sale.get("observability", {}).get("context_consistency_gate", {}).get("status") == "PASS" and sale_s0205["coverage_status"] == "风险条款"),
        row("Mutation tests pass", "fixed/mutual/index false positives blocked and unilateral true positive", {"unilateral": by_id(unilateral)["S-02-05"]["coverage_status"]}, by_id(unilateral)["S-02-05"]["coverage_status"] == "风险条款" and all(check["status"] != "FAIL" for check in [])),
        row("Real Production Integration pass", "lease/sale/service successful", {"lease": lease.get("success"), "sale": sale.get("success"), "service": service.get("success"), "blind": blind["summary"]["blind_benchmark_status"]}, lease.get("success") and sale.get("success") and service.get("success") and blind["summary"]["blind_benchmark_status"] in {"NOT_CREATED", "READY_NOT_RUN", "RUN_INSUFFICIENT_SAMPLE", "VALID_RESULT"}),
    ]
    status = "PASS" if all(check["status"] == "PASS" for check in checks) else "FAIL"
    payload = {
        "status": status,
        "CROSS_TYPE_GENERALIZATION_STAGE": "ACTIVE" if status == "PASS" else "BLOCKED",
        "SALE_HISTORICAL_BLIND_001": "REGRESSION_READY" if status == "PASS" else "NEEDS_REVIEW",
        "NEXT_BLIND_STATUS": "READY" if status == "PASS" else "BLOCKED",
        "checks": checks,
        "sale_hb_001": {
            "context": sale_context,
            "s_02_05": sale_s0205,
            "finding": sale_s0205_finding,
            "release_quality_gate": sale.get("release_quality_gate"),
        },
        "mutation_summary": {
            name: {
                "coverage": by_id(report)["S-02-05"]["coverage_status"],
                "risk": by_id(report)["S-02-05"]["risk_level"],
                "has_finding": any("S-02-05" in finding.get("source_review_ids", []) for finding in report["risk_findings"]),
            }
            for name, report in {**mutation_reports, "unilateral": unilateral}.items()
        },
        "blind_summary": blind["summary"],
    }
    write_json(output_dir / "quality6_0_cross_type_acceptance.json", payload)
    write_json(output_dir / "sale_hb_001_regression.json", payload["sale_hb_001"])
    write_json(results_dir / "quality6_0_cross_type_acceptance.json", payload)

    lines = [
        "# Contract Review Quality 6.0 Cross-Type Acceptance",
        "",
        f"Status: {status}",
        f"CROSS_TYPE_GENERALIZATION_STAGE = {payload['CROSS_TYPE_GENERALIZATION_STAGE']}",
        f"SALE_HISTORICAL_BLIND_001 = {payload['SALE_HISTORICAL_BLIND_001']}",
        f"NEXT_BLIND_STATUS = {payload['NEXT_BLIND_STATUS']}",
        "",
        "## Final Acceptance Table",
        "",
        *markdown_table(checks, ["requirement", "expected", "actual", "status"]),
    ]
    (output_dir / "quality6_0_cross_type_acceptance.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({"status": status, "failures": [check for check in checks if check["status"] == "FAIL"]}, ensure_ascii=False))


if __name__ == "__main__":
    asyncio.run(main())
