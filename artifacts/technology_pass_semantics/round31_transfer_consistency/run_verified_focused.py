import sys,json
from pathlib import Path
root=Path.cwd();out=root/'artifacts/technology_pass_semantics/round31_transfer_consistency'
sys.path[:0]=[str(root/'backend'),str(root/'backend/tests'),str(root)]
import pytest
batch=int(sys.argv[1]);nodes=json.loads((out/'focused_nodes.json').read_text(encoding='utf8'))[batch::4]
with (out/f'verified_focused{batch}.out').open('w',encoding='utf8') as log:
 sys.stdout=sys.stderr=log
 rc=pytest.main(nodes+['-q','--junitxml='+str(out/f'verified_focused{batch}.xml')])
raise SystemExit(rc)
