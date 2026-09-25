"""Ordinary-loan dynamic schema and verified compatibility projections."""
from review_v2.unified_facts.schema import COMMON, Concept, Module, Schema
from review_v2.unified_facts.store import fail

RELATIONSHIPS = {
    'guarantee': '当前是否已有第三方作为保证人向债权人承诺在债务人不履行时承担从属性保证责任。保险人承担保险赔付责任不属于此种保证人责任。拟另签保证、模板或可选提示不是当前保证。',
    'security': '当前借款是否实际设定抵押权、质权或保证人的保证债务；仅有保险理赔的风险转移安排不属于这些担保关系。区分未来拟提供担保。',
    'refinancing': '当前借款是否用于归还旧借款，不是禁止借新还旧的表述。',
    'sale_security': '是否用买卖或回购交易担保借款，不把一般担保或用途描述当成买卖担保。',
    'extension': '是否明确约定允许申请展期及相应展期安排。',
    'extension_excluded': '是否明确排除或禁止申请展期。',
    'early_repayment': '是否约定提前归还或结清借款的安排。',
    'household': '借款是否明确用于家庭日常生活。',
    'joint_business': '借款是否明确用于夫妻共同生产经营。',
    'spouse': '借款是否涉及配偶身份、共同意思表示或相应债务承担。',
    'compound': '是否存在实际计收复利的安排，须有计收行为及未付利息基数、利率/周期等计算条件。清偿顺序列出复利不构成实际计收安排；明确不计收为EXPLICIT_NONE。',
    'limitation_risk': '是否明确记载催收或行权已经超过、临近时效/保证期间等实际时间事实，不作法律时效判断。',
    'voucher_mechanism': '是否有借据、放款回单或系统放款记录等债权或支付凭证机制。预计日期、受托支付、账户、扣收授权仅是履行安排，不是凭证机制；必须引用对应凭证机制原文。',
    'debt_instrument': '是否存在已出具或具体约定出具的借据、借条、欠条、收据等债权凭证。',
}


def element_concept(element_id):
    return 'loan.element.' + element_id


def _parent(node):
    if node == 'loan_sale_security_distinction':
        return (('loan.sale_security', True),)
    if node == 'loan_unreasonable_early_repayment_penalty':
        return (('loan.early_repayment', True),)
    from review_v2.loan_facts import GUARANTEE_NODES, HOUSEHOLD_NODES, JOINT_BUSINESS_NODES, SPOUSE_NODES
    if node.startswith('loan_extension_'):
        return (('loan.extension', True),) + ((('loan.guarantee', True),) if 'guarantor' in node else ())
    if node.startswith('loan_early_repayment_'):
        return (('loan.early_repayment', True),)
    if node in GUARANTEE_NODES:
        return (('loan.guarantee', True),)
    if node == 'loan_old_for_new_guarantor_notice':
        return (('loan.refinancing', True), ('loan.guarantee', True))
    if node == 'loan_guarantee_attachment':
        return (('loan.security', True),)
    if node in HOUSEHOLD_NODES:
        return (('loan.household', True),)
    if node in JOINT_BUSINESS_NODES:
        return (('loan.joint_business', True),)
    if node in SPOUSE_NODES:
        return (('loan.spouse', True),)
    if node == 'loan_compound_interest_limit':
        return (('loan.compound', True),)
    return ()


def schema():
    from review_v2.loan_facts import PROFILES
    from review_v2.unified_facts.loan_bindings import extra_modules, COST_MODULE
    root = Module('credit.loan.relationships', (
        Concept('loan.lender_kind', 'enum', '贷款人主体性质，名称不足以确认时为UNCERTAIN。', ('natural', 'enterprise', 'financial')),
        Concept('loan.borrower_kind', 'enum', '借款人主体性质，不能用收款银行身份代替借款人。', ('natural', 'enterprise', 'financial')),
        *(Concept('loan.' + key, 'boolean', description) for key, description in RELATIONSHIPS.items()),
        Concept('loan.charges', 'boolean', '本合同存在实际计收的利息、逾期利息、违约金或融资费用；未来触发逾期计息也是当前已约定的收费机制。全部无息且无任何收费时为EXPLICIT_NONE。'),
    ))
    shared = Module('credit.loan.amounts_dates', (
        Concept('loan.principal', 'money', '合同约定借款本金，保留币种，不减去预扣费用。'),
        Concept('loan.delivered_principal', 'money', '原文明确的实际到账或交付本金，不通过合同金额猜测。'),
        Concept('loan.maturity_date', 'date', '借款到期日，未明确具体日期则不生成日期。'),
        Concept('loan.duration', 'term', '借款期限。明确长度用amount/unit；只有完整起止日期时用start_date/end_date，不计算年/月/天数。'),
        Concept('loan.regular_rate', 'number', '借期内约定利率的百分数数值；不要与逾期或违约金混淆，不年化。'),
        Concept('loan.regular_rate_period', 'enum', '该借期内利率的期间单位。', ('DAY', 'MONTH', 'YEAR')),
        Concept('loan.day_count_basis', 'enum', '原文明示的年利率转日利率分母：360天为ACT_360，365天为ACT_365，明确按当年实际天数为ACT_ACT。未约定不得假定365。', ('ACT_360','ACT_365','ACT_ACT')),
    ))
    # Reuse existing atomic propositions, not regex patterns or legal verdicts.
    # A shared element belongs to the least restrictive of its consumer scopes.
    elements, parents = {}, {}
    for node, specs in PROFILES.items():
        for spec in specs:
            key = spec['element_id']
            elements[key] = Concept(element_concept(key), 'boolean',
                '是否存在以下具体合同安排（不是法律裁决或主题词命中）：' + spec['proposition'] +
                (' 通知期限不等于通知渠道；提前若干日通知只能证明期限，渠道须有明确书面/短信/电子/口头等方式的原文。' if key.endswith('_channel') else ''))
            parents.setdefault(key, []).append(_parent(node))
    groups = {}
    for key, requirements in parents.items():
        # An unconditional consumer needs the fact even if another consumer is conditional.
        common = set(requirements[0]).intersection(*map(set, requirements[1:]))
        groups.setdefault(tuple(sorted(common)), []).append(elements[key])
    modules = [shared] + [Module('credit.loan.elements.' + str(i), tuple(specs), required)
                          for i, (required, specs) in enumerate(sorted(groups.items()))]
    return Schema('credit.loan', (COMMON, root), modules + extra_modules(_parent) + [COST_MODULE])


