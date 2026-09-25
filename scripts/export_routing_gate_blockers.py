"""Export every real gate refusal with element/source context (no inferred IDs)."""
import argparse
import json
from pathlib import Path


def main():
    p = argparse.ArgumentParser()
    p.add_argument('report', type=Path)
    p.add_argument('output', type=Path)
    p.add_argument('--transitions', type=Path)
    args = p.parse_args()
    report = json.loads(args.report.read_text(encoding='utf8'))
    items = {i['item_id']: i for i in report['items']}
    findings = {f['finding_id']: f for f in report.get('risk_findings', [])}
    transitions = json.loads(args.transitions.read_text(encoding='utf8')) if args.transitions else []
    rows = []

    def visit(failure, parent=None):
        parent = parent or {}
        context = {**parent, **{k: v for k, v in failure.items()
                             if k not in ('details', 'failures', 'mismatches')}}
        children = next((failure[k] for k in ('details', 'failures', 'mismatches')
                         if isinstance(failure.get(k), list) and failure[k]), [])
        if children:
            for child in children:
                visit(child, context)
            return
        rid = context.get('rule_id') or context.get('review_id')
        if not rid and context.get('entity_type') == 'review':
            rid = context.get('entity_id')
        if not rid and context.get('root_cause') in items:
            rid = context['root_cause']
        finding = findings.get(context.get('risk_id') or context.get('finding_id'), {})
        if not rid and finding.get('source_review_ids'):
            rid = ','.join(finding['source_review_ids'])
        item = items.get(rid, {})
        key = context.get('element_id') or context.get('fact_key')
        elements = [e for e in item.get('coverage_elements', [])
                    if not key or e['element_id'] == key]
        source_ids = set(context.get('source_clause_ids') or [])
        for e in elements:
            source_ids.update(e.get('source_clause_ids') or [])
        sources = [{k: e[k] for k in ('evidence_id', 'clause_id', 'quote', 'source_type',
                    'source_span', 'supporting_element_ids') if k in e}
                   for e in item.get('evidence_clauses', [])
                   if e.get('clause_id') in source_ids or key in (e.get('supporting_element_ids') or [])]
        if not sources and finding:
            sources = [{k: e[k] for k in ('evidence_id', 'clause_id', 'quoted_text', 'source_type',
                        'source_span', 'supporting_element_ids') if k in e}
                       for e in finding.get('evidence_bundle', {}).get('items', [])]
        stage_changes = []
        for t in transitions:
            if t['rule_id'] != rid:
                continue
            before = t['before'] or {}
            after = t['after']
            if before.get('coverage') != after['coverage']:
                stage_changes.append({'stage': t['stage'], 'before': before.get('coverage'),
                                      'after': after['coverage']})
        rows.append({'error_code': context.get('requirement') or context.get('code'),
                     'rule_id': rid, 'element_id': key, 'fact_id': context.get('fact_id'),
                     'detected_stage': context.get('failure_stage'),
                     'reject_reason': context.get('reason') or context.get('root_cause'),
                     'source_spans': sources, 'current_elements': elements,
                     'observed_status_transitions': stage_changes, 'gate_tuple': context})

    for failure in report['release_quality_gate']['failures']:
        visit(failure)
    result = {'status': report['release_quality_gate']['status'], 'contract_type': report['contract_type'],
              'selected_contract_type': report['selected_contract_type'],
              'raw_failure_count': len(report['release_quality_gate']['failures']),
              'blocker_tuple_count': len(rows), 'blockers': rows,
              'note': 'Null IDs/stages mean the existing gate did not publish them; none are fabricated.'}
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf8')
    print(json.dumps({k: result[k] for k in ('status', 'raw_failure_count', 'blocker_tuple_count')}))


if __name__ == '__main__':
    main()
