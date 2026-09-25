"""Final guarantee fact consumers: statutory defaults, supplied documents and adverse text."""
from copy import deepcopy
import re
from review_v2.lease_semantics import requirement, corpus_facts
from review_v2.guarantee_scenarios import extract, applicable, CONDITIONS
from review_v2.requirement_kinds import partition

DEFAULTS={
    'assignment_notice_to_guarantor':('第696条','债权转让未通知保证人的，对保证人不发生效力；未复述该法定效果不构成合同缺陷。'),
    'guarantee_invalid_fault_liability':('第682条','保证无效后的过错责任由法定规则补足，未复述不构成合同缺陷。'),
    'guarantee_period_no_suspend_interrupt':('第692条','保证期间不发生中止、中断和延长，未复述不构成合同缺陷。'),
    'guarantor_subrogation_right':('第700条','除当事人另有约定外，保证人承担责任后享有法定追偿及债权人对债务人的权利，但不得损害债权人利益。'),
}
CONFLICTS={
    'assignment_notice_to_guarantor': requirement('assignment_notice_conflict','约定债权转让无需通知即可约束保证人',
        r'(?:债权.{0,15}转让|转让.{0,15}债权)[^。；]{0,45}(?:无需|无须|不必)通知保证人[^。；]{0,35}(?:生效|发生效力|承担|约束)'),
    'guarantee_period_no_suspend_interrupt': requirement('guarantee_period_conflict','约定保证期间中断、中止或自动延长',
        r'保证期间[^。；]{0,30}(?:自动延长|重新起算|可以中断|可以中止|因催收而中断|随催收延长)'),
    'guarantor_subrogation_right': requirement('guarantee_subrogation_waiver','限制或放弃代偿后的代位权',
        r'保证人[^。；]{0,35}(?:放弃|不得行使|不享有|无权行使)[^。；]{0,20}(?:代位权|代位享有|债权人对债务人的权利)'),
    'guarantee_invalid_fault_liability': requirement('guarantee_invalid_no_fault','保证无效后排除过错因素仍要求全部责任',
        r'保证[^。；]{0,10}无效[^。；]{0,30}(?:无论.{0,8}过错|不论.{0,8}过错)[^。；]{0,30}(?:全部|全额)'),
}
CONFLICTS['guarantor_subrogation_right']['excluded_patterns']=[r'不得放弃|不放弃|未放弃']
CONFLICTS['guarantee_period_no_suspend_interrupt']['excluded_patterns']=[r'保证期间不(?:得|会|发生|可以)']


def bind_adverse(item,specs,evidence,reason,suggestion,level='中'):
    item.coverage_status=item.status=item.issue_type='风险条款'
    item.coverage_presence='PRESENT'
    item.risk_status='ADVERSE'
    item.risk_level=level
    item.needs_manual_review=False
    item.risk_point_description=item.reasoning_summary=reason
    item.legal_consequence_if_missing=reason
    item.suggested_clause_example=item.action_suggestion=suggestion
    item.evidence_clauses=deepcopy(evidence)
    item.evidence_location='；'.join(dict.fromkeys(e['location'] for e in evidence))
    item.risk_group=item.node_id+'_adverse'
    item.decision_trace.update(semantic_requirements=specs,review_mode='ABSENCE_REQUIRED',
        review_polarity='NEGATIVE_CLAUSE_CHECK',review_nature='CONTRACTUAL_REQUIREMENT',
        finding_parent_group=item.risk_group,
        negative_check_basis={'method':'DIRECT_ADVERSE_PREDICATE_WITH_SHARED_PARTY_FACT'},
        underlying_risk_identity={'fact':item.risk_group,'scope':'primary_contract','remedy':'correct_adverse_clause'})
    item.decision_trace.pop('non_contractual_review',None)
    for e in item.evidence_clauses:e.update(entailment_status='SUPPORTS',evidence_semantics='ACTUAL_RISK_CLAUSE',affirmative_risk_evidence=True)


def pending(item,requirements,instruction):
    _,assessments=partition([dict(element_id=key,proposition=label,requirement_kind='EXTERNAL_VERIFICATION',
        verification_instruction=instruction,verification_priority='MEDIUM') for key,label in requirements])
    item.decision_trace['requirement_kind_assessments']=assessments
    item.decision_trace['review_nature']='CONTRACTUAL_REQUIREMENT'
    item.coverage_status=item.status='INSUFFICIENT_CONTEXT'
    item.issue_type='待核验'
    item.needs_manual_review=True
    item.risk_level='低'
    item.risk_point_description=item.reasoning_summary=item.legal_consequence_if_missing=instruction
    item.action_suggestion=instruction
    item.suggested_clause_example=''
    item.related_risks=[]
    item.applicability.update(applicable=True,status='APPLICABLE',triggered=True)


