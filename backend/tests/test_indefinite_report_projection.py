from types import SimpleNamespace
from copy import deepcopy
from pytest import MonkeyPatch
from backend.tests.test_part_time_proportionate_coverage import review
from backend.tests.test_employment_dispatch import store_for
from review_v2.employment_fact_store import CURRENT
from review_v2.employment_report_consistency import insurance_exposure,source_counts,theme_display_gate,gate

def test_insurance_amount_bound_to_fact():
 q='单位按月支付人民币2,300元现金补贴替代社保。'
 s=store_for(q+'\n工资为9000元。',[('social_insurance.cash_replacement',True,q)])
 result=insurance_exposure(s.get('social_insurance.cash_replacement')[0])
 assert len(result)==1 and result[0]['fixed_amount_cny']=='2300' and result[0]['period_label']=='每月'
 assert result[0]['actual_loss'] is None

def test_report_theme_levels_and_counts(monkeypatch):
 text='劳动合同\n单位每月支付人民币2300元补贴替代社保缴纳。\n单位可随时任意解除并免除经济补偿。'
 q=text.splitlines()[1];exit=text.splitlines()[2]
 rows=review(monkeypatch,text,[('social_insurance.cash_replacement',True,q),('termination.employer_unrestricted',True,exit),('economic_compensation.waived',True,exit)])
 for k in ['EMP-10-01','EMP-11-01','EMP-16-01']:
  assert rows[k]['risk_level']=='高' and rows[k]['action_priority']=='A_CORE'
 for k in ['EMP-07-01','EMP-13-01']:
  assert '每月2300元' in rows[k]['economic_impact'] and '不等同依法应缴' in rows[k]['economic_impact']
 assert source_counts([SimpleNamespace(**r) for r in rows.values()])=={'rule_risk_hit_count':5,'risk_clause_count':2}

def test_wrong_level_and_count_are_blocked():
 s=store_for('其他事项。',[]);token=CURRENT.set(s)
 try:
  item=SimpleNamespace(item_id='R',coverage_status='风险条款',risk_level='中',action_priority='B_PRACTICAL',evidence_clauses=[{'clause_id':'C1','quote':'x'}])
  t={'source_review_ids':['R'],'severity':'HIGH','priority':'A_CORE'}
  result=theme_display_gate([item],[t],'风险条款：1')
  assert {f['requirement'] for f in result['failures']}=={'THEME_CHILD_DISPLAY_CONSISTENCY','RISK_SOURCE_COUNT_SEMANTICS'}
 finally:CURRENT.reset(token)

def test_missing_amount_report_blocked():
 q='每月支付2000元补贴替代社保。';s=store_for(q,[('social_insurance.cash_replacement',True,q)]);token=CURRENT.set(s)
 try:
  item=SimpleNamespace(item_id='R',node_id='employment_insurance',coverage_status='风险条款',economic_impact='无明显直接金额影响',evidence_clauses=s.evidence(s.get('social_insurance.cash_replacement'),'risk'),decision_trace={})
  assert any(f['requirement']=='VERIFIED_MONETARY_EXPOSURE_DISPLAY' for f in gate([item],'')['failures'])
 finally:CURRENT.reset(token)


def test_multiple_obligation_amounts_not_borrowed():
 q='工资9000元。单位支付2000元补贴替代社保。'
 s=store_for('劳动合同\n第一条 补贴\n'+q,[('social_insurance.cash_replacement',True,q)])
 assert insurance_exposure(s.get('social_insurance.cash_replacement')[0])==[]


def test_public_count_schema_is_serializable():
 from routers.review_v2 import ReviewV2Result
 schema=ReviewV2Result.model_json_schema()
 assert 'risk_clause_count' in schema['properties'] and 'rule_risk_hit_count' in schema['properties']
