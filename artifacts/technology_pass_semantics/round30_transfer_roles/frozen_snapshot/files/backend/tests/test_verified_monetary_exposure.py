import pytest
from backend.tests.test_part_time_proportionate_coverage import review

@pytest.mark.parametrize('amount,quote,expected',[
 ('人民币1,000元','未提前通知须支付人民币1,000元违约金。','1000元'),
 ('合同金额10%','应支付合同金额10%的违约金。','合同金额10%'),
 ('每逾期一日100元','每逾期一日支付100元违约金。','每逾期一日100元'),
])
def test_penalty_exposure(monkeypatch,amount,quote,expected):
 r=review(monkeypatch,'劳动合同\n'+quote,[('penalties.obligations',dict(scope='ORDINARY_RESIGNATION',imposed=True,amount_text=amount),quote)])['EMP-14-01']
 assert expected in r['economic_impact']
 assert r['economic_impact_detail']['actual_loss'] is None
 assert r['economic_impact_detail']['contractual_exposure']


def test_separate_obligation_amounts(monkeypatch):
 deposit='从工资扣设备押金800元，归还设备后返还。';penalty='自行离职支付1000元违约金。'
 text='劳动合同\n第九条 责任\n'+deposit+'\n'+penalty
 rows=review(monkeypatch,text,[('worker.security_payment',dict(required=True,collector='EMPLOYER',deducted_from_wage=True,amount_text='800元'),deposit),('penalties.obligations',dict(scope='ORDINARY_RESIGNATION',imposed=True,amount_text='1000元'),penalty)])
 assert '800元' in rows['EMP-DEPOSIT-01']['economic_impact'] and '1000元' not in rows['EMP-DEPOSIT-01']['economic_impact']
 assert '1000元' in rows['EMP-14-01']['economic_impact'] and '800元' not in rows['EMP-14-01']['economic_impact']


def test_actual_loss_not_guessed(monkeypatch):
 q='损坏设备应赔偿实际损失。'
 rows=review(monkeypatch,'劳动合同\n'+q,[('worker.damage_liability',dict(kind='ACTUAL_DAMAGE_COMPENSATION',basis='实际损失'),q)])
 assert rows['EMP-14-01']['coverage_status']=='通过'
 assert not rows['EMP-14-01']['economic_impact_detail'].get('contractual_exposure')


def test_gate_rejects_stale_no_impact():
 from types import SimpleNamespace
 from backend.tests.test_employment_dispatch import store_for
 from review_v2.employment_fact_store import CURRENT
 from review_v2.employment_report_consistency import gate,monetary_impact
 s=store_for('违约金1000元。',[('penalties.obligations',dict(scope='ORDINARY_RESIGNATION',imposed=True,amount_text='1000元'),'违约金1000元。')])
 token=CURRENT.set(s)
 try:
  r=SimpleNamespace(item_id='EMP-14-01',node_id='employment_general_penalty',coverage_status='风险条款',evidence_clauses=s.evidence(s.get('penalties.obligations'),'test'),decision_trace={},economic_impact='无明显直接金额影响')
  assert gate([r],'## 审查（EMP-14-01）\n无明显直接金额影响')['status']=='BLOCKED'
  r.economic_impact=monetary_impact(r)
  assert gate([r],'## 审查（EMP-14-01）\n'+r.economic_impact)['status']=='REPORT_READY'
 finally:CURRENT.reset(token)
