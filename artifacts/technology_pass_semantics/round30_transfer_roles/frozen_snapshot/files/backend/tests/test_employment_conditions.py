import pytest
from backend.tests.test_employment_dispatch import store_for
from backend.tests.test_employment_fact_pipeline import fact,packet,verified_packet
from review_v2.employment_fact_rules import adverse

@pytest.mark.parametrize('value,risk',[
 ({'consent':'REQUIRED','unilateral_position':False,'unilateral_pay_cut':False},False),
 ({'consent':'NOT_REQUIRED','unilateral_position':True,'position_scope':'BOUNDED','unilateral_pay_cut':False},False),
 ({'consent':'NOT_REQUIRED','unilateral_position':True,'position_scope':'ANY','unilateral_pay_cut':True,'salary_floor_percent':75},True),
 ({'consent':'NOT_REQUIRED','unilateral_position':True,'position_scope':'ANY','unilateral_pay_cut':True,'salary_floor_percent':90},True),
])
def test_change_policy(value,risk):
 s=store_for('岗位变更机制见本条。',[('job.change_terms',value,'岗位变更机制见本条。')])
 assert bool(adverse(s,'employment_work'))==risk

@pytest.mark.parametrize('value,risk',[
 ({'behavior':'MINOR_ATTENDANCE','automatic_serious':False,'immediate_dismissal':False},False),
 ({'behavior':'SUBSTANTIVE_SERIOUS','policy_basis':True,'automatic_serious':False,'immediate_dismissal':True},False),
 ({'behavior':'MINOR_ATTENDANCE','automatic_serious':True,'regardless_impact':True,'immediate_dismissal':True,'occurrence_threshold':7},True),
])
def test_discipline_proportionality(value,risk):
 s=store_for('违纪认定及处理见本条。',[('discipline.dismissal_terms',value,'违纪认定及处理见本条。')])
 assert bool(adverse(s,'employment_exit'))==risk
 assert not adverse(s,'employment_arbitrary_exit')

def test_final_report_keeps_evidence_and_deduplicates(monkeypatch):
 from review_v2 import employment_fact_pipeline as p
 from review_v2.engine import review_contract_v2
 from review_v2.clause_parser import parse_contract_clauses
 text='劳动合同\n双方直接建立固定期限劳动关系。\n公司不经同意可以调至任意岗位并降低报酬至原标准的七成。\n一年迟到五次不论情节均算严重违纪，可即时解雇并不支付补偿。'
 cs=parse_contract_clauses(text);fs=[fact(cs,k,v,q) for k,v,q in [
 ('contract.employment_form','DIRECT','双方直接建立固定期限劳动关系。'),('contract.type','FIXED','双方直接建立固定期限劳动关系。'),
 ('job.change_terms',{'consent':'NOT_REQUIRED','unilateral_position':True,'position_scope':'ANY','unilateral_pay_cut':True,'salary_floor_percent':70},'公司不经同意可以调至任意岗位并降低报酬至原标准的七成。'),
 ('discipline.dismissal_terms',{'behavior':'MINOR_ATTENDANCE','automatic_serious':True,'regardless_impact':True,'immediate_dismissal':True,'compensation_waived':True,'occurrence_threshold':5},'一年迟到五次不论情节均算严重违纪，可即时解雇并不支付补偿。')]]
 monkeypatch.setattr(p,'extract',lambda *a,**kw:packet(cs,fs));monkeypatch.setattr(p,'verify',verified_packet)
 r=review_contract_v2(text,'labor',use_llm=False);items={i['item_id']:i for i in r['items']}
 for key in ['EMP-04-01','EMP-10-01','EMP-16-01']:
  assert items[key]['coverage_status']=='风险条款'
  assert items[key]['evidence_clauses']
 assert not any(k.startswith(('PT-','DSP-','OET-')) for k in items)
 assert r['release_quality_gate']['status']=='REPORT_READY'
 assert r['risk_theme_count']<r['finding_count']
 assert '[支持：用人单位任意解除且免予补偿]' not in r['result']
 assert '[支持：违纪认定与直接解除条件过宽]' in r['result']
 assert r['release_quality_gate']['gate_results']['REPORT_TOPIC_LABEL_CONSISTENCY']=='PASS'

