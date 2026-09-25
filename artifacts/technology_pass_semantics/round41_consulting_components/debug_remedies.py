from pathlib import Path
from review_v2.clause_parser import parse_contract_clauses
from review_v2.engine import _atomic_requirement_family
text=Path('backend/tests/fixtures/round41_consulting.txt').read_text(encoding='utf8')
for e in _atomic_requirement_family('confidentiality_remedies',parse_contract_clauses(text)):
 print(e['element_id'],e['status'],[(x['clause_id'],x['quote']) for x in e.get('supporting_evidence',[])])
