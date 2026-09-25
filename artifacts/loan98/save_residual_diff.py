import json,hashlib
from pathlib import Path
root=Path('artifacts/loan98')
b=json.loads((root/'residual-before.json').read_text(encoding='utf8'));a=json.loads((root/'residual-after.json').read_text(encoding='utf8'))
br={r['item_id']:r for r in b['items']}
lines=['# 借款合同98生产回归','',f"修复前任务：{b['contract_review_trace_id']}",f"修复后任务：{a['contract_review_trace_id']}",f"quality gate：{a['release_quality_gate']['status']}", '原DOCX SHA256：'+hashlib.sha256(next(Path('test_data').glob('98 *.docx')).read_bytes()).hexdigest(),'','|规则|修复前|修复后|','|---|---|---|']
changes=[]
for r in a['items']:
 old=br.get(r['item_id'],{})
 lines.append(f"|{r['item_id']} {r['title']}|{old.get('coverage_status','未运行')}|{r['coverage_status']}|")
 changes.append({'rule':r['item_id'],'before':old,'after':r})
for r in a['items']:
 lines += ['', '## '+r['item_id']+' '+r['title'],r['reasoning_summary'],'适用性：'+json.dumps(r['applicability'],ensure_ascii=False)]
 for e in r.get('evidence_clauses',[]):
  lines += ['- '+e.get('evidence_id',e.get('clause_id',''))+' | '+e.get('location','')+' | '+e.get('quote',e.get('text',''))]
 lines+=['要素：'+json.dumps(r.get('coverage_elements',[]),ensure_ascii=False)]
(root/'residual-diff.md').write_text('\n'.join(lines),encoding='utf8')
(root/'residual-diff.json').write_text(json.dumps(changes,ensure_ascii=False,indent=2),encoding='utf8')
(root/'residual-report.md').write_text(a['result'],encoding='utf8')
(root/'residual-acceptance.json').write_text(json.dumps({k:a.get(k) for k in ['contract_review_trace_id','coverage_summary','final_overview_summary','risk_theme_count','release_quality_gate','production_path_trace']},ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({'before':b['coverage_summary'],'after':a['coverage_summary'],'risk':a['final_overview_summary']},ensure_ascii=False))
