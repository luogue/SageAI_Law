import pytest
from backend.tests.test_employment_dispatch import store_for
from review_v2.employment_rule_adapter import adapt,adverse,REPLACEMENTS
from review_v2.employment_contract_checklist import LABOR_CHECKLIST

@pytest.mark.parametrize('form,term,subtype', [('DIRECT','FIXED','LABOR'),('DISPATCH','FIXED','LABOR_DISPATCH'),('DIRECT','INDEFINITE','LABOR_INDEFINITE'),('DIRECT','TASK','LABOR_TASK'),('PART_TIME','FIXED','LABOR_PART_TIME')])
@pytest.mark.parametrize('risk',[False,True])
def test_matrix_normal_and_risk(form,term,subtype,risk):
 text='劳动合同\n本条确立用工形式和期限。\n约定试用安排。'
 s=store_for(text, [('contract.employment_form',form,'本条确立用工形式和期限。'),('contract.type',term,'本条确立用工形式和期限。'),('probation.arrangement','CURRENT' if risk else 'NONE','约定试用安排。')])
 checklist,audit=adapt(s,LABOR_CHECKLIST);ids={r.item_id for r in checklist}
 assert audit['classification']['subtype']==subtype
 assert 'EMP-14-01' in ids and 'EMP-IP-01' in ids
 assert any(i.startswith('DSP-') for i in ids)==(form=='DISPATCH')
 assert any(i.startswith('OET-') for i in ids)==(term=='INDEFINITE' and form!='PART_TIME')
 if form=='PART_TIME':
  assert not ids.intersection(REPLACEMENTS)
  assert bool(adverse(s,'employment_part_time_probation'))==risk
 elif term=='TASK':
  assert 'EMP-03-01' not in ids and 'EMP-15-01' in ids
 else: assert 'EMP-03-01' in ids and 'EMP-15-01' in ids

@pytest.mark.parametrize('key,value,node,risk',[
 ('working_hours.hours_per_day',4,'hours',False),('working_hours.hours_per_day',5,'hours',True),
 ('working_hours.hours_per_week',24,'hours',False),('working_hours.hours_per_week',25,'hours',True),
 ('salary.cycle_days',15,'wage',False),('salary.cycle_days',16,'wage',True),
 ('salary.cycle_kind','MONTHLY','wage',True),('salary.cycle_kind','WEEKLY','wage',False),
 ('part_time.employee_notice_days',0,'exit',False),('part_time.employee_notice_days',30,'exit',True),
 ('part_time.employer_notice_days',30,'exit',False)])
def test_part_time_thresholds_and_actor(key,value,node,risk):
 s=store_for('劳动合同\n本条约定履行条件。',[(key,value,'本条约定履行条件。')])
 assert bool(adverse(s,'employment_part_time_'+node))==risk


def adaptation_only_engine(*args,**kwargs):
    """Protocol-complete engine stub for tests of extraction repair only."""
    from review_v2.contract_registry import get_checklist
    return {'items':[{'item_id':r.item_id,'coverage_status':'缺失'} for r in get_checklist('labor')],
            'release_quality_gate':{'status':'REPORT_READY','gate_results':{}}}

def test_missing_adapted_rules_blocks_report(monkeypatch):
    from review_v2 import employment_fact_pipeline as pipeline
    from review_v2.clause_parser import parse_contract_clauses
    from review_v2.fact_validation import FactExtractionError
    from backend.tests.test_employment_fact_pipeline import fact,packet,verified_packet
    text='非全日制劳动合同\n双方建立非全日制关系。'
    cs=parse_contract_clauses(text)
    fs=[fact(cs,'contract.employment_form','PART_TIME','双方建立非全日制关系。')]
    monkeypatch.setattr(pipeline,'extract',lambda *a,**k:packet(cs,fs))
    monkeypatch.setattr(pipeline,'verify',verified_packet)
    with pytest.raises(FactExtractionError,match='EMPLOYMENT_RULE_ADAPTATION_MISMATCH'):
        pipeline.run(text,'labor',lambda *a,**k:{'items':[]})
