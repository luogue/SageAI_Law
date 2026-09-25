"""Consulting candidates expressed in the existing atomic fact contract.

Retrieval hints are not semantic predicates. These predicates retain the
performance object and obligation, and publish their own parser source spans.
The independent source verifier re-executes them, as for other atomic families.
"""
import re
from review_v2.obligation_detail_elements import _segments
from review_v2.proposition_scope import arrangement_matches, listed_arrangement_matches
from review_v2.obligation_detail_elements import _DURATION

FAMILIES = {
    'consulting_payment': (
        ('consulting_fee_total', '咨询报酬总额', r'(?:咨询报酬|咨询费|服务费用|报酬总额|合同总价|合同价款).{0,20}(?:\d[\d,.]*|[一二三四五六七八九十百千万]+).{0,4}(?:元|美元|人民币|USD)'),
        ('payment_milestones', '咨询报酬支付节点和期限', r'(?:支付|付款).{0,20}(?:\d[\d,.]*%|\d[\d,.]*元)|(?:\d+(?:个)?工作日|验收后|提交报告后).{0,20}(?:支付|付款)|分[一二三四五六七八九十\d]+期支付[：:].{0,120}(?:工作日|日内|天内)'),
        ('itemized_prices', '咨询分项价格', r'分项.{0,8}合同价.{0,15}\d'),
        ('collection_account', '咨询报酬收款账户', r'(?:开户银行|银行账号|银行帐号|收款账户|收款银行)[：:][^。；]{2,}'),
        ('bank_expense_allocation', '咨询银行费用承担', r'(?:银行费用|汇款费用|手续费).{0,30}(?:承担|负担)|(?:承担|负担).{0,20}(?:银行费用|汇款费用|手续费)'),
        ('out_of_scope_repricing', '超范围咨询服务价格机制', r'(?:超范围|超出.{0,10}范围|额外服务).{0,50}(?:费用|价格|报价).{0,25}(?:协商|确认|调整)|(?:超范围|超出.{0,10}范围|额外服务).{0,40}另行报价'),
    ),
    'consulting_quality': (
        ('consulting_scope', '咨询事项和范围', r'(?:咨询(?:内容|范围|事项)[：:].+|(?:针对|对).{0,90}(?:分析|评估|论证))'),
        ('report_contents', '咨询报告内容', r'(?:报告|成果).{0,12}(?:应包括|须包括|包括|包含|完整覆盖).+'),
        ('delivery_form', '咨询成果交付形式', r'(?:提交|交付|提供).{0,25}(?:电子|纸质|书面).{0,25}(?:报告|成果)|(?:报告|成果).{0,25}(?:电子|纸质|书面)'),
        ('acceptance_standard', '咨询成果验收标准', r'(?:报告|成果).{0,15}(?:应|须).{0,15}(?:完整覆盖|符合|达到).+|验收(?:标准|依据)[：:].+'),
    ),
    'consulting_decision': (
        ('qualified_consulting_decision_risk', '合格咨询成果决策损失承担', r'(?:按照|根据).{0,45}(?:符合|达到).{0,25}(?:标准|方式).{0,30}咨询.{0,50}(?:损失|责任).{0,80}(?:承担|处理)'),
    ),
    'consulting_inputs': (
        ('technical_materials', '委托方提供咨询所需技术资料', r'(?:甲方|委托方|委托人).{0,20}(?:提供|提交).{0,80}(?:资料|图纸|架构图|文档|数据|信息)'),
        ('cooperation_conditions', '委托方提供咨询协作条件', r'(?:甲方|委托方|委托人).{0,20}(?:提供|安排|开放|协助).{0,70}(?:人员|访谈|环境|权限|现场|协助|协作条件)'),
        ('truthfulness_completeness', '委托资料真实完整责任', r'(?:甲方|委托方|委托人).{0,30}(?:保证|确保|负责).{0,30}(?:资料|数据|信息).{0,20}真实.{0,8}完整'),
        ('delivery_time_method', '咨询资料提交时间或方式', r'(?:甲方|委托方|委托人).{0,130}(?:通过|采用|以).{0,25}(?:交接|电子|书面|加密|邮件|方式).{0,30}(?:提交|提供)|(?:资料|数据|信息).{0,30}(?:提交|提供).{0,15}(?:时间|方式|日前|日内)'),
    ),
    'consulting_remedy': (
        ('defect_trigger', '咨询成果瑕疵触发条件', r'(?:咨询成果|咨询报告|报告|成果).{0,20}(?:不符合|未达到|不满意)|(?:对|认为).{0,25}(?:成果|报告).{0,15}不满意'),
        ('correction_period', '咨询成果补正期限', r'(?:合理期限|\d+(?:个)?(?:工作日|天|日)内).{0,20}(?:修改|改正|补正|弥补)|(?:改正|整改|补正|弥补)(?:期限)?[：:]?.{0,12}(?:\d+天|\d+日|合理期限)'),
        ('correction_remedy', '咨询成果补正义务', r'(?:乙方|受托方|咨询方).{0,90}(?:应|须|必须).{0,50}(?:修改|改正|补正|弥补|重新提交)'),
        ('termination_remedy', '瑕疵补正后的解除救济', r'(?:仍|整改|补正|最低验收标准).{0,60}(?:有权|可以).{0,10}解除'),
        ('refund_remedy', '咨询瑕疵解除后的返还', r'(?:退还|退回|返还).{0,12}(?:已付款|款项|价款|报酬)'),
    ),
}
OPTIONAL = {'termination_remedy', 'refund_remedy'}
PAYMENT_OPTIONAL = {'itemized_prices', 'collection_account', 'bank_expense_allocation', 'out_of_scope_repricing'}
FAMILIES['consulting_subject'] = (
    ('consulting_project', '咨询项目或事项', r'项目名称[：:].+|(?:咨询事项|咨询项目)[：:].+'),
    ('technical_question_or_object', '咨询分析对象和技术问题', FAMILIES['consulting_quality'][0][2]),
    FAMILIES['consulting_quality'][0],
    ('consulting_deliverable', '咨询成果', r'(?:提交|提供|出具|完成).{0,30}(?:技术咨询报告|咨询报告|分析评价报告|技术分析报告|可行性论证)'),
)

