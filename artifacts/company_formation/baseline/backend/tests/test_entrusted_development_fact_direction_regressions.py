import pytest

from review_v2.engine import review_contract_v2
from review_v2.technology_service_analysis import analyze_timeline
from review_v2.user_profile import UserRiskProfile


ENTRUSTED_DEVELOPMENT_TEXT = """
软件委托开发合同
甲方（委托方）委托乙方（开发方）开发供应链预测系统。
开发期限自2027年1月1日起至2027年6月30日。系统应于2027年6月30日前上线。上线后进入2个月试运行期。试运行结束后7个工作日内进行最终验收。
合同履行中形成的全部前景知识产权归甲方所有。
开发过程中形成的算法和数据处理方法，其专利申请权归乙方所有，甲方仅在本项目使用。
因双方现有技术水平或数据质量导致项目无法实现目标的，属于无过错技术开发风险。发生该风险时，甲方已支付的研发费用不予退还，剩余研发费用仍应继续支付。
乙方应交付完整源代码，源代码应可独立编译、部署和运行。乙方无需交付其认为属于通用框架、基础算法库和内部工具的源代码。
乙方可以自行选择开源软件及第三方组件。由此产生的许可费用由甲方承担，知识产权纠纷损失由双方各承担50%。乙方自行开发内容侵权的，由乙方承担责任。
双方对履约中获知的商业秘密、技术资料、经营信息和业务数据承担保密义务。合同终止后，保密义务继续有效4年。
乙方可以将甲方业务数据和客户数据匿名化后用于模型训练、产品优化及其他客户商业项目，无需甲方书面同意。合同终止后乙方可保存数据3年，备份数据无需删除。
双方项目联系人可通过微信或电子邮件确认需求变更、费用、工期及验收结果，该确认与盖章补充协议具有同等效力。
"""


def _review(text: str):
    return review_contract_v2(
        text,
        "technology",
        use_llm=False,
        profile=UserRiskProfile(user_identity="甲方"),
    )


@pytest.fixture(scope="module")
def entrusted_review():
    return _review(ENTRUSTED_DEVELOPMENT_TEXT)


def _by_id(review):
    return {item["item_id"]: item for item in review["items"]}


def _elements(item):
    return {
        element["element_id"]: element
        for element in item.get("coverage_elements", [])
    }


def _evidence_text(item):
    return " ".join(
        str(row.get("quote") or row.get("text") or "")
        for row in item.get("evidence_clauses", [])
    )


def test_existing_failure_allocation_is_covered_adverse_not_missing(entrusted_review):
    item = _by_id(entrusted_review)["TC-04-04"]
    elements = _elements(item)

    assert item["coverage_status"] == "风险条款"
    assert item["issue_type"] == "ADVERSE"
    assert elements["no_fault_technical_risk_trigger"]["status"] == "COVERED"
    assert elements["paid_fee_refund"]["status"] == "ADVERSE"
    assert elements["unpaid_fee_obligation"]["status"] == "ADVERSE"
    assert elements["failed_project_result_disposition"]["status"] == "MISSING"
    assert "已支付的研发费用不予退还" in _evidence_text(item)
    assert "剩余研发费用仍应继续支付" in _evidence_text(item)


def test_general_foreground_ip_does_not_override_specific_patent_right(entrusted_review):
    item = _by_id(entrusted_review)["TC-04-03"]
    elements = _elements(item)

    assert item["issue_type"] == "CONFLICTING"
    assert elements["foreground_ip_general_ownership"]["status"] == "COVERED"
    assert elements["patent_application_right_ownership"]["status"] == "CONFLICTING"
    assert elements["patent_application_right_ownership"]["presence_status"] == "COVERED"
    assert "前景知识产权归甲方" in item["risk_point_description"]
    assert "专利申请权归乙方" in item["risk_point_description"]
    evidence = _evidence_text(item)
    assert "前景知识产权归甲方" in evidence
    assert "专利申请权归乙方" in evidence


def test_confidentiality_positive_facts_survive_search_audit(entrusted_review):
    item = _by_id(entrusted_review)["TC-11-02"]
    elements = _elements(item)

    for element_id in (
        "confidential_information_scope",
        "during_contract_confidentiality",
        "post_termination_confidentiality",
        "confidentiality_duration",
    ):
        assert elements[element_id]["status"] == "COVERED"
    assert "合同终止后，保密义务继续有效4年" in _evidence_text(item)
    audit_text = " ".join(
        str(row.get("quote") or row.get("text") or "")
        for row in item.get("evidence_clauses", [])
        if row.get("evidence_type") == "SEARCH_AUDIT"
    )
    assert "未找到合同终止或解除后继续有效的保密期限" not in audit_text
    assert "未找到合同终止或解除后的明确保密期限" not in audit_text


