import json
from pathlib import Path
s=json.loads(Path('artifacts/technology_pass_semantics/round41_consulting_components/final_summary.json').read_text(encoding='utf8'))['party_a']['rules']
for rid,d in s.items():
 print(rid,d.get('coverage_status'))
 if 'elements' in d:
  for k,e in d['elements'].items(): print(' ',k,e['status'],e.get('canonical_fact_key'),e.get('missing_audit'),[(x['clause_id'],x['quote']) for x in e['evidence']])
 else: print(' ',d)
