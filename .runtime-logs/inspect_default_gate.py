from pathlib import Path
from docx import Document
from review_v2.engine import review_contract_v2
path=Path('test_data/53 租赁合同.docx')
report=review_contract_v2('\n'.join(p.text for p in Document(path).paragraphs if p.text.strip()), 'lease', use_llm=False)
gate=report.get('default_law_provenance_gate') or report.get('debug',{}).get('default_law_provenance_debug') or {}
print(gate)
for row in (gate.get('rows') or []):
    if set(row.get('authority_ids') or []) - set(row.get('report_authority_ids') or []): print(row)
PY
