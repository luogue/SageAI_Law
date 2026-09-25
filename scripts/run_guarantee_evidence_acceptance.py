"""Verify original document evidence and unchanged adjudication via production API."""
import json,sys,hashlib
from pathlib import Path
from datetime import timedelta
import requests
root=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(root/'backend'))
from auth.utils import create_access_token
p=next((root/'test_data').glob('69 *.docx'))
assert hashlib.sha256(p.read_bytes()).hexdigest()=='dec08149bef6064a8217056ac4ce81ea3b240fa4e065d8478f95fb2a0bd5da6c'
response=requests.post('http://127.0.0.1:8016/review-v2/file',headers={'Authorization':'Bearer '+create_access_token({'user_id':'1'},timedelta(minutes=3))},
 files={'file':(p.name,p.read_bytes(),'application/vnd.openxmlformats-officedocument.wordprocessingml.document')},
 data={'contract_type':'guarantee','use_llm':'false','include_low_risk':'true'},timeout=180)
response.raise_for_status()
r=response.json()
(root/'artifacts/guarantee-evidence-production.json').write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf8')
baseline=json.loads((root/'artifacts/guarantee-routing-production.json').read_text(encoding='utf8'))
rows={i['item_id']:i for i in r['items']}
assert r['contract_type']==baseline['contract_type']=='guarantee'
for old in baseline['items']:
 for field in ['coverage_status','risk_level','needs_manual_review','action_priority']:
  assert old.get(field)==rows[old['item_id']].get(field),(old['item_id'],field)
assert r['risk_theme_count']==baseline['risk_theme_count']
assert r['final_overview_summary']==baseline['final_overview_summary']
out={}
for key,phrase in [('GUA-02-01','本合同自各方当事人签字或加盖公章之日生效'),('GUA-05-01','之日起两年'),('GUA-09-02','应当取得保证人书面同意')]:
 item=rows[key]
 assert phrase in item['evidence_clauses'][0]['quote']
 out[key]={'status':item['coverage_status'],'final_evidence':item['evidence_clauses']}
assert r['release_quality_gate']['status']=='REPORT_READY',r['release_quality_gate']
out.update(regression_status='PASS',task_id=r['contract_review_trace_id'],worker_pid=r['production_path_trace']['process_id'],release_quality_gate='REPORT_READY',states_unchanged=True)
(root/'artifacts/guarantee-evidence-audit.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf8')
(root/'artifacts/guarantee-evidence-report.md').write_text(r['result'],encoding='utf8')
print(json.dumps(out,ensure_ascii=False,indent=2))
