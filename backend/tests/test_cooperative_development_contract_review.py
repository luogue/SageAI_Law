from pathlib import Path
from types import SimpleNamespace

import pytest
from docx import Document

from review_v2 import engine
from review_v2.engine import review_contract_v2
from review_v2.technology_service_analysis import classify_technology_transaction
from review_v2.user_profile import UserRiskProfile


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "test_data" / "11、合作.docx"


def _fixture_text() -> str:
    document = Document(str(FIXTURE))
    paragraphs = [paragraph.text for paragraph in document.paragraphs if paragraph.text.strip()]
    tables = ["\t".join(cell.text for cell in row.cells) for table in document.tables for row in table.rows]
    return "\n".join(paragraphs + tables)


@pytest.fixture(scope="module")
def cooperative_review() -> dict:
    return review_contract_v2(
        _fixture_text(),
        "technology",
        use_llm=False,
        profile=UserRiskProfile(user_identity="甲方/合作开发方"),
    )


def test_cooperative_development_classification(cooperative_review: dict):
    classification = cooperative_review["deterministic_analysis"]["technology_classification"]

    assert classification["primary_category"] == "TECHNICAL_CONTRACT"
    assert classification["primary_subtype"] == "COOPERATIVE_DEVELOPMENT"
    assert classification["development_mode"] == "COOPERATIVE_DEVELOPMENT"
    assert classification["confidence"] == "high"
    assert set(classification["classification_evidence"]) >= {
        "bilateral_research_investment",
        "bilateral_research_tasks",
        "joint_development_results",
        "joint_development_risk",
    }
    assert cooperative_review["report_context"]["contract_type_label"] == "技术合同—技术开发合同—合作开发合同"
    assert cooperative_review["contract_context"]["user_role"] == "cooperative_developer"
    assert cooperative_review["contract_context"]["counterparty_role"] == "cooperative_developer"
    assert cooperative_review["contract_context"]["perspective_resolution"]["display_role"] == "合作开发方"

    by_id = {row["item_id"]: row for row in cooperative_review["items"]}
    assert all(by_id[f"TC-05-0{index}"]["coverage_status"] != "不适用" for index in range(1, 5))
    assert all(by_id[f"TC-04-0{index}"]["coverage_status"] == "不适用" for index in range(1, 5))
    assert cooperative_review["release_quality_gate"]["status"] == "REPORT_READY"
    assert cooperative_review["result"].startswith("# 合作开发合同审查报告")


def test_commissioned_vs_cooperative_development():
    commissioned = classify_technology_transaction(
        "技术开发合同。甲方委托乙方研究开发智能平台，甲方支付研究开发经费100万元，"
        "乙方负责全部研究开发工作并向甲方交付成果。"
    )
    cooperative = classify_technology_transaction(
        "甲方投入研发人员和研发费用并负责算法模块开发；乙方投入研发人员和研发费用并负责接口模块开发。"
        "双方共同组织验收，共同享有开发成果，并各自承担正常技术风险下已经发生的研发费用。"
    )

    assert commissioned["development_mode"] == "ENTRUSTED_DEVELOPMENT"
    assert cooperative["development_mode"] == "COOPERATIVE_DEVELOPMENT"
    assert "bilateral_research_tasks" in cooperative["classification_evidence"]


def test_single_manual_review_does_not_abort_report(monkeypatch):
    original = engine._applicability_result_for_checkpoint

    def one_uncertain_item(checkpoint, clauses, applicable, reason, canonical_claims=None):
        result = original(checkpoint, clauses, applicable, reason, canonical_claims)
        if checkpoint.item_id == "TC-08-01":
            result.update({
                "status": "UNCERTAIN",
                "applicable": None,
                "reason": "合同未附咨询任务材料，无法确认该局部事项是否适用。",
                "machine_reason": "Missing consulting task attachment.",
                "user_reason": "合同未附咨询任务材料，需确认是否另有技术咨询任务及对应附件。",
                "depends_on": ["consulting_task_attachment"],
            })
        return result

    monkeypatch.setattr(engine, "_applicability_result_for_checkpoint", one_uncertain_item)
    output = review_contract_v2(
        _fixture_text(),
        "technology",
        use_llm=False,
        profile=UserRiskProfile(user_identity="甲方/合作开发方"),
    )

    assert output["release_quality_gate"]["status"] == "REPORT_READY"
    assert output["manual_review_summary"]["manual_review_count"] == 1
    assert output["manual_review_items"][0]["item_id"] == "TC-08-01"
    assert "需确认" in output["manual_review_items"][0]["reason"] or "无法确认" in output["manual_review_items"][0]["reason"]
    assert "正式报告已停止生成" not in output["result"]
    assert "人工复核事项" in output["result"]
    assert all(
        "TC-08-01" not in finding["source_review_ids"]
        for finding in output["risk_findings"]
    )


def test_manual_review_fact_contradiction_is_local_not_fatal():
    manual_item = SimpleNamespace(
        item_id="TC-XX-01",
        coverage_status=engine.INSUFFICIENT_CONTEXT,
        needs_manual_review=True,
        decision_trace={"fact_coverage_contradiction": {"status": "UNRESOLVED"}},
    )

    assert engine._recall_gate_failures(
        [manual_item],
        {"truncated": False, "parsed_character_ratio": 1.0},
    ) == []


