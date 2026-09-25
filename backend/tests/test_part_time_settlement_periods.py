import pytest
from backend.tests.test_employment_dispatch import store_for
from review_v2.part_time_settlement import calendar_interval,assessment

def period(start,end,pay,offset=0):
 return dict(earning_period_start_day=str(start),earning_period_end_day=str(end),payment_deadline_day=str(pay),earning_period_end_month_offset=0,payment_month_offset=offset)

def state(values):
 return assessment(store_for('本条工资结算安排。',[(k,v,'本条工资结算安排。') for k,v in values]))

@pytest.mark.parametrize('values,expected',[
 ([('salary.settlement_period',period(1,15,15)),('salary.settlement_period',period(16,'MONTH_END','MONTH_END'))],'PASS'),
 ([('salary.settlement_period',period(1,10,15)),('salary.settlement_period',period(11,'MONTH_END',5,1))],'RISK'),
 ([('salary.cycle_days',7)],'PASS'),([('salary.cycle_kind','MONTHLY')],'RISK'),
 ([('salary.cycle_kind','SEMIMONTHLY')],'PASS'),([('salary.cycle_kind','PAY_DATES_ONLY')],'VERIFY'),
 ([('salary.settlement_period',period(20,'MONTH_END',15,1))],'RISK'),
 ([('salary.cycle_kind','SEMIMONTHLY'),('salary.settlement_period',period(11,'MONTH_END',5,1))],'RISK'),
])
def test_periods(values,expected):assert state(values)['status']==expected

def test_calendar_all_month_lengths():
 result=calendar_interval(period(11,'MONTH_END',5,1))
 assert result['min_days']==22 and result['max_days']==25
 assert calendar_interval(period(16,'MONTH_END','MONTH_END'))['max_days']==15

def test_invalid_date_not_clamped():assert calendar_interval(period(1,31,31))['status']=='VERIFY'

def test_final_rule_and_evidence(monkeypatch):
 from backend.tests.test_part_time_proportionate_coverage import review
 q='当月一日至十日工资于十五日支付，十一日至月底工资于次月五日支付。'
 rows=review(monkeypatch,'非全日制劳动合同\n双方为非全日制。\n'+q,[('contract.employment_form','PART_TIME','双方为非全日制。'),('salary.settlement_period',period(1,10,15),q),('salary.settlement_period',period(11,'MONTH_END',5,1),q)])
 r=rows['PT-03-01'];assert r['coverage_status']=='风险条款'
 assert r['decision_trace']['specialized_legality']['max_days']==25


def test_pass_without_cycle_proof_is_blocked():
 from types import SimpleNamespace
 from review_v2.employment_report_consistency import gate
 r=SimpleNamespace(node_id='employment_part_time_wage',item_id='PT-03-01',coverage_status='通过',decision_trace={})
 assert gate([r],'')['status']=='BLOCKED'
 r.decision_trace={'specialized_legality':{'status':'PASS','max_days':15,'proof':'EXPLICIT_CYCLE'}}
 assert gate([r],'')['status']=='REPORT_READY'
