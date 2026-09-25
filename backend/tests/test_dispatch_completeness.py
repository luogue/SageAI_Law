import pytest
from backend.tests.test_employment_dispatch import store_for
from review_v2.dispatch_assessment import position_state,pay_state,term_state

def store(values):return store_for('本条约定。',[(k,v,'本条约定。') for k,v in values])
@pytest.mark.parametrize('values,status',[
 ([('dispatch.long_term_position',True)],'VERIFY'),
 ([('dispatch.long_term_position',True),('dispatch.auxiliary_noncore',True),('dispatch.auxiliary_procedure',True)],'PASS'),
 ([('dispatch.position_basis','SUBSTITUTE')],'PASS'),
 ([('dispatch.long_term_position',True),('dispatch.auxiliary_noncore',False),('dispatch.substitute',False)],'RISK')])
def test_independent_position_bases(values,status):assert position_state(store(values))['status']==status

@pytest.mark.parametrize('own,other,comparable,status',[(None,9000,True,'VERIFY'),(7000,9000,False,'VERIFY'),(7000,9000,True,'RISK'),(9000,9000,True,'VERIFY')])
def test_two_sided_pay(own,other,comparable,status):
 values=[('dispatch.equal_pay','LOWER_ALLOWED'),('dispatch.comparable_work',comparable)]
 if own:values.append(('salary.regular',{'amount_text':str(own),'unit':'CNY/MONTH'}))
 if other:values.append(('dispatch.comparator_pay',{'amount_text':str(other),'unit':'CNY/MONTH'}))
 assert pay_state(store(values))['status']==status

@pytest.mark.parametrize('months,status',[(12,'RISK'),(24,'VERIFY'),(36,'VERIFY')])
def test_minimum_dispatch_contract(months,status):assert term_state(store([('contract.type','FIXED'),('contract.duration_months',months)]))['status']==status

def test_two_year_calendar_boundary():
 assert term_state(store([('contract.type','FIXED'),('contract.start_date','2026-01-01'),('contract.end_date','2027-12-31')]))['status']=='PASS'

def test_security_amount_and_cross_rule_display(monkeypatch):
 from review_v2 import employment_fact_pipeline as p
 from review_v2.engine import review_contract_v2
 from review_v2.clause_parser import parse_contract_clauses
 from backend.tests.test_employment_fact_pipeline import fact,packet,verified_packet
 text='劳动合同\n派遣劳动关系。\n正常工资每月七千元，以银行转账支付，每月十日发放。\n退回后拒绝任意岗位即可解除。\n收取可退保证金两千元，从工资扣除。'
 cs=parse_contract_clauses(text)
 values=[('contract.employment_form','DISPATCH','派遣劳动关系。'),
 ('termination.grounds',['拒绝任意岗位解除'],'退回后拒绝任意岗位即可解除。'),('termination.notice','解除通知','退回后拒绝任意岗位即可解除。'),
 ('dispatch.refusal_termination','ANY_OFFER','退回后拒绝任意岗位即可解除。'),
 ('worker.security_payment',dict(nature='REFUNDABLE_SECURITY',collector='AGENCY',required=True,deducted_from_wage=True,amount_text='两千元'),'收取可退保证金两千元，从工资扣除。')]
 monkeypatch.setattr(p,'extract',lambda *a,**k:packet(cs,[fact(cs,c,v,q) for c,v,q in values]));monkeypatch.setattr(p,'verify',verified_packet)
 r=review_contract_v2(text,'labor');rs={i['item_id']:i for i in r['items']}
 assert '2000元' in rs['EMP-06-01']['economic_impact']
 assert rs['EMP-10-01']['coverage_status']=='通过'
 assert rs['EMP-10-01']['decision_trace']['coverage_legality']['legality']=='RELATED_ADVERSE'
 section=r['result'].split('（EMP-10-01）')[1].split('\n## ')[0]
 assert '无需修改' not in section and 'DSP-06-01' in section
 assert rs['EMP-17-01']['coverage_status']=='缺失'
 assert r['release_quality_gate']['status']=='REPORT_READY', str(r['release_quality_gate'].get('failures'))


