import json,hashlib
from pathlib import Path
from datetime import datetime,timezone
root=Path('F:/ai/Sage'); out=root/'artifacts/technology_pass_semantics/round41_consulting_components'
ids={
'TC-11-01':['purpose_limitation'], 'TC-11-02':['prior_notice_when_legally_permitted'],
'TC-11-03':['termination_return_or_delete','confidential_disposal_confirmation'],
'TC-01-03':['consulting_project','consulting_deliverable'],
'TC-08-01':['consulting_scope','report_contents','delivery_form','acceptance_standard'],
'TC-08-02':['qualified_consulting_decision_risk','consultant_fault_exception'],
'TC-08-03':['technical_materials','cooperation_conditions','truthfulness_completeness'],
'TC-08-04':['defect_trigger','correction_period','correction_remedy'],
'TC-08-05':['consulting_fee_total','payment_milestones']}
sides={}
for side in ('party_a','party_b'):
 r=json.loads((out/f'final_{side}/report.json').read_text(encoding='utf-8-sig')); items={i['item_id']:i for i in r['items']}
 rules={}
 for rid,keys in ids.items():
  i=items[rid]; es={e['element_id']:e for e in i['coverage_elements']}; audits={a.get('element_id') for a in i.get('decision_trace',{}).get('element_absence_searches',[]) if a.get('result')=='NOT_FOUND'}
  rules[rid]={'coverage_status':i['coverage_status'],'elements':{}}
  for key in keys:
   e=es[key]; ev=[x for x in i['evidence_clauses'] if x.get('evidence_id') in e.get('evidence_ids',[])]
   rules[rid]['elements'][key]={'status':e['status'],'canonical_fact_key':e.get('source_fact_key'),'canonical_alias_of':e.get('canonical_alias_of'),'missing_audit':key in audits,'components':e.get('component_coverage'),'evidence':[{'evidence_id':x.get('evidence_id'),'clause_id':x.get('clause_id'),'quote':x.get('quote'),'support_type':x.get('support_type'),'verified_original':x.get('verified_original')} for x in ev]}
 inc=items['TC-11-04']; common=items['COMMON-20-01']
 rules['TC-11-04']={'coverage_status':inc['coverage_status'],'force_majeure_evidence':any('不可抗力' in str(x.get('quote') or x.get('text') or '') for x in inc['evidence_clauses']),'mitigation_status':next(e['status'] for e in inc['coverage_elements'] if e['element_id']=='mitigation_obligation')}
 rules['COMMON-20-01']={'coverage_status':common['coverage_status'],'elements':[{k:e.get(k) for k in ('element_id','status','source_fact_key','evidence_ids')} for e in common['coverage_elements']]}
 sides[side]={'review_run_id':r.get('review_run_id'),'contract_type':r.get('report_context',{}).get('contract_type_label') or r.get('contract_type'),'gate':r['release_quality_gate']['status'],'raw_blockers':len(r['release_quality_gate'].get('failures',[]) or []),'expanded_blockers':len(r['release_quality_gate'].get('blocking_entities',[]) or []),'evidence_mismatch':0 if r['release_quality_gate'].get('gate_results',{}).get('REVIEW_EVIDENCE_ELEMENT_MISMATCH')=='PASS' else 1,'rules':rules}
files=['backend/review_v2/technology_service_elements.py','backend/review_v2/consulting_element_facts.py','backend/review_v2/penalty_base.py','backend/review_v2/engine.py','backend/tests/test_round41_consulting_components.py','backend/tests/fixtures/round41_consulting.txt']
hashes={f:hashlib.sha256((root/f).read_bytes()).hexdigest() for f in files}
runtime=json.loads((out/'runtime.json').read_text(encoding='utf8'))
core_match={f:runtime['source_hashes'].get(f.replace('/','\\'))==h for f,h in hashes.items() if f.startswith('backend/review_v2/')}
accept={'round':'Round41','status':'REPORT_READY','created_at':datetime.now(timezone.utc).isoformat(),'input_sha256':hashlib.sha256((out/'input.docx').read_bytes()).hexdigest(),'runtime':runtime,'source_hashes':hashes,'runtime_core_hashes_match_final':core_match,'real_api':sides,'tests':{'round41_targeted':'6 passed','round41_plus_round36_projection':'37 passed','round41_plus_existing_fact_binding':'79 passed','adjacent_verified_confidentiality_penalty':'41 passed','broad_consulting_suite_observed':'167 passed, 11 failed; failures include legacy assertions outside this change, while the two exact-binding regressions initially introduced by this change were corrected and now pass in the 79-test run'},'constraints':{'gate_relaxed':False,'verifier_relaxed':False,'fallback_restored':False,'old_expectations_modified':False}}
(out/'acceptance.json').write_text(json.dumps(accept,ensure_ascii=False,indent=2),encoding='utf8')
(out/'final_summary.json').write_text(json.dumps(sides,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({'core_match':core_match,'api':{k:{x:v[x] for x in ('review_run_id','contract_type','gate','raw_blockers','expanded_blockers','evidence_mismatch')} for k,v in sides.items()}},ensure_ascii=False,indent=2))
