from types import SimpleNamespace
from backend.tests.test_dispatch_completeness import store
from review_v2.dispatch_assessment import term_state
from review_v2.employment_report_consistency import decision_evidence_gate, decision_evidence_lines
import pytest

@pytest.mark.parametrize('kind,start,end,status',[
 ('FIXED','2027-03-01','2029-02-28','PASS'),
 ('FIXED','2027-03-01','2029-02-27','RISK'),
 ('FIXED','2028-02-29','2030-02-27','PASS'),
 ('FIXED','2028-01-01',None,'VERIFY'),
 ('INDEFINITE',None,None,'RISK'),('TASK',None,None,'RISK')])
def test_dispatch_fixed_term(kind,start,end,status):
 values=[('contract.type',kind)]
 if start:values.append(('contract.start_date',start))
 if end:values.append(('contract.end_date',end))
 assert term_state(store(values))['status']==status

def test_decision_evidence_loss_blocks():
 a={'reason':'两方报酬待比较','concepts':[],'input_fact_ids':['F1','F2'],
 'evidence':[{'structured_fact_id':'F1','quote':'正常工资为八千元。','clause_id':'C1'},
 {'structured_fact_id':'F2','quote':'对照岗位工资为一万元。','clause_id':'C2'}]}
 i=SimpleNamespace(item_id='CHECK-1',decision_trace={'specialized_legality':a})
 report='## 检查（CHECK-1）\n'+'\n'.join(decision_evidence_lines(i))
 assert decision_evidence_gate([i],report)['status']=='REPORT_READY'
 assert decision_evidence_gate([i],report.replace('对照岗位工资为一万元。',''))['status']=='BLOCKED'
 a['evidence'].pop()
 assert decision_evidence_gate([i],report)['status']=='BLOCKED'


def test_nested_schema_uses_normalizer_constraints():
 from review_v2.deepseek_facts import relation_value_schemas
 from review_v2.employment_conditions import normalize
 from review_v2.fact_validation import FactExtractionError
 spec=relation_value_schemas(['dispatch.onward_assignment'])['dispatch.onward_assignment']
 assert 'required' not in spec and spec['properties']['recipient']=={'type':'string','minLength':1}
 assert normalize('dispatch.onward_assignment',{'actor':'AGENCY'})=={'actor':'AGENCY'}
 with pytest.raises(FactExtractionError):normalize('dispatch.onward_assignment',{'actor':'AGENCY','recipient':''})
