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
        ('consulting_fee_total', '咨询报酬总额', r'(?:(?:全部)?(?:技术咨询|咨询|顾问)(?:服务)?(?:的)?(?:费|费用|报酬)(?:总额|合计)|(?:技术咨询费|咨询费|咨询报酬).{0,6}(?:为|是|等于|[：:])|服务费用总额|报酬总额|合同总价|合同价款).{0,45}(?:[￥¥]\s*\d[\d,.]*|\d[\d,.]*|[零〇一二两三四五六七八九十百千万壹贰叁肆伍陆柒捌玖拾佰仟萬亿億元整]+).{0,6}(?:元|美元|人民币|USD)'),
        ('payment_milestones', '咨询报酬支付节点和期限', r'(?:支付|付款).{0,20}(?:\d[\d,.]*%|\d[\d,.]*元)|(?:\d+(?:个)?工作日|验收后|提交报告后).{0,20}(?:支付|付款)|分[一二三四五六七八九十\d]+期支付[：:].{0,120}(?:工作日|日内|天内)'),
        ('itemized_prices', '咨询分项价格', r'分项.{0,8}合同价.{0,15}\d'),
        ('collection_account', '咨询报酬收款账户', r'(?:开户银行|银行账号|银行帐号|收款账户|收款银行)[：:][^。；]{2,}'),
        ('bank_expense_allocation', '咨询银行费用承担', r'(?:银行费用|汇款费用|手续费).{0,30}(?:承担|负担)|(?:承担|负担).{0,20}(?:银行费用|汇款费用|手续费)'),
        ('out_of_scope_repricing', '超范围咨询服务价格机制', r'(?:超范围|超出.{0,10}范围|额外服务).{0,50}(?:费用|价格|报价).{0,25}(?:协商|确认|调整)|(?:超范围|超出.{0,10}范围|额外服务).{0,40}另行报价'),
    ),
    'consulting_quality': (
        ('consulting_scope', '咨询事项和范围', r'(?:咨询(?:内容|范围|事项)[：:].+|(?:针对|对).{0,90}(?:分析|评估|论证))'),
        ('report_contents', '咨询报告内容', r'(?:报告|成果).{0,12}(?:应包括|须包括|包括|包含|完整覆盖).+'),
        ('delivery_form', '咨询成果交付形式', r'(?:提交|交付|提供).{0,25}(?:电子|纸质|书面).{0,25}(?:报告|成果)|(?:报告|成果).{0,25}(?:电子|纸质|书面)|(?:报告|文件|成果)[^。；]{0,30}(?:以|按|采用)[^。；]{0,25}(?:CIF|FOB|C&F|CFR|FCA|航空邮寄|挂号邮寄|快递)[^。；]{0,30}(?:交付|提交)'),
        ('acceptance_standard', '咨询成果验收标准', r'(?:报告|成果).{0,20}(?:应|须).{0,30}(?:完整覆盖|符合|达到|具有对应关系|能够说明|作出分析回应).+|验收(?:标准|依据)[：:].+|验收.{0,20}(?:判断|检查|评价|考察).{0,30}(?:报告|成果).{0,20}(?:覆盖|符合|达到|完成|提交|列明|说明)'),
    ),
    'consulting_decision': (
        ('qualified_consulting_decision_risk', '合格咨询成果决策损失承担', r'(?:按照|根据).{0,45}(?:符合|达到).{0,25}(?:标准|方式).{0,30}咨询.{0,50}(?:损失|责任).{0,80}(?:承担|处理)|(?:甲方|委托方|委托人).{0,35}(?:是否采用|如何实施).{0,35}(?:决定|承担)|因(?:甲方|委托方|委托人).{0,80}(?:造成|产生)的后果.{0,15}(?:自行承担|由甲方承担)'),
    ),
    'consulting_inputs': (
        ('technical_materials', '委托方提供咨询所需技术资料', r'(?:甲方|委托方|委托人).{0,20}(?:提供|提交).{0,80}(?:资料|图纸|架构图|文档|数据|信息)'),
        ('cooperation_conditions', '委托方提供咨询协作条件', r'(?:甲方|委托方|委托人).{0,35}(?:提供|安排|开放|协助|指定).{0,70}(?:人员|负责人|访谈|环境|权限|现场|部门|协助|协作条件)'),
        ('truthfulness_completeness', '委托资料真实完整责任', r'(?:甲方|委托方|委托人).{0,30}(?:保证|确保|负责).{0,30}(?:资料|数据|信息).{0,20}真实.{0,8}完整'),
        ('delivery_time_method', '咨询资料提交时间或方式', r'(?:甲方|委托方|委托人).{0,130}(?:通过|采用|以).{0,25}(?:交接|电子|书面|加密|邮件|方式).{0,30}(?:提交|提供)|(?:资料|数据|信息).{0,30}(?:提交|提供).{0,15}(?:时间|方式|日前|日内)'),
    ),
    'consulting_remedy': (
        ('defect_trigger', '咨询成果瑕疵触发条件', r'(?:咨询成果|咨询报告|报告|成果|服务).{0,25}(?:不符合|未达到|不满意|不能令[^。；]{0,8}满意|存在.{0,15}(?:遗漏|缺漏|缺陷|明显错误|与.{0,12}(?:范围|要求).{0,8}不符))|(?:对|认为).{0,25}(?:成果|报告|服务).{0,15}不满意|(?:甲方|委托方).{0,20}(?:提出|发现).{0,30}(?:问题|缺陷|错误|遗漏).{0,25}(?:咨询范围|合理依据)'),
        ('correction_period', '咨询成果补正期限', r'(?:合理期限|\d+(?:个)?(?:工作日|天|日)内).{0,20}(?:修改|改正|补正|弥补)|(?:改正|整改|补正|弥补)(?:期限)?[：:]?.{0,12}(?:\d+天|\d+日|合理期限)'),
        ('correction_remedy', '咨询成果补正义务', r'(?:乙方|受托方|咨询方).{0,90}(?:应|须|必须).{0,50}(?:修改|改正|补正|弥补|重新提交)'),
        ('termination_remedy', '瑕疵补正后的解除救济', r'(?:仍|整改|补正|最低验收标准).{0,60}(?:有权|可以).{0,10}解除'),
        ('refund_remedy', '咨询瑕疵解除后的返还', r'(?:退还|退回|返还).{0,12}(?:已付款|款项|价款|报酬)'),
    ),
}
OPTIONAL = {'termination_remedy', 'refund_remedy'}
PAYMENT_OPTIONAL = {'itemized_prices', 'collection_account', 'bank_expense_allocation', 'out_of_scope_repricing'}
FAMILIES['consulting_subject'] = (
    ('consulting_project', '咨询项目或事项', r'(?:本)?项目名称(?:为|是|[：:]).+|(?:咨询事项|咨询项目)[：:].+|(?:甲方|委托方|委托人)委托(?:乙方|咨询方|受托方)(?:对|就)[^。；]{1,160}(?:提供|开展)[^。；]{0,10}技术咨询'),
    ('technical_question_or_object', '咨询分析对象和技术问题', FAMILIES['consulting_quality'][0][2]),
    FAMILIES['consulting_quality'][0],
    ('consulting_deliverable', '咨询成果', r'(?:提交|提供|出具|完成|形成).{0,45}(?:技术咨询报告|咨询报告|分析评价报告|技术分析报告|可行性论证|成果|诊断|方案|建议|路线图|风险分析)'),
)

