"""Restore this turn's shared changes in memory only to audit legacy failures.

Application-only projection and the new unused registration extractor cannot
execute in the four granted-patent/license controls below. No source is reverted
on disk, so user edits and the running backend remain untouched.
"""
import inspect
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "backend"))
import review_v2.engine as e
import pytest


def replace_function(name, transform):
    source = inspect.getsource(getattr(e, name))
    previous = transform(source)
    assert previous != source, name
    exec(compile(previous, f"<pre-turn-{name}>", "exec"), e.__dict__)


replace_function("_set_multi_element_state", lambda s: s.replace(
    '        if status == "MISSING":\n            proposition = _uncovered_element_label(element)\n', ""))
replace_function("_apply_technology_common_semantic_rules", lambda s: s.replace(
    'missing_proposition = _uncovered_element_label({"element_id": element_id, "proposition": proposition})',
    'missing_proposition = proposition'))
replace_function("_reconcile_specialized_coverage_from_elements", lambda s: s.replace(
    'relevant = [row for row in item.coverage_elements or []\n                if row.get("risk_relevant") is not False and row.get("status") != "NOT_APPLICABLE"]',
    'relevant = [row for row in item.coverage_elements or [] if row.get("risk_relevant") is not False]'))


def previous_precedence(source):
    source = re.sub(r'    direct_source_ids = \{.*?\n    \}\n', '', source, flags=re.S)
    source = source.replace('and direct_source_ids.intersection(', 'and (')
    source = re.sub(r'            and _evidence_strength_at_least[^\n]*\n', '', source)
    source = re.sub(r'        selected = dict\(evidence_bound_positive.*?        reconciled.append\(selected\)',
                    '        reconciled.append(evidence_bound_positive or candidates[-1])', source, flags=re.S)
    start = source.index('    item.decision_trace["final_missing_facts"]')
    return source[:start] + '''    item.decision_trace["final_missing_facts"] = [
        _FINAL_GAP_LABELS.get(str(row.get("element_id") or ""),
            str(row.get("proposition") or _display_element_label(row.get("element_id"))))
        for row in missing
    ]
    return missing
'''


replace_function("_reconcile_item_element_precedence", previous_precedence)
replace_function("_prioritized_missing_elements", lambda s: re.sub(
    r'    if "final_missing_element_ids" in trace and item.coverage_elements:.*?    structured_from_elements =',
    '    structured_from_elements =', s, flags=re.S))
replace_function("_objective_fact_search_targets", lambda s: s[:s.index('    normalized = _positive_required_facts')] + '''    text = str(raw or "")
    if re.search(r"(?:尚未|未约定|无法核验|未提供|不完整|不足|缺失|未达到)", text):
        return []
    return _positive_required_facts(_text_sequence(raw))
''')


def previous_audit(source):
    source = source.replace('    authoritative_elements = final_missing is not None and bool(item.coverage_elements)\n', '')
    source = source.replace('    canonical_final_targets = (', '''    authoritative_elements = bool(final_missing) and all(
        str(row.get("element_id") or "") in _OBJECTIVE_FACT_SEARCH_TARGETS for row in final_missing
    )
    canonical_final_targets = (''')
    source = source.replace('before = canonical_final_targets if authoritative_elements else existing_targets',
                            'before = canonical_final_targets or existing_targets')
    source = source.replace('removed = [] if authoritative_elements else [', 'removed = [')
    source = source.replace('if authoritative_elements\n', 'if canonical_final_targets\n')
    source = source.replace('if authoritative_elements:', 'if canonical_final_targets:')
    return source


replace_function("_reconcile_item_search_audit_with_positive_evidence", previous_audit)
e._evidence_constrained_recommendation = lambda item, text: text
e._finding_recommendation = e._finding_recommendation_unchecked
current_terminology = e._normalize_technology_transaction_terminology
e._normalize_technology_transaction_terminology = lambda items, findings, classification: (
    current_terminology(items, findings, classification)
    if classification.get("primary_subtype") in {"TECHNOLOGY_LICENSE", "COOPERATIVE_DEVELOPMENT"} else None
)


def previous_confidentiality(source):
    source = source.replace('"bound_evidence_ids": [clause.clause_id for clause in obligation_clauses]}',
        '"evidence_terms": ["承担保密义务", "保密义务", "不得向", "不得泄露", "泄密责任", "禁止合作方泄露", "禁止合作人泄露"]}')
    source = source.replace('"bound_evidence_ids": [clause.clause_id for clause in filled_scope]}',
        '"evidence_terms": ["商业秘密", "保密信息", "保密范围", "源代码", "技术文档", "客户信息", "经营数据"]}')
    source = source.replace('合同列明保密信息的具体类别和对象。', '合同列明源代码、技术文档、客户信息和经营数据等保密信息类别。')
    source = source.replace('"required_fact": "保密信息的具体类别和边界"', '"required_fact": "保密信息类别（源代码、技术文档、客户信息和经营数据）"')
    source = source.replace(', "bound_evidence_ids": [clause.clause_id for clause in obligation_clauses if "不得用于" in _compact(clause.text)]', '')
    start = source.index('        if field_clauses and (item := by_id.get("TC-11-01"))')
    end = source.index('            if item.coverage_status == "部分覆盖" and is_cooperative_development:', start)
    block = source[start:end].replace('            _reconcile_specialized_coverage_from_elements(item)\n', '')
    block = block.replace('            if not is_cooperative_development:',
        '            _reconcile_specialized_coverage_from_elements(item)\n            if not is_cooperative_development:')
    return source[:start] + block + source[end:]


replace_function("_apply_technology_confidentiality_semantic_rules", previous_confidentiality)
names = [
    "test_license_evidence_semantics_and_atomic_elements_are_consistent",
    "test_new_patent_transfer_generalization_sample_routes_without_frozen_risks",
    "test_liability_cap_evidence_excludes_patent_maintenance_as_core_support",
    "test_patent_license_direction_and_provenance_golden_sample",
]
raise SystemExit(pytest.main([
    *["backend/tests/test_technology_transaction_routing_consistency.py::" + name for name in names],
    "-q", "--tb=short",
]))
