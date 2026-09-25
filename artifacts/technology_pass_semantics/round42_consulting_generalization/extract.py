from docx import Document
from pathlib import Path
p=Path('artifacts/technology_pass_semantics/round42_consulting_generalization/input.docx')
d=Document(p); text='\n'.join(x.text for x in d.paragraphs if x.text.strip())
Path('backend/tests/fixtures/round42_consulting.txt').write_text(text,encoding='utf8')
print(len(text))
