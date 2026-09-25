"""Technology fact vocabulary: equivalent objects, not equivalent obligations.

Original quotations are never rewritten. Consumers select canonical concepts;
delivery, ownership, testing and liability predicates are still checked separately.
"""
import re
from review_v2.license_terms import LICENSE_TYPE_PATTERN, declared_license_type


DOCUMENTS = {
    'source_and_executable_delivery': ('源代码或可执行程序交付', r'源代码|程序源码|源程序|source\s*code|可执行程序|可运行的软件|目标程序'),
    'generic_technical_documentation': ('技术文档交付', r'技术(?:资料|文档|文件)|开发文档|(?:数据库|系统|软件)设计文档|(?:接口|安装|部署)(?:文档|说明)'),
    'interface_document_delivery': ('接口文档交付', r'接口(?:文档|说明|指南)'),
    'architecture_document_delivery': ('架构文档交付', r'架构(?:文档|说明|设计)'),
    'installation_deployment_document': ('安装部署资料交付', r'(?:安装(?:部署)?|部署)(?:操作)?(?:指南|文档|说明|文件|手册|资料)'),
    'operation_document_delivery': ('用户或操作资料交付', r'(?:用户(?:使用|操作)?|操作|使用)(?:手册|指南|说明|文档)'),
    'test_report_delivery': ('测试报告交付', r'(?:验收)?测试(?:结果)?报告'),
    'defect_list_delivery': ('缺陷记录交付', r'(?:缺陷|bug|问题)\s*(?:清单|列表|记录)'),
}
DOCUMENT_ELEMENT_ALIASES = {
    'deployment_document_delivery': 'installation_deployment_document',
    'installation_document_delivery': 'installation_deployment_document',
}
FACT_KEY_ALIASES = {
    **{'development_documents.' + key: 'development_documents.' + value
       for key, value in DOCUMENT_ELEMENT_ALIASES.items()},
    'development_acceptance.test_report_delivery': 'development_documents.test_report_delivery',
    'development_acceptance.acceptance_metrics': 'technology.transaction.acceptance',
}


def document_concept(key):
    return DOCUMENT_ELEMENT_ALIASES.get(key, key)


def document_pattern(key):
    return DOCUMENTS[document_concept(key)][1]


def mentions_document(key, text, context=''):
    concept = document_concept(key)
    if not re.search(document_pattern(key), text, re.I):
        return False
    if concept == 'defect_list_delivery' and re.search(r'问题(?:清单|列表|记录)', text):
        return bool(re.search(r'技术|软件|系统|代码|测试|缺陷|bug', text + context, re.I))
    return True


# Actions remain separate canonical dimensions: handling a claim does not by
# itself prove payment of damages, and a refund never means returning equipment.
ACTION_PATTERNS = {
    # Nominal grants and permission-with-exclusion are different from ownership.
    'technical_use_entitlement': r'(?:享有|获得|取得).{0,35}(?:使用|实施|商业利用)权',
    'limited_technical_use': r'(?:有权|可以|可).{0,8}(?:继续)?使用.{0,35}(?:不包含|不涉及|不披露).{0,65}(?:通用技术|技术经验|技术成果)',
    'payment_refund': r'退款|(?:退还|返还|退回).{0,12}(?:已支付|已付款|已收款|预付款|开发费用|转让费|价款|许可费)',
    'third_party_claim_handling': r'(?:负责|应|须).{0,10}(?:处理|应对|解决).{0,18}(?:第三方索赔|第三方权利主张)|(?:第三方索赔|第三方权利主张).{0,18}(?:负责|应|须).{0,10}(?:处理|应对|解决)',
    'third_party_liability_party': r'(?:承担|负责).{0,18}(?:第三方权利主张责任|侵权责任|赔偿责任|合理损失)',
}


def matches_action(key, text):
    if re.search(r'不(?:予|再)?(?:退款|退还|返还|承担)|无需(?:退款|承担)', text):
        return False
    return bool(re.search(ACTION_PATTERNS[key], text))


