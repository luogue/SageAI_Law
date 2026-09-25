from copy import deepcopy
from dataclasses import dataclass, field

from review_v2.underlying_issue import (
    underlying_issue_descriptor, underlying_issue_signature, group_duplicate_underlying_issues,
)
from review_v2.material_disposition import material_disposition_elements
from review_v2.clause_parser import parse_contract_clauses


def atom(key="copy_disposition", status="MISSING", **kwargs):
    row = {
        "element_id": key, "source_fact_key": key, "status": status,
        "required_fact": "项目结束后的复制件处置", "residual_gap": "复制件返还、删除或销毁",
        "fact_identity": {"canonical_fact_key": key, "scope": "POST_CONTRACT", "party": "乙方", "object": "copy"},
        "underlying_issue_title": "项目结束后的资料处置机制",
    }
    row.update(kwargs)
    return row


def item(*rows, **kwargs):
    return {"coverage_elements": list(rows), **kwargs}


def test_shared_scoped_requirements_merge_despite_distinct_covered_rules():
    clauses = parse_contract_clauses("第一条 资料处置\n合同终止后，乙方应删除工作电脑中的甲方电子资料。")
    gaps = material_disposition_elements(clauses, actor="乙方", material_owner="甲方")
    a = item(*gaps, atom("ownership", "COVERED"), item_id="RULE-A")
    b = item(*gaps, atom("confidentiality", "COVERED"), item_id="RULE-B")
    assert underlying_issue_signature(a) is not None
    assert underlying_issue_signature(a) == underlying_issue_signature(b)
    assert group_duplicate_underlying_issues([a, b]) == [[0, 1]]


def test_same_key_aliases_order_punctuation_and_provenance_do_not_change_signature():
    first = atom()
    second = deepcopy(first)
    second["element_id"] = "another_rule_local_name"
    second["fact_identity"]["canonical_fact_key"] = "Copy-Disposition"
    second["residual_gap"] = "建议补充明确 复制件返还，删除或销毁。"
    second["source_review_id"] = "UNRELATED-SOURCE-ID"
    a = item(first, atom("backup_disposition"))
    b = item(atom("backup_disposition"), second, deepcopy(second))
    assert underlying_issue_signature(a) == underlying_issue_signature(b)


def test_titles_are_display_only_and_cannot_create_or_prevent_a_merge():
    a = atom(underlying_issue_title="资料处置")
    b = atom(underlying_issue_title="处置边界")
    assert underlying_issue_signature([a]) == underlying_issue_signature([b])
    assert underlying_issue_descriptor([a])["display_title"] == "资料处置"


def test_different_party_object_owner_or_scope_never_merge():
    original = atom()
    signature = underlying_issue_signature([original])
    for name, value in (("party", "甲方"), ("object", "backup"), ("scope", "DURING_CONTRACT"), ("scope", "POST_CONTRACT:OWNER=丙方")):
        changed = deepcopy(original)
        changed["fact_identity"][name] = value
        assert underlying_issue_signature([changed]) != signature


def test_unknown_or_missing_scope_refuses_signature_not_text_fallback():
    for scope in (None, "", "UNKNOWN", "POST_CONTRACT:OWNER=UNKNOWN"):
        row = atom()
        row["fact_identity"]["scope"] = scope
        assert underlying_issue_signature([row]) is None


def test_atomic_fallback_needs_real_source_scope_party_and_domain():
    row = atom()
    del row["fact_identity"]
    assert underlying_issue_signature([row]) is None
    row.update(scope="POST_CONTRACT", obligated_party="乙方", domain="copy", atomic=True)
    assert underlying_issue_signature([row]) is not None
    row["atomic"] = False
    assert underlying_issue_signature([row]) is None


