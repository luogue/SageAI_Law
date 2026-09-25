"""Transport semantic requirements consumed by the existing atomic pipeline."""
from copy import deepcopy
import re
from review_v2.lease_semantics import requirement, corpus_facts, evidence_identity

PROFILES = {
 'transport_freight_amount_payment': [
  requirement('transport_freight_amount','运费金额或可验证价格标准',r'(?:运费|运输费)[^。\n]{0,30}(?:\d[\d,.]*元|报价单|价格表|每吨)|(?:报价单|价格表)[^。\n]{0,40}(?:签章|签字|为准)'),
  requirement('transport_freight_settlement','运费结算方式',r'(?:依据|按照|根据)[^。\n]{0,40}(?:运输合同|派车单|账单)[^。\n]{0,25}结算|按月结算'),
  requirement('transport_freight_date','付款或结算节点',r'每月[^。\n]{0,25}(?:结清|结算|支付)|(?:签收|结算|开票)后[^。\n]{0,20}(?:日|天)[^。\n]{0,12}(?:支付|付款)')],
 'transport_change_request_procedure': [
  requirement('transport_change_notice','变更或终止通知',r'(?:变更|终止|解除)[^。\n]{0,65}(?:通知对方|书面通知)'),
  requirement('transport_change_notice_period','变更终止提前通知期限',r'(?:变更|终止|解除)[^。\n]{0,60}提前[^。\n]{0,20}通知'),
  requirement('transport_change_confirmation','变更指令确认',r'(?:变更|终止|解除)[^。\n]{0,100}(?:双方认可|书面确认|确认指令)')],
 'transport_delivery_procedure': [
  requirement('transport_delivery_recipient','交付对象或收货人',r'(?:交付|交给|送交)[^。\n]{0,25}(?:收货人|指定接收人)|收货人(?:为|[：:])[^。\n_]{2,40}'),
  requirement('transport_delivery_authority','收货身份或授权核验',r'(?:核验|核对|查验)[^。\n]{0,40}(?:收货人身份|收货身份|授权书|收货授权)'),
  requirement('transport_arrival_notice','到货通知',r'(?:到货|到达|货物抵达)[^。\n]{0,50}通知[^。\n]{0,20}(?:收货人|接收人)'),
  requirement('transport_delivery_receipt','签收或交接方式',r'(?:收货人|接收人|双方)[^。\n]{0,40}(?:签署|签字|确认)[^。\n]{0,30}(?:交接单|回单|签收单|签收记录)|(?:采用|通过)[^。\n]{0,15}电子签收'),
  requirement('transport_delivery_completion','交付完成节点或有效签收标准',r'(?:签收|交接)[^。\n]{0,40}(?:视为|即为|标志)[^。\n]{0,15}交付完成|交付完成[^。\n]{0,35}(?:以|须)[^。\n]{0,20}签收')],
 'transport_cargo_handover_list': [
  requirement('transport_handover_names','交接单据中的货物名称',r'(?:托运单|出库单|交接单|清单)[^。\n]{0,100}(?:货物名称|品名)|(?:货物名称|品名)[^。\n]{0,100}(?:托运单|出库单|交接单|清单)'),
  requirement('transport_handover_quantity','交接单据中的数量',r'(?:托运单|出库单|交接单|清单)[^。\n]{0,100}(?:数量|件数)|(?:数量|件数)[^。\n]{0,100}(?:托运单|出库单|交接单|清单)'),
  requirement('transport_handover_appearance','交接时货物外观状态记录',r'(?:交接|签收|清单|出库单|托运单)[^。\n]{0,70}外观'),
  requirement('transport_handover_packaging','交接时包装状态记录',r'(?:交接|签收|清单|出库单|托运单)[^。\n]{0,70}包装(?:状态|情况|完整|完好)'),
  requirement('transport_handover_seal','封签或交接状态记录',r'(?:交接|签收|清单|出库单|托运单)[^。\n]{0,70}(?:封签|封条|交接状态|异常情况)')],
 'transport_exemption_force_majeure': [
  requirement('transport_force_arrangement','不可抗力免责安排',r'不可抗力[^。\n]{0,100}(?:免责|免除|履行|终止)'),
  requirement('transport_force_definition','不可抗力客观认定标准',r'不能预见[^。\n]{0,35}不能避免[^。\n]{0,35}不能克服'),
  requirement('transport_force_effect','根据实际影响处理部分或全部不能履行',r'(?:不可抗力|影响)[^。\n]{0,100}部分[^。\n]{0,30}全部[^。\n]{0,30}(?:责任|履行)'),
  requirement('transport_force_notice','不可抗力通知及证明',r'不可抗力[^。\n]{0,120}通知[^。\n]{0,60}证明'),
  requirement('transport_force_mitigation','不可抗力减损安排',r'(?:不可抗力|受影响方)[^。\n]{0,120}(?:减轻损失|减损|防止损失扩大)')],
 'transport_cargo_nature_value': [
  requirement('transport_cargo_nature','货物种类或性质',r'(?:运输货物|货物种类|货物名称|货物性质|货品)(?:包括|为|是|[：:])[^。\n]{2,100}'),
  requirement('transport_cargo_value','货物价值声明',r'(?:货物|货品|声明|申报)[^。\n]{0,12}价值[^。\n]{0,20}(?:\d[\d,，.]*|[一二三四五六七八九十百千万]+)\s*元')],
 'transport_carrier_safe_transport': [
  requirement('transport_vehicle_fitness','运输车辆技术性能及安全状态',r'(?:车辆|运输工具)[^。\n]{0,45}(?:技术性能良好|性能良好|安全检验合格|符合安全标准)'),
  requirement('transport_vehicle_credentials','运输车辆证照合法有效',r'(?:车辆|证照|证件)[^。\n]{0,45}(?:合法[、，\s]*有效|齐全[、，\s]*(?:合法[、，\s]*)?有效|手续齐全)'),
  requirement('transport_safe_carriage_duty','承运人安全运输或规范操作义务',r'(?:承运人|承运方|乙方)[^。\n]{0,70}(?:应|须|保证|负责|确保)[^。\n]{0,30}(?:安全运输|货物安全|固定及防护|妥善运输|安全规范操作)')],
 'transport_insurance_document': [
  requirement('transport_insurance_arrangement','运输保险安排',r'(?:购买|投保|办理|已投)[^。\n]{0,65}(?:交强险|商业险|责任险|货运险|运输保险|各种保险|相关保险)'),
  requirement('transport_insurance_proof','保险文件提供或留存安排',r'(?:提供|提交|保存|附具)[^。\n]{0,100}(?:保险卡|保单|保险凭证)|(?:保险卡|保单|保险凭证)[^。\n]{0,40}(?:提供|提交|保存)')],
 'transport_party_identity': [
  requirement('transport_shipper_identity','托运方身份',r'(?:委托方|托运人|托运方)[：:]?[^。\n]{0,40}(?:公司|企业|甲方)|甲方[^。\n]{0,12}(?:委托方|托运方)'),
  requirement('transport_carrier_identity','承运方身份',r'(?:承运方|承运人)[：:]?[^。\n]{0,40}(?:公司|企业|乙方)|乙方[^。\n]{0,12}承运方'),
  requirement('transport_consignee_identity','收货人身份',r'收货人[：:]\s*[^_\s。\n]{2,}|收货人(?:为|是)[^。\n]{2,30}')],
 'transport_contract_document_priority': [
  requirement('transport_waybill','运单或托运单安排',r'运单|托运单|物流单'),
  requirement('transport_document_precedence','合同与运输单证冲突时的效力顺位',r'(?:合同|运单|托运单)[^。\n]{0,80}(?:不一致|冲突)[^。\n]{0,60}(?:为准|优先|顺序)|(?:合同|运单|托运单)[^。\n]{0,40}优先适用')],
 'transport_responsibility_period': [
  requirement('transport_in_transit_duty','运输过程中的责任安排',r'(?:乙方|承运人|承运方)[^。\n]{0,20}运输(?:过程|期间|途中)[^。\n]{0,100}(?:承担|负责|赔偿)'),
  requirement('transport_period_start','责任期间起点',r'自[^。\n]{0,35}(?:接收|接管|接货|交接)[^。\n]{0,30}(?:起|开始)'),
  requirement('transport_period_end','责任期间终点',r'(?:至|直到)[^。\n]{0,40}(?:交付|签收)[^。\n]{0,25}(?:止|结束)')],
}
FORCE_ADVERSE = [
 requirement('force_restricted_definition','不可抗力采用排他性事件清单，可能不当缩窄认定范围',r'不可抗力[^。\n]{0,12}(?:仅指|仅限于|只包括|仅包括)[^。\n]{2,80}'),
 requirement('force_expanded_definition','将一般经营或履约困难纳入不可抗力',r'不可抗力[^。\n]{0,35}(?:包括|包含|指)[^。\n]{0,40}(?:资金不足|经营亏损|市场价格波动|人员短缺)'),
 requirement('force_automatic_termination','不能履行即自动终止，未区分影响程度和继续履行可能性',r'不可抗力[^。\n]{0,180}(?:自动终止|自动解除)'),
 requirement('force_notice_waiver','不可抗力排除通知、证明或减损义务',r'不可抗力[^。\n]{0,100}(?:无需|不必|无须)[^。\n]{0,20}(?:通知|证明|减损)'),
]
LIMIT=r'保价|限额赔偿|赔偿限额|最高赔偿|赔偿[^。\n]{0,12}(?:不超过|封顶)|未保价只赔|声明价值[^。\n]{0,20}(?:限额|为限)'
MULTI=r'多式联运|分段运输|区段承运人|海陆联运|公铁联运|铁海联运|多个[^。\n]{0,10}承运人|公路[^。\n]{0,20}(?:转|衔接)铁路'
CONDITIONS={
 'transport_declared_value_clause_prompt':LIMIT,
 'transport_invalid_limitation_clause':LIMIT,
 'transport_multimodal_contracting_carrier':MULTI,
 'transport_segment_carrier_liability':MULTI,
 'transport_unknown_segment_rule':MULTI,
 'transport_special_cargo_handling':r'危险品|冷链|温控|易碎品|易腐|贵重物品|特殊货物',
 'transport_dangerous_goods_notice':r'危险品|危化品|易燃|易爆|有毒',
 'transport_exemption_nature_reasonable_loss':r'自然性质|自然损耗|合理损耗|易腐|挥发|正常短少',
}

