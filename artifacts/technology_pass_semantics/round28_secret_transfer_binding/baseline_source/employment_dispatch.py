"""Employment-form routing and dispatch policy over verified, source-bound facts."""
from dataclasses import replace
from review_v2.priority_checklist_helpers import required

LABELS = {'LABOR':'普通劳动合同', 'LABOR_DISPATCH':'劳务派遣劳动合同',
          'LABOR_INDEFINITE':'无固定期限劳动合同', 'LABOR_TASK':'以完成一定工作任务为期限劳动合同',
          'LABOR_PART_TIME':'非全日制用工'}

CONCEPTS = {
    'contract.employment_form':'当前实际用工关系 DIRECT直接招用 / DISPATCH派遣单位雇佣后派至独立用工单位 / PART_TIME非全日制。公司名称含人力资源或未来可能派遣不等于已设派遣关系；期限类型另存contract.type',
    'dispatch.auxiliary_noncore':'明确岗位为主营业务提供服务的非主营业务岗位（布尔值）；主营业务岗位为false，未知不生成',
    'dispatch.auxiliary_procedure':'辅助岗位已经过职工讨论、平等协商并公示认定的事实（布尔值），仅称辅助不推定程序完成',
    'dispatch.substitute':'明确属于替代暂时离岗员工的岗位（布尔值）；明确不替代为false，未提不推定false',
    'dispatch.worker_pay_method':'被派遣劳动者正式报酬分配办法具体内容（字符串）；仅说体系不同不算具体分配办法',
    'dispatch.comparator_pay_method':'用工单位同岗位人员的具体报酬分配办法（字符串），非笼统对照',
    'dispatch.comparator_pay':'用工单位可比岗位通常工资 money或formula对象，unit与正常工资一致时才可比较；非试用工资',
    'dispatch.comparable_work':'合同明确被派遣劳动者与对照人员属于同岗位、相同工作量、相同工资组成及可比计酬口径（布尔值），仅同岗位但工作量或工资组成未确认不推断可比',
    'dispatch.agency':'当前劳动关系的派遣单位名称（字符串），不是用工单位',
    'dispatch.host':'实际接受派遣并安排劳动的用工单位名称（字符串）',
    'dispatch.position':'派遣工作岗位（字符串）',
    'dispatch.period':'派遣期限或其与劳动合同期限的明确引用关系（字符串）',
    'dispatch.position_basis':'岗位的事实性质 TEMPORARY临时 / AUXILIARY非主营辅助 / SUBSTITUTE替代暂时离岗员工 / REGULAR_CORE常设主营岗位；只提长期固定而无主营描述，不推成REGULAR_CORE，另存long_term_position。可分别保存多个明确性质',
    'dispatch.long_term_position':'派遣岗位明确长期固定或常设（布尔值），不自行判断三性是否合法',
    'dispatch.temporary_duration_months':'临时性岗位明确持续月数（数值）',
    'dispatch.equal_pay':'对比用工单位同岗位员工的报酬安排 EQUAL同工同酬 / LOWER_ALLOWED明确允许低于同岗位 / DIFFERENT_SYSTEM只约定薪酬体系可以不同、未说明较低；不同体系不推断较低；不得低于为EQUAL，否定或禁止差别待遇不能抽成LOWER_ALLOWED',
    'dispatch.idle_pay':'无工作、待派或退回后等待期间报酬 MONTHLY_LOCAL_MINIMUM按月当地最低工资 / PAID_OTHER明确支付其他标准 / NONE明确不支付；禁止不付属于保护，不是NONE',
    'dispatch.worker_charges':'派遣单位或用工单位向劳动者收取派遣服务费、管理费等的安排 PROHIBITED明确禁止 / REQUIRED明确收费。不得收费不能抽成REQUIRED',
    'dispatch.return_procedure':'用工单位退回劳动者的条件及程序（字符串）',
    'dispatch.reassignment_procedure':'退回后另行派遣的安排（字符串）',
    'dispatch.refusal_termination':'拒绝重新派遣岗位的解除条件 ANY_OFFER任意新岗位均可解除 / MAINTAINED_CONDITIONS仅在维持或提高原约定条件且合法退回时可解除 / STATUTORY依合法条件 / PROHIBITED禁止仅因拒绝解除。保留限制性条件，不把任意拒绝与合法限定混淆',
    'dispatch.refusal_compensation_waived':'拒绝重新派遣岗位解除时明确不支付经济补偿（布尔值）；依法支付为false，未提及不推断',
    'dispatch.host_direct_dismissal':'用工单位获准直接解除与派遣单位的劳动合同（布尔值），禁止用工单位直接解除为false',
    'dispatch.agreement_disclosure':'派遣单位须向劳动者告知派遣协议中与其切身利益相关内容（布尔值）',
    'dispatch.agency_obligations':'派遣单位明确承担的雇主义务（字符串数组），如工资、社保、督促保护、解除证明等，按实际原文抽取',
    'dispatch.host_obligations':'用工单位明确承担的实际用工义务（字符串数组），如劳动条件、保护、加班、培训等',
    'dispatch.obligations_waived':'明确整体免除派遣单位或用工单位法定责任（布尔值），分别约定分工不等于免责',
}
ENUMS = {
    'contract.employment_form':{'DIRECT','DISPATCH','PART_TIME'},
    'dispatch.position_basis':{'TEMPORARY','AUXILIARY','SUBSTITUTE','REGULAR_CORE'},
    'dispatch.equal_pay':{'EQUAL','LOWER_ALLOWED','DIFFERENT_SYSTEM'},
    'dispatch.idle_pay':{'MONTHLY_LOCAL_MINIMUM','PAID_OTHER','NONE'},
    'dispatch.worker_charges':{'PROHIBITED','REQUIRED'},
    'dispatch.refusal_termination':{'ANY_OFFER','MAINTAINED_CONDITIONS','STATUTORY','PROHIBITED'},
}

