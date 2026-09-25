"""Service scenario predicates and domain-neutral service evidence."""
import re

def project_checklist(checklist, text):
    """Project authorities and duplicate document checks before evaluation."""
    from dataclasses import replace
    scenario=resolve(text)
    if scenario['values']['consumer']:
        return checklist
    has_primary=any(r.node_id=='provider_qualification_attachment' for r in checklist)
    result=[]
    for rule in checklist:
        if has_primary and rule.node_id=='qualification_attachment':
            continue
        basis=re.sub(r'《(?:中华人民共和国)?消费者权益保护法》[^《；;\n]*', '',rule.legal_basis).strip('、，,；; ')
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
                  indefinite=bool(re.search(r'不定期服务|无固定(?:服务)?期限',text)))
    subtype = 'TRAINING_EDUCATION_SERVICE' if training else 'PREPAID_CONSUMER_SERVICE' if values['prepaid_consumer'] else 'CONSUMER_SERVICE' if consumer else 'GENERAL_B2B_SERVICE' if enterprise else 'GENERAL_SERVICE'
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
    return {key:dict(value=value,label=labels[key],scenario=scenario,
                     searched_clause_ids=[c.clause_id for c in clauses]) for key,value in scenario['values'].items()}


def qualification_conditions(text):
    special = bool(re.search(r'高(?:空|处)(?:作业|外墙|清洗)|特种(?:作业|设备操作)|(?:提供|从事|承担)[^。\n]{0,20}(?:医疗|诊疗|安保|消防设施维护|律师|审计)服务|律师事务所|注册会计师|执业医师', text))
    promised = bool(re.search(r'(?:人员|工作人员|医师|律师|会计师)[^。\n]{0,35}(?:必须|须|应)[^。\n]{0,20}(?:持有|取得|具备)[^。\n]{0,20}(?:资格证|执业证|职称|操作证)', text))
    documents = bool(re.search(r'(?:提供|提交|附具)[^。\n]{0,25}(?:资质证明|资格证|营业执照|许可证)|(?:资质证明|资格证|营业执照|许可证)[^。\n]{0,20}(?:作为附件|详见附件)',text))
    return dict(qualified_staff=special or promised, qualification_documents=documents)


PROFILES = {
 'service_nonperformance_remedy': [
    ('nonperformance_cure','未履行服务时的补救义务',r'(?:未提供|未履行|不能提供)[^。；\n]{0,65}(?:补救|重新履行|整改|退还)'),
    ('nonperformance_liability','未履行合同义务的损失责任',r'(?:违反本合同|未履行)[^。；\n]{0,90}(?:赔偿|承担[^。；]{0,10}损失)')],
 'service_quality_nonconform_remedy': [
    ('quality_cure','服务不符合标准时的整改补救',r'(?:质量|服务)[^。；\n]{0,30}(?:不符合|不达标)[^。；\n]{0,40}(?:整改|补救|重新)'),
    ('failed_cure_remedy','整改仍不达标时的后续救济',r'(?:整改|补救|重新履行)[^。；\n]{0,30}(?:仍|不能)[^。；\n]{0,50}(?:解除|减价|减少费用|退还)')],
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
    ('service_location','服务地点',r'(?:服务地点|办公区域|办公楼)[^。；]{0,120}(?:市|路|号|层)|(?:市|区)[^。；\n]{0,60}(?:路|大道)\d+号')],
 'termination_basis': [('termination_trigger','合同解除权及触发条件',r'(?:有权|可以|可|得)[^。；\n]{0,12}解除(?:本)?合同|合同[^。；\n]{0,15}(?:解除条件|可解除)|(?:严重违约|无法履行)[^。；\n]{0,35}解除')],
 'force_majeure_service_adjustment': [
    ('force_majeure_event','不可抗力事由',r'不可抗力[^。；\n]{0,40}(?:不能预见|自然灾害|政府行为)|不能预见、?不能避免[^。；\n]{0,20}不能克服'),
    ('force_majeure_relief','不可抗力不能履行的责任处理',r'不可抗力[^。；\n]{0,100}(?:不承担|免责|不视为[^。；]{0,10}违约)'),
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


def apply(items,clauses):
    from review_v2.utility_supply_evidence import _set_atomic_item, _find_supports
    scenario=resolve('\n'.join(c.text for c in clauses))
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
            content = PROFILES['service_content_standard'] if item.node_id=='service_item_attachment' else FEE_FACTS[:1]
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
        if item.node_id in PROFILES and not scenario['values']['training']:
            _set_atomic_item(item,PROFILES[item.node_id],clauses)
            item.decision_trace.pop('priority_assessment',None)
            item.judge_source='service_atomic_evidence'
    return items
