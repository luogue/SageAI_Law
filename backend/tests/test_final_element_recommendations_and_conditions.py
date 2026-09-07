from copy import deepcopy
from dataclasses import fields

import pytest

from review_v2 import engine
from review_v2.element_resolution import conditional_element, conditional_element_failures, is_actionable_element
from review_v2.technology_service_analysis import build_technology_fact_registry
from review_v2.user_profile import UserRiskProfile
from backend.tests.test_structured_license_performance_facts import result


def report_advice(report, rule):
    item = next(row for row in report["items"] if row["item_id"] == rule)
    findings = [row for row in report["risk_findings"] if rule in row["source_review_ids"]]
    ids = {row["finding_id"] for row in findings}
    texts = [item["suggested_clause_example"]]
    texts.extend(row["recommendation"] for row in findings)
    texts.extend(row["suggested_text"] for row in report["recommendations"] if ids & set(row["source_finding_ids"]))
    texts.extend(row["recommendation"] for row in report["final_dispositions"] if row["risk_id"] in ids)
    assert len(texts) >= 4
    return texts


@pytest.mark.parametrize("rule,required,forbidden", [
    ("TC-12-01", ["律师费", "诉讼费", "鉴定费", "赔偿款", "和解费用", "停用", "替代"],
     ["擅自修改", "超范围实施", "被许可方自行承担", "尚未细化"]),
    ("TC-10-02", ["期限", "地域", "商业使用", "定价"], ["分许可", "转许可", "再许可"]),
    ("TC-09-04", ["技术服务", "是否另行收费", "计算方式", "支付节点", "包含在许可费"],
     ["责任主体", "适用条件", "权利义务边界", "违约后果", "执行程序", "实质条款内容"]),
])
def test_every_report_projection_uses_the_final_element_actions(result, rule, required, forbidden):
    assert result["release_quality_gate"]["status"] == "REPORT_READY", result["release_quality_gate"]["failures"]
    texts = report_advice(result, rule)
    for text in texts:
        for word in required:
            assert word in text, text
        for word in forbidden:
            assert word not in text, text
    assert len(set(texts)) == 1


def test_recommendation_target_sets_are_complete_and_disjoint(result):
    findings = {row["finding_id"]: row for row in result["risk_findings"]}
    for disposition in result["final_dispositions"]:
        finding = findings[disposition["risk_id"]]
        if finding["aggregation_signals"].get("recommendation_element_policy") != "FINAL_UNRESOLVED_ELEMENTS":
            continue
        recs = [row for row in result["recommendations"] if finding["finding_id"] in row["source_finding_ids"]]
        if not recs:
            continue
        target_ids = {key for row in recs for fragment in row["fragments"] for key in fragment["source_element_ids"]}
        allowed = set(disposition["final_missing_element_ids"])
        covered = set(finding["covered_element_ids"])
        assert target_ids <= allowed
        assert allowed <= target_ids
        assert not target_ids & covered


@pytest.mark.parametrize("prerequisite,proof,status", [
    (False, False, "NOT_APPLICABLE"), (False, True, "NOT_APPLICABLE"),
    (True, False, "MISSING"), (True, True, "COVERED"),
    (None, False, "CONDITION_UNRESOLVED"), (None, True, "CONDITION_UNRESOLVED"),
])
def test_conditional_prerequisite_precedes_evidence(prerequisite, proof, status):
    element = conditional_element(
        "authorization", "授权文件", prerequisite,
        [{"clause_id": "proof1", "quote": "独立授权文件"}] if proof else [],
        prerequisite_fact="交易需要上游授权", verification_instruction="请核验授权前提。",
    )
    assert element["status"] == status
    assert is_actionable_element(element) is (status == "MISSING")
    action, _ = engine._recommendation_action_for_element(element)
    assert bool(action) is (status == "MISSING")


BASE = """专利实施许可合同
甲方（被许可方）：远航制造有限公司
乙方（许可方）：北辰研究有限公司
第一条 标的
专利名称：设备故障监测方法；专利号：ZL202410008877.6；申请日：2024年4月9日；授权日：2025年5月6日。
第二条 实施许可
乙方授予甲方在中国境内实施本专利的普通许可，许可期限五年。
第三条 价款
许可使用费120万元，一次付清。
"""


