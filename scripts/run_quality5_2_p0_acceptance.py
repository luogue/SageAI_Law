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


def count(text: str, needle: str) -> int:
    return (text or "").count(needle)


def number(value: Any) -> float | None:
    match = re.search(r"\d+(?:\.\d+)?", str(value))
    return float(match.group(0)) if match else None


def row(requirement: str, expected: Any, actual: Any, ok: bool, owner: str = "") -> Dict[str, Any]:
    return {
        "requirement": requirement,
        "expected": expected,
        "actual": actual,
        "owner": owner,
        "status": "PASS" if ok else "FAIL",
    }


def finding_for(report: Dict[str, Any], review_id: str) -> Dict[str, Any]:
    return next(finding for finding in report.get("risk_findings", []) if review_id in finding.get("source_review_ids", []))


def supported_evidence(item: Dict[str, Any]) -> List[Dict[str, Any]]:
    return [
        evidence
        for evidence in item.get("evidence_clauses", [])
        if evidence.get("entailment_status") in {"SUPPORTS", "PARTIAL_SUPPORT"}
    ]


def p0_checks(lease: Dict[str, Any], sale: Dict[str, Any]) -> List[Dict[str, Any]]:
    items = by_id(lease)
    markdown = lease.get("result", "")
    facts = lease.get("contract_facts", {})
    hl039 = items["HL-039"]
    hl040 = items["HL-040"]
    hl042 = items["HL-042"]
    hl043 = items["HL-043"]
    hl007 = items["HL-007"]
    hl015 = items["HL-015"]
    hl030 = items["HL-030"]
    early = finding_for(lease, "HL-039")
    hl042_finding = finding_for(lease, "HL-042")
    cases = {case["remaining_days"]: case for case in hl039["scenario_analysis"]["cases"]}
    protected_claims = hl007.get("legal_references", [])
    metrics = lease.get("benchmark_metrics", {})
    forbidden_terms = [
        "DIRECT_SUPPORT",
        "PARTIAL_SUPPORT",
        "BACKGROUND_ONLY",
        "RF-",
        "Scenario Engine",
        "Fact Graph",
        "【法律依据】：法律依据：",
        "【法律依据】：依据：",
    ]
    hl042_has_evidence = bool(hl042.get("evidence_clauses"))
    hl042_evidence_text = "".join(evidence.get("quote") or evidence.get("text") or "" for evidence in hl042.get("evidence_clauses", []))
    hl042_valid_support = (
        not hl042_has_evidence
        and (hl042.get("decision_trace", {}).get("negative_evidence") or {}).get("result") == "NOT_FOUND"
    ) or (
        bool(supported_evidence(hl042))
        and "押金" in hl042_evidence_text
        and any(term in hl042_evidence_text for term in ("抵扣", "扣除", "扣款", "未付租金", "水电费", "维修费"))
        and "提前退租" not in hl042_evidence_text
    )
    legal732 = [
        claim for claim in protected_claims
        if claim.get("article") == "第732条" and claim.get("support_type") == "DIRECT_SUPPORT"
    ]
    legal_claims = lease.get("legal_citation_claims", [])
    drafting_30 = [
        claim for claim in legal_claims
        if claim.get("review_id") == "HL-013" and claim.get("claim_type") == "DRAFTING_RECOMMENDATION"
    ]
    important_findings = [
        finding for finding in lease.get("risk_findings", [])
        if finding.get("priority") in {"A_CORE", "B_PRACTICAL"}
    ]
    important_evidence_ok = all(
        finding.get("evidence")
        or all((items.get(review_id, {}).get("coverage_status") == "缺失") for review_id in finding.get("source_review_ids", []))
        for finding in important_findings
    )

    return [
        row("Evidence Entailment Engine exists", "claim/candidate/negative trace", hl042.get("decision_trace", {}), "evidence_claim" in hl042.get("decision_trace", {}) and "evidence_candidates" in hl042.get("decision_trace", {}), "Evidence"),
        row("HL-042 supporting evidence valid", "deposit offset evidence or explicit negative evidence", {"status": hl042["coverage_status"], "evidence": hl042_evidence_text, "negative": hl042.get("decision_trace", {}).get("negative_evidence")}, hl042_valid_support, "Evidence"),
        row("PARTIAL requires real partial evidence", "HL-042 partial must have supporting deposit-offset sentence", [e.get("entailment_status") for e in hl042.get("evidence_clauses", [])], hl042["coverage_status"] != "部分覆盖" or bool(supported_evidence(hl042)), "Evidence"),
        row("negative evidence modeled correctly", "missing HL-042 has NOT_FOUND", hl042.get("decision_trace", {}).get("negative_evidence"), hl042["coverage_status"] != "缺失" or (hl042.get("decision_trace", {}).get("negative_evidence") or {}).get("result") == "NOT_FOUND", "Evidence"),
        row("important findings have sentence evidence", "A/B finding evidence or missing-item negative presentation", [(f["risk_group"], bool(f.get("evidence"))) for f in important_findings], important_evidence_ok, "Evidence"),
        row("Legal Claim Recall improved", "tenant death recalls Civil Code 732", legal732, bool(legal732) and legal732[0].get("authority_id") == "CN-CIVIL-CODE-732", "Legal"),
        row("direct default-law authority retrievable", "732/734/730/725 direct authorities", sorted({claim.get("article") for claim in legal_claims if claim.get("support_type") == "DIRECT_SUPPORT"}), {"第732条", "第734条", "第730条", "第725条"} <= {claim.get("article") for claim in legal_claims if claim.get("support_type") == "DIRECT_SUPPORT"}, "Legal"),
        row("30-day recommendation separated from statute", "HL-013 drafting claim has no authority", drafting_30, bool(drafting_30) and all(not claim.get("authority_links") for claim in drafting_30), "Legal"),
        row("Default Law affects Priority", "HL-007 clear default lowered to C", hl007.get("decision_trace", {}).get("priority_assessment"), hl007.get("decision_trace", {}).get("default_law_status") == "CLEAR_DEFAULT" and hl007.get("action_priority") == "C_OPTIMIZATION", "Priority"),
        row("low-probability protected issues not over-prioritized", "HL-007 not A/B", hl007.get("action_priority"), hl007.get("action_priority") == "C_OPTIMIZATION", "Priority"),
        row("A_CORE early termination remains", "HL-039/finding A_CORE", {"item": hl039.get("action_priority"), "finding": early.get("priority")}, hl039.get("action_priority") == "A_CORE" and early.get("priority") == "A_CORE", "Regression"),
        row("Legal Freshness remains", "outdated reference issue still detected", lease.get("legal_reference_issues", []), any(issue.get("status") == "OUTDATED_REFERENCE" for issue in lease.get("legal_reference_issues", [])), "Legal"),
        row("Production legal enums hidden", "debug terms absent", {term: count(markdown, term) for term in forbidden_terms}, all(count(markdown, term) == 0 for term in forbidden_terms), "Renderer"),
        row("Production legal wording cleaned", "no duplicate legal-basis prefix", {"double_legal": count(markdown, "【法律依据】：法律依据："), "double_basis": count(markdown, "【法律依据】：依据：")}, "【法律依据】：法律依据：" not in markdown and "【法律依据】：依据：" not in markdown, "Renderer"),
        row("Missing evidence presentation correct", "fake excerpt absent", count(markdown, "原文片段：无正式条款证据"), "原文片段：无正式条款证据" not in markdown, "Renderer"),
        row("Risk Aggregation semantic gate", "HL-042 not merged into early termination", {"HL-042": hl042_finding.get("risk_group"), "early_sources": early.get("source_review_ids")}, hl042_finding.get("risk_group") == "deposit_offset_order" and "HL-042" not in early.get("source_review_ids", []), "Aggregator"),
        row("Rental hard regression", "rent/due/formula/scenarios/HL015/HL030/HL040/HL043", {"rent": facts.get("rent"), "cases": [cases[d]["estimated_penalty"] for d in (30, 90, 180, 300)], "HL015": hl015["coverage_status"], "HL030": hl030["coverage_status"], "HL040": hl040["reasoning_summary"], "HL043": hl043["risk_level"]}, number((facts.get("rent") or {}).get("monthly_amount")) == 3852 and str((facts.get("rent") or {}).get("payment_due_day")) == "5" and (facts.get("early_termination") or {}).get("penalty_formula", {}).get("type") == "remaining_term_rent_multiplier" and [number(cases[d]["estimated_penalty"]) for d in (30, 90, 180, 300)] == [7704, 23112, 46224, 77040] and hl015["coverage_status"] == "通过" and hl030["coverage_status"] == "不适用" and "mortgage" not in hl040["reasoning_summary"].lower() and hl043["risk_level"] != "高", "Regression"),
        row("Cement regression", "sale release gate ready", (sale.get("release_quality_gate") or {}).get("status"), sale.get("success") and (sale.get("release_quality_gate") or {}).get("status") == "REPORT_READY", "Regression"),
        row("Benchmark metrics include 5.2 fields", "evidence/legal recall metrics exposed", sorted(metrics.keys()), {"evidence_entailment_accuracy", "evidence_direction_accuracy", "evidence_source_accuracy", "direct_authority_recall"} <= set(metrics.keys()), "Benchmark"),
    ]


