import pytest
from backend.tests.test_employment_fact_pipeline import fact,packet,verified_packet
from backend.tests.test_part_time_proportionate_coverage import review
from review_v2.clause_parser import parse_contract_clauses
from review_v2.employment_fact_store import FactStore
from review_v2.fact_verification import verified_store
from review_v2.fact_validation import FactExtractionError

@pytest.mark.parametrize('quote,kind',[
 ('设备损坏按实际损失赔偿。','ACTUAL_DAMAGE_COMPENSATION'),
 ('依法承担赔偿责任。','STATUTORY_LIABILITY'),
])
def test_non_penalty_liability(monkeypatch,quote,kind):
 rows=review(monkeypatch,'劳动合同\n'+quote,[('worker.damage_liability',{'kind':kind,'basis':quote},quote)])
 assert rows['EMP-14-01']['coverage_status']=='通过'

@pytest.mark.parametrize('quote,scope,amount',[
 ('损坏设备应赔偿固定金额八百元。','PROPERTY_DAMAGE','八百元'),
 ('每迟延一日支付一百元违约金。','ORDINARY_DISCIPLINE','每日一百元'),
])
def test_fixed_liability_remains_risk(monkeypatch,quote,scope,amount):
 rows=review(monkeypatch,'劳动合同\n'+quote,[('penalties.obligations',{'scope':scope,'amount_text':amount,'imposed':True},quote)])
 assert rows['EMP-14-01']['coverage_status']=='风险条款'


def test_deposit_and_actual_damage_are_separate(monkeypatch):
 q='从首次工资中扣收八百元设备保证金，归还设备后退还。'
 loss='因故意或重大过失损坏设备，按实际损失依法处理。'
 text='非全日制劳动合同\n双方建立非全日制用工。\n第九条 设备\n'+q+'\n'+loss
 values=[('contract.employment_form','PART_TIME','双方建立非全日制用工。'),('worker.security_payment',{'nature':'REFUNDABLE_SECURITY','collector':'EMPLOYER','required':True,'deducted_from_wage':True,'amount_text':'八百元'},q),('worker.damage_liability',{'kind':'ACTUAL_DAMAGE_COMPENSATION','basis':loss},loss)]
 rows=review(monkeypatch,text,values)
 assert rows['EMP-DEPOSIT-01']['coverage_status']=='风险条款'
 assert rows['EMP-14-01']['coverage_status']=='通过'
 assert any(q==e.get('quote') for e in rows['EMP-DEPOSIT-01']['evidence_clauses'])


def test_verifier_rejection_cannot_become_pass():
 text='故意损坏按实际损失处理。';cs=parse_contract_clauses(text)
 s=FactStore(text,cs,packet(cs,[fact(cs,'penalties.obligations',{'scope':'PROPERTY_DAMAGE','imposed':True,'amount_text':'800'},text)]))
 p=verified_packet(cs,s);p['verification']['checks'][0].update(supported=False,reason='原文无固定金额，错误借用其他义务金额')
 with pytest.raises(FactExtractionError,match='CORE_FACT_VERIFICATION_FAILED'):verified_store(s,p)
