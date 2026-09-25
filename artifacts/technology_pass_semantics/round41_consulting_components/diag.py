import json
from pathlib import Path
r=json.loads(Path('artifacts/technology_pass_semantics/round41_consulting_components/before_party_a/report.json').read_text(encoding='utf-8-sig'))
out={'contract_type':r.get('contract_type'),'gate':r['release_quality_gate'],'items':{}}
for rid in ('TC-11-01','TC-11-02','TC-11-03','TC-11-04','COMMON-20-01','TC-01-03','TC-08-01','TC-08-02','TC-08-03','TC-08-04','TC-08-05'):
 i=next((x for x in r['items'] if x['item_id']==rid),None)
 if not i: continue
 out['items'][rid]={'coverage_status':i.get('coverage_status'),'issue_type':i.get('issue_type'),'elements':i.get('coverage_elements'),'evidence':i.get('evidence_clauses'),'audit':i.get('decision_trace',{}).get('element_absence_searches'),'facts':i.get('decision_trace',{}).get('contract_fact_registry_consumption',{}).get('facts'),'narrative':i.get('risk_point_description')}
Path('artifacts/technology_pass_semantics/round41_consulting_components/before_diagnostics.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf8')