ROOT_CAUSE_ROWS = [
    {
        "Problem": "HL-042 used early-termination penalty as supporting evidence",
        "Root Cause": "Risk aggregation and evidence retrieval were only relatedness-based; they did not verify that a sentence entailed the exact deposit-offset-order claim.",
        "Fix": "Added EvidenceClaim/EvidenceCandidate/NegativeEvidence and a semantic gate that rejects related-but-not-supporting penalty sentences.",
    },
    {
        "Problem": "Direct legal authority was missed for tenant death successor",
        "Root Cause": "Citation validation only parsed checklist legal_basis text and had no proposition-level direct authority recall.",
        "Fix": "Added proposition recall for Civil Code Art. 732 and claim-level validation output.",
    },
    {
        "Problem": "30-day drafting suggestion was mixed with statutory rule",
        "Root Cause": "One review item could collapse procedure, legal effect, and drafting advice into one citation status.",
        "Fix": "Split LegalClaim records into LEGAL_EFFECT/PROCEDURE/DRAFTING_RECOMMENDATION with independent authority links.",
    },
    {
        "Problem": "Default-law-protected low-probability gaps were over-prioritized",
        "Root Cause": "Missing clause status mechanically flowed into priority without considering statutory fallback protection and residual practical gap.",
        "Fix": "PriorityInput now includes default-law status and effective gap, and CLEAR_DEFAULT + low residual gap lowers action priority.",
    },
]