def test_extra_independent_adverse_prevents_duplicate_group():
    a = item(atom())
    adverse = atom("independent_reuse", "ADVERSE", supporting_evidence=[{"clause_id": "C9", "quote": "原文"}],
                   residual_gap="删除对外商业使用授权", recommendation_action="删除对外商业使用授权")
    b = item(atom(), adverse)
    assert underlying_issue_signature(b) is not None
    assert underlying_issue_signature(a) != underlying_issue_signature(b)
    del adverse["fact_identity"]
    assert underlying_issue_signature(item(atom(), adverse)) is None


def test_unbound_adverse_and_unknown_condition_are_not_drafting_duplicates():
    assert underlying_issue_signature(item(atom(), atom("x", "ADVERSE"))) is None
    for status in ("CONDITION_UNRESOLVED", "INSUFFICIENT_CONTEXT", "UNKNOWN", "UNCERTAIN", "REFERENCED_BUT_NOT_PROVIDED"):
        assert underlying_issue_signature(item(atom(), atom("conditional", status))) is None
    conditional = atom("conditional", "MISSING", conditional_element=True, prerequisite_status="UNKNOWN")
    assert underlying_issue_signature(item(atom(), conditional)) is None


def test_different_actual_actions_or_residuals_are_not_equivalent():
    a = atom(recommendation_action="删除已有复制件")
    b = atom(recommendation_action="保留已有复制件")
    assert underlying_issue_signature([a]) != underlying_issue_signature([b])
    c = atom(residual_gap="复制件访问权限")
    assert underlying_issue_signature([c]) != underlying_issue_signature([atom()])


def test_final_sets_are_authoritative_and_do_not_hide_independent_adverse():
    a = {"final_missing_elements": [atom()], "final_adverse_elements": []}
    assert underlying_issue_signature(a) == underlying_issue_signature(item(atom()))
    assert underlying_issue_signature({"final_missing_elements": [], "final_adverse_elements": []}) is None
    b = deepcopy(a)
    b["coverage_elements"] = [atom("other", "ADVERSE", evidence_ids=["C9"], residual_gap="取消不利安排")]
    assert underlying_issue_signature(b) != underlying_issue_signature(a)


def test_dataclass_and_dict_input_match_without_mutation():
    @dataclass
    class Finding:
        final_missing_elements: list = field(default_factory=list)
        final_adverse_elements: list = field(default_factory=list)

    data = {"final_missing_elements": [atom()], "final_adverse_elements": []}
    before = deepcopy(data)
    assert underlying_issue_signature(Finding(**data)) == underlying_issue_signature(data)
    assert data == before


def test_duplicate_same_identity_with_conflicting_status_or_action_fails_closed():
    row = atom()
    changed = atom(recommendation_action="删除复制件")
    assert underlying_issue_signature([row, changed]) is None
    changed = atom(status="PARTIALLY_COVERED")
    assert underlying_issue_signature([row, changed]) is None


def test_search_target_order_and_structured_action_target_order_are_stable():
    a = atom(residual_gap="", search_targets=["地域范围", "许可期限"],
             remediation_action={"action": "clarify", "target_keys": ["license_duration", "license_territory"]})
    b = atom(residual_gap="", search_targets=["许可期限。", "地域范围。"],
             remediation_action={"target_keys": ["license_territory", "license_duration"], "action": "clarify", "source_review_id": "X"})
    assert underlying_issue_signature([a]) == underlying_issue_signature([b])


def test_empty_state_only_and_unmodeled_group_do_not_create_signature():
    assert underlying_issue_signature([]) is None
    assert underlying_issue_signature(item(atom(status="COVERED"))) is None
    assert underlying_issue_signature([atom(residual_gap="事项已有部分约定")]) is None
    assert underlying_issue_signature([atom("core_contract_arrangement")]) is None


def test_explicit_source_and_target_domains_remain_significant():
    a = atom(domain="technical_material", source_domain="technical_material")
    b = deepcopy(a)
    b["source_domain"] = "product_acceptance"
    assert underlying_issue_signature([a]) != underlying_issue_signature([b])
    b = deepcopy(a)
    b["domain"] = "service_acceptance"
    assert underlying_issue_signature([a]) != underlying_issue_signature([b])
    alias = deepcopy(a)
    alias["source_domain"] = "Technical-Material"
    assert underlying_issue_signature([a]) == underlying_issue_signature([alias])


