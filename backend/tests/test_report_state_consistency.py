"""Atomic positive/absence, applicability and residual projection invariants."""
from copy import deepcopy

import pytest

from review_v2.report_state_consistency import report_state_consistency_failures


def element(key="application_ownership", status="COVERED", **extra):
    return {"element_id": key, "status": status, "required_fact": key,
            "supporting_evidence": [{"clause_id": "c1", "quote": "甲方享有申请专利的权利。"}]
                if status in {"COVERED", "PARTIALLY_COVERED"} else [], **extra}


def review(elements=()):
    return {"item_id": "TEST", "coverage_status": "部分覆盖", "coverage_elements": list(elements),
            "applicability": {"status": "APPLICABLE"}, "narrative_state": {}, "decision_trace": {},
            "evidence_clauses": []}


def finding(elements=()):
    return {"finding_id": "test", "source_review_ids": ["TEST"], "final_missing_elements": list(elements),
            "final_adverse_elements": [], "aggregation_signals": {"recommendation_element_policy": "FINAL_UNRESOLVED_ELEMENTS",
                "unresolved_requirements": list(elements)},
            "evidence_bundle": {"unresolved_requirements": list(elements)}}


@pytest.mark.parametrize("location", ["trace", "review", "bundle", "bundle_alias"])
def test_exact_positive_and_same_requirement_absence_cannot_coexist(location):
    item, risk = review([element()]), finding()
    audit = {"source_type": "SEARCH_AUDIT", "result": "NOT_FOUND",
             "element_id": "APPLICATION_OWNERSHIP", "searched_absent_element_ids": ["applicationOwnership"]}
    if location == "trace":
        item["decision_trace"]["element_absence_searches"] = [audit]
    elif location == "review":
        item["evidence_clauses"] = [audit]
    else:
        risk["evidence_bundle"]["items" if location == "bundle" else "evidence_items"] = [audit]
    assert "POSITIVE_REQUIREMENT_WITH_ABSENCE_SEARCH" in {
        row["reason"] for row in report_state_consistency_failures([item], [risk])}


def test_partial_source_and_search_for_its_residual_is_not_full_coverage_conflict():
    gap = element("filing_cooperation", "PARTIALLY_COVERED", residual_gap="申请文件签署方式")
    item, risk = review([gap]), finding([gap])
    item["decision_trace"]["element_absence_searches"] = [
        {"element_id": gap["element_id"], "result": "NOT_FOUND", "search_targets": ["申请文件签署方式"]}]
    assert report_state_consistency_failures([item], [risk]) == []


@pytest.mark.parametrize("applicability", [{"status": "not_applicable"}, {"applicable": False}, {"status": "N/A"}])
def test_false_applicability_blocks_a_covered_or_partial_verdict(applicability):
    item = review()
    item["applicability"] = applicability
    assert report_state_consistency_failures([item])[0]["reason"] == "NOT_APPLICABLE_NARRATIVE_STATE_CONFLICT"
    item["coverage_status"] = "不适用"
    assert report_state_consistency_failures([item]) == []


@pytest.mark.parametrize("text", ["本项不适用。", "不适用：本合同不含相关安排。", "审查判断：本规则不适用。"])
def test_not_applicable_assertion_cannot_hide_in_partial_narrative(text):
    item = review()
    item["narrative_state"]["judgment"] = text
    assert report_state_consistency_failures([item])


@pytest.mark.parametrize("text", ["本项并非不适用，仍需审查。", "如无独立服务义务，本项不适用。", "其他规则不适用。"])
def test_conditional_and_negated_na_mentions_are_not_na_verdicts(text):
    item = review()
    item["narrative_state"]["judgment"] = text
    assert report_state_consistency_failures([item]) == []


