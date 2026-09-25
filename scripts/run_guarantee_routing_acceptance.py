"""Actual file endpoint regression, including deliberately incompatible UI selection."""
import json,hashlib,sys
from collections import Counter
from datetime import timedelta
from pathlib import Path
import requests
root=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(root/'backend'))
from auth.utils import create_access_token
p=next((root/'test_data').glob('69 *.docx'))
digest=hashlib.sha256(p.read_bytes()).hexdigest()
assert digest=='dec08149bef6064a8217056ac4ce81ea3b240fa4e065d8478f95fb2a0bd5da6c'
response=requests.post('http://127.0.0.1:8016/review-v2/file',
    headers={'Authorization':'Bearer '+create_access_token({'user_id':'1'},timedelta(minutes=3))},
    files={'file':(p.name,p.read_bytes(),'application/vnd.openxmlformats-officedocument.wordprocessingml.document')},
    data={'contract_type':'confidentiality','use_llm':'false','include_low_risk':'true',
          'profile_json':json.dumps({'contract_scenario':'保密协议'},ensure_ascii=False)},timeout=180)
response.raise_for_status()
r=response.json()
(root/'artifacts/guarantee-routing-production.json').write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf8')
assert r['contract_type']=='guarantee'
assert r['release_quality_gate']['status']=='REPORT_READY',r['release_quality_gate']
assert r['production_path_trace']['runtime_source_drift']['status']=='CURRENT'
assert all(not i['item_id'].startswith(('NDA-','EMP-')) for i in r['items'])
selection=r['domain_selection_resolution']; context=selection['classification_context']
audit={k:context[k] for k in ['primary_contract_type','contract_type_confidence','secondary_clause_features',
    'classification_conflict','guarantee_features_detected','nda_primary_features_detected']}
audit.update(task_id=r['contract_review_trace_id'],worker_pid=r['production_path_trace']['process_id'],
    classification_evidence=selection['classification_evidence'],contract_hash=digest,
    selected_rule_packs=sorted(set(i['item_id'].split('-')[0] for i in r['items'])),
    nda_04_01={'status':'NOT_APPLICABLE','reason':'主类型为保证合同，未加载独立NDA规则包','accepted_evidence':[]},
    final_contract_type=r['contract_type'],contract_type_name=r['contract_type_name'],
    statistics=dict(Counter(i['coverage_status'] for i in r['items'])),
    release_quality_gate=r['release_quality_gate']['status'])
(root/'artifacts/guarantee-routing-audit.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2),encoding='utf8')
(root/'artifacts/guarantee-routing-report.md').write_text(r['result'],encoding='utf8')
print(json.dumps({k:v for k,v in audit.items() if k!='classification_evidence'},ensure_ascii=False,indent=2))
