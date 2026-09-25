"""Typed cooperative predicates and projections onto existing requirement keys.

These are source facts, not topic retrieval candidates. Every source retains
the original parser clause and exact span; partial composite objects keep their
unproved limbs as residual requirements.
"""
import re
from review_v2.obligation_detail_elements import _segments, development_document_elements

LABELS = {
    'development_schedule_and_milestones': '研发期限、工作进度和交付节点',
    'funding_investment': '现金资金投入金额及承担方式',
    'authorized_internal_users': '合作方及其授权人员使用未公开技术成果的范围',
    'independent_use_right': '合作方自行使用成果的权利',
    'external_license_transfer_disclosure': '对外许可、转让及披露的同意程序',
    'post_termination_use_boundary': '合作终止后继续使用成果的边界',
    'confidential_use_restriction': '保密信息仅限为履行合作项目而使用',
    'component_selection_control': '第三方组件的选择主体及使用权限',
    'component_license_cost_allocation': '第三方组件许可费用承担',
    'deployment_and_operation_documentation': '部署和运行文档',
}


def elements(clauses):
    sources = {key: [] for key in LABELS}
    residuals = {}
    # Structured party / contribution-type / amount fields form one fact.
    # Keep the actor heading and adjacent fields as an exact source span;
    # a non-cash valuation must not be projected into cash funding.
    for clause in clauses:
        actors = list(re.finditer(r'(?m)^\s*[甲乙丙丁戊]方[：:]?\s*$', clause.text))
        for index, actor in enumerate(actors):
            end = actors[index + 1].start() if index + 1 < len(actors) else len(clause.text)
            block = clause.text[actor.start():end]
            amount = re.search(r'(?:投资|投入|出资)?金额[：:]\s*(?:人民币)?[\d,，.一二三四五六七八九十百千万亿零壹贰叁肆伍陆柒捌玖拾佰仟]+元', block)
            if amount and re.search(r'提供方式[：:].{0,25}(?:货币|现金)|(?:货币|现金)(?:出资|投资|投入)', block[:amount.start()]):
                sources['funding_investment'].append(dict(clause_id=clause.clause_id,
                    quote=block[:amount.end()].strip()))
    for clause, heading, quote in _segments(clauses):
        text = re.sub(r'\s+', '', quote)
        context = re.sub(r'\s+', '', heading + str(getattr(clause, 'title', '')))
        if getattr(clause, 'block_type', '') == 'HEADING':
            continue
        def add(key, residual=''):
            source = dict(clause_id=clause.clause_id, quote=quote)
            if source not in sources[key]:
                sources[key].append(source)
            if residual:
                residuals[key] = residual
        if (re.search(r'开发|研发|阶段|进度|里程碑', text + context)
                and re.search(r'\d{4}(?:年|[-/.])\d{1,2}', text)
                and re.search(r'至|到|—|－|完成|提交|交付|阶段|验收', text)):
            add('development_schedule_and_milestones')
        if (re.search(r'费用|经费|投入|投资|预算', context)
                and not re.search(r'违约|赔偿|责任', context)
                and re.search(r'[甲乙丙丁]方.{0,15}(?:承担|投入|支付|出资).{0,12}(?:人民币)?[\d,]+元', text)):
            add('funding_investment')
        result_object = bool(re.search(r'共同(?:开发)?成果|合作(?:开发)?成果|技术秘密成果|项目成果', text)
                             or (re.search(r'成果|知识产权', context) and '完整系统' in text))
        if result_object and re.search(r'(?:任何一方|各方|双方|[甲乙]方).{0,15}(?:可|有权|允许).{0,30}(?:使用|用于)', text):
            add('independent_use_right')
            add('authorized_internal_users', '' if re.search(r'员工|人员|授权使用人', text) else '合作方授权人员的成果使用范围')
        if result_object and re.search(r'同意|许可|确认', text) and re.search(r'转让|出售|独占|排他|披露', text):
            gaps = [label for label, pattern in (
                ('第三方普通许可的同意程序', r'普通许可|非独占许可'),
                ('对外披露的同意程序', r'披露'),
            ) if not re.search(pattern, text)]
            add('external_license_transfer_disclosure', '、'.join(gaps))
        if re.search(r'终止|解除|退出', text) and re.search(r'成果', text) and re.search(r'使用|许可|依.{0,12}第.{1,8}条', text):
            add('post_termination_use_boundary', '终止后成果继续使用的具体权限和条件')
        if (re.search(r'不得|禁止|仅限', text) and re.search(r'用于|使用', text)
                and re.search(r'本项目|本合同|合作项目', text)
                and re.search(r'以外|之外|仅限', text) and re.search(r'信息|资料|数据|技术|代码', text)):
            add('confidential_use_restriction', '' if re.search(r'保密信息|技术秘密|保密资料', text) else '其他类别保密信息的项目外使用限制')
        if (re.search(r'第三方|开源|API|组件', text) and re.search(r'(?:双方|各方|[甲乙丙]方).{0,35}(?:可|有权|自行).{0,35}(?:采用|选用|使用|选择)', text)):
            add('component_selection_control')
        elif re.search(r'(?:项目|合同).{0,8}允许使用.{0,50}(?:开源|第三方|API)', text):
            add('component_selection_control', '第三方组件的具体选型主体和确认程序')
        elif re.search(r'引入第三方组件的一方.{0,15}(?:应|须).{0,20}(?:说明|披露)', text):
            add('component_selection_control', '第三方组件的具体选型主体和确认程序')
        if re.search(r'第三方|API|组件|开源', text) and re.search(r'费|价款|购买|采购', text) and re.search(r'承担|分担|协商|结算', text):
            deferred = bool(re.search(r'另行协商|另行约定|待定', text))
            add('component_license_cost_allocation', '第三方组件许可费用的具体分担方式' if deferred else '')
    documents = {e['element_id']: e for e in development_document_elements(clauses)}
    # Aliases belong to the shared document ontology, not this rule's wording.
    from review_v2.technology_fact_ontology import document_concept
    selected = [e for key, e in documents.items() if document_concept(key) in {
        'installation_deployment_document', 'operation_document_delivery'}]
    sources['deployment_and_operation_documentation'] = [s for e in selected for s in e['supporting_evidence']]
    gaps = [e['required_fact'] for e in selected if e['status'] != 'COVERED']
    if gaps:
        residuals['deployment_and_operation_documentation'] = '、'.join(gaps)
    return [dict(element_id=key, source_fact_key='cooperative.' + key,
                 required_fact=label, proposition=label,
                 status='PARTIALLY_COVERED' if sources[key] and residuals.get(key) else 'COVERED' if sources[key] else 'MISSING',
                 residual_gap=residuals.get(key, '') if sources[key] else '',
                 search_targets=[residuals.get(key) or label], supporting_evidence=sources[key],
                 bound_evidence_ids=list(dict.fromkeys(s['clause_id'] for s in sources[key])))
            for key, label in LABELS.items()]