SPECS = (
    ('identity','派遣主体、岗位与期限','《劳动合同法》第58条',
     [('派遣单位','dispatch.agency'),('用工单位','dispatch.host'),('派遣岗位','dispatch.position'),('派遣期限','dispatch.period')],
     '明确派遣单位、用工单位、工作岗位及派遣期限，并保持主体与实际安排一致。'),
    ('position','派遣岗位临时性、辅助性或替代性','《劳动合同法》第66条；《劳务派遣暂行规定》第3条',
     [('派遣岗位性质','dispatch.position_basis')],
     '核实岗位是否符合临时性、辅助性或替代性；辅助性岗位须履行讨论、协商和公示程序，临时性岗位存续不超过六个月。'),
    ('equal_pay','派遣劳动者同工同酬','《劳动合同法》第63条',
     [('同工同酬安排','dispatch.equal_pay')],
     '删除允许低于用工单位同岗位劳动者报酬的约定，实行相同的劳动报酬分配办法。'),
    ('idle_pay','无工作期间报酬','《劳动合同法》第58条；《劳务派遣暂行规定》第12条',
     [('无工作期间按月报酬','dispatch.idle_pay')],
     '明确无工作及待派期间由派遣单位按月支付不低于其所在地规定最低工资标准的报酬。'),
    ('charges','禁止向派遣劳动者收费','《劳动合同法》第60条',
     [('禁止派遣单位及用工单位向劳动者收取派遣费用','dispatch.worker_charges')],
     '明确派遣单位及用工单位均不得向劳动者收取派遣服务费或管理费等费用。'),
    ('return','退回、重新派遣与解除条件','《劳动合同法》第65条；《劳务派遣暂行规定》第12至17条',
     [('用工单位退回条件与程序','dispatch.return_procedure'),('重新派遣安排','dispatch.reassignment_procedure'),('拒绝新岗位后的解除条件','dispatch.refusal_termination')],
     '区分退回与解除，限定合法退回及重新派遣条件；不得将拒绝任意岗位一律视为严重违纪，并依法支付应付经济补偿。'),
    ('disclosure','派遣协议相关内容告知','《劳动合同法》第60条',
     [('告知与劳动者切身利益相关的派遣协议内容','dispatch.agreement_disclosure')],
     '由派遣单位向劳动者告知派遣协议中与其切身利益相关的内容，保留告知记录。'),
    ('duties','派遣单位与用工单位义务分工','《劳动合同法》第58条、第62条',
     [('派遣单位雇主义务','dispatch.agency_obligations'),('用工单位实际用工义务','dispatch.host_obligations')],
     '分别明确派遣单位的雇主义务和用工单位的劳动条件、劳动保护、加班待遇及岗位培训等义务，不得以分工免除法定责任。'),
)
ELEMENTS = {f'employment_dispatch_{node}_{n}':[(concept,)] for node,_,_,elements,_ in SPECS
            for n,(_,concept) in enumerate(elements,1)}
CHECKLIST = tuple(replace(required('DSP',i,'employment_dispatch_'+node,title,(),law,
    [(label,()) for label,_ in elements],risk='高',suggestion=suggestion),
    applicable_if='已验证当前劳动关系属于劳务派遣用工时适用')
    for i,(node,title,law,elements,suggestion) in enumerate(SPECS,1))


