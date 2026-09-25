"""Brokerage requirements share one sentence-bound fact store, including composites.

Coverage is evaluated independently from the adverse arrangement scan. Neither
conversation templates nor report prose are admissible evidence sources.
"""
from copy import deepcopy
import re

from review_v2.lease_semantics import requirement as req, corpus_facts, evidence_identity, supports
from review_v2.brokerage_concepts import attach_concepts


def one(key, label, *patterns):
    return [req(key, label, *patterns)]


ACCEPT = req('broker_service_received', '接受中介服务或约定服务交付的证据形式',
    r'(?:接受|收到|确认).{0,25}(?:中介服务|客户信息|交易机会|客户名单)',
    r'(?:客户名单|微信记录|电子邮件|会议纪要).{0,100}(?:证明|认定).{0,35}(?:提供|履行).{0,15}(?:中介|交易机会|媒介)')
USE = req('broker_opportunity_used', '利用中介提供的订约机会或媒介服务',
    r'(?:委托人|甲方)(?:利用|使用).{0,25}(?:提供|介绍).{0,25}(?:机会|媒介服务)')
BYPASS = req('broker_bypass_contract', '绕开中介直接订立合同并支付报酬',
    r'(?:绕开|绕过).{0,20}(?:直接|自行).{0,25}(?:订立|签订).{0,15}合同.{0,40}(?:支付|给付).{0,10}报酬')
EXCLUSIVE = req('broker_exclusive_scope', '限制相同或相近服务的其他中介委托',
    r'(?:不得|不能|禁止).{0,20}委托其他中介.{0,30}(?:相同|相近|类似)',
    r'☒\s*否\s*可以委托其他中介.{0,30}(?:相同|相近|类似)',
    r'(?:本合同为|实行|采用).{0,8}(?:独家|排他).{0,25}(?:委托|中介).{0,40}(?:范围|事项|服务)')
PERIOD = req('broker_service_period', '中介服务的起止期限',
    r'服务期限[\s\S]{0,25}(?:自|从).{0,25}(?:至|到).{0,25}(?:止|日)',
    r'(?:中介|服务|委托)期限.{0,15}(?:\d+|[一二三四六十]+)个?月')

