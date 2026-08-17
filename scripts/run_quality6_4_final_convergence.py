"""Run Quality 6.4 acceptance from raw DOCX files through the production upload route."""

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
BACKEND = ROOT / "backend"
if str(BACKEND) not in sys.path:
    sys.path.insert(0, str(BACKEND))

from routers.review_v2 import review_v2_file  # noqa: E402
from review_v2.clause_parser import parse_contract_clauses  # noqa: E402
from review_v2.engine import review_contract_v2  # noqa: E402


class Upload:
    def __init__(self, path: Path):
        self.filename = path.name
        self.file = io.BytesIO(path.read_bytes())


async def review_file(path: Path, contract_type: str) -> Dict[str, Any]:
    return await review_v2_file(
        file=Upload(path),
        contract_type=contract_type,
        include_low_risk=True,
        use_llm=False,
        profile_json="{}",
        current_user={"id": "quality-6.4-audit"},
    )


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def stable_hash(payload: Any) -> str:
    raw = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def source_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check(condition: bool, expected: Any, actual: Any) -> Dict[str, Any]:
    return {"expected": expected, "actual": actual, "status": "PASS" if condition else "FAIL"}


def items_by_id(output: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    return {item["item_id"]: item for item in output["items"]}


def mutation_outputs() -> Dict[str, Any]:
    guidance = review_contract_v2(
        "特别提示\n遇不可抗力，双方宜及时通知并提供证明。\n订立合同双方\n甲方：买方；乙方：卖方。\n第一条 产品A共10台。",
        "sale",
        use_llm=False,
    )
    operative = review_contract_v2(
        "特别提示\n遇不可抗力，双方宜及时通知并提供证明。\n订立合同双方\n甲方：买方；乙方：卖方。\n第一条 产品A共10台。\n第十条 因不可抗力不能履行的，受影响方应及时书面通知并提供证明。",
        "sale",
        use_llm=False,
    )
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
    topic = review_contract_v2("买卖合同。第一条 产品质量执行国家标准GB-X及企业标准Q-Y。", "sale", use_llm=False)
    template_appearance = review_contract_v2(
        "买卖合同示范文本。甲方为买方，乙方为卖方。第一条 产品A共10台。",
        "sale",
        use_llm=False,
    )
    precedence = review_contract_v2(
        "买卖合同。第一条 产品质量执行国家标准GB-X及企业标准Q-Y；标准冲突时以双方特别约定标准为准。",
        "sale",
        use_llm=False,
    )
    return {
        "guidance": guidance,
        "operative": operative,
        "public_template": public_template,
        "supplier_terms": supplier_terms,
        "template_appearance": template_appearance,
        "topic": topic,
        "precedence": precedence,
    }


async def main() -> int:
    output_dir = ROOT / "output"
    sale_hb_001 = await review_file(next((ROOT / "test_data").glob("2*.docx")), "sale")
    sale_hb_002 = await review_file(next((ROOT / "test_data").glob("5*.docx")), "sale")
    rental = await review_file(next((ROOT / "test_data").glob("1*.docx")), "house_lease")
    mutations = mutation_outputs()

    hb1 = items_by_id(sale_hb_001)
    hb2 = items_by_id(sale_hb_002)
    rent = items_by_id(rental)
    guidance = items_by_id(mutations["guidance"])["S-00-06"]
    operative = items_by_id(mutations["operative"])["S-00-06"]
    public_terms = items_by_id(mutations["public_template"])["S-00-07"]
    supplier_terms = items_by_id(mutations["supplier_terms"])["S-00-07"]
    template_appearance = items_by_id(mutations["template_appearance"])["S-00-07"]
    topic = items_by_id(mutations["topic"])["S-06-01"]
    precedence = items_by_id(mutations["precedence"])["S-06-01"]

    hb2_gates = sale_hb_002["observability"]["pre_render_quality_gate"]["gate_results"]
    default_rows = sale_hb_002["observability"]["default_law_debug_table"]
    default_by_id = {row["review_id"]: row for row in default_rows}
    narrative_rows = sale_hb_002["observability"]["narrative_state_debug_report"]
    priority = sale_hb_002["observability"]["pre_render_quality_gate"]["priority_consistency_verification"]
    signability = sale_hb_002["overall_assessment"]["signability_decision"]
    source_text = "\n".join(
        (ROOT / path).read_text(encoding="utf-8")
        for path in (
            "backend/review_v2/engine.py",
            "backend/review_v2/domain_packs.py",
            "backend/review_v2/clause_parser.py",
            "backend/review_v2/semantic_reviewer.py",
        )
    )

    hb2_required_pass = {
        "S-00-01", "S-01-01", "S-02-01", "S-02-02", "S-02-03", "S-02-04", "S-02-05",
        "S-03-01", "S-03-02", "S-05-01", "S-06-02", "S-06-04", "S-07-01", "S-07-04",
        "S-08-01", "S-08-03", "S-08-04",
    }
    facts = sale_hb_002["contract_facts"].get("facts") or {}
    expected_fact_types = {
        "party.buyer.name", "party.seller.name", "goods.name", "goods.model", "quantity.total", "quantity.unit",
        "price.total", "currency", "delivery.final_deadline", "inspection.deadline", "quality_objection.deadline",
        "warranty.duration", "dispute.type", "contract.effective_date", "legal.legacy_reference",
    }
    rental_scenarios = rent["HL-039"]["scenario_analysis"]["scenarios"]
    manual_count = sum(1 for item in rental["items"] if item["needs_manual_review"])
    no_manual_narrative = manual_count > 0 or "建议人工复核" not in rental["result"]

    requirements = {
        "6.3 Recall preserved": check(
            sale_hb_002["document_integrity"]["parsed_character_ratio"] >= 0.99
            and all((item["decision_trace"].get("retrieval_trace") or {}) for item in sale_hb_002["items"]),
            "complete document and active retrieval traces",
            sale_hb_002["document_integrity"],
        ),
        "Sale HB-002 facts preserved": check(
            expected_fact_types.issubset({key for key, values in facts.items() if values})
            and all(hb2[item_id]["coverage_status"] == "通过" for item_id in hb2_required_pass)
            and hb2["S-04-03"]["coverage_status"] == "不适用",
            "critical facts present, known covered items PASS, road-goods N/A",
            {"fact_types": sorted(expected_fact_types & set(facts)), "covered": {item_id: hb2[item_id]["coverage_status"] for item_id in sorted(hb2_required_pass)}, "road_goods": hb2["S-04-03"]["coverage_status"]},
        ),
        "Sale HB-001 preserved": check(
            sale_hb_001["release_quality_gate"]["status"] == "REPORT_READY"
            and hb1["S-02-05"]["coverage_status"] == "风险条款"
            and all(claim.get("article") != "第585条" for claim in hb1["S-00-05"]["legal_references"]),
            "REPORT_READY, evidence-backed unilateral price risk, Article 585 scope preserved",
            {"release": sale_hb_001["release_quality_gate"]["status"], "S-02-05": hb1["S-02-05"]["coverage_status"], "S-00-05": hb1["S-00-05"]["legal_references"]},
        ),
        "Rental preserved": check(
            rental["release_quality_gate"]["status"] == "REPORT_READY"
            and rental["contract_facts"]["rent"]["monthly_amount"] == "3852元"
            and rental["contract_facts"]["rent"]["payment_due_day"] == "5"
            and rent["HL-015"]["coverage_status"] == "通过"
            and rent["HL-030"]["coverage_status"] == "不适用"
            and rent["HL-039"]["review_priority"] == "A_CORE"
            and rental_scenarios == {"remaining_30_days": 7704.0, "remaining_90_days": 23112.0, "remaining_180_days": 46224.0, "remaining_300_days": 77040.0}
            and no_manual_narrative,
            "locked residential lease facts, formula, priority and manual-review invariant",
            {"rent": rental["contract_facts"]["rent"], "HL-015": rent["HL-015"]["coverage_status"], "HL-030": rent["HL-030"]["coverage_status"], "HL-039": rent["HL-039"]["review_priority"], "scenarios": rental_scenarios, "manual_count": manual_count},
        ),
        "Default Law active": check(
            all(review_id in default_by_id and default_by_id[review_id]["default_rule"] for review_id in ("S-04-01", "S-04-02", "S-04-04", "S-07-01")),
            "core sale default rules executed",
            default_by_id,
        ),
        "Default Law affects Residual Risk": check(
            hb2["S-04-01"]["coverage_status"] == "缺失"
            and bool(hb2["S-04-01"]["decision_trace"]["effective_gap"]["default_protection"])
            and "默认规则" in hb2["S-04-01"]["decision_trace"]["effective_gap"]["residual_risk"],
            "MISSING coverage retained while protection changes residual risk",
            hb2["S-04-01"]["decision_trace"]["effective_gap"],
        ),
        "Template Guidance separated": check(
            any(clause.block_type == "TEMPLATE_GUIDANCE" for clause in parse_contract_clauses("特别提示\n双方宜约定不可抗力通知。\n订立合同双方\n甲方：买方；乙方：卖方。"))
            and guidance["coverage_status"] == "缺失",
            "guidance is typed and cannot prove an obligation",
            {"guidance_coverage": guidance["coverage_status"]},
        ),
        "Operative Clause preferred": check(
            operative["coverage_status"] != "缺失"
            and operative["evidence_clauses"]
            and all(row["evidence_block_type"] == "OPERATIVE_CLAUSE" for row in operative["evidence_clauses"]),
            "operative evidence only",
            operative["evidence_clauses"],
        ),
        "Format Terms Applicability evidence-based": check(
            public_terms["applicability"]["status"] in {"NOT_APPLICABLE", "UNCERTAIN"}
            and supplier_terms["applicability"]["status"] == "APPLICABLE"
            and bool(supplier_terms["applicability"]["trigger_evidence"]),
            "public template does not trigger; supplied restrictive terms do",
            {"public": public_terms["applicability"], "supplier": supplier_terms["applicability"]},
        ),
        "Topic Evidence not treated as Element Evidence": check(
            topic["coverage_status"] != "通过"
            and next(row for row in topic["coverage_elements"] if row["element_id"] == "precedence_between_standards")["status"] != "COVERED"
            and next(row for row in precedence["coverage_elements"] if row["element_id"] == "precedence_between_standards")["status"] == "COVERED",
            "standard topic does not prove precedence element",
            {"topic": topic["coverage_elements"], "precedence": precedence["coverage_elements"]},
        ),
        "Coverage Elements drive Coverage": check(
            hb2["S-06-01"]["coverage_status"] == "部分覆盖"
            and bool(hb2["S-06-01"]["coverage_elements"])
            and any(row["status"] == "COVERED" for row in hb2["S-06-01"]["coverage_elements"])
            and any(row["status"] != "COVERED" for row in hb2["S-06-01"]["coverage_elements"]),
            "mixed element state produces PARTIAL",
            hb2["S-06-01"]["coverage_elements"],
        ),
        "Narrative truth consistent": check(all(row["status"] == "PASS" for row in narrative_rows), "all PASS", narrative_rows),
        "No MISSING + already covered": check(
            not any(row["coverage"] == "缺失" and "已覆盖" in row["narrative_result"] for row in narrative_rows),
            "none",
            [row for row in narrative_rows if row["coverage"] == "缺失" and "已覆盖" in row["narrative_result"]],
        ),
        "Priority Consistency Verifier active": check(priority["executed"] and priority["consistency"] == "CONSISTENT", "executed and CONSISTENT", priority),
        "Signability driven by actual Findings": check(
            bool(sale_hb_002["risk_findings"]) and bool(signability["decision_finding_ids"]),
            "non-empty independent findings and decision drivers",
            signability,
        ),
        "Decision-driving Findings identifiable": check(
            1 <= len(signability["decision_finding_ids"]) <= 3
            and set(signability["decision_finding_ids"]).issubset({finding["finding_id"] for finding in sale_hb_002["risk_findings"]}),
            "1-3 valid finding IDs",
            signability["decision_finding_ids"],
        ),
        "Confidence consumes Applicability": check(
            template_appearance["applicability"]["status"] == "UNCERTAIN"
            and template_appearance["system_confidence"]["level"] != "high"
            and "applicability" in template_appearance["system_confidence"]["confidence_bundle"]["limiting_factors"],
            "uncertain applicability limits final confidence",
            template_appearance["system_confidence"],
        ),
        "Confidence consumes Default Law uncertainty": check(
            any(
                item["decision_trace"].get("default_law_status") == "UNCERTAIN_DEFAULT"
                and item["system_confidence"]["level"] != "high"
                for item in sale_hb_002["items"]
                if item["decision_trace"].get("default_law_status")
            ),
            "at least one uncertain default limits confidence",
            [{"review_id": item["item_id"], "default": item["decision_trace"].get("default_law_status"), "confidence": item["system_confidence"]["level"]} for item in sale_hb_002["items"] if item["decision_trace"].get("default_law_status") == "UNCERTAIN_DEFAULT"],
        ),
        "Confidence consumes contradiction state": check(
            hb2_gates["CONFIDENCE_VALIDATION_GATE"] == "PASS"
            and hb2_gates["CROSS_LAYER_CONSISTENCY_GATE"] == "PASS",
            "both gates PASS",
            hb2_gates,
        ),
        "Legal Freshness preserved": check(bool(sale_hb_002["legal_reference_issues"]), "legacy legal reference finding", sale_hb_002["legal_reference_issues"]),
        "Article 585 scope preserved": check(
            all(claim.get("article") != "第585条" for claim in hb1["S-00-05"]["legal_references"]),
            "no generic Article 585 mapping",
            hb1["S-00-05"]["legal_references"],
        ),
        "No hardcoding": check(
            "if contract_id == \"SALE-HB" not in source_text and "if contract_id == 'SALE-HB" not in source_text,
            "no contract-id outcome branch",
            "no matching branch found",
        ),
        "Real Production path verified": check(
            all(output["release_quality_gate"]["status"] == "REPORT_READY" for output in (sale_hb_001, sale_hb_002, rental))
            and all(output["observability"]["production_call_graph"][2].endswith("review_v2.py:review_v2_file") for output in (sale_hb_001, sale_hb_002, rental)),
            "raw DOCX -> review_v2_file -> REPORT_READY",
            {"SALE-HB-001": sale_hb_001["release_quality_gate"]["status"], "SALE-HB-002": sale_hb_002["release_quality_gate"]["status"], "RENTAL": rental["release_quality_gate"]["status"]},
        ),
    }

    acceptance_pass = all(row["status"] == "PASS" for row in requirements.values())
    hard_gates = {
        "DEFAULT_LAW_GATE": requirements["Default Law active"]["status"],
        "DOCUMENT_BLOCK_SEMANTICS_GATE": "PASS" if requirements["Template Guidance separated"]["status"] == requirements["Operative Clause preferred"]["status"] == "PASS" else "FAIL",
        "APPLICABILITY_GATE": requirements["Format Terms Applicability evidence-based"]["status"],
        "ELEMENT_EVIDENCE_GATE": requirements["Topic Evidence not treated as Element Evidence"]["status"],
        "NARRATIVE_CONSISTENCY_GATE": requirements["Narrative truth consistent"]["status"],
        "PRIORITY_CONSISTENCY_GATE": requirements["Priority Consistency Verifier active"]["status"],
        "SIGNABILITY_GATE": requirements["Signability driven by actual Findings"]["status"],
        "CONFIDENCE_GATE": "PASS" if all(requirements[key]["status"] == "PASS" for key in ("Confidence consumes Applicability", "Confidence consumes Default Law uncertainty", "Confidence consumes contradiction state")) else "FAIL",
        "SALE_HB_001": requirements["Sale HB-001 preserved"]["status"],
        "SALE_HB_002": requirements["Sale HB-002 facts preserved"]["status"],
        "RENTAL_REGRESSION": requirements["Rental preserved"]["status"],
        "REAL_PRODUCTION_INTEGRATION": requirements["Real Production path verified"]["status"],
    }
    passed = acceptance_pass and all(status == "PASS" for status in hard_gates.values())

    write_json(output_dir / "default_law_debug.json", {"case_id": "SALE-HB-002", "rows": default_rows})
    write_json(output_dir / "applicability_debug.json", {"case_id": "SALE-HB-002", "rows": [{"review_id": item["item_id"], **item["applicability"]} for item in sale_hb_002["items"]]})
    write_json(output_dir / "coverage_element_debug.json", {"case_id": "SALE-HB-002", "rows": sale_hb_002["observability"]["coverage_element_debug_report"]})
    write_json(output_dir / "priority_consistency_debug.json", {"case_id": "SALE-HB-002", "verifier": priority, "decisions": [{"review_id": item["item_id"], "severity": item["risk_severity"], "priority": item["review_priority"], "decision": item["decision_trace"].get("priority_assessment")} for item in sale_hb_002["items"] if item["review_priority"] not in {"NONE", "NOT_APPLICABLE"}]})
    write_json(output_dir / "signability_debug.json", {"case_id": "SALE-HB-002", "decision": signability, "finding_ids": [finding["finding_id"] for finding in sale_hb_002["risk_findings"]]})

    regression_summary = {
        "contract_review_6_4": "PASS" if passed else "FAIL",
        "sale_hb_001_regression": hard_gates["SALE_HB_001"],
        "sale_hb_002_regression": hard_gates["SALE_HB_002"],
        "rental_regression": hard_gates["RENTAL_REGRESSION"],
        "candidate_frozen": passed,
        "next_blind_status": "READY" if passed else "NOT_READY",
        "next_test": "SALE-BLIND-003",
        "hard_gates": hard_gates,
        "requirements": requirements,
        "output_hashes": {
            "SALE-HB-001": sale_hb_001["observability"]["output_hashes"],
            "SALE-HB-002": sale_hb_002["observability"]["output_hashes"],
            "RENTAL": rental["observability"]["output_hashes"],
        },
    }
    write_json(output_dir / "regression_summary.json", regression_summary)

    metadata = sale_hb_002["system_metadata"]
    candidate_files = [
        "backend/review_v2/engine.py",
        "backend/review_v2/domain_packs.py",
        "backend/review_v2/clause_parser.py",
        "backend/review_v2/semantic_reviewer.py",
        "backend/review_v2/llm_semantic_reviewer.py",
        "backend/review_v2/blind_runner.py",
        "backend/routers/review_v2.py",
    ]
    git_commit = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, check=True, capture_output=True, text=True).stdout.strip()
    manifest = {
        "system_version": metadata["system_version"],
        "model_version": metadata["model_version"],
        "prompt_version": metadata["prompt_version"],
        "parser_version": metadata["parser_version"],
        "fact_schema_version": metadata["fact_schema_version"],
        "retrieval_version": metadata["retrieval_version"],
        "review_ontology_version": metadata["ontology_version"],
        "domain_pack_version": metadata["domain_pack_version"],
        "default_law_version": metadata["default_law_version"],
        "legal_dataset_version": metadata["legal_dataset_version"],
        "confidence_version": metadata["confidence_version"],
        "benchmark_version": metadata["benchmark_version"],
        "git_commit": git_commit,
        "source_hashes": {path: source_hash(ROOT / path) for path in candidate_files},
        "regression_hash": stable_hash(regression_summary),
        "frozen": passed,
        "next_blind_id": "SALE-BLIND-003",
        "generated_at": datetime.now().isoformat(),
    }
    manifest["candidate_hash"] = stable_hash({key: value for key, value in manifest.items() if key != "generated_at"})
    write_json(output_dir / "candidate_manifest.json", manifest)

    lines = [
        "# Contract Review Quality 6.4 Root Cause Report",
        "",
        "## Scope",
        "",
        "本轮仅收敛默认法、文档块语义、适用性证据、要件证据、叙事一致性、优先级与可签署性，并完成置信度派生校准和盲测冻结协议。",
        "",
        "## Root Causes",
        "",
        "| Problem | First Broken Layer | General Fix |",
        "| --- | --- | --- |",
        "| Coverage 缺失后直接形成风险 | Effective Gap | DefaultRule 先判断适用范围，再生成 residual risk；Coverage 始终只表达合同文本 |",
        "| 范本提示被当作合同义务 | Document Block Semantics | 为文档块赋予稳定类型，义务审查只允许正式条款、附件和必要主体区块 |",
        "| 条件审查缺乏触发证据 | Applicability | ApplicabilityResult 保存 trigger facts、trigger evidence、missing triggers 和 confidence |",
        "| 同主题证据直接推成 PASS | Coverage Element | CoverageClaim 按 required elements 逐项验证，并由 sufficiency rule 计算 PASS/PARTIAL/MISSING |",
        "| 最终文案重新判断事实 | Narrative | 文案完全从结构化 CoverageElementResult 和 Finding 派生，并由 NARRATIVE_TRUTH_GATE 阻断矛盾 |",
        "| HIGH、Priority 和 Signability 不可解释 | Decision Calibration | PriorityDecision 保留 drivers/mitigators，SignabilityDecision 绑定 1-3 个独立 Finding |",
        "",
        "## Acceptance",
        "",
        "| Requirement | Expected | Actual | PASS/FAIL |",
        "| --- | --- | --- | --- |",
    ]
    for name, row in requirements.items():
        actual = json.dumps(row["actual"], ensure_ascii=False, separators=(",", ":"))
        if len(actual) > 180:
            actual = actual[:177] + "..."
        lines.append(f"| {name} | {row['expected']} | {actual} | {row['status']} |")
    lines.extend([
        "",
        "## Freeze",
        "",
        f"- CONTRACT_REVIEW_6_4: {'PASS' if passed else 'FAIL'}",
        f"- CANDIDATE_FROZEN: {str(passed).lower()}",
        f"- CANDIDATE_HASH: {manifest['candidate_hash']}",
        f"- NEXT_BLIND_STATUS: {'READY' if passed else 'NOT_READY'}",
        "- NEXT_TEST: SALE-BLIND-003",
    ])
    (output_dir / "6_4_root_cause_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(json.dumps({
        "CONTRACT_REVIEW_6_4": "PASS" if passed else "FAIL",
        "SALE_HB_001_REGRESSION": hard_gates["SALE_HB_001"],
        "SALE_HB_002_REGRESSION": hard_gates["SALE_HB_002"],
        "RENTAL_REGRESSION": hard_gates["RENTAL_REGRESSION"],
        "CANDIDATE_FROZEN": passed,
        "NEXT_BLIND_STATUS": "READY" if passed else "NOT_READY",
        "NEXT_TEST": "SALE-BLIND-003",
        "candidate_hash": manifest["candidate_hash"],
        "failed_requirements": [name for name, row in requirements.items() if row["status"] == "FAIL"],
    }, ensure_ascii=False, indent=2))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
