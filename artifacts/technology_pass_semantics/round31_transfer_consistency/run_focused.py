import json,subprocess,sys,os
from pathlib import Path
p=Path('artifacts/technology_pass_semantics/round31_transfer_consistency')
args=json.loads((p/'focused_nodes.json').read_text(encoding='utf-8-sig'))
os.environ['PYTHONPATH']='backend;backend/tests;.;scripts'
# pytest receives the long node list in process, avoiding Windows command limits.
import pytest
with (p/'focused.out').open('w',encoding='utf-8') as log:
 sys.stdout=sys.stderr=log
 result=pytest.main(args+['-q','--junitxml='+str(p/'focused.xml')])
raise SystemExit(result)
