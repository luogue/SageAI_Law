from pathlib import Path
from review_v2.clause_parser import parse_contract_clauses
from review_v2.consulting_element_facts import elements
text=Path('backend/tests/fixtures/round36_consulting.txt').read_text(encoding='utf8')
e={x['element_id']:x for x in elements('consulting_quality',parse_contract_clauses(text))}
print(e['delivery_form']['status'],e['delivery_form']['supporting_evidence'])
