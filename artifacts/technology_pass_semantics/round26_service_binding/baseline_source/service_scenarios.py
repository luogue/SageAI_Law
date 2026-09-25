"""Service scenario predicates and domain-neutral service evidence."""
import re

def is_property_service(text):
    """Identify the service object and obligor, not a province or sample title."""
    return bool(re.search(r'物业服务人|物业服务企业|物业管理公司', text)
                and re.search(r'业主|物业服务区域|共用部位|共用设施', text)
                and re.search(r'物业服务费|物业管理费|提供[^。\n]{0,20}物业服务', text))

def project_checklist(checklist, text):
    """Project authorities and duplicate document checks before evaluation."""
    from dataclasses import replace
    scenario=resolve(text)
    if scenario['values']['consumer']:
        return checklist
    has_primary=any(r.node_id=='provider_qualification_attachment' for r in checklist)
    result=[]
    for rule in checklist:
        if scenario['subtype']=='PROPERTY_SERVICE' and rule.node_id=='indefinite_service_termination':
            rule=replace(rule,legal_basis='《中华人民共和国民法典》第948条')
        if has_primary and rule.node_id=='qualification_attachment':
            continue
        basis=re.sub(r'《(?:中华人民共和国)?消费者权益保护法》[^《；;\n]*', '',rule.legal_basis).strip('、，,；; ')
        basis=re.sub(r'预付式消费司法解释[^《；;\n]*','',basis).strip('、，,；; ')
        result.append(replace(rule,legal_basis=basis))
    return tuple(result)

CONDITIONS = {
    'SVC-02-02':'qualified_staff',
    'SVC-02-03':'qualification_documents',
    'SVC-12-03':'qualification_documents',
    'SVC-03-04':'training',
    **{f'SVC-04-0{i}':'prepaid_consumer' for i in range(1,5)},
    'SVC-05-03':'consumer', 'SVC-06-01':'consumer','SVC-06-02':'consumer',
    'SVC-07-03':'platform', 'SVC-06-04':'indefinite',
    'SVC-08-03':'prepaid_consumer','SVC-08-04':'prepaid_consumer',
    **{f'SVC-09-0{i}':'consumer' for i in range(1,5)},
    **{f'SVC-10-0{i}':'prepaid_consumer' for i in range(1,5)},
    'SVC-11-02':'prepaid_consumer','SVC-11-03':'consumer',
}


def resolve(text):
    # Read the customer identity, not a quoted statute or supplier's company name.
    customer = re.findall(r'(?:甲方|服务接受方|客户|学员|会员)[（(]?[^\n：:]{0,15}[:：]([^\n。]{1,100})',text)
    personal_customer = bool(re.search(r'学员姓名[:：]|会员姓名[:：]|接受培训方监护人|个人生活消费',text))
    enterprise = not personal_customer and any(re.search(r'公司|企业|集团|银行|事务所|学校',c) for c in customer)
    enterprise = enterprise or bool(re.search(r'双方均为企业|企业(?:购买|委托)|办公保洁|办公区域.{0,30}保洁',text))
    training = bool(re.search(r'(?:提供|购买|报名|参加).{0,30}(?:培训课程|教育培训|课时包|教学课程)|(?:总课时|课程名称|教师授课|开课日期)[:：\s]|(?:\d+|[一二三四五六七八九十]+)课时',text))
    personal = bool(re.search(r'个人生活消费|个人(?:购买|办理|报名)|居民个人|身份证(?:号|号码)|学员姓名|会员姓名|乙方为学员|接受培训方监护人',text))
    consumer = bool(not enterprise and personal)
    prepaid = bool(re.search(r'预付|储值|会员(?:年|月)?卡|年卡|课时包|套餐余额|按次消费|未消耗课时|剩余课时|开课前[^。\n]{0,40}(?:支付|缴纳)|(?:一次性|分期)[^。\n]{0,15}(?:支付|缴纳)[^。\n]{0,20}(?:培训|课程)',text))
    values = dict(consumer=consumer,prepaid_consumer=consumer and prepaid,training=training,
                  platform=bool(re.search(r'互联网平台|平台服务条款|平台(?:购买|交易|下单)|通过[^。\n]{0,20}平台',text)),
                  indefinite=bool(re.search(r'不定期服务|无固定(?:服务)?期限|期限[^。\n]{0,12}(?:转为|成为|变更为)不定期|不定期[^。\n]{0,8}(?:合同|继续履行)',text)))
    subtype = 'TRAINING_EDUCATION_SERVICE' if training else 'PREPAID_CONSUMER_SERVICE' if values['prepaid_consumer'] else 'CONSUMER_SERVICE' if consumer else 'GENERAL_B2B_SERVICE' if enterprise else 'GENERAL_SERVICE'
    if is_property_service(text):
        subtype = 'PROPERTY_SERVICE'
    return dict(subtype=subtype,values=values,customer_identity=customer,
                rationale='企业业务用途不属于个人生活消费；引用消费者法或单纯提前付款不构成消费者身份。',
                enterprise_customer=enterprise)