def test_secondary_data_use_is_an_independent_adverse_risk(entrusted_review):
    item = _by_id(entrusted_review)["TECH-SHARED-10"]
    elements = _elements(item)

    assert item["risk_group"] == "technology_data_secondary_use"
    assert item["issue_type"] == "ADVERSE"
    for element_id in (
        "performance_purpose_limitation",
        "training_and_product_optimization",
        "other_customer_or_commercial_use",
        "prior_written_consent",
        "post_termination_retention",
        "backup_deletion",
    ):
        assert elements[element_id]["status"] == "ADVERSE"
    assert elements["anonymization_or_deidentification"]["status"] == "COVERED"
    assert item["risk_group"] != "confidential_material_return_destroy"


def test_complete_source_delivery_is_checked_against_unilateral_carveout(entrusted_review):
    item = _by_id(entrusted_review)["TC-13-01"]
    elements = _elements(item)

    assert item["risk_group"] == "source_code_delivery_scope_conflict"
    assert item["issue_type"] == "CONFLICTING"
    assert elements["complete_source_delivery"]["status"] == "COVERED"
    assert elements["developer_unilateral_source_carveout"]["status"] == "CONFLICTING"
    assert all(term in item["legal_consequence_if_missing"] for term in (
        "编译", "部署", "运维", "修改", "二次开发", "更换供应商",
    ))


def test_developer_controlled_component_risk_keeps_direction_and_procedure_separate(entrusted_review):
    item = _by_id(entrusted_review)["TC-12-02"]
    elements = _elements(item)

    assert item["issue_type"] == "ADVERSE"
    assert elements["developer_component_selection_control"]["status"] == "COVERED"
    assert elements["third_party_component_risk_allocation"]["status"] == "ADVERSE"
    assert elements["claim_notice"]["status"] == "MISSING"
    assert elements["defense_control"]["status"] == "MISSING"
    assert "开发方控制组件选择" in item["risk_point_description"]
    assert "委托方" in item["risk_point_description"]


def test_development_deadline_and_post_deadline_acceptance_form_one_timeline_conflict(entrusted_review):
    timeline = analyze_timeline(ENTRUSTED_DEVELOPMENT_TEXT)
    conflict = next(
        row for row in timeline["conflicts"]
        if row["type"] == "MILESTONE_AFTER_PERFORMANCE_END_RELATIVE_CHAIN"
    )

    assert conflict["performance_end_date"] == "2027-06-30"
    assert conflict["milestone_base_date"] == "2027-06-30"
    assert conflict["trial_months"] == 2
    assert conflict["acceptance_working_days"] == 7
    item = _by_id(entrusted_review)["TECH-SHARED-03"]
    assert "上线后仍安排2个月试运行" in item["risk_point_description"]
    assert "7个工作日内" in item["risk_point_description"]
    assert any(
        row.get("location") == "确定性开发期限校验"
        for row in item.get("evidence_clauses", [])
    )


def test_project_contact_material_change_authority_is_adverse(entrusted_review):
    item = _by_id(entrusted_review)["GEN-AUTH-01"]
    elements = _elements(item)

    assert item["issue_type"] == "ADVERSE"
    assert elements["electronic_contact_confirmation"]["status"] == "COVERED"
    assert elements["material_change_binding_effect"]["status"] == "ADVERSE"
    assert elements["authorization_scope_and_limit"]["status"] == "MISSING"
    assert "表见代理" in item["legal_consequence_if_missing"]


