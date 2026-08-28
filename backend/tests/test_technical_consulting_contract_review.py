import io

import pytest
from docx import Document
from fastapi.testclient import TestClient

from auth.routes import get_current_user
from main import app
from review_v2.engine import TECHNICAL_CONSULTING_EVIDENCE_IMPLEMENTATION
from review_v2.engine import review_contract_v2
from review_v2.clause_parser import parse_contract_clauses
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


CONSULTING_ELEMENT_EVIDENCE_CONTRACT = """
项目名称：新能源汽车动力电池生产线节能优化技术咨询项目
甲方（委托方）：测试甲方
乙方（咨询方）：测试乙方
第一条 咨询事项
乙方针对动力电池生产线能耗数据、主要耗能设备和工艺流程进行分析评估，设计节能改造方案并提交最终技术咨询报告。
第二条 咨询报酬
甲方支付咨询报酬人民币20万元。
第三条 咨询资料
甲方应向乙方提供能耗数据、生产线图纸、设计资料、适用规范和其他咨询所需信息，并保证资料真实、完整。
第四条 保密
保密资料包括双方在项目中接触的商业秘密、技术秘密、图纸、设计资料、规范和未公开信息。
双方承担保密义务，未经对方书面同意不得向第三方披露，但已公开信息和依法必须披露的信息除外。
在任何情形下，本条规定的保密义务应持续有效。
第五条 咨询报告瑕疵救济
甲方对报告不满意的，可以通知乙方整改；乙方应在收到通知后10日内完成修改并重新提交。
整改后仍不能达到验收标准的，甲方可以解除合同，乙方应退还已付款并按年利率4%支付利息。
"""


def test_consulting_elements_and_evidence_are_status_separated_and_contract_grounded():
    output = review_contract_v2(
        CONSULTING_ELEMENT_EVIDENCE_CONTRACT,
        "technology",
        use_llm=False,
        profile=UserRiskProfile(user_identity="甲方/委托方"),
    )
    by_id = _items(output)

    assert by_id["TC-01-03"]["coverage_status"] == "通过"
    assert "专利" not in by_id["TC-01-03"]["narrative_state"]["judgment"]
    assert by_id["TC-13-01"]["coverage_status"] == "不适用"

    materials = by_id["TC-08-03"]
    assert materials["coverage_status"] in {"通过", "部分覆盖"}
    assert "第三条" in str(materials["evidence_clauses"][0]["location"])
    assert "甲方应向乙方提供" in materials["evidence_clauses"][0]["raw_text"]

    remedy = by_id["TC-08-04"]
    remedy_elements = {row["element_id"]: row["status"] for row in remedy["coverage_elements"]}
    assert remedy_elements == {
        "defect_trigger": "COVERED",
        "correction_period": "COVERED",
        "correction_remedy": "COVERED",
        "termination_remedy": "COVERED",
        "refund_remedy": "COVERED",
    }

    confidentiality = by_id["TC-11-02"]
    state = confidentiality["narrative_state"]
    assert confidentiality["coverage_status"] == "部分覆盖"
    assert state["covered_elements"]
    assert state["missing_elements"]
    assert not set(state["covered_elements"]) & set(state["missing_elements"])
    assert "持续有效" in " ".join(row.get("raw_text", "") for row in confidentiality["evidence_clauses"])
    assert "终止后三年" not in output["result"]
    assert "尚未覆盖：双方保密" not in output["result"]


def test_vague_consulting_material_obligation_has_specific_attachment_gaps():
    output = review_contract_v2(
        CONSULTING_ELEMENT_EVIDENCE_CONTRACT + "\n第六条 乙方应提供相关技术资料。",
        "technology",
        use_llm=False,
        profile=UserRiskProfile(user_identity="甲方/委托方"),
    )
    item = _items(output)["TC-13-01"]
    missing_ids = {
        row["element_id"] for row in item["coverage_elements"] if row["status"] == "MISSING"
    }

    assert item["coverage_status"] == "部分覆盖"
    assert missing_ids == {
        "material_names_and_types",
        "material_version_and_quantity",
        "material_delivery_form",
        "material_receipt_confirmation",
    }
    assert "技术资料附件”事项" not in item["narrative_state"]["judgment"]


