"""Unmodified guarantee DOCX through the listening production file endpoint."""
import json, hashlib, sys
from pathlib import Path
from datetime import timedelta
import requests

root=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(root/'backend'))
from auth.utils import create_access_token

p=next((root/'test_data').glob('69 *.docx'))
digest=hashlib.sha256(p.read_bytes()).hexdigest()
assert digest=='dec08149bef6064a8217056ac4ce81ea3b240fa4e065d8478f95fb2a0bd5da6c'
with p.open('rb') as f:
    response=requests.post('http://127.0.0.1:8016/review-v2/file',
        headers={'Authorization':'Bearer '+create_access_token({'user_id':'1'},timedelta(minutes=3))},
        files={'file':(p.name,f,'application/vnd.openxmlformats-officedocument.wordprocessingml.document')},
        data={'contract_type':'guarantee','use_llm':'false','include_low_risk':'true'},timeout=180)
response.raise_for_status()
r=response.json()
(root/'artifacts/guarantee69-final-production.json').write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf8')
rows={i['item_id']:i for i in r['items']}
for key,status in {'GUA-09-01':'法律提示','GUA-09-03':'通过','GUA-13-01':'待核验','GUA-01-01':'风险条款'}.items():
    assert rows[key]['coverage_status']==status,(key,rows[key]['coverage_status'])
assert r['release_quality_gate']['status']=='REPORT_READY',r['release_quality_gate']
from collections import Counter
print(json.dumps({'contract_hash':digest,'task_id':r['contract_review_trace_id'],
 'statuses':dict(Counter(i['coverage_status'] for i in r['items'])),
 'risk_theme_count':r['risk_theme_count'],'overview':r['final_overview_summary'],
 'gate':r['release_quality_gate'],'runtime':r['system_metadata']},ensure_ascii=False,indent=2))
