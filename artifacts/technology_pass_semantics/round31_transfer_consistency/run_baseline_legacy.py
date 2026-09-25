import sys,os
from pathlib import Path
root=Path.cwd();p=root/'artifacts/technology_pass_semantics/round31_transfer_consistency'
sys.path[:0]=[str(root/'backend'),str(root/'backend/tests'),str(root)]
import review_v2
review_v2.__path__=[str(p/'baseline_source')]
import pytest
with (p/'baseline_legacy.out').open('w',encoding='utf-8') as log:
 sys.stdout=sys.stderr=log
 result=pytest.main(['backend/tests/test_final_coverage_and_review_topics.py','-q','--junitxml='+str(p/'baseline_legacy.xml')])
raise SystemExit(result)
