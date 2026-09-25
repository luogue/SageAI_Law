"""Run unchanged adjacent tests against the captured pre-Round36 modules."""
import importlib.util
import json
import sys
from pathlib import Path

root=Path(__file__).resolve().parents[1]
out=root/'artifacts/technology_pass_semantics/round36_consulting_snapshot'
sys.path[:0]=[str(root/'backend'),str(root/'backend/tests'),str(root)]
from backend.test_database_bootstrap import install
install()
import review_v2
review_v2.__path__.insert(0,str(out/'baseline_source'))
import routers
spec=importlib.util.spec_from_file_location('routers.review_v2',out/'baseline_router.py')
router=importlib.util.module_from_spec(spec)
sys.modules['routers.review_v2']=router
spec.loader.exec_module(router)
routers.review_v2=router
import pytest
nodes=['backend/tests/test_consulting_final_fact_binding.py',
       'backend/tests/test_consulting_verified_fact_projection.py',
       'backend/tests/test_technical_consulting_contract_review.py',
       'backend/tests/test_contract_scoped_user_profile.py']
with (out/'adjacent_baseline.log').open('w',encoding='utf8',buffering=1) as log:
    sys.stdout=sys.stderr=log
    code=pytest.main(nodes+['-q','--tb=short','--junitxml='+str(out/'adjacent_baseline.xml')])
raise SystemExit(code)