def classify(store):
    from review_v2.fact_validation import FactExtractionError
    forms=set(store.values('contract.employment_form'))
    if store.coverage['contract.employment_form']=='UNCERTAIN' or len(forms)>1:
        raise FactExtractionError('UNRESOLVED_EMPLOYMENT_FORM',failed_stage='VERIFIED_SUBTYPE',
            field='contract.employment_form',actual=sorted(forms),expected='one verified employment relationship')
    terms=set(store.values('contract.type'))
    form=next(iter(forms),'DIRECT')
    subtype='LABOR_DISPATCH' if form=='DISPATCH' else 'LABOR_PART_TIME' if form=='PART_TIME' else (
        'LABOR_INDEFINITE' if terms=={'INDEFINITE'} else 'LABOR_TASK' if terms=={'TASK'} else 'LABOR')
    evidence=store.evidence(store.get('contract.employment_form')+store.get('contract.type'),'employment_subtype')
    return {'subtype':subtype,'label':LABELS[subtype],'employment_form':form,'term_types':sorted(terms),
            'basis':'VERIFIED_FACTS' if forms else 'FULL_TEXT_NO_SPECIAL_FORM', 'evidence':evidence}


def adverse(store,node):
    selected=[]
    def pick(concept,predicate,reason):
        for f in store.get(concept,positive=False):
            if predicate(f['normalized_value']):
                selected.extend({**e,'reason':reason} for e in store.evidence([f],node+'_adverse'))
    from review_v2.dispatch_assessment import position_state, pay_state, term_state
    if node=='employment_dispatch_position':
        assessment=position_state(store)
        if assessment['status']=='RISK':
            for concept in assessment['concepts']:pick(concept,lambda v:True,assessment['reason'])
    if node=='employment_dispatch_equal_pay':
        assessment=pay_state(store)
        if assessment['status']=='RISK':
            for concept in assessment['concepts']:pick(concept,lambda v:True,assessment['reason'])
    if node=='employment_dispatch_identity':
        assessment=term_state(store)
        if assessment['status']=='RISK':
            for concept in assessment['concepts']:pick(concept,lambda v:True,assessment['reason'])
    if node=='employment_dispatch_idle_pay':
        pick('dispatch.idle_pay',lambda v:v=='NONE','明确排除无工作或待派期间报酬，与派遣单位按月支付最低工资标准报酬的义务冲突。')
    if node=='employment_dispatch_charges':
        pick('dispatch.worker_charges',lambda v:v=='REQUIRED','向劳动者收取派遣相关费用，违反派遣单位和用工单位不得收费的要求。')
    if node=='employment_dispatch_return':
        pick('dispatch.refusal_termination',lambda v:v=='ANY_OFFER','将拒绝任意重新派遣岗位一律作为解除依据，未区分维持或提高原约定条件等法定前提。')
        pick('dispatch.refusal_compensation_waived',lambda v:v is True,'拒绝重新派遣即排除经济补偿，不能替代对法定解除条件和补偿义务的判断。')
        pick('dispatch.host_direct_dismissal',lambda v:v is True,'用工单位退回劳动者不等于有权直接解除劳动者与派遣单位的劳动合同。')
    if node=='employment_dispatch_disclosure':
        pick('dispatch.agreement_disclosure',lambda v:v is False,'明确排除告知与劳动者切身利益相关的派遣协议内容。')
    if node=='employment_dispatch_duties':
        pick('dispatch.obligations_waived',lambda v:v is True,'以派遣单位和用工单位分工为由免除法定义务。')
    from review_v2.employment_conditions import onward_risk, return_risk, charge_risk
    if node=='employment_dispatch_onward':
        pick('dispatch.onward_assignment',onward_risk,'当前用工单位直接向另一用工主体再次安排劳动者，并视为原派遣延续。')
    if node=='employment_dispatch_return_basis':
        pick('dispatch.return_terms',return_risk,'仅凭普通绩效、主观匹配或组织调整即允许退回，扩大法定退回情形。')
    if node=='employment_dispatch_charges':
        security=store.get('worker.security_payment')
        evidence_ids={e['clause_id'] for f in security if charge_risk(f['normalized_value']) for e in f['evidence']}
        # Prefer the typed transaction on the same evidence; retain unrelated fees.
        selected=[e for e in selected if e.get('clause_id') not in evidence_ids]
        pick('worker.security_payment',charge_risk,'向派遣劳动者收取保证金或费用；可退还不排除禁止收取的要求。')
    from review_v2.employment_risk_semantics import annotate
    return annotate(store,selected)

from review_v2.priority_checklist_helpers import forbidden
CHECKLIST += tuple(replace(forbidden('DSP',number,'employment_dispatch_'+node,title,(),law,(),suggestion),
    applicable_if='已验证劳务派遣关系；核验主体流转和实际退回事由，不以关键词触发')
 for number,node,title,law,suggestion in [
 (9,'onward','用工单位再次派遣至其他用人单位','《劳动合同法》第62条','禁止用工单位再次派遣；区分内部工作安排与实际用工主体变更，由派遣单位依法办理必要的新安排。'),
 (10,'return_basis','用工单位退回条件约定过宽','《劳动合同法》第65条；《劳务派遣暂行规定》第12、13条','按法定事由及程序限定退回，不将普通绩效、主观匹配或单纯组织调整当然视为退回依据。')])
