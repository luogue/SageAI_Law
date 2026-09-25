from review_v2.engine import COVERAGE_NOT_APPLICABLE, review_contract_v2
from review_v2.user_profile import UserRiskProfile


CONTRACT = """
技术服务合同
委托人：甲方
受托人：乙方
签订日期：2026年9月2日
有效期限：2026年9月5日至2027年3月4日
一、服务内容、方式和要求
乙方利用专业技术知识为甲方工业生产设备提供预测性维护技术服务，包括设备数据分析与建模、故障诊断、状态监测系统部署、模型训练、参数调试、技术优化和远程技术支持，并对甲方人员提供系统使用培训。
乙方应提交部署程序、预测模型、操作手册、项目实施报告和培训材料。
项目实施过程中形成的新模型、新算法、新程序及其他技术成果均由乙方所有。甲方仅享有在本项目生产场地内部永久使用的权利。
二、履行期限
乙方应于2027年3月15日前提交最终项目实施报告。
最终验收应于2027年3月31日前完成。
三、验收标准和方式
设备故障预警准确率应达到90%以上。
乙方完成系统部署后，应向甲方提交验收申请。
甲方应在收到验收申请后5个工作日内完成验收。甲方未在该期限内提出书面异议的，视为项目验收合格。
如验收未通过，乙方应在10个工作日内整改后重新提交验收。
四、报酬及其支付方式
本项目技术服务报酬总额为人民币1,000,000元。
合同签订后5个工作日内，甲方向乙方支付合同总金额的30%，即人民币300,000元；
系统部署完成后5个工作日内，甲方向乙方支付合同总金额的40%，即人民币400,000元；
项目验收合格后5个工作日内，甲方向乙方支付人民币350,000元。
上述款项合计人民币1,050,000元。
五、违约责任
因乙方原因迟延完成系统部署的，每迟延一日，按照合同总金额的1%向甲方支付违约金。
乙方承担的全部赔偿责任以甲方已经实际支付给乙方的技术服务费总额的20%为最高限额。
前述责任上限适用于人身损害责任以及因乙方故意或者重大过失造成的损失。
六、保密与数据处理
双方对履行本合同过程中获得的对方技术资料、经营数据、设备参数及其他未公开信息承担保密义务。
乙方可以将甲方生产设备运行数据用于乙方其他客户项目。
合同终止后，乙方可以继续保存甲方设备数据及项目数据，用于技术研究和产品改进。
本合同终止后，双方保密义务同时终止。
七、第三方软件及知识产权
乙方可以根据项目需要使用第三方开源软件、算法库或者其他第三方技术，且无需披露具体清单。
因第三方软件、开源软件或者其他第三方技术产生的知识产权纠纷，由甲方自行承担责任。
八、服务中新成果
甲方技术人员根据乙方技术方案提出改进意见并参与形成的成果，也由乙方所有。乙方有权将上述成果提供给其他客户使用。
九、争议解决
协商不成的，双方同意提交上海仲裁委员会仲裁。
同时，任何一方也可以向甲方住所地人民法院提起诉讼。
"""


def _review() -> dict:
    return review_contract_v2(
        CONTRACT,
        "service",
        use_llm=False,
        profile=UserRiskProfile(user_identity="甲方", contract_scenario="技术服务"),
    )


def test_b2b_industrial_service_uses_technical_service_route_and_roles():
    result = _review()
    assert result["domain_selection_resolution"]["selected_domain"] == "TECHNOLOGY"
    assert result["contract_context"]["contract_subtype"] == "TECHNICAL_SERVICE"
    assert result["perspective_resolution"]["display_role"] == "甲方 / 服务接受方"
    assert not [
        item["item_id"] for item in result["items"]
        if item["item_id"].startswith("SVC-") and item["coverage_status"] != "不适用"
    ]


def test_industrial_service_core_risks_survive_route_resolution():
    result = _review()
    groups = {finding["risk_group"] for finding in result["risk_findings"]}
    assert {
        "payment_formula_inconsistency",
        "technical_timeline_conflict",
        "generic_liability_cap_validity",
        "generic_potential_excessive_liquidated_damages",
        "confidentiality_duration_data_use_asymmetry",
        "service_new_result_ownership",
        "third_party_claim_defense",
        "dispute_resolution_choice_conflict",
        "technical_service_quality_acceptance",
    } <= groups
    acceptance = next(
        finding for finding in result["risk_findings"]
        if finding["risk_group"] == "technical_service_quality_acceptance"
    )
    assert acceptance["needs_manual_review"] is False
    assert "隐蔽缺陷" in acceptance["recommendation"]
    assert "补充明确逾期未提出书面异议即视为验收合格" not in acceptance["recommendation"]


