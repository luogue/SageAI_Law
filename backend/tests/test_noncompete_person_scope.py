import os
import pytest
from backend.tests.test_employment_fact_pipeline import fact, packet, verified_packet
from review_v2.clause_parser import parse_contract_clauses

@pytest.mark.parametrize('subject,defined', [('乙方',True),('公司核心技术人员',True),('相关人员',False)])
@pytest.mark.parametrize('actual',[None,True,False])
def test_final_scope_independent_of_eligibility(monkeypatch,subject,defined,actual):
 from review_v2 import employment_fact_pipeline as p
 from review_v2.engine import review_contract_v2
 q=subject+'离职后不得从事数据库软件业务。'
 text='竞业协议\n第一条\n甲方：安城公司。乙方：李某。\n'+q+'\n第二条\n地域限于杭州。竞业期限十八个月。每月按离职前平均工资30%补偿。'
 vals=[('non_compete.arrangement','EXISTS',q),('non_compete.businesses',['数据库软件'],q),('non_compete.territories',['杭州'],'地域限于杭州。'),('non_compete.duration_months',18,'竞业期限十八个月。'),('non_compete.compensation',{'formula':{'kind':'PERCENT_OF_BASE','percent':30,'base':'PREVIOUS_AVERAGE_SALARY'},'unit':'CNY/MONTH'},'每月按离职前平均工资30%补偿。')]
 if defined:vals.append(('non_compete.person_scope',subject,q))
 if actual is not None:
  a='劳动者已实际接触数据库源代码。' if actual else '劳动者从未接触相关商业秘密。'
  text+='\n第三条\n'+a;vals.append(('non_compete.actual_access',actual,a))
 cs=parse_contract_clauses(text)
 monkeypatch.setattr(p,'extract',lambda *a,**kw:packet(cs,[fact(cs,c,v,q) for c,v,q in vals]))
 monkeypatch.setattr(p,'verify',verified_packet)
 r=review_contract_v2(text,'non_compete');rows={i['item_id']:i for i in r['items']}
 assert rows['NC-01-01']['coverage_status']==('通过' if defined else '部分覆盖')
 assert rows['NC-02-01']['coverage_status']=='通过'
 if defined and actual is not True:
  assert rows['NC-01-01']['action_priority']=='NONE'
  assert rows['NC-03-01']['coverage_status']=='待核验'
  assert r['structured_fact_debug']['noncompete_person']['person_eligibility']=='NEED_REVIEW'
 assert r['release_quality_gate']['status']=='REPORT_READY'

@pytest.mark.skipif(os.getenv('RUN_DEEPSEEK_REGRESSION')!='1',reason='live model regression')
@pytest.mark.parametrize('text,exists',[
 ('乙方离职后不得从事竞业行为。',True),
 ('公司核心技术人员离职后不得加入竞争企业。',True),
 ('相关人员应承担竞业义务。',False),
])
def test_live_subject_identification(text,exists):
 from review_v2.deepseek_facts import extract,verify
 from review_v2.employment_fact_store import FactStore
 from review_v2.fact_verification import verified_store
 source='协议\n甲方为安城公司，乙方为李某。\n第一条\n'+text
 cs=parse_contract_clauses(source)
 raw=extract(cs,concept_keys=['non_compete.arrangement','non_compete.person_scope','non_compete.person_eligibility','non_compete.actual_access'])
 s=FactStore(source,cs,raw);s=verified_store(s,verify(cs,s))
 assert bool(s.get('non_compete.person_scope')) is exists
 assert not s.get('non_compete.actual_access')
 from review_v2.noncompete_semantics import person_assessment
 assert person_assessment(s)['person_eligibility']=='NEED_REVIEW'
