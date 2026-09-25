from pathlib import Path
import pytest
from review_v2.formation_rule_semantics import deadline_assessment,transfer_assessment,account_context
from review_v2.clause_parser import parse_contract_clauses as parse
from review_v2.company_formation_checklist import COMPANY_FORMATION_CHECKLIST
from review_v2.priority_contract_review import judge

def checkpoint(node):
    return next(c for c in COMPANY_FORMATION_CHECKLIST if c.node_id==node)

@pytest.mark.parametrize('text,present,compliant,status',[
    ('有限责任公司2026年设立。认缴出资2030年前缴足。',True,True,'PASS'),
    ('有限责任公司2026年设立。认缴出资2035年缴足。',True,False,'RISK'),
    ('有限责任公司2026年设立。认缴期限另行确定。',False,None,'MISSING'),
    ('有限责任公司认缴出资2035年缴足。',True,None,'UNKNOWN'),
    ('有限责任公司2026年1月31日成立。认缴出资2031年1月31日前缴足。',True,True,'PASS'),
    ('有限责任公司2026年1月31日成立。认缴出资2031年2月1日前缴足。',True,False,'RISK'),
    ('有限责任公司2018年成立。认缴出资2035年缴足。',True,None,'UNKNOWN'),
    ('认缴出资自公司成立之日起五年内缴足。',True,True,'PASS'),
    ('认缴出资自公司成立之日起八年内缴足。',True,False,'RISK'),
])
def test_deadline_presence_separate_from_legality(text,present,compliant,status):
    a=deadline_assessment(text)
    assert a['contribution_deadline_present'] is present
    assert a['contribution_deadline_compliant'] is compliant
    assert a['status']==status
    from review_v2.priority_checklist_helpers import PROFILES
    from review_v2.lease_semantics import corpus_facts
    e=PROFILES['formation_contributions'][2]
    assert bool(corpus_facts(parse(text),[e])[e['element_id']]) is present

MODERN='股东对外转让股权，应将数量、价格、支付方式和期限书面通知其他股东。其他股东同等条件下享有优先购买权，接到通知后三十日内未答复视为放弃优先购买权。'
OLD='股东向股东以外的人转让出资必须经过其他股东过半数同意。'

def test_old_transfer_is_risk_with_source():
    j=judge(checkpoint('formation_transfer_exit'),parse(OLD))
    assert j.coverage_status=='风险条款'
    assert '不直接认定' in j.risk_point_description
    assert OLD.rstrip('。') in j.evidence_clauses[0]['text']

def test_modern_transfer_complete():
    assert judge(checkpoint('formation_transfer_exit'),parse(MODERN)).coverage_status=='通过'

def test_charter_specific_not_automatically_invalid():
    text=OLD+'公司章程明确规定对外转让需要过半数同意。'+MODERN
    assert transfer_assessment(text)['status']=='CHARTER_VERIFICATION'
    j=judge(checkpoint('formation_transfer_exit'),parse(text))
    assert j.coverage_status!='风险条款'
    assert '核验有效章程' in j.risk_point_description

def test_preemption_alone_partial():
    assert judge(checkpoint('formation_transfer_exit'),parse('股权转让时其他股东有优先购买权。')).coverage_status=='部分覆盖'

ACCOUNT='各股东认购款汇入个人账户，户名：王海。'
PROTECTION='资金与个人财产隔离，不得挪用。各项支出双人审批。设立后10日内转入公司账户并核对。公司设立失败返还认购款并结算费用。'

def test_personal_account_is_context_only():
    c=account_context(ACCOUNT)
    assert c['personal_account_receiver_identified']
    assert all(r['polarity']=='NEUTRAL' and not r['protective_coverage'] for r in c['evidence'])
    j=judge(checkpoint('formation_fund_safety'),parse(ACCOUNT))
    assert j.coverage_status=='缺失'
    assert '不证明资金安全保护已覆盖' in j.risk_point_description

def test_actual_account_protections_cover():
    j=judge(checkpoint('formation_fund_safety'),parse(ACCOUNT+PROTECTION))
    assert j.coverage_status=='通过'
    assert all('户名' not in r['text'] for r in j.evidence_clauses)

def test_identical_document_real_production():
    from fastapi import FastAPI
    from fastapi.testclient import TestClient
    from routers import review_v2 as route
    app=FastAPI();app.include_router(route.router)
    app.dependency_overrides[route.get_current_user]=lambda:{'id':'rule-semantics'}
    file=Path(__file__).resolve().parents[2]/'test_data'/'86 股东协议.docx'
    original=file.read_bytes()
    with TestClient(app) as client:
        response=client.post('/review-v2/file',data={'contract_type':'investment','use_llm':'false','include_low_risk':'true'},files={'file':(file.name,original,'application/vnd.openxmlformats-officedocument.wordprocessingml.document')})
    assert response.status_code==200
    r=response.json();d={i['item_id']:i for i in r['items']}
    assert r['release_quality_gate']['status']=='REPORT_READY',r['release_quality_gate']['failures']
    assert file.read_bytes()==original
    a=d['CF-02-01']['decision_trace']['contribution_deadline_assessment']
    assert a['contribution_deadline_present'] and a['contribution_deadline_compliant'] is False
    assert next(a for a in d['CF-02-01']['decision_trace']['element_absence_searches'] if a['element_id']=='formation_contributions_3')['result']=='FOUND'
    assert d['CF-16-01']['coverage_status']=='风险条款'
    assert d['CF-09-01']['coverage_status']=='风险条款'
    assert '旧式过半数同意' in d['CF-09-01']['risk_point_description']
    assert not any(e['element_id']=='formation_fund_safety_1' for e in d['CF-04-01']['coverage_elements'])
    assert d['CF-04-01']['decision_trace']['fund_receiver_context']['personal_account_receiver_identified']
    section=r['result'].split('（CF-04-01）',1)[1].split('\n## ',1)[0]
    assert '【触发证据，不计入保护覆盖】' in section
    assert '户名：黄志远' in section
    assert '已覆盖：临时账户户名' not in section
    suggestion=checkpoint('formation_deadline_legality').suggested_clause
    assert '保留已经约定的缴付日期' not in r['result']
    assert '保留明确约定出资缴付期限的条款结构' in suggestion
    assert '调整具体缴付截止日期' in suggestion
    for heading in ['二、核心风险摘要','三、建议优先修改','25. 认缴期限法定上限及成立日核验（CF-16-01）']:
        section=r['result'].split(heading,1)[1].split('\n## ',1)[0]
        assert suggestion in section

