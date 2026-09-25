from pathlib import Path
from review_v2.clause_parser import parse_contract_clauses
from review_v2.technology_service_elements import elements
from review_v2.consulting_element_facts import elements as ce
from review_v2.penalty_base import analyze
text=Path('backend/tests/fixtures/round41_consulting.txt').read_text(encoding='utf8'); c=parse_contract_clauses(text)
for fam in ('confidentiality_controls','confidentiality_disclosure','material_exit'):
 print(fam,[(x['element_id'],x['status'],x.get('source_fact_key')) for x in elements(fam,c)])
for fam in ('consulting_subject','consulting_quality','consulting_decision','consulting_inputs','consulting_remedy','consulting_payment'):
 print(fam,[(x['element_id'],x['status'],x.get('source_fact_key')) for x in ce(fam,c)])
print('penalty',analyze(text))
