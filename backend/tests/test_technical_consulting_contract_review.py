import pytest

from review_v2.engine import review_contract_v2
from review_v2.user_profile import UserRiskProfile


CONSULTING_CONTRACT = """
技术咨询合同
项目名称：智能仓储管理系统技术可行性及架构优化咨询项目
委托方（甲方）：杭州启明科技有限公司
受托方（乙方）：北京智策技术咨询有限公司
签署日期：2020年7月15日

第一条 咨询内容、咨询要求和咨询方式
1、咨询内容：乙方对甲方现有智能仓储管理系统进行技术可行性分析和系统架构评估，分析系统架构、性能瓶颈、接口方案及技术风险。
2、咨询要求：乙方形成技术咨询报告，内容包括技术改造建议、推荐技术架构、实施路线、风险、成本及周期估算。
3、乙方不承担软件开发、技术实施或成果制造义务。

第二条 项目进度
乙方应按双方确认的咨询工作计划完成调研并提交咨询成果。

第三条 甲方协作事项
1、甲方提供系统架构图、数据库结构、ERP/WMS接口文档和系统性能数据。
2、甲方安排技术人员访谈，提供测试环境、系统访问权限并协助说明业务流程。
3、甲方保证资料真实、完整，并通过加密电子文件及现场交接方式提供。

第四条 技术咨询报酬和支付方式
1、技术咨询报酬总额为180,000元（含税），分三期支付：合同生效后5个工作日、提交咨询报告初稿后5个工作日、最终验收通过后10个工作日。
2、收款账户、开户银行和帐号以本条所列信息为准。

第五条 保密
1、保密内容包括甲方的系统架构、源代码、接口资料、业务数据、仓储运营数据及其他未公开技术和经营信息，以及乙方的非公开咨询方法、分析模型和技术方案。
2、涉密人员范围为参与本项目的双方员工及外部顾问。
3、保密期限为合同有效期内及合同终止后3年。
4、违反保密义务造成对方损失的，应赔偿实际损失。

第六条 联系与协调
双方通过指定项目联系人协调咨询工作。

第七条 咨询成果和验收
1、乙方提交电子版及纸质版技术咨询报告。
2、咨询报告应完整覆盖第一条约定内容，并就架构、性能瓶颈、改造路线和主要风险提出明确意见。
3、甲方组织技术人员书面验收。

第八条 咨询成果瑕疵救济
因乙方原因导致咨询成果明显不符合合同约定内容的，乙方应在甲方要求的合理期限内免费修改。

第九条 咨询决策风险
甲方按照乙方符合本合同约定标准和方式完成的技术咨询工作成果作出决策并予以实施所造成的损失，按以下第1种方式处理：
1、乙方不承担责任。
2、乙方承担部分责任。具体承担方式为：无。

第十条 新技术成果
甲方利用咨询成果完成的新的技术成果归甲方所有；乙方利用甲方资料和工作条件完成的新的技术成果归乙方所有。

第十五条 技术文件
经双方书面盖章或确认的电子邮件确认后，下列文件为合同组成部分：《项目技术需求说明书》《现有系统技术资料清单》《项目咨询工作计划》《咨询成果验收确认单》。
"""


@pytest.fixture(scope="module")
def consulting_review() -> dict:
    return review_contract_v2(
        CONSULTING_CONTRACT,
        "technology",
        use_llm=False,
        profile=UserRiskProfile(user_identity="甲方/委托方"),
    )


def _items(output: dict) -> dict:
    return {item["item_id"]: item for item in output["items"]}


def test_consulting_context_and_role_are_single_source(consulting_review: dict):
    classification = consulting_review["deterministic_analysis"]["technology_classification"]
    context = consulting_review["report_context"]

    assert classification["primary_subtype"] == "TECHNICAL_CONSULTING"
    assert context["transaction_structure"] == "B2B_TECHNICAL_CONSULTING"
    assert context["usage_scenario_label"] == "技术咨询"
    assert context["contract_type_label"] == "技术合同—技术咨询合同"
    assert consulting_review["perspective_resolution"]["display_role"] == "甲方 / 委托方"
    assert consulting_review["result"].startswith("# 技术咨询合同审查报告")
    for stale_role in ("专利权受让方", "让与方", "被许可方", "许可方", "委托开发方", "合作开发方"):
        assert stale_role not in consulting_review["result"]


