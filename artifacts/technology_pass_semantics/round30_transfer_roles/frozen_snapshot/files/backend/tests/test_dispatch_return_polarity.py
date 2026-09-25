import pytest
from backend.tests.test_employment_dispatch import store_for
from backend.tests.test_employment_fact_pipeline import fact,packet,verified_packet
from review_v2.employment_conditions import normalize,return_risk

@pytest.mark.parametrize('quote,polarity,risk',[
 ('绩效低于80分可以退回。','ALLOWED_RETURN_REASON',True),
 ('不得仅因绩效低于80分退回。','PROHIBITED_RETURN_REASON',False),
 ('绩效低于80分不当然构成退回事由。','PROHIBITED_RETURN_REASON',False),
 ('法律规定可以退回的情形。','LEGAL_REFERENCE_ONLY',False),
 ('不能仅凭协作评分不足退回。','PROHIBITED_RETURN_REASON',False)])
def test_verified_return_polarity(quote,polarity,risk):
 v={'disposition':polarity,'reason':quote}
 if polarity=='ALLOWED_RETURN_REASON':v.update(reason_type='ORDINARY_PERFORMANCE',basis='REASON_ALONE')
 s=store_for(quote,[('dispatch.return_terms',v,quote)])
 assert bool(s.adverse('employment_dispatch_return_basis'))==risk
 assert return_risk(normalize('dispatch.return_terms',v))==risk

@pytest.mark.parametrize('retry_fails',[False,True])
def test_targeted_correction_preserves_other_concepts(monkeypatch,retry_fails):
 from review_v2 import employment_fact_pipeline as p
 from review_v2.fact_validation import FactExtractionError
 text='劳动合同\n派遣单位雇佣后派至用工单位。\n可以因普通评分过低退回，但不得仅因不合群退回。\n每月五日支付工资。'
 scopes=[];calls=[]
 def extract(cs,**kw):
  scopes.append(kw.get('concept_keys'))
  quote='可以因普通评分过低退回，但不得仅因不合群退回。'
  values=[('contract.employment_form','DISPATCH','派遣单位雇佣后派至用工单位。'),('dispatch.return_terms',{'disposition':'ALLOWED_RETURN_REASON','reason':'普通评分过低','reason_type':'ORDINARY_PERFORMANCE','basis':'REASON_ALONE'},quote),
   ('dispatch.return_terms',{'disposition':'ALLOWED_RETURN_REASON' if len(scopes)==1 or retry_fails else 'PROHIBITED_RETURN_REASON','reason':'不合群'},quote)]
  if not kw.get('concept_keys'):values.append(('salary.payment_date','每月五日','每月五日支付工资。'))
  raw=packet(cs,[fact(cs,c,v,q) for c,v,q in values])
  if kw.get('concept_keys'):
   raw[0]['response']['coverage']={k:v for k,v in raw[0]['response']['coverage'].items() if k in kw['concept_keys']}
  return raw
 def verify(cs,s):
  calls.append(s)
  r=verified_packet(cs,s)
  for c in r['verification']['checks']:
   f=s.by_id[c['fact_id']]
   if f['concept']=='dispatch.return_terms' and f['normalized_value']['reason']=='不合群' and f['normalized_value']['disposition']=='ALLOWED_RETURN_REASON':
    c.update(supported=False,reason='原文禁止以此退回，候选极性相反',error_type='POLARITY_CONFLICT')
  return r
 monkeypatch.setattr(p,'extract',extract);monkeypatch.setattr(p,'verify',verify)
 if retry_fails:
  with pytest.raises(FactExtractionError,match='CORE_FACT_VERIFICATION_FAILED'):p.run(text,'labor',lambda *a,**k:None)
 else:
  from review_v2.engine import _review_contract_v2_legacy
  r=p.run(text,'labor',_review_contract_v2_legacy)
  assert len(calls[-1].get('dispatch.return_terms'))==2
  assert calls[-1].get('salary.payment_date')
  assert r['release_quality_gate']['status']=='REPORT_READY'
 assert scopes==[None,['contract.employment_form','dispatch.return_terms','non_compete.arrangement']]

@pytest.mark.parametrize('value',[
 {'reason':'评分不足','basis':'REASON_ALONE'},
 {'disposition':'PROHIBITED_RETURN_REASON','reason':'评分不足','basis':'REASON_ALONE'},
 {'disposition':'LEGAL_REFERENCE_ONLY','basis':'STATUTORY_CONDITIONED'}])
def test_ambiguous_or_conflicting_polarity_blocked(value):
 from review_v2.fact_validation import FactExtractionError
 with pytest.raises(FactExtractionError):normalize('dispatch.return_terms',value)


def test_same_quote_addition_cannot_hide_rejected_fact():
 from review_v2.fact_verification import verified_store
 from review_v2.clause_parser import parse_contract_clauses
 from review_v2.employment_fact_store import FactStore
 from review_v2.fact_validation import FactExtractionError
 text='不得因不合群退回，但可依法退回。';cs=parse_contract_clauses(text)
 bad=fact(cs,'dispatch.return_terms',{'disposition':'ALLOWED_RETURN_REASON','reason':'不合群'},text)
 s=FactStore(text,cs,packet(cs,[bad]));v=verified_packet(cs,s)
 v['verification']['checks'][0]['supported']=False
 good=fact(cs,'dispatch.return_terms',{'disposition':'PROHIBITED_RETURN_REASON','reason':'不合群'},text)
 v['verification']['additional_facts']=[good]
 with pytest.raises(FactExtractionError,match='CORE_FACT_VERIFICATION_FAILED'):verified_store(s,v)
 good['corrects_fact_id']=s.facts[0]['fact_id']
 assert verified_store(s,v).get('dispatch.return_terms')[0]['normalized_value']['disposition']=='PROHIBITED_RETURN_REASON'


def test_prohibited_fee_keeps_negative_boolean():
 s=store_for('派遣方不得收费。',[('worker.security_payment',{'collector':'AGENCY','required':False},'派遣方不得收费。')])
 assert not s.adverse('employment_dispatch_charges')
 assert s.get('worker.security_payment')[0]['normalized_value']['required'] is False
