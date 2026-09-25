"""Latest entrusted contract through the production upload, evaluator and render path."""
from copy import deepcopy
from dataclasses import fields
from collections import Counter

import pytest

from tests.test_entrusted_development_production_closure import report, item
from review_v2 import engine
from review_v2.clause_parser import parse_contract_clauses
from review_v2.report_state_consistency import report_state_consistency_failures
from review_v2.underlying_issue import underlying_issue_signature, group_duplicate_underlying_issues


def model(raw):
    return engine.ReviewItemResult(**{key: deepcopy(value) for key, value in raw.items()
                                     if key in {f.name for f in fields(engine.ReviewItemResult)}})


def test_shared_disposal_has_the_same_scope_and_remaining_requirements(report):
    ownership = item(report, "TC-05-03")
    confidentiality = item(report, "TC-11-03")
    shared = {e["element_id"]: e for e in confidentiality["coverage_elements"]}
    counterpart = {e["element_id"]: e for e in ownership["coverage_elements"] if e.get("fact_identity")}
    assert set(shared) == set(counterpart) == {"material_disposition", "copy_disposition", "backup_disposition", "material_disposal_confirmation"}
    assert confidentiality["coverage_status"] == "部分覆盖"
    for key, row in shared.items():
        assert row["status"] == counterpart[key]["status"]
        assert row["fact_identity"] == counterpart[key]["fact_identity"]
        assert row.get("supporting_evidence") == counterpart[key].get("supporting_evidence")
    partial = shared["material_disposition"]
    assert partial["status"] == "PARTIALLY_COVERED"
    assert "项目工作电脑" in partial["supporting_evidence"][0]["quote"]
    assert all(row["status"] == "MISSING" for key, row in shared.items() if key != "material_disposition")
    for review in (ownership, confidentiality):
        assert not {"developer_copy_retention", "post_project_use_and_disposition"} & {e["element_id"] for e in review["coverage_elements"]}
        expected = set(review["decision_trace"]["final_missing_element_ids"])
        risk = next(f for f in report["risk_findings"] if review["item_id"] in f["source_review_ids"])
        assert {e["element_id"] for e in risk["final_missing_elements"]} == expected
        for row in risk["final_missing_elements"]:
            label = engine._uncovered_element_label(row).rstrip("。")
            assert label in risk["issue"]
            assert label in risk["recommendation"]
        assert "保密资料及复制件、备份的返还、删除或销毁机制" not in review["risk_point_description"]


def test_shared_disposal_is_one_canonical_issue_in_the_production_report(report):
    sources = {"TC-05-03", "TC-11-03"}
    matches = [f for f in report["risk_findings"] if sources.intersection(f["source_review_ids"])]
    assert len(matches) == 1
    finding = matches[0]
    assert sources | {"TC-09-03"} <= set(finding["source_review_ids"])
    audit = finding["aggregation_signals"]["underlying_issue"]
    assert len(audit["source_group_keys"]) == 2
    assert audit["all_source_clause_ids"]
    for rule in sources:
        review = item(report, rule)
        assert review["coverage_status"] == "部分覆盖"
        assert finding["finding_id"] in review["related_risks"]
        assert underlying_issue_signature(review) == underlying_issue_signature(finding)
    themes = [t for t in report["risk_themes"] if sources.intersection(t["source_rule_ids"])]
    assert len(themes) == 1
    assert sources | {"TC-09-03"} <= set(themes[0]["source_rule_ids"])
    assert themes[0]["canonical_title"] == finding["canonical_title"] == finding["title"]
    dispositions = [d for d in report["final_dispositions"] if sources.intersection(d["review_ids"])]
    assert len(dispositions) == 1
    assert dispositions[0]["risk_id"] == finding["finding_id"]
    assert dispositions[0]["risk_title"] == finding["canonical_title"]
    assert not group_duplicate_underlying_issues(report["risk_findings"])
    assert report["risk_theme_count"] == len(report["risk_themes"])
    rule_count = len({r for f in report["risk_findings"] for r in f["source_review_ids"]})
    assert f"规则级审查命中数：{rule_count}" in report["result"]


