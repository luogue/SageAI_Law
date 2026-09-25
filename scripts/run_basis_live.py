"""Replay the captured upload through the real frontend proxy; never log credentials."""
import sys,json,sqlite3,hashlib
from pathlib import Path
import requests
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'backend'))
import os
os.chdir(ROOT/'backend')
import main  # Match the running worker's configuration/import order.
from auth.utils import create_access_token
baseline=json.loads((ROOT/'artifacts/basis-production-before/result-20908-e17cf8580ba442be88e27a24d6a196ad.json').read_text(encoding='utf8'))
with sqlite3.connect(str(ROOT/'backend/app.db')) as db:
    rows=db.execute("select id from user where mobile like '156%3860'").fetchall()
assert len(rows)==1,'Cannot uniquely resolve the existing signed-in local account'
token=create_access_token({'user_id':str(rows[0][0])})
source=ROOT/'test_data/82 保管合同.docx'
response=requests.post('http://localhost:5173/review-v2/file',headers={'Authorization':'Bearer '+token},
    data={'contract_type':'safekeeping','use_llm':'true','include_low_risk':'true','profile_json':json.dumps(baseline['profile'],ensure_ascii=False)},
    files={'file':(source.name,source.read_bytes(),'application/vnd.openxmlformats-officedocument.wordprocessingml.document')},timeout=180)
print('HTTP',response.status_code)
if response.status_code!=200:
    print(response.text[:1800]);sys.exit(1)
r=response.json();out=ROOT/'artifacts/basis-production-after';out.mkdir(exist_ok=True,parents=True)
(out/'report.json').write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf8')
(out/'report.md').write_text(r['result'],encoding='utf8')
print('PID',r['production_path_trace']['process_id'],'GATE',r['release_quality_gate']['status'])
print('source_sha256',hashlib.sha256(source.read_bytes()).hexdigest())
print('failures',r['release_quality_gate']['failures'])