@pytest.mark.parametrize("projection", ["aggregate", "evidence", "summary", "detail", "formal_recommendation"])
def test_partial_residuals_cannot_be_dropped_by_any_report_projection(projection):
    incomplete, absent = element("file_version", "PARTIALLY_COVERED"), element("file_count", "MISSING")
    item, risk = review([incomplete, absent]), finding([incomplete, absent])
    if projection == "aggregate":
        risk["final_missing_elements"] = [absent]
    elif projection == "evidence":
        risk["evidence_bundle"]["unresolved_requirements"] = [absent]
    else:
        risk["aggregation_signals"]["unresolved_projection_element_ids"] = {projection: [absent["element_id"]]}
    errors = report_state_consistency_failures([item], [risk])
    assert any(row["reason"] == "REPORT_UNRESOLVED_REQUIREMENTS_MISMATCH" and row["projection"] == projection for row in errors)


def test_conditional_unknown_and_adverse_are_not_ordinary_missing_requirements():
    unknown = element("upstream", "CONDITION_UNRESOLVED", conditional_element=True, prerequisite_status="UNKNOWN")
    adverse, missing = element("adverse_term", "ADVERSE"), element("filing_fee", "MISSING")
    item, risk = review([unknown, adverse, missing]), finding([missing])
    risk["final_adverse_elements"] = [adverse]
    risk["aggregation_signals"]["recommendation_element_ids"] = ["adverse_term", "filing_fee"]
    assert report_state_consistency_failures([item], [risk]) == []
    risk["aggregation_signals"]["recommendation_element_ids"].append("upstream")
    assert any(row["reason"] == "RECOMMENDATION_REQUIREMENTS_MISMATCH" for row in report_state_consistency_failures([item], [risk]))


def test_validator_is_read_only_and_identical_alias_errors_are_deduplicated():
    item, risk = review([element()]), finding()
    audit = {"source_type": "SEARCH_AUDIT", "result": "NOT_FOUND", "element_id": "application_ownership"}
    risk["evidence_bundle"].update(items=[audit], evidence_items=[deepcopy(audit)])
    before = deepcopy([item, risk])
    errors = report_state_consistency_failures([item], [risk])
    assert len([row for row in errors if row["reason"] == "POSITIVE_REQUIREMENT_WITH_ABSENCE_SEARCH"]) == 1
    assert [item, risk] == before


def test_remedy_entailment_validator_only_consumes_its_own_requirement_domain():
    from review_v2.confidentiality_remedies import confidentiality_binding_failures

    scope = element("confidential_information_scope", party_coverage=[{
        "obligated_party": "甲方", "status": "COVERED", "required_fact": "甲方保密信息类别",
        "supporting_evidence": [{"clause_id": "c1", "quote": "甲方保密范围包括生产数据。", "obligated_party": "甲方"}],
    }])
    assert confidentiality_binding_failures([scope]) == []
    invented_remedy = deepcopy(scope)
    invented_remedy["element_id"] = "STOP_DISCLOSURE"
    failures = confidentiality_binding_failures([invented_remedy])
    assert any(row["reason"] == "REMEDY_OR_PARTY_NOT_ENTAILED" for row in failures)


@pytest.mark.parametrize("facts", [[], [{"quote": "乙方停止披露。", "obligated_party": "乙方"}],
                                      [{"quote": "未找到", "obligated_party": "甲方", "source_type": "SEARCH_AUDIT"}]])
def test_every_party_covered_requirement_needs_its_own_direct_source(facts):
    row = element("confidential_information_scope", party_coverage=[{
        "obligated_party": "甲方", "status": "COVERED", "supporting_evidence": facts,
    }])
    assert any(error["reason"] == "COVERED_PARTY_WITHOUT_EXACT_SOURCE"
               for error in report_state_consistency_failures([review([row])]))


