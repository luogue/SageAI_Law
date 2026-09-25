"""Deterministic EMP/NC policies over typed facts; no contract text searches."""
from copy import deepcopy
from datetime import date, timedelta

from review_v2.employment_fact_schema import ELEMENTS


def adverse(store, node):
    if node.startswith("termination_"):
        from review_v2.termination_facts import adverse as exit_adverse
        return exit_adverse(store,node)
    if node.startswith("employment_part_time_"):
        from review_v2.employment_rule_adapter import adverse as part_time_adverse
        return part_time_adverse(store,node)
    if node.startswith('employment_dispatch_'):
        from review_v2.employment_dispatch import adverse as dispatch_adverse
        return dispatch_adverse(store,node)
    if node == "employment_open_ended_limit":
        from review_v2.employment_indefinite import limit_adverse
        return limit_adverse(store,node)
    selected = []
    reasons = []

    def select(key, predicate, reason):
        rows = [r for r in store.get(key, positive=False) if predicate(r['normalized_value'])]
        if rows:
            selected.extend(rows)
            reasons.append(reason)

    from review_v2.employment_conditions import change_risk, discipline_risk
    if node == 'employment_worker_charge':
        from review_v2.employment_conditions import charge_risk
        select('worker.security_payment', charge_risk,
               '向劳动者收取押金保证金或从工资扣收费用；返还约定不消除扣收风险。')
    if node == 'employment_safety':
        select('labor_protection.training_excluded', lambda v:v is True,
               '明确排除必要安全培训或允许未经必要培训作业，存在劳动保护风险。')
    if node == 'employment_work':
        select('job.change_terms', change_risk, '未经协商一致单方变更劳动条件、降低工资或以拒绝任意调岗作为违纪，存在变更权限过宽风险。')
    if node == 'employment_exit':
        select('discipline.dismissal_terms', discipline_risk, '机械将轻微行为或不论情节的行为认定为严重违纪并直接解除，缺少严重程度与处分比例性的审查。')
    if node == 'employment_arbitrary_exit':
        select('discipline.dismissal_terms', lambda v: discipline_risk(v) and v.get('compensation_waived') is True,
               '机械认定严重违纪并直接解除，同时明确排除经济补偿。')
    insurance = {'employment_insurance','employment_illegal_waiver'}
    if node in insurance:
        for key in ('cash_replacement','waived','employer_share_shifted','employer_underpays',
                    'employer_liability_excluded','employee_remedy_excluded'):
            select('social_insurance.' + key, lambda v: v is True, '现金替代、放弃或转嫁单位法定社保义务，与参保缴费义务冲突。')
    if node == 'employment_hours':
        select('working_hours.overtime', lambda v:v in {'ALL_INCLUDED','WAIVED','HOLIDAY_TIME_OFF_ONLY'},
               '约定排除加班报酬或用调休替代法定节假日加班工资。')
        select('working_hours.rest_days_per_week', lambda v:v < 1, '约定每周没有休息日。')
        select('working_hours.rest_waived', lambda v:v is True, '明确剥夺劳动者休息安排。')
    if node == 'employment_wage':
        from review_v2.employment_conditions import charge_risk
        select('worker.security_payment',lambda v:charge_risk(v) and v.get('deducted_from_wage') is True,'从工资中扣收押金保证金或费用。')
        select('salary.withheld_for_handover', lambda v:v is True, '以交接等条件扣留已挣得工资。')
    if node in {'employment_exit','employment_arbitrary_exit'} and 'TASK' in store.values('contract.type'):
        select('contract.term_limit_mode',lambda v:v=='EMPLOYER_DETERMINED_COMPLETION',
               '任务完成由用人单位单方自行决定并据此终止，缺少客观完成标准及确认程序，存在任意终止风险。')
    if node == 'employment_exit':
        select('termination.approval_required', lambda v:v is True, '以单位批准限制劳动者依法辞职。')
        select('termination.employee_right_waived', lambda v:v is True, '排除劳动者依法解除或辞职的权利。')
        select('termination.notice_days', lambda v:v > 30, '普通辞职通知期限超过三十日，需核对其对法定辞职权的限制。')
        select('termination.employer_unrestricted', lambda v:v is True, '雇主任意解除授权超出法定解除条件。')
    if node in {'employment_compensation','employment_arbitrary_exit'}:
        unrestricted = store.get('termination.employer_unrestricted')
        if node == 'employment_compensation' or unrestricted:
            select('economic_compensation.statutory', lambda v:v['kind'] in {'WAIVED','EXCLUDED'}, '排除或放弃解除终止后的法定经济补偿。')
        for key in ('waived','reduced'):
            if node == 'employment_compensation' or unrestricted:
                select('economic_compensation.' + key, lambda v:v is True, '排除或降低解除终止后的法定经济补偿。')
        if selected and node == 'employment_arbitrary_exit':
            selected.extend(unrestricted)
    if node == 'employment_compensation':
        select('economic_compensation.statutory_percentage', lambda v:v < 100, '约定补偿比例低于法定补偿标准。')
        select('economic_compensation.payment_delay_months', lambda v:v >= 3, '解除补偿延后数月支付，需处理迟延结算风险。')
    if node == 'employment_general_penalty':
        select('penalties.obligations', lambda v:v.get('imposed',True) is True and v.get('scope') in {'ORDINARY_RESIGNATION','CONFIDENTIALITY','ORDINARY_DISCIPLINE','PROPERTY_DAMAGE','PROJECT_TASK_PERFORMANCE','WORK_TASK_COMPLETION','ATTENDANCE','RESIGNATION_NOTICE','OTHER'},
               '约定劳动者承担项目任务履行、普通离职、考勤纪律或一般保密违约金；应区分法定允许的培训服务期、竞业违约金与实际损失赔偿。')
    if node in {'employment_noncompete_adverse','employment_noncompete_term'}:
        select('non_compete.compensation_waived', lambda v:v is True, '离职竞业限制排除经济补偿。')
        select('non_compete.duration_months', lambda v:v > 24, '离职竞业限制期限超过二十四个月。')
        if node == 'employment_noncompete_adverse':
            from review_v2.noncompete_financial import assess
            financial, financial_facts = assess(store)
            if financial['risks']:
                selected.extend(financial_facts)
                reasons.extend(financial['risks'])
            select('non_compete.all_staff', lambda v:v is True, '竞业义务概括适用于所有员工，未按秘密接触范围限定。')
    if node == 'employment_ip_ownership':
        select('ip.allocations', lambda v:v['beneficiary'] in {'EMPLOYER','HOST'} and v['mode'] == 'AUTOMATIC'
               and v['scope'] in {'ALL_DURING_EMPLOYMENT','NON_DUTY','PRE_EXISTING','UNDIFFERENTIATED_RESULTS'},
               '概括将非职务成果或所有在职成果自动归用人单位，未区分工作关联及法定权利类型。')
        select('ip.personal_rights_waived', lambda v:v is True, '概括排除署名等人身权。')
    if node == 'employment_probation_limit':
        from review_v2.employment_facts import add_months
        select('probation.repeated', lambda v:v is True, '同一劳动者与用人单位重复约定试用期。')
        kinds = store.values('contract.type')
        months = store.values('contract.duration_months')
        start, end = store.values('contract.start_date'), store.values('contract.end_date')
        trial = store.values('probation.duration_months')
        ts, te = store.values('probation.start_date'), store.values('probation.end_date')
        if 'TASK' in kinds:
            present = ('CURRENT' in store.values('probation.arrangement') or any(m > 0 for m in trial) or bool(ts or te))
            if present:
                for key in ('contract.type','probation.arrangement','probation.duration_months','probation.start_date','probation.end_date'):
                    selected.extend(f for f in store.get(key) if key != 'probation.arrangement' or f['normalized_value']=='CURRENT')
                reasons.append('以完成一定工作任务为期限的劳动合同不得约定试用期；不是缩短期限或调整试用工资的问题。')
            limit = None
        elif 'INDEFINITE' in kinds:
            limit = 6
        elif start and end:
            s, e = date.fromisoformat(start[0]), date.fromisoformat(end[0]) + timedelta(days=1)
            limit = 0 if e < add_months(s,3) else 1 if e < add_months(s,12) else 2 if e < add_months(s,36) else 6
        elif months:
            m = min(months)
            limit = 0 if m < 3 else 1 if m < 12 else 2 if m < 36 else 6
        else:
            limit = None
        excessive = limit is not None and (any(m > limit for m in trial) or
            (ts and te and date.fromisoformat(te[0]) + timedelta(days=1) > add_months(date.fromisoformat(ts[0]),limit)))
        if excessive:
            for key in ('contract.type','contract.duration_months','contract.start_date','contract.end_date',
                        'probation.duration_months','probation.start_date','probation.end_date'):
                selected.extend(store.get(key))
            reasons.append(f'代码按合同期限计算试用期上限为{limit}个月，约定试用期超过该上限。')
    rows = store.evidence(list({f['fact_id']:f for f in selected}.values()), node + '_adverse')
    for row in rows:
        row['reason'] = '；'.join(dict.fromkeys(reasons))
    if node in {"employment_arbitrary_exit", "employment_exit"}:
        from review_v2.employment_indefinite import capability_adverse
        rows.extend(capability_adverse(store,node))
    from review_v2.employment_risk_semantics import annotate
    return annotate(store,rows)