PROFILES = {
    'brokerage_contract_nature': one('broker_nature', '提供订约机会或媒介服务的中介关系', r'(?:报告|提供)订立合同的(?:机会|媒介服务)'),
    'broker_not_party_to_deal': one('broker_deal_parties', '交易由委托人与第三人订立', r'(?:促成甲方与|甲方.{0,30}与第三人).{0,30}(?:签订|订立).{0,20}合同'),
    'brokerage_not_agency_or_commission': one('broker_no_agency', '约定中介事务为报告订约机会或提供媒介服务', r'(?:报告|提供)订立合同的(?:机会|媒介服务)', r'(?:乙方|中介人).{0,15}(?:不代|无权代|不作为).{0,15}(?:签订|当事人)'),
    'oral_brokerage_evidence': one('broker_oral_proof', '口头中介约定的证明方式', r'(?:口头|口头约定).{0,50}(?:记录|录音|证明|证据)'),
    'report_brokerage_scope': one('broker_report_scope', '报告订约机会的服务内容', r'(?:报告订立合同的机会|提供.{0,15}客户信息)'),
    'media_brokerage_scope': one('broker_media_scope', '提供订约媒介服务', r'提供订立合同的媒介服务', r'(?:乙方|中介人).{0,25}(?:组织|协助).{0,15}(?:谈判|磋商|接洽)'),
    'service_period_and_area': [PERIOD, req('broker_service_area', '委托服务地域或业务范围', r'(?:全国|[\u4e00-\u9fff]{2,8}区域).{0,30}(?:代理|客户|渠道|中介)', r'服务(?:区域|范围).{0,30}[\u4e00-\u9fff]')],
    'service_record_attachment': one('broker_service_records', '服务履行材料的记录和证明', r'(?:客户名单|会议纪要|微信记录).{0,100}(?:证明|认定).{0,30}(?:履行|提供)'),
    'truthful_report_obligation': one('broker_truthful_report', '中介人向委托人如实报告订约事项', r'(?:乙方|中介人).{0,30}(?:应|须|有义务).{0,20}如实.{0,10}(?:报告|告知)', r'(?:应当|应|须)向(?:甲方|委托人)如实报告.{0,35}(?:订立合同|事项|情况)', r'(?:甲方|委托人).{0,20}有权要求(?:乙方|中介人).{0,25}如实告知.{0,35}(?:订立合同|有关信息|有关的?信息|情况)', r'(?:乙方|中介人).{0,35}(?:提供|告知|报告).{0,20}(?:完整、?准确、?真实|真实、?准确、?完整).{0,20}(?:信息|情况)'),
    'important_fact_disclosure': one('broker_material_disclosure', '订约重要事实的披露义务', r'(?:不得|禁止).{0,15}(?:隐瞒|提供虚假).{0,30}(?:重要事实|有关事项|情况)', r'(?:如实|披露|告知).{0,45}(?:重要事实|重要情况|履约能力|资信)', r'(?:完整、?准确、?真实|真实、?准确、?完整).{0,25}(?:信息|情况)', r'(?:故意隐瞒|隐瞒).{0,15}(?:重要事实|重要情况).{0,80}(?:不得请求|赔偿)', r'(?:故意隐瞒|提供虚假情况).{0,60}(?:不得请求|赔偿)'),
    'best_efforts_obligation': one('broker_diligence', '中介尽力促成交易的义务', r'(?:乙方|中介人).{0,20}(?:应|须|承诺).{0,20}(?:尽力|勤勉|积极).{0,30}(?:促成|服务|交易)'),
    'broker_confidentiality': one('broker_secrecy', '保密信息范围及保护要求', r'保密信息包括[\s\S]{0,180}(?:客户名单|交易条件|技术资料)', r'(?:双方|乙方|中介人).{0,30}(?:应|须|负有).{0,20}保密'),
    'principal_pay_remuneration': one('broker_principal_payment', '委托人支付中介报酬义务', r'甲方.{0,30}(?:按照|应当|应|向乙方).{0,40}支付中介报酬'),
    'principal_cooperation_obligation': one('broker_principal_cooperation', '委托人提供必要协助配合', r'(?:甲方|委托人).{0,25}(?:应|须|承诺).{0,25}(?:配合|协助|提供.{0,8}(?:资料|材料))', r'(?:甲方|委托人).{0,25}(?:应当|应|须).{0,20}(?:对|向|为)(?:乙方|中介人).{0,12}提供.{0,8}(?:必要|所需).{0,8}(?:协助|配合|便利)', r'(?:为乙方|为中介人).{0,20}提供.{0,15}(?:必要|所需).{0,10}(?:协助|配合|便利)'),
    'principal_information_accuracy': one('broker_principal_accuracy', '委托人提供的信息真实准确', r'(?:甲方|委托人).{0,40}(?:保证|确保|负责).{0,45}(?:真实|准确|合法)', r'(?:甲方|委托人).{0,15}(?:应当|必须|应|须).{0,25}(?:向|对)(?:乙方|中介人).{0,20}提供.{0,20}(?:真实|准确|合法).{0,12}(?:信息|资料|材料)', r'(?:甲方|委托人)提供.{0,25}(?:信息|资料|材料).{0,20}(?:应当|必须|应).{0,10}(?:真实|准确)'),
    'principal_no_obstruction': one('broker_no_obstruction', '委托人不得妨碍服务', r'(?:甲方|委托人).{0,20}(?:不得|不能).{0,15}(?:阻碍|妨碍|干扰)'),
    'remuneration_condition_concluded_contract': one('broker_commission_trigger', '促成交易与支付报酬的对应关系', r'促成.{0,60}(?:签订|成立|订立).{0,80}支付.{0,10}(?:中介)?报酬'),
    'remuneration_amount_method': one('broker_commission_amount', '报酬计价标准', r'(?:按照|按).{0,30}(?:金额|价款).{0,10}\d+(?:\.\d+)?%.{0,20}(?:报酬|佣金)', r'(?:中介报酬|佣金)(?:为|金额为).{0,12}\d+元'),
    'media_service_both_parties_bear': one('broker_commission_allocation', '媒介报酬由哪方承担的约定', r'甲方.{0,30}按照.{0,50}向乙方支付中介报酬', r'(?:双方|交易双方).{0,25}(?:承担|负担).{0,15}(?:报酬|佣金)'),
    'remuneration_unclear_fallback': one('broker_unclear_commission', '报酬不明确时的确定路径', r'报酬.{0,15}(?:不明确|未约定).{0,50}(?:补充|协商|交易习惯|合理)'),
    'accepted_service_evidence': [ACCEPT], 'used_opportunity_evidence': [USE],
    'bypass_remuneration_liability': [BYPASS], 'bypass_order_three_elements': [ACCEPT, USE, BYPASS],
    'nonexclusive_other_broker_exception': one('broker_other_source', '非独家情形可经其他中介成交', r'(?:非独家|可以委托其他中介).{0,100}(?:不承担|不需要|无需).{0,20}(?:报酬|违约)'),
    'original_broker_not_causal': one('broker_no_causation', '未利用中介服务时不支付报酬', r'未利用.{0,60}(?:机会|媒介服务).{0,40}(?:不需要|无需|不必).{0,15}支付报酬'),
    'policy_failure_no_remuneration': one('broker_policy_failure', '政策原因交易失败时的报酬处理', r'(?:政策|监管|审批|限购|贷款).{0,40}(?:无法|不能|未能).{0,40}(?:退还|不支付|不收取).{0,10}(?:报酬|佣金)'),
    'public_information_exception': one('broker_public_source', '公开或自行取得信息的排除', r'(?:公开信息|公开渠道|自行取得).{0,60}(?:不构成跳单|无需|不支付|不承担)'),
    'necessary_expense_when_no_contract': one('broker_failed_expense', '未促成合同的必要费用承担', r'未促成合同成立.{0,60}必要费用由.{0,20}负担'),
    'expense_scope_and_cap': [req('broker_expense_scope', '必要费用的范围', r'(?:交通费|差旅费|住宿费).{0,70}(?:必要费用|费用范围)'), req('broker_expense_cap', '费用限额或事先审批安排', r'(?:单笔费用|费用总额|费用上限).{0,50}(?:元|批准|同意)', r'(?:费用|支出).{0,25}(?:经|取得).{0,15}书面同意')],
    'broker_activity_expense_burden': one('broker_success_expense', '促成合同的中介活动费用承担', r'促成合同成立.{0,30}费用应当由乙方负担'),
    'expense_evidence': one('broker_expense_proof', '必要费用按实际支出凭证结算', r'(?:实际支出|费用|报销).{0,8}(?:凭证|票据|发票).{0,20}(?:支付|结算|核验)', r'(?:提供|提交).{0,20}(?:费用|支出|报销).{0,8}(?:凭证|票据|发票)'),
    'truthful_report_breach_consequence': [req('broker_dishonesty_no_commission', '隐瞒或虚假报告的报酬后果', r'(?:隐瞒|虚假情况).{0,80}(?:不得请求|不应支付|无权收取|退还).{0,18}(?:报酬|服务费用|中介费用|佣金)'), req('broker_dishonesty_damages', '隐瞒或虚假报告的损失赔偿', r'(?:隐瞒|虚假情况).{0,120}(?:赔偿|损害赔偿|承担.{0,10}损失赔偿)')],
    'staff_scope_act_liability': one('broker_staff_liability', '工作人员职务行为归责', r'(?:工作人员|员工|雇员).{0,50}(?:行为|职务).{0,50}(?:乙方|中介人).{0,20}承担'),
    'principal_wrong_info_allocation': one('broker_wrong_info_liability', '委托人错误信息造成损失的责任', r'(?:甲方|委托人).{0,30}(?:虚假|错误|不实).{0,50}(?:赔偿|承担)'),
    'broker_liability_limit': one('broker_liability_boundary', '中介不对第三人履约提供保证的边界', r'(?:乙方|中介人).{0,25}(?:不保证|不担保|不承担).{0,30}(?:履约|第三人|第三方)'),
    'exclusive_entrustment_clause': [EXCLUSIVE, PERIOD],
    'exclusive_bypass_consequence': one('broker_exclusive_consequence', '违反独家约定的责任', r'违反.{0,30}独家.{0,90}(?:支付|承担).{0,25}违约金'),
    'exclusive_service_standard': one('broker_exclusive_standard', '独家服务投入及报告频率', r'(?:每周|每月|定期).{0,40}(?:报告|汇报|提交).{0,30}(?:工作|服务|进展)'),
    'exclusive_termination': one('broker_exclusive_exit', '独家委托提前退出程序', r'甲方提前终止本合同.{0,40}(?:通知|违约|结算)'),
    'unreasonable_standard_clause': one('broker_standard_adverse', '明确排除主要权利或免责的格式安排', r'(?:乙方|中介人).{0,20}(?:无论任何原因|任何情况下).{0,20}(?:不承担|免责)', r'(?:甲方|委托人).{0,20}放弃.{0,15}(?:全部|所有).{0,10}(?:权利|异议)'),
    'burden_of_proof_rule': [req('broker_proof_materials', '可用于证明中介服务的证据材料', r'(?:客户名单|微信记录|电子邮件|会议纪要).{0,100}(?:证明|认定|依据)'), req('broker_proof_burden', '对报酬条件或跳单事实的举证责任分配', r'(?:乙方|中介人).{0,30}(?:承担举证责任|负责举证|应当证明).{0,40}(?:提供|利用|交易|服务|跳单)')],
    'post_contract_obligation': one('broker_post_contract', '合同终止后的持续义务', r'合同终止后.{0,15}(?:年|月|保密)', r'不因本合同终止而免除.{0,30}支付中介报酬'),
    'termination_reference_mandate': one('broker_termination', '委托终止及通知程序', r'甲方提前终止本合同.{0,40}(?:通知|违约|结算)'),
}


