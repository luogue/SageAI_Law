import json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
out=root/'artifacts/technology_pass_semantics/round36_consulting_snapshot'
rows={}
for p in sorted(out.glob('protection_*/report.json')):
    r=json.loads(p.read_text(encoding='utf8'))
    b=json.loads((out.parent/'round35_development_consumers'/p.parent.name/'report.json').read_text(encoding='utf8'))
    old={i['item_id']:i['coverage_status'] for i in b['items']}
    new={i['item_id']:i['coverage_status'] for i in r['items']}
    groups=lambda x:{t['risk_group'] for t in x['risk_themes']}
    rows[p.parent.name.removeprefix('protection_')]={
        'gate':r['release_quality_gate']['status'],
        'added':sorted(groups(r)-groups(b)), 'removed':sorted(groups(b)-groups(r)),
        'states':{k:[v,new.get(k)] for k,v in old.items() if v!=new.get(k)}}
(out/'protection_progress.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({'completed':len(rows),'ready':sum(r['gate']=='REPORT_READY' for r in rows.values()),
    'differences':{k:v for k,v in rows.items() if v['added'] or v['removed'] or v['states']}},ensure_ascii=False))
