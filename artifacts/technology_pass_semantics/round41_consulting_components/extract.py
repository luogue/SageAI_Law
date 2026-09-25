from docx import Document
from pathlib import Path
p=Path('artifacts/technology_pass_semantics/round41_consulting_components/input.docx')
d=Document(p)
text='\n'.join(x.text for x in d.paragraphs if x.text.strip())
Path('backend/tests/fixtures/round41_consulting.txt').write_text(text,encoding='utf8')
print(len(text))
