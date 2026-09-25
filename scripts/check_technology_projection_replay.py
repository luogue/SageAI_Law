"""Read-only replay assertion for the original patent candidate snapshot."""
from copy import deepcopy
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / 'backend'), str(ROOT)]
from backend.test_database_bootstrap import install
install()
from review_v2 import engine
from tests.test_patent_license_input_integrity_routing import FULL_PATENT_LICENSE, _docx_bytes, _review_bytes


def snapshot(items):
    return {item.item_id: {
        'coverage': item.coverage_status,
        'applicability': item.applicability,
        'elements': item.coverage_elements,
        'evidence': item.evidence_clauses,
        'risk_group': item.risk_group,
        'risk_level': item.risk_level,
    } for item in items}


original = engine._apply_final_technology_fact_projection
checks = []


def checked(items, *args, **kwargs):
    result = original(items, *args, **kwargs)
    before = deepcopy(snapshot(result))
    replay = original(deepcopy(result), *args, **kwargs)
    after = snapshot(replay)
    changed = {key: [field for field in before[key] if before[key][field] != after[key][field]]
               for key in before if before[key] != after[key]}
    checks.append({'mismatch_count': len(changed), 'changed': changed})
    return result


engine._apply_final_technology_fact_projection = checked
report = _review_bytes(_docx_bytes(FULL_PATENT_LICENSE))
out = {'checks': checks, 'gate': report['release_quality_gate']['status']}
(ROOT / 'artifacts/technology_pass_semantics/round7_projection_replay.json').write_text(
    json.dumps(out, ensure_ascii=False, indent=2), encoding='utf8')
print(json.dumps(out, ensure_ascii=False))
assert checks and all(c['mismatch_count'] == 0 for c in checks)
