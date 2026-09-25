"""Replay an explicitly selected immutable document, retaining full evidence."""
import sys, json, hashlib
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'backend'))
from layers.input_layer import InputLayer
from review_v2.engine import review_contract_v2

source, output = map(Path, sys.argv[1:3])
text = InputLayer()._extract_from_docx_content(source.read_bytes())
if len(sys.argv) > 3:
    from datetime import timedelta
    import requests
    from dotenv import load_dotenv
    load_dotenv(ROOT/'backend/.env')
    from auth.utils import create_access_token
    response=requests.post(sys.argv[3].rstrip('/')+'/review-v2/file',
        headers={'Authorization':'Bearer '+create_access_token({'user_id':'1'},timedelta(minutes=5))},
        files={'file':(source.name,source.read_bytes(),'application/vnd.openxmlformats-officedocument.wordprocessingml.document')},
        data={'contract_type':'loan','use_llm':'false','include_low_risk':'true'},timeout=180)
    response.raise_for_status()
    report=response.json()
else:
    report = review_contract_v2(text, 'loan', use_llm=False)
output.parent.mkdir(parents=True, exist_ok=True)
output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf8')
ids = {'L-01-02','L-01-04','L-02-04','L-04-02','L-04-03','L-04-04','L-07-02','L-11-03','COMMON-20-01','REG-06-01'}
print(json.dumps({'file':str(source),'hash':hashlib.sha256(source.read_bytes()).hexdigest(),
    'items':[{k:i.get(k) for k in ('item_id','coverage_status','reasoning_summary')} for i in report['items'] if i['item_id'] in ids],
    'gate':report['release_quality_gate']['status'], 'failures':report['release_quality_gate'].get('failures')}, ensure_ascii=False))