# Reusable grammatical units, bounded to the same sentence. These describe
# obligations and charging consequences rather than any fixture's wording.
REMUNERATION = r'(?:中介|居间|服务)?(?:报酬|佣金|费用|费)'
SENTENCE_GAP = r'[^。；;\n]{0,180}'
OBLIGATION = r'(?:应当|必须|须|应|负责)'
DUTY_GAP = r'(?:(?!乙方(?:应|须|负责|提供)|通知乙方|要求乙方|无需|无须|不必|不提供)[^。；;\n]){0,180}'


def requirements(text):
    """Resolve role aliases from the contract, never assume the alphabetic side."""
    profiles = deepcopy(PROFILES)
    attach_concepts(profiles)
    cooperation = profiles['principal_cooperation_obligation'][0]
    cooperation['semantic_patterns'] = (*cooperation['semantic_patterns'],
        rf'(?:甲方|委托人){OBLIGATION}{DUTY_GAP}提供{DUTY_GAP}(?:资料|信息|协助|配合)',
        rf'(?:甲方|委托人)不得(?:无故)?(?:拒绝|拖延|拒绝、拖延){SENTENCE_GAP}(?:协助|配合)')
    consequence = profiles['truthful_report_breach_consequence'][0]
    consequence['excluded_patterns'] = [r'(?:无需|无须|不必|不应|不得).{0,8}(?:退还|返还)',
                                        r'(?:仍有权|仍可|可以).{0,8}(?:请求|收取).{0,12}(?:报酬|佣金|中介费)']
    consequence['semantic_patterns'] = (*consequence['semantic_patterns'],
        rf'(?:隐瞒|虚假情况){SENTENCE_GAP}(?:无权|不得|不能)(?:请求|要求|收取){SENTENCE_GAP}{REMUNERATION}',
        rf'(?:隐瞒|虚假情况)[^。\n]{{0,240}}(?:已收取|已经收取|已支付|已经支付)(?:的)?{REMUNERATION}[^。\n]{{0,80}}(?:退还|返还)')
    period = profiles['service_period_and_area'][0]
    period['semantic_patterns'] = (*period['semantic_patterns'],
        r'(?:本合同|本协议|服务|委托)(?:有效期|期限)?自[^。；\n]{0,35}日起\d+个月内有效')
    amount = profiles['remuneration_amount_method'][0]
    amount['semantic_patterns'] = (*amount['semantic_patterns'],
        rf'(?:按照|按)[^。；\n]{{0,40}}(?:总金额|金额|价款)(?:的)?\s*\d+(?:\.\d+)?\s*[%％][^。；\n]{{0,20}}(?:支付|给付){REMUNERATION}',
        rf'(?:按照|按)[^。；\n]{{0,40}}(?:总金额|金额|价款)(?:的)?\s*\d+(?:\.\d+)?\s*[%％][^。；\n]{{0,20}}向(?:乙方|中介人)支付{REMUNERATION}')
    implicit = {
        'truthful_report_obligation': ('乙方', r'(?:应当|应|须).{0,25}(?:如实.{0,10}(?:报告|告知)|提供.{0,15}(?:完整、?准确、?真实|真实、?准确、?完整).{0,12}(?:信息|情况))'),
        'principal_information_accuracy': ('甲方', r'(?:保证|确保).{0,30}(?:资料|信息|材料).{0,15}(?:真实|准确|合法)'),
        'principal_cooperation_obligation': ('甲方', r'(?:应当|应|须).{0,25}(?:提供必要.{0,5}协助|配合|协助)'),
    }
    for node, (role, pattern) in implicit.items():
        profiles[node][0]['contextual_patterns'] = [{'context': role + r'.{0,8}(?:权利|义务|责任)', 'predicate': pattern}]
        profiles[node][0]['excluded_patterns'] = [r'(?:无须|无需|不必|不应|不承担).{0,8}(?:如实|保证|确保|配合|协助|披露)']
    principal = re.search(r'([甲乙丙丁]方)[（(](?:委托人|委托方)[）)]', text)
    broker = re.search(r'([甲乙丙丁]方)[（(](?:中介人|居间人|中介方)[）)]', text)
    aliases = {'甲方': principal[1] if principal else '委托人', '乙方': broker[1] if broker else '中介人'}
    for elements in profiles.values():
        for e in elements:
            e['semantic_patterns'] = [re.sub('甲方|乙方', lambda m: aliases[m[0]], p) for p in e['semantic_patterns']]
            e['excluded_patterns'] = [re.sub('甲方|乙方', lambda m: aliases[m[0]], p) for p in e.get('excluded_patterns', [])]
            for p in e.get('contextual_patterns', []):
                p['context'] = re.sub('甲方|乙方', lambda m: aliases[m[0]], p['context'])
    return profiles


