from pathlib import Path
from review_v2.clause_parser import parse_contract_clauses
from review_v2.consulting_element_facts import elements as ce
from review_v2.technology_service_elements import elements as te
from review_v2.penalty_base import analyze
text=Path('backend/tests/fixtures/round42_consulting.txt').read_text(encoding='utf8'); c=parse_contract_clauses(text)
for fam,fn in [('consulting_subject',ce),('consulting_quality',ce),('consulting_decision',ce),('consulting_inputs',ce),('consulting_payment',ce),('confidentiality_controls',te),('confidentiality_disclosure',te),('material_exit',te)]:
 print(fam,[(x['element_id'],x['status']) for x in fn(fam,c)])
print(analyze(text))
