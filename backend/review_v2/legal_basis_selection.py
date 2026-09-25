"""Explicit proposition authority selection, separate from contract fact coverage."""
import re

TOPICS={
 'custody_fee_obligation':('寄存人应当按照约定向保管人支付保管费','第889条','DIRECT_SUPPORT'),
 'liquidated_damages_calculation':('当事人可以约定违约金及因违约产生的损失赔偿额计算方法','第585条','DIRECT_SUPPORT'),
 'general_breach_liability':('不履行或履行不符合约定时的一般违约责任','第577条','PARTIAL_SUPPORT'),
 'remuneration_payment':('有偿保管费用按约定期限支付；支付期限不明时的处理', '第902条','DIRECT_SUPPORT'),
 'performance_cooperation':('依约全面履行并按诚信原则履行通知、协助等义务；具体费用及凭证安排属于合同细化','第509条','PARTIAL_SUPPORT'),
 'unclear_contract_terms':('报酬、费用承担及履行方式约定不明时通过补充协议、相关条款或交易习惯确定','第510条','PARTIAL_SUPPORT'),
 'divisible_lien_scope':('留置财产为可分物时，其价值应当相当于债务金额','第450条','DIRECT_SUPPORT'),
 'lien_realization_period':('留置后的债务履行期限及到期未履行后的折价、拍卖、变卖程序；不等于法定事前通知义务','第453条','DIRECT_SUPPORT'),
 'custody_lien_source':('欠付保管费或其他费用时的保管人留置权来源，不直接规定费用项目、金额或凭证','第903条','DIRECT_SUPPORT'),
 'lien_same_relationship':('留置动产与债权属于同一法律关系，企业之间留置除外','第448条','DIRECT_SUPPORT'),
}