def test_atomic_consequence_cannot_fall_back_to_an_unrelated_composite_gap():
    gap = element("fee_settlement", "MISSING", required_fact="已发生研发费用结算")
    item = review([element(), gap])
    item["decision_trace"] = {"atomic_requirement_family": "development_failure",
                              "consequence_element_ids": ["fee_settlement"]}
    item["narrative_state"]["consequence"] = "已发生研发费用结算未明确，可能引发结算争议。"
    item["narrative_state"]["judgment"] = item["risk_point_description"] = "尚未覆盖：已发生研发费用结算。"
    item["legal_consequence_if_missing"] = item["narrative_state"]["consequence"]
    assert not report_state_consistency_failures([item])
    item["narrative_state"]["consequence"] = "无过错技术风险分担尚未明确。"
    assert any(row["reason"] == "CONSEQUENCE_REQUIREMENTS_MISMATCH"
               for row in report_state_consistency_failures([item]))


def scoped_reviews():
    identity = {"canonical_fact_key": "data_disposal", "scope": "termination", "party": "甲方", "object": "source_code"}
    first = review([element("return_source", fact_identity=identity)])
    first["item_id"] = "RULE-A"
    second = review([element("different_consumer_key", "MISSING", fact_identity={**identity, "canonical_fact_key": "DATA_DISPOSAL"})])
    second["item_id"] = "RULE-B"
    return first, second


def test_shared_atomic_fact_cannot_be_covered_and_missing_across_rules():
    first, second = scoped_reviews()
    errors = report_state_consistency_failures([first, second])
    assert errors == [{"reason": "CROSS_RULE_SCOPED_FACT_STATUS_CONFLICT", "canonical_fact_key": "data_disposal",
                       "scope": "termination", "party": "甲方", "object": "source_code",
                       "covered_reviews": ["RULE-A"], "missing_reviews": ["RULE-B"]}]


@pytest.mark.parametrize("dimension,value", [("scope", "normal_delivery"), ("party", "乙方"),
                                            ("object", "product_sample"), ("canonical_fact_key", "data_use")])
def test_different_actors_objects_events_and_facts_do_not_conflict(dimension, value):
    first, second = scoped_reviews()
    second["coverage_elements"][0]["fact_identity"][dimension] = value
    assert report_state_consistency_failures([first, second]) == []


@pytest.mark.parametrize("dimension", ["scope", "party", "object"])
def test_missing_identity_dimension_is_not_a_cross_rule_wildcard(dimension):
    first, second = scoped_reviews()
    second["coverage_elements"][0]["fact_identity"].pop(dimension)
    assert report_state_consistency_failures([first, second]) == []


def test_principle_level_partial_source_does_not_prove_full_shared_coverage():
    first, second = scoped_reviews()
    first["coverage_elements"][0]["status"] = "PARTIALLY_COVERED"
    assert report_state_consistency_failures([first, second]) == []


@pytest.mark.parametrize("field,value", [("needs_manual_review", True), ("status", "HUMAN_REVIEW"),
    ("recommended_action", "manual_review"), ("issue_type", "人工复核"), ("review_priority", "MANUAL_REVIEW")])
def test_pass_cannot_coexist_with_pending_manual_review(field, value):
    item = review([element()])
    item["coverage_status"] = "PASS"
    item[field] = value
    assert any(row["reason"] == "PASS_WITH_PENDING_MANUAL_REVIEW" for row in report_state_consistency_failures([item]))
    item["coverage_status"] = "INSUFFICIENT_CONTEXT"
    assert not any(row["reason"] == "PASS_WITH_PENDING_MANUAL_REVIEW" for row in report_state_consistency_failures([item]))


def secret_item(reason):
    item = review()
    item["coverage_status"] = "不适用"
    item["applicability"] = {"status": "NOT_APPLICABLE", "reason": reason}
    item["decision_trace"] = {
        "secret_material_applicability": {"status": "CONFIRMED", "source_clause_ids": ["SECRET-1"]},
        "confidentiality_applicability": {"status": "CONFIRMED", "technical_secret_positive_fact": True,
                                          "technical_secret_clause_ids": ["SECRET-1"]},
    }
    return item