def apply(items,clauses,text):
    from review_v2.engine import _set_item_not_applicable,_set_item_pass,_apply_review_nature_outcomes
    f=extract(text)
    shared=next((i.decision_trace.get('guarantee_shared_facts') for i in items if i.decision_trace.get('guarantee_shared_facts')), {})
    shared.update(f)
    shared['signature_party_type_consistency']='MISMATCH' if shared.get('signature_mismatches') else 'UNKNOWN' if f['guarantee_party_type']=='UNKNOWN' else 'CONSISTENT'
    for item in items:
        item.decision_trace['guarantee_shared_facts']=shared
        active=applicable(item.node_id,f)
        if active is not None:
            item.applicable_if=CONDITIONS[item.node_id]
            item.applicability.update(condition=item.applicable_if,applicable=active,triggered=active,status='APPLICABLE' if active else 'NOT_APPLICABLE')
            if not active:
                _set_item_not_applicable(item,item.applicable_if+'；本合同未触发。')
                item.related_risks=[]
                item.suggested_clause_example=''
                item.needs_manual_review=False
                continue
        if item.node_id in DEFAULTS:
            spec=CONFLICTS[item.node_id]
            evidence=corpus_facts(clauses,[spec])[spec['element_id']]
            if evidence:
                bind_adverse(item,[spec],evidence,'已有条款偏离法定默认机制，需要评估并调整。','建议按实际责任安排调整该约定，保留法定责任边界及当事人依法可作的安排。')
            elif item.node_id=='assignment_notice_to_guarantor' and (notice_evidence:=corpus_facts(clauses,[notice_spec:=requirement('assignment_notice_obligation','债权转让通知保证人',
                    r'(?:债权.{0,15}转让|转让.{0,15}债权)[^。；]{0,60}(?<!无)(?:应|须|需|必须)[^。；]{0,12}通知保证人',
                    r'(?:债权.{0,15}转让|转让.{0,15}债权)[^。；]{0,40}未经通知保证人[^。；]{0,25}不发生效力')])[notice_spec['element_id']]):
                _set_item_pass(item,[],'合同明确约定债权转让通知保证人。','通知义务已有正文支持。')
                item.decision_trace['semantic_requirements']=[notice_spec]
                item.evidence_clauses=notice_evidence
                item.evidence_location='；'.join(dict.fromkeys(e['location'] for e in notice_evidence))
                item.legal_consequence_if_missing='本项通知义务已明确，无独立条款缺口。'
            else:
                article,protection=DEFAULTS[item.node_id]
                item.decision_trace['review_nature']='LEGAL_REMINDER'
                _apply_review_nature_outcomes([item])
                item.reasoning_summary=item.risk_point_description='适用《民法典》'+article+'。'+protection+'无需修改。'
                item.legal_consequence_if_missing=protection
                item.decision_trace['requirement_kind_assessments']=partition([dict(element_id=item.node_id+'_default',proposition=item.title,
                    requirement_kind='STATUTORY_DEFAULT',statutory_protection=protection,legal_basis='《民法典》'+article)])[1]
                if item.node_id=='assignment_notice_to_guarantor':
                    support=requirement('general_notice_context','统一通知机制（辅助证据，不等于专项通知义务）',r'(?:全部|所有)通知[^。]{0,100}(?:快递|邮件|送达)')
                    item.decision_trace['supporting_notice_context']=corpus_facts(clauses,[support])[support['element_id']]
        if item.node_id=='assignment_no_increase_scope':
            spec=requirement('assignment_original_scope','债权转让后保证责任仍限于原范围',
                r'(?:债权.{0,15}转让|转让.{0,20}债权)[^。；]{0,50}(?<!不)在(?:原|本合同)(?:保证|担保)(?:的)?范围内继续承担',
                r'债权转让不改变保证范围|保证责任不因债权转让而扩大',
                r'受让人取得的保证权利以原保证范围为限')
            evidence=corpus_facts(clauses,[spec])[spec['element_id']]
            item.decision_trace['semantic_requirements']=[spec]
            if evidence:
                _set_item_pass(item,[],'债权转让后的保证责任限于原合同范围。','转让不扩大保证责任的原文边界已明确。')
                item.evidence_clauses=evidence
                item.evidence_location='；'.join(dict.fromkeys(e['location'] for e in evidence))
                item.legal_consequence_if_missing='保证责任边界已有明确约定，无本项缺失。'
        if item.node_id=='no_damage_creditor_interest':
            spec=requirement('recourse_creditor_priority','追偿不妨碍债权实现或债权人优先受偿',
                r'保证人[^。]{0,160}追偿[^。]{0,120}(?:优先偿付|优先受偿)[^。]{0,35}债权人',
                r'(?:追偿|代位)[^。]{0,60}(?:不得损害债权人利益|不影响债权人债权实现|劣后于债权人剩余债权)',
                r'不影响债务人[^。]{0,25}向债权人偿还[^。]{0,50}追偿')
            evidence=corpus_facts(clauses,[spec])[spec['element_id']]
            item.decision_trace['semantic_requirements']=[spec]
            if evidence:
                _set_item_pass(item,[],'已约定追偿与债权人剩余债权的受偿顺序。','原文支持债权人优先受偿。')
                item.legal_consequence_if_missing='原文已明确追偿不得影响债权人受偿，不存在本项独立条款缺口。'
                item.evidence_clauses=evidence
                item.evidence_location='；'.join(dict.fromkeys(e['location'] for e in evidence))
        if item.node_id=='guarantor_identity_capacity' and shared.get('signature_mismatches'):
            specs=[];evidence=[];suggestions=[]
            for p in f['guarantors']:
                if not any(m['party']==p['name'] for m in shared['signature_mismatches']):continue
                signer=re.escape(p['side'])+r'\s*[:：][^\n]*'
                spec=requirement('signature_template_'+str(len(specs)),'已识别保证人类型与签署栏身份字段冲突',
                    signer+r'(?:公章|法定代表人)' if p['party_type']=='NATURAL_PERSON' else signer+r'(?:签字|签名)')
                specs.append(spec);evidence+=corpus_facts(clauses,[spec])[spec['element_id']]
                suggestions.append(f'将签署栏改为“{p["side"]}（保证人）：{p["name"]}（签字/捺印）”，删除法人专用的公章、法定代表人字段。' if p['party_type']=='NATURAL_PERSON' else '公司保证人应使用公司签署栏，列明盖章及代表人签署身份。')
            bind_adverse(item,specs,evidence,'保证人主体已明确，但签署栏使用了与该主体类型不一致的字段，应修改签署模板。','；'.join(suggestions),level='低')
            item.decision_trace['verified_document_defect']={'kind':'PARTY_SIGNATURE_TYPE_CONFLICT',
                'confirmed':True,'evidence_clause_ids':[e['clause_id'] for e in evidence],
                'repair':'CORRECT_SIGNING_FIELDS','external_fact_required':False}
            item.legal_consequence_if_missing='可能造成签署形式与主体身份表达混乱。'
            item.decision_trace['risk_narrative_components']={
                'judgment':'发现可直接修正的签署模板错误，建议修改。',
                'issue':item.risk_point_description,
                'consequence':item.legal_consequence_if_missing,
                'exposure':'合同文本已明确保证人身份，本项主要属于签署模板规范性风险。'}
            item.reasoning_summary=item.decision_trace['risk_narrative_components']['judgment']
        if item.node_id=='guarantee_attachment_integrity':
            inventory=f['attachment_inventory']
            if inventory['status']=='VERIFIED':
                _set_item_pass(item,[],'上传文件包含可核验的独立附件正文。','附件实际正文已提供。')
                spec=requirement('provided_annex_body','上传的独立附件包含实质权利义务正文',r'(?:本金|价款|利息|履行义务|违约责任|偿还)')
                spec['required_section_types']=['附件']
                item.decision_trace['semantic_requirements']=[spec]
                item.evidence_clauses=corpus_facts(clauses,[spec])[spec['element_id']]
            else:
                spec=requirement('annex_reference_only','正文引用主合同或附件，尚不证明文件提供',r'主合同|本合同的附件')
                item.decision_trace['semantic_requirements']=[spec]
                item.evidence_clauses=corpus_facts(clauses,[spec])[spec['element_id']]
                pending(item,[('actual_annex_documents','引用文件实际提供并完整')],'核验所引用主合同及附件的实际文件；正文引用、编号和“附件为组成部分”不证明文件已经提供。')
        if item.node_id=='credit_reporting_eligibility':
            specs=[requirement('credit_authorization','征信查询/报送的书面授权条款',r'授权[^。]{0,50}(?:征信|查询|报送|上报)'),
                   requirement('credit_purpose','征信查询/报送用途范围',r'(?:资产|征信)状况[^。]{0,15}(?:查询|监督)|本合同对应业务相关的信息')]
            hits=corpus_facts(clauses,specs)
            item.decision_trace['semantic_requirements']=specs
            item.evidence_clauses=[e for s in specs for e in hits[s['element_id']]]
            eligibility={'status':'PENDING_VERIFICATION','authorization_text':'FOUND' if hits['credit_authorization'] else 'NOT_FOUND',
                'purpose_text':'FOUND' if hits['credit_purpose'] else 'NOT_FOUND',
                'query_access_qualification':'UNVERIFIED','reporting_institution_qualification':'UNVERIFIED',
                'authorization_confers_access':False}
            shared['credit_reporting_eligibility']=eligibility
            pending(item,[('credit_query_access','征信查询接入资格'),('credit_reporting_institution','信贷信息报送机构及业务资格')],
                '核验债权人的金融信用信息基础数据库查询接入资格及信贷信息报送资格；合同授权不产生机构资格，未确认前不得据此直接查询或报送。')
    shared.setdefault('credit_reporting_eligibility',{'status':'NOT_APPLICABLE'})
    return items
