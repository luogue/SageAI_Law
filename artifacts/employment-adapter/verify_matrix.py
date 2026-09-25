import json
from pathlib import Path
root=Path('artifacts/employment-adapter')
labels={'ordinary':'LABOR','dispatch':'LABOR_DISPATCH','indefinite':'LABOR_INDEFINITE','task':'LABOR_TASK','part_time':'LABOR_PART_TIME'}
risks={'ordinary':{'EMP-15-01'},'dispatch':{'DSP-03-01'},'indefinite':{'OET-01-01'},'task':{'EMP-15-01'},'part_time':{'PT-01-01','PT-02-01','PT-03-01','PT-07-01','EMP-14-01'}}
summary=[]
for form,subtype in labels.items():
 for kind in ('normal','risk'):
  d=json.loads((root/'matrix'/f'{form}-{kind}'/'result.json').read_text(encoding='utf8'))
  assert d['employment_classification']['subtype']==subtype
  assert d['release_quality_gate']['status']=='REPORT_READY'
  rows={r['item_id']:r for r in d['items']};audit=d['employment_rule_adaptation']
  actual={i for i in rows if i.startswith(('EMP-','NC-','PT-','OET-','DSP-'))}
  assert actual==set(audit['retained'])|set(audit['added'])
  assert not actual.intersection(audit['disabled']) and not actual.intersection(audit['replaced'])
  found={i for i,r in rows.items() if r['coverage_status']=='风险条款'}
  assert found==(risks[form] if kind=='risk' else set()),(form,kind,found)
  assert any(i.startswith('PT-') for i in actual)==(form=='part_time')
  assert any(i.startswith('DSP-') for i in actual)==(form=='dispatch')
  assert any(i.startswith('OET-') for i in actual)==(form=='indefinite')
  if form=='task':assert 'EMP-03-01' not in actual and 'EMP-15-01' in actual
  for i in found:assert rows[i]['evidence_clauses'] and all(e.get('structured_fact_id') and e.get('verified_original') for e in rows[i]['evidence_clauses'])
  summary.append({'sample':f'{form}-{kind}','subtype':subtype,'risk_rules':sorted(found),'gate':'REPORT_READY','routing_assertions':'PASS'})
live=json.loads((root/'live/response.json').read_text(encoding='utf8'));rows={r['item_id']:r for r in live['items']}
assert live['release_quality_gate']['gate_results']['EMPLOYMENT_RULE_ADAPTATION']=='PASS'
assert live['employment_classification']['subtype']=='LABOR_PART_TIME'
assert all(rows[i]['coverage_status']=='风险条款' for i in risks['part_time'])
assert not set(rows)&set(live['employment_rule_adaptation']['replaced'])
for bad in ('补充试用期工资','缺少经济补偿约定'): assert bad not in live['result']
(root/'acceptance.json').write_text(json.dumps({'matrix':summary,'current_gate':live['release_quality_gate']['status'],'current_rules':[{k:r[k] for k in ('item_id','title','coverage_status')} for r in rows.values()]},ensure_ascii=False,indent=2),encoding='utf8')
print('PASS: 10 fresh DeepSeek samples, exact risk/routing sets; live part-time HTTP result')
