"""Replay previously unlisted legacy tests on the inverse-patch baseline."""
import sys
from pathlib import Path
import importlib.abc
import importlib.machinery
import importlib.util

ROOT = Path('F:/ai/Sage')
OUT = ROOT / 'artifacts/technology_pass_semantics/round21_semantics'
sys.path[:0] = [str(ROOT / 'backend'), str(ROOT), str(ROOT / 'scripts')]
MODIFIED = {'engine', 'proposition_scope', 'technology_adverse_evidence', 'technology_service_analysis',
            'license_control_facts', 'technology_fact_ontology', 'obligation_detail_elements', 'element_resolution'}


class BaselineLoader(importlib.machinery.SourceFileLoader):
    def get_code(self, fullname):
        source = OUT / 'baseline_round20/review_v2' / (fullname.rsplit('.', 1)[-1] + '.py')
        return compile(source.read_bytes(), self.path, 'exec')


class BaselineFinder(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname.startswith('review_v2.') and fullname.rsplit('.', 1)[-1] in MODIFIED:
            original = ROOT / 'backend/review_v2' / (fullname.rsplit('.', 1)[-1] + '.py')
            return importlib.util.spec_from_file_location(fullname, original, loader=BaselineLoader(fullname, str(original)))


sys.meta_path.insert(0, BaselineFinder())
print('BASELINE_SOURCE_OVERLAY', sorted(MODIFIED), flush=True)
import pytest
raise SystemExit(pytest.main([
    'backend/tests/test_secret_license_production_closure.py',
    'backend/tests/test_foreign_secret_license_evidence_consistency.py',
    '-q', '--tb=short', '--junitxml=' + str(OUT / 'supplemental_before.xml'),
]))
