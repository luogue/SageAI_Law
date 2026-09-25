"""Cross-clause legal-effect checks. Presence of an obligation is not safety.

The predicates bind operative waivers; comparison facts retain both parties'
source spans. No contract names, locations, article numbers or sample amounts.
"""
import re
from dataclasses import replace
from review_v2.priority_checklist_helpers import forbidden as F

THIRD_PARTY = r'第三[方人][^。\n]{0,100}(?:人员伤亡|人身|财产|损失)[^。\n]{0,40}(?:不承担|无需承担|免除)[^。\n]{0,15}(?:赔偿|责任)'
OWN_FAULT = r'(?:无论|不论|即使)[^。\n]{0,70}(?:过错|疏忽|脱岗|监控盲区|失职)[^。\n]{0,40}(?:不承担|无需承担|免责)'
EXIT = r'提前[^。\n]{0,90}解除[^。\n]{0,40}(?:无需承担|不承担)[^。\n]{0,15}违约责任'
DISPUTE = r'(?:申请|提交|提请)仲裁[^。\n]{0,100}(?:也可以|亦可|或者|或可|均可)[^。\n]{0,40}(?:法院|诉讼)|(?:法院|诉讼)[^。\n]{0,100}(?:也可以|亦可|或者)[^。\n]{0,40}仲裁'

SPECS = (
 ('common_delegated_service_waiver',40,'委托第三方服务后的责任排除',THIRD_PARTY,
  '《民法典》第593条、第941条',
  '删除以第三方资质或选聘程序免除服务方合同责任的约定；明确服务方对委托事项向服务接受方负责，内部追偿不影响对外责任。'),
 ('common_own_fault_waiver',41,'自身过错及人身财产损失的绝对免责',OWN_FAULT,
  '《民法典》第506条、第942条',
  '删除即使存在履职过错也一概免责的约定，按照实际履约、过错和因果关系承担责任，不得排除依法不得免除的赔偿责任。'),
 ('common_asymmetric_exit',42,'提前解除的通知、违约责任不对等',EXIT,
  '《民法典》第496条、第497条、第584条、第585条、第946条、第948条',
  '合理平衡双方提前解除的通知和交接义务，删除服务方无责退出安排；提前解除违约金应结合可证明损失、履行情况与剩余期限确定，并保留依法调整的权利。'),
 ('common_elective_dispute_routes',43,'仲裁与诉讼并列选择冲突',DISPUTE,
  '《仲裁法》（2025年修订，2026年3月1日起施行）第27条、第29条；仲裁法司法解释第7条',
  '明确选择仲裁或诉讼一种争议解决方式；选择仲裁时明确仲裁机构及事项，删除可直接就同一争议另行起诉的任选表述。'),
)
RELATION_REQUIREMENTS = {'common_delegated_service_waiver':'DELEGATED_PERFORMANCE'}

def relation_facts(clauses, relation):
    if relation != 'DELEGATED_PERFORMANCE':
        return []
    from review_v2.adverse_evidence import direct_evidence
    positive,_=direct_evidence(clauses, (
        r'(?:委托|转委托|交由)[^。；\n]{0,40}第三[方人][^。；\n]{0,30}(?:实施|履行|服务|办理|完成|保管)',
        r'第三[方人][^。；\n]{0,20}(?:受托|接受委托)[^。；\n]{0,30}(?:实施|履行|服务|办理|完成)',
    ), require_assertion=False)
    return positive

def applicability(node, clauses):
    relation=RELATION_REQUIREMENTS.get(node)
    if not relation:
        return None
    facts=relation_facts(clauses,relation)
    return {'applicable':bool(facts),'required_relation':relation,'evidence':facts,
            'reason':'已识别第三方受托履行关系。' if facts else '未识别第三方委托或受托履行关系；第三方受损或事故免责本身不触发本项。'}
