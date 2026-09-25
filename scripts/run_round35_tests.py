"""Reproducible Round33 test selection; preserve pre-existing tests verbatim."""
import sys,json,hashlib
from pathlib import Path
root=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(root/'backend'),str(root/'backend/tests'),str(root)]
import pytest
out=root/'artifacts/technology_pass_semantics/round35_development_consumers'
mode=sys.argv[1]
def hashes():
 return {str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest()
         for p in (root/'backend/review_v2').glob('*.py')}
before=hashes()
if mode=='technical':nodes=json.loads((out.parent/'round31_transfer_consistency/focused_nodes.json').read_text(encoding='utf8'))
elif mode.startswith('technical'):
 batch=int(mode[-1]);nodes=json.loads((out.parent/'round31_transfer_consistency/focused_nodes.json').read_text(encoding='utf8'))[batch::4]
elif mode.startswith('patent') and mode[-1].isdigit():nodes=json.loads((out/'patent_nodes.json').read_text(encoding='utf8'))[int(mode[-1])::3]
elif mode=='targeted':nodes=['backend/tests/test_development_consumer_snapshot.py']
elif mode=='frozen':nodes=['backend/tests/test_patent_transfer_exact_projection.py','backend/tests/test_cooperative_routing_consistency.py']
elif mode=='patent':nodes=['backend/tests/test_patent_transfer_acquisition_and_remedies.py','backend/tests/test_patent_right_transfer_contract_review.py','backend/tests/test_application_transfer_exact_projection.py']
else:nodes=['backend/tests/'+name for name in (
 'test_patent_application_transfer_consistency.py','test_application_transfer_adverse_fact_consistency.py',
 'test_application_transfer_element_report_consistency.py','test_application_rejection_and_theme_closure.py','test_penalty_base.py')]
with (out/(mode+'.log')).open('w',encoding='utf8') as log:
 sys.stdout=sys.stderr=log
 rc=pytest.main(nodes+['-q','--tb=short','--junitxml='+str(out/(mode+'.xml'))])
(out/(mode+'_source_integrity.json')).write_text(json.dumps({'before':before,'after':hashes(),'unchanged':before==hashes()},indent=2),encoding='utf8')
raise SystemExit(rc)
