"""Factual inputs for the 18 non-atomic loan nodes; no model legal verdicts."""
from review_v2.unified_facts.schema import Concept, Module

# Descriptions specify observable arrangements, never ask the model whether a
# rule passes, a fee is excessive, a guarantee is valid or a debt is joint.
EXTRA = {
 'loan_contract_type_identification': (
    ('funds_return', 'boolean', '双方约定提供货币资金并返还本金的交易安排。'),),
 'loan_sale_security_distinction': (
    ('sale_security_nature', 'boolean', '买卖或转让仅作借款担保的明确约定。'),
    ('sale_security_no_automatic_title', 'boolean', '债务不履行时不直接归属担保物、依法清算的约定。')),
 'loan_relending_bank_loan_invalid': (
    ('bank_relending', 'boolean', '文本肯定叙述出借资金源自金融机构贷款后转贷；禁止、否认或合法资金承诺是EXPLICIT_NONE，不代表外部事实已证实。'),),
 'loan_professional_lender_invalid': (
    ('unlicensed_repeated_lending', 'boolean', '文本肯定叙述未取得放贷资格、为营利向不特定对象反复放贷的事实；否认或承诺不做此事是EXPLICIT_NONE。'),),
 'loan_illegal_purpose_known_invalid': (
    ('known_illegal_use', 'boolean', '文本肯定叙述出借人明知违法犯罪用途仍出借；或明确本笔资金用于违法犯罪。禁止违法用途是EXPLICIT_NONE。'),),
 'loan_principal_amount': (),  # typed money, not a topic-presence boolean
 'loan_deducted_interest_forbidden': (
    ('upfront_deduction', 'boolean', '实际约定从本金预扣利息或融资服务费。禁止预扣是EXPLICIT_NONE。'),),
 'loan_interest_lpr_cap': (),  # typed charge calculation below
 'loan_hidden_fee_over_cap': (
    ('financing_fee', 'boolean', '实际收取融资服务费、管理费、咨询费等；不包括实现债权费用、一般违约金和不收取费用的约定。'),),
 'loan_early_repayment_right': (
    ('early_permission', 'boolean', '合同是否允许借款人提前返还本金。明确禁止为PRESENT false并引用禁止原文。'),),
 'loan_unreasonable_early_repayment_penalty': (
    ('early_prohibited', 'boolean', '绝对禁止提前还款的约定。'),
    ('early_charge', 'boolean', '提前清偿需支付违约金、补偿金或手续费的肯定安排；免收是EXPLICIT_NONE，不评价高低。')),
 'loan_guarantee_type_joint_or_general': (
    ('guarantee_mode', 'enum', '具体约定的一般保证或连带责任保证；泛称保证不推定方式。'),),
 'loan_guarantee_period': (
    ('guarantee_term', 'duration', '明确的保证期间长度；保证至本息还清不能归一为期限。'),
    ('guarantee_term_start', 'string', '保证期间起算事件或日期。')),
 'loan_guarantee_scope': (
    ('guarantee_scope', 'string', '保证覆盖的债务项目及明确限制，不用其他人的付款义务代替。'),),
 'loan_spousal_joint_intent': (
    ('spouse_assent', 'boolean', '配偶实际共同签名或明确追认本笔债务；未来要求签名不等于已经签署。'),),
 'loan_daily_family_need': (
    ('family_use', 'string', '本笔资金用于家庭日常生活的具体用途。'),),
 'loan_joint_business_need': (
    ('joint_business_use', 'string', '夫妻共同经营项目、资金用途或共同受益的具体约定。'),),
 'loan_beyond_family_need_evidence': (
    ('joint_debt_proof', 'boolean', '本笔借款夫妻共同签署、追认，或共同生活经营用途证明的具体记载/凭据；未来补交不是已有证明。'),),
}


def extra_modules(parent):
    return [Module('credit.loan.rule.' + node, tuple(
        Concept('loan.' + key, kind, description,
                ('GENERAL', 'JOINT') if key == 'guarantee_mode' else ())
        for key, kind, description in specs), parent(node))
        for node, specs in EXTRA.items() if specs]


def node_concepts(node):
    from review_v2.loan_facts import PROFILES
    if node == 'loan_financial_private_distinction':
        return ('loan.lender_kind',)
    if node in PROFILES:
        return tuple('loan.element.' + e['element_id'] for e in PROFILES[node])
    if node == 'loan_principal_amount':
        return ('loan.principal',)
    if node == 'loan_interest_lpr_cap':
        return COST_CONCEPTS
    return tuple('loan.' + key for key, _, _ in EXTRA[node])


COST_CONCEPTS = ('loan.charges', 'loan.cost_components', 'loan.cost_cumulative',
    'loan.cost_replacement', 'loan.cost_exclusive', 'loan.cost_combined_cap', 'common.signing_date')
COST_MODULE = Module('credit.loan.charges', (
    Concept('loan.cost_components', 'loan_charge',
      '逐一提取实际收取的借期利息、逾期利息、违约金、融资费用。全部免责或禁止不算收费。'
      'kind=regular_interest/overdue_interest/penalty/financing_fee; charge_key是同一收费的稳定名称；'
      'base=PRINCIPAL（全部本金）/UNPAID_PRINCIPAL（未偿本金）/UNPAID_INTEREST（未付利息）/UNKNOWN；scope=LOAN_TERM表示仅借期内，OVERDUE表示从逾期起算至清偿，'
      'UNTIL_REPAYMENT表示从放款起持续到清偿（包括借期及逾期），UNKNOWN表示起止不明。'
      'scope由代码从accrual_window投影，不由模型输出。按value_schema提取明示的start_event/end_event。'
      'base也由代码处理，模型只输出base_expression原文短语；原文没有明确基数时base_expression=null。对象键严格按value_schema。'
      '不能仅因出现“至清偿”就推断从放款开始，也不能仅因另有逾期条款就推断到期停止。'
      'rate={state:PRESENT,percent:原始百分数,period:DAY/MONTH/YEAR/ONCE}；按一次违约收取本金百分比的period为ONCE，绝不年化或伪造日/月单位。相对借期利率使用'
      '{state:PRESENT,multiplier:倍数,reference:REGULAR_RATE}；无法确定的金额/公式使用{state:UNKNOWN}，'
      '未来另定用{state:DEFERRED}。不要猜本金基数，不要年化，不合并不同费用。', multiple=True),
    Concept('loan.cost_cumulative', 'boolean', '明确约定逾期后借期利息和逾期责任继续叠加计收。'),
    Concept('loan.cost_replacement', 'boolean', '明确约定逾期责任替代借期利息，借期利息停止计收。'),
    Concept('loan.cost_exclusive', 'boolean', '逾期收费明确择一主张、不得同时计收。'),
    Concept('loan.cost_combined_cap', 'boolean', '全部实际融资收费合计明确受合同成立时一年期LPR四倍限制；只限制单项利息而另有其他费用不算合计限制。'),
), (('loan.charges', True),))
