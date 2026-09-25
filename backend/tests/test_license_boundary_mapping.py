"""Licence boundaries keep their action, condition and source polarity."""
import pytest
from review_v2.clause_parser import parse_contract_clauses
from review_v2.license_control_facts import elements


def atom(text, key):
    return next(e for e in elements('secret_license_scope', parse_contract_clauses(text)) if e['element_id'] == key)


@pytest.mark.parametrize('action', ['转让', '再许可', '转许可', '分许可'])
@pytest.mark.parametrize('sentence', [
    '未经甲方书面同意，乙方不得将本合同项下许可权整体{action}给第三方。',
    '被许可方不得向第三方{action}本合同许可技术。',
    '乙方{action}许可权须取得甲方书面同意。',
    '经许可方书面批准，被许可方方可向第三方{action}许可技术。',
])
def test_disposition_word_order_and_consent(action, sentence):
    text = sentence.format(action=action)
    result = atom(text, 'transfer_or_sublicense_boundary')
    assert result['status'] == 'COVERED'
    assert all(s['quote'] in text for s in result['supporting_evidence'])


@pytest.mark.parametrize('trigger', ['合同终止后', '合同解除后', '许可期限届满后', '许可期到期后', '合同期满后'])
@pytest.mark.parametrize('duty', ['乙方应停止继续使用许可技术秘密。', '乙方不得继续使用许可技术。', '乙方继续使用相关技术的，应另行协商并签订书面协议。'])
def test_expiration_and_termination_boundary(trigger, duty):
    text = trigger + '，' + duty
    result = atom(text, 'post_termination_use_boundary')
    assert result['status'] == 'COVERED'
    assert result['supporting_evidence'][0]['quote'] == text


@pytest.mark.parametrize('text,key', [
    ('双方未明确约定乙方不得再许可。', 'transfer_or_sublicense_boundary'),
    ('乙方是否不得再许可，双方未作明确约定。', 'transfer_or_sublicense_boundary'),
    ('双方未明确约定：\n乙方不得再许可；\n乙方不得转让许可权。', 'transfer_or_sublicense_boundary'),
    ('双方否认乙方不得再许可。', 'transfer_or_sublicense_boundary'),
    ('双方未约定合同终止后乙方应停止使用许可技术。', 'post_termination_use_boundary'),
    ('合同终止后乙方是否应停止使用许可技术，双方未明确。', 'post_termination_use_boundary'),
    ('双方未明确约定：\n合同终止后乙方应停止使用许可技术。', 'post_termination_use_boundary'),
    ('合同终止后，乙方可以继续使用许可技术。', 'post_termination_use_boundary'),
    ('乙方应停止使用许可技术。', 'post_termination_use_boundary'),
    ('合同终止后，双方继续承担保密义务。', 'post_termination_use_boundary'),
    ('后续改进成果不得转让。', 'transfer_or_sublicense_boundary'),
    ('乙方不得向第三方转让应收账款。', 'transfer_or_sublicense_boundary'),
    ('合同终止后，乙方应停止使用甲方设备。', 'post_termination_use_boundary'),
    ('合同终止后，乙方不应停止继续使用许可技术。', 'post_termination_use_boundary'),
    ('许可期限届满后，乙方继续使用技术无需签订书面协议。', 'post_termination_use_boundary'),
])
def test_absence_or_another_proposition_is_not_a_boundary(text, key):
    result = atom(text, key)
    assert result['status'] == 'MISSING'
    assert not result['supporting_evidence']


@pytest.mark.parametrize('party', ['甲方/许可方', '乙方/被许可方'])
def test_boundary_facts_reach_final_report_with_owned_evidence(party):
    from pathlib import Path
    from review_v2.engine import review_contract_v2
    from review_v2.user_profile import UserRiskProfile
    text = Path(__file__).with_name('fixtures').joinpath('technical_secret_scoped_license.txt').read_text(encoding='utf-8')
    report = review_contract_v2(text, 'technology', use_llm=False, profile=UserRiskProfile(user_identity=party))
    assert report['release_quality_gate']['status'] == 'REPORT_READY'
    assert not report['release_quality_gate']['failures']
    item = next(i for i in report['items'] if i['item_id'] == 'TC-07-01')
    rows = {e['element_id']: e for e in item['coverage_elements']}
    assert len(rows) == 7
    assert all(e['status'] == 'COVERED' and e['evidence_ids'] for e in rows.values())
    for key in ('transfer_or_sublicense_boundary', 'post_termination_use_boundary'):
        assert rows[key]['source_fact_key'] == 'license_control.' + key
        assert rows[key]['supporting_evidence']
        assert all(s['quote'] in text for s in rows[key]['supporting_evidence'])
