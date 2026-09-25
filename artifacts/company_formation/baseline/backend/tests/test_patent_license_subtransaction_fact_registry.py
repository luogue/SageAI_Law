from review_v2.engine import review_contract_v2
from review_v2.technology_service_analysis import (
    build_technology_fact_registry,
    classify_technology_transaction,
)
from review_v2.user_profile import UserRiskProfile


PATENT_LICENSE_BASE = """
专利实施许可合同
甲方（被许可方）与乙方（许可方）约定：乙方许可甲方在中国境内实施专利技术。
专利名称：工业检测方法；专利号：ZL202610000001.1；专利权人：乙方；授权日：2026年1月10日。
许可期限五年，甲方不得超出许可地域、用途或者许可方式实施本专利。
"""


def _review(text: str) -> dict:
    return review_contract_v2(
        text,
        "technology",
        include_low_risk=True,
        use_llm=False,
        profile=UserRiskProfile(user_identity="甲方/被许可方"),
    )


def _items(output: dict) -> dict:
    return {row["item_id"]: row for row in output["items"]}


def _element_statuses(item: dict) -> dict:
    return {row["element_id"]: row["status"] for row in item.get("coverage_elements", [])}


def _finding(output: dict, group: str) -> dict:
    return next(row for row in output["risk_findings"] if row["risk_group"] == group)


def test_pure_patent_license_keeps_main_transaction_without_inventing_service_module():
    classification = classify_technology_transaction(PATENT_LICENSE_BASE)

    assert classification["primary_subtype"] == "TECHNOLOGY_LICENSE"
    assert classification["tertiary_subtype"] == "PATENT_LICENSE"
    assert "technical_service" not in classification["sub_transactions"]
    assert "technical_secret" not in classification["sub_transactions"]


def test_patent_license_plus_technical_secret_activates_secret_rule_without_reclassification():
    text = PATENT_LICENSE_BASE + """
第六条 技术秘密
未公开的算法参数、训练方法和测试数据属于技术秘密，仅可用于实施本合同专利。
技术秘密使用费为人民币10万元，保密期限五年。
"""
    classification = classify_technology_transaction(text)
    item = _items(_review(text))["TC-12-03"]

    assert classification["primary_subtype"] == "TECHNOLOGY_LICENSE"
    assert classification["tertiary_subtype"] == "PATENT_LICENSE"
    assert "technical_secret" in classification["sub_transactions"]
    assert item["coverage_status"] != "不适用"
    assert _element_statuses(item)["technical_secret_scope"] == "COVERED"


def test_patent_license_plus_technical_service_activates_tc09_without_changing_main_type():
    text = PATENT_LICENSE_BASE + """
第七条 技术服务和技术指导
乙方提供实施说明、部署指导、参数配置培训和故障排查指导，采用远程会议和现场培训方式。
技术服务和指导费为人民币5万元。
第八条 验收标准
准确率达到95%，连续稳定运行30日；验收不合格的，乙方整改后重新验收。
"""
    classification = classify_technology_transaction(text)
    items = _items(_review(text))

    assert classification["primary_subtype"] == "TECHNOLOGY_LICENSE"
    assert classification["tertiary_subtype"] == "PATENT_LICENSE"
    assert "technical_service" in classification["sub_transactions"]
    assert "TECHNICAL_SERVICE" in classification["secondary_modules"]
    assert items["TC-09-01"]["coverage_status"] != "不适用"
    assert items["TC-09-02"]["coverage_status"] != "不适用"
    assert items["TC-09-01"]["applicable_if"] == "适用于技术服务合同，或其他合同中实际包含独立技术服务义务的场景。"


THIRD_PARTY_PARTIAL = """
第九条 第三方权利责任
乙方保证其为专利权人并有权授予本合同许可。
第三方主张甲方按照本合同实施侵犯其权利时，乙方负责交涉、应诉，并承担合理律师费、诉讼费及甲方直接经济损失。
"""


def test_third_party_claim_partial_uses_concrete_covered_and_missing_elements():
    output = _review(PATENT_LICENSE_BASE + THIRD_PARTY_PARTIAL)
    item = _items(output)["TC-12-02"]
    statuses = _element_statuses(item)

    assert item["coverage_status"] == "部分覆盖"
    assert statuses["claim_handling"] == "COVERED"
    assert statuses["litigation_handling"] == "COVERED"
    assert statuses["attorney_fee"] == "COVERED"
    assert statuses["litigation_cost"] == "COVERED"
    assert statuses["direct_damage"] == "COVERED"
    assert statuses["notification_requirement"] == "MISSING"
    assert statuses["defense_control"] == "MISSING"
    assert statuses["lawyer_selection"] == "MISSING"
    assert statuses["settlement_authority"] == "MISSING"
    assert statuses["replacement_remedy"] == "MISSING"