def test_consulting_tc08_rules_and_direct_evidence(consulting_review: dict):
    by_id = _items(consulting_review)
    assert [by_id[f"TC-08-0{index}"]["coverage_status"] for index in range(1, 5)] == ["通过"] * 4
    assert by_id["TC-08-05"]["coverage_status"] == "通过"
    assert by_id["TC-08-05"]["risk_level"] == "低"
    assert by_id["TC-08-05"]["action_priority"] == "NONE"

    locations = {
        item_id: " ".join(str(row.get("location") or "") for row in by_id[item_id]["evidence_clauses"])
        for item_id in ("TC-08-01", "TC-08-02", "TC-08-03", "TC-08-04")
    }
    quality_text = " ".join(
        str(row.get("quote") or row.get("text") or "") for row in by_id["TC-08-01"]["evidence_clauses"]
    )
    assert "咨询内容" in quality_text and "完整覆盖" in quality_text
    assert "第九条" in locations["TC-08-02"] and "第十一条" not in locations["TC-08-02"]
    assert "第三条" in locations["TC-08-03"]
    assert "第八条" in locations["TC-08-04"]


def test_consulting_subtype_applicability_is_isolated(consulting_review: dict):
    by_id = _items(consulting_review)
    assert by_id["TC-01-04"]["coverage_status"] == "不适用"
    for item_id in ("TC-10-01", "TC-10-02", "TC-10-03", "TC-10-04"):
        assert by_id[item_id]["coverage_status"] == "不适用"
        assert "当前技术咨询交易" in by_id[item_id]["applicability"]["reason"]
        assert "当前技术服务交易" not in by_id[item_id]["applicability"]["reason"]
    for item_id in ("TC-03-04", "TC-12-02", "TC-12-04", "TC-13-02", "TC-13-03"):
        assert by_id[item_id]["coverage_status"] == "不适用"


def test_consulting_confidentiality_uses_shared_atomic_evidence(consulting_review: dict):
    by_id = _items(consulting_review)
    expected = {
        "TC-11-01": ("部分覆盖", "中"),
        "TC-11-02": ("部分覆盖", "低"),
        "TC-11-03": ("缺失", "低"),
        "TC-11-04": ("部分覆盖", "中"),
    }
    for item_id, (coverage, level) in expected.items():
        assert by_id[item_id]["coverage_status"] == coverage
        assert by_id[item_id]["risk_level"] == level

    tc1104 = {row["element_id"]: row for row in by_id["TC-11-04"]["coverage_elements"]}
    assert tc1104["breach_damage_liability"]["status"] == "COVERED"
    assert tc1104["stop_disclosure"]["status"] == "MISSING"
    assert tc1104["return_delete_destroy"]["status"] == "MISSING"
    assert tc1104["specific_confidentiality_penalty"]["status"] == "NOT_APPLICABLE"

    evidence = by_id["TC-11-04"]["evidence_clauses"]
    assert "第五条第4项" in evidence[0]["location"]
    assert "违反保密义务" in evidence[0]["quote"]
    assert "实际损失" in evidence[0]["quote"]
    assert evidence[0]["semantic_evidence_type"] == "EXISTING_CONFIDENTIALITY_DAMAGE_LIABILITY"
    assert evidence[0]["semantic_support_level"] == "DIRECT"
    assert any(
        row.get("semantic_support_level") == "SUPPORTING" and "第五条第1项" in row["location"]
        for row in evidence[1:]
    )


def test_consulting_attachments_and_release_gate(consulting_review: dict):
    by_id = _items(consulting_review)
    attachment = by_id["TC-13-01"]
    assert attachment["coverage_status"] == "通过"
    assert all("第十五条" in str(row.get("location") or "") for row in attachment["evidence_clauses"])
    assert consulting_review["review_evidence_element_gate"]["mismatch_count"] == 0
    assert consulting_review["release_quality_gate"]["status"] == "REPORT_READY"
    assert consulting_review["system_metadata"]["technology_technical_consulting"] == "FROZEN_REGRESSION"
    assert consulting_review["result"]


