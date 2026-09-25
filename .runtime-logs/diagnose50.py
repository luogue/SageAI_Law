import json
from pathlib import Path
from test_construction_coverage_statistics import TEXT
from review_v2.engine import review_contract_v2
r=review_contract_v2(TEXT,'construction',use_llm=False)
Path('artifacts/construction50-diagnostic.json').write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf8')
for i in r['items']:
 if i['item_id'] in ['CE-12-02','CE-13-01','CE-01-01']:
  print(i['item_id'],i['coverage_status'],json.dumps(i['decision_trace'].get('verified_pass_source_gate'),ensure_ascii=False))
  for e in i['evidence_clauses']:print(json.dumps({k:e.get(k) for k in ['evidence_id','clause_id','text','location','source_verification']},ensure_ascii=False))
print(json.dumps(r['release_quality_gate'],ensure_ascii=False))
