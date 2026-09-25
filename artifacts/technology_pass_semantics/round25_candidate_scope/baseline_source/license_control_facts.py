"""Typed sources for the existing licence-control requirements.

No rule status is inferred from a retrieval pool. Each predicate is executed
on parser-owned spans; compound controls retain separate premise sources.
"""
import re
from review_v2.license_terms import declared_license_type
from review_v2.obligation_detail_elements import _segments, _DURATION
from review_v2.proposition_scope import arrangement_matches

FAMILIES = ('license_mutual_confidentiality', 'license_secret_controls', 'license_scope_remedies', 'secret_license_scope', 'main_license_fee')
OBJECT = r'技术秘密|未公开|非公开|源代码|算法|控制参数|测试数据|生产数据|销售数据|客户资料|经营数据|保密内容|Know-how'
DUTY = r'承担保密义务|负有保密义务|应予保密'
DISCLOSURE = r'未经.{0,18}(?:书面)?同意.{0,25}不得.{0,25}(?:第三方|披露)|(?:不得|禁止).{0,30}第三方.{0,20}(?:转让|许可|提供|披露|泄露)'
PURPOSE = r'超出本合同目的使用|仅限本合同目的|为生产合同产品之目的|仅为履行本合同'
COPY = r'为.{0,18}(?:生产|履行).{0,18}目的.{0,12}(?:复制|编译|使用)'
BREACH = r'超范围实施|超出许可范围|违反(?:(?!排他|独占).){0,50}许可范围|擅自再许可|未经授权(?:分许可|转许可)|未经.{0,18}同意.{0,18}(?:分许可|转许可|再许可)|扩大许可(?:地域|用途)'
REMEDY = r'违约金|停止|承担(?:违约)?责任|赔偿'

# These predicates describe operative boundaries, not the occurrence of a
# transfer or termination. Prohibitions and consent conditions are affirmative
# arrangements; questions and absent arrangements retain their source polarity.
_DISPOSITION = r'(?:再许可|转许可|分许可|转让)'
_END = r'(?:合同(?:终止|解除)|许可(?:期限|期)?(?:届满|到期)|期限届满|合同期满)(?:或者|或|及|和)?[^。；;]{0,20}后'
_TRANSFER_BOUNDARY = (
    rf'(?:不得|禁止|不可|不允许)[^。；;]{{0,35}}{_DISPOSITION}'
    rf'|{_DISPOSITION}[^。；;]{{0,25}}(?:须|应当|应|需)[^。；;]{{0,25}}(?:同意|批准|授权)'
    rf'|(?<!未)(?:经|取得)[^。；;]{{0,25}}(?:同意|批准|授权)[^。；;]{{0,30}}(?:方可|可以|(?<!许)可(?!权)|有权)[^。；;]{{0,25}}{_DISPOSITION}'
)
_POST_USE_BOUNDARY = (
    rf'{_END}[^。；;]{{0,100}}(?<!不)(?<!无)(?<!毋)(?:应当|应|须|必须)[^。；;]{{0,8}}停止(?:继续)?(?:使用|实施)'
    rf'|{_END}[^。；;]{{0,100}}(?:不得|禁止)(?:继续)?(?:使用|实施)'
    rf'|{_END}[^。；;]{{0,40}}(?:继续使用|继续实施)[^。；;]{{0,25}}(?<!不)(?<!无)(?<!毋)(?:应当|应|须|必须|需)[^。；;]{{0,35}}(?:签订|订立|达成)[^。；;]{{0,12}}书面(?:协议|合同)'
)


def license_boundary_sources(clauses, pattern):
    """Resolve full proposition scopes before selecting exact original quotes."""
    rows = []
    for clause in clauses:
        if getattr(clause, 'block_type', '') == 'HEADING':
            continue
        if re.search(r'曾向|既有许可|后续改进|改进成果', str(getattr(clause, 'heading_path', '')) + clause.text):
            continue
        for source in arrangement_matches(pattern, clause.text):
            # Assignment of a receivable or return of equipment is not a
            # boundary on the licensed technology or implementation right.
            if not re.search(r'技术|许可权|再许可|转许可|分许可|实施权', source['quote']):
                continue
            rows.append(dict(clause_id=clause.clause_id, quote=source['quote'], location=clause.location))
    return rows


