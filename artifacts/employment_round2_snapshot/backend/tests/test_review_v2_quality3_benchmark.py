from review_v2.benchmark import GoldContract, run_blind_evaluation, run_regression_benchmark, write_quality_report


def _fake_review(text: str, contract_type: str):
    return {
        "success": bool(text and contract_type),
        "release_quality_gate": {"status": "REPORT_READY"},
        "risk_findings": [{"finding_id": "RF-001"}],
    }


def test_benchmark_does_not_claim_accuracy_with_small_sample():
    samples = [
        GoldContract("reg-lease-001", "house_lease", "租赁合同", {}, "regression"),
    ]

    result = run_regression_benchmark(samples, _fake_review)

    assert result["sample_size"] == 1
    assert result["sample_status"] == "INSUFFICIENT SAMPLE SIZE"
    assert result["metrics"]["finding_precision"] is None
    assert "FORMULA_WRONG" in result["failure_taxonomy"]
    assert result["metrics"]["micro"] == {}


def test_blind_runner_keeps_regression_samples_out_of_blind_split():
    samples = [
        GoldContract("reg-lease-001", "house_lease", "租赁合同", {}, "regression"),
        GoldContract("blind-lease-001", "house_lease", "未见过的租赁合同", {}, "blind"),
    ]

    result = run_blind_evaluation(samples, _fake_review)

    assert result["split"] == "blind"
    assert result["sample_size"] == 1
    assert [case["sample_id"] for case in result["cases"]] == ["blind-lease-001"]
    assert result["sample_status"] == "INSUFFICIENT SAMPLE SIZE"


def test_quality_report_is_written_separately(tmp_path):
    result = run_regression_benchmark(
        [GoldContract("reg-lease-001", "house_lease", "租赁合同", {}, "regression")],
        _fake_review,
    )

    written = write_quality_report(result, tmp_path / "quality_report.json")

    assert written["sample_status"] == "INSUFFICIENT SAMPLE SIZE"
    assert (tmp_path / "quality_report.json").exists()