def evidence_mapping_report(lease: Dict[str, Any]) -> List[Dict[str, Any]]:
    items = by_id(lease)
    rows = []
    for review_id in ("HL-039", "HL-040", "HL-042", "HL-043"):
        item = items[review_id]
        rows.append(
            {
                "review_id": review_id,
                "risk_group": item.get("risk_group"),
                "coverage": item.get("coverage_status"),
                "entailment": [evidence.get("entailment_status") for evidence in item.get("evidence_clauses", [])],
                "negative_evidence": (item.get("decision_trace", {}).get("negative_evidence") or {}).get("result"),
            }
        )
    return rows


def legal_claim_report(lease: Dict[str, Any]) -> List[Dict[str, Any]]:
    targets = {
        "HL-007": "tenant death successor",
        "HL-013": "term expiry to indefinite / indefinite termination notice / 30-day drafting",
        "HL-039": "early termination penalty reduction",
        "HL-005": "notice delivery",
        "HL-012": "ownership change",
    }
    claims = lease.get("legal_citation_claims", [])
    return [
        {
            "topic": label,
            "review_id": review_id,
            "claims": [
                {
                    "claim_type": claim.get("claim_type"),
                    "article": claim.get("article"),
                    "support_type": claim.get("support_type"),
                    "authority_id": claim.get("authority_id"),
                    "citation_existence_status": claim.get("citation_existence_status"),
                }
                for claim in claims
                if claim.get("review_id") == review_id
            ],
        }
        for review_id, label in targets.items()
    ]


