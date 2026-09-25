"""Reject loss of actionable children between detail, theme and recommendations."""
import re


def compact(text):
    return re.sub(r'[\s。；;：:、，,]+', '', str(text)).removeprefix('建议')


def child_set_gate(report):
    by_id = {r['item_id']: r for r in report['items']}
    failures, checks = [], []
    top = report.get('result', '').split('## 六、完整审查明细', 1)[0]
    for finding in report['risk_findings']:
        children = [by_id[k] for k in finding['source_review_ids'] if k in by_id
                    and by_id[k]['coverage_status'] in {'缺失', '部分覆盖'}
                    and by_id[k]['action_priority'] in {'A_CORE', 'B_PRACTICAL', 'C_OPTIMIZATION'}]
        if len(children) < 2:
            continue
        expected = {r['item_id'] for r in children}
        elements = finding.get('final_missing_elements', []) + finding.get('final_adverse_elements', [])
        theme = {k for e in elements for k in (e.get('source_review_ids') or [e.get('source_review_id')]) if k}
        recs = [r for r in report['recommendations'] if finding['finding_id'] in r['source_finding_ids']]
        fragments = [f for r in recs for f in r.get('fragments', [])]
        formal = {k for f in fragments for k in f.get('source_review_ids', []) if k}
        missing_text = [f['text'] for f in fragments if compact(f['text']) not in compact(top)]
        row = {'risk_id': finding['finding_id'], 'actionable_child_ids': sorted(expected),
               'theme_child_ids': sorted(theme), 'formal_child_ids': sorted(formal),
               'missing_top_fragments': missing_text}
        checks.append(row)
        if expected - theme or expected - formal or missing_text:
            failures.append({'requirement': 'ACTIONABLE_CHILD_RECOMMENDATION_OMITTED',
                             'current_status': 'FAIL', 'failure_stage': 'Recommendation aggregation',
                             'root_cause': finding['finding_id'], 'details': row})
    return {'status': 'BLOCKED' if failures else 'REPORT_READY', 'failures': failures, 'rows': checks}
