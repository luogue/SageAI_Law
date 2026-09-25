from types import SimpleNamespace
from unittest.mock import patch
import pytest

from review_v2.engine import review_contract_v2
from review_v2.evidence_compatibility import evidence_compatible, evidence_compatibility_failures
from review_v2.prerequisite_resolution import resolve_prerequisites, prerequisite_status_failures


def run(text):
    return review_contract_v2("供用电合同。\n" + text, "utility_supply", use_llm=False)


def item(output, key):
    return next(i for i in output["items"] if i["item_id"] == key)


def test_billing_accuracy_is_not_supply_quality_evidence():
    result = run("第四条 电能计量\n双方以电能表记录的用电量作为电费结算依据，计量装置误差超标时调整电费。")
    quality = item(result, "US-03-04")
    assert quality["coverage_status"] == "缺失"
    assert not quality["evidence_clauses"]
    assert item(result, "US-10-01")["coverage_status"] == "通过"


def test_quality_monitoring_and_preservation_provide_direct_support():
    result = run("第五条 质量监测\n供电方设置电压和频率自动监测装置，并保存监测数据供双方核验。")
    quality = item(result, "US-03-04")
    assert quality["coverage_status"] == "通过"
    assert all("电压" in e["quote"] for e in quality["evidence_clauses"])
    assert result["semantic_boundary_gate"]["status"] == "REPORT_READY"


def test_mixed_measurement_clause_binds_only_matching_sentence():
    result = run("第四条 监测资料\n电能表记录用电量作为结算依据，计量误差超标时调整电费。供电方设置电压和频率自动监测装置，并保存监测数据供双方核验。")
    quality = item(result, "US-03-04")
    assert quality["coverage_status"] == "通过"
    assert all("调整电费" not in e["quote"] for e in quality["evidence_clauses"])
    assert not evidence_compatible("供电电压符合标准，电表计量误差应检测。", "supply_quality_measurement")


@pytest.mark.parametrize("text, expected", [
    ("乙方为经主管部门认定的一级重要电力用户。", "缺失"),
    ("乙方为普通商业办公企业。", "INSUFFICIENT_CONTEXT"),
    ("乙方为制造企业，实行连续生产，用电容量20000kVA。", "INSUFFICIENT_CONTEXT"),
    ("乙方不属于重要电力用户。", "不适用"),
    ("若乙方为一级重要电力用户，应另行制定保障措施。", "INSUFFICIENT_CONTEXT"),
])
def test_important_identity_prerequisite_branches(text, expected):
    result = run(text)
    for key in ("US-06-04", "US-11-03"):
        row = item(result, key)
        assert row["coverage_status"] == expected
        assert row["applicable_if"] != "始终适用"
    assert result["semantic_boundary_gate"]["status"] == "REPORT_READY"


def test_unknown_prerequisite_never_reaches_rule_evaluator():
    from review_v2 import engine
    original = engine._judge_checkpoints_with_registry
    seen = []
    def capture(checkpoints, *args, **kwargs):
        seen.extend(c.item_id for c in checkpoints)
        return original(checkpoints, *args, **kwargs)
    with patch.object(engine, "_judge_checkpoints_with_registry", capture):
        result = run("乙方为连续生产的工业企业。")
    assert "US-06-04" not in seen and "US-11-03" not in seen
    assert item(result, "US-06-04")["applicability"]["applicable"] is None


@pytest.mark.parametrize("key", ["identity", "industry", "subject_type", "transaction", "amount_threshold", "guarantee", "personal_data", "cross_border", "important_user", "consumer", "special_facility"])
def test_generic_three_state_prerequisite_contract(key):
    checkpoint = SimpleNamespace(prerequisite_facts=(key,), applicable_if="前置事实成立")
    for value in (True, False, None):
        resolved = resolve_prerequisites(checkpoint, {key: dict(value=value, label=key)})
        assert resolved["applicable"] is value
    assert resolve_prerequisites(checkpoint, {})["status"] == "INSUFFICIENT_CONTEXT"


@pytest.mark.parametrize("text, wrong_domain", [
    ("电能表计量误差检测", "supply_quality_measurement"),
    ("付款凭证", "acceptance_evidence"),
    ("专利证书", "quality_proof"),
    ("乙方应通知甲方", "notice_record"),
    ("违约方承担赔偿责任", "performance_obligation"),
    ("正文约定容量500kVA", "attachment_entity"),
])
def test_neighboring_domains_cannot_substitute_for_required_evidence(text, wrong_domain):
    assert not evidence_compatible(text, wrong_domain)


def test_gates_reject_forged_type_and_unresolved_missing():
    result = run("乙方为制造企业。")
    unknown = item(result, "US-06-04")
    unknown["coverage_status"] = "缺失"
    assert prerequisite_status_failures([unknown])
    quality = item(result, "US-03-04")
    quality["evidence_clauses"] = [dict(quote="电能表计量误差检测", supported_elements=["quality_monitoring"], source_domains=["supply_quality_measurement"])]
    assert evidence_compatibility_failures([quality])


def test_identity_facts_are_request_local():
    assert item(run("乙方为一级重要电力用户。"), "US-06-04")["applicability"]["applicable"] is True
    assert item(run("乙方为普通制造企业。"), "US-06-04")["applicability"]["applicable"] is None
