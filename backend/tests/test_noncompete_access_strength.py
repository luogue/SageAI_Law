import pytest
from backend.tests.test_part_time_proportionate_coverage import review
from backend.tests.test_employment_fact_pipeline import fact,packet,verified_packet
from review_v2.employment_fact_store import FactStore
from review_v2.clause_parser import parse_contract_clauses
from review_v2.fact_verification import verified_store
from review_v2.fact_validation import FactExtractionError

@pytest.mark.parametrize('quote,concept,expected',[
 ('乙方可能接触商业秘密。','non_compete.access_capability','通过'),
 ('乙方岗位能够接触商业秘密。','non_compete.access_capability','通过'),
 ('乙方在工作中已实际接触客户底价、源代码等商业秘密。','non_compete.actual_access','通过'),
])
def test_access_strength_report(monkeypatch,quote,concept,expected):
 text='劳动合同\n约定乙方承担竞业限制。\n适用人员为软件工程师。\n竞业业务限于软件开发，地域为北京市。\n'+quote
 vals=[('non_compete.arrangement','EXISTS','约定乙方承担竞业限制。'),('non_compete.personnel','软件工程师','适用人员为软件工程师。'),('non_compete.businesses','软件开发','竞业业务限于软件开发，地域为北京市。'),('non_compete.territories','北京市','竞业业务限于软件开发，地域为北京市。'),(concept,True,quote)]
 rows=review(monkeypatch,text,vals);item=rows['NC-01-01']
 assert item['coverage_status']==expected
 actual=[e for e in item['coverage_elements'] if 'actual_access' in e['element_id']]
 assert not actual
 assert item['action_priority']=='NONE'

def test_capability_cannot_verify_actual():
 q='岗位有机会接触商业秘密。';cs=parse_contract_clauses(q)
 s=FactStore(q,cs,packet(cs,[fact(cs,'non_compete.actual_access',True,q)]));v=verified_packet(cs,s)
 v['verification']['checks'][0].update(supported=False,reason='可能接触不支持已经实际接触')
 with pytest.raises(FactExtractionError,match='CORE_FACT_VERIFICATION_FAILED'):verified_store(s,v)

def test_both_strengths_stay_distinct():
 q='岗位能够接触秘密。乙方已经掌握源代码。';cs=parse_contract_clauses('劳动合同\n第一条\n'+q)
 s=FactStore(q,cs,packet(cs,[fact(cs,'non_compete.access_capability',True,'岗位能够接触秘密。'),fact(cs,'non_compete.actual_access',True,'乙方已经掌握源代码。')]))
 assert s.get('non_compete.access_capability')[0]['fact_id']!=s.get('non_compete.actual_access')[0]['fact_id']
 assert s.get('non_compete.actual_access')[0]['evidence'][0]['quote']=='乙方已经掌握源代码。'

@pytest.mark.parametrize('gap', ['non_compete.personnel','non_compete.businesses','non_compete.territories'])
def test_contract_scope_gap_remains_defect(monkeypatch,gap):
 text='劳动合同\n双方约定竞业限制。\n人员为研发主管。\n业务限于软件开发。\n地域限于上海。'
 vals=[('non_compete.arrangement','EXISTS','双方约定竞业限制。'),('non_compete.personnel','研发主管','人员为研发主管。'),('non_compete.businesses','软件开发','业务限于软件开发。'),('non_compete.territories','上海','地域限于上海。')]
 removed=next(v for v in vals if v[0]==gap);text=text.replace(removed[2],'');vals.remove(removed)
 item=review(monkeypatch,text,vals)['NC-01-01']
 assert any(e['status']=='MISSING' for e in item['coverage_elements'])
 assert item['action_priority']!='NONE'

def test_explicit_denial_preserved(monkeypatch):
 text='劳动合同\n双方约定竞业限制。\n人员为研发主管。\n业务限于软件开发，地域限于上海。\n乙方从未接触相关商业秘密。'
 vals=[('non_compete.arrangement','EXISTS','双方约定竞业限制。'),('non_compete.personnel','研发主管','人员为研发主管。'),('non_compete.businesses','软件开发','业务限于软件开发，地域限于上海。'),('non_compete.territories','上海','业务限于软件开发，地域限于上海。'),('non_compete.actual_access',False,'乙方从未接触相关商业秘密。')]
 rows=review(monkeypatch,text,vals)
 for key in ('NC-01-01','NC-03-01'):
  assert rows[key]['decision_trace']['external_actual_access']['state']=='DENIED'
 assert rows['NC-01-01']['coverage_status']=='通过'
 assert rows['NC-03-01']['coverage_status']!='通过'