def elements(family, clauses):
    sources = [(c, q, re.sub(r'\s+', '', q)) for c, _, q in _segments(clauses)
               if getattr(c, 'block_type', '') != 'HEADING']
    def select(predicate):
        return [dict(clause_id=c.clause_id, quote=q, location=c.location)
                for c, q, t in sources if predicate(t)]
    def has(pattern, text):
        return bool(re.search(pattern, text, re.I))
    from review_v2.technology_patent_transfer_analysis import _declared_party_aliases
    contract_text = '\n'.join(c.text for c in clauses)
    providers = {'许可方', '许可人', '卖方'} | _declared_party_aliases(contract_text, r'(?:(?<!被)许可方|(?<!被)许可人|卖方)')
    recipients = {'被许可方', '被许可人', '买方', '接受方'} | _declared_party_aliases(contract_text, r'(?:被许可方|被许可人|买方|接受方)')
    def recipient_breach(text):
        event = re.search(BREACH, text)
        if not event or not has(REMEDY, text):
            return False
        actor = re.search(r'被许可方|被许可人|许可方|许可人|买方|卖方|接受方|[甲乙丙丁]方', text[:event.start()])
        return not (actor and actor[0] in providers and actor[0] not in recipients)
    # The domain label, licence price and delivery warranty are not a scope
    # definition. Require named information plus a secrecy/definition relation.
    named_information = r'源代码|算法|控制参数|测试数据|生产数据|销售数据|客户资料|经营数据|技术资料|经营信息'
    scope = select(lambda t: not has(r'(?:未使用|未利用).{0,30}(?:未公开|非公开|技术秘密)', t) and ((has(OBJECT, t) and has(DUTY, t)) or (has(named_information, t) and (
        has(r'(?:技术秘密|保密信息|保密内容).{0,12}(?:包括|为|是|[：:])', t)
        or has(r'(?:未公开|非公开).{0,30}(?:算法|资料|数据|源代码)', t)))))
    purpose = select(lambda t: has(PURPOSE, t))
    copy = select(lambda t: has(COPY, t))
    # Consent to transfer an implementation right is not consent to disclose
    # information. Require the restricted action and its information object.
    disclosure = select(lambda t: has(DISCLOSURE, t) and (
        has(r'(?:不得|禁止)[^。；]{0,50}(?:披露|泄露)', t)
        or has(r'(?:技术秘密|保密信息|技术资料|源代码|非公开信息)', t)
        and has(r'(?:提供|转让|许可)', t)))
    breach = select(recipient_breach)
    if family == 'main_license_fee':
        price = r'(?:固定许可费|许可使用费|许可费|使用费|许可费用)[^。；]{0,30}(?:[\d一二三四五六七八九十百千万][\d,，.一二三四五六七八九十百千万]*(?:万元|元)|免费|无偿)|(?:按|按照)[^。；]{0,25}(?:销售额|销售收入|净销售额)[^。；]{0,20}(?:%|％|百分之)'
        excluded = r'改进成果|后续改进|无效|丧失秘密|退还|赔偿|第三方主张'
        rows = [dict(clause_id=c.clause_id, quote=q, location=c.location)
                for c, q, t in sources
                if not has(excluded, str(getattr(c, 'heading_path', '')) + t)
                # _segments preserves a field label with its following value;
                # whitespace is presentation, not a new legal relationship.
                and list(arrangement_matches(price, t))]
        specs = [('main_license_fee_arrangement', '主合同许可使用费约定', rows)]
    elif family == 'secret_license_scope':
        # Bind this grant, not historical grants to third parties or future
        # improvements. Field labels and values remain in parser-owned spans.
        current = [(c, q, t) for c, q, t in sources
                   if not has(r'曾向|许可他人|既有许可|后续改进|改进成果', str(getattr(c, 'heading_path', '')) + t)]
        def grant(pattern):
            return [dict(clause_id=c.clause_id, quote=q, location=c.location)
                    for c, q, t in current if has(pattern, t)]
        specs = [
            ('licensed_secret_subject', '技术秘密标的', grant(r'(?:技术秘密(?:名称|的内容|内容)?[：:]|(?:未公开|非公开).{0,20})(?:[^。；]{0,50})(?:算法|源代码|技术|参数|方法|工艺|Know-how)')),
            ('permitted_implementation_acts', '实施范围和方式', grant(r'(?:买方|被许可[方人]).{0,18}(?:仅可|可以|有权|可).{0,65}(?:研发|生产|销售|制造|复制|编译|使用)|(?:授予|许可).{0,30}(?:研发|生产|销售|制造|复制|编译|使用)')),
            ('license_territory', '许可地域', grant(r'(?:许可地域|实施地域)[：:]?[^。；]+|(?:买方|被许可[方人]).{0,15}(?:仅可|可以|有权|可)在[^。；]{0,40}(?:地区|境内|境外|区域|全国|全世界)')),
            ('license_term', '许可期限', grant(r'(?:本合同|合同|许可|实施)(?:的)?(?:有效)?(?:期|期限)'
                rf'(?:自)?.{{0,45}}(?:\d{{4}}年\d+月\d+日|{_DURATION}|起至|届满)')),
            ('license_type', '许可类型', [dict(clause_id=c.clause_id, quote=q, location=c.location)
                 for c, q, t in current if declared_license_type(t)]),
            ('transfer_or_sublicense_boundary', '向第三方转让、许可或提供边界', license_boundary_sources(clauses, _TRANSFER_BOUNDARY)),
            ('post_termination_use_boundary', '许可期限与终止后继续使用权的边界', license_boundary_sources(clauses, _POST_USE_BOUNDARY)),
        ]
    elif family == 'license_mutual_confidentiality':
        specs = [
            ('mutual_confidentiality_responsibility', '双方均承担保密义务', select(lambda t: has(r'双方|各方|任何一方', t) and has(DUTY, t))),
            ('confidential_information_scope', '双方商业和技术保密信息范围', scope),
            ('third_party_disclosure_restriction', '未经信息提供方同意不得披露', disclosure),
            ('post_termination_confidentiality', '双方终止后保密期限', select(lambda t: has(r'双方|各方|任何一方', t) and has(r'保密', t) and has(r'(?:终止|解除)后.{0,20}(?:\d+|[一二两三四五六七八九十]+)年', t))),
        ]
    elif family == 'license_secret_controls':
        specs = [
            ('confidential_information_scope', '受保护的技术秘密范围', scope),
            ('confidential_personnel_control', '涉密人员及知悉必要性', select(lambda t: has(r'涉密人员范围|确有知悉必要|直接参与本项目', t))),
            ('contract_purpose_use_restriction', '合同目的使用限制', purpose),
            ('third_party_transfer_disclosure_restriction', '第三方转让或披露限制', disclosure),
            ('purpose_scoped_copying_boundary', '目的内复制权限和使用边界', copy + [r for r in purpose if r not in copy] if copy and purpose else []),
        ]
    else:
        def remedy_sources(pattern):
            return [r for r in breach if list(arrangement_matches(pattern, r['quote']))]
        def general_remedy_sources(pattern):
            # A general-remedy sentence in the same operative provision can
            # govern the preceding breach. Preserve its own exact span; do
            # not require repetition of the breach phrase in every sentence.
            context_ids = {r['clause_id'] for r in breach}
            return remedy_sources(pattern) + [dict(clause_id=c.clause_id,quote=q,location=c.location)
                for c,q,t in sources if c.clause_id in context_ids and has(pattern,t)
                and has(r'一般违约|违约赔偿|上述责任|该责任|故意或重大过失',t)
                and not has(BREACH,t)]
        specs = [
            ('over_scope_breach_remedy', '超范围违约责任', breach),
            ('damage_compensation', '超范围违约损失赔偿', remedy_sources(r'赔偿[^。；]{0,45}损失|(?:造成|遭受)[^。；]{0,25}损失[^。；]{0,30}(?<!不)(?<!无须)(?<!无需)(?:承担|负责)[^。；]{0,10}赔偿')),
            ('stop_breach_obligation', '超范围违约停止义务', remedy_sources(r'停止(?:违约行为|超范围实施|使用|分许可|转许可|再许可)|立即停止')),
            ('unauthorized_transfer_or_sublicense_liability', '未经授权向第三方转让或再许可责任', remedy_sources(r'禁止擅自向第三方|擅自再许可|未经授权(?:分许可|转许可)')),
            ('fixed_penalty', '超范围固定违约金', remedy_sources(r'违约金') if any(has(r'[\d,]+元', r['quote']) for r in breach) else []),
            ('cumulative_remedy_boundary', '违约金与赔偿的抵扣并用', remedy_sources(r'不重复计算|抵扣|以较高者为准|赔偿差额|违约金不足以弥补')),
            ('over_scope_liability_cap', '超范围责任总额边界', general_remedy_sources(r'责任上限|赔偿上限|最高不超过|总额不超过')),
            ('over_scope_breach_differentiation', '不同超范围行为的责任区分', general_remedy_sources(r'一般违约|严重违约|重大违约|故意|重大过失')),
        ]
    # Fact identity is shared across families. Original spans carry the actor,
    # object, modality and exceptions; they are never synthesized into a quote.
    return [dict(element_id=k, source_fact_key='license_control.' + k,
                 required_fact=label, proposition=label, search_targets=[label],
                 status='COVERED' if rows else 'MISSING', supporting_evidence=rows,
                 residual_gap='' if rows else label) for k, label, rows in specs]