CONSULTING_CONFIDENTIALITY_BINDING_CONTRACT = CONSULTING_ELEMENT_EVIDENCE_CONTRACT + """
第六条 保密范围与义务
保密资料包括与本项目有关的经营情况、财务情况、商业秘密、技术秘密、图纸和其他未公开信息。
双方应采取适当措施严格保密，未经信息拥有方书面同意，不得使用或向第三方泄露从对方获得的保密信息。
公众已知信息以及法律法规或司法程序要求披露的信息不属于违反保密义务，但依法披露前应尽合理努力通知信息拥有方。
在任何情形下，本条规定的保密义务应持续有效。
第七条 保密违约救济
任何一方违反保密义务的，守约方可以解除合同，并可采取法律允许的其他补救措施。
"""


def test_consulting_confidentiality_elements_bind_to_actual_clause_evidence():
    output = review_contract_v2(
        CONSULTING_CONFIDENTIALITY_BINDING_CONTRACT,
        "technology",
        use_llm=False,
        profile=UserRiskProfile(user_identity="甲方/委托方"),
    )
    by_id = _items(output)

    tc1101 = by_id["TC-11-01"]
    tc1101_elements = {row["element_id"]: row for row in tc1101["coverage_elements"]}
    assert tc1101["coverage_status"] == "部分覆盖"
    for element_id in (
        "confidential_information_scope",
        "confidentiality_obligation",
        "third_party_disclosure_restriction",
        "confidentiality_duration",
    ):
        assert tc1101_elements[element_id]["status"] == "COVERED"
        assert tc1101_elements[element_id]["evidence_ids"]
    assert tc1101_elements["purpose_limitation"]["status"] == "PARTIALLY_COVERED"
    assert tc1101_elements["purpose_limitation"]["evidence_ids"]

    tc1102 = by_id["TC-11-02"]
    tc1102_elements = {row["element_id"]: row for row in tc1102["coverage_elements"]}
    assert tc1102["coverage_status"] == "部分覆盖"
    assert tc1102_elements["confidential_information_scope"]["status"] == "COVERED"
    assert tc1102_elements["confidentiality_period"]["status"] == "COVERED"
    assert tc1102_elements["public_information_exception"]["status"] == "COVERED"
    assert tc1102_elements["required_disclosure_exception"]["status"] == "PARTIALLY_COVERED"
    assert tc1102_elements["lawful_third_party_source_exception"]["status"] == "MISSING"
    assert tc1102_elements["independent_development_exception"]["status"] == "MISSING"
    assert "终止后三年" not in output["result"]

    tc1104 = by_id["TC-11-04"]
    tc1104_elements = {row["element_id"]: row for row in tc1104["coverage_elements"]}
    assert tc1104["coverage_status"] == "部分覆盖"
    assert tc1104_elements["confidentiality_obligation"]["status"] == "COVERED"
    assert tc1104_elements["confidentiality_obligation"]["evidence_ids"]
    assert tc1104_elements["breach_damage_liability"]["status"] == "PARTIALLY_COVERED"
    assert tc1104_elements["breach_damage_liability"]["evidence_ids"]
    assert tc1104_elements["stop_use"]["status"] == "MISSING"
    assert tc1104_elements["return_delete_destroy"]["status"] == "MISSING"

    for item_id in ("TC-11-01", "TC-11-02", "TC-11-04"):
        item = by_id[item_id]
        for element in item["coverage_elements"]:
            if element["status"] in {"COVERED", "PARTIALLY_COVERED"}:
                assert element["evidence_ids"], (item_id, element["element_id"])
        assert not (
            item["coverage_status"] in {"通过", "部分覆盖"}
            and item["evidence_location"] == "合同正文及附件中未找到对应约定"
        )


