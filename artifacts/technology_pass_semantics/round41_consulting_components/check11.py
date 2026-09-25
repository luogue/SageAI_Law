import json
from pathlib import Path
r=json.loads(Path('artifacts/technology_pass_semantics/round41_consulting_components/before_party_a/report.json').read_text(encoding='utf-8-sig'))
i=next(x for x in r['items'] if x['item_id']=='TC-11-04')
for k in ('atomic_requirement_family','direct_fact_bindings','general_breach_semantic_propagation','element_report_projection','specialized_elements'): print(k,repr(i['decision_trace'].get(k)))
