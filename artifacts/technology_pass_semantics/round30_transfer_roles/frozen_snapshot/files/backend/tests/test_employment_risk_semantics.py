from types import SimpleNamespace
from copy import deepcopy
from backend.tests.test_employment_dispatch import store_for
from review_v2.employment_fact_store import CURRENT
from review_v2.employment_risk_semantics import annotate,project_item,consistency_failures
from review_v2.adverse_theme_projection import groups

def item(rows):
 return SimpleNamespace(item_id='TEST',coverage_status='风险条款',title='任意解除且免予补偿',evidence_clauses=rows,decision_trace={})

def fixture():
 return store_for('劳动合同\n单位可自行终止。\n另条约定不支付补偿。',[
  ('termination.employer_unrestricted',True,'单位可自行终止。'),
  ('economic_compensation.waived',True,'另条约定不支付补偿。')])

def test_title_only_claims_supported_fact_and_gate_detects_mutation():
 s=fixture(); rows=annotate(s,s.evidence(s.get('termination.employer_unrestricted'),'risk'))
 r=item(rows);project_item(r)
 assert '补偿' not in r.title
 token=CURRENT.set(s)
 try:
  assert not consistency_failures([r])
  r.title+='且免予补偿'
  assert consistency_failures([r])
 finally: CURRENT.reset(token)

def test_compound_requires_each_original_evidence():
 s=fixture();rows=annotate(s,s.evidence(s.facts,'risk'));r=item(rows);project_item(r)
 assert '补偿' in r.title and '终止' in r.title
 token=CURRENT.set(s)
 try:
  assert not consistency_failures([r])
  r.evidence_clauses=rows[:1]
  assert consistency_failures([r])
 finally: CURRENT.reset(token)

def test_same_fact_two_rule_views_merge_without_merging_other_exposure():
 s=fixture();rows=annotate(s,s.evidence(s.facts,'risk'))
 def finding(atom): return SimpleNamespace(aggregation_signals={'adverse_fact_atoms':[atom]})
 result,remaining=groups([finding(rows[0]['adverse_fact_atom']),finding(deepcopy(rows[0]['adverse_fact_atom'])),finding(rows[1]['adverse_fact_atom'])])
 assert not remaining and len(result)==2
 assert sorted(len(g['members']) for g in result)==[1,2]

def test_final_report_three_independent_themes(monkeypatch):
 from review_v2 import employment_fact_pipeline as pipeline
 from review_v2.engine import review_contract_v2
 from backend.tests.test_employment_fact_pipeline import fact,packet,verified_packet
 from review_v2.clause_parser import parse_contract_clauses
 text='劳动合同\n以任务完成为期。\n公司自行判断任务完毕并终止。\n任务结束不付经济补偿。\n试用一个月。'
 cs=parse_contract_clauses(text)
 fs=[fact(cs,k,v,q) for k,v,q in [('contract.type','TASK','以任务完成为期。'),('contract.term_limit_mode','EMPLOYER_DETERMINED_COMPLETION','公司自行判断任务完毕并终止。'),('economic_compensation.waived',True,'任务结束不付经济补偿。'),('probation.arrangement','CURRENT','试用一个月。'),('probation.duration_months',1,'试用一个月。')]]
 monkeypatch.setattr(pipeline,'extract',lambda *a,**k:packet(cs,fs))
 monkeypatch.setattr(pipeline,'verify',verified_packet)
 d=review_contract_v2(text,'labor',include_low_risk=True)
 rows={r['item_id']:r for r in d['items']}
 assert rows['EMP-10-01']['coverage_status']==rows['EMP-16-01']['coverage_status']=='风险条款'
 assert '补偿' not in rows['EMP-16-01']['title']
 relevant=[t for t in d['risk_themes'] if {'EMP-10-01','EMP-16-01'} & set(t.get('related_review_ids',t.get('related_rule_ids',[])))]
 # The summary must reduce duplicated rule views without discarding rule hits.
 assert d['risk_theme_count'] < d['finding_count']
 assert d['release_quality_gate']['status']=='REPORT_READY',d['release_quality_gate']['failures']
