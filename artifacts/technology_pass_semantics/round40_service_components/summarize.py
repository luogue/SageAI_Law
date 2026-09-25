import json
from pathlib import Path
root=Path('artifacts/technology_pass_semantics/round40_service_components')
for side in ('party_a','party_b'):
 r=json.loads((root/f'final_{side}/report.json').read_text(encoding='utf-8-sig'))
 print('\n',side,r['review_run_id'],r['release_quality_gate']['status'])
 print('gates', {k:v for k,v in r['release_quality_gate'].get('gate_results',{}).items() if 'MISMATCH' in k or 'INVARIANT' in k})
 for rid in ('TC-12-02','TC-11-03','TC-09-02','TC-11-02'):
  i=next(x for x in r['items'] if x['item_id']==rid)
  print(rid,i['coverage_status'])
  for e in i.get('coverage_elements',[]):
   if e['element_id'] in {'claim_handling_responsibility','provider_infringement_liability','direct_damage','termination_return_or_delete','written_objection_mechanism','rectification_mechanism','rectification_deadline','post_termination_confidentiality'}:
    ev=[x for x in i.get('evidence_clauses',[]) if x.get('evidence_id') in e.get('evidence_ids',[])]
    print(' ',e['element_id'],e['status'],e.get('source_fact_key'),e.get('component_coverage'),e.get('evidence_ids'),[(x.get('clause_id'),x.get('quote'),x.get('evidence_id'),x.get('support_type'),x.get('verified_original')) for x in ev])
  missing=[x.get('element_id') for x in i.get('decision_trace',{}).get('element_absence_searches',[]) if x.get('result')=='NOT_FOUND']
  print(' missing_audits',missing)