# Reusable legal propositions. These describe legal effects, not report verdicts.
TOPICS.update({
 'unclear_custody_fee_default':('保管费约定不明且按补充确定规则仍不能确定时视为无偿保管','第889条','DIRECT_SUPPORT'),
 'custody_definition':('接受交付、保管并返还保管物构成保管合同','第888条','DIRECT_SUPPORT'),
 'custody_delivery_formation':('保管合同自交付时成立，另有约定除外','第890条','DIRECT_SUPPORT'),
 'custody_receipt':('交付时保管人应出具保管凭证，另有交易习惯除外','第891条','DIRECT_SUPPORT'),
 'proper_custody':('保管人应妥善保管保管物','第892条','DIRECT_SUPPORT'),
 'custody_method':('约定保管场所或方法，除紧急情况或维护寄存人利益外不得擅自改变','第892条','DIRECT_SUPPORT'),
 'defect_disclosure':('寄存人应告知保管物瑕疵和特殊保管需求，未告知时按法定条件分配损失责任','第893条','DIRECT_SUPPORT'),
 'unauthorized_subcustody':('保管人不得擅自转交第三人保管，另有约定除外；违反规定转交并造成损失应赔偿','第894条','DIRECT_SUPPORT'),
 'authorized_subcustody_liability':('因第三人原因违约时仍向合同相对方承担违约责任，内部争议依法另行处理','第593条','DIRECT_SUPPORT'),
 'custody_loss_liability':('保管不善造成毁损灭失应赔偿；无偿保管可依法证明无故意或重大过失而免责','第897条','DIRECT_SUPPORT'),
 'valuable_declaration':('货币、有价证券及贵重物品应声明并由保管人验收或封存；未声明可按一般物品赔偿','第898条','DIRECT_SUPPORT'),
 'retrieval_right':('寄存人可随时领取；期限不明时保管人可请求领取，约定期限时不得无特别事由请求提前领取','第899条','DIRECT_SUPPORT'),
 'return_original_fruits':('期限届满或提前领取时，保管人返还原物及其孳息','第900条','DIRECT_SUPPORT'),
 'fungible_return':('货币返还同种类同数量；其他可替代物可约定返还同种类品质数量','第901条','DIRECT_SUPPORT'),
 'subject_description':('合同内容通常包括标的、数量等约定；不等于每个字段缺失即无效','第470条','DIRECT_SUPPORT'),
 'written_attachments':('书面形式包括能够有形表现所载内容的数据电文等形式','第469条','STRONG_RELATED'),
 'interpretation':('解释争议条款应结合词句、相关条款、行为性质目的、习惯及诚信原则','第466条','STRONG_RELATED'),
 'intent_interpretation':('有相对人的意思表示按词句、相关条款、行为性质目的、习惯及诚信原则解释','第142条','STRONG_RELATED'),
 'state_records':('照片、视频、交接状态和事故记录有助协作及证明；本条不直接规定具体留档清单','第509条','STRONG_RELATED'),
 'packaging_assistance':('包装及交付协助可按约定与诚信协作原则细化；本条不直接规定具体包装标准','第509条','STRONG_RELATED'),
 'value_assessment':('违约损失赔偿范围与可预见性；价值确认可作为损失计算证据，不是法定声明全部物品价值义务','第584条','STRONG_RELATED'),
 'pre_delivery_risk':('交付前风险及迟延接收应结合当事人具体义务与违约判断；本条不统一规定全部交付前风险归属','第577条','STRONG_RELATED'),
 'retrieval_procedure':('领取身份核验、签收和具体通知流程属于依约履行与协作细化','第509条','STRONG_RELATED'),
 'overdue_retrieval':('违反约定领取义务的责任需结合约定、违约及损失判断，并非一逾期即自动欠付固定费用','第577条','DIRECT_SUPPORT'),
 'extra_fee_arrangement':('逾期产生额外费用的项目和计费方式依合同安排判断，本条仅提供依约履行的一般支持','第509条','STRONG_RELATED'),
 'overdue_payment_context':('保管费支付期限仅为背景，不直接规定逾期领取责任或额外费用','第902条','BACKGROUND_ONLY'),
 'overdue_retrieval_context':('随时领取及请求领取规则是逾期领取背景，并不直接规定逾期加收费用或处置费','第899条','BACKGROUND_ONLY'),
 'necessary_disposal_costs':('必要处置费用需另核对处置依据、必要性及约定；当前命题未绑定一项自动由寄存人承担全部处置费的直接法条','','NO_DIRECT_AUTHORITY'),
 'income_agreement':('消费保管利息、收益是否支付须结合约定判断，返还同种类货币不当然产生利息义务','第509条','STRONG_RELATED'),
 'attachment_precedence':('正文附件冲突的解释可结合相关条款；不直接创设统一的附件优先顺序','第466条','STRONG_RELATED'),
})