def test_generated_recommendation_prefix_does_not_create_a_distinct_action():
    a = atom()
    b = atom(recommendation_action="建议明确复制件返还、删除或销毁。")
    assert underlying_issue_signature([a]) == underlying_issue_signature([b])


def test_structured_action_requirement_key_aliases_normalize():
    a = atom(remediation_action={"action": "clarify", "target_keys": ["copyDisposition"]})
    b = atom(remediation_action={"action": "clarify", "targetKeys": ["COPY-DISPOSITION"], "sourceReviewId": "X"})
    assert underlying_issue_signature([a]) == underlying_issue_signature([b])


def test_false_conditional_na_is_ignored_but_unknown_conditions_block_merge():
    a = item(atom())
    b = item(atom(), atom("upstream_authorization", "N/A", conditional_element=True, prerequisite_status="FALSE"))
    assert underlying_issue_signature(a) == underlying_issue_signature(b)
    b["coverage_elements"][-1].update(status="CONDITION_UNRESOLVED", prerequisite_status="UNKNOWN")
    assert underlying_issue_signature(b) is None


def test_exclusive_only_qualifier_is_never_removed_from_a_remedy():
    a = atom(recommendation_action="建议明确仅删除电子复制件")
    b = atom(recommendation_action="建议明确删除电子复制件")
    assert underlying_issue_signature([a]) != underlying_issue_signature([b])
    assert underlying_issue_descriptor([a])["requirements"][0]["remediation"].startswith("仅")


def test_structured_procedure_lists_preserve_order_and_repeated_actions():
    for field_name in ("steps", "actions", "sequence"):
        a = atom(remediation_action={field_name: ["完成资料交接", "删除备份"]})
        b = atom(remediation_action={field_name: ["删除备份", "完成资料交接"]})
        assert underlying_issue_signature([a]) != underlying_issue_signature([b])
        repeated = atom(remediation_action={field_name: ["完成资料交接", "删除备份", "完成资料交接"]})
        assert underlying_issue_signature([a]) != underlying_issue_signature([repeated])
    a = atom(remediation_action=["完成资料交接", "删除备份"])
    b = atom(remediation_action=["删除备份", "完成资料交接"])
    assert underlying_issue_signature([a]) != underlying_issue_signature([b])


def test_custom_overall_recommendations_without_projection_policy_refuse_merge():
    a = item(atom(), recommendation="建议删除所有复制件。")
    b = item(atom(), recommendation="建议保留所有复制件。")
    assert underlying_issue_descriptor(a) is None
    assert underlying_issue_descriptor(b) is None
    assert group_duplicate_underlying_issues([a, b]) == []
    for field_name in ("formal_recommendation", "suggested_clause_example", "action_suggestion", "正式建议"):
        assert underlying_issue_descriptor(item(atom(), **{field_name: "建议采取独立措施。"})) is None


def test_production_item_and_finding_projection_policy_use_same_comparison():
    row = atom(recommendation_action="删除复制件")
    a = item(row, suggested_clause_example="建议删除复制件。", decision_trace={
        "recommendation_element_projection": {"policy": "FINAL_UNRESOLVED_ELEMENTS"},
    })
    b = {"final_missing_elements": [row], "final_adverse_elements": [],
         "recommendation": "建议删除复制件。",
         "aggregation_signals": {"recommendation_element_policy": "FINAL_UNRESOLVED_ELEMENTS"}}
    assert underlying_issue_signature(a) is not None
    assert underlying_issue_signature(a) == underlying_issue_signature(b)
    assert group_duplicate_underlying_issues([a, b]) == [[0, 1]]
    changed = deepcopy(b)
    changed["final_missing_elements"][0]["recommendation_action"] = "保留复制件"
    changed["recommendation"] = "建议保留复制件。"
    assert underlying_issue_signature(a) != underlying_issue_signature(changed)
    assert underlying_issue_signature([row]) is not None