# Extend the existing semantic definitions, retaining their canonical keys.
# Normal commercial risk and an advisor's fault exception are distinct duties.
ALIASES = {
    'consulting_project': r'拟(?:建设|实施|开展)[^。；]{1,70}(?:系统|工程|项目)[^。；]{0,80}(?:咨询|论证)|就[^。；]{1,50}项目提供技术咨询',
    'consulting_scope': r'就[^。；]{1,70}(?:提供|开展)技术咨询|(?:分析|比较|评估|论证)[^。；]{1,70}(?:技术|方案|参数|风险)',
    'qualified_consulting_decision_risk': r'(?:根据|依据)[^。；]{0,40}咨询(?:意见|建议)[^。；]{0,60}(?:决策责任|决策风险|商业风险)[^。；]{0,20}(?:甲方|委托方|委托人)[^。；]{0,6}承担|(?:甲方|委托方|委托人)(?:应|须)?(?:自行)?承担正常商业决策风险',
    'defect_trigger': r'(?:认为|发现)[^。；]{0,20}(?:报告|成果)[^。；]{0,15}(?:遗漏|缺漏|缺陷|错误)',
    'correction_period': _DURATION + r'内[^。；]{0,20}(?:补充|补正|修正|改正|修改)',
    'correction_remedy': r'(?:乙方|咨询方|受托方)[^。；]{0,10}(?:应|须)[^。；]{0,45}(?:合理)?(?:补充|补正|修正)',
    'payment_milestones': r'(?:支付|付款)[^。；]{0,12}\d[\d,.]*万?元',
}
for family, definitions in list(FAMILIES.items()):
    FAMILIES[family] = tuple((key,label,pattern+'|'+ALIASES[key] if key in ALIASES else pattern)
                              for key,label,pattern in definitions)
FAMILIES['consulting_decision'] += (
    ('consultant_fault_exception', '咨询方故意或重大过错的责任例外',
     r'(?:乙方|咨询方|受托方)[^。；]{0,90}(?:故意|重大过失|重大过错)[^。；]{0,90}(?:承担|赔偿)|(?:乙方|咨询方|受托方)[^。；]{0,35}下列情形[^。；]{0,90}(?:承担|赔偿)'),)
FAMILIES['consulting_remedy'] += (
    ('reinspection_deadline', '补正完成后的再次验收期限',
     _DURATION+r'内[^。；]{0,20}(?:再次验收|重新验收|复验)'),)

FAMILIES['consulting_boundary'] = (
    ('excluded_construction_performance', '咨询与建设施工履行边界', r'(?:不(?:直接)?承包|不负责|不包括|不包含)[^。；]{0,20}(?:建设|施工|安装)'),
    ('excluded_goods_procurement', '咨询与设备采购履行边界', r'(?:不负责|不包括|不包含)[^。；]{0,12}设备采购'),
    ('excluded_software_implementation', '咨询与完整软件开发实施边界', r'不(?:直接)?开发[^。；]{0,20}(?:完整|软件)|(?:不负责|不包括|不包含)(?:(?!但|而是|负责|承担)[^。；，,]){0,40}(?:软件开发|系统实施)'),
)