CHECKPOINTS = tuple(replace(F('COMMON',n,node,title,('责任','解除','仲裁'),law,(pattern,),suggestion),
    applicable_if='正文存在对应责任排除、解除或争议解决安排时，核对整体法律效果。',
    legal_consequence_if_missing='该安排可能削弱实际履约保障或引发责任、程序效力争议，应按对应法律规则修订。')
    for node,n,title,pattern,law,suggestion in SPECS)

def evidence(node, clauses, *, check_applicability=True):
    condition=applicability(node,clauses)
    if check_applicability and condition and not condition['applicable']:
        return []
    spec=next(s for s in SPECS if s[0]==node)
    rows=[]
    for c in clauses:
        if c.section_type not in {'正式合同条款','附件'}: continue
        for part in re.finditer(r'[^。\n]+[。]?',c.text):
            quote=part.group().strip()
            match=re.search(spec[3],quote)
            if not match: continue
            from review_v2.adverse_evidence import proposition_polarity
            # A conditional loss event followed by an express waiver remains
            # adverse. PREVENTIVE describes sanctions, not "even if at fault,
            # no liability". Only a negated/prohibited waiver is protective.
            if proposition_polarity(quote,match.start(),match.end())=='NEGATED': continue
            if node=='common_elective_dispute_routes' and re.search(r'(?:裁决|仲裁协议)[^。]{0,15}(?:撤销|无效|不予执行)',quote): continue
            rows.append(dict(clause_id=c.clause_id,location=c.location,text=quote,quote=quote,
                             polarity='AFFIRMED',section_type=c.section_type,block_type=c.block_type))
    if node=='common_asymmetric_exit' and rows:
        # Keep the counterparty burden, not just the favourable exit sentence.
        for c in clauses:
            for part in re.finditer(r'[^。\n]+[。]?',c.text):
                quote=part.group().strip()
                if re.search(r'提前解除[^。\n]{0,100}(?:违约金|赔偿)|提前[^。\n]{0,20}通知[^。\n]{0,30}解除',quote) and not any(r['text']==quote for r in rows):
                    rows.append(dict(clause_id=c.clause_id,location=c.location,text=quote,quote=quote,
                                     polarity='AFFIRMED',section_type=c.section_type,block_type=c.block_type))
        # A bilateral no-liability exit is not an asymmetry.
        burdens=set(); exits=set()
        for r in rows:
            parties=re.findall(r'甲方|乙方|服务提供方|服务接受方|委托方|受托方',r['text'].split('提前')[0])
            if not parties: continue
            party=parties[-1]
            if re.search(r'(?:支付|承担)[^。\n]{0,35}违约金',r['text']): burdens.add(party)
            if re.search(r'(?:无需承担|不承担)[^。\n]{0,15}违约责任',r['text']): exits.add(party)
        if not any(a!=b for a in burdens for b in exits): return []
    return rows

def active(text):
    from review_v2.clause_parser import parse_contract_clauses
    clauses=parse_contract_clauses(text)
    from review_v2.service_scenarios import is_property_service
    selected=[c for c in CHECKPOINTS if evidence(c.node_id,clauses,check_applicability=False)]
    if not is_property_service(text):
        selected=[replace(c,legal_basis=re.sub(r'、?第9(?:41|42|46|48)条','',c.legal_basis)) for c in selected]
    return selected

def augment(checklist,text):
    existing={c.node_id for c in checklist}
    return tuple(checklist)+tuple(c for c in active(text) if c.node_id not in existing)