def apply(items, clauses, text):
    from review_v2.engine import _set_item_not_applicable
    from review_v2.brokerage_adverse import scan, bind
    profiles = requirements(text)
    facts = corpus_facts(clauses, [e for values in profiles.values() for e in values])
    scan_result = scan(clauses)
    exclusive_triggered = bool(facts['broker_exclusive_scope'])
    nonexclusive_triggered = bool(re.search(r'(?:☒\s*是\s*可以委托其他中介|非独家|非排他|可以委托其他中介)', text))
    policy_dependent = bool(re.search(r'(?:限购|贷款政策|房贷|按揭|监管审批|行政审批|政策准入|许可审批|备案审批|外汇审批|资质审批)', text))
    for item in items:
        specs = profiles[item.node_id]
        # Consumers, including the composite, bind the very same canonical rows.
        evidence = [evidence_identity(row) for spec in specs for row in facts[spec['element_id']]]
        missing = [s['proposition'] for s in specs if not facts[s['element_id']]]
        trace = item.decision_trace
        trace['semantic_requirements'] = specs
        # Retain the production search proof for concept-backed requirements,
        # including positive matches (absence-only audits cannot explain reuse).
        if any(s.get('semantic_concepts') for s in specs):
            from review_v2.engine import _search_final_element
            trace['concept_search_audits'] = [
                _search_final_element(item, s, clauses) for s in specs]
        trace['brokerage_canonical_coverage'] = {'required_elements': deepcopy(specs), 'missing': missing,
            'evidence': deepcopy(evidence), 'status': 'PARTIAL' if evidence and missing else 'MISSING' if missing else 'PASS'}
        trace['adverse_clause_scan'] = deepcopy(scan_result)
        trace.pop('element_evidence_truth', None)
        item.evidence_clauses = evidence
        item.evidence_location = '；'.join(dict.fromkeys(r['location'] for r in evidence))
        item.coverage_status = '部分覆盖' if evidence and missing else '缺失' if missing else '通过'
        item.status = item.coverage_status
        item.issue_type = {'通过': '通过', '缺失': '完全缺失', '部分覆盖': '条款缺陷'}[item.coverage_status]
        item.risk_level = '低' if not missing else item.risk_level
        item.reasoning_summary = item.risk_point_description = ('尚未找到：' + '、'.join(missing) + '。' if missing else '原文明确约定：' + '、'.join(s['proposition'] for s in specs) + '。')
        item.judge_source = 'rule_fallback'
        item.fallback_reason = '完整正文共享事实核验'
        item.needs_manual_review = False
        if item.node_id == 'bypass_order_three_elements':
            trace['composite_dependencies'] = ['accepted_service_evidence', 'used_opportunity_evidence', 'bypass_remuneration_liability']
        condition = None
        if item.node_id == 'oral_brokerage_evidence':
            condition = ('涉及口头中介约定时适用', bool(re.search(r'口头(?:中介|约定|合同)', text)))
        elif item.node_id == 'remuneration_unclear_fallback':
            condition = ('报酬计价标准未明确时适用', not facts['broker_commission_amount'])
        elif item.node_id.startswith('exclusive_'):
            condition = ('存在独家或排他中介约定时适用', bool(facts['broker_exclusive_scope']))
        elif item.node_id == 'nonexclusive_other_broker_exception':
            condition = ('非独家或允许另行委托其他中介时适用', bool(nonexclusive_triggered and not exclusive_triggered))
        elif item.node_id == 'policy_failure_no_remuneration':
            condition = ('交易存在政策准入、审批、贷款、限购等外部政策依赖时适用', policy_dependent)
        if condition:
            item.applicable_if = condition[0]
            if not condition[1]:
                _set_item_not_applicable(item, condition[0] + '；本合同未触发。')
            item.applicability.update(condition=condition[0], triggered=bool(condition[1]))
        if item.node_id == 'unreasonable_standard_clause':
            trace['negative_check_basis'] = {'method': 'CANONICAL_ADVERSE_REQUIREMENT_SEARCH'}
            trace['review_mode'] = 'ABSENCE_REQUIRED'
            trace['review_polarity'] = 'NEGATIVE_CLAUSE_CHECK'
            if not evidence:
                trace.pop('semantic_requirements', None)
                item.coverage_status = item.status = '通过'
                item.issue_type = '通过'
                item.risk_level = '低'
                item.reasoning_summary = item.risk_point_description = '合同文本未发现本项明确免责或权利排除安排；不代表所有条款均无不利内容。'
            else:
                item.coverage_status = item.status = item.issue_type = '风险条款'
        bind(item, scan_result)
    return items