def extract_facts(clauses):
    text='\n'.join(c.text for c in clauses)
    scenario=resolve(text)
    scenario['values'].update(qualification_conditions(text))
    labels={'qualified_staff':'存在法定或合同约定的人员执业资格要求',
            'qualification_documents':'存在明确的资质证明材料提供要求',
            'consumer':'已确认消费者个人生活消费','prepaid_consumer':'已确认消费者身份及预付消费',
            'training':'已确认课程教学服务','platform':'存在互联网平台交易','indefinite':'存在不定期继续性服务'}
    facts = {key:dict(value=value,label=labels[key],scenario=scenario,
                     searched_clause_ids=[c.clause_id for c in clauses]) for key,value in scenario['values'].items()}
    from review_v2.utility_supply_evidence import _find_supports
    _, rows = _find_supports(clauses, 'indefinite_applicability', PROFILES['indefinite_service_termination'][:1])
    facts['indefinite']['evidence'] = rows
    facts['indefinite']['requires_direct_evidence'] = True
    return facts


def qualification_conditions(text):
    special = bool(re.search(r'高(?:空|处)(?:作业|外墙|清洗)|特种(?:作业|设备操作)|(?:提供|从事|承担)[^。\n]{0,20}(?:医疗|诊疗|安保|消防设施维护|律师|审计)服务|律师事务所|注册会计师|执业医师', text))
    promised = bool(re.search(r'(?:人员|工作人员|医师|律师|会计师)[^。\n]{0,35}(?:必须|须|应)[^。\n]{0,20}(?:持有|取得|具备)[^。\n]{0,20}(?:资格证|执业证|职称|操作证)', text))
    documents = bool(re.search(r'(?:提供|提交|附具)[^。\n]{0,25}(?:资质证明|资格证|营业执照|许可证)|(?:资质证明|资格证|营业执照|许可证)[^。\n]{0,20}(?:作为附件|详见附件)',text))
    return dict(qualified_staff=special or promised, qualification_documents=documents)