def test_balanced_or_absent_arrangements_do_not_create_the_new_adverse_findings():
    text = """
    软件委托开发合同
    甲方（委托方）委托乙方（开发方）开发管理系统。
    开发期限自2027年1月1日至2027年6月30日，最终验收应在开发期限内完成。
    前景知识产权及专利申请权均归甲方所有。
    无过错技术风险导致研发失败时，双方按已完成工作量结算，未发生费用不再支付，乙方交付全部阶段成果。
    乙方交付完整源代码及全部构建依赖，甲方可独立编译、部署和维护。
    乙方选用的第三方组件由乙方完成许可核验并承担侵权责任。
    乙方仅可为履行本项目处理甲方数据，合同终止后删除全部数据和备份。
    项目联系人仅负责日常沟通，价款、范围、工期、验收标准及知识产权变更须经法定代表人或特别授权人员书面签署。
    """
    result = _review(text)
    items = _by_id(result)

    assert items["TC-04-03"]["issue_type"] != "CONFLICTING"
    assert items["TC-04-04"]["issue_type"] != "ADVERSE"
    assert items["TC-13-01"]["risk_group"] != "source_code_delivery_scope_conflict"
    assert items["TC-12-02"]["title"] != "开发方选用第三方组件但风险转嫁委托方"
    assert "TECH-SHARED-10" not in items
    assert "GEN-AUTH-01" not in items


def test_major_liability_cap_separates_statutory_validity_and_commercial_recovery_risks():
    result = _review("""
    软件委托开发合同
    甲方委托乙方开发工业设备预测系统并交付源代码。
    除乙方因故意或者重大过失造成甲方损失外，乙方累计赔偿责任最高不超过甲方已支付开发费的25%。
    前述责任上限同时适用于数据泄露、保密义务、第三方知识产权侵权和人身损害责任。
    """)
    items = _by_id(result)

    commercial = items["TC-12-04"]
    assert commercial["risk_group"] == "entrusted_major_liability_cap"
    assert commercial["issue_type"] == "ADVERSE"
    assert "数据泄露" in commercial["risk_point_description"]
    assert "第三方知识产权侵权" in commercial["risk_point_description"]
    assert "实际可追偿金额" in commercial["legal_consequence_if_missing"]
    assert set(_elements(commercial)) >= {
        "cumulative_liability_cap",
        "intent_and_gross_negligence_exception",
        "personal_injury_exception",
        "data_confidentiality_ip_cap",
    }

    validity = items["GEN-LIAB-02"]
    assert "人身损害" in validity["risk_point_description"]
    assert "民法典》第506条" in validity["legal_basis_index"]
    assert "任何和所有责任" not in validity["risk_point_description"]

    themes = [
        theme for theme in result["risk_themes"]
        if set(theme["source_rule_ids"]) & {"TC-12-04", "GEN-LIAB-02"}
    ]
    assert len(themes) == 1
    assert themes[0]["title"] == "责任限制机制风险"
    assert set(themes[0]["source_rule_ids"]) == {"TC-12-04", "GEN-LIAB-02"}
    assert themes[0]["underlying_finding_count"] == 2


def test_liability_cap_with_explicit_mandatory_exceptions_does_not_create_validity_false_positive():
    result = _review("""
    软件委托开发合同
    甲方委托乙方开发工业系统。
    乙方一般违约累计赔偿责任最高不超过合同总价。
    责任上限不适用于人身损害以及乙方故意或者重大过失造成甲方财产损失的情形。
    """)
    items = _by_id(result)

    assert "GEN-LIAB-02" not in items
    assert items["TC-12-04"]["risk_group"] != "entrusted_major_liability_cap"


def test_project_ip_reuse_conflict_is_independent_from_secondary_data_use():
    result = _review("""
    软件委托开发合同
    甲方委托乙方开发控制系统。
    本项目形成的软件著作权、程序代码、算法模型和技术方案等前景知识产权归甲方所有。
    乙方有权将本项目形成的代码结构、算法模型及技术方案用于其他客户项目。
    """)
    items = _by_id(result)

    item = items["TECH-SHARED-11"]
    assert item["issue_type"] == "CONFLICTING"
    assert "前景知识产权归甲方" in _evidence_text(item)
    assert "其他客户项目" in _evidence_text(item)
    assert "TECH-SHARED-10" not in items


def test_complex_project_short_deemed_acceptance_preserves_latent_defect_review():
    result = _review("""
    软件委托开发合同
    甲方委托乙方开发算法系统并交付源代码。
    系统上线后试运行三个月，最终验收要求连续稳定运行30日且接口响应时间不超过2秒。
    乙方提交验收申请后，甲方未在5个工作日内提出书面异议的，视为验收合格。
    """)
    item = _by_id(result)["TECH-SHARED-12"]
    elements = _elements(item)

    assert item["issue_type"] == "ADVERSE"
    assert elements["deemed_acceptance_clause"]["status"] == "ADVERSE"
    assert elements["complex_or_sustained_testing"]["status"] == "COVERED"
    assert elements["latent_defect_and_warranty_carveout"]["status"] == "MISSING"
    assert "隐蔽缺陷" in item["suggested_clause_example"]
    assert "连续稳定运行" in _evidence_text(item)