def test_production_release_gate_blocks_duplicate_scoped_issues(report):
    reviews = [model(row) for row in report["items"]]
    fields_allowed = {f.name for f in fields(engine.RiskFinding)}
    findings = [engine.RiskFinding(**{k: deepcopy(v) for k, v in row.items() if k in fields_allowed})
                for row in report["risk_findings"]]
    duplicate = deepcopy(next(f for f in findings if "TC-11-03" in f.source_review_ids))
    duplicate.finding_id += "-DUPLICATE"
    duplicate.title = "Different display title cannot hide a duplicate issue"
    findings.append(duplicate)
    failures = report_state_consistency_failures(reviews, findings)
    assert any(e.get("reason") == "DUPLICATE_UNDERLYING_ISSUE" for e in failures)
    assert engine._release_quality_gate(reviews, findings, report["result"])["status"] == "BLOCKED"


def test_applicability_prose_matches_the_active_entrusted_branch(report):
    review = model(item(report, "TC-05-03"))
    assert review.applicability["status"] in {"APPLICABLE", "CONDITIONALLY_APPLICABLE"}
    assert "适用于委托开发或合作开发" in review.applicable_if
    review.applicable_if = review.applicable_if.replace("委托开发或合作开发", "合作开发")
    failures = report_state_consistency_failures([review], [])
    assert any(e.get("reason") == "APPLICABILITY_DESCRIPTION_EXCLUDES_ACTIVE_TRANSACTION" for e in failures)
    assert engine._release_quality_gate([review], [], report["result"])["status"] == "BLOCKED"


def test_completed_negative_check_does_not_leave_an_obsolete_manual_review(report):
    review = item(report, "TC-10-04")
    assert review["coverage_status"] == "通过"
    assert not review["needs_manual_review"]
    assert not review["quality_gate_failure_reason"]
    assert "人工复核" not in review["action_suggestion"]
    assert not review["decision_trace"].get("manual_review_record")
    assert not any(row["coverage_status"] in {"通过", "PASS", "已覆盖"} and row["needs_manual_review"] for row in report["items"])


def test_service_acceptance_cannot_borrow_personnel_or_product_evidence(report):
    review = item(report, "TC-09-02")
    assert review["applicability"]["status"] == "APPLICABLE"
    assert review["coverage_status"] != "通过"
    assert review["decision_trace"]["atomic_requirement_family"] == "service_acceptance"
    assert "core_contract_arrangement" not in {e["element_id"] for e in review["coverage_elements"]}
    assert all("涉密人员" not in str(e.get("supporting_evidence")) for e in review["coverage_elements"])
    assert "第十一条第2项" not in review["evidence_location"]
    assert all(e["status"] == "MISSING" for e in review["coverage_elements"])
    assert {r["element_id"] for r in review["decision_trace"]["element_absence_searches"] if r["result"] == "NOT_FOUND"} == set(review["decision_trace"]["final_missing_element_ids"])


def test_na_excludes_the_economic_trigger_without_denying_secret_material(report):
    review = item(report, "TC-12-03")
    assert review["coverage_status"] == "不适用"
    reasons = [review["applicability"][key] for key in ("reason", "machine_reason", "user_reason")]
    assert len(set(reasons)) == 1
    assert all("合同虽涉及技术秘密或保密资料" in reason for reason in reasons)
    assert "未形成可识别的技术秘密范围" not in report["result"]


def test_release_gate_rejects_reintroduced_manual_and_wrong_domain_support(report):
    review = model(item(report, "TC-10-04"))
    review.needs_manual_review = True
    assert engine._release_quality_gate([review], [], report["result"])["status"] == "BLOCKED"
    quality = model(item(report, "TC-09-02"))
    row = quality.coverage_elements[0]
    wrong = {"clause_id": "wrong", "quote": "涉密人员：直接参与项目研发、测试、管理及验收的人员。"}
    row.update(status="COVERED", supporting_evidence=[wrong], evidence_ids=["wrong"], supporting_evidence_ids=["wrong"])
    quality.evidence_clauses = [{**wrong, "element_ids": [row["element_id"]]}]
    errors = engine._exact_element_report_invariants([quality], [])
    assert any(e.get("reason") == "NO_OPERATIVE_ACCEPTANCE_REQUIREMENT" for e in errors), errors
    assert engine._release_quality_gate([quality], [], report["result"])["status"] == "BLOCKED"