PROFILES = {
 'service_contract_type_identification': [
    ('service_performance_object','持续或阶段性服务履行对象',r'(?:提供|服务内容[:：]?)[^。；\n]{0,40}(?:保洁|清洁|维护|咨询|运维)|(?:共用部位|共用设施设备|公共区域)[^。；\n]{0,35}(?:维护|管理|清洁|巡查)'),
    ('service_consideration','服务费用或计费安排',r'(?:服务费|服务费用|物业公共服务费|物业费)[^。\n]{0,50}(?:元|标准|支付|包干)')],
 'service_contract_vs_work_contract': [('service_process','约定服务行为而非仅交付制作成果',r'(?:每日|每月|日常|定期)[^。；\n]{0,35}(?:清扫|清洁|维护|巡检|服务)|(?:客服|报修)[^。；\n]{0,25}(?:响应|服务)')],
 'service_contract_vs_agency_contract': [('service_performance','实际承担约定的服务履行',r'(?:提供|承担|履行)[^。；\n]{0,30}(?:物业服务|保洁服务|清洁服务|维护服务)|(?:共用部位|公共区域)[^。；\n]{0,30}(?:维护|清洁)')],
 'service_contract_subtype': [('service_kind','具体服务对象或业务类型',r'物业服务人|物业服务区域|办公保洁|IT运维|健身服务|摄影服务|咨询服务|美容服务')],
 'provider_legal_qualification': [('provider_document_commitment','服务方证照公示、提供或资格承诺',r'(?:乙方|服务提供方|服务方)[^。；\n]{0,30}(?:公示|提供|出示|具备|持有)[^。；\n]{0,20}(?:营业执照|经营许可证|执业资格)')],
 'provider_change_requires_consent': [('change_agreement','既有合同或服务变更须经双方同意',r'(?:合同|服务)[^。；\n]{0,25}(?:变更|修改|调整)[^。；\n]{0,25}(?:应|须|必须|需经)[^。；\n]{0,20}(?:双方[^。；\n]{0,10}(?:同意|协商一致)|服务接受方[^。；\n]{0,10}同意)|(?:经双方协商一致|经双方同意)[^。；\n]{0,12}(?:方可|可以)[^。；\n]{0,12}(?:变更|修改|调整)(?:本合同|服务)')],
 'change_record_and_confirmation': [('written_change','既有合同或服务变更的书面确认要求',r'(?:合同|服务)[^。；\n]{0,20}(?:变更|修改|调整)[^。；\n]{0,20}(?:应|须|必须)[^。；\n]{0,25}(?:书面确认|书面形式|签署[^。；\n]{0,8}变更协议|签字确认)|双方(?:应|须)[^。；\n]{0,15}(?:书面|邮件|短信)[^。；\n]{0,10}确认[^。；\n]{0,10}(?:合同|服务)变更')],
 'service_nonperformance_remedy': [
    ('nonperformance_cure','未履行服务时的补救义务',r'(?:未提供|未履行|不能提供)[^。；\n]{0,65}(?:补救|重新履行|整改|退还)'),
    ('nonperformance_liability','未履行合同义务的损失责任',r'(?:违反本合同|未(?:按[^。；\n]{0,15})?履行)[^。；\n]{0,90}(?:赔偿|损失[^。；\n]{0,20}承担|承担[^。；]{0,15}(?:损失|责任))')],
 'service_quality_nonconform_remedy': [
    ('quality_cure','服务不符合标准时的整改补救',r'(?:质量|服务)[^。；\n]{0,30}(?:不符合|不达标)[^。；\n]{0,40}(?:整改|补救|重新)'),
    ('failed_cure_remedy','整改仍不达标时的后续救济',r'(?:整改|补救|重新履行|书面催告)[^。；\n]{0,30}(?:仍|不能)[^。；\n]{0,50}(?:解除|减价|减少费用|退还)')],
 'provider_qualification_attachment': [('qualification_entity','实际资质证明附件',r'附件[一二三四五六七八九十\d]*[:：、\s]+[^。；\n]{0,25}(?:营业执照|资质证明|许可证)')],
 'service_content_standard': [
    ('service_content','具体服务事项',r'(?:提供|服务内容[:：]?)[^。；\n]{0,35}(?:保洁|清洁|垃圾清运|消毒|运维|维护|巡检|技术支持|咨询|健身|摄影|设计|管理服务)(?!所需)'),
    ('service_frequency','服务频次或周期',r'(?:每日|每天|每周|每月|每季度|每年)[^。；\n]{0,20}(?:清洁|保洁|消毒|清运|巡检|维护|运维)(?:[^。；\n]{0,12}[一二三四五六七八九十\d]+次)?')],
 'service_quality_standard': [
    ('service_quality_standard','可识别服务质量标准',r'(?:地面|桌面|卫生间|公共设施)[^。；\n]{0,20}无(?:明显)?(?:污渍|异味|灰尘|垃圾)|(?:服务|技术|产品)[^。；\n]{0,25}(?:符合|达到)[^。；\n]{0,25}标准|可用率[^。；\n]{0,10}\d'),
    ('service_operating_requirements','服务操作要求',r'(?:工作人员|服务人员|操作流程)[^。；\n]{0,90}(?:应|不得|遵守)|(?:不得擅自|须经).{0,25}(?:资料|设备|进入)')],
 'service_schedule_and_place': [
    ('service_time','具体服务操作时间',r'(?:每日|每天|每周)[^。；\n]{0,20}\d{1,2}[:：时]\d{0,2}'),
    ('service_period','服务起止日期',r'自\d{4}年\d{1,2}月\d{1,2}日起?至\d{4}年\d{1,2}月\d{1,2}日'),
    ('service_location','服务地点',r'(?:服务地点|办公区域|办公楼|坐落位置)[^。；]{0,120}(?:市|路|号|层)')],
 'termination_basis': [('termination_trigger','合同解除权及触发条件',r'(?:有权|可以|可|得)[^。；\n]{0,12}解除(?:本)?合同|合同[^。；\n]{0,15}(?:解除条件|可解除)|(?:严重违约|无法履行)[^。；\n]{0,35}解除')],
 'force_majeure_service_adjustment': [
    ('force_majeure_event','不可抗力事由',r'不可抗力[^。；\n]{0,40}(?:不能预见|自然灾害|政府行为|导致|造成)|不能预见、?不能避免[^。；\n]{0,20}不能克服'),
    ('force_majeure_relief','服务不能履行时的免责范围说明',r'不可抗力[^。；\n]{0,100}(?:不承担|免责|不视为[^。；]{0,10}违约)|(?:出现|发生)下列情形[^。；\n]{0,25}不承担责任'),
    ('force_majeure_notice','不可抗力通知',r'不可抗力[^。；\n]{0,70}(?:应|须)[^。；\n]{0,20}通知'),
    ('force_majeure_proof','不可抗力证明',r'不可抗力[^。；\n]{0,70}(?:提供|提交)[^。；\n]{0,20}证明'),
    ('force_majeure_adjustment','不可抗力延期、替代履行或结算机制',r'不可抗力[^。；\n]{0,100}(?:延期|替代服务|结算|退还)')],
 'prepaid_refund_condition_process': [
    ('refund_condition','退费触发条件',r'(?:解除|终止|未提供|未消费)[^。；\n]{0,40}(?:退款|退费|退还)'),
    ('refund_process','退费办理流程或期限',r'(?:退费|退款)[^。；\n]{0,45}(?:申请|工作日|日内)|(?:申请|日内)[^。；\n]{0,30}(?:退款|退费)')],
 'fee_standard_attachment': [('fee_attachment','实际收费标准附件',r'附件[一二三四五六七八九十\d]*[:：、\s]+[^。；\n]{0,20}(?:收费标准|价格表|费用明细)')],
 'service_item_attachment': [('service_attachment','实际服务项目清单附件',r'附件[一二三四五六七八九十\d]*[:：、\s]+[^。；\n]{0,20}(?:服务项目|服务清单)')],
 'performance_record_attachment': [('service_record','服务记录及确认',r'(?:做好|保存|提供)[^。；\n]{0,20}服务记录|服务记录[^。；\n]{0,25}(?:确认|依据)')],
}
FEE_FACTS = [
 ('service_fee_total','服务费用总额',r'服务费(?:用)?(?:总计|合计|总额)?(?:为)?(?:人民币)?\s*[\d,，]+(?:\.\d+)?元'),
 ('service_monthly_fee','每月服务费用',r'每月服务费(?:用)?(?:为)?(?:人民币)?\s*[\d,，]+元'),
 ('payment_cycle','付款周期',r'按月支付|按季支付|按年支付'),
]

