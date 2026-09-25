"""Read-only phase observations for the current cooperative upload."""
import json
from copy import deepcopy
from pathlib import Path

events = []


def snapshot(value):
    items = [value] if hasattr(value, 'item_id') else value
    if not isinstance(items, list):
        return []
    return [deepcopy(dict(rule_id=i.item_id, status=i.coverage_status,
        elements=i.coverage_elements, evidence=i.evidence_clauses))
        for i in items if getattr(i, 'item_id', '') in {'TC-11-02', 'TC-05-04', 'TC-11-04', 'TC-12-02'}]


def pytest_configure(config):
    from review_v2 import engine
    for name in ('_set_multi_element_state', '_adapt_atomic_candidate_sources',
                 '_apply_final_technology_fact_projection', '_apply_technology_confidentiality_semantic_rules',
                 '_apply_technology_transaction_evidence_consistency', '_apply_coverage_gap_consistency_guard',
                 '_bind_material_narrative_elements', '_verified_pass_sources',
                 '_reconcile_specialized_coverage_from_elements'):
        old = getattr(engine, name)
        def observe(value, *args, _old=old, _name=name, **kwargs):
            before = snapshot(value)
            result = _old(value, *args, **kwargs)
            after = snapshot(value)
            if before != after:
                events.append(dict(stage=_name, before=before, after=after))
            return result
        setattr(engine, name, observe)


def pytest_sessionfinish(session, exitstatus):
    path = Path(__file__).resolve().parents[1] / 'artifacts/technology_pass_semantics/round12_stage_trace.json'
    path.write_text(json.dumps(events, ensure_ascii=False, indent=2), encoding='utf8')
