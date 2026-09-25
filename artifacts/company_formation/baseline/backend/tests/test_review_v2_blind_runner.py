import json

from review_v2.blind_runner import run_blind_benchmark


def test_blind_runner_writes_predictions_metrics_errors_and_report(tmp_path):
    benchmark_root = tmp_path / "benchmark" / "blind"
    contracts_dir = benchmark_root / "contracts"
    gold_dir = benchmark_root / "gold_private"
    contracts_dir.mkdir(parents=True)
    gold_dir.mkdir(parents=True)
    (contracts_dir / "blind-001.json").write_text(
        json.dumps(
            {
                "contract_id": "blind-001",
                "contract_type": "house_lease",
                "text": "盲测租赁合同。乙方提前退租的，应按剩余租期租金2倍支付违约金。",
                "perspective": "tenant",
                "complexity": "SIMPLE",
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    (gold_dir / "blind-001.json").write_text(
        json.dumps(
            {
                "contract_type": "house_lease",
                "expected": {"release_quality_gate": "REPORT_READY"},
                "annotator": "expert-a",
                "reviewer": "expert-b",
                "legal_version": "cn-civil-code-2026-08-11",
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    def fake_review(text: str, contract_type: str):
        return {
            "success": True,
            "release_quality_gate": {"status": "REPORT_READY"},
            "risk_findings": [{"finding_id": "RF-TEST-001"}],
            "system_metadata": {
                "system_version": "test-system",
                "model_version": "deterministic_pipeline",
                "prompt_version": "test-prompt",
                "rule_version": "test-rule",
                "legal_dataset_version": "test-law",
                "benchmark_version": "test-benchmark",
            },
        }

    output_root = tmp_path / "out"
    result = run_blind_benchmark(benchmark_root, output_root, review_fn=fake_review)

    assert result["summary"]["blind_benchmark_status"] == "RUN_INSUFFICIENT_SAMPLE"
    assert result["summary"]["prediction_count"] == 1
    assert (output_root / "predictions" / "blind-001.json").exists()
    assert (output_root / "benchmark_summary.json").exists()
    assert (output_root / "benchmark_metrics.json").exists()
    assert (output_root / "benchmark_errors.json").exists()
    assert (output_root / "benchmark_report.md").exists()
    assert result["metrics"]["cases"][0]["gold_metadata"]["annotator"] == "expert-a"


def test_blind_runner_without_private_gold_is_ready_not_run(tmp_path):
    benchmark_root = tmp_path / "benchmark" / "blind"
    contracts_dir = benchmark_root / "contracts"
    contracts_dir.mkdir(parents=True)
    (contracts_dir / "blind-002.txt").write_text("没有Gold的盲测合同", encoding="utf-8")

    output_root = tmp_path / "out"
    result = run_blind_benchmark(
        benchmark_root,
        output_root,
        review_fn=lambda text, contract_type: {"success": True, "release_quality_gate": {"status": "REPORT_READY"}},
    )

    assert result["summary"]["blind_benchmark_status"] == "READY_NOT_RUN"
    assert result["summary"]["gold_count"] == 0
