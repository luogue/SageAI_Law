"""Gift semantic facts, shared prerequisites and directly bound requirements."""
import re

# Predicates express transactions, not incidental cost/material vocabulary.
PREDICATES = {
    'notarized': (r'(?:本合同|本赠与|赠与合同).{0,12}(?:已经|已|经过|经).{0,8}公证|公证书编号', '赠与已经公证'),
    'public_moral': (r'(?:赠与|捐赠).{0,30}(?:用于救灾|用于扶贫|用于助残|具有公益|道德义务)|(?:公益|慈善|道德义务)(?:性质)?赠与', '存在公益或道德义务性质赠与'),
    'attached': (r'(?<!不)附义务赠与|(?:受赠人|乙方).{0,20}(?:应|须|承诺).{0,12}(?:赡养|扶养|照护|照顾|供养)|(?:以|作为).{0,25}(?:照护|赡养|履行特定义务).{0,12}(?:条件|前提)', '存在赠与附加的实质义务'),
    'support': (r'(?:受赠人|乙方).{0,20}(?:负有|承担|履行).{0,12}(?:扶养|赡养|抚养)义务', '受赠人对赠与人负有扶养义务'),
    'registered': (r'不动产|房屋|股权|车辆|过户', '赠与标的涉及登记'),
    'waiver': (r'永(?:无|不)反悔|绝不反悔|不再反悔|不得反悔|放弃.{0,8}撤销权|不得.{0,8}撤销|不可撤销', '存在撤销权限制或放弃安排'),
    'poverty': (r'经济状况显著恶化|穷困抗辩|资力不足.{0,20}(?:停止|暂停|不再)履行', '存在穷困抗辩安排或事实'),
    'installments': (r'分期赠与|持续赠与|分批赠与|每(?:月|年).{0,20}赠与', '存在分期或持续赠与'),
    'defect_guarantee': (r'保证.{0,12}(?:无瑕疵|无缺陷|质量合格)', '赠与人作出无瑕疵质量保证'),
    'attachment': (r'附件(?:清单|[一二三四五六七八九十\d]+[:：、])|本合同附件', '合同设置附件'),
}

# Every rule is explicitly classified below: unconditional, or a fact prerequisite.
CONDITIONS = {
    'G-03-01': 'notarized', 'G-03-02': 'public_moral', 'G-03-03': 'attached',
    'G-03-04': 'registered', 'G-04-02': 'irrevocable', 'G-04-03': 'waiver',
    'G-05-02': 'support', 'G-05-03': 'attached',
    'G-07-02': 'poverty', 'G-07-03': 'installments',
    'G-08-01': 'notarized', 'G-08-02': 'public_moral', 'G-08-03': 'irrevocable',
    **{f'G-09-0{i}': 'attached' for i in range(1, 5)},
    'G-10-03': 'defect_guarantee', 'G-10-04': 'attached',
    'G-12-03': 'formalities', 'G-12-04': 'attachment',
}


def extract_facts(clauses):
    facts = {}
    for key, (pattern, label) in PREDICATES.items():
        evidence, unresolved = [], False
        for c in clauses:
            for sentence in re.split(r'[。；\n]', c.text):
                if not re.search(pattern, sentence):
                    continue
                if re.search(r'是否|待确认|待核验|尚未确定', sentence):
                    unresolved = True
                    continue
                if re.search(r'不附义务|非公益|不属于.{0,8}(?:公益|道德)|未经公证|未公证', sentence):
                    continue
                if re.search(r'^(?:如|若|如果)|(?:如|若)属于', sentence.strip()):
                    continue
                evidence.append(dict(clause_id=c.clause_id, location=c.location, quote=sentence))
        facts[key] = dict(value=True if evidence else None if unresolved else False,
                          label=label, evidence=evidence,
                          searched_clause_ids=[c.clause_id for c in clauses])
    for key, inputs in {'irrevocable': ['notarized', 'public_moral'],
                        'formalities': ['notarized', 'registered']}.items():
        values = [facts[k]['value'] for k in inputs]
        facts[key] = dict(value=True if True in values else None if None in values else False,
                          label='或'.join(facts[k]['label'] for k in inputs),
                          evidence=[e for k in inputs for e in facts[k]['evidence']])
    return facts