# Used after the shared third-party-event and actor resolver. Event context is
# required by the caller; an isolated general duty is not a claim-handling fact.
CLAIM_ACTIONS = {
    'handling': r'(?:负责|应当|应|须|自行).{0,12}?(?:交涉|处理|应诉|抗辩|诉讼|行政程序)(?!费|成本)',
    'liability_party': r'(?:承担|负担).{0,40}(?:法律责任|赔偿责任|侵权责任|损失)|(?:法律责任|赔偿责任|侵权责任).{0,30}(?:承担|负担)|赔偿(?:全部|直接|相应|合理)?损失',
}


def claim_action(key, text):
    return re.search(CLAIM_ACTIONS[key], text)


# Event, actor, modality and remedy are distinct dimensions. A beneficiary
# between 应 and 支付/赔偿 does not interrupt the obligation; a liability cap
# mentioning confidentiality does not establish an operative breach remedy.
CONFIDENTIALITY_BREACH = (
    r'(?:违反|违背)[^。；]{0,30}(?:保密|秘密)|泄密|'
    r'泄露[^。；]{0,25}(?:保密|秘密)|未经授权披露|超出本合同目的使用'
)


def has_confidentiality_remedy(text):
    for sentence in re.split(r'[。；;]', re.sub(r'\s+', '', text)):
        trigger = re.search(CONFIDENTIALITY_BREACH, sentence)
        if not trigger:
            continue
        tail = sentence[trigger.end():]
        if re.search(r'(?:无需|不必|无须|不承担|免除).{0,12}(?:赔偿|责任|违约金)', tail):
            continue
        action = re.search(
            r'(?:应当|应|须|必须|负责|由)[^。；]{0,40}?'
            r'(?:支付[^。；]{0,45}违约金|承担(?:违约|赔偿|损害赔偿)责任|'
            r'赔偿[^。；]{0,35}损失|停止[^。；]{0,20}(?:披露|使用)|采取[^。；]{0,20}(?:措施|补救))', tail)
        if action:
            # Merely defining the maximum of an otherwise unproven liability
            # is different from imposing a remedy for this breach event.
            if re.search(r'(?:责任.{0,6})?(?:最高|上限|以.{0,25}为限|不超过)', tail) and not re.search(
                    r'支付.{0,45}违约金|赔偿.{0,35}损失|停止|采取', action[0]):
                continue
            return True
        if re.match(r'(?:的|时)?[：:，,](?:支付|承担|赔偿).{0,65}(?:违约金|损失|赔偿责任)', tail):
            return True
    return False


LICENSE_COMPONENTS = {
    'patent_name': r'专利(?:技术)?名称[：:].+|[“\"]?专利技术[”\"]?(?:是)?指.{0,150}(?:技术|方法|装置)',
    'patent_number': r'专利(?:号|编号)[为：:]?\s*(?:ZL)?[A-Z0-9][A-Z0-9.]{5,}',
    'implementation_acts': r'(?:授予|许可|授权).{0,65}(?:制造|生产|设计).{0,40}(?:使用|销售|出口).{0,25}(?:许可|权)',
    'territory': r'许可(?:地域|区域|地区|范围)[：:].+|(?:授予|许可).{0,25}在.{1,30}(?:制造|生产|设计|使用|销售)',
    'term': r'(?:许可期限|合同有效期|本合同有效期).{0,35}(?:\d+|[一二三四五六七八九十]+)(?:年|个月|月|日)|许可期限[：:].{0,50}至',
    'type': LICENSE_TYPE_PATTERN,
    'transfer_boundary': r'(?:许可权|实施权|使用权).{0,35}(?:不可转让|不得转让|不得再许可)|(?:不得|禁止|未经.{0,15}同意不得).{0,20}(?:转让许可权|转许可|再许可)',
}
LICENSE_ELEMENTS = (
    ('licensed_patent_subject', '许可标的', ('patent_name', 'patent_number')),
    ('permitted_implementation_acts', '实施方式', ('implementation_acts',)),
    ('license_territory', '许可地域', ('territory',)),
    ('license_term', '许可期限', ('term',)),
    ('license_type', '许可类型', ('type',)),
    ('transfer_or_sublicense_boundary', '许可权转让或再许可边界', ('transfer_boundary',)),
)