# Each entry binds an operative list introduction to its own objects. Conditions,
# missing-list introductions and article boundaries retain their original scope.
LIST_PREDICATES = {
    'consulting_project': (r'(?:甲方|委托方|委托人)委托(?:乙方|咨询方|受托方)就[：:]$', r'提供[^。；]{0,10}技术咨询'),
    'report_contents': (r'(?:应|须)[^。；]{0,20}(?:交付|提交|提供)[：:]$', r'报告|方案|建议书|测算表|路线图'),
    'acceptance_standard': (r'(?:报告|成果)[^。；]{0,12}(?:应|须)[：:]$|验收(?:依据|标准)[：:]$', r'明确|说明|列明|质量标准|成果清单|咨询目标|咨询范围'),
    'consulting_scope': (r'咨询范围(?:包括|包含)?[：:]$|(?:分析|评估|论证)[：:]$', r'.+'),
    'consultant_fault_exception': (r'(?:如果|如|若)[^。；]{0,20}(?:乙方|咨询方|受托方)[^。；]{0,20}(?:存在|发生)[^。；]{0,10}(?:情况|情形)[：:]$', r'赔偿责任|承担责任'),
}


def list_sources(key, clauses):
    if key not in LIST_PREDICATES:
        return []
    intro, member = LIST_PREDICATES[key]
    rows = []
    for clause in clauses:
        context = clause.title + clause.text
        if not re.search(r'咨询|报告|成果|验收|方案|分析', context):
            continue
        for match in listed_arrangement_matches(member, clause.text, introduction_pattern=intro):
            # A fault list must state a professional error as well as its remedy.
            if key == 'consultant_fault_exception' and not re.search(r'伪造|重大|明知|故意|明显忽略', match['quote']):
                continue
            rows.append(dict(clause_id=clause.clause_id, quote=match['quote'], location=clause.location))
    return rows


def fault_list_sources(clauses):
    """Retain the error condition and consequent liability across a colon list."""
    rows = []
    for clause in clauses:
        pattern = (r'(?:如果|如|若)(?:乙方|咨询方|受托方)存在(?:以下|下列)(?:情况|情形)[：:]'
                   r'[^。]*?(?:乙方|咨询方|受托方)(?:应当|应|须)承担(?:赔偿)?责任[。]?')
        for match in re.finditer(pattern, clause.text):
            quote = match[0]
            if (re.search(r'伪造|重大|明知|故意|明显忽略', quote)
                    and not re.search(r'未约定|未明确|另行协商', quote)):
                rows.append(dict(clause_id=clause.clause_id, quote=quote, location=clause.location))
    return rows


def evaluation_dimensions(clauses):
    """An evaluation list's '是否' defines criteria, not an unanswered query."""
    rows = []
    for clause in clauses:
        start = None
        for m in re.finditer(r'[^\n。；;]+[。；;]?', clause.text):
            q = m[0].strip()
            if list(arrangement_matches(r'验收(?:主要)?(?:检查|评价|考察)[：:]$', q)):
                start = m.start()
            elif start is not None and re.match(r'是否(?:完成|提交|列明|说明|分析|对)', q):
                rows.append(dict(clause_id=clause.clause_id, quote=clause.text[start:m.end()].strip(),location=clause.location))
            else:
                start = None
    return rows


def _client_action(text, action):
    """Resolve the clause's acting party, excluding 向乙方 as a recipient.

    Long timing/method modifiers do not sever a party's obligation. An explicit
    later subject does: a consultant's warranty cannot prove a client's warranty.
    """
    parties = r'甲方|乙方|委托方|委托人|受托方|受托人|咨询方'
    for match in re.finditer(action, text):
        actors = [m[0] for m in re.finditer(parties, text[:match.start()])
                  if m.start() == 0 or text[m.start()-1] not in '向给对与由']
        if actors and actors[-1] in {'甲方', '委托方', '委托人'}:
            return True
    return False