# Extend the existing semantic definitions, retaining their canonical keys.
# Normal commercial risk and an advisor's fault exception are distinct duties.
ALIASES = {
    'consulting_project': r'拟(?:建设|实施|开展)[^。；]{1,70}(?:系统|工程|项目)[^。；]{0,80}(?:咨询|论证)|就[^。；]{1,50}项目提供技术咨询|(?:甲方|委托方|委托人)委托(?:乙方|咨询方|受托方)(?:对|就)[^。；]{1,160}(?:诊断|分析|评估|论证|提出建议)|(?:项目|专项工作)(?:的)?(?:名称|主题)(?:为|是|[：:])',
    'consulting_scope': r'就[^。；]{1,70}(?:提供|开展)技术咨询|(?:调查|诊断|分析|比较|评估|评价|论证)[^。；]{1,90}(?:技术|方案|参数|流程|系统|数据|风险|建议)',
    'qualified_consulting_decision_risk': r'(?:根据|依据)[^。；]{0,40}(?:咨询)?(?:意见|建议)[^。；]{0,180}(?:决策责任|决策风险|商业风险)[^。；]{0,35}(?:甲方|委托方|委托人)[^。；]{0,8}(?:自行)?承担|(?:甲方|委托方|委托人)(?:应|须)?(?:自行)?承担(?:正常|通常|一般)?商业决策风险|(?:甲方|委托方|委托人)[^。；]{0,20}(?:是否采用|如何实施)[^。；]{0,20}(?:自行决定|由其决定)|因[^。；]{0,80}(?:市场变化|经营决策|第三方实施)[^。；]{0,60}(?:咨询方|乙方)[^。；]{0,12}不承担责任|(?:一般|正常|通常)商业风险[^。；]{0,16}由(?:甲方|委托方|委托人)(?:自行)?承担|(?:仅供|仅作为|仅系)[^。；]{0,40}(?:决策|经营|投资|技术)[^。；]{0,12}参考|(?:甲方|委托方|委托人)[^。；]{0,30}(?:自行)?决定[^。；]{0,15}(?:是否|如何)[^。；]{0,25}(?:采用|实施|使用)',
    'truthfulness_completeness': r'(?:甲方|委托方|委托人)[^。；]{0,40}(?:保证|确保|负责)[^。；]{0,40}(?:资料|数据|信息)[^。；]{0,25}(?:真实|完整|准确)|(?:甲方|委托方|委托人)[^。；]{0,55}(?:资料|数据|信息)[^。；]{0,30}(?:应当|应|须)(?:当)?[^。；]{0,8}(?:真实|完整|准确)|(?:甲方|委托方|委托人)[^。；]{0,40}(?:资料|数据|信息)[^。；]{0,25}(?:真实性|完整性|准确性)[^。；]{0,15}(?:负责|承担)',
    'defect_trigger': r'(?:认为|发现)[^。；]{0,20}(?:报告|成果)[^。；]{0,15}(?:遗漏|缺漏|缺陷|错误)',
    'correction_period': _DURATION + r'(?:内|的期限|期限)[^。；]{0,20}(?:补充|补正|修正|修订|改正|修改|弥补)',
    'correction_remedy': r'(?:乙方|咨询方|受托方)[^。；]{0,10}(?:应|须)[^。；]{0,45}(?:合理)?(?:补充|补正|修正|修订)',
    'payment_milestones': r'(?:支付|付款)[^。；]{0,12}\d[\d,.]*万?元',
}
for family, definitions in list(FAMILIES.items()):
    FAMILIES[family] = tuple((key,label,pattern+'|'+ALIASES[key] if key in ALIASES else pattern)
                              for key,label,pattern in definitions)
