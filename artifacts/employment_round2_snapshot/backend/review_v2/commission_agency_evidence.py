"""Direct transaction evidence, distinguished from intervention and collusion."""
import re

INTERVENTION = {
    'intervention_right_condition', 'intervention_notice_disclosure',
    'intervention_remuneration', 'intervention_conflict_control',
}
OWN = r'以(?:行纪人)?自己(?:的)?名义.{0,35}(?:交易|销售|订立|买卖)'
SELF = r'(?:自己|自行|亲自)作为(?:买受人|出卖人|买方|卖方)|行使介入权'
COLLUSION = r'恶意串通|利益输送|虚假交易'


def prerequisite(text, node):
    if node not in INTERVENTION:
        return None
    exists = any(re.search(SELF, s) and not re.search(r'不得|禁止|不允许', s)
                 for s in re.split(r'[。；\n]', text))
    return exists, ('已识别自行作为买受人或出卖人的介入安排。' if exists else
                    '未识别行纪人自行作为买受人或出卖人的介入安排，不启动介入交易专项完整性审查；普通第三方交易不等于介入交易。')


def apply(items, clauses):
    from review_v2.engine import _set_item_pass, _set_item_partial, _set_item_not_applicable
    text = '\n'.join(c.text for c in clauses)
    for item in items:
        dep = prerequisite(text, item.node_id)
        if dep and not dep[0]:
            _set_item_not_applicable(item, dep[1])
            item.suggested_clause_example = ''
            item.needs_manual_review = False
            continue
        if item.node_id == 'malicious_collusion_with_third_party':
            adverse = [s for s in re.split(r'[。；\n]', text) if re.search(COLLUSION, s)
                       and not re.search(r'不得|禁止|严禁|防止|避免|不应', s)]
            if not adverse:
                _set_item_pass(item, [], '未发现约定恶意串通、利益输送或虚假交易的不利安排。',
                               '普通第三方交易授权不证明恶意串通。')
                item.evidence_clauses = []
                item.evidence_location = ''
                item.suggested_clause_example = ''
            continue
        profiles = []
        if item.node_id == 'own_name_trade':
            profiles = [('own_name_trade', '行纪人以自己的名义对外交易', OWN)]
        elif item.node_id == 'post_termination_settlement':
            profiles = [
                ('termination_liquidation', '合同解除后货物、货款、报酬及费用清算', r'(?:解除|终止)后.{0,100}(?:清算|结算)'),
                ('unsold_goods_return', '剩余待售货物返还', r'(?:尚未出售|未售出|未出售).{0,65}返还'),
                ('return_cost_allocation', '返还费用承担', r'返还.{0,20}费用.{0,30}承担'),
            ]
        if not profiles:
            continue
        specs = [dict(element_id=k, proposition=p, terms=[p], semantic_patterns=[pattern])
                 for k, p, pattern in profiles]
        item.decision_trace['semantic_requirements'] = specs
        sources = []
        covered = set()
        for c in clauses:
            keys = [k for k, _, pattern in profiles if re.search(pattern, c.text)
                    and not (k == 'own_name_trade' and re.search(r'不得.{0,8}以', c.text))]
            if keys:
                covered.update(keys)
                sources.append(dict(clause_id=c.clause_id, location=c.location, text=c.text,
                    quote=c.text, source_type='SOURCE_CLAUSE', supported_elements=keys,
                    evidence_id=f'CA-DIRECT-{item.node_id}-{c.clause_id}'))
        if len(covered) == len(profiles):
            _set_item_pass(item, [], '已覆盖：' + '；'.join(p for _, p, _ in profiles) + '。',
                           '上述要素均有对应原文支持。')
            item.suggested_clause_example = ''
        elif covered:
            missing = [p for k, p, _ in profiles if k not in covered]
            reason = '尚需明确：' + '；'.join(missing) + '。'
            _set_item_partial(item, [], item.risk_level, reason, reason)
            item.suggested_clause_example = '建议明确' + '；'.join(missing) + '。'
        item.evidence_clauses = sources
        item.evidence_location = '；'.join(dict.fromkeys(e['location'] for e in sources))
    return items
