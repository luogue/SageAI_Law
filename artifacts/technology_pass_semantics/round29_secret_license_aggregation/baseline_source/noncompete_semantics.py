"""Noncompete temporal roles and evidence prerequisites; no sample literals."""
import re

DURATION = r'[一二两三四五六七八九十百\d]+\s*个?\s*(?:月|年|日|天)'
TERM_PATTERNS = (
    r'劳动合同(?:解除(?:或者|或)?终止|解除|终止)(?:后|之日起)\s*' + DURATION + r'内[^。；\n]{0,60}不得[^。；\n]{0,80}(?:竞争|同类|类似|相同)',
    r'(?:自)?劳动合同(?:解除|终止)之日起\s*' + DURATION + r'内[^。；\n]{0,50}不得[^。；\n]{0,40}(?:竞争|同类|类似)',
    r'竞业(?:限制|禁止)(?:持续)?期(?:限)?\s*(?:为|是|：|:)\s*' + DURATION,
    r'离职后\s*' + DURATION + r'(?:内)?[^。；\n]{0,12}(?:承担|履行|遵守)竞业(?:限制|禁止)',
    r'(?:离职|解除劳动合同|终止劳动合同)后[^。；\n]{0,12}竞业(?:限制|禁止)(?:期(?:限)?)?\s*(?:为|：|:)?\s*' + DURATION,
)
DEFINED_TERM = r'之日起(?:的)?\s*' + DURATION + r'内[^。；\n]{0,35}(?:不得|履行|承担)'

# Human-facing names are separate from schema identifiers. Both consumers use
# FactStore.get, including its verification and positive-assertion filtering.
PREREQUISITE_FACTS = {
    'non_compete.person_scope': '竞业限制适用人员范围',
    'non_compete.actual_access': '员工已经实际接触、知悉、掌握商业秘密或实际负责具体秘密事项的事实',
    'non_compete.businesses': '竞业业务范围',
    'non_compete.territories': '竞业地域范围',
    'non_compete.duration_months': '竞业限制期限',
    'non_compete.compensation': '竞业限制补偿标准',
}


def prerequisite_facts(store):
    return [{'concept': key, 'label': label,
             'covered': bool(person_scope_facts(store) if key == 'non_compete.person_scope' else store.get(key)),
             'fact_ids': [f['fact_id'] for f in (person_scope_facts(store) if key == 'non_compete.person_scope' else store.get(key))]}
            for key, label in PREREQUISITE_FACTS.items()]


def person_scope_facts(store):
    return store.get('non_compete.person_scope') or store.get('non_compete.personnel')


def person_assessment(store):
    """External eligibility never participates in contractual completeness."""
    access = actual_access_verification(store)
    return {'person_scope': 'EXISTS' if person_scope_facts(store) else 'NOT_FOUND',
            'person_scope_fact_ids': [f['fact_id'] for f in person_scope_facts(store)],
            'person_eligibility': 'NEED_REVIEW' if access['state'] != 'CONFIRMED' else 'FACT_BASIS_AVAILABLE',
            'eligibility_basis_fact_ids': [f['fact_id'] for f in store.get('non_compete.person_eligibility')],
            'actual_access': access['state'],
            'instruction': '应结合人员类别、岗位职责、保密义务及实际接触秘密情况核验人员适格性；受限人员已写明不等于依法适格，适格性未知也不等于合同人员范围缺失。'}


def actual_access_verification(store):
    rows = store.get('non_compete.actual_access', positive=False)
    values = {f['normalized_value'] for f in rows}
    state = 'CONFIRMED' if values == {True} else 'DENIED' if values == {False} else 'NEEDS_VERIFICATION'
    message = ('原文明示劳动者尚未接触相关商业秘密，应核验竞业限制是否具备实际适用基础，不能仅以岗位接触能力代替。'
               if state == 'DENIED' else
               '合同适用范围与实际接触事实应分别判断；劳动者是否实际知悉、接触相关商业秘密无法仅凭现有合同文本确认，建议结合岗位职责、权限记录、项目资料等核验，不要求在合同中补写已接触声明。')
    return {'state': state, 'fact_ids': [f['fact_id'] for f in rows], 'instruction': message}