def test_tc12_rules_share_one_registry_and_do_not_re_report_confirmed_costs():
    output = _review(PATENT_LICENSE_BASE + THIRD_PARTY_PARTIAL)
    items = _items(output)
    expected_registry = build_technology_fact_registry(
        PATENT_LICENSE_BASE + THIRD_PARTY_PARTIAL
    )["third_party_claim"]

    for item_id in ("TC-12-01", "TC-12-02", "TC-12-04"):
        assert items[item_id]["decision_trace"]["fact_registry"]["third_party_claim"] == expected_registry

    liability_statuses = _element_statuses(items["TC-12-04"])
    assert liability_statuses["attorney_fee_allocation"] == "COVERED"
    assert liability_statuses["litigation_cost_allocation"] == "COVERED"
    assert liability_statuses["infringement_damage_items"] == "COVERED"
    liability_narrative = "\n".join(
        str(items["TC-12-04"].get(field, ""))
        for field in ("reasoning_summary", "risk_point_description", "suggested_clause_example")
    )
    assert "未明确律师费" not in liability_narrative
    assert "未明确诉讼费" not in liability_narrative
    assert "未明确直接损失" not in liability_narrative


def test_patent_license_without_software_facts_does_not_request_software_or_open_source_proof():
    output = _review(PATENT_LICENSE_BASE)
    items = _items(output)
    combined = "\n".join(
        str(value)
        for item_id in ("TC-03-04", "TC-13-02")
        for value in (
            items[item_id].get("reasoning_summary", ""),
            items[item_id].get("risk_point_description", ""),
            items[item_id].get("suggested_clause_example", ""),
        )
    )

    assert "软件著作权" not in combined
    assert "开源组件" not in combined
    assert "人员成果归集" not in combined
    assert "专利" in combined


def test_existing_improvement_ownership_and_priority_arrangement_is_partial_not_missing():
    text = PATENT_LICENSE_BASE + """
第十条 改进成果
甲方改进成果归甲方，乙方使用需另行协商；乙方改进成果归乙方，甲方享有优先许可权。
"""
    item = _items(_review(text))["TC-10-02"]
    statuses = _element_statuses(item)

    assert item["coverage_status"] == "部分覆盖"
    assert statuses["licensee_improvement_ownership"] == "COVERED"
    assert statuses["licensor_improvement_ownership"] == "COVERED"
    assert statuses["priority_or_negotiated_license"] == "PARTIALLY_COVERED"
    assert statuses["license_fee"] == "MISSING"
    assert item["suggested_clause_example"] == "建议在现有优先许可和另行协商机制基础上，进一步明确许可费或定价机制、许可地域、期限、商业使用及分许可条件。"


def test_coverage_evidence_is_bound_to_over_scope_and_material_delivery_clauses():
    text = PATENT_LICENSE_BASE + """
第四条 技术资料：乙方应向甲方交付图纸、程序和操作手册。
第二十一条 附件：技术资料交付清单。
第十六条 甲方超出许可范围实施或者擅自再许可的，应停止违约行为并支付违约金。
"""
    items = _items(_review(text))
    over_scope_evidence = "\n".join(row["quote"] for row in items["TC-07-03"]["evidence_clauses"])
    material_locations = "\n".join(row["location"] for row in items["TC-13-01"]["evidence_clauses"])

    assert "超出许可范围" in over_scope_evidence
    assert "违约金" in over_scope_evidence
    assert "第四条" in material_locations
    assert "第二十一条" in material_locations


