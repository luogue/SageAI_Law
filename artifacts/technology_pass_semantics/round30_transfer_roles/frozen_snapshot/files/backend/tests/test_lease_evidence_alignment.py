"""Evidence relationships survive renumbering, unrelated clauses and stale PASS."""
from copy import deepcopy
from types import SimpleNamespace

import pytest

from .test_lease_semantic_consistency import report
from review_v2.clause_parser import parse_contract_clauses
from review_v2.engine import _apply_coverage_evidence_gate, _search_final_element, _specific_gap_consequence
from review_v2.lease_semantics import PROFILES, corpus_facts, supports, consistency_failures


@pytest.mark.parametrize('node', ['no_damage_return', 'damage_definition', 'tenant_fault_damage', 'handover_evidence'])
def test_pass_has_exact_positive_elements_and_matching_audit(report, node):
    row = next(r for r in report['items'] if r['node_id'] == node)
    assert row['coverage_status'] == '通过'
    for requirement in PROFILES[node]:
        element = next(e for e in row['coverage_elements'] if e['element_id'] == requirement['element_id'])
        assert element['status'] == 'COVERED'
        assert any(supports(requirement, e) for e in row['evidence_clauses'])
        assert element['source_spans'] and element['source_locations']
        audit = next(a for a in row['decision_trace']['element_absence_searches'] if a['element_id'] == requirement['element_id'])
        assert audit['result'] == 'FOUND' and audit['supporting_evidence']


@pytest.mark.parametrize('node', ['no_damage_return', 'damage_definition', 'tenant_fault_damage', 'handover_evidence', 'reasonable_repair_cost'])
def test_unrelated_same_theme_is_not_positive(node):
    clauses = parse_contract_clauses('99.6 房屋约定\n未经甲方同意转租应承担违约责任。甲方不维修时乙方可自行维修。')
    assert not any(corpus_facts(clauses, PROFILES[node]).values())


def test_repair_cost_atoms_do_not_reuse_repair_permission(report):
    row = next(r for r in report['items'] if r['node_id'] == 'reasonable_repair_cost')
    states = {e['element_id']: e['status'] for e in row['coverage_elements']}
    assert states == {'repair_necessary': 'MISSING', 'repair_reasonable': 'MISSING', 'repair_actual': 'MISSING', 'repair_voucher': 'MISSING'}
    assert row['coverage_status'] == '缺失'
    for e in row['evidence_clauses']:
        assert '合理维修费用' in e['text']
    element = PROFILES['reasonable_repair_cost'][2]
    quote = {'clause_id': 'C8', 'location': '第八条', 'text': '乙方造成损坏时，从押金扣除的维修费用以实际发生为限。', 'supports_element_ids': ['repair_reasonable']}
    assert not supports(element, quote)
    quote['supports_element_ids'] = ['repair_actual']
    assert supports(element, quote)
    quote['source_type'] = 'SEARCH_AUDIT'
    assert not supports(element, quote)


def test_stale_pass_without_positive_fails_gate_and_is_readjudicated(report):
    row = deepcopy(next(r for r in report['items'] if r['node_id'] == 'tenant_fault_damage'))
    row['item_id'] = 'RENAMED-RULE'
    row['evidence_clauses'] = [{'source_type': 'SEARCH_AUDIT', 'result': 'no_positive_fact',
                              'clause_id': 'SEARCH-ONLY', 'location': '全文检索',
                              'text': '乙方使用不当造成损坏的，乙方承担赔偿责任。'}]
    for e in row['coverage_elements']:
        e.update(status='MISSING', source_spans=[], source_locations=[])
    row['decision_trace']['element_evidence_truth'] = {}
    obj = SimpleNamespace(**row)
    assert any(f['requirement'] == 'PASS_WITHOUT_POSITIVE_ELEMENT_EVIDENCE' for f in consistency_failures([obj]))
    _apply_coverage_evidence_gate([obj])
    assert obj.coverage_status != '通过'


def test_absence_audit_uses_same_predicate_as_positive_evidence(report):
    row = SimpleNamespace(**deepcopy(next(r for r in report['items'] if r['node_id'] == 'reasonable_repair_cost')))
    clauses = parse_contract_clauses('88.9 修理\n合理维修费用由甲方承担。')
    for e in row.coverage_elements:
        audit = _search_final_element(row, e, clauses)
        assert audit['result'] != 'FOUND'


def test_lease_narratives_are_domain_scoped_even_after_renumbering(report):
    row = SimpleNamespace(**deepcopy(next(r for r in report['items'] if r['node_id'] == 'third_party_tort')))
    row.item_id = 'CUSTOM-006'
    consequence = _specific_gap_consequence(row, '第三方侵权')
    assert '房屋' in consequence
    for term in ('停用、下架', '替换成本', '出卖人追偿', '对出卖人'):
        assert term not in consequence
        assert term not in report['result']


def test_report_counts_are_rederived(report):
    from collections import Counter
    from review_v2.report_statistics import statistics_gate
    assert Counter(r['coverage_status'] for r in report['items']) == report['coverage_summary']
    assert statistics_gate(report)['status'] == 'REPORT_READY'
    assert report['release_quality_gate']['status'] == 'BLOCKED'
    assert any(failure.get('requirement') == 'RELEASE_HOLD' for failure in report['release_quality_gate']['failures'])


def test_fact_graph_cannot_bind_damage_to_unauthorised_sublease():
    from review_v2.lease_contract_facts import extract_house_lease_facts
    facts = extract_house_lease_facts('第三条 乙方擅自转租应承担违约责任。\n第十条 因乙方使用不当造成损坏的，由乙方赔偿维修费用。')
    assert facts.repair.tenant_fault == 'tenant'
    assert all('使用不当' in e.source_text for e in facts.nodes['repair.tenant_fault'].evidence)
