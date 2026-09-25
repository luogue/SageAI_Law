import json
from pathlib import Path
x=json.loads(Path('artifacts/technology_pass_semantics/round41_consulting_components/before_diagnostics.json').read_text(encoding='utf8'))
for rid,d in x['items'].items():
 print('\n###',rid,d['coverage_status'])
 for e in d['elements'] or []:
  print(e.get('element_id'),e.get('status'),e.get('source_fact_key'),e.get('evidence_ids'),e.get('residual_gap'))
 print('AUDIT',[(a.get('element_id'),a.get('result'),a.get('search_targets')) for a in d['audit'] or [] if a.get('result')=='NOT_FOUND'])
 print('EVID',[(e.get('evidence_id'),e.get('clause_id'),e.get('support_type'),e.get('supporting_element_ids'),e.get('quote')) for e in d['evidence'] or [] if e.get('source_type')!='SEARCH_AUDIT'])