def test_reasonable_acceptance_period_with_latent_defect_carveout_is_not_flagged_as_short_deemed_acceptance():
    result = _review("""
    软件委托开发合同
    甲方委托乙方开发算法系统并交付源代码。
    系统上线后试运行一个月。
    甲方未在15个工作日内提出书面异议的，视为验收合格；该默示验收不影响隐蔽缺陷、质保责任和法定救济。
    """)
    assert "TECH-SHARED-12" not in _by_id(result)


def test_demand_reduction_exit_cost_uses_direct_clause_evidence_without_manual_review():
    result = _review("""
    软件委托开发合同
    甲方委托乙方开发管理系统。
    如甲方提出减少功能，除按照减少后的实际工作结算外，还应支付减少金额30%的补偿；
    调整后开发费用不得低于原合同总价的90%，低于90%的，乙方有权解除合同。
    """)
    item = _by_id(result)["GEN-COMM-01"]
    evidence = item.get("evidence_clauses", [])

    assert item["issue_type"] == "ADVERSE"
    assert item["needs_manual_review"] is False
    assert item["evidence_location"]
    assert any("减少金额30%的补偿" in str(row.get("quote") or row.get("text") or "") for row in evidence)
    assert any("不得低于原合同总价的90%" in str(row.get("quote") or row.get("text") or "") for row in evidence)
    assert all(str(row.get("source_type") or "").upper() != "SEARCH_AUDIT" for row in evidence)


def test_development_failure_full_price_exposure_is_direct_and_quantified():
    result = _review("""
    软件委托开发合同
    甲方委托乙方开发管理系统，合同总价为人民币800000元。
    因现有技术水平导致项目无法实现约定目标的，视为无过错技术开发风险。
    发生该风险时，甲方已支付的开发费用不予退还，剩余开发费用仍应继续支付。
    """)
    item = _by_id(result)["TC-04-04"]

    assert item["economic_impact"] == "high"
    assert item["economic_impact_detail"]["has_direct_financial_exposure"] is True
    assert item["economic_impact_detail"]["cash_flow_direction"] == "OUTFLOW_FROM_REVIEW_PARTY"
    assert item["economic_impact_detail"]["maximum_exposure_amount"] == 800000
    assert item["economic_impact_detail"]["contract_value_ratio"] == 1.0
    assert {row["clause_id"] for row in item["evidence_clauses"]} == {"C0003", "C0004"}


def test_confidentiality_covered_elements_bind_distinct_direct_evidence():
    result = _review("""
    软件委托开发合同
    甲方委托乙方开发管理系统。
    双方对履约中知悉的商业秘密和技术资料承担保密义务，不得向第三方披露。
    乙方违反保密义务的，应赔偿甲方全部实际损失。
    除乙方故意或重大过失外，乙方累计赔偿责任最高不超过已支付开发费的30%。
    """)
    item = _by_id(result)["TC-11-04"]
    elements = _elements(item)
    evidence_by_id = {
        str(row.get("clause_id") or row.get("evidence_id")): str(row.get("quote") or row.get("text") or "")
        for row in item["evidence_clauses"]
    }

    obligation_ids = elements["confidentiality_obligation"]["evidence_ids"]
    damage_ids = elements["breach_damage_liability"]["evidence_ids"]
    assert obligation_ids and damage_ids and obligation_ids != damage_ids
    assert all("保密义务" in evidence_by_id[evidence_id] for evidence_id in obligation_ids)
    assert all("赔偿" in evidence_by_id[evidence_id] for evidence_id in damage_ids)
    assert all("责任上限" not in evidence_by_id[evidence_id] for evidence_id in damage_ids)


def test_liability_cap_reference_alone_does_not_cover_confidentiality_damages():
    result = _review("""
    软件委托开发合同
    甲方委托乙方开发管理系统。
    双方对履约中知悉的商业秘密和技术资料承担保密义务。
    乙方累计赔偿责任最高不超过已支付开发费的30%，该上限适用于保密义务和数据泄露责任。
    """)
    item = _by_id(result)["TC-11-04"]
    elements = _elements(item)

    assert elements["confidentiality_obligation"]["status"] == "COVERED"
    assert elements["breach_damage_liability"]["status"] == "MISSING"
    evidence_text = _evidence_text(item)
    assert "承担保密义务" in evidence_text
    assert "责任上限" not in evidence_text
