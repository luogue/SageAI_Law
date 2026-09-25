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
    if node == 'oral_contract_evidence':
        oral = bool(re.search(r'未签.{0,5}书面合同|仅.{0,4}口头|口头委托', text))
        written = bool(re.search(r'第[一二三四五六七八九十\d]+条', text) and
                       re.search(r'本合同|双方签署|盖章', text))
        return not (written and not oral), ('已有明确书面合同文本，口头行纪证据专项审查不适用。'
                if written and not oral else '口头委托或书面合同状态尚待确认，核验行纪关系证据。')
    patterns = {
        'special_goods_license': r'食品|药品|危险品|危险化学品|二手车|进出口|报关|特殊经营许可',
        'perishable_goods_emergency_disposal': r'易腐烂|易变质|容易腐烂|容易变质|价值快速减损|价值明显减损',
    }
    if node in patterns:
        exists = any(re.search(patterns[node], s) and not re.search(r'不涉及|不属于|并非|非易', s)
                     for s in re.split(r'[。；\n]', text))
        return exists, ('已识别专项商品或交易前提。' if exists else '未识别本专项商品或交易前提，不纳入必备要素审查。')
    if node not in INTERVENTION:
        return None
    exists = any(re.search(SELF, s) and not re.search(r'不得|禁止|不允许', s)
                 for s in re.split(r'[。；\n]', text))
    return exists, ('已识别自行作为买受人或出卖人的介入安排。' if exists else
                    '未识别行纪人自行作为买受人或出卖人的介入安排，不启动介入交易专项完整性审查；普通第三方交易不等于介入交易。')


def apply(items, clauses):
    from review_v2.engine import _set_item_pass, _set_item_partial, _set_item_not_applicable, _set_item_missing
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
        elif item.node_id in {'principal_provide_information', 'goods_defect_disclosure'}:
            profiles = [('principal_defect_disclosure', '委托人主动告知货物瑕疵及交易限制',
                         r'委托人[^。；]{0,30}(?:应|须|有义务)[^。；]{0,15}(?:披露|告知|说明)[^。；]{0,30}(?:瑕疵|质量缺陷|权利限制|危险)')]
            if item.node_id == 'principal_provide_information':
                profiles += [
                    ('principal_information_delivery', '委托人提供委托物资料', r'委托人[^。；]{0,20}(?:应|须)[^。；]{0,15}提供[^。；]{0,25}(?:资料|证明|说明书|检验报告)'),
                    ('principal_defect_liability', '委托物瑕疵或违法问题的责任承担', r'委托人提供[^。；]{0,100}(?:质量缺陷|侵权|违法)[^。；]{0,100}委托人承担'),
                ]
        elif item.node_id == 'principal_instruction_response':
            profiles = [('principal_instruction_deadline', '委托人对交易调整或处分请求的答复期限',
                         r'(?:价格调整|价格变更|瑕疵处分|取回|请求.{0,6}指示)[^。；]{0,100}委托人[^。；]{0,30}(?:\d+|[一二三五十]+).{0,8}(?:小时|日|天)[^。；]{0,15}(?:答复|回复)')]
        elif item.node_id == 'commission_agent_identity_separation':
            profiles = [
                ('commission_business_separate_management', '委托物及交易资料与自营业务分别管理', r'(?:委托物|货物|交易资料)[^。；]{0,60}(?:分别管理|分开管理|隔离管理)'),
                ('commission_business_separate_accounts', '行纪价款与自营业务分别记账核算', r'(?:价款|货款|行纪事务|行纪业务)[^。；]{0,60}(?:分别记账|独立核算|分账|分别核算)'),
            ]
        elif item.node_id == 'commission_agent_trade_qualification':
            profiles = [('agent_current_trade_qualification', '行纪人具备本交易经营资格的确认',
                         r'行纪人[^。；]{0,20}(?:承诺|保证|确认|具备|具有|持有)[^。；]{0,45}(?:经营范围|营业执照|贸易资格|经营资格|经营资质)')]
        elif item.node_id == 'commission_deposit_right':
            profiles = [('agent_deposit_right', '受领或取回障碍下行纪人依法提存的安排',
                         r'(?:拒绝受领|拒绝取回|无法受领|逾期.{0,6}取回)[^。；]{0,100}行纪人[^。；]{0,20}(?:可|有权)[^。；]{0,10}提存')]
        elif item.node_id == 'defective_goods_disposal':
            profiles = [
                ('defective_goods_notice', '发现委托物瑕疵时通知委托人', r'(?:瑕疵|质量问题|数量短缺|型号不符|明显破损)[^。；]{0,70}(?:应|须)[^。；]{0,30}通知委托人'),
                ('defective_goods_authorized_disposal', '瑕疵物依委托人指示或同意处分', r'(?:瑕疵|质量问题|不符合交易要求)[^。；]{0,70}委托人(?:同意|指示)[^。；]{0,25}处分'),
                ('defective_goods_proceeds', '瑕疵物处分所得向委托人交付', r'(?:瑕疵|质量问题)[^。；]{0,70}(?:所得|价款)[^。；]{0,30}(?:转交|交付|支付|归)委托人'),
            ]
        elif item.node_id == 'termination_right_reference_mandate':
            profiles = [('discretionary_termination', '不以特定违约事由为前提的任意解除安排',
                         r'(?:任何一方|双方|委托人|行纪人)[^。；]{0,15}(?:有权|可以|可)[^。；]{0,15}(?:随时|任意|无需理由|无须理由)[^。；]{0,15}(?:解除|终止)')]
        elif item.node_id == 'third_party_default_liability':
            profiles = [
                ('third_party_default_notice', '第三人不履行义务时通知委托人', r'第三[方人][^。；]{0,30}不履行[^。；]{0,70}通知委托人'),
                ('third_party_default_mitigation', '第三人不履行义务时催收或保全', r'第三[方人][^。；]{0,30}不履行[^。；]{0,100}(?:催收|保全)'),
                ('third_party_default_compensation', '第三人不履行致委托人受损时行纪人承担赔偿责任', r'第三[方人][^。；]{0,30}(?:不履行|违约)[^。；]{0,80}行纪人(?:应|须|负责|向委托人|承担|赔偿)[^。；]{0,30}(?:赔偿责任|赔偿损失|承担赔偿)'),
            ]
        elif item.node_id == 'third_party_credit_review':
            profiles = [
                ('credit_risk_notice', '发现第三人履约能力或欺诈风险后的通知', r'行纪人发现第三[方人][^。；]{0,80}(?:无履约能力|欺诈)[^。；]{0,80}通知委托人'),
                ('credit_due_diligence', '选择交易第三人时核验资信和履约能力', r'行纪人[^。；]{0,30}(?:应|须)[^。；]{0,30}(?:核验|审查|调查)[^。；]{0,30}(?:资信|履约能力|信用)'),
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
        else:
            reason = '尚需明确：' + '；'.join(p for _, p, _ in profiles) + '。'
            _set_item_missing(item, item.risk_level, reason, reason, 'commission_direct_evidence')
        item.evidence_clauses = sources
        item.evidence_location = '；'.join(dict.fromkeys(e['location'] for e in sources))
        if item.node_id == 'defective_goods_disposal' and covered and len(covered) < len(profiles):
            from review_v2.engine import _specific_gap_consequence
            item.legal_consequence_if_missing = _specific_gap_consequence(item, '')
    return items
