"""Append-only legal enrichment: business results never cross back from law workers."""
from contextlib import contextmanager
from contextvars import ContextVar
from copy import deepcopy
import hashlib
import json

_ENABLED = ContextVar('legal_enrichment_enabled', default=True)
LEGAL_FIELDS = {'legal_basis_index', 'legal_references'}
LEGAL_TRACE_FIELDS = {'legal_basis_runtime_trace', 'legal_authority_selection', 'legal_enrichment_boundary'}


@contextmanager
def enrichment_mode(enabled):
    """Request-scoped diagnostic switch; never a global environment/cache toggle."""
    token = _ENABLED.set(enabled)
    try:
        yield
    finally:
        _ENABLED.reset(token)


def business_snapshot(item):
    data = deepcopy(item if isinstance(item, dict) else vars(item))
    for key in LEGAL_FIELDS:
        data.pop(key, None)
    trace = data.get('decision_trace', {})
    for key in LEGAL_TRACE_FIELDS:
        trace.pop(key, None)
    return data


def digest(data):
    return hashlib.sha256(json.dumps(data, sort_keys=True, ensure_ascii=False, default=str).encode()).hexdigest()


def enrich(items, checkpoints, operation):
    before = [business_snapshot(i) for i in items]
    # Even an accidentally mutating selector receives no references to live facts
    # or frozen checkpoint metadata. Reject its business delta; do not mask it.
    copies = deepcopy(items)
    detached_checkpoints = deepcopy(checkpoints)
    checkpoint_before = deepcopy([vars(c) for c in detached_checkpoints])
    gate = operation(copies, detached_checkpoints) if _ENABLED.get() else {
        'status': 'REPORT_READY', 'failures': [], 'rows': []}
    after = [business_snapshot(i) for i in copies]
    failures = []
    if len(copies) != len(items) or len(detached_checkpoints) != len(checkpoints):
        failures.append({'requirement': 'LEGAL_ENRICHMENT_ROW_PRESERVATION',
                         'root_cause': 'Legal worker changed the review/checkpoint collection.', 'current_status': 'FAIL'})
    for original, candidate in zip(checkpoint_before, detached_checkpoints):
        changed = sorted(k for k in set(original) | set(vars(candidate))
                         if original.get(k) != vars(candidate).get(k))
        if changed:
            failures.append({'requirement': 'LEGAL_ENRICHMENT_CHECKPOINT_IMMUTABILITY',
                'root_cause': original.get('item_id'), 'changed_fields': changed, 'current_status': 'FAIL'})
    for index, (item, candidate) in enumerate(zip(items, copies)):
        changed = sorted(k for k in set(before[index]) | set(after[index])
                         if before[index].get(k) != after[index].get(k))
        trace = {'enabled': _ENABLED.get(), 'before': before[index], 'after': after[index],
                 'hash_before': digest(before[index]), 'hash_after': digest(after[index]),
                 'changed_fields': changed, 'status': 'BLOCKED' if changed else 'PASS'}
        if changed:
            failures.append({'requirement': 'LEGAL_ENRICHMENT_BUSINESS_IMMUTABILITY',
                'root_cause': item.item_id, 'changed_fields': changed, 'current_status': 'FAIL'})
        elif _ENABLED.get():
            for key in LEGAL_FIELDS:
                setattr(item, key, deepcopy(getattr(candidate, key)))
            for key in LEGAL_TRACE_FIELDS - {'legal_enrichment_boundary'}:
                if key in candidate.decision_trace:
                    item.decision_trace[key] = deepcopy(candidate.decision_trace[key])
        item.decision_trace['legal_enrichment_boundary'] = trace
    return {**gate, 'failures': list(gate.get('failures', [])) + failures,
            'status': 'BLOCKED' if failures or gate.get('status') == 'BLOCKED' else 'REPORT_READY'}


def positive_consistency(items):
    """An established, source-bound atom cannot become a negative search result."""
    failures = []
    for item in items:
        data = item if isinstance(item, dict) else vars(item)
        trace = data.get('decision_trace', {})
        pool = trace.get('shared_concept_facts', {})
        audits = {a['element_id']: a for a in trace.get('element_absence_searches', [])}
        for element in data.get('coverage_elements', []):
            key = element['element_id']
            if element['status'] == 'NOT_APPLICABLE':
                continue
            positive = bool(pool.get(key)) or (
                element['status'] == 'COVERED' and bool(element.get('evidence_ids')))
            contradiction = positive and (
                element['status'] == 'MISSING' or audits.get(key, {}).get('result') == 'NOT_FOUND'
                or data.get('coverage_status') in ('缺失', 'MISSING', 'COMPLETELY_MISSING'))
            if contradiction:
                failures.append({'requirement': 'POSITIVE_FACT_MONOTONICITY',
                    'root_cause': data['item_id'], 'element_id': key,
                    'final_element_status': element['status'],
                    'bound_evidence_ids': element.get('evidence_ids', []),
                    'search_audit': audits.get(key), 'current_status': 'FAIL'})
    return {'status': 'BLOCKED' if failures else 'REPORT_READY', 'failures': failures}
