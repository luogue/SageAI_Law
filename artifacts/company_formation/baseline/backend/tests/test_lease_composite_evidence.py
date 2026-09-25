from copy import deepcopy

import pytest

from .test_lease_semantic_consistency import report
from review_v2.clause_parser import parse_contract_clauses
from review_v2.lease_semantics import EARLY, PROFILES, corpus_facts, supports


NOTICE = '任何一方因不可抗力不能履行合同或者不能完全履行合同的，应及时通知另一方，并在10日内提供合理证明材料。'
EXIT = '不可抗力持续超过30日且导致房屋无法正常使用的，任何一方均有权书面通知另一方解除合同。'


@pytest.mark.parametrize('text,event,notice', [(NOTICE, False, True), (EXIT, True, False)])
def test_force_facts_do_not_cross_bind(text, event, notice):
    row = {'clause_id': 'custom', 'location': '自定义条款', 'text': text}
    assert supports(PROFILES['force_majeure'][0], row) is event
    assert supports(PROFILES['force_majeure'][1], row) is notice


@pytest.mark.parametrize('tail,covered', [
    ('', False),
    ('违约方应支付一个月租金作为违约金。', True),
    ('违约方无需承担违约金或赔偿。', True),
])
def test_composite_requires_condition_and_consequence(tail, covered):
    clauses = parse_contract_clauses('第九条 退出\n提前退租应提前20日通知对方。\n' + tail)
    facts = corpus_facts(clauses, [EARLY])['early_exit']
    assert bool(facts) is covered
    if covered:
        assert tail in facts[0]['text']
        assert supports(EARLY, facts[0])


def test_unrelated_clause_penalty_cannot_complete_exit():
    clauses = parse_contract_clauses('第九条 提前退租\n提前退租应提前20日通知对方。\n第十条 欠租\n欠租方应支付违约金。')
    assert not corpus_facts(clauses, [EARLY])['early_exit']


def test_current_rule_mapping_and_display_prove_coverage(report):
    for node in ('force_majeure', 'early_surrender'):
        item = next(i for i in report['items'] if i['node_id'] == node)
        specs = {e['element_id']: e for e in item['decision_trace']['semantic_requirements']}
        positives = [r for r in item['rule_evidence_package']['items'] if r.get('source_type') != 'SEARCH_AUDIT']
        for row in positives:
            for key in row['supports_element_ids']:
                assert supports(specs[key], row)
                assert supports(specs[key], {**row, 'text': row['quoted_text']})
        for element in item['coverage_elements']:
            if element['status'] == 'COVERED':
                assert any(supports(specs[element['element_id']], r) for r in positives)
        for row in item['evidence_clauses']:
            for key in row.get('supports_element_ids', []):
                assert supports(specs[key], row)
                assert supports(specs[key], {**row, 'text': row['quote']})
    early = next(i for i in report['items'] if i['node_id'] == 'early_surrender')
    assert early['coverage_status'] == '通过'
    quotes = '\n'.join(r['quoted_text'] for r in early['rule_evidence_package']['items'])
    assert '提前30日' in quotes and '两个月房屋租金' in quotes and '76,000元' in quotes
    force = next(i for i in report['items'] if i['node_id'] == 'force_majeure')
    assert {e['element_id']: e['status'] for e in force['coverage_elements']} == {
        'force_event': 'COVERED', 'force_notice': 'COVERED', 'force_settlement': 'MISSING'}
