import pytest
from review_v2.employment_fact_store import normalize,FactStore
from review_v2.fact_validation import FactExtractionError
from backend.tests.test_employment_dispatch import store_for

@pytest.mark.parametrize('value,expected',[
 ('TASK_COMPLETION','TASK_COMPLETION'),('任务完成','TASK_COMPLETION'),
 ({'mode':'PROJECT_COMPLETION'},'TASK_COMPLETION'),
 ({'mode':'EMPLOYER_DETERMINES_COMPLETION'},'EMPLOYER_DETERMINED_COMPLETION'),
 (' ｃａｌｅｎｄａｒ＿ｅｘｐｉｒｙ ','CALENDAR_EXPIRY')])
def test_enum_semantic_adaptation(value,expected):
 assert normalize('contract.term_limit_mode',value)==expected

@pytest.mark.parametrize('value',[{'mode':'MADE_UP'},['NONE'],{'mode':'NONE','type':'TASK_COMPLETION'},False,{'mode':'NONE','extra':True}])
def test_invalid_values_remain_closed(value):
 with pytest.raises(FactExtractionError): normalize('contract.term_limit_mode',value)

def test_wrapped_other_concept_and_unknown_rejected():
 assert normalize('capability.compensation',{'compensation':'WAIVED'})=='WAIVED'
 with pytest.raises(FactExtractionError): normalize('capability.compensation',{'type':'WAIVED','text':'原文说明'})
 with pytest.raises(FactExtractionError): normalize('capability.compensation',{'type':'TASK_COMPLETION'})

def test_failed_store_has_complete_diagnostic():
 with pytest.raises(FactExtractionError) as captured:
  store_for('劳动合同\n第一条\n具体终止安排。',[('contract.term_limit_mode',{'mode':'BAD'},'具体终止安排。')])
 d=captured.value.diagnostics[0]
 assert d['fact_key']=='contract.term_limit_mode'
 assert d['raw_value']=={'mode':'BAD'} and d['normalized_value'] is None
 assert 'TASK_COMPLETION' in d['allowed_values']
 assert d['evidence'] and d['source_clause'][0]['text']

@pytest.mark.parametrize('mode,risk',[('TASK_COMPLETION',False),('EMPLOYER_DETERMINED_COMPLETION',True)])
def test_task_completion_consumer(mode,risk):
 s=store_for('劳动合同\n任务终止约定。',[(k,v,'任务终止约定。') for k,v in [('contract.type','TASK'),('contract.term_limit_mode',mode)]])
 assert bool(s.adverse('employment_arbitrary_exit'))==risk

def test_route_returns_structured_error(monkeypatch):
 from fastapi import FastAPI
 from fastapi.testclient import TestClient
 from routers import review_v2 as route
 def fail(*args,**kwargs):
  store_for('劳动合同\n终止约定。',[('contract.term_limit_mode',{'mode':'BAD'},'终止约定。')])
 monkeypatch.setattr(route,'review_contract_v2',fail)
 app=FastAPI(); app.include_router(route.router)
 app.dependency_overrides[route.get_current_user]=lambda:0
 with TestClient(app) as client:
  from io import BytesIO
  from docx import Document
  doc=Document(); doc.add_paragraph('劳动合同'); stream=BytesIO(); doc.save(stream)
  response=client.post('/review-v2/file',data={'contract_type':'labor'},files={'file':('test.docx',stream.getvalue(),'application/vnd.openxmlformats-officedocument.wordprocessingml.document')})
 assert response.status_code==503,response.text
 payload=response.json()['detail']; d=payload['diagnostics'][0]
 assert payload['release_quality_gate']=='BLOCKED' and payload['trace_id']
 assert {'stage','code','fact_key','field','raw_value','normalized_value','allowed_values','evidence','clause','message'}<=set(d)