def reconcile(items, clauses):
    """Project the source-bound adverse outcome, including related core rules."""
    from review_v2.utility_supply_evidence import _set_adverse_if_found
    rows={c.node_id:evidence(c.node_id,clauses) for c in CHECKPOINTS}
    for item in items:
        node=item.node_id
        target = node if node in rows else 'common_asymmetric_exit' if node == 'termination_basis' else None
        if not target or not rows[target]: continue
        cp=next(c for c in CHECKPOINTS if c.node_id==target)
        quotes=list(dict.fromkeys(r['text'] for r in rows[target]))
        pattern='|'.join(re.escape(q) for q in quotes)
        reason=cp.title+'：'+ '；'.join(quotes)
        _set_adverse_if_found(item,clauses,assessment=(pattern,reason))
        # Replace the whole-clause candidates with the precise adverse spans.
        from review_v2.utility_supply_evidence import _evidence, _normalize_element_source_ids
        from review_v2.engine import _set_multi_element_state, _register_element_bound_core_claims
        elements=[]; bound=[]; requirements=[]
        by_id={c.clause_id:c for c in clauses}
        for index,row in enumerate(rows[target]):
            key=f'{target}_fact_{index+1}'
            ev=_evidence(by_id[row['clause_id']],item.node_id,[key])
            ev.update(text=row['text'],quote=row['text'],raw_text=row['text'])
            ev['evidence_id']+=f'-F{index+1}'; ev['evidence_claim_id']=ev['evidence_id']
            bound.append(ev)
            action=cp.suggested_clause.removeprefix('建议').rstrip('。')
            if target=='common_asymmetric_exit':
                action=('删除服务方无责提前退出安排，设置与对方合理对等的通知期限、违约责任及交接保障'
                        if re.search(r'(?:无需承担|不承担)[^。]{0,15}违约责任',row['text']) else
                        '结合可证明损失、实际履行及剩余期限调整提前解除违约金，合理平衡双方通知义务，保留依法调整违约金的权利')
            requirement={'element_id':key,'proposition':row['text'],'semantic_patterns':[re.escape(row['text'])], 'evidence_unit':'clause','recommendation_action':action}
            requirements.append(requirement)
            elements.append({**requirement,'status':'ADVERSE','presence_status':'COVERED','direction':'ADVERSE','risk_relevant':True,'bound_evidence_ids':[ev['evidence_id']]})
        item.evidence_clauses=bound
        item.decision_trace['semantic_requirements']=requirements
        item.decision_trace.pop('element_evidence_truth',None)
        _set_multi_element_state(item,elements,bound)
        _normalize_element_source_ids(item,bound)
        _register_element_bound_core_claims(item)
        item.suggested_clause_example=cp.suggested_clause
        from review_v2.service_scenarios import is_property_service
        item.legal_basis_index=cp.legal_basis if is_property_service('\n'.join(c.text for c in clauses)) else re.sub(r'、?第9(?:41|42|46|48)条','',cp.legal_basis)
        item.risk_group=target
        item.decision_trace['finding_parent_group']=target
        item.decision_trace['effect_source_quotes']=quotes
        item.decision_trace['effect_node']=target
        item.decision_trace['priority_positive_adverse_verification']={'source_clause_ids':[r['clause_id'] for r in rows[target]]}

def consistency_failures(items):
    failures=[]
    for i in items:
        for fact in i.decision_trace.get('service_positive_source_facts',[]):
            element=next((e for e in i.coverage_elements if e.get('element_id')==fact['element_id']),{})
            if element.get('status')=='MISSING' or i.coverage_status in {'缺失','MISSING'}:
                failures.append({'requirement':'POSITIVE_SERVICE_FACT_REPORTED_ABSENT','root_cause':i.item_id+':'+fact['element_id']})
        quotes=i.decision_trace.get('effect_source_quotes',[])
        if quotes and i.coverage_status not in {'风险条款','RISK_CLAUSE','RISK'}:
            failures.append({'requirement':'ADVERSE_LEGAL_EFFECT_LOST','root_cause':i.item_id})
        if quotes:
            rendered='\n'.join(str(r.get('quote') or r.get('text') or '') for r in i.evidence_clauses if r.get('source_type')!='SEARCH_AUDIT')
            if any(re.sub(r'\s+','',q) not in re.sub(r'\s+','',rendered) for q in quotes):
                failures.append({'requirement':'ADVERSE_EFFECT_SOURCE_OMITTED','root_cause':i.item_id})
    return failures