def consistency_failures(items):
    failures = []
    scoped = {i.node_id: i for i in items if 'brokerage_canonical_coverage' in i.decision_trace}
    for item in scoped.values():
        def fail(name):
            failures.append(dict(requirement=name, root_cause=item.item_id, current_status='FAIL', failure_stage='Brokerage canonical facts'))
        coverage = item.decision_trace['brokerage_canonical_coverage']
        if coverage['evidence'] and item.coverage_status == '缺失':
            fail('POSITIVE_FACT_REPORTED_MISSING')
        if item.coverage_status in {'通过', '部分覆盖', '风险条款'}:
            specs = item.decision_trace.get('semantic_requirements', [])
            for row in item.evidence_clauses:
                if not any(supports(s, row) for s in specs):
                    fail('PASS_EVIDENCE_NOT_ENTAILED')
            if item.evidence_location != '；'.join(dict.fromkeys(r['location'] for r in item.evidence_clauses)):
                fail('CANONICAL_LOCATION_MISMATCH')
        scan_result = item.decision_trace.get('adverse_clause_scan', {})
        if scan_result.get('status') != 'COMPLETE':
            fail('ADVERSE_SCAN_REQUIRED')
        if any(f['node_id'] == item.node_id for f in scan_result.get('findings', [])) and item.coverage_status != '风险条款':
            fail('ADVERSE_FACT_LOST')
        deps = item.decision_trace.get('composite_dependencies', [])
        if deps and all(scoped[n].decision_trace['brokerage_canonical_coverage']['status'] == 'PASS' for n in deps) and item.coverage_status == '缺失':
            fail('COMPOSITE_CHILD_CONFLICT')
    return failures