FAMILIES['consulting_decision'] += (
    ('consultant_fault_exception', '咨询方故意或重大过错的责任例外',
     r'(?:乙方|咨询方|受托方)[^。；]{0,90}(?:故意|重大过失|重大过错)[^。；]{0,90}(?:承担|赔偿)|(?:乙方|咨询方|受托方)[^。；]{0,35}下列情形[^。；]{0,90}(?:承担|赔偿)'
     # A consultant's own professional error (material computation/data error,
     # departure from accepted standards) is the same fault-based exception.
     r'|(?:因|对因)[^。；]{0,60}(?:重大(?:计算|数据|处理)?错误|数据处理错误|违反[^。；]{0,25}技术标准|虚假数据|伪造)[^。；]{0,60}(?:造成|导致)[^。；]{0,40}(?:承担|赔偿)'),)
FAMILIES['consulting_remedy'] += (
    ('reinspection_deadline', '补正完成后的再次验收期限',
     _DURATION+r'内[^。；]{0,20}(?:再次验收|重新验收|复验)'),)

FAMILIES['consulting_boundary'] = (
    ('excluded_construction_performance', '咨询与建设施工履行边界', r'(?:不承担|不负责|不包括|不包含|不涉及)(?:(?!但|然而)[^。；]){0,45}(?:建设|施工|安装)|(?:建设|施工|安装)(?:(?!但|然而)[^。；]){0,18}(?:不承担|不负责|不包括|不包含|不涉及)'),
    ('excluded_goods_procurement', '咨询与设备采购履行边界', r'(?:不承担|不负责|不包括|不包含|不涉及)(?:(?!但|然而)[^。；]){0,35}(?:设备|硬件|材料)(?:(?!但|然而)[^。；]){0,8}(?:采购|供应)|(?:设备|硬件|材料)采购(?:(?!但|然而)[^。；]){0,18}(?:不承担|不负责|不包括|不包含|不涉及)'),
    ('excluded_software_implementation', '咨询与完整软件开发实施边界', r'(?:不承担|不负责|不包括|不包含|不涉及)(?:(?!但|然而)[^。；]){0,45}(?:软件|系统)(?:(?!但|然而)[^。；]){0,12}(?:编码|开发|实施|运维)|不(?:直接)?开发(?:(?!但|然而)[^。；]){0,20}(?:完整|软件)'),
)

