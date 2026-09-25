"""Trace the original NDA protection failure without altering candidates."""
import json
import sys
from pathlib import Path
from copy import deepcopy

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'backend'))
from review_v2 import engine
from docx import Document

events = []


def snapshot(items):
    item = next((i for i in items if i.item_id == 'NDA-01-01'), None)
    if not item:
        return None
    return deepcopy(dict(status=item.coverage_status, elements=item.coverage_elements,
                         evidence=item.evidence_clauses,
                         gate=item.decision_trace.get('verified_pass_source_gate')))


for name in ('_protect_deterministic_semantic_evidence', '_verified_pass_sources',
             '_enrich_reasoning_and_citation', '_apply_element_level_narratives',
             '_attach_evidence_traceability', '_apply_review_evidence_ownership',
             '_apply_factual_grounding_gate', '_enrich_evidence_sources'):
    original = getattr(engine, name)

    def trace(items, *a, _name=name, _original=original, **kw):
        before = snapshot(items)
        out = _original(items, *a, **kw)
        after = snapshot(items)
        if before != after:
            events.append(dict(stage=_name, before=before, after=after))
        return out

    setattr(engine, name, trace)

def pytest_configure(config):
    original = engine.review_contract_v2

    def capture(*a, **kw):
        report = original(*a, **kw)
        path = ROOT / 'artifacts/technology_pass_semantics/round8_nda_trace.json'
        path.write_text(json.dumps(dict(transitions=events, report=report), ensure_ascii=False, indent=2), encoding='utf8')
        return report

    engine.review_contract_v2 = capture
