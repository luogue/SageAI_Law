import sys,json
from pathlib import Path
sys.path[:0]=['backend','.']
from review_v2.engine import _operative_technology_clauses, _atomic_requirement_family
from review_v2.material_disposition import extract_scoped_material_disposition_facts
p=Path('artifacts/technology_pass_semantics/round35_development_consumers')
cs=_operative_technology_clauses((p/'input/original.txt').read_text(encoding='utf8'))
facts=extract_scoped_material_disposition_facts(cs)
print('disposals',json.dumps(facts,ensure_ascii=False))
for c in cs:
 if '删除电子' in c.text: print('CLAUSE',c.model_dump())
for family in ('development_proof','development_creator'):
 print(family,json.dumps(_atomic_requirement_family(family,cs),ensure_ascii=False))