def temporal_roles(clauses):
    from review_v2.employment_fact_store import current
    store = current()
    if store is not None:
        return [{**ev, 'expression':str(f['normalized_value'])+'个月','role':'NONCOMPETE_DURATION'}
                for f in store.get('non_compete.duration_months') for ev in f['evidence']]
    rows=[]
    for clause in clauses:
        if clause.section_type not in {'正式合同条款','附件'}:
            continue
        for sentence in re.finditer(r'[^。；\n]+',clause.text):
            text=sentence.group()
            approved=[m.span() for p in TERM_PATTERNS for m in re.finditer(p,text)]
            if re.search(r'竞业(?:限制|禁止)期', ' '.join(clause.heading_path or [])):
                approved += [m.span() for m in re.finditer(DEFINED_TERM,text)]
            for m in re.finditer(DURATION+r'|每月|按月|每个自然月',text):
                before,after=text[max(0,m.start()-18):m.start()],text[m.end():m.end()+20]
                role='OTHER'
                if re.search(r'提前\s*$',before) and '通知' in after: role='NOTICE_PERIOD'
                elif re.search(r'解除(?:通知)?期限(?:为|：|:)\s*$',before): role='TERMINATION_PERIOD'
                elif m.group() in {'每月','按月','每个自然月'}: role='PAYMENT_CYCLE'
                elif '违约' in text and re.search(r'内.{0,10}(?:支付|履行|赔偿|纠正)',after): role='BREACH_PERFORMANCE_PERIOD'
                elif any(a<=m.start() and m.end()<=b for a,b in approved): role='NONCOMPETE_DURATION'
                rows.append({'clause_id':clause.clause_id,'location':clause.location,'text':text,
                    'expression':m.group(),'role':role,'source_start':sentence.start()+m.start(),'source_end':sentence.start()+m.end()})
    return rows