def license_scope_elements(clauses):
    from review_v2.obligation_detail_elements import _segments, _element
    from review_v2.technology_patent_transfer_analysis import _declared_party_aliases
    text = '\n'.join(c.text for c in clauses)
    recipient_aliases = _declared_party_aliases(text, r'(?:被许可方|被许可人|接受方|买方)')
    recipient = '(?:被许可方|被许可人|接受方|买方' + ''.join('|' + re.escape(p) for p in sorted(recipient_aliases)) + ')'
    found = {key: [] for key in LICENSE_COMPONENTS}
    for clause, _, quote in _segments(clauses):
        # Field values inherit their operative licence scope, not an unrelated
        # place/address or a historical third-party grant elsewhere in the text.
        context = str(getattr(clause, 'heading_path', '')) + clause.text
        scope_context = bool(re.search(r'许可范围|实施范围|范围内实施', context))
        field_patterns = {
            'territory': r'(?:^|\n)\s*(?:地域|区域|地区)[：:]\s*[^；。]+',
            'implementation_acts': r'(?:^|\n)\s*实施方式[：:]\s*[^；。]+',
        }
        for key, pattern in LICENSE_COMPONENTS.items():
            if key == 'type' and not declared_license_type(quote):
                continue
            if key in {'term', 'type'}:
                if re.search(r'既有许可|曾(?:于|向)|已披露', quote):
                    continue
                # Negation/violation must govern this component, not another
                # obligation in the same sentence (e.g. a five-year term plus
                # a prohibition on exceeding the licensed territory).
                matches = list(re.finditer(pattern, quote, re.I))
                if not any(not re.search(r'(?:违反|不得|不存在|另行协商)[^，；。\n]{0,12}$',
                                         quote[:m.start()]) for m in matches):
                    continue
            if key == 'transfer_boundary':
                # A licensor's promise not to license a competitor is not a
                # restriction on the recipient's assignment or sublicensing.
                if recipient_aliases:
                    if re.search(recipient + r'.{0,20}不得.{0,45}(?:转让|分许可|转许可|再许可)', quote):
                        found[key].append(dict(clause_id=clause.clause_id, quote=quote, component_key=key))
                    continue
            if re.search(pattern, quote, re.I) or (scope_context and key in field_patterns
                                                  and re.search(field_patterns[key], quote)):
                found[key].append(dict(clause_id=clause.clause_id, quote=quote, component_key=key))
    result = []
    for key, label, components in LICENSE_ELEMENTS:
        sources = [s for component in components for s in found[component]]
        missing = [c for c in components if not found[c]]
        result.append(_element(key, label, sources,
            status='PARTIALLY_COVERED' if sources and missing else 'COVERED' if sources else 'MISSING',
            source_fact_key='technology.license_scope.' + key,
            residuals=[label] if missing else []))
    return result


def registration_elements(clauses):
    from review_v2.technology_patent_transfer_analysis import extract_transfer_registration_facts
    from review_v2.obligation_detail_elements import _element
    facts = extract_transfer_registration_facts(clauses)
    labels = {'registration_responsible_party': '专利申请权转让登记的具体办理主体',
              'registration_deadline': '专利申请权转让登记的提交期限',
              'registration_cooperation': '申请人变更及申请权转让登记材料配合义务'}
    return [_element(key, label, facts.get(key, []), source_fact_key='technology.registration.' + key)
            for key, label in labels.items()]


def register_ontology_facts(graph, clauses):
    from review_v2.obligation_detail_elements import development_document_elements, _segments
    by_id = {c.clause_id: c for c in clauses}
    for element in development_document_elements(clauses):
        for source in element['supporting_evidence']:
            graph.add(element['source_fact_key'], source['quote'], by_id[source['clause_id']],
                      source_span=source['quote'])
    for clause, _, quote in _segments(clauses):
        for key in ACTION_PATTERNS:
            if matches_action(key, quote):
                graph.add('technology.actions.' + key, quote, clause, source_span=quote)