def project_shared(store):
    """Reuse LoanFacts.applicability unchanged, with explicit uncertainty handling."""
    from review_v2.loan_facts import LoanFacts, PROFILES
    if store.schema.family != 'credit.loan' or not store.is_verified:
        fail('VERIFIED_LOAN_STORE_REQUIRED')
    values, evidence, states = {}, {}, {}
    for name in ('lender_kind', 'borrower_kind', *RELATIONSHIPS):
        concept = 'loan.' + name
        rows = store.get(concept, consumer='LoanFacts.applicability')
        state = store.state(concept)
        states[name] = state
        evidence[name] = list(dict.fromkeys(e['clause_id'] for f in rows for e in f['evidence']))
        if name in {'lender_kind', 'borrower_kind'}:
            values[name] = store.scalar(concept, consumer='LoanFacts.party_kind') if state == 'PRESENT' else 'unknown'
        else:
            values[name] = store.scalar(concept, consumer='LoanFacts.relationship') if state == 'PRESENT' else None if state in {'UNKNOWN', 'CONFLICT', 'UNCERTAIN', 'DEFERRED'} else False
    values['party_type'] = ('natural_person' if values['lender_kind'] == values['borrower_kind'] == 'natural'
                           else 'mixed' if values['lender_kind'] != values['borrower_kind'] else values['lender_kind'])
    values['lender_party_type'], values['borrower_party_type'] = values['lender_kind'], values['borrower_kind']
    if values['extension_excluded'] is True:
        values['extension'] = False
    for name, node in {'maturity': 'loan_repayment_deadline', 'agreed_rate': 'loan_interest_rate_agreed'}.items():
        concepts = [element_concept(e['element_id']) for e in PROFILES[node]]
        records = [f for c in concepts for f in store.get(c, consumer=node)]
        values[name] = any(f.get('normalized_value') is True for f in records)
        states[name] = 'UNKNOWN' if any(store.state(c) in {'UNKNOWN', 'CONFLICT', 'UNCERTAIN', 'DEFERRED'} for c in concepts) else 'PRESENT' if values[name] else 'ABSENT'
        evidence[name] = evidence_for(store, node)
    result = LoanFacts(values, evidence, list(store.clause_ids))
    result.verified_states = states
    result.verified_store = store
    result.verified_concept_keys = {name: 'loan.' + name for name in ('lender_kind', 'borrower_kind', *RELATIONSHIPS)}
    result.verified_concept_keys.update(maturity=element_concept('loan_maturity'), agreed_rate=element_concept('loan_agreed_rate'))
    return result


def evidence_for(store, node):
    from review_v2.loan_facts import PROFILES
    if node not in PROFILES:
        fail('UNMIGRATED_LOAN_EVIDENCE_CONSUMER', node)
    evidence = {}
    for spec in PROFILES[node]:
        key = spec['element_id']
        for fact in store.get(element_concept(key), consumer=node):
            if fact['state'] != 'PRESENT' or fact['normalized_value'] is not True:
                continue
            for ref in fact['evidence']:
                identity = (ref['clause_id'], ref['source_start'], ref['source_end'])
                row = evidence.setdefault(identity, {
                    **ref, 'text': ref['quote'], 'location': ref['section'],
                    'source_type': 'VERIFIED_FACT', 'evidence_id': fact['fact_id'] + ':' + str(ref['source_start']),
                    'structured_fact_ids': [], 'supports_element_ids': [], 'entailment_status': 'SUPPORTS'})
                row['structured_fact_ids'].append(fact['fact_id'])
                row['supports_element_ids'].append(key)
    return list(evidence.values())


def migration_inventory():
    from review_v2.loan_facts import PROFILES
    from review_v2.loan_contract_checklist import LOAN_REVIEW_CHECKLIST
    from review_v2.unified_facts.loan_bindings import EXTRA
    return {'status': 'ACTIVE', 'migrated_fact_consumers':
        ['LoanFacts.applicability', 'loan_rules.evaluate', 'loan_costs.analyze', 'loan_pipeline.report'],
        'atomic_coverage_nodes': sorted(PROFILES),
        'unmapped_rule_nodes': [c.node_id for c in LOAN_REVIEW_CHECKLIST if c.node_id not in PROFILES and c.node_id not in EXTRA],
        'blocked_legacy_stages': ['extract_contract_fact_graph', 'loan_facts.units',
            'loan_costs.analyze_costs', 'loan_facts.negative_scan', 'legacy per-rule/raw-text postprocessing'],
        'consumer_migration_complete': True}
