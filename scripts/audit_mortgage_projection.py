"""Print source-bound blockers and the final report facts beside them."""
import json
import re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'artifacts/mortgage_projection_fixed'
records=[]
for phase, path in [('before',ROOT/'artifacts/mortgage_rule_kinds/report.json'),('after',OUT/'report.json')]:
    report=json.loads(path.read_text(encoding='utf-8'))
    failures=report['release_quality_gate'].get('failures',[])
    for item in report['items']:
        section=re.search(r'^## [^\n]*'+re.escape(item['item_id'])+r'[^\n]*\n(.*?)(?=^## |\Z)',report['result'],re.M|re.S)
        for e in item.get('coverage_elements',[]):
            ids=e.get('evidence_ids') or e.get('source_clause_ids') or []
            records.append(dict(phase=phase,rule_id=item['item_id'],element_id=e['element_id'],
                final_element_status=e['status'],bound_evidence_id=ids,
                report_fact=section.group(1) if section else '',
                bound_quotes=[r.get('quote') or r.get('text') for r in item.get('evidence_clauses',[])
                    if (r.get('evidence_id') or r.get('clause_id')) in ids],
                blocking_details=[d for f in failures for d in f.get('details',[])
                    if d.get('review_id')==item['item_id'] and d.get('element_id')==e['element_id']]))
    print(phase,report['release_quality_gate']['status'],json.dumps(failures,ensure_ascii=False))
(OUT/'projection_audit.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8')
lines=['# 最终要素与报告投影审计','']
for r in records:
    if r['rule_id'] not in {'SEC-04-01','S-00-01','S-00-03'}:continue
    lines += [f"## {r['phase']} {r['rule_id']} / {r['element_id']}",'',
        f"final_element_status={r['final_element_status']}; bound_evidence_id={r['bound_evidence_id']}",'',
        'bound_quotes: '+json.dumps(r['bound_quotes'],ensure_ascii=False),'',
        'blocking_details: '+json.dumps(r['blocking_details'],ensure_ascii=False),'',
        'report_fact:',r['report_fact'],'']
(OUT/'projection_audit.md').write_text('\n'.join(lines),encoding='utf-8')