ACCEPTANCE = r'(?:受赠人|乙方).{0,25}(?:自愿|同意|表示|承诺|确认).{0,15}接受.{0,50}赠与'
WAIVER = PREDICATES['waiver'][0]
PRESERVE_STATUTORY = r'(?:不影响|保留|仍可|仍有权).{0,35}法定撤销|法定撤销权.{0,10}(?:不受影响|予以保留)'
PROFILES = {
    'gift_delivery_deadline_method': [
        ('delivery_method', '赠与财产交付或登记方式', r'(?:办理|完成).{0,15}(?:转移登记|过户)|(?:转账|实物交付|移交钥匙)'),
        ('delivery_deadline', '赠与财产交付或登记具体期限', r'(?:生效|签订|签署).{0,12}[0-9一二三四五六七八九十百]+(?:个工作)?日内.{0,25}(?:交付|登记|过户)|[0-9]{4}年[0-9]{1,2}月[0-9]{1,2}日.{0,10}(?:交付|登记|过户)')],
    'gift_return_after_revocation': [('revocation_return', '依法撤销后返还赠与财产', r'(?:撤销|撤回).{0,35}(?:返还|恢复原状)')],
    'gift_return_costs': [('revocation_return_cost', '撤销返还费用的承担安排', r'(?:撤销|返还).{0,40}(?:费用|税费|运输费|保管费).{0,20}(?:承担|支付|负担)')],
    'gift_donee_acceptance': [('donee_acceptance', '受赠人接受赠与的意思表示', ACCEPTANCE)],
    'gift_notarized_type': [('notarization_completed', '赠与已经完成公证', PREDICATES['notarized'][0])],
    'gift_arbitrary_revocation_before_transfer': [('revocation_arrangement', '权利转移前撤销或放弃撤销的安排', r'权利转移.{0,15}前.{0,20}撤销|'+WAIVER)],
    'gift_waiver_arbitrary_revocation': [('revocation_waiver', '放弃或限制任意撤销的意思表示', WAIVER)],
    'gift_property_list_attachment': [('property_attachment', '实际财产清单附件', r'(?:附件[一二三四五六七八九十\d]*[:：、\s]+|附件清单[:：]).{0,25}财产清单')],
    'gift_title_certificate_attachment': [('title_attachment', '实际权属证明附件', r'(?:附件[一二三四五六七八九十\d]*[:：、\s]+|附件清单[:：]).{0,25}(?:权属证明|权属证书|产权证|不动产权证)')],
    'gift_notary_tax_registration_materials': [('formalities_material_list', '公证或登记办理材料清单', r'(?:附件[一二三四五六七八九十\d]*[:：、\s]+|材料清单[:：]).{0,35}(?:公证|登记|身份证明|权属)')],
    'gift_obligation_value_proportion': [('obligation_value', '附义务成本或负担与赠与价值的比例边界', r'(?:所负义务|义务履行成本|义务价值).{0,40}(?:不超过|相当|比例|限度)')],
}


def apply(items, clauses):
    from review_v2.utility_supply_evidence import _set_atomic_item, _set_adverse_if_found
    from review_v2.engine import _apply_review_nature_outcomes
    for item in items:
        if item.coverage_status in {'不适用', 'NOT_APPLICABLE', 'INSUFFICIENT_CONTEXT'}:
            continue
        statutory = item.decision_trace.get('review_nature') == 'STATUTORY_DEFAULT'
        if item.node_id in PROFILES and (not statutory or item.decision_trace.get('linked_adverse_rules')):
            _set_atomic_item(item, PROFILES[item.node_id], clauses)
        if item.node_id in {'gift_statutory_revocation_one_year', 'gift_heir_revocation_six_months'}:
            validate_revocation_period(item, clauses)
        if item.node_id == 'gift_waiver_statutory_revocation_overbroad':
            # A reservation of statutory revocation prevents interpreting the
            # same unrestricted wording as a total waiver.
            if not any(re.search(PRESERVE_STATUTORY, c.text) for c in clauses):
                _set_adverse_if_found(item, clauses, assessment=(
                    WAIVER,
                    '合同存在概括性不反悔或不可撤销承诺，未区分任意撤销与法定撤销，存在过度排除法定救济的解释风险。'))
        if item.node_id in PROFILES or item.node_id == 'gift_waiver_statutory_revocation_overbroad':
            item.decision_trace.pop('priority_assessment', None)
    return _apply_review_nature_outcomes(items)


def validate_revocation_period(item, clauses):
    """A stated period is checked; an unstated statutory period is not a gap."""
    from review_v2.utility_supply_evidence import _set_adverse_if_found
    heirs = item.node_id == 'gift_heir_revocation_six_months'
    expected = 6 if heirs else 12
    numbers = {'一':1,'二':2,'两':2,'三':3,'六':6,'十二':12,'十':10}
    for clause in clauses:
        for sentence in re.split(r'[。；\n]', clause.text):
            if '撤销' not in sentence or ('继承人' in sentence or '法定代理人' in sentence) != heirs:
                continue
            if not heirs and not re.search(r'法定|撤销事由|除斥', sentence):
                continue
            for match in re.finditer(r'(\d+|十二|[一二两三六十])(?:个)?(月|年)(?:内|期间|期限)', sentence):
                n = int(match[1]) if match[1].isdigit() else numbers[match[1]]
                months = n * (12 if match[2]=='年' else 1)
                if months != expected:
                    _set_adverse_if_found(item, clauses, assessment=(re.escape(sentence),
                        f'合同约定撤销权行使期间为{match[0]}，与适用的{expected}个月法定期间不一致。'))