def test_non_fatal_quality_gate_does_not_stop_report_generation():
    output = review_contract_v2(
        "培训服务合同。课程名称：数学培训。课程名称：英语培训。总课时：20节。"
        "上课时间：每周六上午。开课日期：2026年9月10日。预计结课日期：2027年6月30日。",
        "service",
        use_llm=False,
    )

    assert output["release_quality_gate"]["status"] == "BLOCKED"
    assert output["report_generation_decision"]["status"] == "GENERATED_WITH_QUALITY_WARNINGS"
    assert output["report_generation_decision"]["report_generated"] is True
    assert output["fatal_report_generation_gate"]["status"] == "PASS"
    assert output["result"].startswith("# ")
    assert "正式报告已停止生成" not in output["result"]


def test_only_global_input_failure_is_fatal():
    output = review_contract_v2("", "technology", use_llm=False)
    gate = output["fatal_report_generation_gate"]

    assert gate["status"] == "FATAL"
    assert gate["fatal_rule_ids"] == ["EMPTY_CONTRACT_BODY"]
    assert output["report_generation_decision"]["status"] == "STOPPED_FATAL"
    assert output["report_generation_decision"]["report_generated"] is False


def test_cooperative_rules_use_operational_facts_and_direct_evidence(cooperative_review: dict):
    by_id = {row["item_id"]: row for row in cooperative_review["items"]}

    assert by_id["TC-01-01"]["coverage_status"] == "通过"
    assert by_id["TC-01-04"]["coverage_status"] == "不适用"

    investment = by_id["TC-05-01"]
    assert investment["coverage_status"] == "通过"
    assert {row["element_id"] for row in investment["coverage_elements"]} == {
        "bilateral_research_investment",
        "investment_form_and_amount",
        "research_task_allocation",
        "budget_overrun_allocation",
        "technical_coordination",
        "major_decision_process",
    }
    investment_text = "\n".join(str(row.get("text") or "") for row in investment["evidence_clauses"])
    assert "120万元" in investment_text
    assert "100万元" in investment_text
    assert "各自超出的成本由各自承担" in investment_text

    exit_item = by_id["TC-05-04"]
    assert exit_item["coverage_status"] != "通过"
    exit_text = "\n".join(str(row.get("text") or "") for row in exit_item["evidence_clauses"])
    assert "源代码" in exit_text
    assert "自行决定是否" in exit_text
    assert "无权强制要求" in exit_text

    improvement = by_id["TC-10-02"]
    assert improvement["coverage_status"] == "部分覆盖"
    assert all("第十四条" in str(row.get("location") or "") for row in improvement["evidence_clauses"])
    assert all("净利润" not in str(row.get("text") or "") for row in improvement["evidence_clauses"])

    notification = by_id["TC-10-03"]
    assert notification["coverage_status"] == "缺失"
    assert notification["needs_manual_review"] is False
    assert notification["system_confidence"]["level"] == "high"
    assert "双方未约定" in str(notification["evidence_clauses"][0].get("text") or "")
    assert by_id["TC-10-04"]["coverage_status"] == "部分覆盖"

    confidentiality = by_id["TC-11-04"]
    assert confidentiality["coverage_status"] == "部分覆盖"
    assert {str(row.get("location") or "").split()[0] for row in confidentiality["evidence_clauses"]} == {
        "第十条",
        "第十五条",
    }
    confidentiality_quotes = "\n".join(str(row.get("quote") or "") for row in confidentiality["evidence_clauses"])
    assert "不得向第三方披露" in confidentiality_quotes
    assert "10万元违约金" in confidentiality_quotes
    assert "30万元违约金" in confidentiality_quotes

    infringement = by_id["TC-12-04"]
    assert infringement["coverage_status"] == "部分覆盖"
    assert all("第九条" in str(row.get("location") or "") for row in infringement["evidence_clauses"])

    assert by_id["TC-13-02"]["coverage_status"] == "部分覆盖"
    assert by_id["TC-13-03"]["coverage_status"] == "部分覆盖"
    assert cooperative_review["release_quality_gate"]["status"] == "REPORT_READY"


def test_cross_contract_risks_are_general_and_canonical(cooperative_review: dict):
    findings = cooperative_review["risk_findings"]
    by_finding_id = {row["finding_id"]: row for row in findings}

    expected = {
        "RF-LIABILITY-ASYMMETRY-001": "TECH-GEN-01",
        "RF-DISPUTE-CONFLICT-001": "TECH-GEN-02",
        "RF-TECH-RESTRICT-001": "TECH-GEN-03",
        "RF-TECH-OSS-001": "TECH-GEN-04",
        "RF-TECH-EXIT-001": "TC-05-04",
    }
    for finding_id, review_id in expected.items():
        assert finding_id in by_finding_id
        assert by_finding_id[finding_id]["source_review_ids"] == [review_id]
        assert sum(row["finding_id"] == finding_id for row in findings) == 1

    liability_text = str(by_finding_id["RF-LIABILITY-ASYMMETRY-001"])
    assert "10万元" in liability_text
    assert "30万元" in liability_text

    dispute_text = str(by_finding_id["RF-DISPUTE-CONFLICT-001"])
    assert "南京仲裁委员会" in dispute_text
    assert "甲方所在地有管辖权的人民法院" in dispute_text

    restriction_text = str(by_finding_id["RF-TECH-RESTRICT-001"])
    assert "3年" in restriction_text
    assert "200万元" in restriction_text

    open_source_text = str(by_finding_id["RF-TECH-OSS-001"])
    assert "SBOM" in open_source_text