def test_licence_with_secret_service_guidance_and_acceptance_activates_real_applicability_chain():
    text = PATENT_LICENSE_BASE + """
第六条 技术秘密
技术秘密内容包括模型训练参数、数据标注规范和部署优化参数；实施要求：仅限甲方实施许可专利。
技术秘密使用费为人民币8万元，保密期限五年。
第七条 技术服务和指导
技术服务和指导内容：系统部署、模型训练、生产环境调试及技术人员培训。
技术服务和指导方式：现场指导与远程技术支持相结合。
第八条 验收
技术资料完整交付并经甲方书面确认，识别准确率应达到95%。
第九条 技术服务和指导费为人民币3万元。
"""
    output = _review(text)
    classification = classify_technology_transaction(text)
    items = _items(output)

    assert classification["primary_subtype"] == "TECHNOLOGY_LICENSE"
    assert {"technical_secret", "technical_service", "technical_guidance", "acceptance"} <= set(
        classification["sub_transactions"]
    )
    assert all(items[f"TC-09-0{index}"]["coverage_status"] != "不适用" for index in (1, 2, 4))
    assert items["TC-09-03"]["coverage_status"] == "不适用"
    assert items["TC-09-03"]["decision_trace"]["service_generated_result_applicability"]["improvement_result_reused"] is False
    assert items["TC-12-03"]["coverage_status"] != "不适用"
    assert _element_statuses(items["TC-12-03"])["technical_secret_use_boundary"] == "COVERED"


def test_third_person_claim_wording_flows_from_registry_to_all_tc12_consumers():
    text = PATENT_LICENSE_BASE + """
第十条 第三人侵权责任
乙方负责与第三方交涉、应诉，并承担合理律师费、诉讼费及甲方直接经济损失。
"""
    output = _review(text)
    items = _items(output)

    assert items["TC-12-02"]["coverage_status"] == "部分覆盖"
    assert _element_statuses(items["TC-12-02"])["attorney_fee"] == "COVERED"
    assert _element_statuses(items["TC-12-02"])["litigation_cost"] == "COVERED"
    assert _element_statuses(items["TC-12-04"])["attorney_fee_allocation"] == "COVERED"
    assert _element_statuses(items["TC-12-04"])["litigation_cost_allocation"] == "COVERED"


def test_material_registry_recognizes_method_quantity_confirmation_and_versioned_schedule():
    text = PATENT_LICENSE_BASE + """
第四条 技术资料
技术资料包括系统架构说明、模型训练参数、部署说明、设备接口说明和操作手册。
第五条 提交方式
乙方提供加密电子文件及纸质资料各一套。
第八条 验收
技术资料完整交付并经甲方书面确认。
第二十一条 附件
《技术资料交付清单V2.1》为本合同附件。
"""
    item = _items(_review(text))["TC-13-01"]
    statuses = _element_statuses(item)

    assert statuses["major_document_types"] == "COVERED"
    assert statuses["delivery_method"] == "COVERED"
    assert statuses["delivery_quantity"] == "COVERED"
    assert statuses["receipt_confirmation"] == "COVERED"
    assert statuses["closed_attachment_schedule"] == "COVERED"
    assert statuses["file_version"] == "COVERED"


def test_classification_ontology_is_not_a_required_contract_phrase():
    output = _review(PATENT_LICENSE_BASE)
    item = _items(output)["TC-01-04"]

    assert item["coverage_status"] == "通过"
    assert item["decision_trace"]["review_nature"] == "INTERNAL_CLASSIFICATION"
    assert "无需合同另写声明条款" in item["reasoning_summary"]
    assert output["release_quality_gate"]["status"] == "REPORT_READY"


def test_licensor_equal_to_named_patent_owner_does_not_require_upstream_chain():
    text = """
专利实施许可合同
受让方（甲方）：智能制造有限公司
让与方（乙方）：先进技术研究院
乙方授予甲方在中国境内实施本专利的许可。
专利名称：工业检测技术；专利号：ZL202610000099.9；专利权人：先进技术研究院；授权日：2026年2月1日。
专利有效期至2046年2月1日，专利年费已缴纳。
许可期限五年。
"""
    output = _review(text)
    item = _items(output)["TC-03-04"]
    statuses = _element_statuses(item)
    registry = build_technology_fact_registry(text)["third_party_claim"]

    assert registry["licensor_is_patent_owner"] is True
    assert statuses["licensor_authority_and_upstream_authorization"] == "COVERED"
    assert "无需另行证明上游授权或再许可权限" in "\n".join(
        row["proposition"] for row in item["coverage_elements"]
    )


def test_colon_style_improvement_ownership_is_partial_not_missing():
    text = PATENT_LICENSE_BASE + """
第十四条 改进成果
甲方后续改进成果归属：甲方所有；乙方使用应另行协商许可。
乙方后续改进成果归属：乙方所有；甲方享有同等条件下优先获得许可的权利。
"""
    item = _items(_review(text))["TC-10-02"]
    statuses = _element_statuses(item)

    assert item["coverage_status"] == "部分覆盖"
    assert statuses["licensee_improvement_ownership"] == "COVERED"
    assert statuses["licensor_improvement_ownership"] == "COVERED"


