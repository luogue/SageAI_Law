import json
from pathlib import Path
p=Path('artifacts/technology_pass_semantics/round35_development_consumers')
read=lambda f:json.loads(f.read_text(encoding='utf8'))
pid=read(p/'runtime.json')['process_id']
results={}
for f in sorted(p.glob('protection_*/report.json')):
 r=read(f)
 if r['production_path_trace']['process_id']!=pid:continue
 name=f.parent.name.replace('protection_','')
 base=p.parent/'round34_cooperative_routing'/('final_party_'+name[-1] if name.startswith('cooperative_') else f.parent.name)/'report.json'
 if name in ('service_client','service_provider','consulting_client','consulting_provider','entrusted'):
  base=p.parent/('round30_accepted_'+name)/'report.json'
 b=read(base)
 old={i['item_id']:i['coverage_status'] for i in b['items']};new={i['item_id']:i['coverage_status'] for i in r['items']}
 x={i['risk_group'] for i in b['risk_themes']};y={i['risk_group'] for i in r['risk_themes']}
 results[name]=dict(gate=r['release_quality_gate']['status'],added_groups=sorted(y-x),removed_groups=sorted(x-y),
                   changed_statuses={k:[v,new.get(k)] for k,v in old.items() if v!=new.get(k)})
(p/'protection_progress.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf8')
print('Completed',len(results),'ready',sum(r['gate']=='REPORT_READY' for r in results.values()))
for n,r in results.items():
 if r['added_groups'] or r['removed_groups'] or r['changed_statuses'] or r['gate']!='REPORT_READY':print(n,json.dumps(r,ensure_ascii=False))