# A populated unit price is a pricing method, not an empty total-price field.
UNIT_PRICE = r'\d+(?:\.\d+)?\s*元\s*[/／每]\s*(?:月|季|年|日)\s*[·•/／每]\s*(?:平方米|平米|个|位|次|人|台)'
SCOPE_ITEM = r'(?:房屋共用部位|共用设施设备|公共区域|公共绿化|停车秩序|装饰装修|物业档案|公共秩序|生活垃圾)[^。；\n]{0,45}(?:维护|管理|清洁|养护|收集|巡查|处理)'
QUANTIFIED_SERVICE = r'(?:客服|值守|清扫|垃圾|电梯|消防|报修|清洁|维护|维保)[^。；\n]{0,45}(?:\d+\s*(?:小时|分钟|日|次)|\d{1,2}[:：]\d{2}|日产日清)|(?:每日|每周|每月|每\d+日)[^。；\n]{0,35}(?:清扫|清洁|维保|维护|巡检|保养)|\d+小时[^。；\n]{0,8}值守'
PROFILES['service_content_standard'][0] = ('service_content','具体服务事项', r'^(?![\s\S]*(?:主要用于|费用承担|清运费))(?=[\s\S]*(?:'+PROFILES['service_content_standard'][0][2]+'|'+SCOPE_ITEM+r'))[\s\S]+')
PROFILES['service_content_standard'][1] = ('service_frequency','服务频次或周期', PROFILES['service_content_standard'][1][2]+'|'+QUANTIFIED_SERVICE)
PROFILES['service_quality_standard'][0] = ('service_quality_standard','可识别服务质量标准', PROFILES['service_quality_standard'][0][2]+'|'+QUANTIFIED_SERVICE)
PROFILES['service_quality_standard'][1] = ('service_operating_requirements','服务操作要求', PROFILES['service_quality_standard'][1][2]+'|'+QUANTIFIED_SERVICE)
PROFILES['indefinite_service_termination'] = [
 ('indefinite_continuation','期满后不定期继续履行安排',r'期限[^。\n]{0,12}(?:转为|成为|变更为)不定期|不定期服务|无固定(?:服务)?期限'),
 ('termination_notice','不定期阶段解除的通知安排',r'(?:不定期|无固定期限)[^。\n]{0,80}(?:提前[^。\n]{0,30}通知[^。\n]{0,25}解除|解除[^。\n]{0,40}提前[^。\n]{0,25}通知)'),
]