def condition_matches(pattern,text):
    for m in re.finditer(pattern,text):
        if not re.search(r'不涉及|不属于|不含|非|无',text[max(0,m.start()-6):m.start()]):
            return True
    return False

def apply(items,clauses):
    from review_v2.engine import _set_item_not_applicable, _set_multi_element_state
    text='\n'.join(c.text for c in clauses)
    from review_v2.carriage_scope import analyze, SHIPMENT_ITEMS
    framework = analyze(text)['framework']
    for item in items:
        if framework and item.item_id in SHIPMENT_ITEMS:
            item.applicable_if='当前协议直接约定具体运输任务时适用；明确另签每票运输单的事项在下游审查。'
            item.applicability.update({'applicable':False,'condition':item.applicable_if})
            _set_item_not_applicable(item,'具体运输任务明确留待每票另签合同或运单，本框架不重复要求单票事实。')
            continue
        condition=CONDITIONS.get(item.node_id)
        if condition:
            active=condition_matches(condition,text)
            item.applicable_if='存在对应的限额、特殊货物或多式/分段运输事实时适用。'
            item.applicability.update({'applicable':active,'condition':item.applicable_if})
            if not active:
                _set_item_not_applicable(item,'全文未识别本专项规则所要求的前置交易事实，不因缺少专项条款认定风险。')
                continue
        specs=PROFILES.get(item.node_id)
        if not specs: continue
        specs=deepcopy(specs)
        adverse=False
        if item.node_id == 'transport_exemption_force_majeure':
            adverse_facts=corpus_facts(clauses,FORCE_ADVERSE)
            matched=[s for s in FORCE_ADVERSE if adverse_facts[s['element_id']]]
            if matched:
                specs=deepcopy(matched)
                adverse=True
        if item.node_id == 'transport_insurance_document' and condition_matches(r'保价',text):
            specs.append(requirement('transport_declared_value_proof','保价确认文件',r'(?:提供|签署|保存|附具)[^。\n]{0,50}(?:保价确认书|保价单|保价凭证)'))
        facts=corpus_facts(clauses,specs)
        facts={k:[evidence_identity(r) for r in rows] for k,rows in facts.items()}
        evidence=[r for e in specs for r in facts[e['element_id']]]
        covered=[e['proposition'] for e in specs if facts[e['element_id']]]
        missing=[e['proposition'] for e in specs if not facts[e['element_id']]]
        item.decision_trace['semantic_requirements']=deepcopy(specs)
        item.decision_trace['shared_semantic_facts']=deepcopy(facts)
        item.evidence_clauses=evidence
        item.evidence_location='；'.join(dict.fromkeys(r['location'] for r in evidence))
        item.coverage_status=item.status='通过' if not missing else '部分覆盖' if covered else '缺失'
        item.issue_type='通过' if not missing else '条款缺陷' if covered else '完全缺失'
        item.reasoning_summary=item.risk_point_description=('已覆盖：'+'；'.join(covered)+'。' if covered else '')+('尚需明确：'+'；'.join(missing)+'。' if missing else '')
        item.suggested_clause_example='建议明确'+'；'.join(missing)+'。' if missing else ''
        if covered and missing:
            item.legal_consequence_if_missing='尚未明确'+ '；'.join(missing)+'，可能导致相应履行标准、责任认定或举证争议。'
        item.needs_manual_review=False
        item.decision_trace.pop('element_evidence_truth',None)
        if adverse:
            item.coverage_status=item.status='风险条款'
            item.issue_type='条款风险'
            item.reasoning_summary=item.risk_point_description='；'.join(covered)+'。'
            item.legal_consequence_if_missing='；'.join(covered)+'，可能造成免责范围、继续履行及终止效力争议。'
            item.suggested_clause_example='建议以法定客观标准认定不可抗力，按实际影响区分部分或全部不能履行；仅在符合解除条件时终止，并保留及时通知、提供证明及合理减损义务。'
            item.decision_trace['priority_positive_adverse_verification']={'source_clause_ids':list({r['clause_id'] for r in evidence})}
        _set_multi_element_state(item,[{**e,'status':('ADVERSE' if adverse else 'COVERED') if facts[e['element_id']] else 'MISSING',
            'bound_evidence_ids':[r.get('evidence_id') for r in facts[e['element_id']]]} for e in specs],evidence)
    return items
