"""Opt-in DeepSeek regression; no mocked semantic answers or sample identities."""
import os
import pytest
from review_v2.clause_parser import parse_contract_clauses
from review_v2.deepseek_facts import extract, verify
from review_v2.employment_fact_store import FactStore
from review_v2.fact_verification import verified_store


@pytest.mark.skipif(os.getenv('RUN_DEEPSEEK_REGRESSION') != '1', reason='explicit live model regression')
@pytest.mark.parametrize('exclusion,restriction,expected_prior,arrangement', [
    ('受领之前已向公众合法开放的资料不属于保密资料。',
     '受领人离任后原则上不能加入竞争企业，具体地域、期间和补偿另议。', False, 'EXISTS'),
    ('受领人在此次获取之前已合法持有的资料除外。',
     '离任后是否承担竞争从业限制，由双方届时另行协商。', True, 'DEFERRED'),
    ('在获取前已公开的资料、受领人能证明此前已合法掌握的资料均除外。',
     '受领人离任后不得经营竞争业务，期限以后再行确定。', True, 'EXISTS'),
])
def test_live_proposition_boundaries(exclusion, restriction, expected_prior, arrangement):
    text = '信息保密协议\n第一条\n'+exclusion+'\n第二条\n'+restriction+'\n第三条\n发现泄露应立即通知提供人并协助减轻损害。\n第四条\n因违反保密承诺造成损失的，承担依法赔偿损失的责任。'
    keys = ['non_compete.arrangement', 'non_compete.businesses', 'nda.exception_public', 'nda.exception_prior', 'nda.remedies', 'nda.incident_response']
    clauses = parse_contract_clauses(text)
    raw = extract(clauses, concept_keys=keys)
    store = FactStore(text, clauses, raw)
    checked = verified_store(store, verify(clauses, store))
    assert bool(checked.get('nda.exception_prior')) is expected_prior
    # Explicit statement that no current obligation is assumed can also be
    # recorded as EXPLICIT_NONE, but parameter deferral must remain EXISTS.
    assert arrangement in checked.values('non_compete.arrangement')
    assert not checked.get('non_compete.businesses')
    assert checked.get('nda.remedies') and checked.get('nda.incident_response')
    for f in checked.get('nda.remedies'):
        assert all('赔偿' in e['quote'] for e in f['evidence'])
