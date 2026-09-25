from copy import deepcopy
from pathlib import Path
from types import SimpleNamespace

import pytest

from .test_lease_semantic_consistency import report
from review_v2.clause_parser import parse_contract_clauses
from review_v2.engine import _search_final_element, review_contract_v2
from review_v2.lease_semantics import PROFILES, corpus_facts
from review_v2.recommendation_children import child_set_gate


@pytest.mark.parametrize('sentence', [
    '甲方应在30个工作日内将押金返还乙方。',
    '甲方应在三十个工作日内将押金：\n☐计息\n☑不计息\n返还乙方。',
    '甲方应在7日内返还押金。',
    '押金应当在十日内退还。',
])
def test_deadline_word_orders_share_positive_audit(report, sentence):
    clauses = parse_contract_clauses('98.2 押金结算\n' + sentence)
    spec = PROFILES['deposit_return_deadline'][1]
    facts = corpus_facts(clauses, [spec])
    assert facts['return_deadline']
    item = SimpleNamespace(**deepcopy(next(i for i in report['items'] if i['node_id'] == 'deposit_return_deadline')))
    audit = _search_final_element(item, spec, clauses)
    assert audit['result'] == 'FOUND' and audit['supporting_evidence']


def test_unrelated_payment_deadline_cannot_support_deposit_deadline():
    clauses = parse_contract_clauses('第九条 付款\n乙方应在30个工作日内支付租金。押金在终止时返还。')
    assert not corpus_facts(clauses, PROFILES['deposit_return_deadline'])['return_deadline']


def test_current_deadline_and_preemption_have_source_bound_pass(report):
    for node, location in [('deposit_return_deadline', '第六条（三）'), ('sale_notice_preemption', '第十一条')]:
        row = next(r for r in report['items'] if r['node_id'] == node)
        assert row['coverage_status'] == '通过'
        assert row['evidence_clauses']
        target_ids = {'return_deadline'} if node == 'deposit_return_deadline' else {'sale_notice', 'preemption_right'}
        targets = [e for e in row['coverage_elements'] if e['element_id'] in target_ids]
        assert targets and all(e['source_locations'] and all(loc.startswith(location) for loc in e['source_locations']) for e in targets)
        assert all(a['result'] == 'FOUND' and a['supporting_evidence'] for a in row['decision_trace']['element_absence_searches'])


def test_all_actionable_children_survive_each_projection(report):
    gate = child_set_gate(report)
    assert gate['status'] == 'REPORT_READY'
    row = next(r for r in gate['rows'] if r['risk_id'] == 'RF-PROPERTY-DAMAGE-001')
    expected = {'HL-035', 'HL-037', 'HL-040', 'HL-041'}
    assert set(row['actionable_child_ids']) == set(row['theme_child_ids']) == set(row['formal_child_ids']) == expected
    assert not row['missing_top_fragments']
    broken = deepcopy(report)
    for rec in broken['recommendations']:
        rec['fragments'] = [f for f in rec['fragments'] if 'HL-041' not in f.get('source_review_ids', [])]
    assert child_set_gate(broken)['status'] == 'BLOCKED'


def core_projection(result):
    return {i['node_id']: (i['coverage_status'], sorted(
        (e['element_id'], e['status'], tuple(e.get('source_locations', [])), tuple(e.get('source_spans', [])))
        for e in i['coverage_elements'])) for i in result['items'] if i['node_id'] in PROFILES}


def test_same_input_repeated_runs_keep_core_evidence_and_coverage(report):
    from docx import Document
    path = Path(__file__).resolve().parents[2] / 'test_data/53 租赁合同.docx'
    text = '\n'.join(p.text for p in Document(path).paragraphs if p.text.strip())
    second = review_contract_v2(text, 'lease', use_llm=False)
    assert core_projection(report) == core_projection(second)
    assert {i['node_id']: i['coverage_status'] for i in report['items']} == {i['node_id']: i['coverage_status'] for i in second['items']}


def test_release_hold_keeps_full_report_blocked(monkeypatch):
    monkeypatch.setenv('REVIEW_V2_RELEASE_HOLD_DOMAINS', 'lease')
    output = review_contract_v2('第六条 甲方在30个工作日内将押金返还乙方。', 'lease', use_llm=False)
    assert output['release_quality_gate']['status'] == 'BLOCKED'
    assert output['release_hold']['active']
    assert output['items'] and output['result']