def elements(family, clauses):
    # A reinspection deadline refines a stated reinspection topic. Do not
    # manufacture a sixth remedy component in contracts that never mention it.
    reinspection_addressed = any(re.search(r'再次验收|重新验收|复验', c.text) for c in clauses)
    definitions = tuple(row for row in FAMILIES[family]
                        if row[0] != 'reinspection_deadline' or reinspection_addressed)
    result = []
    for key, label, predicate in definitions:
        sources = []
        for clause, heading, quote in _segments(clauses):
            text = re.sub(r'\s+', '', quote)
            matched = bool(list(arrangement_matches(predicate, text)))
            if family == 'consulting_inputs':
                actions = {
                    'technical_materials': r'(?:提供|提交).{0,80}(?:资料|图纸|架构图|文档|数据|信息)',
                    'cooperation_conditions': r'(?:提供|安排|开放|协助).{0,70}(?:人员|访谈|环境|权限|现场|协作条件)',
                    'truthfulness_completeness': r'(?:保证|确保).{0,20}(?:资料|数据|信息).{0,20}真实.{0,8}完整',
                    'delivery_time_method': r'(?:通过|采用|以).{0,25}(?:电子|交接|书面|加密|方式).{0,30}(?:提供|提交)',
                }
                matched = _client_action(text, actions[key]) and bool(list(arrangement_matches(actions[key], text)))
            if getattr(clause, 'block_type', '') == 'HEADING' or not matched:
                continue
            # Scope/standards concern the consulting performance, not another
            # obligation sharing “report”, “data” or “correction”.
            context = text + str(getattr(clause, 'title', ''))
            if family in {'consulting_quality', 'consulting_remedy'} and not re.search(r'咨询|报告|成果|验收', context):
                continue
            if re.search(r'(?:无需|不必|不予|不承担).{0,10}(?:提供|提交|修改|补正)', text):
                continue
            sources.append({'clause_id': clause.clause_id, 'quote': quote,
                            'location': clause.location})
        if key == 'acceptance_standard':
            sources.extend(evaluation_dimensions(clauses))
        sources.extend(list_sources(key, clauses))
        if key == 'consultant_fault_exception':
            sources.extend(fault_list_sources(clauses))
        if key in {'consulting_project', 'consulting_fee_total'}:
            from review_v2.technology_service_elements import sources as find
            if key == 'consulting_project':
                sources.extend(find(clauses, r'(?:甲方|委托方|委托人)委托(?:乙方|咨询方|受托方)就[：:]?[^。；]{1,160}提供[^。；]{0,10}技术咨询'))
            else:
                sources.extend(find(clauses, r'(?:合同总价|咨询费|咨询报酬)[：:]?\s*(?:人民币)?\s*\d[\d,.]*\s*万?元', context=r'费用|报酬|价款'))
        if key == 'payment_milestones':
            from review_v2.technology_service_elements import sources as find
            sources.extend(find(clauses, r'(?:合同生效后|验收通过后|提交报告后)[^。；]{0,25}支付[^。；]{0,30}\d[\d,.]*元', context=r'咨询|费用|价款|报酬'))
        if family == 'consulting_payment':
            # A bare label such as “合同总价” gets its remuneration object from
            # its article. Keep that exact context in the published proposition,
            # not just in metadata hidden from downstream evidence consumers.
            by_id = {c.clause_id: c for c in clauses}
            bound = []
            for source in sources:
                c = by_id[source['clause_id']]
                if re.search(r'违约|赔偿|迟延', c.title) and key in {'consulting_fee_total', 'payment_milestones'}:
                    continue
                if re.search(r'咨询.*(?:费用|报酬)|(?:费用|报酬).*咨询', c.title):
                    end = c.text.find(source['quote'])
                    if end >= 0:
                        source = {**source, 'quote': c.text[:end + len(source['quote'])]}
                if source not in bound:
                    bound.append(source)
            sources = bound
        optional = key in OPTIONAL | PAYMENT_OPTIONAL
        # These refine an existing allocation/remedy, rather than creating
        # additional mandatory business requirements when never addressed.
        if key == 'consultant_fault_exception':
            optional = True
        if key == 'reinspection_deadline':
            optional = False
        if key in PAYMENT_OPTIONAL and not sources and not any(label[:4] in c.text for c in clauses):
            # Optional payment arrangements that are never addressed are outside
            # this contract's component set, not missing mandatory requirements.
            continue
        result.append(dict(element_id=key, source_fact_key=family + '.' + key,
                           status='COVERED' if sources else 'MISSING',
                           required_fact=label, proposition=label,
                           search_targets=[label], supporting_evidence=sources,
                           risk_relevant=not optional,
                           residual_gap='' if sources else label))
    if family == 'consulting_subject':
        scope = next(e for e in result if e['element_id'] == 'consulting_scope')
        question = next(e for e in result if e['element_id'] == 'technical_question_or_object')
        if scope['supporting_evidence'] and not question['supporting_evidence']:
            question.update(status='COVERED', supporting_evidence=scope['supporting_evidence'], residual_gap='')
    return result
