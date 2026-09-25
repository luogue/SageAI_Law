import pytest
from backend.tests.test_employment_fact_pipeline import fact,packet,verified_packet
from review_v2.clause_parser import parse_contract_clauses
from review_v2.employment_fact_store import FactStore
from review_v2.fact_validation import FactExtractionError

@pytest.mark.parametrize('quote,amount', [('应支付违约金30万元。','30万元'),('违约金为损失的20%。','损失的20%')])
def test_positive_penalty(quote,amount):
 cs=parse_contract_clauses(quote)
 s=FactStore(quote,cs,packet(cs,[fact(cs,'penalties.obligations',{'scope':'CONFIDENTIALITY','imposed':True,'amount_text':amount},quote)]))
 assert s.facts[0]['normalized_value']['imposed'] is True

def test_false_obligation_rejected():
 text='未约定固定金额违约金。';cs=parse_contract_clauses(text)
 with pytest.raises(FactExtractionError,match='INVALID_OBLIGATION_POLARITY'):
  FactStore(text,cs,packet(cs,[fact(cs,'penalties.obligations',{'scope':'CONFIDENTIALITY','imposed':False},text)]))

@pytest.mark.parametrize('damage', [False,True])
def test_explicit_absence_final_report(monkeypatch,damage):
 from review_v2 import employment_fact_pipeline as p
 from review_v2.engine import review_contract_v2
 text='保密协议\n第一条\n乙方系甲方员工。\n第二条\n未约定固定金额违约金。造成损失的按实际损失赔偿。'
 cs=parse_contract_clauses(text)
 vals=[('nda.employment_relationship',True,'乙方系甲方员工。'),('penalties.exclusions',{'kind':'EXPLICIT_ABSENCE','scope':'固定金额违约金','basis':'未约定固定金额违约金'},'未约定固定金额违约金。')]
 if damage:vals.append(('worker.damage_liability',{'kind':'ACTUAL_DAMAGE_COMPENSATION','trigger':'造成损失','basis':'按实际损失赔偿'},'造成损失的按实际损失赔偿。'))
 monkeypatch.setattr(p,'extract',lambda *a,**k:packet(cs,[fact(cs,c,v,q) for c,v,q in vals]))
 monkeypatch.setattr(p,'verify',verified_packet)
 r=review_contract_v2(text,'confidentiality')
 row=next(i for i in r['items'] if i['item_id']=='EMP-14-01')
 assert row['coverage_status']!='风险条款'
 assert r['release_quality_gate']['status']=='REPORT_READY',r['release_quality_gate']
