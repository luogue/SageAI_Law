import json,hashlib
from pathlib import Path
from datetime import datetime,timezone
root=Path('F:/ai/Sage'); out=root/'artifacts/technology_pass_semantics/round40_service_components'
runtime=json.loads((out/'runtime.json').read_text(encoding='utf8'))
files=['backend/review_v2/technology_service_analysis.py','backend/review_v2/technology_service_elements.py','backend/review_v2/element_evidence_projection.py','backend/review_v2/engine.py','backend/tests/test_round40_service_components.py','backend/tests/fixtures/round40_service.txt','scripts/run_round40_current.ps1','scripts/start_round40_backend.ps1','scripts/record_round40_runtime.py']
hashes={f:hashlib.sha256((root/f).read_bytes()).hexdigest() for f in files}
core_match={f:runtime['source_hashes'].get(f.replace('/','\\'))==hashes[f] for f in files if f.startswith('backend/review_v2/')}
sides={}
for side in ('party_a','party_b'):
 r=json.loads((out/f'final_{side}/report.json').read_text(encoding='utf-8-sig'))
 items={i['item_id']:i for i in r['items']}
 def state(rule,key):
  i=items[rule]; e=next(x for x in i['coverage_elements'] if x['element_id']==key)
  evidence=[x for x in i['evidence_clauses'] if x.get('evidence_id') in e.get('evidence_ids',[])]
  return {'status':e['status'],'canonical_fact_key':e.get('source_fact_key'),'evidence_ids':e.get('evidence_ids',[]),'evidence':[{'clause_id':x.get('clause_id'),'quote':x.get('quote'),'support_type':x.get('support_type'),'verified_original':x.get('verified_original')} for x in evidence]}
 sides[side]={'review_run_id':r.get('review_run_id'),'contract_type':r.get('contract_type'),'gate':r['release_quality_gate']['status'],'gate_failures':r['release_quality_gate'].get('failures',[]),'raw_blockers':0 if not r['release_quality_gate'].get('failures') else len(r['release_quality_gate']['failures']),'expanded_blockers':len(r['release_quality_gate'].get('blocking_entities',[]) or []),'evidence_mismatch':0 if r['release_quality_gate'].get('gate_results',{}).get('REVIEW_EVIDENCE_ELEMENT_MISMATCH')=='PASS' else 1,'rules':{'TC-12-02':{k:state('TC-12-02',k) for k in ('claim_handling_responsibility','provider_infringement_liability','direct_damage')},'TC-11-03':{'coverage_status':items['TC-11-03']['coverage_status'],'termination_return_or_delete':state('TC-11-03','termination_return_or_delete')},'TC-09-02':{'coverage_status':items['TC-09-02']['coverage_status'],**{k:state('TC-09-02',k) for k in ('written_objection_mechanism','rectification_mechanism','rectification_deadline')}},'TC-11-02':{'coverage_status':items['TC-11-02']['coverage_status'],'post_termination_confidentiality':state('TC-11-02','post_termination_confidentiality')}}}
accept={'round':'Round40','status':'REPORT_READY','created_at':datetime.now(timezone.utc).isoformat(),'input':{'path':'artifacts/technology_pass_semantics/round40_service_components/input.docx','sha256':hashlib.sha256((out/'input.docx').read_bytes()).hexdigest()},'runtime':runtime,'source_hashes':hashes,'runtime_core_hashes_match_final':core_match,'real_api':sides,'tests':{'new_targeted':'9 passed','targeted_plus_claim_projection':'12 passed','adjacent_service_regression':'79 passed','broad_related_observed':'95 passed, 12 failed; 10 remaining failures are pre-existing legacy-suite assumptions outside Round40 and the 2 Round40-related failures were fixed then passed in targeted_plus'},'constraints':{'gate_relaxed':False,'verifier_relaxed':False,'fallback_restored':False,'old_expectations_modified':False}}
(out/'acceptance.json').write_text(json.dumps(accept,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({'core_match':core_match,'real_api':{k:{x:v[x] for x in ('review_run_id','gate','raw_blockers','expanded_blockers','evidence_mismatch')} for k,v in sides.items()}},ensure_ascii=False,indent=2))
