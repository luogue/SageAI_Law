"""Run Quality 6.1 acceptance only through the production upload route."""

from __future__ import annotations

import asyncio
import io
import json
import sys
from pathlib import Path
from typing import Any, Dict


ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"
if str(BACKEND) not in sys.path:
    sys.path.insert(0, str(BACKEND))

from routers.review_v2 import review_v2_file  # noqa: E402


class _UploadFile:
    def __init__(self, path: Path):
        self.filename = path.name
        self.file = io.BytesIO(path.read_bytes())


async def _review(path: Path, contract_type: str) -> Dict[str, Any]:
    return await review_v2_file(
        file=_UploadFile(path),
        contract_type=contract_type,
        include_low_risk=True,
        use_llm=False,
        profile_json="{}",
        current_user={"id": "quality-6.1-audit"},
    )


def _check(condition: bool, expected: str, actual: Any) -> Dict[str, Any]:
    return {"expected": expected, "actual": actual, "status": "PASS" if condition else "FAIL"}


async def main() -> int:
    test_data = ROOT / "test_data"
    sale_path = next(test_data.glob("2*.docx"))
    rental_path = next(test_data.glob("1*.docx"))
    sale = await _review(sale_path, "sale")
    rental = await _review(rental_path, "house_lease")
    sale_items = {item["item_id"]: item for item in sale["items"]}
    unilateral = sale_items["S-02-05"]
    litigation_cost = sale_items["S-00-05"]
    quality_remedy = sale_items["S-06-03"]
    priority = sale["observability"]["pre_render_quality_gate"]["priority_consistency_verification"]

    requirements = {
        "real_production_entry": _check(
            sale["observability"]["production_call_graph"][2].endswith("review_v2.py:review_v2_file"),
            "review_v2_file",
            sale["observability"]["production_call_graph"][2],
        ),
        "sale_domain_pack": _check(
            sale["observability"]["domain_pack_snapshot"]["contract_type"] == "sale",
            "sale",
            sale["observability"]["domain_pack_snapshot"],
        ),
        "no_rental_context_leakage": _check(
            sale["contract_context"]["usage_scenario"] == "GENERAL_GOODS_SALE"
            and sale["profile"]["contract_scenario"] == "商品买卖",
            "GENERAL_GOODS_SALE / 商品买卖",
            {"context": sale["contract_context"]["usage_scenario"], "profile": sale["profile"]["contract_scenario"]},
        ),
        "positive_finding_evidence_gate": _check(
            unilateral["coverage_status"] == "风险条款"
            and any(e.get("entailment_status") == "SUPPORTS" for e in unilateral["evidence_clauses"]),
            "RISK_CLAUSE with SUPPORTS",
            {"coverage": unilateral["coverage_status"], "entailment": [e.get("entailment_status") for e in unilateral["evidence_clauses"]]},
        ),
        "litigation_cost_not_585": _check(
            not any(claim.get("article") == "第585条" for claim in litigation_cost["legal_references"]),
            "no Article 585",
            [claim.get("article") for claim in litigation_cost["legal_references"]],
        ),
        "element_narrative": _check(
            quality_remedy["coverage_status"] == "部分覆盖"
            and "未约定质量异议处理机制" not in quality_remedy["reasoning_summary"],
            "PARTIAL without contradictory missing narrative",
            quality_remedy["reasoning_summary"],
        ),
        "priority_verifier": _check(priority.get("executed") and bool(priority.get("consistency")), "executed", priority),
        "quality_gate_before_renderer": _check(
            sale["observability"]["pre_render_quality_gate"]["status"] == "REPORT_READY",
            "REPORT_READY before renderer",
            sale["observability"]["pre_render_quality_gate"]["status"],
        ),
        "sale_regression": _check(sale["release_quality_gate"]["status"] == "REPORT_READY", "REPORT_READY", sale["release_quality_gate"]["status"]),
        "rental_regression": _check(rental["release_quality_gate"]["status"] == "REPORT_READY", "REPORT_READY", rental["release_quality_gate"]["status"]),
    }
    passed = all(row["status"] == "PASS" for row in requirements.values())
    payload = {
        "production_implementation_audit": "PASS" if passed else "FAIL",
        "active_pipeline_verified": passed,
        "sale_hb_001_regression": requirements["sale_regression"]["status"],
        "rental_regression": requirements["rental_regression"]["status"],
        "next_blind_status": "READY" if passed else "NOT_READY",
        "requirements": requirements,
        "sale_output_hashes": sale["observability"]["output_hashes"],
        "rental_output_hashes": rental["observability"]["output_hashes"],
    }
    output = ROOT / "output"
    output.mkdir(exist_ok=True)
    (output / "quality6_1_production_audit.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    (output / "debug_trace.json").write_text(
        json.dumps({"sale": sale["observability"]["production_trace"], "rental": rental["observability"]["production_trace"]}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