def test_service_generated_result_is_distinct_from_follow_on_technical_improvement():
    improvement_only = PATENT_LICENSE_BASE + """
第七条 技术服务
乙方提供安装调试和技术指导。
第十四条 后续改进成果
甲方对许可专利形成的后续改进成果归甲方，乙方使用应另行协商许可。
"""
    assert _items(_review(improvement_only))["TC-09-03"]["coverage_status"] == "不适用"

    service_result = PATENT_LICENSE_BASE + """
第七条 技术服务
技术服务和指导内容：乙方提供部署支持和技术人员培训；技术服务过程中形成的调试报告和实施方案归甲方所有，乙方仅可为履行本合同使用。
"""
    item = _items(_review(service_result))["TC-09-03"]
    assert item["coverage_status"] != "不适用"
    assert _element_statuses(item)["service_generated_result_ownership"] == "COVERED"


def test_tc12_final_absence_audit_respects_registry_and_rule_ownership():
    output = _review(PATENT_LICENSE_BASE + THIRD_PARTY_PARTIAL)
    infringement = _finding(output, "license_infringement_responsibility")
    claim = _finding(output, "third_party_claim_defense")
    indemnity = _finding(output, "indemnity_and_liability_cap")
    cluster_ids = {
        row["aggregation_signals"]["user_visible_risk_cluster"]["cluster_id"]
        for row in (infringement, claim, indemnity)
    }
    claim_missing = "\n".join(row["proposition"] for row in claim["final_missing_elements"])
    indemnity_missing = "\n".join(row["proposition"] for row in indemnity["final_missing_elements"])

    assert cluster_ids == {"third_party_ip_claim_and_remedy"}
    assert "第三方知识产权主张与侵权救济机制" in output["result"]
    assert "通知" in claim_missing and "抗辩控制" in claim_missing and "和解决策" in claim_missing
    assert "未明确律师费" not in indemnity_missing
    assert "未明确诉讼费" not in indemnity_missing
    assert "第三方侵权赔偿项目" not in indemnity_missing


def test_tc1201_combined_licensor_and_out_of_scope_liability_closes_boundary():
    text = PATENT_LICENSE_BASE + THIRD_PARTY_PARTIAL + """
第十六条 超范围实施责任
甲方超出许可范围实施、擅自修改许可技术或未经乙方同意擅自再许可的，应立即停止并自行承担相应责任。
"""
    output = _review(text)
    item = _items(output)["TC-12-01"]

    assert item["coverage_status"] == "通过"
    assert _element_statuses(item)["compliant_use_scope_boundary"] == "COVERED"
    assert item["decision_trace"]["responsibility_boundary_assessment"]["boundary_closed_by_combined_clauses"] is True
    assert not any(row["risk_group"] == "license_infringement_responsibility" for row in output["risk_findings"])


def test_named_owner_with_only_independent_patent_proof_missing_is_low_optional():
    text = PATENT_LICENSE_BASE + """
专利有效期限至2046年1月10日，年费已按期缴纳。
乙方确认不存在共有权人、既有许可、独占或排他许可冲突、质押、查封及其他权利负担。
"""
    finding = _finding(_review(text), "technology_ip_rights_provenance")

    assert finding["missing_element_ids"] == ["patent_certificate_or_register_attachment"]
    assert finding["severity"] == "LOW"
    assert finding["priority"] == "C_OPTIMIZATION"


def test_material_recommendation_only_mentions_identifier_when_it_is_the_only_gap():
    text = PATENT_LICENSE_BASE + """
第四条 技术资料
技术资料包括总体设计图、机械零件图、电气原理图、PLC源程序及安装调试手册。
第五条 交付方式
乙方应以加密电子文件及纸质资料各一套交付甲方。
第八条 验收
技术资料完整交付后由甲方书面确认。
第二十一条 附件
附件一《技术资料交付清单V1.0》列明上述最终交付文件。
"""
    item = _items(_review(text))["TC-13-01"]

    assert _element_statuses(item)["file_identifier"] == "MISSING"
    assert "文件编号" in item["suggested_clause_example"]
    assert "文件名称" not in item["suggested_clause_example"]
    assert "版本号" not in item["suggested_clause_example"]


