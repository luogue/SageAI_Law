"""Non-mutating instrumentation of the normal upload's element transitions."""
import json
from pathlib import Path
from functools import wraps
from fastapi.testclient import TestClient
from main import app
from auth.utils import create_access_token
import review_v2.engine as engine

root = Path(__file__).resolve().parents[1]
events = []
last = None

def snapshot(value, phase):
    global last
    candidates = value if isinstance(value, (list, tuple)) else [value]
    for item in candidates:
        if getattr(item, 'item_id', None) != 'TC-07-03' or not hasattr(item, 'coverage_elements'):
            continue
        state = dict(status=item.coverage_status, elements=item.coverage_elements,
            evidence=[{k:r.get(k) for k in ('evidence_id','clause_id','quote','supporting_element_ids')}
                      for r in item.evidence_clauses],
            narrative=item.risk_point_description, consequence=item.legal_consequence_if_missing,
            family=item.decision_trace.get('atomic_requirement_family'))
        serialized = json.dumps(state, ensure_ascii=False, default=str)
        if serialized != last:
            events.append(dict(stage=phase, **json.loads(serialized)))
            last = serialized

def wrap(name, func):
    @wraps(func)
    def traced(*args, **kwargs):
        result = func(*args, **kwargs)
        for value in args:
            snapshot(value, name)
        snapshot(result, name)
        return result
    return traced

for name, func in list(vars(engine).items()):
    if callable(func) and name.startswith(('_apply_', '_set_multi', '_adapt_', '_attach_', '_project_', '_reconcile_')):
        setattr(engine, name, wrap(name, func))
source = root / 'artifacts/technology_pass_semantics/round17_license_input/original.docx'
with TestClient(app) as client:
    response = client.post('/review-v2/file',
        headers={'Authorization': 'Bearer ' + create_access_token({'user_id': '1'})},
        data={'contract_type':'technology','use_llm':'false','profile_json':json.dumps({'user_identity':'乙方'})},
        files={'file':('original.docx',source.read_bytes(),'application/vnd.openxmlformats-officedocument.wordprocessingml.document')})
(root / 'artifacts/technology_pass_semantics/round17_stages.json').write_text(json.dumps(events,ensure_ascii=False,indent=2),encoding='utf8')
print(response.status_code, len(events))
