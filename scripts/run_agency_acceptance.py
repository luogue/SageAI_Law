"""Real endpoint acceptance and complete rule diff for the unchanged mandate file."""
import json,sys,hashlib
from pathlib import Path
from datetime import timedelta
from collections import Counter
import requests
root=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(root/'backend'))
from auth.utils import create_access_token
p=next((root/'test_data').glob('77 *.docx'))
r=requests.post('http://127.0.0.1:8016/review-v2/file',headers={'Authorization':'Bearer '+create_access_token({'user_id':'1'},timedelta(minutes=3))},
 files={'file':(p.name,p.read_bytes(),'application/vnd.openxmlformats-officedocument.wordprocessingml.document')},
 data={'contract_type':'agency','use_llm':'false','include_low_risk':'true'},timeout=180)
r.raise_for_status();a=r.json()
(root/'artifacts/agency77-production.json').write_text(json.dumps(a,ensure_ascii=False,indent=2),encoding='utf8')
assert a['release_quality_gate']['status']=='REPORT_READY',a['release_quality_gate']
assert a['contract_type']=='agency' and len(a['items'])==43
before=json.loads((root/'artifacts/agency77-before.json').read_text(encoding='utf8'))
old={i['item_id']:i for i in before['items']}
rows={i['item_id']:i for i in a['items']}
for key in ['A-01-01','A-03-03','A-04-03','A-06-02','A-12-03','A-13-03','COMMON-20-01']:assert rows[key]['coverage_status']=='通过',key
for key in ['A-01-02','A-07-02','A-11-02']:assert rows[key]['coverage_status']=='不适用',key
diff=[{'rule':i['item_id'],'before':old[i['item_id']]['coverage_status'],'after':i['coverage_status'],'evidence':i['evidence_clauses']} for i in a['items']]
(root/'artifacts/agency77-diff.json').write_text(json.dumps(diff,ensure_ascii=False,indent=2),encoding='utf8')
(root/'artifacts/agency77-report.md').write_text(a['result'],encoding='utf8')
summary={'task':a['contract_review_trace_id'],'pid':a['production_path_trace']['process_id'],'file_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),
 'before':dict(Counter(i['coverage_status'] for i in before['items'])),'after':dict(Counter(i['coverage_status'] for i in a['items'])),
 'overview':a['final_overview_summary'],'gate':a['release_quality_gate']['status']}
(root/'artifacts/agency77-acceptance.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(summary,ensure_ascii=False,indent=2))