def test_internal_element_keys_never_reach_rendered_report():
    output = _review(PATENT_LICENSE_BASE + THIRD_PARTY_PARTIAL)
    for internal_key in (
        "compliant_use_scope_boundary", "claim_handling", "attorney_fee",
        "license_cure", "replacement_remedy",
    ):
        assert internal_key not in output["result"]


def test_named_patent_owner_recommendation_only_requests_independent_title_proof():
    output = _review(PATENT_LICENSE_BASE + THIRD_PARTY_PARTIAL)
    finding = _finding(output, "technology_ip_rights_provenance")

    assert "专利证书" in finding["recommendation"]
    assert "专利登记簿副本" in finding["recommendation"]
    assert "上游授权" not in finding["recommendation"]
    assert "再许可权限" not in finding["recommendation"]


def test_actionable_secret_and_acceptance_recommendations_use_natural_contract_language():
    text = PATENT_LICENSE_BASE + """
第六条 技术秘密
技术秘密内容包括模型训练参数、数据标注规范和部署优化参数；实施要求：仅限甲方实施本合同许可专利使用；技术秘密使用费5万元，保密期限五年。
第七条 技术服务
技术服务和指导内容：乙方提供系统部署、模型训练和技术人员培训。
第八条 验收
准确率应达到95%。
"""
    output = _review(text)
    items = _items(output)

    assert "因非被许可方原因公开或丧失秘密性" in items["TC-12-03"]["suggested_clause_example"]
    assert "不影响其违约和赔偿责任" in items["TC-12-03"]["suggested_clause_example"]
    acceptance = items["TC-09-02"]["suggested_clause_example"]
    assert "整改期限" in acceptance and "再次验收程序" in acceptance
    assert "明确。" not in acceptance


def test_material_finding_binds_types_delivery_receipt_and_attachment_clauses():
    text = PATENT_LICENSE_BASE + """
第四条 技术资料
专利说明书、算法原理、系统架构说明、部署说明和操作手册。
第五条 提交方式
乙方提交加密电子文件及纸质资料各一套。
第八条 验收
技术资料完整交付并经甲方书面确认。
第二十一条 附件
《技术资料交付清单V1.0》为本合同附件。
"""
    finding = _finding(_review(text), "technical_material_attachment")
    heading_paths = {
        heading
        for row in finding["evidence_bundle"]["items"]
        for heading in row.get("heading_path", [])
    }

    assert all(any(heading.startswith(article) for heading in heading_paths) for article in (
        "第四条", "第五条", "第八条", "第二十一条",
    ))


def test_user_report_distinguishes_cluster_topics_from_underlying_findings():
    output = _review(PATENT_LICENSE_BASE + THIRD_PARTY_PARTIAL)
    report = output["result"]
    raw_count = len(output["risk_findings"])
    clustered_count = raw_count - 2

    assert f"- 风险主题数（聚合后）：{clustered_count}" in report
    assert f"- 底层审查发现数：{raw_count}" in report
    assert f"本报告共{clustered_count}个风险主题，对应{raw_count}个底层审查发现" in report
    assert "完整风险明细（底层审查发现）" in report


def test_tc1203_consistently_reviews_loss_of_secrecy_not_contract_invalidity():
    text = PATENT_LICENSE_BASE + """
第六条 技术秘密
本合同同时包含技术秘密许可。未公开的工艺参数和测试方法属于技术秘密，仅限实施许可专利使用，技术秘密使用费为5万元。
技术秘密进入公共领域后，双方另行协商继续使用和费用处理。
"""
    output = _review(text)
    item = _items(output)["TC-12-03"]
    combined = "\n".join((
        item["title"], item["applicable_if"], item["risk_point_description"],
        item["suggested_clause_example"], output["result"],
    ))

    assert item["title"] == "技术秘密丧失秘密性后的使用与费用处理"
    assert "公开或丧失秘密性" in combined
    assert "使用费" in combined
    assert "合同无效" not in combined
    assert "许可被确认无效" not in combined


def test_final_report_has_no_positive_fact_recommendation_conflict():
    text = PATENT_LICENSE_BASE + """
第十四条 改进成果
甲方改进成果归甲方，乙方使用需另行协商；乙方改进成果归乙方，甲方享有优先许可权。
"""
    report = _review(text)["result"]

    assert "建议补充明确优先许可" not in report
    assert "建议补充明确优先许可、另行协商或不当然无偿许可的原则安排已经存在" not in report
    assert "建议明确已经明确" not in report