def test_payment_and_timeline_are_bound_to_current_contract_facts():
    result = _review()
    payment = result["deterministic_analysis"]["payment_formula"]
    assert payment["contract_total"] == 1000000
    assert payment["amount_total"] == 1050000
    assert payment["amount_delta"] == 50000

    timeline = result["deterministic_analysis"]["timeline"]
    # The header states contractual validity, not an express service deadline.
    assert timeline["validity_end_date"] == "2027-03-04"
    assert timeline["service_end_date"] is None
    assert any(row["date"] == "2027-03-31" for row in timeline["milestone_facts"])
    assert not any(row.get("performance_end_date") == "2027-03-04" for row in timeline["conflicts"])


def test_third_party_component_fact_is_shared_by_claim_and_proof_reviews():
    result = _review()
    items = {row["item_id"]: row for row in result["items"]}
    for review_id in ("TC-03-04", "TC-13-02"):
        item = items[review_id]
        assert item["applicability"]["applicable"] is True
        assert item["coverage_status"] == "部分覆盖"
        assert "未出现第三方软件" not in item["applicability"]["reason"]
        trace = item["decision_trace"]["shared_third_party_component_fact"]
        assert trace["status"] == "CONFIRMED"
        assert trace["fact_key"] == "third_party_component_dependency"
        assert set(trace["consumers"]) == {"TC-03-04", "TC-12-02", "TC-13-02"}
        statuses = {row["element_id"]: row["status"] for row in item["coverage_elements"]}
        assert statuses["third_party_component_dependency"] == "COVERED"
        assert statuses["third_party_component_inventory"] == "MISSING"
        assert statuses["third_party_license_and_authorization"] == "MISSING"
    claim_text = " ".join(
        row.get("text") or "" for row in items["TC-12-02"]["evidence_clauses"]
    )
    assert "第三方开源软件" in claim_text


def test_service_current_project_outputs_do_not_activate_follow_on_improvement_rules():
    result = _review()
    items = {row["item_id"]: row for row in result["items"]}
    for review_id in ("TC-10-01", "TC-10-02", "TC-10-03"):
        assert items[review_id]["coverage_status"] == COVERAGE_NOT_APPLICABLE
        assert items[review_id]["applicability"]["applicable"] is False
    assert "在现有优先许可和另行协商机制基础上" not in result["result"]

    current_project_improvement = review_contract_v2(
        CONTRACT + "\n项目实施过程中形成的模型优化成果、算法改进成果及软件功能改进均归乙方所有。",
        "service",
        use_llm=False,
        profile=UserRiskProfile(user_identity="甲方", contract_scenario="技术服务"),
    )
    current_items = {row["item_id"]: row for row in current_project_improvement["items"]}
    assert all(
        current_items[review_id]["coverage_status"] == COVERAGE_NOT_APPLICABLE
        for review_id in ("TC-10-01", "TC-10-02", "TC-10-03")
    )


def test_explicit_service_follow_on_improvement_still_activates_tc10():
    result = review_contract_v2(
        CONTRACT + "\n服务完成后，乙方进一步开发形成的后续改进成果应优先许可甲方使用，具体条件由双方另行协商。",
        "service",
        use_llm=False,
        profile=UserRiskProfile(user_identity="甲方", contract_scenario="技术服务"),
    )
    items = {row["item_id"]: row for row in result["items"]}
    for review_id in ("TC-10-01", "TC-10-02", "TC-10-03"):
        assert items[review_id]["applicability"]["applicable"] is True
        assert items[review_id]["coverage_status"] != COVERAGE_NOT_APPLICABLE


def test_improvement_recommendation_does_not_invent_existing_mechanisms():
    result = review_contract_v2(
        CONTRACT + "\n服务完成后形成的后续改进成果归乙方所有，但未约定向甲方分享或许可的条件。",
        "service",
        use_llm=False,
        profile=UserRiskProfile(user_identity="甲方", contract_scenario="技术服务"),
    )
    sharing = next(row for row in result["items"] if row["item_id"] == "TC-10-02")
    assert sharing["applicability"]["applicable"] is True
    finding = next(
        row for row in result["risk_findings"]
        if row["risk_group"] == "improvement_sharing_license"
    )
    assert "在现有优先许可和另行协商机制基础上" not in finding["recommendation"]
    assert "建议明确改进成果的分享或许可机制" in finding["recommendation"]


def test_complete_review_rows_are_unique_and_partial_rows_have_real_gaps():
    result = _review()
    item_ids = [row["item_id"] for row in result["items"]]
    assert len(item_ids) == len(set(item_ids))
    assert item_ids.count("TECH-SHARED-03") == 1

    items = {row["item_id"]: row for row in result["items"]}
    assert items["TC-01-03"]["coverage_status"] == "通过"
    assert not any("TC-01-03" in row["source_review_ids"] for row in result["risk_findings"])
    for item in result["items"]:
        if item["coverage_status"] != "部分覆盖":
            continue
        concrete_gaps = [
            element for element in item.get("coverage_elements") or []
            if element.get("status") in {"MISSING", "PARTIALLY_COVERED", "UNCERTAIN"}
            and not element.get("internal_meta")
            and element.get("user_visible") is not False
        ]
        assert concrete_gaps, item["item_id"]
