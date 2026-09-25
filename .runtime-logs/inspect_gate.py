from pathlib import Path
from docx import Document
from review_v2.engine import review_contract_v2
path=Path('test_data/53 租赁合同.docx')
report=review_contract_v2('\n'.join(p.text for p in Document(path).paragraphs if p.text.strip()), 'lease', use_llm=False)
print(report['release_quality_gate']['status'])
print(report['release_quality_gate'].get('failures'))
print(report['technical_quality_gate']['status'])
print(report['technical_quality_gate'].get('failures'))
