"""Capture actual production adapter transitions without changing decisions."""
import argparse
import importlib
import json
from copy import deepcopy
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / 'backend'), str(ROOT)]
from backend.test_database_bootstrap import install
install()
from review_v2 import engine


def main():
    p = argparse.ArgumentParser()
    p.add_argument('module'); p.add_argument('factory'); p.add_argument('output', type=Path)
    args = p.parse_args()
    transitions = []
    for name in ('_apply_coverage_gap_consistency_guard', '_apply_review_evidence_ownership',
                 '_apply_coverage_evidence_gate', '_apply_final_technology_fact_projection'):
        original = getattr(engine, name)
        def traced(items, *a, _name=name, _original=original, **kw):
            before = {i.item_id: dict(status=i.coverage_status, elements=deepcopy(i.coverage_elements),
                      evidence=deepcopy(i.evidence_clauses)) for i in items if i.item_id.startswith('TC-')}
            result = _original(items, *a, **kw)
            for i in result:
                b = before.get(i.item_id)
                if b and (b['status'] != i.coverage_status or b['elements'] != i.coverage_elements):
                    transitions.append(dict(stage=_name, rule_id=i.item_id, before=b,
                        after=dict(status=i.coverage_status, elements=deepcopy(i.coverage_elements),
                                   evidence=deepcopy(i.evidence_clauses))))
            return result
        setattr(engine, name, traced)
    factory = getattr(importlib.import_module(args.module), args.factory)
    result = getattr(factory, '__wrapped__', factory)()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(dict(gate=result['release_quality_gate'],
        items=result['items'], transitions=transitions), ensure_ascii=False, indent=2), encoding='utf8')
    print(json.dumps(dict(gate=result['release_quality_gate']['status'],
        failures=result['release_quality_gate']['failures'], transitions=len(transitions)), ensure_ascii=False))


if __name__ == '__main__': main()