@pytest.mark.parametrize("reason", ["本项不适用，合同不涉及技术秘密。", "未确认存在保密资料，不进入资料处置审查。",
                                     "未明确保密范围，本项不适用。"])
def test_na_reason_cannot_deny_confirmed_secret_facts(reason):
    assert any(row["reason"] == "NA_REASON_DENIES_CONFIRMED_PREREQUISITE"
               for row in report_state_consistency_failures([secret_item(reason)]))


@pytest.mark.parametrize("reason", ["合同未形成技术秘密成果，成果权属规则不适用。", "若不涉及技术秘密，本项不适用。",
                                     "资料返还条款不涉及质押担保，本项不适用。", "本项不适用；不代表不存在保密资料。"])
def test_confirmed_secret_material_does_not_force_unrelated_rule_applicability(reason):
    assert report_state_consistency_failures([secret_item(reason)]) == []


def test_unknown_secret_context_and_commercial_confidentiality_do_not_prove_technical_secret():
    item = secret_item("未确认存在技术秘密，本项不适用。")
    item["decision_trace"]["confidentiality_applicability"].update(technical_secret_positive_fact=False,
        confidentiality_scope_positive_fact=True, confidentiality_scope_clause_ids=["COMMERCIAL-1"])
    assert report_state_consistency_failures([item]) == []
    item["applicability"]["reason"] = "未确认存在保密资料，本项不适用。"
    item["decision_trace"] = {"secret_material_applicability": {"status": "NEEDS_FACT_VERIFICATION"}}
    assert report_state_consistency_failures([item]) == []


@pytest.mark.parametrize("alias", ["machine_reason", "user_reason"])
def test_correct_na_display_reason_cannot_hide_stale_reason_alias(alias):
    item = secret_item("合同已有技术秘密范围；本项针对独立技术秘密许可价款，目前不适用。")
    item["applicability"][alias] = "当前合同未形成可识别的技术秘密范围、限制使用或独立对价事实，本项不适用。"
    failures = report_state_consistency_failures([item])
    conflict = next(row for row in failures if row["reason"] == "NA_REASON_DENIES_CONFIRMED_PREREQUISITE")
    assert conflict["reason_fields"] == ["applicability." + alias]
    assert conflict["source_clause_ids"] == ["SECRET-1"]


@pytest.mark.parametrize("alias", ["reason", "machine_reason", "user_reason"])
def test_reason_alias_may_exclude_independent_secret_license_without_denying_secret_material(alias):
    item = secret_item("本项不适用。")
    item["applicability"][alias] = "合同未形成技术秘密许可交易，但保密技术资料已经明确。"
    assert report_state_consistency_failures([item]) == []


@pytest.mark.parametrize("alias", ["reason", "machine_reason", "user_reason"])
def test_proving_rule_secret_trace_is_shared_with_na_rule_without_a_local_copy(alias):
    proving = secret_item("本项適用。")
    proving.update(item_id="SOURCE-RULE", coverage_status="部分覆盖", applicability={"status": "APPLICABLE"})
    dependent = review()
    dependent.update(item_id="DEPENDENT-RULE", coverage_status="不适用", applicability={
        "status": "NOT_APPLICABLE", "reason": "本项不适用，未形成独立技术秘密许可交易。",
        alias: "当前合同未形成可识别的技术秘密范围、限制使用或独立对价事实，本项不适用。",
    })
    assert dependent["decision_trace"] == {}
    failures = report_state_consistency_failures([proving, dependent])
    conflict = next(row for row in failures if row["reason"] == "NA_REASON_DENIES_CONFIRMED_PREREQUISITE")
    assert conflict["review_id"] == "DEPENDENT-RULE"
    assert conflict["source_review_ids"] == ["SOURCE-RULE"]
    assert conflict["source_clause_ids"] == ["SECRET-1"]
    assert conflict["reason_fields"] == ["applicability." + alias]


