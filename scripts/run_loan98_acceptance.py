"""Replay the immutable current file through the production HTTP entry."""
import sys,json,hashlib,os
from pathlib import Path
from datetime import timedelta
import requests
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'backend'))
from dotenv import load_dotenv
load_dotenv(ROOT/'backend/.env')
from auth.utils import create_access_token
p=next((ROOT/'test_data').glob('98 *.docx'))
r=requests.post(os.environ.get('REVIEW_URL','http://127.0.0.1:8016/review-v2/file'),headers={'Authorization':'Bearer '+create_access_token({'user_id':'1'},timedelta(minutes=5))},files={'file':(p.name,p.read_bytes(),'application/vnd.openxmlformats-officedocument.wordprocessingml.document')},data={'contract_type':'loan','use_llm':'false','include_low_risk':'true'},timeout=180)
r.raise_for_status()
data=r.json()
out=ROOT/'artifacts/loan98'/sys.argv[1]
out.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({'file_hash':hashlib.sha256(p.read_bytes()).hexdigest(),'task':data['contract_review_trace_id'],'gate':data['release_quality_gate'],'count':len(data['items'])},ensure_ascii=False))
