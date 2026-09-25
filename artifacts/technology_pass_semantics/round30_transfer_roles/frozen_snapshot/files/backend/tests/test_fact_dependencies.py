import json
import pytest
from review_v2.fact_dependencies import validate,dependencies,ROOTS
from review_v2.employment_fact_schema import CONCEPTS,SCHEMA_VERSION
from review_v2.employment_fact_store import normalize
from review_v2.fact_validation import FactExtractionError

@pytest.mark.parametrize('parent', ['EXPLICIT_NONE','DEFERRED',None])
def test_no_current_obligation_prohibits_parameters(parent):
 rows=[] if parent is None else [{'concept':'non_compete.arrangement','value':parent}]
 validate(rows,CONCEPTS)
 for c in dependencies(CONCEPTS):
  if not c.startswith('non_compete.'):continue
  with pytest.raises(FactExtractionError,match='UNSATISFIED_FACT_DEPENDENCY'):
   validate(rows+[{'concept':c,'value':24}],CONCEPTS)

def test_current_term():
 validate([{'concept':'non_compete.arrangement','value':'EXISTS'},{'concept':'non_compete.duration_months','value':24}],CONCEPTS)
 assert normalize('non_compete.duration_months',24)==24

def test_dispatch_needs_relationship():
 with pytest.raises(FactExtractionError,match='UNSATISFIED_FACT_DEPENDENCY'):
  validate([{'concept':'job.position','value':'工程师'},{'concept':'dispatch.comparator_pay','value':{'amount_text':'10000','unit':'CNY/MONTH'}}],CONCEPTS)

@pytest.mark.parametrize('c',['non_compete.duration_months','dispatch.temporary_duration_months','dispatch.comparator_pay','non_compete.compensation','non_compete.compensation_floor','non_compete.salary_base'])
@pytest.mark.parametrize('value',['未约定','未来另行约定','不适用'])
def test_placeholders_remain_invalid(c,value):
 with pytest.raises(FactExtractionError):normalize(c,value)

def test_staged_full_text_requests(monkeypatch):
 from review_v2 import deepseek_facts as d
 from review_v2.clause_parser import parse_contract_clauses
 calls=[]
 cs=parse_contract_clauses('保密协议\n员工保密。双方不设竞业。')
 monkeypatch.setattr(d,'configuration',lambda:{'key':'test','url':'test','model':'deepseek'})
 class Response:
  status_code=200
  def __init__(self,p):self.p=p
  def json(self):return {'choices':[{'finish_reason':'stop','message':{'content':json.dumps(self.p)}}]}
 def post(*a,**kw):
  p=json.loads(kw['json']['messages'][1]['content']);calls.append(p)
  facts=[{'concept':'non_compete.arrangement','value':'EXPLICIT_NONE'}] if 'non_compete.arrangement' in p['concepts'] else []
  return Response({'schema_version':SCHEMA_VERSION,'searched_concepts':p['required_searched_concepts'],'reviewed_clause_ids':[c.clause_id for c in cs],'unresolved_concepts':[],'facts':facts})
 monkeypatch.setattr(d.requests,'post',post)
 raw=d.extract(cs)
 assert set(calls[0]['concepts'])==set(ROOTS)
 assert all(p['relationship_context'] for p in calls[1:])
 assert all(len(p['document'])==len(cs) for p in calls)
 from review_v2.fact_modules import select
 assert set(k for p in raw for k in p['response']['searched_concepts'])==set(select(CONCEPTS,[{'concept':'non_compete.arrangement','value':'EXPLICIT_NONE'}],'labor'))
 assert not any(f['concept'].startswith('dispatch.') for p in raw for f in p['response']['facts'])


def test_module_value_scope_is_not_search_scope():
 from review_v2.fact_dependencies import eligible
 roots=[{'concept':'non_compete.arrangement','value':'DEFERRED'},{'concept':'contract.employment_form','value':'DIRECT'}]
 active=eligible(CONCEPTS,roots)
 assert not any(c.startswith('dispatch.') for c in active)
 assert not any(c in active for c in ('non_compete.duration_months','non_compete.compensation','non_compete.salary_base'))
 assert 'non_compete.access_capability' in active
 roots[0]['value']='EXISTS';roots[1]['value']='DISPATCH'
 assert set(eligible(CONCEPTS,roots))==set(CONCEPTS)