def test_duplicate_proving_traces_deduplicate_shared_evidence_and_retain_source_rules():
    first = secret_item("本项适用。")
    first.update(item_id="SOURCE-A", coverage_status="部分覆盖", applicability={"status": "APPLICABLE"})
    second = deepcopy(first)
    second["item_id"] = "SOURCE-B"
    dependent = secret_item("未确认存在技术秘密，本项不适用。")
    dependent.update(item_id="TARGET", decision_trace={})
    errors = report_state_consistency_failures([first, second, dependent])
    conflict = next(row for row in errors if row["reason"] == "NA_REASON_DENIES_CONFIRMED_PREREQUISITE")
    assert conflict["source_clause_ids"] == ["SECRET-1"]
    assert conflict["source_review_ids"] == ["SOURCE-A", "SOURCE-B"]


def test_shared_prerequisite_is_not_inferred_from_unvalidated_keywords():
    proving = review([element("ordinary_material", supporting_evidence=[{
        "clause_id": "DOC-1", "quote": "专利资料和算法说明，技术秘密另行确认。",
    }])])
    proving["item_id"] = "SOURCE"
    dependent = secret_item("未确认存在技术秘密，本项不适用。")
    dependent.update(item_id="TARGET", decision_trace={})
    assert report_state_consistency_failures([proving, dependent]) == []


def test_development_result_checklist_description_includes_both_existing_development_branches():
    from review_v2.technology_contract_checklist import TECHNOLOGY_REVIEW_CHECKLIST
    checkpoint = next(row for row in TECHNOLOGY_REVIEW_CHECKLIST if row.node_id == "technical_secret_result_rights")
    assert "委托开发" in checkpoint.applicable_if
    assert "合作开发" in checkpoint.applicable_if
    for subtype in ("ENTRUSTED_DEVELOPMENT", "COOPERATIVE_DEVELOPMENT"):
        item = review()
        item["applicable_if"] = checkpoint.applicable_if
        assert report_state_consistency_failures([item], transaction_context={"primary_subtype": subtype}) == []


@pytest.mark.parametrize("description,active", [
    ("适用于合作开发中需要审查成果使用转让的场景。", "ENTRUSTED_DEVELOPMENT"),
    ("仅适用于技术转让合同。", "TECHNOLOGY_LICENSE"),
    ("适用于技术咨询合同。", "TECHNICAL_SERVICE"),
])
def test_applicable_rule_description_cannot_exclude_its_actual_active_scene(description, active):
    item = review()
    item["applicable_if"] = description
    errors = report_state_consistency_failures([item], transaction_context={"primary_subtype": active})
    assert any(row["reason"] == "APPLICABILITY_DESCRIPTION_EXCLUDES_ACTIVE_TRANSACTION" for row in errors)


def test_description_check_consumes_existing_shared_classification_trace():
    classified = review()
    classified.update(item_id="CLASSIFIER", decision_trace={"classification_context": {"primary_subtype": "ENTRUSTED_DEVELOPMENT"}})
    reviewed = review()
    reviewed["applicable_if"] = "适用于合作开发中需要审查成果使用转让的场景。"
    assert any(row["reason"] == "APPLICABILITY_DESCRIPTION_EXCLUDES_ACTIVE_TRANSACTION"
               for row in report_state_consistency_failures([classified, reviewed]))


