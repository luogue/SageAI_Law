"""Read-only report projections; never change review decisions or audit data."""
from copy import deepcopy
from review_v2.report_statistics import requires_verification, report_status


def verification_projection(item):
    projected = deepcopy(item)
    if item.coverage_status == '不适用':
        projected.needs_manual_review = False
    if item.coverage_status == '通过' and requires_verification(item):
        instructions = list(dict.fromkeys(e.get('verification_instruction') or e.get('prerequisite_fact')
            for e in item.coverage_elements or []
            if e.get('status') in {'CONDITION_UNRESOLVED', 'PENDING_VERIFICATION'}))
        pending = '；'.join(s for s in instructions if s) or '需结合实际履行事实人工核验。'
        covered = '、'.join(dict.fromkeys(e.get('proposition', '') for e in item.coverage_elements or [] if e.get('status') == 'COVERED'))
        message = (f'合同文本已覆盖：{covered}。' if covered else '已有合同文本证据。') + '仍需人工核验：' + pending
        projected.coverage_status = 'INSUFFICIENT_CONTEXT'
        projected.status = projected.issue_type = '待核验'
        projected.needs_manual_review = True
        projected.reasoning_summary = projected.risk_point_description = message
        projected.reasoning = message
        projected.action_suggestion = '人工核验后确认本项结论。'
        projected.legal_consequence_if_missing = message
        projected.narrative_state = {**(projected.narrative_state or {}), 'judgment': message, 'consequence': message}
        projected.decision_trace['report_status_resolution'] = {'rule_coverage_status': item.coverage_status, 'report_status': '待核验', 'reason': message}
    return projected


def public_report_item(item):
    projected = verification_projection(item)
    row = projected.to_public_dict()
    row['coverage_status'] = report_status(projected)
    row['presentation'] = public_presentation(projected)
    return row

PASS_ONLY = '未发现禁止性不利约定时不产生该项风险；不要求新增风险条款。'
EXPOSURES = {
    'employment_illegal_waiver': '概括转嫁社保责任或排除法定救济的约定可能不被支持，用人单位仍可能承担补缴及相应法律责任；劳动者依法享有的救济不因该约定当然消失。',
    'employment_ip_ownership': '一揽子成果归属可能超出依法或有效约定可取得的权利范围，引发成果确权、收益分配及侵权争议；非职务成果及依法保留的人身权不能仅凭在职时间归单位。',
}


def adverse_consequence(item):
    if item.coverage_status != '风险条款':
        return ''
    current = str(item.legal_consequence_if_missing or '')
    if PASS_ONLY not in current:
        return ''
    return EXPOSURES.get(item.node_id, f'已确认“{item.title}”存在不利约定，可能导致相关约定难以执行或产生责任争议；应结合命中原文及本项法律依据调整。')


def is_search_audit(row):
    return any(str(row.get(key) or '').upper() == 'SEARCH_AUDIT'
               for key in ('source_type', 'evidence_type', 'section_type', 'source_kind'))


def public_presentation(item):
    evidence = item.evidence_clauses or []
    if item.coverage_status == '通过':
        evidence = [row for row in evidence if not is_search_audit(row)]
    from review_v2.lease_semantics import rule_evidence_package
    citations = [r for r in rule_evidence_package(item)['items'] if not is_search_audit(r)]
    from review_v2.lease_semantics import evidence_identity
    for check in (item.decision_trace or {}).get('noncompete_proportionality', {}).get('checks', []):
        label = {'broad_geography': '地域范围必要性', 'duration_compensation': '期限与补偿匹配性',
                 'compensation_baseline': '补偿合理性基准', 'early_termination_compensation': '提前解除额外补偿'}.get(check['key'], '综合合理性')
        for source in check.get('evidence', []):
            citations.append(evidence_identity({**source, 'supporting_element_ids': [check['key']],
                'support_labels': ['待核验事项的触发事实：' + label]}))
    return {'legal_consequence': adverse_consequence(item), 'evidence_clauses': deepcopy(evidence), 'element_citations': citations}


def render_element_citations(item):
    rows = public_presentation(item)['element_citations']
    if not rows:
        return []
    lines = ['【证据定位】']
    for row in rows:
        lines.append('- 支持要素：' + '、'.join(row.get('support_labels') or row.get('supporting_element_ids') or []))
        lines.append('- 条款编号：' + str(row.get('clause_number') or row.get('location') or '合同正文'))
        lines.append('- 原文片段：' + str(row.get('quoted_text') or row.get('quote') or row.get('text') or ''))
    return lines + ['']


def render_projection(items, findings):
    projected = [verification_projection(item) for item in items]
    risks = deepcopy(findings)
    passed_nodes = {item.node_id for item in items if item.coverage_status == '通过'}
    consequences = {}
    for item in projected:
        consequence = adverse_consequence(item)
        if consequence:
            consequences[item.item_id] = consequence
            item.legal_consequence_if_missing = consequence
            if item.narrative_state:
                item.narrative_state['consequence'] = consequence
    for finding in risks:
        if finding.evidence_bundle:
            finding.evidence_bundle['items'] = [row for row in finding.evidence_bundle.get('items', [])
                if not (is_search_audit(row) and str(row.get('claim_id') or '').split(':')[0] in passed_nodes)]
        replacements = [consequences[key] for key in finding.source_review_ids if key in consequences]
        if replacements and PASS_ONLY in str(finding.consequence or ''):
            finding.consequence = '；'.join(dict.fromkeys(replacements))
    return projected, risks
