from __future__ import annotations

import asyncio
import hashlib
import io
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List


ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"
if str(BACKEND) not in sys.path:
    sys.path.insert(0, str(BACKEND))

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


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def by_id(report: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    return {item["item_id"]: item for item in report.get("items", [])}


def number(value: Any) -> float | None:
    match = re.search(r"\d+(?:\.\d+)?", str(value))
    return float(match.group(0)) if match else None


def row(requirement: str, expected: Any, actual: Any, ok: bool) -> Dict[str, Any]:
    return {"requirement": requirement, "expected": expected, "actual": actual, "status": "PASS" if ok else "FAIL"}


def finding_for(report: Dict[str, Any], review_id: str) -> Dict[str, Any]:
    return next(finding for finding in report.get("risk_findings", []) if review_id in finding.get("source_review_ids", []))


def p0_checks(lease: Dict[str, Any], sale: Dict[str, Any]) -> List[Dict[str, Any]]:
    items = by_id(lease)
    facts = lease["contract_facts"]
    markdown = lease["result"]
    claims = lease["legal_citation_claims"]
    confidence_rows = lease["observability"]["confidence_debug_report"]
    legal_rows = lease["observability"]["legal_claim_debug_report"]
    narrative_rows = lease["observability"]["narrative_state_debug_report"]
    hl039 = items["HL-039"]
    hl040 = items["HL-040"]
    hl042 = items["HL-042"]
    hl043 = items["HL-043"]
    hl007 = items["HL-007"]
    hl008 = items["HL-008"]
    hl013 = items["HL-013"]
    hl037 = items["HL-037"]
    early = finding_for(lease, "HL-039")
    cases = {case["remaining_days"]: case for case in hl039["scenario_analysis"]["cases"]}
    direct_claims = [claim for claim in claims if claim.get("support_type") == "DIRECT_SUPPORT"]
    drafting_30 = [claim for claim in hl013["legal_references"] if claim.get("claim_type") == "DRAFTING_RECOMMENDATION"]
    explicit_fact_ids = ("HL-001", "HL-002", "HL-003", "HL-015", "HL-028", "HL-049")
    explicit_fact_conf = {review_id: items[review_id]["system_confidence"] for review_id in explicit_fact_ids}
    forbidden_engineering = ("LLM_PRIORITY", "DIRECT_SUPPORT", "PARTIAL_SUPPORT", "BACKGROUND_ONLY", "RF-", "Scenario Engine", "Fact Graph", "系统确定性")
    missing_bad_sections = []
    for item in lease["items"]:
        if item["coverage_status"] != "缺失":
            continue
        marker = f"（{item['item_id']}）"
        if marker not in markdown:
            continue
        section = markdown.split(marker, 1)[1].split("---", 1)[0]
        if any(term in section for term in ("已出现", "尚未完整覆盖", "已覆盖部分内容")):
            missing_bad_sections.append(item["item_id"])

    return [
        row("Confidence Bundle exists", "all 50 reviews expose bundle", len(confidence_rows), len(confidence_rows) == 50 and all((item.get("system_confidence") or {}).get("confidence_bundle") for item in lease["items"])),
        row("Dependency-aware confidence", "ignored components are not limiting factors", explicit_fact_conf, all("legal" in conf["confidence_bundle"]["ignored_components"] for conf in explicit_fact_conf.values())),
        row("Fact confidence independent from legal", "explicit facts not LOW due to legal uncertainty", explicit_fact_conf, all(conf["level"] in {"high", "medium"} for conf in explicit_fact_conf.values())),
        row("Explicit PASS facts no longer mechanically LOW", "clear PASS facts high/medium", {k: v["level"] for k, v in explicit_fact_conf.items()}, all(v["level"] != "low" for v in explicit_fact_conf.values())),
        row("MISSING can have calibrated confidence", "HL-042 missing with negative evidence not fake evidence", hl042["system_confidence"], hl042["coverage_status"] == "缺失" and hl042["system_confidence"]["level"] in {"high", "medium"} and not hl042["evidence_clauses"]),
        row("Negative review confidence works", "negative evidence search recorded", hl042["decision_trace"].get("negative_evidence"), (hl042["decision_trace"].get("negative_evidence") or {}).get("result") == "NOT_FOUND"),
        row("Citation claim-level mapping works", "legal debug rows have claim ids", legal_rows[:5], bool(legal_rows) and all(row_.get("claim_id") for row_ in legal_rows)),
        row("Citation support_scope required", "direct claims have non-empty support_scope", direct_claims, bool(direct_claims) and all(claim.get("support_scope") for claim in direct_claims)),
        row("No cross-claim citation propagation", "HL-008 does not inherit Article 732", hl008["legal_references"], all(claim.get("article") != "第732条" and not claim.get("authority_links") for claim in hl008["legal_references"])),
        row("Death continuation claim validated", "HL-007 Article 732 direct", hl007["legal_references"], any(claim.get("article") == "第732条" and claim.get("support_type") == "DIRECT_SUPPORT" for claim in hl007["legal_references"])),
        row("Death/no-successor claim independently validated", "HL-008 no direct authority", hl008["legal_references"], all(claim.get("citation_existence_status") == "NO_DIRECT_AUTHORITY" for claim in hl008["legal_references"])),
        row("Repair-cost legal claim independently validated", "HL-037 does not use penalty article as repair-cost basis", hl037["legal_references"], all(claim.get("article") != "第585条" for claim in hl037["legal_references"])),
        row("30-day drafting choice separated", "30-day claim is drafting choice only", drafting_30, bool(drafting_30) and all(not claim.get("authority_links") for claim in drafting_30) and "法定30" not in markdown),
        row("MISSING narrative invariant", "missing sections do not use partial narrative", missing_bad_sections, not missing_bad_sections and all(item["status"] == "PASS" for item in narrative_rows)),
        row("Duplicate narrative removed", "no repeated low-probability sentence in one item", markdown.count("该项属于低概率完善项。该项属于低概率完善项") == 0, "该项属于低概率完善项。该项属于低概率完善项" not in markdown),
        row("Priority regression pass", "HL-039 A_CORE and protected low-probability C", {"HL039": hl039["action_priority"], "finding": early["priority"], "HL007": hl007["action_priority"]}, hl039["action_priority"] == "A_CORE" and early["priority"] == "A_CORE" and hl007["action_priority"] == "C_OPTIMIZATION"),
        row("Formula regression pass", "remaining term rent x2 scenarios", [cases[d]["estimated_penalty"] for d in (30, 90, 180, 300)], (facts["early_termination"]["penalty_formula"]["type"] == "remaining_term_rent_multiplier" and [number(cases[d]["estimated_penalty"]) for d in (30, 90, 180, 300)] == [7704, 23112, 46224, 77040])),
        row("Legal Freshness pass", "outdated Contract Law detected", lease["legal_reference_issues"], any(issue.get("status") == "OUTDATED_REFERENCE" for issue in lease["legal_reference_issues"])),
        row("Rental regression pass", "rent facts and fixed gates", {"rent": facts["rent"], "HL015": items["HL-015"]["coverage_status"], "HL030": items["HL-030"]["coverage_status"], "HL040": hl040["coverage_status"], "HL043": hl043["risk_level"]}, number(facts["rent"]["monthly_amount"]) == 3852 and str(facts["rent"]["payment_due_day"]) == "5" and items["HL-015"]["coverage_status"] == "通过" and items["HL-030"]["coverage_status"] == "不适用" and hl040["coverage_status"] != "通过" and hl043["risk_level"] != "高"),
        row("Cement regression pass", "sale release gate ready", sale.get("release_quality_gate"), sale.get("success") and (sale.get("release_quality_gate") or {}).get("status") == "REPORT_READY"),
        row("Real Production Integration pass", "real entry debug reports and renderer gate pass", lease.get("quality4_gate"), lease.get("quality4_gate", {}).get("status") == "REPORT_READY" and all(term not in markdown for term in forbidden_engineering)),
    ]


ROOT_CAUSE_ROWS = [
    {
        "Problem": "39/50 LOW confidence",
        "Root Cause": "Evidence entailment trace wrote semantic_entailment=False for non-strict review items where entailment was merely not checked.",
        "File": "backend/review_v2/engine.py",
        "Function": "_apply_evidence_entailment_gate / _system_confidence_for_item",
        "Fix": "Only strict evidence gates can set negative entailment; final confidence is computed from dependency-aware ConfidenceBundle.",
    },
    {
        "Problem": "Legal confidence could contaminate final confidence",
        "Root Cause": "The previous confidence model exposed one level and did not know whether a review depended on legal authority.",
        "File": "backend/review_v2/engine.py",
        "Function": "_confidence_dependency_for_item / _confidence_bundle_for_item",
        "Fix": "Legal, formula and calculation components participate only when required by the current review.",
    },
    {
        "Problem": "Legal authority scope over-propagation",
        "Root Cause": "Adjacent death/repair topics could reuse checklist legal references without proposition-level support.",
        "File": "backend/review_v2/engine.py",
        "Function": "_legal_claim_specs_for_item",
        "Fix": "Death continuation, no-successor handover and repair-cost claims are split and validated independently.",
    },
    {
        "Problem": "MISSING using PARTIAL narrative",
        "Root Cause": "Risk descriptions could survive prior partial evidence before coverage was downgraded to missing.",
        "File": "backend/review_v2/engine.py",
        "Function": "_coverage_safe_reasoning / _professional_item_conclusion",
        "Fix": "Coverage-state templates now drive production narrative and reject partial phrases for missing items.",
    },
]


def frozen_snapshot(path: Path, report: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "source_file": str(path),
        "source_sha256": sha256(path),
        "system_version": (report.get("system_metadata") or {}).get("system_version"),
        "model_version": (report.get("system_metadata") or {}).get("model_version"),
        "prompt_version": (report.get("system_metadata") or {}).get("prompt_version"),
        "rule_version": (report.get("system_metadata") or {}).get("rule_version"),
        "ontology_version": (report.get("system_metadata") or {}).get("ontology_version"),
        "legal_dataset_version": (report.get("system_metadata") or {}).get("legal_dataset_version"),
        "canonical_facts": report.get("contract_facts"),
        "review_results": report.get("items"),
        "risk_findings": report.get("risk_findings"),
        "recommendations": report.get("recommendations"),
        "confidence_bundle": report.get("observability", {}).get("confidence_debug_report"),
        "legal_claims": report.get("legal_citation_claims"),
        "final_markdown": report.get("result"),
    }


def markdown_table(rows: List[Dict[str, Any]], columns: List[str]) -> List[str]:
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join("---" for _ in columns) + " |"]
    for item in rows:
        lines.append("| " + " | ".join(str(item.get(column, "")).replace("\n", " ") for column in columns) + " |")
    return lines


