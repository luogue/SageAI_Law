"""Replay the unchanged construction document via the frontend's live proxy."""
import os, sys, json, hashlib, sqlite3
from pathlib import Path
import requests

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'backend'))
os.chdir(ROOT/'backend')
import main  # Same .env and auth configuration as the live worker.
from auth.utils import create_access_token

with sqlite3.connect(ROOT/'backend/app.db') as db:
    users=db.execute("select id from user where mobile like '156%3860'").fetchall()
assert len(users)==1
token=create_access_token({'user_id':str(users[0][0])})
source=next((ROOT/'test_data').glob(os.environ.get('CONSTRUCTION_INPUT_GLOB','97 *.docx')))
response=requests.post('http://localhost:5173/review-v2/file',
    headers={'Authorization':'Bearer '+token},
    data={'contract_type':'construction','use_llm':os.environ.get('CONSTRUCTION_USE_LLM','false'),'include_low_risk':'true'},
    files={'file':(source.name,source.read_bytes(),'application/vnd.openxmlformats-officedocument.wordprocessingml.document')},
    timeout=240)
assert response.status_code==200,(response.status_code,response.text[:1000])
result=response.json()
out=ROOT/'artifacts'/os.environ.get('CONSTRUCTION_AUDIT_DIR','construction97-live-final');out.mkdir(parents=True,exist_ok=True)
(out/'report.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8')
(out/'report.md').write_text(result['result'],encoding='utf8')
audit={'input_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
       'report_sha256':hashlib.sha256(result['result'].encode()).hexdigest(),
       'runtime':result.get('production_path_trace'),
       'coverage_summary':result['coverage_summary'],
       'release_quality_gate':result['release_quality_gate'],
       'rules':[i for i in result['items'] if i['item_id'] in ('CE-01-01','CE-05-01','CE-05-03','CE-05-04','CE-07-04','COMMON-20-01','COMMON-40-01')]}
(out/'acceptance.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2),encoding='utf8')
print('HTTP',response.status_code,'PID',result.get('production_path_trace',{}).get('process_id'))
print('INPUT_SHA256',audit['input_sha256'])
for i in audit['rules']:
    print(i['item_id'],i['coverage_status'],[(e.get('evidence_id'),e.get('location')) for e in i['evidence_clauses']])
print('COUNTS',result['coverage_summary'])
print('GATE',result['release_quality_gate']['status'],result['release_quality_gate']['failures'])