@pytest.mark.parametrize("identity,upstream", [
    ("专利权人：北辰研究有限公司。", "NOT_APPLICABLE"),
    ("专利权人：南岭技术有限公司。", "MISSING"),
    ("许可方不是本专利权人。", "MISSING"),
    ("", "CONDITION_UNRESOLVED"),
])
@pytest.mark.parametrize("permission,sublicense", [
    ("被许可方可以向第三方分许可本专利。", "MISSING"),
    ("被许可方不得向第三方分许可本专利。", "NOT_APPLICABLE"),
    ("", "CONDITION_UNRESOLVED"),
])
def test_conditional_authorization_survives_the_complete_report(identity, upstream, permission, sublicense):
    report = engine.review_contract_v2(BASE + identity + "\n" + permission, "technology", use_llm=False,
        profile=UserRiskProfile(user_identity="甲方/被许可方"))
    for rule in ("TC-03-04", "TC-13-02"):
        item = next(row for row in report["items"] if row["item_id"] == rule)
        elements = {row["element_id"]: row for row in item["coverage_elements"]}
        for key, status, label in (
            ("upstream_authorization_file", upstream, "上游授权链"),
            ("sublicense_authorization_file", sublicense, "再许可权限证明"),
        ):
            assert elements[key]["status"] == status
            assert elements[key]["conditional_element"]
            if status != "MISSING":
                assert label not in item["suggested_clause_example"]
                for finding in report["risk_findings"]:
                    if rule in finding["source_review_ids"]:
                        assert key not in {row["element_id"] for row in finding["final_missing_elements"]}
                        assert label not in finding["recommendation"]
            if status == "CONDITION_UNRESOLVED":
                reviews = [row for row in report["manual_review_items"] if rule in row["source_rules"]]
                assert reviews and key in reviews[0]["conditional_element_ids"]
                assert "核验" in reviews[0]["review_instruction"]


def test_improvement_sublicense_ban_does_not_resolve_patent_sublicense_permission():
    facts = build_technology_fact_registry(BASE + "第四条 后续改进\n双方不得向第三方转许可改进技术。")
    assert facts["third_party_claim"]["sublicense_permission"] is None


@pytest.mark.parametrize("prerequisite,status", [("UNKNOWN", "MISSING"), ("FALSE", "MISSING"), ("UNKNOWN", "COVERED"), ("TRUE", "NOT_APPLICABLE")])
def test_conditional_state_contradictions_cannot_pass_gate(prerequisite, status):
    failures = conditional_element_failures([{
        "element_id": "permission", "conditional_element": True,
        "prerequisite_status": prerequisite, "status": status,
    }])
    assert failures
    gate = engine._combine_quality_gates({"status": "REPORT_READY", "failures": []}, {"failures": failures})
    assert gate["status"] == "BLOCKED"


@pytest.mark.parametrize("mutation", ["covered", "extra", "omit", "all_omitted", "static_template", "exclude_core"])
def test_quality_gate_rejects_recommendation_drift(result, mutation):
    def load(cls, key):
        return [cls(**{f.name: row[f.name] for f in fields(cls) if f.name in row}) for row in deepcopy(result[key])]
    findings = load(engine.RiskFinding, "risk_findings")
    recs = load(engine.Recommendation, "recommendations")
    dispositions = load(engine.FinalDisposition, "final_dispositions")
    finding = next(f for f in findings if "TC-10-02" in f.source_review_ids)
    rec = next(r for r in recs if finding.finding_id in r.source_finding_ids)
    if mutation == "covered":
        rec.fragments[0]["source_element_ids"] = ["improvement_sublicense"]
    elif mutation == "extra":
        rec.fragments[0]["text"] += "；补充违约后果和执行程序"
    elif mutation == "omit":
        rec.fragments.pop()
    elif mutation == "all_omitted":
        recs.remove(rec)
    elif mutation == "exclude_core":
        fragment = rec.fragments.pop()
        rec.excluded_reasons[fragment["source_element_ids"][0]] = "Template did not include this core gap."
    else:
        rec.suggested_text = "建议补充分许可条件。"
    audit = engine._recommendation_truth_binding_audit(recs, findings, dispositions)
    assert engine._recommendation_truth_binding_gate(audit)["status"] == "BLOCKED"
