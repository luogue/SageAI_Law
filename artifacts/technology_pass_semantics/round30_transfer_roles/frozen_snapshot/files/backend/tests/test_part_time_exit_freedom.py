import pytest
from backend.tests.test_part_time_proportionate_coverage import review
from backend.tests.test_employment_dispatch import store_for

@pytest.mark.parametrize('quote,extra,status',[
 ('任一方均可随时通知结束用工。',[('part_time.exit_permission',True)],'通过'),
 ('任一方均可依法通知对方终止用工。',[('part_time.exit_permission',True)],'通过'),
 ('本协议约定小时计酬。',[],'通过'),
 ('劳动者离开须提前七日通知。',[('part_time.employee_notice_days',7),('part_time.exit_constraint','NOTICE_WAIT')],'风险条款'),
 ('未提前三十天通知离职须支付一个月报酬。',[('part_time.exit_constraint','PENALTY')],'风险条款'),
 ('至少履行六个月以后方可终止。',[('part_time.exit_constraint','MINIMUM_SERVICE')],'风险条款'),
])
def test_final_exit_result(monkeypatch,quote,extra,status):
 text='非全日制劳动合同\n双方为非全日制用工。\n'+quote
 rows=review(monkeypatch,text,[('contract.employment_form','PART_TIME','双方为非全日制用工。')]+[(c,v,quote) for c,v in extra])
 r=rows['PT-07-01']
 assert r['coverage_status']==status
 assert not r['needs_manual_review']
 if extra and status=='通过':
  assert any(quote in e.get('quote',e.get('text','')) for e in r['evidence_clauses'])
 assert r['decision_trace']['verified_negative_search']['result']==('NO_ADVERSE_FOUND' if status=='通过' else 'ADVERSE_FOUND')


def test_no_numeric_value_does_not_veto_conclusive_restriction_search():
 s=store_for('双方依法终止。',[])
 s.coverage['part_time.employee_notice_days']='UNCERTAIN'
 assert s.pending_reason('employment_part_time_exit')==''
 assert s.values('part_time.employee_notice_days')==[]
 s.coverage['part_time.exit_constraint']='UNCERTAIN'
 assert s.pending_reason('employment_part_time_exit')


def test_protective_permission_does_not_cancel_penalty(monkeypatch):
 text='双方确认非全日制。\n双方随时通知终止。\n但劳动者离职须承担违约金。'
 values=[('contract.employment_form','PART_TIME','双方确认非全日制。'),('part_time.exit_permission',True,'双方随时通知终止。'),('penalties.obligations',{'scope':'ORDINARY_RESIGNATION','imposed':True,'amount_text':'一个月工资'},'但劳动者离职须承担违约金。')]
 assert review(monkeypatch,text,values)['PT-07-01']['coverage_status']=='风险条款'


def test_absence_is_not_a_fact_enum():
 from review_v2.employment_fact_store import normalize
 from review_v2.fact_validation import FactExtractionError
 with pytest.raises(FactExtractionError):
  normalize('part_time.exit_constraint','ABSENT')
