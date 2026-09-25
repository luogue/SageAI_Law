from types import SimpleNamespace
import pytest
from review_v2.legal_basis_selection import select, audit_result, rank_candidates, directness_score
from test_legal_basis_production_path import upload

def evaluate(topics):
    item=SimpleNamespace(item_id='arbitrary',coverage_status='通过',legal_basis_index='',legal_references=[],
        decision_trace={'legal_basis_runtime_trace':{'stages':[]}})
    select(item,SimpleNamespace(legal_basis_topics=topics,legal_basis=''))
    return item

def test_direct_special_beats_direct_general():
    item=evaluate(('overdue_retrieval','unauthorized_subcustody'))
    assert item.legal_basis_index.startswith('《中华人民共和国民法典》第894条')

def test_direct_general_beats_only_related_special():
    rows=[{'relevance_score':directness_score('STRONG_RELATED','SPECIAL'),'article':'special'},
          {'relevance_score':directness_score('DIRECT','GENERAL'),'article':'general'}]
    assert rank_candidates(rows)[0]['article']=='general'

def test_only_general_is_allowed():
    item=evaluate(('retrieval_procedure',))
    assert audit_result(item)['status']=='REPORT_READY'
    assert item.legal_basis_index=='《中华人民共和国民法典》第509条'

def test_other_part_of_same_mechanism_not_direct():
    item=evaluate(('overdue_retrieval','overdue_payment_context','extra_fee_arrangement','necessary_disposal_costs'))
    trace=item.decision_trace['legal_basis_runtime_trace']
    candidate=next(c for c in trace['candidate_articles']if c['article']=='第902条')
    assert candidate['basis_relation']=='BACKGROUND' and not candidate['eligible']
    assert '第902条' not in item.legal_basis_index
    assert any(p['support_type']=='NO_DIRECT_AUTHORITY' for p in trace['legal_propositions'])

def test_subcustody_special_before_breach_background():
    item=evaluate(('general_breach_liability','unauthorized_subcustody'))
    assert item.legal_basis_index.startswith('《中华人民共和国民法典》第894条')

def test_audit_catches_removed_special():
    item=evaluate(('unauthorized_subcustody','general_breach_liability'))
    item.legal_basis_index='《中华人民共和国民法典》第577条'
    assert audit_result(item)['special_over_general_violation']

def test_audit_catches_weak_basis_promoted_to_direct():
    item=evaluate(('state_records',))
    item.legal_references=[{'article':'第509条','support_type':'DIRECT_SUPPORT','claim_id':'bad'}]
    assert audit_result(item)['weak_related_as_direct']==['bad']

def test_other_contract_special_is_not_applicable():
    item=evaluate(('unauthorized_subcustody','general_breach_liability'))
    select(item,SimpleNamespace(legal_basis_topics=('unauthorized_subcustody','general_breach_liability'),
        legal_basis='',legal_basis_domain='sale'))
    assert '第894条' not in item.legal_basis_index
    assert item.legal_basis_index=='《中华人民共和国民法典》第577条'

def test_same_contract_special_has_domain_weight():
    item=evaluate(('unauthorized_subcustody',))
    select(item,SimpleNamespace(legal_basis_topics=('unauthorized_subcustody',),legal_basis='',legal_basis_domain='custody'))
    candidate=item.decision_trace['legal_basis_runtime_trace']['candidate_articles'][0]
    assert candidate['same_contract_domain'] and candidate['relevance_score']>1.0

@pytest.fixture(scope='module')
def full_report():return upload()

def test_all_fifty_rules_have_explained_audit(full_report):
    assert len(full_report['items'])==50
    for item in full_report['items']:
        audit=item['decision_trace']['legal_basis_runtime_trace']['full_basis_audit']
        assert audit['status']=='REPORT_READY',(item['item_id'],audit)
        assert not audit['special_over_general_violation']
        assert not audit['weak_related_as_direct']
        assert audit['explanation']!='UNMAPPED'
        assert audit['legal_propositions']
    assert full_report['release_quality_gate']['status']=='REPORT_READY'

def test_full_report_preserves_protected_states(full_report):
    rows={i['item_id']:i for i in full_report['items']}
    for rid in ('D-01-02','D-01-03','D-02-03','D-07-01','D-07-02','D-08-03','D-09-04','D-11-02','COMMON-20-01','COMMON-21-01'):
        assert rows[rid]['coverage_status']=='通过'
    assert rows['D-04-04']['coverage_status']==rows['D-09-03']['coverage_status']=='不适用'
    assert rows['D-12-04']['coverage_status']=='部分覆盖'
