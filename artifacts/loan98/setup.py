from pathlib import Path
s=Path('scripts/run_work85_acceptance.py').read_text(encoding='utf8').replace("glob('85 *.docx')","glob('98 *.docx')").replace("'contract_type':'work'","'contract_type':'loan'").replace("artifacts/work85","artifacts/loan98")
Path('scripts/run_loan98_acceptance.py').write_text(s,encoding='utf8')
from docx import Document
p=next(Path('test_data').glob('98 *.docx'))
d=Document(p)
Path('artifacts/loan98/source.txt').write_text('\n'.join(x.text for x in d.paragraphs),encoding='utf8')
