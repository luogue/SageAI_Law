import sys,json
from pathlib import Path
from datetime import timedelta
import requests
from dotenv import load_dotenv
load_dotenv('backend/.env')
sys.path.insert(0,'backend')
from auth.utils import create_access_token
p=Path('test_data/110 非全日制用工劳动合同.docx')
token=create_access_token({'user_id':'0'},expires_delta=timedelta(minutes=3))
r=requests.post('http://127.0.0.1:8016/review-v2/file',headers={'Authorization':'Bearer '+token},data={'contract_type':'labor','include_low_risk':'true','use_llm':'true'},files={'file':(p.name,p.read_bytes(),'application/vnd.openxmlformats-officedocument.wordprocessingml.document')},timeout=600)
Path('artifacts/employment-adapter/live/response.json').write_text(r.text,encoding='utf8')
print('HTTP',r.status_code)
r.raise_for_status()
d=r.json()
Path('artifacts/employment-adapter/live/report.md').write_text(d['result'],encoding='utf8')
print('GATE',d['release_quality_gate']['status'])
