"""Typed technical-service arrangements, with predicate-owned original spans.

The same definitions publish registry facts and resolve final report elements.
An occurrence/heading is not an obligation; absence and permission keep their
own objects and list scope. This module does not classify contracts.
"""
import re
from review_v2.obligation_detail_elements import _element, _DURATION
from review_v2.proposition_scope import arrangement_matches
from review_v2.verified_source import exact_span


FAMILIES = ('ancillary_service_content', 'ancillary_service_quality', 'service_content', 'service_payment', 'service_quality',
            'service_results', 'service_claims', 'material_exit', 'component_inventory',
            'confidentiality_controls', 'confidentiality_disclosure', 'confidentiality_scope_controls')
RULE_FAMILIES = {'TC-09-01': 'service_content', 'TC-09-04': 'service_payment',
                 'TC-09-02': 'service_quality', 'TC-09-03': 'service_results',
                 'TC-12-02': 'service_claims', 'TC-11-03': 'material_exit',
                 'TC-03-04': 'component_inventory', 'TC-13-02': 'component_inventory'}
PARTY = r'(?:[甲乙丙丁]方|双方|服务方|服务提供方|受托方|委托方|客户|接收方)'


def claim_missing_consequence(missing_elements):
    """Derive the effect of each unresolved claim-process dimension.

    This consumes final atomic states. A sourced covered component contributes
    no missing consequence, and the text never comes from a report template.
    """
    missing = {row['element_id'] for row in missing_elements}
    dimensions = (
        ({'third_party_claim_trigger', 'claim_handling_responsibility',
          'provider_infringement_liability', 'direct_damage'},
         '第三方提出权利主张后，受理索赔、组织应对和承担直接损失的主体可能无法确定'),
        ({'notification_requirement', 'notification_deadline', 'necessary_assistance'},
         '通知期限及协助义务不清，可能延误证据保全和争议应对'),
        ({'defense_control', 'lawyer_selection', 'settlement_authority'},
         '抗辩、律师选择与和解决策缺乏控制边界，可能出现未经相关方参与即承认责任或作出和解'),
        ({'defense_cost_allocation', 'third_party_compensation'},
         '抗辩费用和对第三方的赔偿由谁承担不清，可能引发额外费用及追偿争议'),
        ({'replacement_remedy', 'license_cure'},
         '缺少替代方案或取得授权的修复路径，可能导致有关成果无法继续使用'),
        ({'termination_remedy', 'refund_remedy'},
         '权利瑕疵无法修复时缺少解除及退款安排，可能使已付款项和终止后的救济难以处理'),
    )
    parts = []
    for keys, effect in dimensions:
        labels = [str(row.get('residual_gap') or row.get('required_fact') or '').strip('。；; ')
                  for row in missing_elements if row['element_id'] in keys]
        if labels:
            parts.append('、'.join(label for label in labels if label) + '未明确时，' + effect)
    return '；'.join(parts) + '。' if parts else ''


def sources(clauses, pattern, *, context=None, inherit_lists=False):
    result = []
    for clause in clauses:
        if getattr(clause, 'block_type', '') in {'TITLE', 'HEADING'}:
            continue
        if context and not re.search(context, clause.text):
            continue
        for match in arrangement_matches(pattern, clause.text, inherit_lists=inherit_lists):
            original = getattr(clause, 'raw_text', '') or clause.text
            span = exact_span(original, match['quote'])
            if not span:
                continue
            row = dict(clause_id=clause.clause_id, quote=original[span[0]:span[1]],
                       location=clause.location, proposition_polarity='AFFIRMATIVE',
                       predicate_pattern=pattern, condition=match.get('condition', ''))
            if row not in result:
                result.append(row)
    return result


def _rows(family, specs):
    return [_element(key, label, proof, source_fact_key='technology.' + family + '.' + key)
            for key, label, proof in specs]


