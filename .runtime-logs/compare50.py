import json
from pathlib import Path
from test_construction_coverage_statistics import TEXT
import review_v2.engine as e
r=e.review_contract_v2(TEXT,'construction',use_llm=False)
Path('artifacts/construction50-final.json').write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf8')
e._verified_pass_sources=lambda *a,**k: {'status':'REPORT_READY','failures':[]}
b=e.review_contract_v2(TEXT,'construction',use_llm=False)
print('CONTROL_ONLY_NOT_PRODUCTION')
for rid in ['CE-01-01','CE-12-03','CE-13-03']:
 for name,v in [('current',r),('without_new_pass_gate',b)]:
  i=next(i for i in v['items'] if i['item_id']==rid)
  print(name,rid,i['coverage_status'],json.dumps(i['decision_trace'].get('verified_pass_source_gate'),ensure_ascii=False))
print('counts',len(r['items']),len(b['items']))
print('recommendations',r['final_overview_summary'],b['final_overview_summary'])
