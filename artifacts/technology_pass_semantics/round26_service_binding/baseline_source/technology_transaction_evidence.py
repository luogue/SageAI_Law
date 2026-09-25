"""Predicate-bearing transaction spans, shared by extraction and verification.

Classification is an inference over core performances, not over a fee mentioned
in a damages cap.  A component's sources are retained independently: finding an
invoice does not prove the amount, schedule, or change-price mechanism.
"""
import re

from review_v2.obligation_detail_elements import _segments


PARTY = r"(?:甲方|乙方|丙方|委托方|受托方|开发方|委托人|受托人|研究开发人|双方|各方)"
TECH = r"(?:技术|软件|系统|平台|算法|产品|工艺|设备|模型|数据库)"
RD = rf"(?:研究开发|研发|{TECH}.{{0,12}}(?:设计|开发)|(?:设计|开发).{{0,12}}{TECH})"
LIABILITY = r"违约金|赔偿|免责|责任上限|最高限额|逾期|迟延|无权|不得|不承担|不负责|承担.{0,20}损失"
COOPERATIVE = rf"(?:{PARTY}.{{0,25}}(?:共同|合作|联合)(?:研究开发|研发|开发)(?!经费|资金|项目)|(?:进行|开展|承担)(?:共同|合作|联合)(?:研究开发|研发|开发))"
NUMBER = r"(?:\d[\d,.]*|[壹贰叁肆伍陆柒捌玖拾佰仟万亿一二三四五六七八九十百]+)"

# Each entry is an independently verifiable predicate, not a topic query.
PREDICATES = {
    'rd_performance': rf"(?:{PARTY}.{{0,55}}(?:完成|负责|承担|进行|开展).{{0,35}}{RD}|委托.{{0,35}}(?:研究开发|研发|开发)|{COOPERATIVE}|(?:开发|研发)(?:目标|内容|范围)[：:].+)",
    'entrusted_direction': rf"(?:{PARTY}.{{0,30}}委托.{{0,30}}(?:研究开发|研发|开发)|乙方(?:应|须)?.{{0,10}}(?:根据|按照|依照)甲方.{{0,25}}(?:需求|要求|委托).{{0,30}}(?:开发|研发)|(?:委托方|受托方).{{0,40}}(?:委托开发|研发|开发任务))",
    'cooperative_direction': rf"{COOPERATIVE}|(?:双方|各方).{{0,20}}(?:共同投入|研发分工|开发分工)",
    'license_performance': r"(?:授予|许可).{0,25}(?:实施|使用).{0,30}(?:专利|技术|软件)|(?:许可方|甲方).{0,15}(?:授予|许可).{0,30}(?:许可权|实施权|使用权)",
    'transfer_performance': r"(?:专利权|专利申请权|技术秘密|技术成果).{0,35}(?:转让给|转移至|转让予)|(?:转让方|让与方|甲方).{0,20}(?:转让|转移).{0,30}(?:专利权|专利申请权|技术秘密|技术成果)",
    'consulting_performance': r"(?:提供|提交|出具|完成).{0,30}(?:技术咨询|咨询报告|可行性论证|技术预测|专题技术调查|分析评价报告)",
    'service_performance': rf"(?:提供|完成|负责|开展|承担).{{0,35}}(?:技术服务|技术支持|技术诊断|性能诊断|性能优化|故障处理|数据库分析|系统优化|参数调试)|技术服务(?:内容|目标|方式)[：:].+",
    'project': r"项目名称[：:].+|(?:开发|研发|技术)(?:项目|目标)[：:].+",
    'functions': r"(?:主要功能|主要模块|功能范围|技术范围|开发内容|研发内容|需求规格)[：：:].+|实现以下主要功能|(?:功能|模块).{0,20}以.{0,20}需求规格.{0,12}为准",
    'schedule': r"(?:阶段|最终版本|里程碑|开发期限|研发期限).{0,50}(?:\d{4}年|\d+月|日前|日内|个月|工作日).{0,30}(?:完成|交付|提交|验收)|(?:开发期限|研发期限|里程碑)[：:].{0,25}(?:\d|[一二三四五六七八九十]+)(?:年|月|日|个工作日|个月)",
    'deliverables': r"(?:交付|提交|提供).{0,35}(?:源代码|源程序|技术文档|开发成果|技术成果|设计文件)|(?:交付内容|交付成果)[：:].+",
    'acceptance': r"验收(?:标准|依据|条件|指标)[：:].+|(?:依据|按照|以).{0,35}(?:需求规格|技术指标|测试用例|技术方案).{0,20}(?:验收|为准)|(?:功能|性能).{0,25}(?:符合|达到).{0,25}(?:需求|指标|标准)|(?:系统|软件|平台)(?:应|须)(?:能够)?(?:完成|实现).{0,25}(?:列明|约定|规定).{0,15}(?:业务)?功能",
    'fee_total': rf"(?:开发费|研发费|研究开发经费|开发费用|合同总价|合同价款|开发经费).{{0,20}}(?:人民币)?{NUMBER}\s*万?元",
    'payment_schedule': rf"(?:支付|付款).{{0,25}}(?:{NUMBER}\s*%|{NUMBER}\s*万?元)|(?:{NUMBER}\s*%|{NUMBER}\s*万?元).{{0,25}}(?:支付|付款)",
    'change_price': r"(?:需求|项目|范围).{0,20}(?:变更|调整).{0,50}(?:费用|价款|报酬).{0,25}(?:调整|确认|协商|约定)|(?:费用|价款).{0,20}(?:根据|随).{0,20}(?:变更|调整)|(?:新增|增加|扩展).{0,30}(?:功能|模块|范围|需求).{0,35}(?:另行|重新)(?:确认|协商|约定).{0,12}(?:费用|价款|报酬)",
    'invoice': r"(?:开具|提供|出具).{0,20}发票",
    'account': r"(?:收款|开户|银行)账户[：:].+|(?:收款账号|银行账号|开户行)[：:].+|支付至.{0,20}(?:账户|账号)",
}

