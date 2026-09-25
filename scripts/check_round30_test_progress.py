"""Progress-only comparison; final acceptance still requires complete JUnit files."""
from pathlib import Path
import re,xml.etree.ElementTree as E
p=Path(__file__).resolve().parents[1]/'artifacts/technology_pass_semantics'
for b in [0,1]:
 text=(p/f'round30_transfer_roles/full82_batch{b}.out').read_text(encoding='utf-8-sig')
 marks=''.join(re.findall(r'^([.FEsxX]+)\s+\[\s*\d+%\]',text,re.M))
 rows=list(E.parse(p/f'round29_secret_license_aggregation/full80_batch{b}.xml').iter('testcase'))
 changes=[]
 for i,m in enumerate(marks[:len(rows)]):
  before='F' if rows[i].find('failure') is not None or rows[i].find('error') is not None else '.'
  if m!=before:changes.append((rows[i].get('classname')+'::'+rows[i].get('name'),before,m))
 print('Progress only:',b,'completed markers',len(marks),'changes',changes)