def test_comparison_binds_both_wages_and_comparability():
 from review_v2.employment_dispatch import adverse
 text='正式月报酬七千元。对照岗位月报酬九千元。双方为相同岗位和计酬口径。'
 s=store_for(text,[('salary.regular',{'amount_text':'七千','unit':'CNY/MONTH'},'正式月报酬七千元。'),
 ('dispatch.comparator_pay',{'amount_text':'九千','unit':'CNY/MONTH'},'对照岗位月报酬九千元。'),
 ('dispatch.comparable_work',True,'双方为相同岗位和计酬口径。')])
 rows=adverse(s,'employment_dispatch_equal_pay')
 assert {s.by_id[r['structured_fact_id']]['concept'] for r in rows}=={'salary.regular','dispatch.comparator_pay','dispatch.comparable_work'}
 assert len({r['quote'] for r in rows})==3

@pytest.mark.parametrize('regular,expected',[(True,'通过'),(False,'部分覆盖')])
def test_remuneration_is_independent_of_probation(monkeypatch,regular,expected):
 from review_v2 import employment_fact_pipeline as p
 from review_v2.engine import review_contract_v2
 from review_v2.clause_parser import parse_contract_clauses
 from backend.tests.test_employment_fact_pipeline import fact,packet,verified_packet
 text='劳动合同\n负责人林某，劳动者住在西城区。\n试用月薪五千元。\n正式月薪六千元。\n每月八日通过银行付款。'
 cs=parse_contract_clauses(text)
 values=[('identity.employer_representative','林某','负责人林某，劳动者住在西城区。'),('identity.worker_address','西城区','负责人林某，劳动者住在西城区。'),
 ('probation.salary',{'amount_text':'五千','unit':'CNY/MONTH'},'试用月薪五千元。'),
 ('salary.payment_date','每月八日','每月八日通过银行付款。'),('salary.payment_method','BANK','每月八日通过银行付款。')]
 if regular:values.append(('salary.regular',{'amount_text':'六千','unit':'CNY/MONTH'},'正式月薪六千元。'))
 monkeypatch.setattr(p,'extract',lambda *a,**k:packet(cs,[fact(cs,c,v,q) for c,v,q in values]))
 monkeypatch.setattr(p,'verify',verified_packet)
 r=review_contract_v2(text,'labor');rs={i['item_id']:i for i in r['items']}
 assert rs['EMP-17-01']['coverage_status']==expected
 covered={e['element_id'] for e in rs['EMP-01-01']['coverage_elements'] if e['status']=='COVERED'}
 assert {'employment_identity_3','employment_identity_4'}<=covered
 assert r['release_quality_gate']['status']=='REPORT_READY',str(r['release_quality_gate']['failures'])


def test_stale_pass_display_is_blocked():
 from types import SimpleNamespace
 from review_v2.employment_report_consistency import gate
 item=SimpleNamespace(item_id='R-1',node_id='employment_exit',coverage_status='通过',decision_trace={'coverage_legality':{'message':'形式已覆盖但须处理关联风险'}})
 assert gate([item],'## 项目（R-1）\n已覆盖，无需修改')['status']=='BLOCKED'
 assert gate([item],'## 项目（R-1）\n形式已覆盖但须处理关联风险')['status']=='REPORT_READY'


def test_different_pay_system_is_not_lower_pay():
 s=store([('dispatch.equal_pay','DIFFERENT_SYSTEM')])
 assert pay_state(s)['status']=='VERIFY'


def test_different_wage_components_are_not_directly_compared():
 s=store([('salary.regular',{'amount_text':'7200','unit':'CNY/MONTH','component':'TOTAL'}),
 ('dispatch.comparator_pay',{'amount_text':'8800','unit':'CNY/MONTH','component':'BASE'}),('dispatch.comparable_work',True)])
 assert pay_state(s)['status']=='VERIFY'


def test_short_labor_term_binds_labor_not_dispatch_period():
 from review_v2.employment_dispatch import adverse
 s=store([('contract.type','FIXED'),('contract.duration_months',18),('dispatch.period','派遣三年')])
 rows=adverse(s,'employment_dispatch_identity')
 assert rows
 assert {s.by_id[r['structured_fact_id']]['concept'] for r in rows}=={'contract.type','contract.duration_months'}
