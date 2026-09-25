import pytest
from backend.tests.test_part_time_proportionate_coverage import review

@pytest.mark.parametrize('form,amount',[('DIRECT',1000),('DISPATCH',1500),('PART_TIME',800)])
def test_shared_charge_rule(monkeypatch,form,amount):
 q=f'单位从工资扣收{amount}元设备保证金，交回设备后退还。'
 text='劳动合同\n本条确认用工形式。\n'+q
 values=[('contract.employment_form',form,'本条确认用工形式。'),('worker.security_payment',dict(required=True,collector='EMPLOYER',nature='REFUNDABLE_SECURITY',deducted_from_wage=True,amount_text=str(amount)),q)]
 rows=review(monkeypatch,text,values)
 assert rows['EMP-DEPOSIT-01']['coverage_status']=='风险条款'
 if form=='PART_TIME':assert rows['PT-03-01']['coverage_status']!='风险条款'

@pytest.mark.parametrize('concept,value,quote',[
 ('social_insurance.employee_withheld',True,'依法代扣个人应缴社会保险费用。'),
 ('worker.damage_liability',dict(kind='ACTUAL_DAMAGE_COMPENSATION',basis='实际损失'),'损坏设备按实际损失处理。')])
def test_not_deposit(monkeypatch,concept,value,quote):
 rows=review(monkeypatch,'劳动合同\n'+quote,[(concept,value,quote)])
 assert rows['EMP-DEPOSIT-01']['coverage_status']=='通过'
 assert rows['EMP-14-01']['coverage_status']=='通过'

def test_unrelated_rule_ownership_blocks():
 from types import SimpleNamespace
 from backend.tests.test_employment_dispatch import store_for
 from review_v2.employment_fact_store import CURRENT
 from review_v2.employment_report_consistency import gate
 s=store_for('扣收设备押金。',[('worker.security_payment',dict(required=True,collector='EMPLOYER'),'扣收设备押金。')])
 token=CURRENT.set(s)
 try:
  item=SimpleNamespace(item_id='PT-03-01',node_id='employment_part_time_wage',coverage_status='风险条款',evidence_clauses=s.evidence(s.get('worker.security_payment'),'test'),decision_trace={})
  assert gate([item],'')['status']=='BLOCKED'
  item.node_id='employment_worker_charge'
  assert gate([item],'')['status']=='REPORT_READY'
 finally:CURRENT.reset(token)