CLASSIFICATION_COMPONENTS = {
    'ENTRUSTED_DEVELOPMENT': ('rd_performance', 'entrusted_direction'),
    'COOPERATIVE_DEVELOPMENT': ('rd_performance', 'cooperative_direction'),
    'TECHNOLOGY_LICENSE': ('license_performance',),
    'TECHNOLOGY_TRANSFER': ('transfer_performance',),
    'TECHNICAL_CONSULTING': ('consulting_performance',),
    'TECHNICAL_SERVICE': ('service_performance',),
}
LABELS = {
    'rd_performance': '研究开发核心给付', 'entrusted_direction': '委托方提出需求、受托方承担开发的交易结构',
    'cooperative_direction': '共同研发交易结构', 'license_performance': '技术实施或使用权许可给付',
    'transfer_performance': '技术权利转让给付', 'consulting_performance': '技术咨询给付',
    'service_performance': '解决技术问题的服务给付',
    'project': '项目及目标', 'functions': '功能和技术范围', 'schedule': '开发期限及里程碑',
    'deliverables': '开发成果交付', 'acceptance': '验收标准', 'fee_total': '开发费用总额',
    'payment_schedule': '阶段付款金额及节点', 'change_price': '变更费用调整', 'invoice': '发票', 'account': '收款账户',
}
FAMILIES = {
    'technical_service_subject': (
        ('technical_service_scope', ('service_performance',)),
        ('technical_service_activities', ('service_activities',)),
        ('technical_service_deliverables', ('service_deliverables',)),
    ),
    'development_scope': (
        ('commissioned_project_and_objective', ('project',)),
        ('functional_and_technical_scope', ('functions',)),
        ('schedule_and_milestones', ('schedule',)),
        ('deliverables_and_acceptance', ('deliverables', 'acceptance')),
    ),
    'development_funding': (
        ('development_fee_total', ('fee_total',)),
        ('milestone_payment_schedule', ('payment_schedule',)),
        ('fee_adjustment', ('change_price',)),
        ('invoice_and_account', ('invoice', 'account')),
    ),
}

# The service producer already distinguishes activities from outputs. Publish
# those predicates with the transaction facts instead of passing retrieval hints.
PREDICATES.update({
    'service_activities': r'(?:通过|进行|提供|采用|开展|实施).{0,45}(?:技术诊断|系统分析|性能测试|算法优化|参数调试|软件调试|技术支持|性能诊断|数据库分析|SQL优化)',
    'service_deliverables': r'(?:提交|提供|交付|出具|形成).{0,100}(?:诊断报告|优化建议书|测试结果记录|技术优化报告|算法参数文件|测试记录|服务记录|故障处理记录|变更记录|操作手册|项目实施报告|培训材料)',
})
LABELS.update(service_activities='核心技术服务活动', service_deliverables='主要技术服务交付物')


