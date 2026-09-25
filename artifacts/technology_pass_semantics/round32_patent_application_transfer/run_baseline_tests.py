from pathlib import Path
import sys
import review_v2
import pytest
base=Path(__file__).resolve().parent
review_v2.__path__=[str(base/'baseline_source')]
args=['backend/tests/test_patent_application_transfer_consistency.py',
      'backend/tests/test_application_transfer_adverse_fact_consistency.py',
      'backend/tests/test_application_transfer_element_report_consistency.py',
      'backend/tests/test_application_rejection_and_theme_closure.py',
      'backend/tests/test_penalty_base.py','-q','--tb=short',
      '--junitxml='+str(base/'baseline_tests.xml')]
sys.exit(pytest.main(args))