def profiles_for(clauses):
    """Bind remedies to the identified provider, not a fixed party letter."""
    text='\n'.join(c.text for c in clauses)
    providers=set(re.findall(r'([甲乙丙丁]方)[（(](?:物业服务人|服务提供方|服务方|承接方)[）)]',text))
    providers.update(re.findall(r'([甲乙丙丁]方)(?:应|负责|为[^。\n]{0,25})?提供[^。\n]{0,12}(?:物业|保洁|运维|咨询)服务',text))
    provider='(?:服务提供方|服务方|物业服务人'+''.join('|'+re.escape(p) for p in sorted(providers))+')'
    recipients={'甲方','乙方'}-providers if len(providers)==1 else set()
    recipient='(?:服务接受方|委托方'+''.join('|'+re.escape(p) for p in sorted(recipients))+')'
    quality=provider+r'[^。；\n]{0,65}(?:不符合|不达标)[^。；\n]{0,20}(?:服务|质量|标准)'
    result=dict(PROFILES)
    result['service_quality_nonconform_remedy']=[
        ('quality_cure','服务方质量不符合约定时向服务接受方整改补救',quality+r'[^。；\n]{0,35}(?:应|须)[^。；\n]{0,15}(?:整改|补救|重新履行)'),
        ('failed_cure_remedy','服务方质量经催告仍不达标时服务接受方的后续救济',provider+r'[^。；\n]{0,35}(?:整改|补救|书面催告)[^。；\n]{0,20}仍[^。；\n]{0,15}(?:不符合|不达标)[^。；\n]{0,20}(?:服务|质量|标准)[^。；\n]{0,10}'+recipient+r'[^。；\n]{0,12}(?:有权|可以|可)(?:解除|要求减价|减少费用|要求退还)')]
    return result

PROPERTY_INDEFINITE_LAW = '《中华人民共和国民法典》第948条'
PROPERTY_INDEFINITE_NOTICE = '不定期物业服务合同任何一方均可随时解除，但应提前60日书面通知对方；合同未复述不影响该法定通知规则适用。'
PROPERTY_INDEFINITE_ACTION = '明确约定不定期阶段任何一方解除合同应提前60日书面通知对方'

def apply_property_indefinite_law(item, clauses):
    """Keep the special legal rule separate from contractual coverage facts."""
    if item.node_id!='indefinite_service_termination':
        return
    if item.decision_trace.get('service_scenario',{}).get('subtype')!='PROPERTY_SERVICE':
        return
    item.legal_basis_index=PROPERTY_INDEFINITE_LAW
    item.decision_trace['applicable_legal_proposition']={
        'proposition':PROPERTY_INDEFINITE_NOTICE,'claim_type':'PROCEDURE',
        'references':[{'law_name':'中华人民共和国民法典','article':'第948条','paragraph':''}]}
    # General early-exit clauses are not evidence of this phase-specific rule.
    from review_v2.parameter_validation import extract_parameters
    from review_v2.utility_supply_evidence import _set_adverse_if_found
    conflicts=[]
    for clause in clauses:
        for sentence in re.split(r'[。\n]',clause.text):
            if not re.search(r'不定期|无固定期限',sentence) or '解除' not in sentence:
                continue
            durations=[p for p in extract_parameters(sentence) if p['kind']=='duration' and not p['calendar_uncertain']]
            if (re.search(r'(?:无需|无须|不必|免于)[^，；]{0,8}(?:书面|通知)',sentence)
                or ('提前' in sentence and '通知' in sentence and any(p['normalized']<60*24 for p in durations))):
                conflicts.append(sentence)
    if conflicts:
        item.decision_trace.pop('statutory_default_notice',None)
        _set_adverse_if_found(item,clauses,assessment=('|'.join(map(re.escape,conflicts)),
            '不定期物业服务解除条款缩短或排除法定通知保护，应按第948条审查。'))
        item.decision_trace['semantic_requirements']=[dict(e) for e in item.coverage_elements]
        item.decision_trace['priority_positive_adverse_verification']={
            'source_clause_ids':[e['clause_id'] for e in item.evidence_clauses]}
        for row in item.coverage_elements+item.decision_trace['semantic_requirements']:
            row['recommendation_action']=PROPERTY_INDEFINITE_ACTION
        item.judge_source='service_atomic_evidence'
        item.suggested_clause_example='建议'+PROPERTY_INDEFINITE_ACTION+'。'
        return
    if item.coverage_status=='部分覆盖':
        item.decision_trace['statutory_default_notice']=PROPERTY_INDEFINITE_NOTICE
        item.risk_level='低'
        item.legal_consequence_if_missing=PROPERTY_INDEFINITE_NOTICE+'可在合同中明确以便履行。'
        item.risk_point_description='已约定转为不定期；合同未复述不定期阶段的60日书面通知要求，但法定规则仍然适用，仅需表达优化。'
        item.reasoning_summary=item.risk_point_description
        item.suggested_clause_example='建议'+PROPERTY_INDEFINITE_ACTION+'。'
        for row in item.coverage_elements+item.decision_trace.get('semantic_requirements',[]):
            if row.get('element_id')=='termination_notice':
                row['recommendation_action']=PROPERTY_INDEFINITE_ACTION


