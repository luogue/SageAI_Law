"""Blind benchmark runner for contract review.

The runner saves predictions before reading private gold files. This keeps the
workflow honest: known regression contracts can be scored, but they are not
counted as blind unless they live under benchmark/blind/contracts.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

from review_v2.benchmark import GoldContract, MIN_RELIABLE_SAMPLE_SIZE, run_blind_evaluation
from review_v2.engine import review_contract_v2


def _read_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def _stable_hash(payload: Dict[str, Any]) -> str:
    raw = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def _load_contract(path: Path) -> Dict[str, Any]:
    if path.suffix.lower() == ".json":
        data = _read_json(path)
        data.setdefault("contract_id", path.stem)
        data.setdefault("contract_type", "house_lease")
        data.setdefault("text", "")
        return data
    return {
        "contract_id": path.stem,
        "contract_type": "house_lease",
        "text": path.read_text(encoding="utf-8"),
        "perspective": "neutral",
        "complexity": "SIMPLE",
    }


def _contract_files(contracts_dir: Path) -> List[Path]:
    if not contracts_dir.exists():
        return []
    return sorted(
        path for path in contracts_dir.iterdir()
        if path.is_file() and path.suffix.lower() in {".json", ".txt", ".md"}
    )


def _load_gold(gold_dir: Path, contract: Dict[str, Any]) -> Optional[GoldContract]:
    gold_path = gold_dir / f"{contract['contract_id']}.json"
    if not gold_path.exists():
        return None
    gold = _read_json(gold_path)
    return GoldContract(
        sample_id=contract["contract_id"],
        contract_type=gold.get("contract_type") or contract.get("contract_type") or "house_lease",
        text=contract.get("text", ""),
        expected=gold.get("expected") or gold,
        split="blind",
        complexity=gold.get("complexity") or contract.get("complexity") or "SIMPLE",
        perspective=gold.get("perspective") or contract.get("perspective") or "neutral",
        annotator=gold.get("annotator", ""),
        reviewer=gold.get("reviewer", ""),
        annotation_date=gold.get("annotation_date", ""),
        legal_version=gold.get("legal_version", ""),
        confidence=gold.get("confidence", "medium"),
        notes=gold.get("notes", ""),
        ambiguity=gold.get("ambiguity", ""),
    )


def _version_snapshot(predictions: List[Dict[str, Any]]) -> Dict[str, Any]:
    for prediction in predictions:
        metadata = (prediction.get("output") or {}).get("system_metadata") or {}
        if metadata:
            return {
                "system_version": metadata.get("system_version"),
                "model_version": metadata.get("model_version"),
                "prompt_version": metadata.get("prompt_version"),
                "rule_version": metadata.get("rule_version"),
                "legal_dataset_version": metadata.get("legal_dataset_version"),
                "benchmark_version": metadata.get("benchmark_version"),
                "ontology_version": metadata.get("ontology_version"),
            }
    return {}


def _benchmark_status(sample_size: int, has_predictions: bool, has_gold: bool) -> str:
    if not has_predictions:
        return "NOT_CREATED"
    if not has_gold:
        return "READY_NOT_RUN"
    if sample_size < MIN_RELIABLE_SAMPLE_SIZE:
        return "RUN_INSUFFICIENT_SAMPLE"
    return "VALID_RESULT"


def _write_report(path: Path, summary: Dict[str, Any], result: Dict[str, Any]) -> None:
    metrics = result.get("metrics") or {}
    lines = [
        "# Blind Benchmark Report",
        "",
        "## Run Summary",
        "",
        f"- System Version: {summary.get('system_version') or (summary.get('version_snapshot') or {}).get('system_version')}",
        f"- Dataset Version: {summary.get('dataset_version')}",
        f"- Status: {summary['blind_benchmark_status']}",
        f"- Sample size: {summary['sample_size']}",
        f"- Contract Types: {summary.get('contract_types')}",
        f"- Complexity Distribution: {summary.get('complexity_distribution')}",
        f"- Created at: {summary['created_at']}",
        f"- Release gate: {summary.get('release_gate_status')}",
        f"- Critical FN: {metrics.get('critical_false_negative_rate')}",
        f"- Material Precision: {metrics.get('material_finding_precision')}",
        f"- Material Recall: {metrics.get('material_finding_recall')}",
        f"- Evidence Fidelity: {metrics.get('evidence_fidelity')}",
        f"- Legal Accuracy: {metrics.get('legal_citation_accuracy')}",
        f"- Formula Accuracy: {metrics.get('formula_accuracy')}",
        f"- Top-5 Recall: {metrics.get('top5_risk_recall')}",
        "",
        "## Version Snapshot",
        "",
    ]
    for key, value in (summary.get("version_snapshot") or {}).items():
        lines.append(f"- {key}: {value}")
    lines.extend(["", "## Worst Errors", ""])
    failures = result.get("top_20_failures") or []
    if not failures:
        lines.append("- No material failures recorded.")
    for failure in failures[:20]:
        lines.append(
            f"- {failure.get('contract')}: {failure.get('failure_type')} at "
            f"{failure.get('failure_stage')} - {failure.get('root_cause')}"
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def run_blind_benchmark(
    benchmark_root: str | Path = "benchmark/blind",
    output_root: str | Path = "output/blind_benchmark",
    *,
    system_version: str = "",
    review_fn: Callable[[str, str], Dict[str, Any]] = review_contract_v2,
) -> Dict[str, Any]:
    benchmark_root = Path(benchmark_root)
    output_root = Path(output_root)
    contracts_dir = benchmark_root / "contracts"
    gold_dir = benchmark_root / "gold_private"
    run_id = datetime.now().strftime("blind-%Y%m%d-%H%M%S")
    predictions_dir = output_root / "predictions" / run_id
    contracts = [_load_contract(path) for path in _contract_files(contracts_dir)]

    predictions: List[Dict[str, Any]] = []
    for contract in contracts:
        output = review_fn(contract.get("text", ""), contract.get("contract_type", "house_lease"))
        prediction = {
            "contract_id": contract["contract_id"],
            "contract_type": contract.get("contract_type"),
            "created_at": datetime.now().isoformat(),
            "prediction_artifact": {
                "facts": output.get("contract_facts") or output.get("contract_context") or {},
                "reviews": output.get("review_results_4_0") or output.get("items") or [],
                "findings": output.get("risk_findings") or [],
                "recommendations": output.get("recommendations") or [],
                "report": output.get("result") or "",
            },
            "output": output,
        }
        prediction["prediction_hash"] = _stable_hash(prediction["prediction_artifact"])
        predictions.append(prediction)
        _write_json(predictions_dir / f"{contract['contract_id']}.json", prediction)
        _write_json(output_root / "predictions" / f"{contract['contract_id']}.json", prediction)

    lock = {
        "run_id": run_id,
        "created_at": datetime.now().isoformat(),
        "prediction_count": len(predictions),
        "prediction_hashes": {prediction["contract_id"]: prediction["prediction_hash"] for prediction in predictions},
        "gold_loaded_during_prediction": False,
    }
    _write_json(output_root / "prediction_lock.json", lock)

    gold_samples = [sample for contract in contracts if (sample := _load_gold(gold_dir, contract))]
    prediction_by_text = {contract.get("text", ""): prediction["output"] for contract, prediction in zip(contracts, predictions)}
    if gold_samples:
        result = run_blind_evaluation(gold_samples, lambda text, contract_type: prediction_by_text.get(text) or review_fn(text, contract_type))
    else:
        result = {
            "sample_size": 0,
            "sample_status": "INSUFFICIENT SAMPLE SIZE",
            "split": "blind",
            "metrics": {},
            "cases": [],
            "top_20_failures": [],
            "release_gate_status": "BLOCKED" if contracts else "NOT_CREATED",
        }

    status = _benchmark_status(len(gold_samples), bool(predictions), bool(gold_samples))
    summary = {
        "run_id": run_id,
        "blind_benchmark_status": status,
        "sample_size": len(gold_samples),
        "prediction_count": len(predictions),
        "gold_count": len(gold_samples),
        "sample_status": result.get("sample_status"),
        "release_gate_status": result.get("release_gate_status"),
        "created_at": datetime.now().isoformat(),
        "system_version": system_version,
        "dataset_version": benchmark_root.name,
        "contract_types": sorted({contract.get("contract_type", "unknown") for contract in contracts}),
        "complexity_distribution": {
            complexity: sum(1 for contract in contracts if contract.get("complexity") == complexity)
            for complexity in sorted({contract.get("complexity", "UNKNOWN") for contract in contracts})
        },
        "version_snapshot": _version_snapshot(predictions),
        "prediction_lock": lock,
        "notes": "Regression contracts must not be placed here and counted as blind.",
    }
    _write_json(output_root / "benchmark_summary.json", summary)
    _write_json(output_root / "benchmark_metrics.json", result)
    _write_json(output_root / "benchmark_errors.json", {"top_20_failures": result.get("top_20_failures", [])})
    _write_report(output_root / "benchmark_report.md", summary, result)
    return {"summary": summary, "metrics": result}


def main() -> None:
    parser = argparse.ArgumentParser(description="Run blind contract-review benchmark.")
    parser.add_argument("--benchmark-root", default="benchmark/blind")
    parser.add_argument("--output-root", default="output/blind_benchmark")
    parser.add_argument("--dataset", default=None, help="Alias for --benchmark-root.")
    parser.add_argument("--output", default=None, help="Alias for --output-root.")
    parser.add_argument("--system-version", default="")
    args = parser.parse_args()
    benchmark_root = args.dataset or args.benchmark_root
    output_root = args.output or args.output_root
    result = run_blind_benchmark(benchmark_root, output_root, system_version=args.system_version)
    print(json.dumps(result["summary"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
