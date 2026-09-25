import json
from types import SimpleNamespace
import pytest
from review_v2.verification_batches import check_ids
from review_v2.fact_validation import FactExtractionError
from review_v2 import deepseek_facts as m

@pytest.mark.parametrize('count',[20,50,80,100])
def test_actual_transport_batches(monkeypatch,count):
    facts=[{'fact_id':f'EF-{i:016x}','concept':'job.position','normalized_value':str(i),'confidence':.99,'assertion':'EXPLICIT','evidence':[{'clause_id':'C1','quote':'source'}]} for i in range(count)]
    calls=[]
    def post(*a,**kw):
        p=json.loads(kw['json']['messages'][1]['content']);calls.append(p)
        data={'verification_schema_version':'fact-verification-2','checks':[{'fact_id':f['fact_id'],'supported':True,'reason':'source'} for f in p['candidate_facts']], 'searched_concepts':p['required_concepts'],'reviewed_clause_ids':['C1'],'additional_facts':[],'absence_audits':[],'unresolved_concepts':[]}
        return SimpleNamespace(status_code=200,json=lambda:{'choices':[{'finish_reason':'stop','message':{'content':json.dumps(data)}}]})
    monkeypatch.setattr(m,'configuration',lambda:{'url':'test','key':'test','model':'deepseek'})
    monkeypatch.setattr(m.requests,'post',post)
    packet=m.verify([SimpleNamespace(clause_id='C1',text='source')],SimpleNamespace(facts=facts,active_concepts={'job.position'},coverage={},verification_feedback='old EF-abcdef'))
    assert len(packet['verification']['checks'])==count
    assert all(len(p['candidate_facts'])<=20 for p in calls)
    assert all('EF-abcdef' not in p['validation_feedback'] for p in calls)
    assert set(packet['verification']['searched_concepts']) == {'job.position'}
    assert all(set(p['concept_definitions']) == {'job.position'} for p in calls)
    check_ids(facts,packet['verification']['checks'])

@pytest.mark.parametrize('ids,missing,unexpected,duplicate',[([],['a'],[],[]),(['b'],['a'],['b'],[]),(['a','a'],[],[],['a'])])
def test_exact_identity_failure(ids,missing,unexpected,duplicate):
    with pytest.raises(FactExtractionError) as e:check_ids([{'fact_id':'a','concept':'job.position','value':'role','evidence':['source']}],[{'fact_id':i} for i in ids],2)
    d=e.value.diagnostics[0]
    assert d['missing_fact_ids']==missing and d['unexpected_fact_ids']==unexpected and d['duplicate_fact_ids']==duplicate
    assert d['batch_id']==2