def shared_deployment_acceptance(clauses):
    """Reuse acceptance only when its deliverable is an actual service activity.

    File delivery/asset metrics alone do not establish deployment service quality.
    A matching operative deployment requirement links the two legal relations.
    """
    service = [c for c in clauses if re.search(r'技术服务|技术支持|实施服务', c.text + c.title)]
    activities = [a for a in ('部署', '安装', '调试', '配置')
                  if sources(service, r'(?:应|须|提供)[^。；]{0,50}' + a, inherit_lists=True)]
    if not activities:
        return []
    result = []
    for c in clauses:
        if not re.search(r'验收', c.title + c.text):
            continue
        if sources([c], r'(?:完成|实现)[^。；]{0,25}(?:' + '|'.join(activities) + r')', inherit_lists=True):
            result.append(c)
    return result


def elements(family, clauses):
    def find(pattern, **kw):
        return sources(clauses, pattern, **kw)
    if family == 'confidentiality_scope_controls':
        # The scope/obligation rule does not require every security control or
        # a fixed duration (reviewed separately). Publish stated controls as
        # additional facts without importing another rule's missing checklist.
        return [e for e in elements('confidentiality_controls', clauses)
                if e['element_id'] in {'confidential_information_scope', 'confidentiality_obligation'}
                or e['element_id'] in {'need_to_know_personnel', 'third_party_disclosure_restriction'} and e['supporting_evidence']]
    if family in {'confidentiality_controls', 'confidentiality_disclosure'}:
        from review_v2.obligation_detail_elements import confidentiality_detail_elements
        from review_v2.engine import extract_semantic_field_value
        facts = {e['element_id']:e for e in confidentiality_detail_elements(clauses, extract_field=extract_semantic_field_value)}
        # A defined secret is itself the confidentiality object; the concrete
        # scope need not be repeated under a later confidentiality heading.
        from review_v2.requirement_entailment import technical_secret_identity_support
        if not facts['confidential_information_scope']['supporting_evidence']:
            secret_scope = [s for s in find(r'(?:技术秘密|专有技术)[^。；]{0,12}(?:主要包括|包括|范围|内容)[：:]?', inherit_lists=True)
                            if technical_secret_identity_support(s['quote'])]
            if secret_scope:
                facts['confidential_information_scope'] = _element('confidential_information_scope', '保密信息类别和范围', secret_scope,
                    source_fact_key='technology.confidentiality_controls.confidential_information_scope')
        if family == 'confidentiality_controls':
            mappings = [('confidential_information_scope','confidential_information_scope'),
                        ('during_contract_confidentiality','confidentiality_obligation'),
                        ('confidential_personnel_scope','need_to_know_personnel'),
                        ('confidentiality_duration','confidentiality_duration')]
            atoms = [{**facts[a], 'element_id':b} for a,b in mappings]
            atoms += _rows(family, [
                ('purpose_limitation','保密数据的合同目的使用限制',find(r'(?:只能|仅可|仅限)[^。；]{0,35}(?:本项目|咨询目的|合同目的)[^。；]{0,25}(?:处理|使用)')),
                ('third_party_disclosure_restriction','向第三方披露的限制',find(r'未经[^。；]{0,25}同意[^。；]{0,35}不得[^。；]{0,35}(?:披露|泄露)|不得[^。；]{0,25}第三方[^。；]{0,12}(?:披露|提供)', context=r'秘密|保密')),
                ('copying_restriction','保密资料复制限制',find(r'(?:不得|禁止|仅可)[^。；]{0,25}复制',context=r'保密|秘密')),
                ('security_measures','保密信息安全措施',find(r'(?:应|须)[^。；]{0,25}(?:加密|访问控制|权限管理)',context=r'保密|秘密|信息'))])
            return atoms
        specs = [('confidential_information_scope','保密信息范围',facts['confidential_information_scope']['supporting_evidence']),
                 ('confidentiality_period','保密期限',facts['confidentiality_duration']['supporting_evidence'])]
        components = facts['confidentiality_exceptions']['component_coverage']
        for key, component in zip(('public_information_exception','lawful_third_party_source_exception',
                                   'independent_development_exception','compelled_disclosure_exception'),components):
            specs.append((key,component['required_fact'],component['supporting_evidence']))
        specs.append(('prior_notice_when_legally_permitted','依法强制披露时在法律允许范围内提前通知',
            find(r'(?:应|须)[^。；]{0,25}(?:法律允许|依法允许)[^。；]{0,12}(?:提前|事先)通知[^。；]{0,12}(?:另一方|对方|甲方|乙方|让与方|受让方)',context=r'法律|机关')))
        return _rows(family,specs)
    if family == 'ancillary_service_content':
        # Consume the existing ancillary service elements through predicate-owned
        # spans. The transfer subject and its acceptance do not prove service quality.
        activity = r'(?:部署指导|现场部署|线上培训|技术答疑|参数配置|故障排查|实施说明|技术培训|技术指导)'
        scoped = [c for c in clauses if re.search(r'技术服务|技术支持|技术指导|培训', c.text)]
        def service_find(pattern):
            return sources(scoped, pattern, inherit_lists=True)
        content = service_find(r'(?:应当|应|须|提供)[^。；]{0,50}' + activity + r'|' + activity + r'[^。；]{0,12}(?:支持|服务)')
        specs = [
            ('service_existence', '技术服务或培训安排', content),
            ('service_scope', '技术服务工作范围', content),
            ('service_content', '技术服务具体内容', content),
            ('service_response_time', '技术服务响应时间', service_find(r'(?:响应|接到[^。；]{0,12}(?:通知|请求))[^。；]{0,20}' + _DURATION)),
            ('service_delivery_standard', '技术服务交付标准', service_find(r'(?:技术服务|培训|技术指导)[^。；]{0,30}(?:达到|合格标准|交付标准)')),
            ('service_period', '技术服务期限', service_find(r'技术服务期限[：:]?[^。；]{0,20}' + _DURATION)),
            ('service_method', '技术服务方式', service_find(r'(?:远程|线上|现场)[^。；]{0,15}(?:技术|部署|培训|服务)')),
            ('service_frequency', '技术服务频次', service_find(r'(?:\d+|[一二三四五六七八九十两]+)次[^。；]{0,15}(?:技术|部署|培训|服务)')),
        ]
        result = _rows(family, specs)
        linked = shared_deployment_acceptance(clauses)
        if linked:
            standard = next(e for e in result if e['element_id']=='service_delivery_standard')
            proof = sources(linked, r'验收标准[：:]|(?:完成|实现)[^。；]{0,25}(?:部署|安装|调试|配置)', inherit_lists=True)
            if proof and not standard['supporting_evidence']:
                # Only actual additional service activities can leave residual gaps.
                other = [label for pattern,label in ((r'培训','培训'), (r'远程[^。；]{0,8}(?:答疑|支持)','远程答疑'),
                         (r'故障排查','故障排查'), (r'实施说明','实施说明'))
                         if service_find(pattern)]
                residuals = ['及'.join(other) + '的交付标准'] if other else []
                components = [dict(element_id='deployment_standard',status='COVERED',required_fact='部署服务验收标准',supporting_evidence=proof)]
                if residuals:
                    components.append(dict(element_id='other_service_standard',status='MISSING',required_fact=residuals[0],supporting_evidence=[]))
                standard.update(_element('service_delivery_standard', '技术服务交付标准', proof,
                    status='PARTIALLY_COVERED' if residuals else 'COVERED', residuals=residuals,
                    source_fact_key='technology.ancillary_service_content.service_delivery_standard',
                    component_coverage=components))
        period = next(e for e in result if e['element_id'] == 'service_period')
        if not period['supporting_evidence']:
            remote = service_find(_DURATION + r'[^。；]{0,12}(?:远程[^。；]{0,8}(?:答疑|支持))')
            if remote:
                period.update(_element('service_period', '技术服务期限', remote,
                    status='PARTIALLY_COVERED', residuals=['现场部署及培训的履行期限'],
                    source_fact_key='technology.ancillary_service_content.service_period',
                    component_coverage=[dict(element_id='remote_support_period', status='COVERED', required_fact='远程答疑期限', supporting_evidence=remote),
                                        dict(element_id='other_service_period', status='MISSING', required_fact='现场部署及培训的履行期限', supporting_evidence=[])]))
        return result
    if family == 'ancillary_service_quality':
        linked = shared_deployment_acceptance(clauses)
        if not linked:
            return []
        def acceptance(pattern):
            return sources(linked, pattern, inherit_lists=True)
        specs = [
            ('objective_acceptance_standard','部署服务质量和验收标准',acceptance(r'验收标准[：:]|(?:准确率|误报率)[^。；]{0,18}\d|连续运行[^。；]{0,15}无[^。；]{0,10}故障|完成[^。；]{0,20}部署')),
            ('acceptance_process','验收组织程序',acceptance(PARTY+r'[^。；]{0,50}(?:完成|组织|进行)验收')),
            ('acceptance_deadline','验收期限',acceptance(_DURATION+r'内[^。；]{0,12}(?:完成|进行)?验收')),
            ('written_objection_mechanism','验收书面异议程序',acceptance(r'(?:应|须)[^。；]{0,35}书面[^。；]{0,20}(?:问题|异议|意见)')),
            ('rectification_mechanism','验收不合格后的补充修正',acceptance(r'(?:应|须)[^。；]{0,50}(?:整改|补正|修正)')),
            ('rectification_deadline','补正期限',acceptance(_DURATION+r'内[^。；]{0,20}(?:整改|补正|修正)')),
            ('reinspection_procedure','补正后的复验程序',acceptance(r'(?:有权|应|可)[^。；]{0,20}(?:第二次验收|再次验收|复验|重新验收)')),
            ('reinspection_deadline','复验期限',acceptance(_DURATION+r'内[^。；]{0,20}(?:第二次验收|再次验收|复验|重新验收)')),
        ]
        return _rows(family,specs)
    if family == 'service_content':
        from review_v2.technology_transaction_evidence import extract_elements
        atoms = extract_elements('technical_service_subject', clauses)
        proof = [s for e in atoms if e['element_id'] in {'technical_service_scope', 'technical_service_activities'}
                 for s in e['supporting_evidence']]
        return _rows(family, [('core_contract_arrangement', '技术服务内容', proof)])
    if family == 'service_payment':
        amount = r'(?:人民币\s*)?(?:\d[\d.,，]*\s*万?元|[一二三四五六七八九十百千万]+元|免费|无偿)'
        explicit = find(r'(?:技术服务费|服务费|服务报酬|服务费用)[^。；;]{0,25}' + amount)
        # A clause heading supplies the legal relation while its first operative
        # sentence supplies the amount. Proposition splitting intentionally does
        # not merge those sentences, so bind the amount sentence under the
        # verified service-fee heading instead of falling back to lexical context.
        scoped = sources(
            [c for c in clauses if re.search(r'(?:技术)?服务(?:费用|费|报酬)(?:及支付|与支付)?', c.title)],
            r'(?:本合同)?(?:含税)?(?:总价|价款|费用|报酬)[^。；;]{0,18}(?:为|共计|合计|：|:)[^。；;]{0,8}' + amount,
        )
        proof = []
        for source in [*explicit, *scoped]:
            if (source['clause_id'], source['quote']) not in {(row['clause_id'], row['quote']) for row in proof}:
                proof.append(source)
        return _rows(family, [('technical_service_remuneration', '技术服务报酬和费用安排', proof)])
    if family == 'service_quality':
        context = r'服务标准|服务质量|验收|服务成果|技术报告'
        specs = [
            ('objective_acceptance_standard', '服务质量和验收标准',
             find(r'(?:应|按照|依据)[^。；;]{0,25}(?:技术标准|设备运行目标)|验收(?:主要)?(?:检查|标准|依据|内容)[：:]', context=context, inherit_lists=True)),
            ('acceptance_process', '验收组织程序', find(PARTY + r'[^。；;]{0,45}(?:完成|进行|组织)验收', context=context)),
            ('acceptance_deadline', '验收期限', find(_DURATION + r'内[^。；;]{0,12}(?:完成|进行)?验收', context=context)),
            ('written_objection_mechanism', '验收书面异议程序', find(r'(?:应|须)[^。；;]{0,35}书面[^。；;]{0,20}(?:问题|异议|意见)', context=context)),
            ('rectification_mechanism', '验收不合格后的补充修正', find(r'(?:应|须)[^。；;]{0,50}(?:补充|修正|整改|补正)', context=context)),
            ('rectification_deadline', '补正期限', find(_DURATION + r'内[^。；;]{0,20}(?:补充|修正|整改|补正)', context=context)),
            ('reinspection_procedure', '补正后的复验程序', find(r'(?:应|须|可以|有权)[^。；;]{0,35}(?:复验|重新验收|再次验收)', context=context)),
            ('reinspection_deadline', '复验期限', find(_DURATION + r'内[^。；;]{0,20}(?:复验|重新验收|再次验收)', context=context)),
        ]
        return _rows(family, specs)
    if family == 'service_results':
        context = r'成果|知识产权|权利归|归属'
        specs = [
            ('service_result_scope', '服务中新成果的范围', find(r'(?:本项目|服务过程)[^。；;]{0,80}(?:形成|成果)[^。；;]{0,80}(?:报告|参数|工具|算法|记录)', context=context)),
            ('background_result_ownership', '背景成果和原有资料的权利归属', find(r'(?:履行本合同前|原有|既有)[^。；;]{0,110}(?:仍归|归[^。；;]{0,10}所有)', context=context)),
            ('project_result_ownership', '针对委托方形成的项目成果权属', find(r'(?:本项目|服务过程)[^。；;]{0,35}(?:特定|专用)[^。；;]{0,100}(?:所有权|知识产权|权利)[^。；;]{0,20}(?:归|属于)', context=context)),
            ('general_result_ownership', '可独立使用的通用成果权属', find(r'(?:通用工具|通用算法|通用成果)[^。；;]{0,35}(?:权利|知识产权)?归[^。；;]{0,10}所有', context=context)),
            ('service_result_use_boundary', '项目成果使用权限和边界', find(r'(?:报告|参数优化清单|测试记录|项目成果)[^。；;]{0,40}(?:有权|可以)[^。；;]{0,35}(?:内部|生产经营)[^。；;]{0,15}使用', context=context)),
        ]
        return _rows(family, specs)
    if family == 'material_exit':
        context = r'返还|删除|销毁|资料处置'
        dispose = find(r'(?:终止|解除|届满)[^。；;]{0,50}(?:有权要求|应|须)[^。；;]{0,30}(?:返还|删除|销毁)[^。；;]{0,60}(?:资料|数据|程序|信息)', context=context)
        deadlines = []
        if dispose:
            for clause in clauses:
                prior = [s for s in dispose if s['clause_id'] == clause.clause_id]
                if not prior:
                    continue
                for s in sources([clause], r'(?:应|须)[^。；;]{0,40}' + _DURATION + r'内(?:完成)?(?:处理|返还|删除|销毁)'):
                    # "处理" inherits the immediately governing disposal object,
                    # never a deadline in a different article or legal relation.
                    original = getattr(clause, 'raw_text', '') or clause.text
                    a, b = exact_span(original, prior[0]['quote']), exact_span(original, s['quote'])
                    if a and b and a[0] < b[0]:
                        deadlines.append(dict(s, quote=original[a[0]:b[1]]))
        specs = [
            ('termination_return_or_delete', '终止后的原始资料返还或删除', dispose),
            ('processing_deadline', '资料返还或删除处理期限', deadlines),
            ('retained_backup_use_restriction', '暂留备份继续保密且不得用于项目之外',
             find(r'备份[^。；;]{0,45}(?:应|须)[^。；;]{0,30}保密[^。；;]{0,25}不得[^。；;]{0,25}(?:项目之外|非履约|其他用途)', context=context)),
            ('confidential_copy_deletion', '复制件删除', find(r'(?:应|须)[^。；;]{0,30}(?:删除|销毁)[^。；;]{0,20}(?:复制件|副本)|(?:复制件|副本)[^。；;]{0,20}(?:应|须)[^。；;]{0,20}(?:删除|销毁)', context=context)),
            ('confidential_backup_deletion', '备份最终删除期限', find(r'备份[^。；;]{0,30}(?:应|须)[^。；;]{0,25}' + _DURATION + r'内[^。；;]{0,15}删除', context=context)),
            ('confidential_material_destruction', '资料销毁安排', find(r'(?:应|须)[^。；;]{0,20}销毁[^。；;]{0,20}(?:资料|数据|信息)', context=context)),
            ('confidential_disposal_confirmation', '资料处置书面确认', find(r'(?:应|须)[^。；;]{0,20}(?:出具|提供)[^。；;]{0,20}(?:书面确认|销毁证明|删除证明)', context=context)),
        ]
        return _rows(family, specs)
    if family == 'component_inventory':
        return _rows(family, [
            ('third_party_component_dependency', '第三方软件或组件使用安排', find(r'(?:可以|有权|可)[^。；;]{0,20}使用[^。；;]{0,40}(?:软件|组件|工具)|(?:如|若)(?:需|需要)使用[^。；;]{0,40}(?:第三方软件|开源组件|第三方技术)[^。；;]{0,35}(?:应|须)[^。；;]{0,15}(?:告知|通知|同意)', context=r'第三方|开源')),
            ('third_party_component_inventory', '第三方软件及开源组件清单', find(r'(?:提供|提交|附有)[^。；;]{0,45}(?:第三方软件|开源组件)[^。；;]{0,20}清单')),
            ('third_party_license_and_authorization', '第三方软件许可证或授权链材料', find(r'(?:提供|提交|附有)[^。；;]{0,35}(?:许可证|授权证明|授权链)')),
        ])
    if family == 'service_claims':
        from review_v2.technology_service_analysis import extract_claim_response_facts, analyze_technical_service_core_facts
        facts = analyze_technical_service_core_facts('\n'.join(c.text for c in clauses))
        liability = facts.get('liability', {})
        provider = re.escape(liability.get('service_provider_party') or '服务方')
        recipient = re.escape(liability.get('service_recipient_party') or '委托方')
        proof = extract_claim_response_facts(clauses, provider, recipient)
        mapping = [
            ('third_party_claim_trigger', 'claim_trigger', '第三方权利主张触发情形'),
            ('claim_handling_responsibility', 'claim_handling', '第三方索赔处理责任主体'),
            ('provider_infringement_liability', 'liability_responsible_party', '服务方对其侵权来源承担责任'),
            ('direct_damage', 'direct_damage', '第三方侵权直接损失责任'),
            ('defense_cost_allocation', 'claim_cost_allocation', '第三方索赔处理费用承担'),
            ('third_party_compensation', 'third_party_compensation_allocation', '第三方侵权赔偿责任'),
            ('notification_requirement', 'notification_requirement', '第三方索赔通知义务'),
            ('notification_deadline', 'notification_deadline', '第三方索赔通知期限'),
            ('necessary_assistance', 'claim_assistance', '第三方索赔必要协助'),
            ('termination_remedy', 'termination_remedy', '权利瑕疵无法修复后的解除救济'),
            ('refund_remedy', 'refund_remedy', '权利瑕疵后的退款救济'),
            ('defense_control', 'defense_control', '第三方索赔抗辩控制权'),
            ('lawyer_selection', 'lawyer_selection', '第三方索赔律师选择权'),
            ('settlement_authority', 'settlement_authority', '第三方索赔和解审批权限'),
            ('replacement_remedy', 'replacement_remedy', '替代技术或绕开侵权方案'),
            ('license_cure', 'license_cure', '取得第三方授权的修复机制'),
        ]
        from review_v2.technology_service_analysis import CLAIM_RESPONSE_ELEMENT_FACT_KEYS
        result = [_element(key, label, proof.get(canonical, []), source_fact_key=canonical)
                for key, source, label in mapping
                for canonical in [CLAIM_RESPONSE_ELEMENT_FACT_KEYS.get(key, source)]]
        control = next(e for e in result if e['element_id'] == 'defense_control')
        if not control['supporting_evidence'] and proof.get('claim_handling'):
            basic = proof['claim_handling']
            gap = '抗辩决策及当前审查方参与机制'
            control.update(_element('defense_control', control['required_fact'], basic,
                                    source_fact_key='claim_handling'))
            control.update(status='PARTIALLY_COVERED', source_fact_key='claim_handling',
                supporting_evidence=basic, residual_gap=gap, search_targets=[gap],
                proposition='；'.join(s['quote'] for s in basic) + '，形成基础处理主导安排，但' + gap + '仍未完整明确。',
                component_coverage=[dict(element_id='basic_claim_handling_control', status='COVERED',
                    required_fact='基础处理主导安排：' + '；'.join(s['quote'] for s in basic), supporting_evidence=basic),
                    dict(element_id='express_defense_decision_control', status='MISSING',
                         required_fact=gap, supporting_evidence=[])])
        return result
    raise ValueError(family)
