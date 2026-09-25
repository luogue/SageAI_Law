"""Coverage and severity/action explanations project final rules, not defect types."""
from copy import deepcopy

STATUS = {'通过':'PASS','部分覆盖':'PARTIAL','缺失':'MISSING','风险条款':'ADVERSE',
          '不适用':'NOT_APPLICABLE','待核验':'UNCERTAIN','PARTIALLY_COVERED':'PARTIAL',
          'COVERED':'PASS'}


def normalized(value):
    return STATUS.get(value, value or 'UNCERTAIN')


def aggregate(states):
    states = {normalized(s) for s in states} - {'NOT_APPLICABLE'}
    if not states: return 'NOT_APPLICABLE'
    if states & {'ADVERSE','CONFLICTING'}: return 'ADVERSE'
    if states == {'PASS'}: return 'PASS'
    if 'PARTIAL' in states or ('PASS' in states and states - {'PASS'}): return 'PARTIAL'
    if states == {'MISSING'}: return 'MISSING'
    return 'UNCERTAIN'


def project(theme, members, items=(), dispositions=()):
    by_id = {i.item_id:i for i in items}
    sources, components = {}, {}
    for key in theme['source_rule_ids']:
        if key in by_id:
            item = by_id[key]
            sources[key] = normalized(item.coverage_status)
            components[key] = deepcopy(item.coverage_elements)
        else:
            values = [m.legal_impact.get('coverage') for m in members if key in m.source_review_ids]
            sources[key] = aggregate(values)
    status = (next(iter(sources.values())) if len(sources)==1 else
              aggregate(e['status'] for rows in components.values() for e in rows)
              if components else aggregate(sources.values()))
    theme.update(status=status, theme_status=status, coverage_status=status,
                 source_rule_statuses=sources, source_components=components,
                 coverage_basis='FINAL_SOURCE_COMPONENTS',
                 residual_issue_types=sorted({m.issue_type for m in members}))
    reasons = list(dict.fromkeys(d.downgrade_reason for d in dispositions
                                if getattr(d, 'downgrade_reason', '')))
    theme['action_priority_reason'] = '；'.join(reasons).replace('counter_evidence', '合同已有保护性约定或反向证据')
    if reasons:
        theme['action_priority_reason'] = '严重度评估潜在后果，行动优先级另行考虑既有保护和剩余缺口。' + theme['action_priority_reason']
    if len(sources)==1:
        assert theme['status'] == next(iter(sources.values())), 'SINGLE_SOURCE_THEME_STATUS_MISMATCH'
    return theme
