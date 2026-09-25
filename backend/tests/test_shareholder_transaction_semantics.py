from copy import deepcopy
from pathlib import Path
from types import SimpleNamespace
import pytest
from review_v2.clause_parser import parse_contract_clauses as parse
from review_v2.shareholder_transaction_facts import transaction_facts, protection_polarity, source_consistency_failures, consistency
from review_v2.company_formation_checklist import COMPANY_FORMATION_CHECKLIST
from review_v2.priority_contract_review import applicability
from review_v2.priority_checklist_helpers import PROFILES
from review_v2.lease_semantics import corpus_facts, supports


@pytest.mark.parametrize('asset',['租赁权益','知识产权','股权','债权','土地使用权','房屋相关权益','可转让的其他财产权利'])
def test_nonmonetary_property_structure(asset):
    text=f'甲方以其{asset}作价人民币37万元出资成立公司。'
    checkpoint=next(c for c in COMPANY_FORMATION_CHECKLIST if c.item_id=='CF-03-01')
    assert applicability(text,checkpoint,'shareholders')[0]


@pytest.mark.parametrize('arrangement',[
    '各股东认购款汇入甲方银行账号，户名：张三。',
    '投资款支付给发起人。',
    '认购款支付至股东账户。',
    '甲方：张三，身份证号略。\n出资款汇入甲方银行账号。',
])
def test_personal_recipient(arrangement):
    assert any(f['fact_type']=='personal_subscription_account' for f in transaction_facts(arrangement))


@pytest.mark.parametrize('arrangement',[
    '甲方对任何表决事项具有一票否决权。',
    '借款、担保、资产处置由乙方自行决定，无须提交股东会。',
    '重大采购由丙方审批后生效。',
])
def test_reserved_control(arrangement):
    checkpoint=next(c for c in COMPANY_FORMATION_CHECKLIST if c.item_id=='CF-12-01')
    assert applicability(arrangement,checkpoint,'shareholders')[0]


@pytest.mark.parametrize('text,polarity',[
    ('股东有权查阅公司账簿。','POSITIVE'),
    ('股东查阅账簿应提前通知公司。','NEUTRAL'),
    ('股东经甲方同意后方可查阅账簿。','RESTRICTIVE'),
    ('其他股东不得查阅公司账簿。','ADVERSE'),
])
def test_inspection_polarity(text,polarity):
    assert protection_polarity(text)['polarity']==polarity
    e=PROFILES['formation_governance'][3]
    facts=corpus_facts(parse(text),[e])
    assert bool(facts[e['element_id']]) is (polarity=='POSITIVE')


def test_scope_same_clause_different_property():
    assert not any(f['fact_type']=='unilateral_reserved_decision' for f in transaction_facts('甲方审批日常办公用品。'))
    assert not any(f['fact_type']=='personal_subscription_account' for f in transaction_facts('认购款汇入公司银行账户，户名：明朗有限公司。'))
    assert not any(f['fact_type']=='nonmonetary_contribution' for f in transaction_facts('甲方以现金出资。公司另行采购设备。'))


@pytest.fixture(scope='module')
def production():
    from fastapi import FastAPI
    from fastapi.testclient import TestClient
    from routers import review_v2 as route
    app=FastAPI();app.include_router(route.router)
    app.dependency_overrides[route.get_current_user]=lambda:{'id':'shareholder-source-semantics'}
    source=Path(__file__).resolve().parents[2]/'test_data'/'86 股东协议.docx'
    original=source.read_bytes()
    with TestClient(app) as client:
        response=client.post('/review-v2/file',data={'contract_type':'investment','use_llm':'false','include_low_risk':'true'},files={'file':(source.name,original,'application/vnd.openxmlformats-officedocument.wordprocessingml.document')})
    assert response.status_code==200
    assert source.read_bytes()==original
    return response.json()


def test_same_document_all_requested_assertions(production):
    r=production; d={i['item_id']:i for i in r['items']}
    assert r['release_quality_gate']['status']=='REPORT_READY',r['release_quality_gate']['failures']
    assert r['contract_type']=='shareholders'
    assert not any(i['node_id'].startswith('sale_') for i in r['items'])
    for key in ['CF-03-01','CF-04-01','CF-12-01']:
        assert d[key]['applicability']['status']=='APPLICABLE'
    for key in ['CF-01-01','CF-05-01','CF-08-01','CF-12-01','COMMON-23-01','COMMON-24-01']:
        assert d[key]['coverage_status']=='风险条款'
    for fact in ['110%','110万元','戊方','2034-09-30','2031-06-30']:
        assert fact in d['CF-01-01']['risk_point_description']
    for key,element in [('CF-02-01','formation_contributions_3'),('COMMON-26-01','common_contract_termination_1'),('CF-10-01','formation_articles_alignment_2')]:
        assert next(a for a in d[key]['decision_trace']['element_absence_searches'] if a['element_id']==element)['result']=='FOUND'
    assert not any(e['element_id']=='formation_transfer_exit_3' for e in d['CF-09-01']['coverage_elements'])
    assert '查账' in d['CF-05-01']['risk_point_description']
    assert '凭证' in d['CF-08-01']['risk_point_description']
    assert '直接实际损失' in d['COMMON-23-01']['risk_point_description']


@pytest.mark.parametrize('kind',['applicability','search','polarity'])
def test_semantic_corruption_remains_blocked(production,kind):
    from review_v2.engine import _combine_quality_gates
    d={i['item_id']:deepcopy(i) for i in production['items']}
    if kind=='applicability':
        item=d['CF-03-01'];item['coverage_status']='不适用';item['applicability']['status']='NOT_APPLICABLE'
        expected='SOURCE_FACT_APPLICABILITY_CONFLICT'
    elif kind=='search':
        item=d['CF-02-01']
        next(a for a in item['decision_trace']['element_absence_searches'] if a['element_id']=='formation_contributions_3')['result']='NOT_FOUND'
        expected='SOURCE_FACT_SEARCH_AUDIT_CONFLICT'
    else:
        item=d['CF-05-01'];e=deepcopy(PROFILES['formation_governance'][3])
        item['decision_trace']['semantic_requirements']=[e]
        item['evidence_clauses']=[{'clause_id':'C1','location':'第八条','text':'股东经甲方同意后方可查阅账簿。','polarity':'POSITIVE','supports_element_ids':[e['element_id']]}]
        assert not supports(e,item['evidence_clauses'][0])
        expected='RESTRICTIVE_EVIDENCE_AS_POSITIVE_COVERAGE'
    failures=source_consistency_failures([SimpleNamespace(**item)])
    assert expected in {f['requirement'] for f in failures}
    assert _combine_quality_gates({'status':'BLOCKED','failures':failures})['status']=='BLOCKED'