def test_consulting_material_direct_obligation_ranks_before_collection_progress():
    output = review_contract_v2(
        CONSULTING_ELEMENT_EVIDENCE_CONTRACT,
        "technology",
        use_llm=False,
        profile=UserRiskProfile(user_identity="甲方/委托方"),
    )
    item = _items(output)["TC-08-03"]
    first = item["evidence_clauses"][0]["raw_text"]
    assert "甲方应向乙方提供" in first
    assert "资料收集" not in first


def test_contract_section_parser_keeps_confidentiality_section_visible_with_offsets():
    text = """
第一条 服务
乙方提供技术咨询服务。
第二条 付款
甲方应支付咨询报酬。
第三条 责任
违约方应承担违约责任。
第四条 保密
双方应对商业秘密和技术秘密严格保密，未经书面同意不得向第三方披露。本条保密义务持续有效。
第五条 保证
乙方保证咨询报告符合约定。
"""
    clauses = parse_contract_clauses(text)
    article_clauses = {
        clause.location.split("第")[1].split("条")[0]: clause
        for clause in clauses
        if clause.location.startswith("第") and "条" in clause.location
    }

    for article in ("一", "二", "三", "四", "五"):
        assert article in article_clauses
        clause = article_clauses[article]
        assert clause.start_offset >= 0
        assert clause.end_offset > clause.start_offset
    confidentiality = article_clauses["四"]
    assert "商业秘密" in confidentiality.text
    assert "不得向第三方披露" in confidentiality.text
    assert "持续有效" in confidentiality.text


def test_production_file_endpoint_uses_active_consulting_evidence_implementation():
    document = Document()
    for line in CONSULTING_CONFIDENTIALITY_BINDING_CONTRACT.strip().splitlines():
        document.add_paragraph(line)
    buffer = io.BytesIO()
    document.save(buffer)

    app.dependency_overrides[get_current_user] = lambda: {"id": 1, "phone": "test"}
    try:
        with TestClient(app) as client:
            response = client.post(
                "/review-v2/file",
                files={
                    "file": (
                        "consulting-production-path.docx",
                        buffer.getvalue(),
                        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    )
                },
                data={
                    "contract_type": "technology",
                    "include_low_risk": "true",
                    "use_llm": "false",
                    "profile_json": '{"user_identity":"甲方/委托方"}',
                },
            )
    finally:
        app.dependency_overrides.pop(get_current_user, None)

    assert response.status_code == 200
    payload = response.json()
    trace = payload["production_path_trace"]
    assert trace["entrypoint"] == "routers.review_v2.review_v2_file"
    assert trace["engine_function"] == "review_v2.engine.review_contract_v2"
    assert trace["evidence_implementation"] == TECHNICAL_CONSULTING_EVIDENCE_IMPLEMENTATION
    assert trace["cache"]["status"] == "MISS"
    assert trace["input_visibility"]["confidentiality_terms_present"] is True

    by_id = {item["item_id"]: item for item in payload["items"]}
    for item_id in ("TC-11-01", "TC-11-02", "TC-11-03", "TC-11-04", "TC-08-03"):
        assert by_id[item_id]["decision_trace"]["implementation_identity"]["version"] == TECHNICAL_CONSULTING_EVIDENCE_IMPLEMENTATION
    assert by_id["TC-11-01"]["coverage_status"] == "部分覆盖"
    assert by_id["TC-11-02"]["coverage_status"] == "部分覆盖"
    assert by_id["TC-11-03"]["coverage_status"] == "缺失"
    assert by_id["TC-11-04"]["coverage_status"] == "部分覆盖"
    assert "甲方应向乙方提供" in by_id["TC-08-03"]["evidence_clauses"][0]["raw_text"]
