import pytest
from backend.tests.test_employment_dispatch import store_for
from backend.tests.test_employment_fact_pipeline import fact,packet,verified_packet
from review_v2.employment_conditions import onward_risk,return_risk

@pytest.mark.parametrize('actor,entity,procedure,expected',[
 ('HOST','OTHER_ENTITY','HOST_DIRECT_CONTINUATION',True),('HOST','SAME_ENTITY','HOST_DIRECT_CONTINUATION',False),
 ('AGENCY','OTHER_ENTITY','AGENCY_NEW_ARRANGEMENT',False),('HOST','UNCERTAIN','HOST_DIRECT_CONTINUATION',False)])
def test_entity_transition(actor,entity,procedure,expected):
 assert onward_risk(dict(actor=actor,recipient_relation=entity,procedure=procedure,permitted=True,agency='派遣方',host='接收方',recipient='新接收方'))==expected

@pytest.mark.parametrize('kind,basis,expected',[
 ('ORDINARY_PERFORMANCE','REASON_ALONE',True),('SUBJECTIVE_MISMATCH','REASON_ALONE',True),('ORGANIZATION_CHANGE','REASON_ALONE',True),
 ('ORDINARY_PERFORMANCE','STATUTORY_CONDITIONED',False),('SERIOUS_MISCONDUCT','STATUTORY_CONDITIONED',False),('ORGANIZATION_CHANGE','STATUTORY_CONDITIONED',False)])
def test_return_grounds(kind,basis,expected):
 assert return_risk(dict(disposition="ALLOWED_RETURN_REASON",reason_type=kind,basis=basis,threshold=47))==expected

def test_refundable_security_not_penalty():
 s=store_for('工资扣收的可退还押金。',[('worker.security_payment',dict(nature='REFUNDABLE_SECURITY',collector='AGENCY',required=True,deducted_from_wage=True,amount_text='900元'),'工资扣收的可退还押金。')])
 assert s.adverse('employment_wage') and s.adverse('employment_dispatch_charges')
 assert not s.adverse('employment_general_penalty')

def test_dispatch_final_report(monkeypatch):
 from review_v2 import employment_fact_pipeline as p
 from review_v2.engine import review_contract_v2
 from review_v2.clause_parser import parse_contract_clauses
 text='劳动合同\n派遣方招用员工交由接收方使用。\n接收方直接送员工到其他独立企业工作，视为原安排继续。\n接收方认为不适合即可退回。\n派遣方收取可退押金九百元，并从工资扣收。'
 cs=parse_contract_clauses(text)
 values=[('contract.employment_form','DISPATCH','派遣方招用员工交由接收方使用。'),
 ('dispatch.onward_assignment',dict(actor='HOST',recipient_relation='OTHER_ENTITY',procedure='HOST_DIRECT_CONTINUATION',permitted=True,agency='派遣方',host='接收方',recipient='其他独立企业'),'接收方直接送员工到其他独立企业工作，视为原安排继续。'),
 ('dispatch.return_terms',dict(disposition='ALLOWED_RETURN_REASON',reason='不适合',reason_type='SUBJECTIVE_MISMATCH',basis='REASON_ALONE'),'接收方认为不适合即可退回。'),
 ('worker.security_payment',dict(nature='REFUNDABLE_SECURITY',collector='AGENCY',required=True,deducted_from_wage=True,amount_text='九百元'),'派遣方收取可退押金九百元，并从工资扣收。')]
 monkeypatch.setattr(p,'extract',lambda *a,**k:packet(cs,[fact(cs,c,v,q) for c,v,q in values]));monkeypatch.setattr(p,'verify',verified_packet)
 r=review_contract_v2(text,'labor');items={i['item_id']:i for i in r['items']}
 for k in ['DSP-09-01','DSP-10-01','DSP-05-01','EMP-06-01']:assert items[k]['coverage_status']=='风险条款'
 assert items['EMP-14-01']['coverage_status']!='风险条款'
 themes=[t for t in r['risk_themes'] if 'DSP-05-01' in t['related_rule_ids']]
 assert len(themes)==1 and 'EMP-06-01' in themes[0]['related_rule_ids']
 assert r['release_quality_gate']['status']=='REPORT_READY'