def test_gate_rejects_shared_fact_and_stale_na_reason_mutations(report):
    a, b = (deepcopy(item(report, rule)) for rule in ("TC-05-03", "TC-11-03"))
    first = next(e for e in a["coverage_elements"] if e["element_id"] == "material_disposition")
    second = next(e for e in b["coverage_elements"] if e["element_id"] == "material_disposition")
    first["status"], second["status"] = "COVERED", "MISSING"
    assert any(e["reason"] == "CROSS_RULE_SCOPED_FACT_STATUS_CONFLICT" for e in report_state_consistency_failures([a, b]))
    reviews = deepcopy(report["items"])
    secret = next(r for r in reviews if r["item_id"] == "TC-12-03")
    secret["applicability"]["user_reason"] = "当前合同未形成可识别的技术秘密范围，本项不适用。"
    assert any(e["reason"] == "NA_REASON_DENIES_CONFIRMED_PREREQUISITE" for e in report_state_consistency_failures(reviews))


def test_late_positive_material_projection_retains_exact_evidence_ownership(report):
    review = model(item(report, "TC-11-03"))
    clauses = parse_contract_clauses("第一条 项目结束\n合同终止后，乙方应返还甲方全部资料。")
    assert engine._project_shared_material_disposition(review, clauses, [{"actor": "乙方", "material_owner": "甲方"}])
    covered = next(e for e in review.coverage_elements if e["element_id"] == "material_disposition")
    assert covered["status"] == "COVERED"
    assert not engine._review_evidence_element_gate([review])["mismatches"]


def test_unmodeled_ownership_is_not_replaced_by_disposal_requirements(report):
    review = model(item(report, "TC-05-03"))
    review.coverage_elements = [{"element_id": "core_contract_arrangement", "status": "UNCERTAIN"}]
    original = deepcopy(review)
    clauses = parse_contract_clauses("第一条 项目结束\n合同终止后，乙方应返还甲方全部资料。")
    assert not engine._project_shared_material_disposition(review, clauses, [{"actor": "乙方"}], preserve_ownership=True)
    assert review == original


def test_multiple_disposal_scopes_do_not_share_a_positive_fact_bucket(report):
    review = model(item(report, "TC-11-03"))
    clauses = parse_contract_clauses("第一条 项目结束\n合同终止后，乙方应返还甲方全部资料。")
    scopes = [{"actor": "乙方", "material_owner": "甲方"}, {"actor": "丙方", "material_owner": "甲方"}]
    assert engine._project_shared_material_disposition(review, clauses, scopes)
    buckets = review.decision_trace["direct_fact_bindings"]
    rows = review.coverage_elements
    assert len({row["source_fact_key"] for row in rows}) == len(rows)
    for row in rows:
        if row["obligated_party"] == "丙方":
            assert row["status"] == "MISSING"
            assert not buckets.get(row["source_fact_key"])
    assert not engine._review_evidence_element_gate([review])["mismatches"]


def test_final_report_passes_all_original_and_new_gates(report):
    assert report["release_quality_gate"]["status"] == "REPORT_READY", report["release_quality_gate"]
    assert not report["release_quality_gate"]["failures"]
    assert not report_state_consistency_failures(report["items"], report["risk_findings"])


def test_final_statistics_are_derived_from_the_same_report_objects(report):
    overview = report["final_overview_summary"]
    severities = Counter(row["severity"] for row in report["risk_findings"])
    assert overview["major_risk"] == severities["HIGH"] + severities["CRITICAL"]
    assert overview["medium_risk"] == severities["MEDIUM"]
    assert overview["low_risk"] == severities["LOW"]
    assert sum(overview[key] for key in ("major_risk", "medium_risk", "low_risk")) == len(report["risk_findings"])
    assert overview["manual_review"] == len(report["manual_review_items"])
    assert not any(row["coverage_status"] == "通过" and row["needs_manual_review"] for row in report["items"])
    coverage = Counter(row["coverage_status"] for row in report["items"])
    for label, status in (("已覆盖", "通过"), ("部分覆盖", "部分覆盖"), ("缺失", "缺失"), ("不适用", "不适用")):
        assert f"- {label}：{coverage[status]} 项" in report["result"]
    assert f"风险主题数（聚合后）：{len(report['risk_findings'])}" in report["result"]
    assert f"人工复核项：{overview['manual_review']}" in report["result"]


@pytest.mark.parametrize("reason", ["NEEDS_EXTERNAL_VERIFICATION", "CONDITIONAL_PREREQUISITE_UNKNOWN"])
def test_negative_check_must_not_clear_an_unrelated_pending_review(reason, report):
    review = model(item(report, "TC-10-04"))
    review.needs_manual_review = True
    review.quality_gate_failure_reason = reason
    review.decision_trace["negative_clause_check"] = {"search_coverage": "SUFFICIENT", "adverse_clause_exists": False, "confidence": "high"}
    engine._resolve_completed_negative_check_review(review)
    assert review.needs_manual_review