def supports_component(key, text):
    compact = re.sub(r'\s+', '', text)
    if not re.search(PREDICATES[key], compact):
        return False
    # Do not treat references in a negative/remedial allocation as performance.
    if key not in ('invoice', 'account') and re.search(LIABILITY, compact):
        return False
    if key == 'deliverables' and re.search(r'不侵犯|合法知识产权|权利瑕疵|保证其|保证所', compact):
        return False
    if key == 'deliverables' and re.search(r'(?:提交|提供|交付)的.{0,15}(?:成果|代码|文档).{0,10}(?:如涉及|所涉|归属|所有权)', compact):
        return False  # An already supplied object's IP treatment is not delivery.
    if key == 'payment_schedule' and not re.search(r'签订|生效|阶段|验收|交付|首付|预付|尾款|前|后|日内|按月', compact):
        return False
    return True


def register_facts(graph, clauses):
    for clause, _, quote in _segments(clauses):
        if getattr(clause, 'block_type', '') in ('TITLE', 'HEADING'):
            continue
        for key in PREDICATES:
            if supports_component(key, quote):
                graph.add('technology.transaction.' + key, quote, clause, source_span=quote)
    # Numbered outputs keep the governing delivery verb in the exact span.
    # A warranty about supplied code is not itself an obligation to deliver it.
    from review_v2.obligation_detail_elements import _delivery_sources
    for clause, _, quote in _delivery_sources(clauses):
        if supports_component('deliverables', quote):
            graph.add('technology.transaction.deliverables', quote, clause, source_span=quote)
        if supports_component('service_deliverables', quote):
            graph.add('technology.transaction.service_deliverables', quote, clause, source_span=quote)
    # Scope and acceptance reviews consume the same verified quantitative
    # standard predicate, not two independently maintained label searches.
    from review_v2.obligation_detail_elements import development_acceptance_detail_elements
    by_id = {c.clause_id: c for c in clauses}
    for atom in development_acceptance_detail_elements(clauses):
        if atom['element_id'] == 'acceptance_metrics':
            for source in atom['supporting_evidence']:
                graph.add('technology.transaction.acceptance', source['quote'],
                          by_id[source['clause_id']], source_span=source['quote'])


def elements_from_graph(family, graph):
    if family.startswith('transaction_classification:'):
        subtype = family.split(':', 1)[1]
        specs = [('transaction_' + key, (key,)) for key in CLASSIFICATION_COMPONENTS.get(subtype, ())]
    else:
        specs = FAMILIES[family]
    elements = []
    for element_id, components in specs:
        sources, missing, fact_ids = [], [], []
        for component in components:
            facts = graph.facts.get('technology.transaction.' + component, [])
            if not facts:
                missing.append(LABELS[component])
            for fact in facts:
                fact_ids.append(fact.fact_id)
                sources.extend({'clause_id': cid, 'quote': span,
                                'component_key': component, 'fact_id': fact.fact_id}
                               for cid, span in zip(fact.source_clause_ids, fact.source_spans))
        state = 'PARTIALLY_COVERED' if sources and missing else 'COVERED' if sources else 'MISSING'
        label = '、'.join(LABELS[key] for key in components)
        elements.append(dict(element_id=element_id, source_fact_key='technology.transaction.' + (components[0] if len(components) == 1 else element_id),
            required_fact=label, proposition=label + ('已有直接约定。' if state == 'COVERED' else ''),
            status=state, supporting_evidence=sources, bound_evidence_ids=list(dict.fromkeys(s['clause_id'] for s in sources)),
            fact_ids=list(dict.fromkeys(fact_ids)), residual_gap='、'.join(missing), search_targets=missing,
            risk_relevant=True))
        if len(components) > 1:
            # Preserve the composite API, while production resolves its leaves
            # independently. A proved invoice cannot make the account PARTIAL.
            children = []
            for component in components:
                direct = [s for s in sources if s['component_key'] == component]
                children.append(dict(element_id=component, source_fact_key='technology.transaction.' + component,
                    required_fact=LABELS[component], proposition=LABELS[component],
                    status='COVERED' if direct else 'MISSING', supporting_evidence=direct,
                    bound_evidence_ids=list(dict.fromkeys(s['clause_id'] for s in direct)),
                    fact_ids=list(dict.fromkeys(s['fact_id'] for s in direct)),
                    residual_gap='' if direct else LABELS[component],
                    search_targets=[] if direct else [LABELS[component]], risk_relevant=True))
            elements[-1]['child_elements'] = children
    return elements


def extract_elements(family, clauses):
    from review_v2.contract_facts import ContractFactGraph
    graph = ContractFactGraph()
    register_facts(graph, clauses)
    return elements_from_graph(family, graph)