def test_conditional_atomic_review_consumes_production_legal_router_scene_trace():
    item = review()
    item["applicability"] = {"status": "CONDITIONALLY_APPLICABLE", "applicable": True}
    item["decision_trace"]["legal_basis_applicability"] = {
        "status": "PASSTHROUGH", "primary_subtype": "ENTRUSTED_DEVELOPMENT",
        "activated_modules": ["TECHNICAL_SERVICE"],
        "active_scenes": ["ENTRUSTED_DEVELOPMENT", "TECHNICAL_SERVICE"],
    }
    item["applicable_if"] = (
        "适用于合作开发中需要审查最终成果归属、背景技术和既有知识产权保留、"
        "独立成果与项目依赖型成果承接，以及许可、转让和商业复用边界的情形。"
    )
    assert "classification_context" not in item["decision_trace"]
    failures = report_state_consistency_failures([item])
    assert failures == [{"review_id": "TEST", "reason": "APPLICABILITY_DESCRIPTION_EXCLUDES_ACTIVE_TRANSACTION",
                         "declared_transaction_types": ["COOPERATIVE_DEVELOPMENT"],
                         "active_transaction_types": ["ENTRUSTED_DEVELOPMENT", "TECHNICAL_SERVICE"]}]
    item["applicable_if"] = item["applicable_if"].replace("合作开发", "委托开发或合作开发")
    assert report_state_consistency_failures([item]) == []


@pytest.mark.parametrize("description,active", [
    ("仅适用于技术转让或许可中受让人或被许可人按约实施现有专利或技术秘密的场景。", "TECHNOLOGY_LICENSE"),
    ("适用于技术咨询或服务合同。", "TECHNICAL_SERVICE"),
    ("适用于技术转让、许可及咨询合同。", "TECHNICAL_CONSULTING"),
    ("适用于技术转让/许可合同。", "TECHNOLOGY_LICENSE"),
    ("适用于技术转让／许可合同。", "TECHNOLOGY_LICENSE"),
    ("适用于技术转让合同与许可合同。", "TECHNOLOGY_LICENSE"),
    ("适用于技术开发和转让合同。", "TECHNOLOGY_TRANSFER"),
    ("适用于技术转让或技术许可合同。", "TECHNOLOGY_LICENSE"),
])
def test_shared_technology_prefix_in_coordinated_type_names_is_not_exclusive(description, active):
    item = review()
    item["applicable_if"] = description
    assert report_state_consistency_failures([item], transaction_context={"primary_subtype": active}) == []


def test_real_claim_liability_description_allows_activated_license_and_transfer_scenes():
    from review_v2.technology_contract_checklist import TECHNOLOGY_REVIEW_CHECKLIST
    checkpoint = next(row for row in TECHNOLOGY_REVIEW_CHECKLIST if row.item_id == "TC-12-01")
    item = review()
    item["applicable_if"] = checkpoint.applicable_if
    for primary in ("TECHNOLOGY_LICENSE", "TECHNOLOGY_TRANSFER"):
        item["decision_trace"]["legal_basis_applicability"] = {
            "primary_subtype": primary, "active_scenes": [primary, "TECHNICAL_SERVICE"],
        }
        assert report_state_consistency_failures([item]) == []


@pytest.mark.parametrize("description", ["仅适用于技术转让合同，费用及许可边界另行评估。",
    "仅适用于技术转让中受让人或被许可人请求核验资料的情形。"])
def test_role_mentions_and_disconnected_nouns_do_not_expand_declared_contract_types(description):
    item = review()
    item["applicable_if"] = description
    assert any(row["reason"] == "APPLICABILITY_DESCRIPTION_EXCLUDES_ACTIVE_TRANSACTION"
               for row in report_state_consistency_failures([item], transaction_context={"primary_subtype": "TECHNOLOGY_LICENSE"}))


@pytest.mark.parametrize("description", ["适用于委托开发或合作开发中涉及研发成果的情形。",
    "适用于技术服务合同，或其他合同中包含可独立识别的技术服务义务时。", "适用于技术开发合同。"])
def test_general_and_mixed_development_descriptions_remain_valid(description):
    item = review()
    item["applicable_if"] = description
    assert report_state_consistency_failures([item], transaction_context={"primary_subtype": "ENTRUSTED_DEVELOPMENT"}) == []


