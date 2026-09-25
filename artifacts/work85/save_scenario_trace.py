import json
from pathlib import Path
from collections import Counter
root=Path('artifacts/work85');d=json.loads((root/'scenario-after.json').read_text(encoding='utf8'))
keys=['COMMON-23-01','W-03-03','W-03-04','W-10-01','W-10-02','W-10-03','W-04-03','W-04-04']
rows={r['item_id']:r for r in d['items']}
lines=['# 承揽合同适用性定向复测', '', '任务：'+d['contract_review_trace_id'], '质量门禁：'+d['release_quality_gate']['status'], '覆盖统计：'+str(dict(Counter(r['coverage_status'] for r in d['items']))), '处理优先级：'+str(dict(Counter(r['action_priority'] for r in d['items'])))]
trace={}
for key in keys:
 r=rows[key];a=r.get('applicability',{});trace[key]=r
 lines+=['','## '+key+'：'+r['coverage_status'],a.get('reason','')]
 for name,hits in a.get('shared_transaction_facts',{}).items():
  if name not in ('transfer','customer_assistance','auxiliary','lien_excluded','lien_reserved'):continue
  lines+=['- '+name+': '+str(len(hits))]
  for e in hits:
   lines+=['  '+e.get('evidence_id','')+' / '+e.get('location','')+'：'+e.get('quote','')]
 if not a.get('trigger_evidence'):lines+=['- trigger_evidence=[]（未激活的专项不生成正向证据）']
 for e in r.get('evidence_clauses',[]):
  lines+=['- 最终证据：'+json.dumps(e,ensure_ascii=False)]
(root/'scenario-trace.json').write_text(json.dumps(trace,ensure_ascii=False,indent=2),encoding='utf8')
(root/'scenario-verification.md').write_text('\n'.join(lines),encoding='utf8')
for k in keys: print(k, rows[k]['coverage_status'])
print('counts',dict(Counter(r['coverage_status'] for r in d['items'])))
print('priority',dict(Counter(r['action_priority'] for r in d['items'])))
print('top keys',list(d))