AUTHORITY_TEXTS={
 '第142条':'有相对人的意思表示的解释，应当按照所使用的词句，结合相关条款、行为的性质和目的、习惯以及诚信原则，确定意思表示的含义。无相对人的意思表示的解释，不能完全拘泥于所使用的词句，而应当结合相关条款、行为的性质和目的、习惯以及诚信原则，确定行为人的真实意思。',
 '第466条':'当事人对合同条款的理解有争议的，应当依据本法第一百四十二条第一款的规定，确定争议条款的含义。合同文本采用两种以上文字订立并约定具有同等效力的，对各文本使用的词句推定具有相同含义。各文本使用的词句不一致的，应当根据合同的相关条款、性质、目的以及诚信原则等予以解释。',
 '第469条':'当事人订立合同，可以采用书面形式、口头形式或者其他形式。书面形式是合同书、信件、电报、电传、传真等可以有形地表现所载内容的形式。以电子数据交换、电子邮件等方式能够有形地表现所载内容，并可以随时调取查用的数据电文，视为书面形式。',
 '第470条':'合同的内容由当事人约定，一般包括下列条款：（一）当事人的姓名或者名称和住所；（二）标的；（三）数量；（四）质量；（五）价款或者报酬；（六）履行期限、地点和方式；（七）违约责任；（八）解决争议的方法。当事人可以参照各类合同的示范文本订立合同。',
 '第888条':'保管合同是保管人保管寄存人交付的保管物，并返还该物的合同。寄存人到保管人处从事购物、就餐、住宿等活动，将物品存放在指定场所的，视为保管，但是当事人另有约定或者另有交易习惯的除外。',
 '第890条':'保管合同自保管物交付时成立，但是当事人另有约定的除外。',
 '第891条':'寄存人向保管人交付保管物的，保管人应当出具保管凭证，但是另有交易习惯的除外。',
 '第892条':'保管人应当妥善保管保管物。当事人可以约定保管场所或者方法。除紧急情况或者为维护寄存人利益外，不得擅自改变保管场所或者方法。',
 '第893条':'寄存人交付的保管物有瑕疵或者根据保管物的性质需要采取特殊保管措施的，寄存人应当将有关情况告知保管人。寄存人未告知，致使保管物受损失的，保管人不承担赔偿责任；保管人因此受损失的，除保管人知道或者应当知道且未采取补救措施外，寄存人应当承担赔偿责任。',
 '第894条':'保管人不得将保管物转交第三人保管，但是当事人另有约定的除外。保管人违反前款规定，将保管物转交第三人保管，造成保管物损失的，应当承担赔偿责任。',
 '第897条':'保管期内，因保管人保管不善造成保管物毁损、灭失的，保管人应当承担赔偿责任。但是，无偿保管人证明自己没有故意或者重大过失的，不承担赔偿责任。',
 '第898条':'寄存人寄存货币、有价证券或者其他贵重物品的，应当向保管人声明，由保管人验收或者封存；寄存人未声明的，该物品毁损、灭失后，保管人可以按照一般物品予以赔偿。',
 '第899条':'寄存人可以随时领取保管物。当事人对保管期限没有约定或者约定不明确的，保管人可以随时请求寄存人领取保管物；约定保管期限的，保管人无特别事由，不得请求寄存人提前领取保管物。',
 '第900条':'保管期限届满或者寄存人提前领取保管物的，保管人应当将原物及其孳息归还寄存人。',
 '第901条':'保管人保管货币的，可以返还相同种类、数量的货币；保管其他可替代物的，可以按照约定返还相同种类、品质、数量的物品。',
 '第593条':'当事人一方因第三人的原因造成违约的，应当依法向对方承担违约责任。当事人一方和第三人之间的纠纷，依照法律规定或者按照约定处理。',
}

# Legal metadata, not contract-text keyword matching. Topic order breaks ties only.
ARTICLE_METADATA={article:{'article_id':article,'legal_domain':'contract',
    'contract_type':'general','proposition_tags':[t for t,p in TOPICS.items() if p[1]==article],
    'normative_object':next(p[0] for p in TOPICS.values() if p[1]==article),
    'trigger_conditions':[], 'effect_type':'statutory_rule','specificity_level':'SPECIAL'}
    for article in {p[1] for p in TOPICS.values() if p[1]}}
for article in ('第889条','第902条','第903条'):
    ARTICLE_METADATA[article].update(legal_domain='custody',contract_type='custody')
ARTICLE_METADATA['第585条'].update(legal_domain='breach',effect_type='agreed_damages',
    proposition_tags=['liquidated_damages_calculation','liquidated_damages','agreed_damages','damages_calculation_method','damages_adjustment'])
for article in ('第509条','第577条','第593条','第584条','第470条','第469条','第142条','第466条'):
    ARTICLE_METADATA[article]['specificity_level']='GENERAL'
for article in AUTHORITY_TEXTS:
    if 888 <= int(article[1:-1]) <= 903:
        ARTICLE_METADATA[article].update(legal_domain='custody',contract_type='custody')
ARTICLE_METADATA['第510条'].update(specificity_level='SUPPLEMENTARY',trigger_conditions=['unclear_terms'])

def rank_candidates(candidates):
    """An applicable direct special provision always outranks general/background law."""
    return sorted(candidates,key=lambda c:-c['relevance_score'])

RELATION={'DIRECT_SUPPORT':'DIRECT','PARTIAL_SUPPORT':'STRONG_RELATED','STRONG_RELATED':'STRONG_RELATED',
          'BACKGROUND_ONLY':'BACKGROUND','NO_DIRECT_AUTHORITY':'IRRELEVANT'}

