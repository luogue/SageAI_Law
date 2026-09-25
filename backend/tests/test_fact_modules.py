import pytest
from review_v2.fact_modules import select
from review_v2.employment_fact_schema import CONCEPTS
from backend.tests.test_employment_fact_pipeline import packet,verified_packet
from review_v2.employment_fact_store import FactStore
from review_v2.fact_verification import verified_store
from review_v2.clause_parser import parse_contract_clauses

def test_nda_scope_and_verification():
 keys=select(CONCEPTS,[], 'confidentiality')
 assert not any(k.startswith(('dispatch.','part_time.','salary.')) for k in keys)
 assert 'nda.information_flow' in keys
 assert 'penalties.obligations' in keys
 text='保密协议';cs=parse_contract_clauses(text);raw=packet(cs,[])
 raw[0]['active_concepts']=keys;raw[0]['response']['coverage']={k:'ABSENT' for k in keys}
 s=FactStore(text,cs,raw);v=verified_packet(cs,s);v['verification']['searched_concepts']=keys
 s=verified_store(s,v)
 assert s.coverage['dispatch.comparator_pay']=='NOT_APPLICABLE'
 assert s.coverage['nda.information_flow']=='ABSENT'
 assert not s.facts

@pytest.mark.parametrize('form,prefix',[('DISPATCH','dispatch.'),('PART_TIME','part_time.')])
def test_relationship_loads_module(form,prefix):
 keys=select(CONCEPTS,[{'concept':'contract.employment_form','value':form}], 'labor')
 assert any(k.startswith(prefix) for k in keys)

def test_nda_with_real_competition():
 keys=select(CONCEPTS,[{'concept':'non_compete.arrangement','value':'EXISTS'}], 'confidentiality')
 assert 'non_compete.duration_months' in keys
 assert 'dispatch.comparator_pay' not in keys


def test_transport_verifier_reconciles_only_active_scope(monkeypatch):
 import json
 from review_v2 import deepseek_facts as d
 keys=select(CONCEPTS,[], 'confidentiality')
 cs=parse_contract_clauses('保密协议');raw=packet(cs,[])
 raw[0]['active_concepts']=keys;raw[0]['response']['coverage']={k:'ABSENT' for k in keys}
 s=FactStore('保密协议',cs,raw);calls=[]
 monkeypatch.setattr(d,'configuration',lambda:{'key':'test','url':'test','model':'deepseek'})
 class Response:
  status_code=200
  def __init__(self,p):self.p=p
  def json(self):return {'choices':[{'finish_reason':'stop','message':{'content':json.dumps(self.p)}}]}
 def post(*a,**kw):
  p=json.loads(kw['json']['messages'][1]['content']);calls.append(p)
  return Response({'checks':[],'searched_concepts':p['required_concepts'],'reviewed_clause_ids':[c.clause_id for c in cs],'additional_facts':[],'unresolved_concepts':[],'absence_audits':[]})
 monkeypatch.setattr(d.requests,'post',post)
 v=d.verify(cs,s)
 assert set(v['verification']['searched_concepts'])==set(keys)
 assert all(not any(c.startswith('dispatch.') for c in p['concept_definitions']) for p in calls)
 verified_store(s,v)