def requirements(store, node, original):
    from review_v2.lease_semantics import requirement
    from review_v2.element_resolution import conditional_element
    rows = deepcopy(original)
    if node in {'employment_secret_scope','employment_secret_duty','confidentiality_parties','confidentiality_remedies'}:
        from review_v2.nda_semantics import resolve
        rows = resolve(node, rows, '')
    conditions = []
    if node == 'employment_compensation' and getattr(store,'agreement_type','labor')=='employment_termination':
        # Settlement has two independent payment obligations. One deadline
        # cannot prove the other; keep separate verified evidence bindings.
        rows = [r for r in rows if r['element_id']!='employment_compensation_2'] + [
            requirement('termination_wage_deadline','解除终止后工资及奖金结算期限'),
            requirement('termination_compensation_deadline','解除终止经济补偿结算期限')]
    if node == 'employment_noncompete_scope':
        for row in rows:
            if row['element_id'] == 'employment_noncompete_scope_1':
                row['proposition'] = '竞业限制适用人员范围'
    # External eligibility facts belong to the reasonableness assessment, not
    # this rule's completeness conditions. Even an unresolved condition here
    # would change the contract coverage verdict during aggregation.
    if node == 'employment_identity' and getattr(store,'agreement_type','labor')=='non_compete':
        rows = [r for r in rows if r['element_id'] in {'employment_identity_name','employment_identity_2'}]
        if not any(r['element_id']=='employment_identity_name' for r in rows):
            rows.insert(0,requirement('employment_identity_name','用人单位名称'))
    if node == 'employment_term':
        rows = rows[:1] + [requirement('employment_term_start','生效或起始日期')]
        kinds = store.values('contract.type')
        if 'TASK' in kinds:
            rows.extend([requirement('employment_term_task','具体工作任务'),requirement('employment_term_task_end','任务完成终止节点')])
        elif 'INDEFINITE' not in kinds:
            rows.append(requirement('employment_term_end','终止日期'))
    if node == 'employment_safety':
        health = next(r for r in rows if r['element_id'] == 'employment_safety_2')
        hazards = store.values('labor_protection.hazard_exists')
        prerequisite = hazards[0] if len(set(hazards)) == 1 else None
        condition = conditional_element(health['element_id'],health['proposition'],prerequisite,store.element(health['element_id']),
            prerequisite_fact='岗位实际存在职业病危害因素', verification_instruction='核实岗位是否存在职业病危害因素，再确定专项保护义务。')
        condition['prerequisite_evidence'] = store.evidence(store.get('labor_protection.hazard_exists',positive=False),health['element_id'])
        condition['source_clause_ids'] = [e['clause_id'] for e in condition['prerequisite_evidence']]
        conditions = [condition]
        if prerequisite is not True:
            rows = [r for r in rows if r['element_id'] != health['element_id']]
        needs_training = prerequisite is True or True in store.values('labor_protection.special_training_required')
        for row in rows:
            if row['element_id'] == 'employment_safety_training':
                row['risk_relevant'] = needs_training
                row['gap_risk_level'] = '中' if needs_training else '低'
                if not needs_training:
                    row['proposition'] = '安全培训条款（可选完善；未单列不等于未履行培训义务）'
    for row in rows:
        key = row['element_id']
        if key not in ELEMENTS:
            from review_v2.deepseek_facts import FactExtractionError
            raise FactExtractionError('UNMAPPED_EMPLOYMENT_REQUIREMENT:' + key)
        # Preserve the established requirement protocol, but no lexical
        # pattern is used by the structured-fact supports/corpus implementation.
        row.update(fact_concepts=ELEMENTS[key], semantic_patterns=(), evidence_unit='clause')
    # Split conjunctive coverage into atomic children. A single known identity
    # or insurance duty must survive even when its sibling is absent.
    atomic = []
    for row in rows:
        options = row['fact_concepts']
        if len(options) == 1 and len(options[0]) > 1:
            from review_v2.employment_fact_schema import CONCEPTS
            for concept in options[0]:
                key = row['element_id'] + '::' + concept
                spec = [(concept,)]
                store.element_specs[key] = spec
                label = CONCEPTS[concept].split('（')[0].split('，')[0]
                atomic.append({**row,'element_id':key,'parent_element_id':row['element_id'],
                               'proposition':label,'fact_concepts':spec})
        else:
            atomic.append(row)
    confirmed = []
    for row in atomic:
        if store.unresolved(row['element_id']):
            condition = conditional_element(row['element_id'],row['proposition'],None,[],
                prerequisite_fact='全文事实抽取结果可以确定',
                verification_instruction='抽取与独立语义核验尚不能确定：'+row['proposition']+'；需人工确认原文，不能判为缺失。')
            conditions.append(condition)
        else:
            confirmed.append(row)
    from review_v2.dispatch_assessment import assessment
    legal_assessment = assessment(store, node)
    if legal_assessment and legal_assessment['status'] == 'VERIFY':
        confirmed.append({
            'element_id': node + '_legal_verification',
            'proposition': '专项合法性事实核验',
            'requirement_kind': 'EXTERNAL_VERIFICATION',
            'verification_instruction': legal_assessment['reason'],
            'risk_relevant': False,
        })
    return confirmed, conditions