def test_activated_secondary_scene_is_respected_and_inapplicable_rules_are_not_reactivated():
    item = review()
    item["applicable_if"] = "仅适用于技术服务合同。"
    assert report_state_consistency_failures([item], transaction_context={"primary_subtype": "TECHNOLOGY_LICENSE", "secondary_modules": ["TECHNICAL_SERVICE"]}) == []
    item["applicability"] = {"status": "NOT_APPLICABLE", "applicable": False}
    item["coverage_status"] = "不适用"
    assert report_state_consistency_failures([item], transaction_context={"primary_subtype": "ENTRUSTED_DEVELOPMENT"}) == []


def scoped_disposal_finding(risk_id, source, title):
    gaps = [element(key, "MISSING", required_fact=label, residual_gap=label,
        remediation_action="明确" + label,
        fact_identity={"canonical_fact_key": key, "scope": "POST_CONTRACT:OWNER=甲方",
                       "party": "乙方", "object": target})
        for key, label, target in (
            ("copy_disposal", "复制件返还删除或销毁", "copy"),
            ("backup_disposal", "备份返还删除或销毁", "backup"),
            ("retention_deadline", "留存资料的删除期限", "retained_material"),
            ("disposal_confirmation", "处置完成确认", "retained_material"),
        )]
    return {"finding_id": risk_id, "source_review_ids": [source], "title": title,
            # Actions are modeled on each atom; no unvalidated whole-finding
            # prose is used as a substitute for that remediation projection.
            "final_missing_elements": gaps, "final_adverse_elements": []}


def test_same_atomic_issue_cannot_remain_two_risk_themes_under_different_titles():
    first = scoped_disposal_finding("risk-a", "RULE-A", "成果资料处置")
    second = scoped_disposal_finding("risk-b", "RULE-B", "保密资料返还销毁")
    before = deepcopy([first, second])
    assert report_state_consistency_failures([], [first, second]) == [{
        "reason": "DUPLICATE_UNDERLYING_ISSUE", "finding_indices": [0, 1],
        "risk_ids": ["risk-a", "risk-b"], "source_rule_ids": ["RULE-A", "RULE-B"],
    }]
    assert [first, second] == before
    first["source_rule_ids"] = ["RULE-A", "RULE-B"]
    assert report_state_consistency_failures([], [first]) == []


@pytest.mark.parametrize("dimension,value", [("scope", "NORMAL_DELIVERY"), ("party", "甲方"),
                                            ("object", "product_sample")])
def test_duplicate_gate_preserves_different_scope_actor_and_object(dimension, value):
    first = scoped_disposal_finding("risk-a", "RULE-A", "资料处置")
    second = scoped_disposal_finding("risk-b", "RULE-B", "资料处置")
    second["final_missing_elements"][0]["fact_identity"][dimension] = value
    assert report_state_consistency_failures([], [first, second]) == []


@pytest.mark.parametrize("change", ["independent_adverse", "different_action", "unknown_identity"])
def test_duplicate_gate_requires_same_complete_issue_and_remediation(change):
    first = scoped_disposal_finding("risk-a", "RULE-A", "资料处置")
    second = scoped_disposal_finding("risk-b", "RULE-B", "资料处置")
    if change == "independent_adverse":
        second["final_adverse_elements"] = [element("external_use", "ADVERSE",
            residual_gap="删除对外商业使用授权", remediation_action="删除对外商业使用授权",
            fact_identity={"canonical_fact_key": "external_use", "scope": "POST_CONTRACT",
                           "party": "乙方", "object": "production_data"},
            supporting_evidence=[{"clause_id": "c2", "quote": "乙方可对外商业使用生产数据。"}])]
    elif change == "different_action":
        second["final_missing_elements"][0]["remediation_action"] = "保留复制件并限制访问"
    else:
        second["final_missing_elements"][0]["fact_identity"].pop("party")
    assert report_state_consistency_failures([], [first, second]) == []
