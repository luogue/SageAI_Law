"""Noncompete temporal roles and evidence prerequisites; no sample literals."""
import re

DURATION = r'[一二两三四五六七八九十百\d]+\s*个?\s*(?:月|年|日|天)'
TERM_PATTERNS = (
    r'(?:自)?劳动合同(?:解除|终止)之日起\s*' + DURATION + r'内[^。；\n]{0,50}不得[^。；\n]{0,40}(?:竞争|同类|类似)',
    r'竞业(?:限制|禁止)(?:持续)?期(?:限)?\s*(?:为|是|：|:)\s*' + DURATION,
    r'离职后\s*' + DURATION + r'(?:内)?[^。；\n]{0,12}(?:承担|履行|遵守)竞业(?:限制|禁止)',
    r'(?:离职|解除劳动合同|终止劳动合同)后[^。；\n]{0,12}竞业(?:限制|禁止)(?:期(?:限)?)?\s*(?:为|：|:)?\s*' + DURATION,
)
DEFINED_TERM = r'之日起(?:的)?\s*' + DURATION + r'内[^。；\n]{0,35}(?:不得|履行|承担)'


def temporal_roles(clauses):
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
