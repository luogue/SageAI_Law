from pathlib import Path

from docx import Document

from review_v2.engine import review_contract_v2
from review_v2.user_profile import UserRiskProfile


FIXTURE = Path(__file__).resolve().parents[2] / "test_data" / "8、技术服务.docx"


def _review() -> dict:
    document = Document(str(FIXTURE))
    text = "\n".join(paragraph.text for paragraph in document.paragraphs if paragraph.text.strip())
    return review_contract_v2(
        text,
        "technology",
        use_llm=False,
        profile=UserRiskProfile(
            user_identity="乙方/技术服务提供方",
            contract_scenario="高校科研数据治理技术服务",
        ),
    )


def test_report_sections_project_the_same_evidence_bundle():
    output = _review()
    projections = output["report_evidence_projection"]
    for risk_id, row in projections.items():
        assert row["summary_bundle_id"] == row["risk_detail_bundle_id"] == row["review_detail_bundle_id"]
        assert row["summary_evidence_ids"] == row["risk_detail_evidence_ids"] == row["review_detail_evidence_ids"]
        assert row["bundle_id"] in output["result"]


def test_claim_level_bundles_are_complete_and_deduplicated():
    findings = {row["risk_group"]: row for row in _review()["risk_findings"]}
    for finding in findings.values():
        bundle = finding.get("evidence_bundle") or {}
        if not bundle:
            continue
        assert bundle["bundle_id"]
        assert set(bundle["required_claim_ids"]) <= set(bundle["supported_claim_ids"])
        assert not bundle["unsupported_claim_ids"]
        keys = [
            (row["clause_node_id"], row["start_offset"], row["end_offset"], row["claim_id"])
            for row in bundle["items"]
        ]
        assert len(keys) == len(set(keys))
        assert all(row["claim_id"] and row["entailment_score"] >= 0.8 for row in bundle["items"])

    payment = findings["payment_formula_inconsistency"]["evidence_bundle"]
    node_items = [row for row in payment["items"] if row["fact_type"].startswith("payment_node_")]
    assert len(node_items) == 4
    assert all("合同总额的" in row["quoted_text"] and "人民币" in row["quoted_text"] for row in node_items)
    total = next(row for row in payment["items"] if row["fact_type"] == "contract_total")
    assert "人民币" in total["quoted_text"] and "元" in total["quoted_text"]
    calculation = next(row for row in payment["items"] if row["fact_type"] == "calculation_result")
    assert all(term in calculation["quoted_text"] for term in ("付款比例", "付款金额", "差额"))


def test_semantic_fact_roles_exclude_keyword_collisions():
    findings = {row["risk_group"]: row for row in _review()["risk_findings"]}

    liability = " ".join(row["quoted_text"] for row in findings["technical_uncapped_cumulative_liability"]["evidence_bundle"]["items"])
    assert "甲方未按合同约定" not in liability
    assert "不可抗力事件结束" not in liability
    assert "通用算法、规则模板、技术框架" not in liability

    objection = " ".join(row["quoted_text"] for row in findings["short_data_objection_deemed_acceptance"]["evidence_bundle"]["items"])
    assert "现场调研" not in objection
    assert "视为甲方提供的全部资料" in objection

    retention = " ".join(row["quoted_text"] for row in findings["data_retention_warranty_conflict"]["evidence_bundle"]["items"])
    assert "支付合同总额" not in retention
    assert "归还或者删除" in retention and "12个月" in retention and "保证期内" in retention

    remediation = " ".join(row["quoted_text"] for row in findings["external_change_free_remediation"]["evidence_bundle"]["items"])
    assert "调整业务规则" in remediation and "先行完成修正" in remediation and "无偿修正" in remediation


def test_issue_types_describe_formula_conflict_validity_and_partial_gap():
    findings = {row["risk_group"]: row for row in _review()["risk_findings"]}
    assert findings["payment_formula_inconsistency"]["issue_type"] == "FORMULA_ERROR"
    assert findings["technical_background_ip_overtransfer"]["issue_type"] == "CONFLICTING"
    assert findings["technical_timeline_conflict"]["issue_type"] == "CONFLICTING"
    assert findings["data_retention_warranty_conflict"]["issue_type"] == "CONFLICTING"
    assert findings["personal_injury_liability_exclusion"]["issue_type"] == "INVALID_OR_UNENFORCEABLE"
    assert findings["personal_information_processing_gap"]["issue_type"] == "PARTIAL"
    assert findings["legal_reference"]["issue_type"] == "OUTDATED_REFERENCE"


def test_applicability_display_uses_the_resolved_decision_reason():
    items = {row["item_id"]: row for row in _review()["items"]}
    for review_id in ("TC-03-01", "TC-03-02", "TC-03-03"):
        reason = items[review_id]["applicability"]["user_reason"]
        assert "自然人" in reason or "员工" in reason
        assert "技术合同均适用" not in reason
    assert "受让人或被许可人" in items["TC-12-01"]["applicability"]["user_reason"]
    assert "技术秘密丧失秘密性后的使用与费用处理" in items["TC-12-03"]["applicability"]["user_reason"]
    assert "第三方权利主张" not in items["TC-12-04"]["applicable_if"]


def test_report_explains_summary_truncation_and_uses_non_placeholder_partial_text():
    output = _review()
    report = output["result"]
    view = output["report_view_model"]
    # The summary keeps all current fact-driven service risks, including the
    # acceptance-link, confidentiality, third-party-claim and material checks;
    # only the highest-priority ten are expanded in the overview.
    assert view["summary_total_count"] == len(output["risk_findings"])
    disclosure = (
        f"以下展示优先级最高的{view['summary_displayed_count']}项，"
        f"其余{view['summary_remaining_count']}项见完整风险明细"
    )
    # The report may use the risk-theme projection, which intentionally shows
    # every aggregated theme instead of truncating to ten.  Both display modes
    # must still account for every current finding.
    if disclosure not in report:
        summary_section = report.split("## 三、", 1)[0]
        assert all(finding["title"] in summary_section for finding in output["risk_findings"])
    assert "建议优先修改" in report
    assert "仍需补足：\u201c个人信息委托处理条款缺失\u201d所需的保护机制" not in report
    assert "没有完整约定处理目的、期限、方式、安全措施、监督、转委托及终止后的返还删除机制" in report