def test_consulting_signing_law_context_is_not_false_positive(consulting_review: dict):
    by_id = _items(consulting_review)
    expected = {
        "TC-08-02": ("第359条", "第881条"),
        "TC-11-04": ("第113条", "第584条"),
    }
    for item_id, (historical_article, current_article) in expected.items():
        context = by_id[item_id]["decision_trace"]["legal_time_context"]
        assert context["signed_at"] == "2020-07-15"
        assert context["law_at_signing"] == "中华人民共和国合同法"
        assert historical_article in context["historical_reference"]
        assert current_article in context["current_reference"]
        assert context["status"] == "HISTORICAL_AT_SIGNING"
        assert context["display_text"] in consulting_review["result"]
    assert not any(finding.get("risk_type") == "legal_reference" for finding in consulting_review["risk_findings"])


def test_modern_consulting_contract_does_not_display_repealed_contract_law():
    modern_contract = CONSULTING_CONTRACT.replace("2020年7月15日", "2024年7月15日")
    output = review_contract_v2(
        modern_contract,
        "technology",
        use_llm=False,
        profile=UserRiskProfile(user_identity="甲方/委托方"),
    )
    by_id = _items(output)
    for item_id, article in (("TC-08-02", "第881条"), ("TC-11-04", "第584条")):
        context = by_id[item_id]["decision_trace"]["legal_time_context"]
        assert context["status"] == "CURRENT_LAW_AT_SIGNING"
        assert context["display_text"] == f"《中华人民共和国民法典》{article}"
    assert "签署时法律依据：《中华人民共和国合同法》" not in output["result"]


def test_consulting_party_b_role_is_not_development_role():
    output = review_contract_v2(
        CONSULTING_CONTRACT,
        "technology",
        use_llm=False,
        profile=UserRiskProfile(user_identity="乙方/受托方"),
    )
    assert output["perspective_resolution"]["display_role"] == "乙方 / 受托方"
    assert output["report_context"]["perspective"] == "technical_consultant"


def test_consulting_subtype_is_inferred_from_transaction_substance_without_explicit_title():
    title_neutral_contract = CONSULTING_CONTRACT.replace("技术咨询合同", "智能仓储项目协议", 1)
    output = review_contract_v2(
        title_neutral_contract,
        "technology",
        use_llm=False,
        profile=UserRiskProfile(user_identity="甲方/委托方"),
    )
    classification = output["deterministic_analysis"]["technology_classification"]
    by_id = _items(output)

    assert classification["primary_subtype"] == "TECHNICAL_CONSULTING"
    assert classification["primary_contract_type"] == "technology_consulting"
    assert "title:technical_consulting" not in classification["classification_evidence"]
    assert {
        "core_obligation:analysis_evaluation_advice",
        "deliverable:consulting_report_or_opinion",
        "consideration:consulting_fee",
    }.issubset(set(classification["classification_evidence"]))
    assert output["contract_context"]["contract_subtype"] == "TECHNICAL_CONSULTING"
    assert output["report_context"]["contract_type_label"] == "技术合同—技术咨询合同"
    assert all(by_id[f"TC-08-0{index}"]["coverage_status"] != "不适用" for index in range(1, 6))
    assert by_id["TC-01-03"]["coverage_status"] == "通过"
    assert by_id["TC-01-04"]["coverage_status"] == "不适用"
    assert all(by_id[f"TC-10-0{index}"]["coverage_status"] == "不适用" for index in range(1, 5))
    assert by_id["TC-11-01"]["coverage_status"] != "缺失"
    assert by_id["TC-11-02"]["coverage_status"] != "缺失"
    for item_id in ("TC-03-04", "TC-12-02", "TC-12-04", "TC-13-02"):
        assert by_id[item_id]["coverage_status"] == "不适用"