def directness_score(relation,specificity):
    if relation=='DIRECT':return 1.0 if specificity=='SPECIAL' else 0.8
    if relation=='STRONG_RELATED':return 0.7 if specificity=='SPECIAL' else 0.6
    return 0.3 if relation=='BACKGROUND' else 0.0

def unclear_terms_trigger(item):
    # Consume existing adjudication; never extract/reclassify facts here.
    status=getattr(item,'coverage_status','')
    status=getattr(status,'value',status)
    return status in ('PARTIAL','MISSING','部分覆盖','缺失','完全缺失')

def select(item,checkpoint):
    from review_v2.quality4 import validate_legal_citation
    topics=checkpoint.legal_basis_topics
    if not topics:return
    trace=item.decision_trace['legal_basis_runtime_trace']
    articles=list(dict.fromkeys([TOPICS[t][1] for t in topics if TOPICS[t][1]]+re.findall(r'第\d+条',checkpoint.legal_basis)))
    candidates=[]
    unclear=unclear_terms_trigger(item)
    status=getattr(item,'coverage_status','')
    status=getattr(status,'value',status)
    applicable=status not in ('不适用','NOT_APPLICABLE','N/A')
    for article in articles:
        matched=[t for t in topics if TOPICS[t][1]==article]
        validation=validate_legal_citation('中华人民共和国民法典',article)
        metadata=ARTICLE_METADATA.get(article,{})
        specificity=metadata.get('specificity_level','UNMAPPED')
        domain=getattr(checkpoint,'legal_basis_domain','')
        article_domain=metadata.get('contract_type','general')
        domain_match=not domain or article_domain=='general' or article_domain==domain
        triggered=applicable and domain_match and (not metadata.get('trigger_conditions') or unclear)
        relations=[RELATION[TOPICS[t][2]] for t in matched]
        relation=max(relations,key=lambda r:directness_score(r,specificity)) if relations else 'IRRELEVANT'
        score=directness_score(relation,specificity)
        if specificity=='SUPPLEMENTARY':score=min(score,0.3)
        same_domain=bool(domain and article_domain==domain and specificity=='SPECIAL')
        if same_domain and relation in ('DIRECT','STRONG_RELATED'):score+=0.01
        # Main proposition precedes mechanism background across equal relations.
        # This bounded tie weight cannot invert any directness/specificity band.
        if matched:score-=0.02*min(min(topics.index(t) for t in matched),4)
        if not triggered:score=0.1 if matched else 0
        candidates.append({'article':article,'matched_propositions':matched,
            'metadata':metadata,'trigger_satisfied':triggered,'eligible':bool(matched) and triggered and relation in ('DIRECT','STRONG_RELATED'),
            'basis_relation':relation,'specificity':specificity,'directness':relation,
            'same_contract_domain':same_domain,'domain_match':domain_match,
            'relevance_score':score,
            'score_semantics':'DIRECT_SPECIAL > DIRECT_GENERAL > STRONG_RELATED_SPECIAL > STRONG_RELATED_GENERAL > BACKGROUND > IRRELEVANT',
            'reason':('补充规则前提未触发，仅保留候选背景，不进入最终依据' if matched and not triggered else
                      '明确法律命题对应；按直接性及专门性排序，并非词频相似度' if matched else '旧配置候选，但没有目标法律命题对应，不选择'),
            'authority_validation':validation})
    candidates=rank_candidates(candidates)
    selected=[c['article'] for c in candidates if c['eligible'] and c['authority_validation']['status']=='CURRENT']
    selected=list(dict.fromkeys(selected))
    value='；'.join('《中华人民共和国民法典》'+a for a in selected)
    primary=[c['article'] for c in candidates if c['article'] in selected and c['basis_relation']=='DIRECT'] or selected[:1]
    trace.update(candidate_articles=candidates,primary_basis=primary,secondary_basis=[a for a in selected if a not in primary],selected_basis=value,
        legal_propositions=[{'id':t,'proposition':TOPICS[t][0],'article':TOPICS[t][1],'support_type':TOPICS[t][2],
                            'basis_relation':RELATION[TOPICS[t][2]],'selected':TOPICS[t][1] in selected} for t in topics],
        supplementary_trigger={'unclear_terms':unclear,'source':'existing coverage_status; no fact mutation'})
    trace['stages'].append({'STAGE':'PROPOSITION_SELECTION','SOURCE_FILE':__file__,'SOURCE_FIELD':'ReviewCheckpoint.legal_basis_topics -> ReviewItemResult.legal_basis_index',
        'VALUE_BEFORE':item.legal_basis_index,'VALUE_AFTER':value})
    item.legal_basis_index=value
    trace['selection_complete']=len(selected)==len([c for c in candidates if c['eligible']])
    # Fold ordering invariants into the existing fail-closed selection gate.
    specials=[c['article'] for c in candidates if c['eligible'] and c['basis_relation']=='DIRECT' and c['metadata'].get('specificity_level')=='SPECIAL']
    invariant=not specials or bool(selected and selected[0] in specials)
    trace['special_over_general_passed']=invariant
    trace['selection_complete']=trace['selection_complete'] and invariant
    trace['special_over_general_violation']=not invariant
    trace['audit_explanation']=('规则已由既有适用性判断为不适用；不要求当前合同适用候选条文。' if not applicable else
        '直接特别法已优先；一般或弱关联条文未替代特别法。' if specials else
        '当前命题未匹配适用直接特别法；一般依据可保留，具体程序不宣称有直接法条。')