# Each entry binds an operative list introduction to its own objects. Conditions,
# missing-list introductions and article boundaries retain their original scope.
LIST_PREDICATES = {
    'consulting_project': (r'(?:甲方|委托方|委托人)委托(?:乙方|咨询方|受托方)就[：:]$', r'提供[^。；]{0,10}技术咨询'),
    'report_contents': (r'(?:应|须)[^。；]{0,35}(?:交付|提交|提供)[：:]$|(?:最终|咨询)?成果(?:至少)?(?:应)?(?:包括|包含|体现|列明)[：:]$', r'报告|方案|建议书|测算表|路线图|演示文件|分析|依据|前提|优先|风险|依赖'),
    'consulting_deliverable': (r'(?:应|须)[^。；]{0,45}(?:提交(?:以下)?成果|形成)[：:]$', r'《[^》]+(?:报告|方案|建议书)》|诊断|分析|建议|方案|架构|测算|路线图'),
    'delivery_form': (r'(?:全部|上述)?(?:文件|报告|成果)[^。；]{0,15}(?:提交|交付|提供)[：:]$', r'PDF|电子版|电子文档|纸质版|纸质文件|可编辑'),
    'acceptance_standard': (r'(?:报告|成果)[^。；]{0,12}(?:应|须)[：:]$|验收(?:依据|标准)[：:]$', r'明确|说明|列明|质量标准|成果清单|咨询目标|咨询范围'),
    'consulting_scope': (r'咨询范围(?:包括|包含)?[：:]$|(?:分析|评估|论证)[：:]$', r'.+'),
    'cooperation_conditions': (r'(?:甲方|委托方|委托人)(?:(?:应|须)[：:]$|负责[^。；]{0,25}(?:提供|配合)[^。；]{0,20}(?:条件)?(?:包括)?[：:]$)', r'(?:指定|安排|协调|组织|开放|协助)[^。；]{0,70}(?:负责人|人员|部门|访谈|专题会议|办公区域|确认需求|权限|现场|调研)'),
    'truthfulness_completeness': (r'(?:甲方|委托方|委托人)(?:应|须)[：:]$', r'(?:保证|确保)[^。；]{0,70}(?:资料|数据|信息|文件)[^。；]{0,35}(?:真实|完整|准确)'),
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
        for match in re.finditer(
                r'[^。；]*(?:验收|审核)[^。；]{0,20}(?:判断|检查|评价|考察)[^。；]{0,35}'
                r'是否[^。；]{0,12}(?:覆盖|符合|达到|完成|提交|列明|说明)[^。；]*[。；]?',
                clause.text):
            quote = match[0].strip()
            if quote and not re.search(r'未约定|未明确|如何判断|如何验收', quote):
                rows.append(dict(clause_id=clause.clause_id, quote=quote, location=clause.location))
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


def consulting_fee_total_sources(clauses):
    """One semantic definition for consultation remuneration totals.

    A total may use fee, remuneration, lump-sum price or service-total wording,
    and the numeric amount may follow a colon on the next line.  Payment-node
    amounts are excluded because the definition must express totality.
    """
    amount = r'(?:人民币\s*)?(?:[零〇一二两三四五六七八九十百千万壹贰叁肆伍陆柒捌玖拾佰仟萬亿億元整]+|[￥¥]?\s*\d[\d,，.]*)\s*(?:万|亿)?元(?:整)?(?:\s*[（(][￥¥]?\s*\d[\d,，.]*\s*元?[）)])?'
    concept = (
        r'(?:本合同项下|本项目|本合同)?(?:全部)?[^。；\n]{0,20}'
        r'(?:(?:技术咨询|咨询|顾问)(?:服务)?(?:的)?(?:费|费用|报酬)|包干(?:价|费用|报酬)|咨询服务总价)'
        r'(?:总额|合计|总价|包干)?'
    )
    pattern = (concept + r'\s*'
               r'(?:(?:合计|总计)\s*(?:(?:为|是|等于)\s*[：:]?|[：:])?|'
               r'(?:(?:为|是|等于)\s*[：:]?|[：:]))\s*(?:\n\s*)?' + amount)
    rows = []
    for clause in clauses:
        if not re.search(r'咨询|顾问', clause.title + clause.text):
            continue
        original = getattr(clause, 'raw_text', '') or clause.text
        for match in re.finditer(pattern, original):
            quote = match[0].strip()
            row = dict(clause_id=clause.clause_id, quote=quote, location=clause.location)
            if row not in rows:
                rows.append(row)
    return rows


def defect_criterion_sources(clauses):
    """Acceptance questions state operative defect criteria, not uncertainty."""
    rows = []
    for clause in clauses:
        for match in re.finditer(
                r'[^。；]*(?:成果|报告)是否存在[^。；]{0,60}'
                r'(?:遗漏|缺漏|明显错误|数据引用错误|重大矛盾|不符合)[^。；]*[。；]?', clause.text):
            quote = match[0].strip()
            if quote and not re.search(r'未约定|未明确', quote):
                rows.append(dict(clause_id=clause.clause_id, quote=quote, location=clause.location))
    return rows


def referred_defect_trigger_sources(clauses):
    """Resolve a defect trigger that points to an explicit prior criterion.

    The source remains the contiguous acceptance passage, so ``前述问题`` is
    independently verifiable rather than treated as a free-standing keyword.
    """
    rows = []
    for clause in clauses:
        original = getattr(clause, 'raw_text', '') or clause.text
        criterion = re.search(
            r'(?:不存在|不应存在)[^。；]{0,80}'
            r'(?:遗漏|错误|矛盾|缺陷|不符)[^。；]*[。；]?', original)
        trigger = re.search(
            r'(?:甲方|委托方)[^。；]{0,20}认为(?:报告|成果)[^。；]{0,25}'
            r'(?:前述|上述|该)[^。；]{0,15}(?:问题|情形|标准|条件)[^。；]{0,60}(?:应|须)[^。；]{0,25}(?:书面|提出|说明)', original)
        if criterion and trigger and criterion.start() < trigger.end():
            rows.append(dict(clause_id=clause.clause_id,
                             quote=original[criterion.start():trigger.end()].strip(),
                             location=clause.location))
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
                    'cooperation_conditions': r'(?:提供|安排|开放|协助|指定).{0,70}(?:人员|负责人|访谈|环境|权限|现场|部门|协作条件)',
                    'truthfulness_completeness': r'(?:保证|确保|负责)[^。；]{0,35}(?:资料|数据|信息)[^。；]{0,25}(?:真实|完整|准确)|(?:资料|数据|信息)[^。；]{0,45}(?:应当|应|须)(?:当)?[^。；]{0,25}(?:保证|确保)?[^。；]{0,12}(?:真实|完整|准确)|(?:资料|数据|信息)[^。；]{0,25}(?:真实性|完整性|准确性)[^。；]{0,15}(?:负责|承担)',
                    'delivery_time_method': r'(?:通过|采用|以).{0,25}(?:电子|交接|书面|加密|方式).{0,30}(?:提供|提交)',
                }
                matched = _client_action(text, actions[key]) and bool(list(arrangement_matches(actions[key], text)))
            if getattr(clause, 'block_type', '') == 'HEADING' or not matched:
                continue
            # Scope/standards concern the consulting performance, not another
            # obligation sharing “report”, “data” or “correction”.
            context = text + str(getattr(clause, 'title', ''))
            if family in {'consulting_quality', 'consulting_remedy'} and not re.search(r'咨询|报告|成果|验收', context):
                if not (key == 'correction_period' and re.search(
                        r'(?:甲方|委托方).{0,20}(?:意见|异议).{0,25}(?:乙方|咨询方|受托方).{0,20}'
                        + _DURATION + r'内.{0,12}(?:完成)?(?:修改|修订|补充|补正|修正|改正)', text)):
                    continue
            if re.search(r'(?:无需|不必|不予|不承担).{0,10}(?:提供|提交|修改|补正)', text):
                continue
            sources.append({'clause_id': clause.clause_id, 'quote': quote,
                            'location': clause.location})
        if key == 'acceptance_standard':
            sources.extend(evaluation_dimensions(clauses))
            from review_v2.technology_service_elements import sources as find
            sources.extend(find(clauses,
                r'(?:报告|成果)[^。；]{0,15}(?:应|须)[^。；]{0,15}(?:说明|列明|包含|包括)[^。；]{2,120}',
                context=r'咨询|报告|成果'))
            # A written-objection list enumerating objective defects is an
            # acceptance standard even when the article does not use that label.
            groups = {}
            for clause in clauses:
                root = (getattr(clause, 'heading_path', None) or [clause.title])[0]
                groups.setdefault(root, []).append(clause)
            for group in groups.values():
                intro = next((c for c in group if re.search(
                    r'(?:报告|成果)[^。；]{0,20}(?:下列|以下)情形[^。；]{0,15}(?:修改|异议|意见)|'
                    r'(?:可|可以|有权)[^。；]{0,20}(?:下列|以下)情形[^。；]{0,15}(?:修改|异议|意见)', c.text)), None)
                criteria = [c for c in group if re.search(r'遗漏|不一致|逻辑矛盾|重大错误|实质影响|无法正常使用', c.text)]
                if intro and criteria:
                    for criterion in criteria:
                        sources.append(dict(clause_id=criterion.clause_id, quote=criterion.text,
                                            location=criterion.location,
                                            domain_context_evidence=[dict(clause_id=intro.clause_id,
                                                                          quote=intro.text,
                                                                          location=intro.location)]))
        sources.extend(list_sources(key, clauses))
        if key == 'report_contents' and not sources:
            # A results article's enumerated named reports is the report-content
            # specification consumed by both the subject and quality rules.
            from review_v2.technology_service_elements import sources as find
            sources.extend(find(clauses,
                r'《[^》]+(?:报告|方案|建议书)》|(?:项目)?汇报演示文件',
                context=r'咨询成果|报告', inherit_lists=True))
        if key == 'report_contents':
            from review_v2.technology_service_elements import sources as find
            sources.extend(find(
                clauses,
                r'(?:上述|前述|全部)?(?:文件|报告|成果)[^。；]{0,12}(?:应|须)[^。；]{0,12}'
                r'(?:至少)?(?:包含|包括|列明|说明)[^。；]{2,120}',
                context=r'成果|报告|文件',
            ))
        if key == 'consultant_fault_exception':
            sources.extend(fault_list_sources(clauses))
        if key == 'defect_trigger':
            sources.extend(defect_criterion_sources(clauses))
            sources.extend(referred_defect_trigger_sources(clauses))
            # Reuse the verified acceptance-standard defect list and require a
            # later operative reference to that list before publishing trigger.
            standard_rows = elements('consulting_quality', clauses)
            standards = next(e for e in standard_rows if e['element_id'] == 'acceptance_standard')['supporting_evidence']
            referred = [c for c in clauses if re.search(r'(?:如|若|发现|出现)[^。；]{0,18}(?:前述|上述|该)[^。；]{0,15}(?:问题|情形)[^。；]{0,35}(?:补正|修改|修订|重新提交)', c.text)]
            if standards and referred:
                for clause in referred:
                    sources.append(dict(clause_id=clause.clause_id, quote=clause.text,
                                        location=clause.location,
                                        domain_context_evidence=standards))
        if key == 'consultant_fault_exception':
            from review_v2.technology_service_elements import sources as find
            sources.extend(find(
                clauses,
                r'(?:因|但)(?:乙方|咨询方|受托方)[^。；]{0,80}'
                r'(?:故意|重大过失|重大过错)[^。；]{0,45}(?:损失|责任)[^。；]{0,12}(?:除外|承担|赔偿)',
                context=r'咨询|决策|专业',
            ))
        if key == 'qualified_consulting_decision_risk':
            from review_v2.technology_service_elements import sources as find
            sources.extend(find(
                clauses,
                r'(?:甲方|委托方|委托人)[^。；]{0,30}(?:根据|依据)[^。；]{0,30}'
                r'(?:咨询)?(?:意见|建议)[^。；]{0,100}(?:投资|采购|生产|经营|系统|技术改造|决策)'
                r'[^。；]{0,100}(?:一般|正常|通常)商业风险[^。；]{0,25}由(?:甲方|委托方|委托人)(?:自行)?承担',
                context=r'咨询|决策|商业风险',
            ))
            from review_v2.proposition_scope import scoped_propositions
            for clause in clauses:
                for scoped in scoped_propositions(clause.text):
                    quote = scoped['quote']
                    if (scoped['polarity'] == 'CONDITIONAL'
                            and re.search(r'(?:已|按照|按约)[^。；]{0,35}(?:履行|完成|成果)', scoped.get('condition', ''))
                            and re.search(r'(?:甲方|委托方|委托人)[^。；]{0,50}(?:咨询)?(?:意见|建议)[^。；]{0,100}决策', quote)
                            and re.search(r'(?:一般|正常|通常)商业风险[^。；]{0,25}由(?:甲方|委托方|委托人)(?:自行)?承担', quote)):
                        sources.append(dict(clause_id=clause.clause_id, quote=quote,
                                            location=clause.location,
                                            condition=scoped['condition']))
        if key == 'cooperation_conditions':
            from review_v2.technology_service_elements import sources as find
            sources.extend(find(
                clauses,
                r'(?:甲方|委托方|委托人)负责[^。；]{0,30}'
                r'(?:条件|配合)[^。；]{0,15}(?:包括)?[：:][^。]{0,480}'
                r'(?:安排|协调|组织)[^。；]{0,60}(?:人员|访谈|会议|现场|区域|调研)',
                context=r'咨询|配合|协作',
                inherit_lists=True,
            ))
            for clause in clauses:
                original = getattr(clause, 'raw_text', '') or clause.text
                intro = re.search(
                    r'(?:甲方|委托方|委托人)负责[^。；\n]{0,35}'
                    r'(?:条件|配合)[^。；\n]{0,20}(?:包括)?[：:]', original)
                if not intro:
                    continue
                member = re.search(
                    r'(?:安排|协调|组织|开放|协助)[^。；\n]{0,80}'
                    r'(?:人员|访谈|专题会议|现场|办公区域|调研)', original[intro.end():])
                if member:
                    end = intro.end() + member.end()
                    sources.append(dict(clause_id=clause.clause_id,
                                        quote=original[intro.start():end].strip(),
                                        location=clause.location))
            roots = {}
            for clause in clauses:
                original = getattr(clause, 'raw_text', '') or clause.text
                if re.search(r'(?:甲方|委托方|委托人)负责[^。；\n]{0,35}'
                             r'(?:条件|配合)[^。；\n]{0,20}(?:包括)?[：:]', original):
                    root = (getattr(clause, 'heading_path', None) or [clause.title])[0]
                    roots[root] = dict(clause_id=clause.clause_id, quote=original,
                                       location=clause.location,
                                       evidence_role='OBLIGATED_PARTY_CONTEXT')
            for clause in clauses:
                root = (getattr(clause, 'heading_path', None) or [clause.title])[0]
                if root not in roots:
                    continue
                original = getattr(clause, 'raw_text', '') or clause.text
                if re.search(r'(?:安排|协调|组织|开放|协助)[^。；\n]{0,80}'
                             r'(?:人员|访谈|专题会议|现场|办公区域|调研)', original):
                    sources.append(dict(clause_id=clause.clause_id, quote=original.strip(),
                                        location=clause.location,
                                        actor_source_evidence=[roots[root]]))
        if key in {'consulting_project', 'consulting_fee_total'}:
            from review_v2.technology_service_elements import sources as find
            if key == 'consulting_project':
                sources.extend(find(clauses, r'(?:甲方|委托方|委托人)委托(?:乙方|咨询方|受托方)就[：:]?[^。；]{1,160}提供[^。；]{0,10}技术咨询'))
                # A named project/work topic is a field whose value can be on
                # the following line. Keep the field and value in one source.
                sources.extend(find(
                    clauses,
                    r'(?:项目|专项工作)(?:的)?(?:名称|主题)(?:为|是|[：:])\s*\n?[^\n。；]{2,100}',
                    context=r'咨询|专项|项目',
                ))
            else:
                sources.extend(consulting_fee_total_sources(clauses))
        if key == 'delivery_form':
            from review_v2.technology_service_elements import sources as find
            sources.extend(find(
                clauses,
                r'(?:报告|文件|成果)[^。；]{0,35}(?:通过|采用|以)[^。；]{0,25}(?:电子邮箱|电子邮件|项目协作平台|在线平台)[^。；]{0,20}(?:提交|交付)|'
                r'(?:通过|采用|以)[^。；]{0,25}(?:电子邮箱|电子邮件|项目协作平台|在线平台)[^。；]{0,25}(?:提交|交付)[^。；]{0,20}(?:报告|文件|成果)',
                context=r'成果|报告|文件',
            ))
            # A delivery form is not only electronic/paper: an Incoterm or a
            # stated mailing/courier channel is an equally explicit form.
            sources = [source for source in sources if re.search(
                r'电子(?:文档|文件|邮箱|邮件)|项目协作平台|在线平台|电子版|PDF|纸质(?:文件|文本|版|[^。；]{0,8}报告)|书面报告'
                r'|CIF|FOB|C&F|CFR|FCA|航空邮寄|挂号邮寄|快递', source['quote'], re.I,
            ) and not re.search(r'书面反馈|书面意见|书面提出', source['quote'])]
        if key == 'consulting_scope':
            from review_v2.technology_service_elements import sources as find
            # The consulting article supplies the legal relation; an operative
            # investigation/analysis/evaluation/advice cluster defines scope.
            sources.extend(find(
                clauses,
                r'(?:乙方|咨询方|受托方)(?:应|须)[^。；]{0,100}'
                r'(?:调查|诊断|分析|评估|评价|论证)[^。；]{0,30}'
                r'(?:建议|方案|结论|路径)',
                context=r'咨询|专项工作',
                inherit_lists=True,
            ))
        if key == 'payment_milestones':
            from review_v2.technology_service_elements import sources as find
            sources.extend(find(clauses, r'(?:合同生效后|验收通过后|提交报告后)[^。；]{0,25}支付[^。；]{0,30}\d[\d,.]*元', context=r'咨询|费用|价款|报酬'))
        if key == 'correction_period':
            from review_v2.technology_service_elements import sources as find
            sources.extend(find(
                clauses,
                r'(?:补正|修改|修订|整改)[^。；]{0,45}' + _DURATION +
                r'内[^。；]{0,18}(?:重新提交|完成|改正)|' + _DURATION +
                r'内[^。；]{0,45}(?:重新提交|补正|修改|修订|整改)',
                context=r'成果|报告|修改|补正',
            ))
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
                # The heading is useful to disambiguate a bare total amount,
                # but it must not turn each payment node into a cumulative
                # article prefix.  Milestone evidence owns its exact operative
                # sentence (trigger + deadline + amount).
                if re.search(r'咨询.*(?:费用|报酬)|(?:费用|报酬).*咨询', c.title):
                    if key == 'consulting_fee_total':
                        end = c.text.find(source['quote'])
                        if end >= 0:
                            source = {**source, 'quote': c.text[:end + len(source['quote'])]}
                    elif key == 'payment_milestones' and re.search(r'合同总价', c.text) and not re.search(
                            r'(?:技术咨询|咨询|顾问)(?:服务)?(?:费|费用|报酬)', c.text.split('\n', 1)[-1]):
                        # A bare “合同总价” needs its consulting article scope.
                        # Contracts that state the consulting/advisory fee object
                        # expressly keep each operative node as its exact span.
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
        if key == 'truthfulness_completeness' and sources:
            joined = ''.join(source['quote'] for source in sources)
            truth = bool(re.search(r'真实|准确', joined))
            complete = bool(re.search(r'完整', joined))
            row = result[-1]
            row['component_coverage'] = [
                dict(element_id='material_truthfulness', status='COVERED' if truth else 'MISSING', required_fact='委托资料真实性责任', supporting_evidence=sources if truth else []),
                dict(element_id='material_completeness', status='COVERED' if complete else 'MISSING', required_fact='委托资料完整性责任', supporting_evidence=sources if complete else []),
            ]
            if not (truth and complete):
                row['status'] = 'PARTIALLY_COVERED'
                gaps = [c['required_fact'] for c in row['component_coverage'] if c['status'] == 'MISSING']
                row['residual_gap'] = '、'.join(gaps)
                row['search_targets'] = gaps
    if family == 'consulting_subject':
        scope = next(e for e in result if e['element_id'] == 'consulting_scope')
        question = next(e for e in result if e['element_id'] == 'technical_question_or_object')
        if scope['supporting_evidence'] and not question['supporting_evidence']:
            question.update(status='COVERED', supporting_evidence=scope['supporting_evidence'], residual_gap='')
        project = next(e for e in result if e['element_id'] == 'consulting_project')
        if not project['supporting_evidence'] and scope['supporting_evidence']:
            # These public elements intentionally share one canonical concept:
            # an explicit consulting objective/scope is the consulting matter.
            project.update(status='COVERED', supporting_evidence=scope['supporting_evidence'],
                           residual_gap='', search_targets=[])
        # Preserve each public atom's stable registry key while declaring the
        # shared consulting fact it consumes. Validators can still reproduce
        # the exact element predicate without treating the alias as a new fact.
        canonical_aliases = {
            'consulting_project': 'consulting_quality.consulting_scope',
            'consulting_scope': 'consulting_quality.consulting_scope',
            'technical_question_or_object': 'consulting_quality.consulting_scope',
            'consulting_deliverable': 'consulting_quality.report_contents',
        }
        for row in result:
            row['canonical_alias_of'] = canonical_aliases.get(row['element_id'])
    return result