def attach_prerequisites(items, clauses):
    from review_v2.employment_fact_store import current
    store = current()
    if store is not None:
        for item in items:
            if item.node_id in {'employment_noncompete_scope','employment_noncompete_adverse'}:
                item.decision_trace['external_actual_access'] = actual_access_verification(store)
                item.decision_trace['noncompete_person_assessment'] = person_assessment(store)
            if item.node_id == 'employment_noncompete_adverse':
                item.decision_trace['noncompete_fact_prerequisites'] = {
                    'arrangement':store.values('non_compete.arrangement'),
                    'personnel':bool(person_scope_facts(store)),
                    'actual_access':bool(store.get('non_compete.actual_access')),
                    'access_capability':bool(store.get('non_compete.access_capability'))}
                if item.coverage_status not in {'不适用','风险条款'}:
                    from review_v2.noncompete_financial import assess
                    financial, financial_facts = assess(store)
                    item.decision_trace['noncompete_financial'] = financial
                    facts = prerequisite_facts(store)
                    missing = [f['label'] for f in facts if not f['covered']]
                    item.decision_trace['noncompete_prerequisite_assessment'] = {
                        'facts': facts, 'missing_facts': missing,
                        'status': 'UNRESOLVED' if missing else 'COMPLETE'}
                    if missing or financial['checks']:
                        from review_v2.element_resolution import conditional_element
                        message = ('竞业合理性核验尚缺：' + '、'.join(missing) + '；请补充核验该事实，不能据此直接认定竞业范围合理或违法。') if missing else ''
                        if missing == [PREREQUISITE_FACTS['non_compete.actual_access']]:
                            message = actual_access_verification(store)['instruction']
                        message = ' '.join([*financial['checks'], message]).strip()
                        item.decision_trace['priority_conditional_elements'] = [conditional_element(
                            'noncompete_reasonableness_prerequisites','竞业范围及补偿合理性判断前提',None,[],
                            prerequisite_fact='人员、秘密接触、范围、期限和补偿事实完整',verification_instruction=message)]
                        condition = item.decision_trace['priority_conditional_elements'][0]
                        condition['prerequisite_evidence'] = store.evidence(financial_facts, 'noncompete_reasonableness_prerequisites')
                        condition['source_clause_ids'] = list(dict.fromkeys(e['clause_id'] for e in condition['prerequisite_evidence']))
                        item.needs_manual_review = True
                        item.coverage_status = 'INSUFFICIENT_CONTEXT'
                        item.status = item.issue_type = '待核验'
                        item.action_suggestion = item.reasoning_summary = item.risk_point_description = message
        return
    from review_v2.priority_checklist_helpers import PROFILES
    from review_v2.lease_semantics import corpus_facts
    from review_v2.element_resolution import conditional_element
    by_node={i.node_id:i for i in items}
    consumer=by_node.get('employment_noncompete_adverse')
    if not consumer or consumer.coverage_status == '不适用':
        return
    if consumer.coverage_status == '风险条款':
        from review_v2.noncompete_reasonableness import assess
        assessment = assess(clauses)
        consumer.decision_trace['noncompete_proportionality'] = assessment
        consumer.needs_manual_review = True
        consumer.action_suggestion += ' 同时核实岗位、秘密接触、实际业务及地域范围，明确不支付补偿的风险不替代范围合理性核验。'
        return
    missing=[]
    for node in ('employment_noncompete_scope','employment_noncompete_term'):
        source=by_node.get(node)
        if not source or source.coverage_status=='不适用':
            continue
        facts=corpus_facts(clauses,PROFILES[node])
        missing += [e['proposition'] for e in PROFILES[node] if not facts[e['element_id']]]
    from review_v2.lease_semantics import requirement
    context = [
        requirement('noncompete_job_context', '劳动者具体岗位', r'(?:乙方|劳动者).{0,25}(?:担任|任职|岗位为|职务为)[^。；_]{2,40}'),
        requirement('noncompete_business_context', '公司实际业务覆盖范围', r'(?:甲方|公司).{0,15}(?:实际|主营|主要经营).{0,15}(?:业务|经营范围).{0,8}(?:为|包括|：|:)[^。；_]{3,80}'),
    ]
    context_facts = corpus_facts(clauses, context)
    missing += [e['proposition'] for e in context if not context_facts[e['element_id']]]
    consumer.decision_trace['reasonableness_context'] = {'facts': context_facts, 'ready_for_assessment': not missing}
    from review_v2.noncompete_reasonableness import assess
    assessment = assess(clauses)
    consumer.decision_trace['noncompete_proportionality'] = assessment
    if missing or assessment['checks']:
        message=('合理性判断所需事实尚不完整：'+'、'.join(missing)+'；不能据此直接认定范围合理或违法。' if missing else '')
        message += ' '.join(c['message'] + c.get('legal_basis', '') for c in assessment['checks'])
        condition=conditional_element('noncompete_reasonableness_prerequisites','竞业范围及补偿合理性判断前提',None,[],
            prerequisite_fact='人员、秘密接触、范围、期限及补偿事实足以判断合理性',verification_instruction=message)
        consumer.decision_trace['priority_conditional_elements']=[condition]
        consumer.decision_trace['noncompete_prerequisite_assessment']={'missing_facts':missing,'status':'UNRESOLVED'}
        consumer.needs_manual_review=True
        consumer.action_suggestion=message
        consumer.coverage_status='INSUFFICIENT_CONTEXT'
        consumer.status=consumer.issue_type='待核验'
        consumer.reasoning_summary=consumer.risk_point_description=message


def consistency_failures(items):
    by_node={i.node_id:i for i in items}
    consumer=by_node.get('employment_noncompete_adverse')
    scope=by_node.get('employment_noncompete_scope')
    if consumer and scope and not consumer.decision_trace.get('reasonableness_context', {}).get('ready_for_assessment'):
        if any(e.get('status')=='COVERED' and re.search(r'相称|合理性已确认', e.get('proposition', '')) for e in scope.coverage_elements):
            return [{'requirement':'REASONABLENESS_WITHOUT_PREREQUISITE_FACTS','root_cause':scope.item_id,
                     'failure_stage':'Semantic consistency','current_status':'FAIL'}]
    if not consumer or consumer.coverage_status in {'不适用','风险条款'}:
        return []
    incomplete=bool(consumer.decision_trace.get('noncompete_proportionality', {}).get('checks')) or any(by_node[n].coverage_status in {'部分覆盖','缺失','风险条款','待核验','INSUFFICIENT_CONTEXT'}
        for n in ('employment_noncompete_scope','employment_noncompete_term') if n in by_node)
    pending=any(e.get('status')=='CONDITION_UNRESOLVED' for e in consumer.coverage_elements)
    if incomplete and not (pending or consumer.coverage_status in {'待核验','INSUFFICIENT_CONTEXT','部分覆盖'}):
        return [{'requirement':'CROSS_RULE_PREREQUISITE_CONFLICT','root_cause':consumer.item_id,
                 'failure_stage':'Semantic consistency','current_status':'FAIL'}]
    return []