def default_law_report(lease: Dict[str, Any]) -> List[Dict[str, Any]]:
    items = by_id(lease)
    return [
        {
            "review_id": review_id,
            "risk_group": items[review_id].get("risk_group"),
            "coverage": items[review_id].get("coverage_status"),
            "default_law_status": items[review_id].get("decision_trace", {}).get("default_law_status"),
            "effective_gap": items[review_id].get("decision_trace", {}).get("effective_gap"),
            "action_priority": items[review_id].get("action_priority"),
        }
        for review_id in ("HL-007", "HL-012", "HL-013", "HL-042")
    ]


def frozen_snapshot(path: Path, report: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "source_file": str(path),
        "source_sha256": sha256(path),
        "system_version": (report.get("system_metadata") or {}).get("system_version"),
        "model_version": (report.get("system_metadata") or {}).get("model_version"),
        "prompt_version": (report.get("system_metadata") or {}).get("prompt_version"),
        "rule_version": (report.get("system_metadata") or {}).get("rule_version"),
        "legal_dataset_version": (report.get("system_metadata") or {}).get("legal_dataset_version"),
        "ontology_version": (report.get("system_metadata") or {}).get("ontology_version"),
        "canonical_facts": report.get("contract_facts"),
        "reviews": report.get("items"),
        "findings": report.get("risk_findings"),
        "recommendations": report.get("recommendations"),
        "final_report": report.get("result"),
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
    blind_status = "READY" if status == "PASS" else "NOT_READY"
    payload = {
        "status": status,
        "P0_FINAL_CONVERGENCE": status == "PASS",
        "RENTAL_REGRESSION_FROZEN": status == "PASS",
        "BLIND_BENCHMARK_STATUS": blind_status,
        "checks": checks,
        "root_cause_report": ROOT_CAUSE_ROWS,
        "evidence_mapping_report": evidence_mapping_report(lease),
        "legal_claim_report": legal_claim_report(lease),
        "default_law_report": default_law_report(lease),
        "notes": "Blind benchmark status is readiness only; no blind accuracy claim is made without unseen contracts and private Gold.",
    }
    write_json(output_dir / "quality5_2_p0_acceptance.json", payload)
    write_json(output_dir / "frozen_regression_snapshot_quality5_2.json", frozen_snapshot(lease_path, lease))

    lines = [
        "# Contract Review Quality 5.2 P0 Acceptance",
        "",
        f"Status: {status}",
        f"P0_FINAL_CONVERGENCE = {status}",
        f"RENTAL_REGRESSION_FROZEN = {str(status == 'PASS').lower()}",
        f"BLIND_BENCHMARK_STATUS = {blind_status}",
        "",
        "## Final Acceptance Table",
        "",
        *markdown_table(checks, ["requirement", "expected", "actual", "owner", "status"]),
        "",
        "## Root Cause Report",
        "",
        *markdown_table(ROOT_CAUSE_ROWS, ["Problem", "Root Cause", "Fix"]),
        "",
        "## Evidence Mapping Report",
        "",
        *markdown_table(payload["evidence_mapping_report"], ["review_id", "risk_group", "coverage", "entailment", "negative_evidence"]),
        "",
        "## Legal Claim Report",
        "",
        *markdown_table(payload["legal_claim_report"], ["topic", "review_id", "claims"]),
        "",
        "## Default Law Report",
        "",
        *markdown_table(payload["default_law_report"], ["review_id", "risk_group", "coverage", "default_law_status", "effective_gap", "action_priority"]),
    ]
    (output_dir / "quality5_2_p0_acceptance.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({"status": status, "blind_benchmark_status": blind_status, "failures": [check for check in checks if check["status"] == "FAIL"]}, ensure_ascii=False))


if __name__ == "__main__":
    asyncio.run(main())
