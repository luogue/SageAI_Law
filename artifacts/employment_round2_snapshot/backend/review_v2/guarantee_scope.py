"""Direct guarantee-scope evidence, excluding the guarantor's recourse costs."""
import re


def scope_evidence(clauses):
    rows = []
    for clause in clauses:
        for quote in re.split(r'(?<=[。；;])|\n', clause.text):
            text = re.sub(r'\s+', '', quote)
            if re.search(r'追偿|求偿|代偿后|承担保证责任后|向借款人.*偿还', text):
                continue
            cap = re.search(r'(?:最高保证金额|最高保证额|保证金额(?:总额|上限)|保证责任上限).{0,12}[\d一二三四五六七八九十百千万亿]', text)
            exclusion = re.search(r'(?:超出|超过).{0,25}保证(?:金额|期限).{0,25}不承担', text)
            enumerated = ('本金' in text and '利息' in text and '违约金' in text
                          and '实现债权费用' in text and bool(re.search(r'保证范围|保证人.{0,20}承担|全部承担', text)))
            if not (cap or exclusion or enumerated):
                continue
            rows.append({'clause_id': clause.clause_id, 'location': clause.location,
                         'quote': quote.strip(), 'text': quote.strip(), 'source_type': 'SOURCE_CLAUSE',
                         'source_domain': 'GUARANTEE_SCOPE',
                         'supported_elements': ['guarantee_scope_boundary'],
                         'evidence_id': f'GUA-SCOPE-{clause.clause_id}-{len(rows)}'})
    return rows


def apply_scope(items, clauses):
    from review_v2.engine import _set_item_pass
    evidence = scope_evidence(clauses)
    if not evidence:
        return items
    for item in items:
        if item.node_id != 'guarantee_scope_exclusions':
            continue
        item.decision_trace['guarantee_scope_elements'] = [{
            'element_id': 'guarantee_scope_boundary', 'proposition': '保证范围或责任上限已明确',
            'terms': ['最高保证金额', '最高保证额', '保证金额', '保证责任上限', '保证范围', '全部承担']}]
        _set_item_pass(item, [], '合同已明确保证范围、责任金额上限或超出范围不承担责任的边界。',
                       '保证范围边界已有直接条款，不要求另行重复列明限制。')
        item.evidence_clauses = [dict(row) for row in evidence]
        item.evidence_location = '；'.join(dict.fromkeys(row['location'] for row in evidence))
        item.suggested_clause_example = ''
        item.legal_consequence_if_missing = '无独立修改缺口。'
        item.needs_manual_review = False
        item.judge_source = 'guarantee_scope_fact'
    return items
