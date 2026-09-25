import pytest
from backend.tests.test_employment_dispatch import store_for
from backend.tests.test_employment_fact_pipeline import fact,packet,verified_packet
from review_v2.employment_indefinite import limit_adverse,capability_adverse
from review_v2.clause_parser import parse_contract_clauses

@pytest.mark.parametrize('kind,mode,expected', [('INDEFINITE','CALENDAR_EXPIRY',True),('INDEFINITE','MAXIMUM_DURATION',True),('INDEFINITE','EMPLOYER_RENEWAL',True),('INDEFINITE','NONE',False),('FIXED','CALENDAR_EXPIRY',False)])
def test_limit_requires_open_ended_fact(kind,mode,expected):
 text='劳动合同\n本条约定期限性质与终止机制。'
 s=store_for(text,[(k,v,'本条约定期限性质与终止机制。') for k,v in [('contract.type',kind),('contract.term_limit_mode',mode)]])
 assert bool(limit_adverse(s,'employment_open_ended_limit'))==expected

@pytest.mark.parametrize('concept,bad,good',[
 ('capability.ground','RANK_ALONE','STATUTORY'),
 ('capability.reassessment',False,True),
 ('capability.notice','IMMEDIATE_NO_ALTERNATIVE','NOTICE_OR_PAY'),
 ('capability.compensation','WAIVED','STATUTORY')])
def test_capability_polarity(concept,bad,good):
 text='劳动合同\n本条规定不能胜任解除条件。'
 for value,expected in [(bad,True),(good,False)]:
  s=store_for(text,[(concept,value,'本条规定不能胜任解除条件。')])
  assert bool(capability_adverse(s,'employment_arbitrary_exit'))==expected

@pytest.mark.parametrize('training,reassignment,risk',[(False,False,True),(True,False,False),(False,True,False),(True,True,False)])
def test_training_or_reassignment_are_alternatives(training,reassignment,risk):
 text='劳动合同\n培训措施。\n岗位调整措施。'
 s=store_for(text,[('capability.training',training,'培训措施。'),('capability.reassignment',reassignment,'岗位调整措施。')])
 assert bool(capability_adverse(s,'employment_arbitrary_exit'))==risk

@pytest.mark.parametrize('node,key', [('employment_open_ended_limit','contract.term_limit_mode'),('employment_arbitrary_exit','capability.ground')])
def test_uncertain_facts_use_natural_language(node,key):
 s=store_for('劳动合同\n有关安排需要核对。',[])
 s.coverage[key]='UNCERTAIN'
 reason=s.pending_reason(node)
 assert reason and key not in reason
 assert not any(token in reason for token in ('RANK_ALONE','CALENDAR_EXPIRY','STATUTORY'))

def test_final_report_open_ended_risks_and_six_months(monkeypatch):
 from review_v2 import employment_fact_pipeline as pipeline
 from review_v2.engine import review_contract_v2
 text='劳动合同\n本合同无固定期限。\n协议将于未来约定日期自行失效。\n考核排在最后即可解聘。\n约定六个月试用。'
 cs=parse_contract_clauses(text)
 fs=[fact(cs,k,v,q) for k,v,q in [('contract.type','INDEFINITE','本合同无固定期限。'),('contract.term_limit_mode','CALENDAR_EXPIRY','协议将于未来约定日期自行失效。'),('capability.ground','RANK_ALONE','考核排在最后即可解聘。'),('probation.arrangement','CURRENT','约定六个月试用。'),('probation.duration_months',6,'约定六个月试用。')]]
 monkeypatch.setattr(pipeline,'extract',lambda *a,**k:packet(cs,fs))
 monkeypatch.setattr(pipeline,'verify',verified_packet)
 result=review_contract_v2(text,'labor',include_low_risk=True)
 rows={r['item_id']:r for r in result['items']}
 assert result['contract_type_name']=='无固定期限劳动合同'
 for key in ('OET-01-01','EMP-16-01','EMP-10-01'):
  assert rows[key]['coverage_status']=='风险条款'
  assert all(e['quote'] in text and e.get('structured_fact_id') for e in rows[key]['evidence_clauses'])
 assert rows['EMP-15-01']['coverage_status']=='通过'
 assert result['release_quality_gate']['status']=='REPORT_READY'
 assert 'RANK_ALONE' not in result['result']