def apply(items,clauses):
    from review_v2.utility_supply_evidence import _set_atomic_item, _find_supports
    scenario=resolve('\n'.join(c.text for c in clauses))
    profiles=profiles_for(clauses)
    _,fee_evidence=_find_supports(clauses,'service_fee_facts',FEE_FACTS)
    for item in items:
        item.decision_trace['service_scenario']=scenario
        item.decision_trace['service_fee_facts']=fee_evidence
        if not scenario['values']['consumer']:
            # Localize generated prose only; never rewrite source quotations.
            for field in ('risk_point_description','legal_consequence_if_missing','suggested_clause_example','reasoning_summary','action_suggestion'):
                value=getattr(item,field,None)
                if isinstance(value,str):
                    setattr(item,field,value.replace('消费者','服务接受方'))
        if item.coverage_status in {'不适用','NOT_APPLICABLE','INSUFFICIENT_CONTEXT'}:
            continue
        if not scenario['values']['training'] and item.node_id in {'service_item_attachment','fee_standard_attachment'}:
            content = PROFILES['service_content_standard'] if item.node_id=='service_item_attachment' else [('service_price_method','服务总价或可执行的单价计费标准', FEE_FACTS[0][2]+'|'+UNIT_PRICE)]
            subject = r'服务项目|服务清单|项目清单' if item.node_id=='service_item_attachment' else r'收费标准|费用明细|价格表'
            text='\n'.join(c.text for c in clauses)
            explicit_reference=bool(re.search(r'(?:'+subject+r')[^。\n]{0,25}(?:详见|见|以)[^。\n]{0,10}附件|附件[^。\n]{0,20}(?:缺失|未提供)',text))
            if not explicit_reference:
                _set_atomic_item(item,content,clauses)
                item.decision_trace['document_equivalence']='BODY_OR_ATTACHMENT_CONTENT'
                item.judge_source='service_atomic_evidence'
                continue
        if item.node_id in {'provider_qualification_attachment','qualification_attachment'} and not scenario['values']['training']:
            _set_atomic_item(item,PROFILES['provider_qualification_attachment'],clauses)
            item.risk_group='service_qualification_document_delivery'
            item.decision_trace['finding_parent_group']='service_qualification_document_delivery'
            item.judge_source='service_atomic_evidence'
            continue
        if item.node_id in profiles and not scenario['values']['training']:
            _set_atomic_item(item,profiles[item.node_id],clauses)
            item.decision_trace.pop('priority_assessment',None)
            item.judge_source='service_atomic_evidence'
            apply_property_indefinite_law(item,clauses)
    from review_v2.contract_effects import reconcile
    # Retain source-search truth independently of the final evidence projection.
    # Later renderers cannot make a directly found element absent by dropping
    # its citation or overwriting the rule's compound status.
    for item in items:
        specs=profiles.get(item.node_id)
        if specs and not scenario['values']['training'] and item.coverage_status not in {'不适用','NOT_APPLICABLE','INSUFFICIENT_CONTEXT'}:
            found,source_rows=_find_supports(clauses,item.node_id,specs)
            item.decision_trace['service_positive_source_facts']=[
                {'element_id':key,'quotes':[r['quote'] for r in source_rows if key in r['supported_elements']]}
                for key in sorted(found)]
    reconcile(items,clauses)
    return items