def specs(item):
    trace=item.decision_trace.get('legal_basis_runtime_trace',{})
    if 'selected_basis' not in trace:return None
    return [{'proposition':p['proposition'],'claim_type':'STATUTORY_RULE',
             'maximum_support_type':'PARTIAL_SUPPORT' if p['basis_relation']=='STRONG_RELATED' else p['support_type'],
             'references':[{'law_name':'中华人民共和国民法典','article':p['article'],'paragraph':''}]}
            for p in trace['legal_propositions'] if p['selected']]

def audit_result(item):
    """Validate the actual post-citation result, independently of sorting code."""
    trace=item.decision_trace.get('legal_basis_runtime_trace',{})
    candidates=trace.get('candidate_articles',[])
    selected=re.findall(r'第\d+条',item.legal_basis_index or '')
    direct_special=[c['article'] for c in candidates if c['eligible'] and c['basis_relation']=='DIRECT' and c['specificity']=='SPECIAL']
    missing_special=[a for a in direct_special if a not in selected]
    violation=bool(missing_special or (direct_special and (not selected or selected[0] not in direct_special)))
    weak=[]
    for claim in getattr(item,'legal_references',[]) or []:
        candidate=next((c for c in candidates if c['article']==claim.get('article')),None)
        proposition=next((p for p in trace.get('legal_propositions',[]) if p['proposition']==claim.get('proposition') and p['article']==claim.get('article')),None)
        relation=proposition['basis_relation'] if proposition else candidate['basis_relation'] if candidate else None
        if relation and relation!='DIRECT' and claim.get('support_type')=='DIRECT_SUPPORT':
            weak.append(claim.get('claim_id'))
    return {'rule_id':item.item_id,'rule_name':trace.get('runtime_rule_metadata',{}).get('title',''),
        'required_elements':trace.get('required_elements',[]),'legal_propositions':trace.get('legal_propositions',[]),
        'current_primary_basis':trace.get('primary_basis',[]),'current_secondary_basis':trace.get('secondary_basis',[]),
        'candidate_articles':candidates,'has_applicable_direct_special':bool(direct_special),
        'general_or_background_only':bool(selected) and not any(c['article'] in selected and c['specificity']=='SPECIAL' for c in candidates),
        'special_over_general_violation':violation,'missing_special':missing_special,
        'weak_related_as_direct':weak,'explanation':trace.get('audit_explanation','UNMAPPED'),
        'status':'BLOCKED' if violation or weak or not trace.get('selection_complete') else 'REPORT_READY'}
