import sys,json,hashlib
from pathlib import Path
root=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(root/'backend'),str(root/'backend/tests'),str(root)]
import pytest
out=root/'artifacts/technology_pass_semantics/round37_export_blockers'
hashes=lambda:{str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (root/'backend/review_v2').glob('*.py')}
before=hashes()
with (out/'regression.log').open('w',encoding='utf8') as log:
    sys.stdout=sys.stderr=log
    rc=pytest.main(['backend/tests/test_service_export_blockers.py',
        'backend/tests/test_final_review_snapshot.py','backend/tests/test_snapshot_export_routes.py',
        'backend/tests/test_consulting_final_projection.py','backend/tests/test_service_final_fact_binding.py',
        '-q','--tb=short','--junitxml='+str(out/'regression.xml')])
(out/'test_source_integrity.json').write_text(json.dumps({'before':before,'after':hashes(),'unchanged':before==hashes()},indent=2),encoding='utf8')
raise SystemExit(rc)
