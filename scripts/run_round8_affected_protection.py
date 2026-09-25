"""Original passing consumers in the three affected modules, plus five targets."""
import json
from pathlib import Path
import subprocess
import sys
import xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
ART=ROOT/'artifacts/technology_pass_semantics'
modules={'backend.tests.test_technical_secret_license_contract_review',
         'backend.tests.test_technical_secret_transfer_contract_review',
         'backend.tests.test_technical_service_dynamic_roles_and_grounding'}
ids=[]
for path in ART.glob('full19_batch*.xml'):
    for c in ET.parse(path).iter('testcase'):
        if c.get('classname') in modules and c.find('failure') is None and c.find('error') is None:
            ids.append(c.get('classname')+'::'+c.get('name'))
old=json.loads((ART/'round8_adjudication.json').read_text(encoding='utf8'))
ids += [r['test_id'] for r in old['items'] if r['current']['status']=='FAIL']
nodes=[key.split('::')[0].replace('.','/')+'.py::'+key.split('::',1)[1] for key in dict.fromkeys(ids)]
with (ART/'round8_affected_protection.out').open('w',encoding='utf8') as log:
    result=subprocess.run([sys.executable,'-X','utf8','-m','pytest',*nodes,'-q','--tb=short',
        '--junitxml='+str(ART/'round8_affected_protection.xml')],cwd=ROOT,stdout=log,stderr=subprocess.STDOUT)
print('original_tests',len(nodes),'exit',result.returncode,flush=True)
