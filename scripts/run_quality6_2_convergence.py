"""Run Quality 6.2 acceptance through the production upload route."""

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
        current_user={"id": "quality-6.2-audit"},
    )


def _check(condition: bool, expected: str, actual: Any) -> Dict[str, Any]:
    return {"expected": expected, "actual": actual, "status": "PASS" if condition else "FAIL"}


async def main() -> int:
    sale = await _review(next((ROOT / "test_data").glob("2*.docx")), "sale")
    rental = await _review(next((ROOT / "test_data").glob("1*.docx")), "house_lease")
    sale_items = {item["item_id"]: item for item in sale["items"]}
    sale_findings = sale["risk_findings"]
    gates = sale["observability"]["pre_render_quality_gate"]["gate_results"]
    unilateral_findings = [row for row in sale_findings if row["risk_group"] == "sale_unilateral_price_adjustment"]
    unilateral_ok = all(
        row["supporting_evidence"]
        and all(evidence.get("entailment_status") == "SUPPORTS" for evidence in row["supporting_evidence"])
        for row in unilateral_findings
    )
    quality_remedy = sale_items["S-06-03"]
    default_rows = {
        row["review_id"]: row
        for row in sale["observability"]["default_law_debug_table"]
    }
    requirements = {
        "sale_context_preserved": _check(
            sale["profile"]["contract_scenario"] == "商品买卖"
            and sale["contract_context"]["user_perspective"] == "buyer"
            and all(item["decision_trace"]["user_perspective"] == "BUYER" for item in sale["items"]),
            "sale / buyer / 商品买卖",
            {"profile": sale["profile"], "context": sale["contract_context"]},
        ),
        "article_585_regression": _check(
            not any(claim.get("article") == "第585条" for claim in sale_items["S-00-05"]["legal_references"]),
            "litigation cost has no generic Article 585",
            sale_items["S-00-05"]["legal_references"],
        ),
        "positive_finding_entailment": _check(unilateral_ok, "SUPPORTS only", unilateral_findings),
        "cross_layer_consistency": _check(gates["CROSS_LAYER_CONSISTENCY_GATE"] == "PASS", "PASS", gates),
        "sale_default_law_executes": _check(
            all(review_id in default_rows and default_rows[review_id]["default_rule"] for review_id in ("S-04-01", "S-04-02", "S-04-04")),
            "structured default rules for risk transfer and delayed acceptance",
            default_rows,
        ),
        "coverage_default_independence": _check(
            all(
                sale_items[review_id]["decision_trace"]["effective_gap"]["contract_coverage"] == sale_items[review_id]["coverage_status"]
                for review_id in ("S-04-01", "S-04-02", "S-04-04")
            ),
            "effective gap preserves contract coverage",
            {review_id: sale_items[review_id]["decision_trace"]["effective_gap"] for review_id in ("S-04-01", "S-04-02", "S-04-04")},
        ),
        "confidence_gates": _check(gates["CONFIDENCE_VALIDATION_GATE"] == "PASS", "PASS", gates),
        "partial_element_narrative": _check(
            quality_remedy["coverage_status"] == "部分覆盖"
            and "未约定质量异议处理机制" not in sale["result"]
            and bool(quality_remedy["decision_trace"].get("narrative_elements")),
            "element-derived PARTIAL narrative",
            quality_remedy["decision_trace"].get("narrative_elements"),
        ),
        "all_new_gates": _check(all(value == "PASS" for value in gates.values()), "all PASS", gates),
        "sale_real_production": _check(sale["release_quality_gate"]["status"] == "REPORT_READY", "REPORT_READY", sale["release_quality_gate"]),
        "rental_regression": _check(rental["release_quality_gate"]["status"] == "REPORT_READY", "REPORT_READY", rental["release_quality_gate"]),
        "frozen_regression": _check(
            sale["system_metadata"]["sale_historical_blind_001"] == "FROZEN_REGRESSION"
            and sale["system_metadata"]["next_blind_status"] == "READY",
            "FROZEN_REGRESSION / READY",
            sale["system_metadata"],
        ),
    }
    passed = all(row["status"] == "PASS" for row in requirements.values())
    payload = {
        "sale_generalization_convergence": "PASS" if passed else "FAIL",
        "sale_hb_001_frozen": passed,
        "next_blind_status": "READY" if passed else "NOT_READY",
        "requirements": requirements,
        "root_causes": [
            {"problem": "Unsupported unilateral price Finding", "root_cause": "candidate evidence was copied to supporting_evidence and PARTIAL_SUPPORT was accepted for existence claims", "active_file": "backend/review_v2/engine.py", "function": "_build_risk_findings/_filter_unsupported_positive_findings", "general_fix": "RiskClaim existence_type plus SUPPORTS-only evidence gate"},
            {"problem": "Cross-layer contradiction not blocking", "root_cause": "only late report strings were checked", "active_file": "backend/review_v2/engine.py", "function": "_pre_render_quality_gate", "general_fix": "structured pre-render cross-layer gate"},
            {"problem": "Confidence ignores evidence contradiction", "root_cause": "confidence finalized before independent verification", "active_file": "backend/review_v2/engine.py", "function": "_apply_post_verification_confidence", "general_fix": "verifier and consistency become limiting components"},
            {"problem": "Sale Default Law not affecting residual risk", "root_cause": "domain pack stored only status strings", "active_file": "backend/review_v2/domain_packs.py", "function": "DefaultRule/get_default_rule", "general_fix": "structured applicability, scope and remaining gap"},
            {"problem": "PARTIAL narrative uses missing template", "root_cause": "renderer ignored CoverageElementResult", "active_file": "backend/review_v2/engine.py", "function": "_apply_element_level_narratives", "general_fix": "covered/missing elements own PARTIAL narrative"},
        ],
        "evidence_finding_debug_table": sale["observability"]["evidence_finding_debug_table"],
        "default_law_debug_table": sale["observability"]["default_law_debug_table"],
        "narrative_debug_table": sale["observability"]["narrative_state_debug_report"],
        "confidence_debug_table": sale["observability"]["confidence_debug_report"],
        "priority_debug_table": [
            {"review_id": item["item_id"], "severity": item["risk_severity"], "priority": item["review_priority"], "reason": item["decision_trace"].get("priority_assessment")}
            for item in sale["items"]
            if item["risk_severity"] in {"HIGH", "CRITICAL"} or item["review_priority"] == "A_CORE"
        ],
        "sale_hashes": sale["observability"]["output_hashes"],
        "rental_hashes": rental["observability"]["output_hashes"],
    }
    output = ROOT / "output"
    output.mkdir(exist_ok=True)
    (output / "quality6_2_convergence.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({
        "sale_generalization_convergence": payload["sale_generalization_convergence"],
        "sale_hb_001_frozen": payload["sale_hb_001_frozen"],
        "next_blind_status": payload["next_blind_status"],
        "requirements": {key: row["status"] for key, row in requirements.items()},
    }, ensure_ascii=True, indent=2))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
