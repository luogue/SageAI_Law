"""Quality 3.0 benchmark and blind-evaluation helpers.

The module intentionally does not claim production accuracy when the project has
too few expert-labelled contracts. Regression cases and blind cases are kept
separate so known contracts are never counted as blind evaluation samples.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import json
from pathlib import Path
from typing import Any, Callable, Dict, Iterable, List, Optional


MIN_RELIABLE_SAMPLE_SIZE = 30
BENCHMARK_VERSION = "quality4-target-benchmark-2026-08-11"
FAILURE_TAXONOMY = {
    "PARSER_ERROR",
    "FACT_MISS",
    "FACT_FALSE",
    "FACT_CONFLICT",
    "APPLICABILITY_ERROR",
    "EVIDENCE_WRONG",
    "EVIDENCE_RELATED_NOT_SUPPORTING",
    "EVIDENCE_WRONG_CLAIM",
    "EVIDENCE_WRONG_PARTY",
    "EVIDENCE_WRONG_DIRECTION",
    "EVIDENCE_WRONG_CONDITION",
    "EVIDENCE_MISSING_EXCEPTION",
    "EVIDENCE_DIRECTION_ERROR",
    "RETRIEVAL_MISS",
    "APPLICABILITY_WRONG",
    "LEGAL_WRONG",
    "LEGAL_OUTDATED",
    "LEGAL_OUTDATED_MISS",
    "LEGAL_CITATION_MISS",
    "LEGAL_WRONG_AUTHORITY",
    "LEGAL_OUTDATED_REFERENCE_MISS",
    "LEGAL_DRAFTING_AS_STATUTORY",
    "LEGAL_DEFAULT_PROTECTION_MISS",
    "LEGAL_ENTAILMENT_ERROR",
    "LEGAL_ENTAILMENT_WRONG",
    "FORMULA_WRONG",
    "CALCULATION_WRONG",
    "SEVERITY_WRONG",
    "PRIORITY_WRONG",
    "FALSE_POSITIVE",
    "FALSE_NEGATIVE",
    "CONTRADICTION",
    "DUPLICATE_FINDING",
    "MISSED_AGGREGATION",
    "DUPLICATION",
    "REPORT_MISLEADING",
    "CONFIDENCE_OVERCLAIM",
}


@dataclass(frozen=True)
class GoldContract:
    sample_id: str
    contract_type: str
    text: str
    expected: Dict[str, Any]
    split: str = "regression"
    complexity: str = "standard"
    perspective: str = "neutral"
    annotator: str = ""
    reviewer: str = ""
    annotation_date: str = ""
    legal_version: str = ""
    confidence: str = "medium"
    notes: str = ""
    ambiguity: str = ""


@dataclass
class BenchmarkResult:
    benchmark_version: str = BENCHMARK_VERSION
    sample_size: int = 0
    sample_status: str = "INSUFFICIENT SAMPLE SIZE"
    split: str = "regression"
    metrics: Dict[str, Any] = field(default_factory=dict)
    cases: List[Dict[str, Any]] = field(default_factory=list)

    def to_public_dict(self) -> Dict[str, Any]:
        return {
            "benchmark_version": self.benchmark_version,
            "sample_size": self.sample_size,
            "sample_status": self.sample_status,
            "split": self.split,
            "metrics": self.metrics,
            "cases": self.cases,
        }


def _empty_metrics() -> Dict[str, Any]:
    return {
        "contract_type_accuracy": None,
        "fact_precision": None,
        "fact_recall": None,
        "critical_fact_recall": None,
        "applicability_accuracy": None,
        "evidence_precision": None,
        "evidence_recall": None,
        "evidence_fidelity": None,
        "evidence_entailment_accuracy": None,
        "evidence_direction_accuracy": None,
        "evidence_source_accuracy": None,
        "coverage_accuracy": None,
        "finding_precision": None,
        "finding_recall": None,
        "material_finding_precision": None,
        "material_finding_recall": None,
        "critical_false_negative_rate": None,
        "material_false_positive_rate": None,
        "severity_accuracy": None,
        "priority_accuracy": None,
        "formula_accuracy": None,
        "formula_parse_accuracy": None,
        "formula_operand_accuracy": None,
        "formula_unit_accuracy": None,
        "formula_party_direction_accuracy": None,
        "calculation_accuracy": None,
        "legal_citation_accuracy": None,
        "direct_authority_recall": None,
        "legal_citation_existence_accuracy": None,
        "legal_citation_entailment_accuracy": None,
        "legal_freshness_accuracy": None,
        "legal_proposition_accuracy": None,
        "contradiction_rate": None,
        "duplicate_finding_rate": None,
        "missed_aggregation_rate": None,
        "top5_risk_recall": None,
        "recommendation_accuracy": None,
        "manual_review_precision": None,
        "manual_review_recall": None,
        "abstention_precision": None,
        "abstention_recall": None,
        "confidence_calibration_error": None,
        "micro_average": {},
        "macro_average": {},
        "micro": {},
        "macro": {},
        "per_contract_type": {},
        "per_complexity": {},
        "per_risk_category": {},
        "per_risk_group": {},
    }


def _case_failures(sample: GoldContract, actual: Dict[str, Any]) -> List[Dict[str, Any]]:
    failures: List[Dict[str, Any]] = []
    expected = sample.expected or {}
    expected_gate = expected.get("release_quality_gate")
    actual_gate = (actual.get("release_quality_gate") or {}).get("status")
    if expected_gate and expected_gate != actual_gate:
        failures.append(
            {
                "contract": sample.sample_id,
                "contract_id": sample.sample_id,
                "expected": expected_gate,
                "actual": actual_gate,
                "failure_type": "REPORT_MISLEADING",
                "error_type": "REPORT_MISLEADING",
                "failure_stage": "Release Quality Gate",
                "severity": "material",
                "root_cause": "候选输出的 release gate 与 Gold 不一致。",
                "fix_owner": "Quality Gate",
            }
        )
    expected_formula = expected.get("formula_type")
    if expected_formula:
        actual_formula = None
        for item in actual.get("items") or []:
            formula = ((item.get("scenario_analysis") or {}).get("formula") or {})
            if formula.get("type"):
                actual_formula = formula.get("type")
                break
        if actual_formula != expected_formula:
            failures.append(
                {
                "contract": sample.sample_id,
                "contract_id": sample.sample_id,
                "expected": expected_formula,
                "actual": actual_formula,
                "failure_type": "FORMULA_WRONG",
                "error_type": "FORMULA_WRONG",
                "failure_stage": "Formula Validation",
                    "severity": "critical",
                    "root_cause": "公式类型与 Gold 不一致。",
                    "fix_owner": "Formula Parser",
                }
            )
    return failures


def _run_split_benchmark(
    samples: Iterable[GoldContract],
    review_fn: Callable[[str, str], Dict[str, Any]],
    split: str,
) -> Dict[str, Any]:
    cases: List[Dict[str, Any]] = []
    failures: List[Dict[str, Any]] = []
    selected_samples = [sample for sample in samples if sample.split == split]
    for sample in selected_samples:
        actual = review_fn(sample.text, sample.contract_type)
        case_failures = _case_failures(sample, actual)
        failures.extend(case_failures)
        cases.append(
            {
                "sample_id": sample.sample_id,
                "contract_type": sample.contract_type,
                "complexity": sample.complexity,
                "perspective": sample.perspective,
                "gold_metadata": {
                    "annotator": sample.annotator,
                    "reviewer": sample.reviewer,
                    "annotation_date": sample.annotation_date,
                    "legal_version": sample.legal_version,
                    "confidence": sample.confidence,
                    "ambiguity": sample.ambiguity,
                    "notes": sample.notes,
                },
                "success": bool(actual.get("success")),
                "release_quality_gate": (actual.get("release_quality_gate") or {}).get("status"),
                "risk_finding_count": len(actual.get("risk_findings") or []),
                "failure_count": len(case_failures),
            }
        )
    result = BenchmarkResult(sample_size=len(selected_samples), split=split, metrics=_empty_metrics(), cases=cases)
    if len(selected_samples) >= MIN_RELIABLE_SAMPLE_SIZE:
        result.sample_status = "READY"
    public = result.to_public_dict()
    public["failure_taxonomy"] = sorted(FAILURE_TAXONOMY)
    public["top_20_failures"] = sorted(failures, key=lambda failure: 0 if failure["severity"] == "critical" else 1)[:20]
    public["release_gate_status"] = "BLOCKED" if any(f["severity"] == "critical" for f in failures) else "REPORT_READY"
    return public


def run_regression_benchmark(
    samples: Iterable[GoldContract],
    review_fn: Callable[[str, str], Dict[str, Any]],
) -> Dict[str, Any]:
    return _run_split_benchmark(samples, review_fn, "regression")


def run_blind_evaluation(
    samples: Iterable[GoldContract],
    review_fn: Callable[[str, str], Dict[str, Any]],
) -> Dict[str, Any]:
    return _run_split_benchmark(samples, review_fn, "blind")


def write_quality_report(
    report: Dict[str, Any],
    output_path: Optional[str | Path] = None,
) -> Dict[str, Any]:
    path = Path(output_path or "output/quality_report.json")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    return {"path": str(path), "sample_status": report.get("sample_status"), "release_gate_status": report.get("release_gate_status")}
