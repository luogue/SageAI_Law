"""Diagnostic only: record actual verdict writes without changing decisions."""
import json
import sys
import traceback
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'backend'))
from review_v2.engine import ReviewItemResult
events = []
original = ReviewItemResult.__setattr__
def traced(self, key, value):
    if getattr(self, 'item_id', None) == 'EMP-11-01' and key in {'coverage_status', 'evidence_clauses'}:
        events.append({'field': key, 'before': getattr(self, key, None), 'after': value,
                       'object_id': id(self), 'stack': traceback.format_stack(limit=9)})
    original(self, key, value)
ReviewItemResult.__setattr__ = traced
import runpy
sys.argv = [str(ROOT / 'scripts/run_employment_file_acceptance.py'),
            str(ROOT / 'test_data/100 劳动合同.docx'), '--http', '--output',
            str(ROOT / 'artifacts/employment_runtime_audit_0910')]
try:
    runpy.run_path(sys.argv[0], run_name='__main__')
finally:
    (ROOT / 'artifacts/employment_runtime_audit_0910/verdict_writes.json').write_text(
        json.dumps(events, ensure_ascii=False, indent=2, default=str), encoding='utf-8')
