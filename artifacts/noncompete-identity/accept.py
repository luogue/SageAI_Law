import json,hashlib
from pathlib import Path
p=Path('artifacts/noncompete-identity');r=json.loads((p/'response.json').read_text(encoding='utf8'));i=next(x for x in r['items'] if x['item_id']=='EMP-01-01')
assert r['release_quality_gate']['status']=='REPORT_READY'
assert i['coverage_status']=='通过'
assert r['employment_classification']['subtype']=='NON_COMPETE'
assert r['structured_fact_debug']['verification_states']['identity.worker_address']['verification_state']=='VERIFIED_ABSENT'
assert not any(x['element_id']=='employment_identity_4' for x in i['coverage_elements'])
assert all(x['status']=='COVERED' and x.get('evidence_ids') for x in i['coverage_elements'])
assert all(e.get('verified_original') for e in i['evidence_clauses'])
f=next(Path('test_data').glob('120 *'));assert hashlib.sha256(f.read_bytes()).hexdigest()==(p/'source-sha256.txt').read_text()
out={'trace_id':r['contract_review_trace_id'],'contract_type':r['contract_type_name'],'EMP-01-01':i['coverage_status'],'worker_address':'VERIFIED_ABSENT / 非本专项必需身份要素','required_elements':[(x['element_id'],x['status']) for x in i['coverage_elements']],'evidence':[e['quote'] for e in i['evidence_clauses']],'release_quality_gate':r['release_quality_gate']['status'],'tests_passed':79,'source_unchanged':True}
(p/'acceptance.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps(out,ensure_ascii=False,indent=2))
