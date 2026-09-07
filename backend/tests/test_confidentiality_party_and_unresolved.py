from copy import deepcopy
from types import SimpleNamespace

import pytest

from review_v2.clause_parser import parse_contract_clauses
from review_v2.confidentiality_remedies import confidentiality_remedy_elements, confidentiality_binding_failures
from review_v2.element_resolution import unresolved_requirements
from review_v2 import engine


def remedies(text):
    return {row['element_id']: row for row in confidentiality_remedy_elements(parse_contract_clauses(text))}


@pytest.mark.parametrize('a,b', [('买方', '卖方'), ('甲方', '乙方'), ('被许可方', '许可方')])
def test_compensation_is_not_penalty_and_one_party_is_not_another(a, b):
    rows = remedies(f'第一条 泄密责任\n{a}违反保密义务的，应停止使用和披露，采取措施防止继续扩散并赔偿损失。\n'
                    f'第二条 泄密责任\n{b}违反保密义务的，应停止使用和披露并赔偿可证明损失。')
    assert rows['breach_damage_liability']['status'] == 'COVERED'
    assert rows['specific_confidentiality_penalty']['status'] == 'NOT_APPLICABLE'
    assert rows['excess_loss_compensation']['status'] == 'NOT_APPLICABLE'
    mitigation = rows['mitigation_obligation']
    assert mitigation['status'] == 'PARTIALLY_COVERED'
    parties = {r['obligated_party']: r for r in mitigation['party_coverage']}
    assert parties[a]['status'] == 'COVERED'
    assert parties[b]['status'] == 'MISSING'
    assert mitigation['residual_gap'].startswith(b)
    assert all(f['obligated_party'] == a for f in mitigation['supporting_evidence'])
    assert not confidentiality_binding_failures(list(rows.values()))
    corrupt = deepcopy(mitigation)
    corrupt['party_coverage'][1]['status'] = 'COVERED'
    corrupt['party_coverage'][1]['supporting_evidence'] = corrupt['supporting_evidence']
    assert confidentiality_binding_failures([corrupt])


def test_specific_penalty_and_shortfall_require_separate_direct_terms():
    rows = remedies('第一条 泄密责任\n任何一方违反保密义务，应支付30万元违约金；违约金不足以弥补损失的，还应赔偿不足部分。')
    assert rows['specific_confidentiality_penalty']['status'] == 'COVERED'
    assert rows['excess_loss_compensation']['status'] == 'COVERED'
    assert not confidentiality_binding_failures(list(rows.values()))
    rows = remedies('第一条 泄密责任\n甲方违反保密义务应赔偿损失，不承担违约金。')
    assert rows['specific_confidentiality_penalty']['status'] == 'NOT_APPLICABLE'


def test_same_paragraph_different_actors_do_not_share_remedies():
    rows = remedies('第一条 泄密责任\n买方违反保密义务应采取措施防止扩散并赔偿损失；卖方违反保密义务应停止披露并赔偿损失。')
    mitigation = rows['mitigation_obligation']
    assert mitigation['status'] == 'PARTIALLY_COVERED'
    assert mitigation['residual_gap'].startswith('卖方')
    assert all('卖方违反' not in f['quote'] for f in mitigation['supporting_evidence'])
    disclosure = rows['stop_disclosure']
    assert disclosure['residual_gap'].startswith('买方')
    assert all(f['obligated_party'] == '卖方' for f in disclosure['supporting_evidence'])
    assert not confidentiality_binding_failures(list(rows.values()))


def test_partial_without_residual_metadata_is_not_silently_discarded():
    rows = [
        {'element_id': 'record_scope', 'status': 'PARTIALLY_COVERED', 'proposition': '历史记录的具体范围', 'evidence_ids': ['C1']},
        {'element_id': 'record_number', 'status': 'MISSING', 'proposition': '记录编号'},
        {'element_id': 'record_exists', 'status': 'COVERED', 'proposition': '记录存在'},
        {'element_id': 'open_source', 'status': 'CONDITION_UNRESOLVED', 'conditional_element': True, 'prerequisite_status': 'UNKNOWN'},
    ]
    source = SimpleNamespace(item_id='EXAMPLE', coverage_elements=rows, decision_trace={}, suggested_clause_example='')
    finding = SimpleNamespace(source_review_ids=['EXAMPLE'], final_missing_elements=[], aggregation_signals={}, issue='')
    engine._finalize_element_recommendation_sources([source], [finding])
    expected = {'record_scope', 'record_number'}
    assert {r['element_id'] for r in unresolved_requirements(rows)} == expected
    assert {r['element_id'] for r in finding.final_missing_elements} == expected
    assert '历史记录的具体范围' in finding.recommendation
    assert '历史记录的具体范围' in finding.issue
    assert '记录存在' not in finding.recommendation
