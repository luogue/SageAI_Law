"""Company organs, financing constraints and performance-stage facts.

Predicates concern legal relationships, never fixture names, amounts or dates.
"""
import re


NO_ORGAN = r'(?:公司|本公司)[，,\s]*(?:不设|不设置|不设立)股东会(?!会议)'

def organ_prerequisites(text):
    identity = '\n'.join(s for s in re.split(r'[。；\n]', text) if not re.search(r'若|如|变更为|导致|转让后', s))
    single = bool(re.search(r'(?:只有|仅有|仅设|唯一|一个|一名)股东|一人(?:有限责任)?公司', identity))
    multiple = bool(re.search(r'(?:两|二|三|多|2|3)名股东|多股东|甲[、，]?乙双方(?:股东|共同投资)|甲乙双方(?:股东|共同投资)', identity)) or all(re.search(p, identity) for p in (r'甲方[^。\n]{0,35}出资', r'乙方[^。\n]{0,35}出资'))
    return {'limited_liability_company': bool(re.search(r'有限责任公司|有限公司', identity)),
            'multiple_shareholders': multiple and not single, 'no_shareholder_organ': bool(re.search(NO_ORGAN, text))}

def risk_atom(kind, c, summary):
    definitions = {
        'absent_shareholder_organ': ('股东会机关设置冲突', 'organ_legality', 'retain_shareholder_organ', '保留多股东有限责任公司的股东会机关，区分机关设置与全体股东书面一致决定时可不召开会议'),
        'unilateral_reserved_decision': ('重大事项单方决定权冲突', 'reserved_decision_authority', 'restrict_unilateral_reserved_decisions', '删除或限制重大事项的单方最终决定及跳过协商授权，明确合法表决与僵局解决机制'),
    }
    title, exposure, remedy, recommendation = definitions[kind]
    return dict(fact=kind, scope='primary_company_governance', actor='company_shareholders', object='reserved_corporate_decisions',
                legal_exposure=exposure, remedy=remedy, evidence_ids=[c.clause_id], title=title,
                parent_title='公司重大事项治理与股东会机制冲突', summary=summary, recommendation=recommendation)


def governance_evidence(node, clauses):
    rows = [c for c in clauses if c.section_type in {'正式合同条款', '附件'}]
    text = '\n'.join(c.text for c in rows)
    prerequisites = organ_prerequisites(text)
    result = []
    for c in rows:
        reason = ''
        atom_kind = None
        if node in {'formation_governance', 'formation_no_shareholder_organ', 'formation_unilateral_control'}:
            if node != 'formation_unilateral_control' and all(prerequisites.values()) and re.search(NO_ORGAN, c.text):
                atom_kind = 'absent_shareholder_organ'
                reason = '多股东有限责任公司约定不设股东会，混淆公司权力机关与会议形式。全体股东书面一致决定可以不召开会议，不等于不设股东会；另有例会不能消除该矛盾。'
            if node in {'formation_governance', 'formation_unilateral_control'} and re.search(r'(?:由甲方|由乙方|任一方)[^。；\n]{0,60}(?:最终决定|最终决策)|(?:甲方|乙方)[^。；\n]{0,85}不经[^。；\n]{0,20}直接决定', c.text):
                atom_kind = 'unilateral_reserved_decision'
                reason = '重大事项共同决策与单方最终决定或跳过协商的授权相冲突，不能仅因存在表决条款认定治理安排全部通过。'
        elif node == 'formation_capital_increase':
            locked = re.search(r'(?:股份|股权|持股)比例[^。\n]{0,15}(?:保持不变|不得改变|固定不变)', text)
            if locked and re.search(r'(?:不得|禁止|不能)(?:用|采用|通过)?股权投资|不得[^。\n]{0,12}股权融资', c.text):
                exception = bool(re.search(r'全体股东同意[^。\n]{0,45}其他[^。\n]{0,15}增资', text))
                reason = '持股比例锁定并限制股权融资，未跟投时可能限制融资选择并形成融资僵局。' + ('另有全体股东同意的调整出口，但仍依赖一致同意，建议明确无法一致时的融资及退出路径。' if exception else '建议约定未跟投的调整、稀释或其他融资退出路径。')
        if reason:
            result.append({**c.to_public_dict(), 'quote': c.text, 'quoted_text': c.text, 'original_excerpt': c.text, 'reason': reason, **({'adverse_fact_atom': risk_atom(atom_kind, c, reason)} if atom_kind else {})})
    return result


def contribution_requirements(requirements, text):
    """Payment proof is external evidence, not mandatory drafting content."""
    result = []
    completed = bool(re.search(r'(?:已经|已)(?:全部|足额|完成)?(?:实缴|缴纳出资|缴付出资)|实缴完毕', text))
    for original in requirements:
        row = dict(original)
        if row['element_id'] == 'formation_contributions_4':
            if not completed:
                continue
            row.update(requirement_kind='EXTERNAL_VERIFICATION', fact_type='actual_payment',
                       verification_instruction='合同声明已实缴，履行阶段核验银行流水、财务记录或资产权属移转材料；未提供外部材料不等于合同条款缺失。',
                       verification_priority='LOW', risk_relevant=False)
        result.append(row)
    return result
