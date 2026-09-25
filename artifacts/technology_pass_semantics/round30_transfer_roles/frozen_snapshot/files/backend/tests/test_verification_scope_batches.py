import json
from types import SimpleNamespace
import pytest
from review_v2 import deepseek_facts as m
from review_v2.verification_batches import plan_scope,check_scope
from review_v2.fact_validation import FactExtractionError

@pytest.mark.parametrize('count',[20,50,125])
def test_full_transport_scope_including_no_fact_concepts(monkeypatch,count):
 schema={f'concept.{i:03}':'definition' for i in range(count-3)}
 schema.update({'dispatch.onward_assignment':'relation','dispatch.return_terms':'grounds','worker.security_payment':'payment'})
 monkeypatch.setattr(m,'CONCEPTS',schema);monkeypatch.setattr(m,'configuration',lambda:{'url':'test','key':'test','model':'deepseek'})
 calls=[]
 def post(*a,**kw):
  p=json.loads(kw['json']['messages'][1]['content']);calls.append(p)
  data={'verification_schema_version':'fact-verification-2','checks':[], 'searched_concepts':p['required_concepts'],'reviewed_clause_ids':['C1'],'additional_facts':[],'absence_audits':[],'unresolved_concepts':[]}
  return SimpleNamespace(status_code=200,json=lambda:{'choices':[{'finish_reason':'stop','message':{'content':json.dumps(data)}}]})
 monkeypatch.setattr(m.requests,'post',post)
 r=m.verify([SimpleNamespace(clause_id='C1',text='全文')],SimpleNamespace(facts=[],active_concepts=set(schema),coverage={},verification_feedback=''))
 assert set(r['verification']['searched_concepts'])==set(schema)
 assert all(len(p['required_concepts'])<=20 and p['document'] for p in calls)
 assert set(k for p in calls for k in p['required_concepts'])==set(schema)

@pytest.mark.parametrize('actual',[None,[],['a'],['a','b','x']])
def test_bad_scope_fail_closed(actual):
 with pytest.raises(FactExtractionError) as e:check_scope(['a','b'],actual,3)
 d=e.value.diagnostics[0]
 assert d['expected_count']==2 and d['batch_id']==3
 assert d['missing_concepts']==sorted({'a','b'}-set(actual or []))
 assert d['unexpected_concepts']==sorted(set(actual or [])-{'a','b'})

def test_stable_plan_many_facts_one_concept_keeps_single_audit_owner():
 facts=[{'fact_id':str(i),'concept':'a'} for i in range(51)]
 p=plan_scope(['a','b'],list(reversed(facts)))
 assert p==plan_scope(['b','a'],facts)
 assert all(len(b['facts'])<=20 for b in p)
 assert sum(b['audit'] for b in p if 'a' in b['concepts'])==1
 assert any('b' in b['concepts'] and not b['facts'] for b in p)