async def main() -> None:
    test_data = ROOT / "test_data"
    output_dir = ROOT / "output"
    lease_path = next(test_data.glob("1*.docx"))
    sale_path = next(test_data.glob("2*.docx"))
    lease = await run_file(lease_path, "house_lease")
    sale = await run_file(sale_path, "sale")
    checks = p0_checks(lease, sale)
    status = "PASS" if all(check["status"] == "PASS" for check in checks) else "FAIL"
    blind_ready = status == "PASS"
    payload = {
        "status": status,
        "P0_FINAL_CONVERGENCE": status == "PASS",
        "RENTAL_REGRESSION_FROZEN": status == "PASS",
        "BLIND_BENCHMARK_READY": blind_ready,
        "checks": checks,
        "root_cause_report": ROOT_CAUSE_ROWS,
        "confidence_debug_report": lease["observability"]["confidence_debug_report"],
        "legal_citation_debug_report": lease["observability"]["legal_claim_debug_report"],
        "narrative_state_debug_report": lease["observability"]["narrative_state_debug_report"],
        "notes": "Blind benchmark ready means the production pipeline is ready to run unseen contracts with private Gold; no blind accuracy is claimed here.",
    }
    write_json(output_dir / "quality5_3_p0_acceptance.json", payload)
    write_json(output_dir / "frozen_regression_snapshot_quality5_3.json", frozen_snapshot(lease_path, lease))

    lines = [
        "# Contract Review Quality 5.3 P0 Acceptance",
        "",
        f"Status: {status}",
        f"P0_FINAL_CONVERGENCE = {status}",
        f"RENTAL_REGRESSION_FROZEN = {str(status == 'PASS').lower()}",
        f"BLIND_BENCHMARK_READY = {str(blind_ready).lower()}",
        "",
        "## Final Acceptance Table",
        "",
        *markdown_table(checks, ["requirement", "expected", "actual", "status"]),
        "",
        "## Root Cause Report",
        "",
        *markdown_table(ROOT_CAUSE_ROWS, ["Problem", "Root Cause", "File", "Function", "Fix"]),
        "",
        "## Confidence Debug Report",
        "",
        *markdown_table(payload["confidence_debug_report"], ["review_id", "coverage", "parser", "fact", "evidence", "applicability", "legal", "formula", "final", "limiting_factors"]),
        "",
        "## Legal Citation Debug Report",
        "",
        *markdown_table(payload["legal_citation_debug_report"], ["review_id", "claim_id", "claim_type", "authority", "entailment", "support_scope", "result"]),
        "",
        "## Narrative State Debug Report",
        "",
        *markdown_table(payload["narrative_state_debug_report"], ["review_id", "coverage", "narrative_template", "evidence_state", "status"]),
    ]
    (output_dir / "quality5_3_p0_acceptance.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({"status": status, "blind_benchmark_ready": blind_ready, "failures": [check for check in checks if check["status"] == "FAIL"]}, ensure_ascii=False))


if __name__ == "__main__":
    asyncio.run(main())
