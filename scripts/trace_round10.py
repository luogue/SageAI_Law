"""Read-only stage snapshots for the original transfer fixture."""
from copy import deepcopy
from pathlib import Path
import json

TARGETS = {'TC-06-02', 'TC-11-03', 'TC-11-04', 'GEN-PAY-01', 'GEN-LIAB-02', 'GEN-LIAB-03', 'TECH-SHARED-03'}
events = []

def snapshot(objects):
    if hasattr(objects, 'item_id'):
        objects = [objects]
    if not isinstance(objects, list):
        return []
    return [deepcopy({'rule_id': i.item_id, 'status': i.coverage_status,
        'elements': i.coverage_elements, 'evidence': i.evidence_clauses,
        'trace': i.decision_trace}) for i in objects if getattr(i, 'item_id', '') in TARGETS]

def pytest_configure(config):
    from review_v2 import engine
    for name in ('_set_multi_element_state', '_protect_deterministic_semantic_evidence',
        '_apply_final_technology_fact_projection', '_apply_technology_confidentiality_semantic_rules',
        '_verified_pass_sources', '_repair_pass_evidence_by_coverage_proposition',
        '_enrich_evidence_sources', '_attach_evidence_traceability', '_apply_review_evidence_ownership',
        '_bind_material_narrative_elements'):
        old = getattr(engine, name)
        def observer(items, *args, _name=name, _old=old, **kwargs):
            before = snapshot(items)
            result = _old(items, *args, **kwargs)
            after = snapshot(items)
            if before != after:
                events.append(dict(stage=_name, before=before, after=after))
            return result
        setattr(engine, name, observer)
    old_review = engine.review_contract_v2
    def review(*args, **kwargs):
        report = old_review(*args, **kwargs)
        path = Path(__file__).resolve().parents[1] / 'artifacts/technology_pass_semantics/round10_stage_trace.json'
        path.write_text(json.dumps({'events': events, 'report': report}, ensure_ascii=False, indent=2), encoding='utf8')
        return report
    engine.review_contract_v2 = review
