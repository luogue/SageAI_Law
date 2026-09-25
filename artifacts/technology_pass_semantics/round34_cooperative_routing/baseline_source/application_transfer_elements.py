"""Patent application assets and procedural arrangements with exact source ownership.

Disclosure, operative control, and proof completeness are separate requirements.
Application-stage conditions describe arrangements, never granted-patent facts.
"""
import re
from review_v2.technology_service_elements import sources
from review_v2.obligation_detail_elements import _element, _DURATION
from review_v2.disclosure_facts import negative_sources

FAMILIES = ('application_identity', 'application_control', 'application_proof',
            'application_warranty', 'application_registration', 'application_outcomes',
            'application_stage', 'application_liability')
RULE_FAMILIES = {'TC-01-03':'application_identity','TC-06-01':'application_control',
    'TC-03-04':'application_proof','TC-13-02':'application_proof'}


def elements(family, clauses):
    if family not in FAMILIES: return []
    def find(pattern, scope=None):
        selected=[c for c in clauses if not scope or re.search(scope,c.title+'\n'+c.text)]
        result=sources(selected,pattern,inherit_lists=True)
        if '[：:]' in pattern:
            # A labelled scalar may have its value in the next paragraph.
            from review_v2.obligation_detail_elements import _segments
            from review_v2.proposition_scope import event_polarity
            for c,_,quote in _segments(selected):
                m=re.search(pattern,quote)
                if m and event_polarity(quote,m.start(),m.end())=='AFFIRMATIVE':
                    row=dict(clause_id=c.clause_id,quote=quote,location=c.location,proposition_polarity='AFFIRMATIVE')
                    if not any(r['clause_id']==c.clause_id and r['quote']==quote for r in result):result.append(row)
        return result
    def atom(key,label,proof,**kw):
        return _element(key,label,proof,source_fact_key='technology.application.'+key,**kw)
    identity = [
        ('patent_application_identity','专利申请名称',find(r'(?:专利申请名称|发明名称|发明创造名称)[：:]\s*[^\n。；]{3,100}')),
        ('application_number','专利申请号',find(r'(?:专利)?申请(?:号|号码)[：:]\s*(?:CN)?\s*\d[\d.]+')),
        ('application_date','专利申请日',find(r'申请(?:日|日期)[：:]\s*\d{4}年\d{1,2}月\d{1,2}日')),
        ('publication_number','专利申请公开号',find(r'(?:公开(?:（公告）|\(公告\))?|公布)(?:号|号码)[：:]\s*(?:CN)?\d+[A-Z]?')),
        ('application_status','专利申请当前法律状态',find(r'(?:当前法律状态|当前状态|审查状态)[：:]\s*[^。；\n]+|(?:尚未|未)[^。；]{0,8}(?:取得|获得)授权')),
        ('current_applicant','当前专利申请人',find(r'(?:当前)?(?:专利)?申请人[：:]\s*[^。；\n]+|(?:为|系)当前专利申请人')),
    ]
    direct={k:(label,rows) for k,label,rows in identity}
    # Canonical identity prefers the substantive first definition over repeats in attachments.
    for key,(label,proof) in direct.items():
        primary=[q for q in proof if not any(c.clause_id==q['clause_id'] and ('附件' in c.location or getattr(c,'source_type','')=='ATTACHMENT') for c in clauses)]
        field_pattern={'application_status':r'(?:当前法律状态|当前状态|审查状态)[：:]',
                       'current_applicant':r'(?:当前)?(?:专利)?申请人[：:]'}.get(key)
        labelled=[q for q in primary if field_pattern and re.search(field_pattern,q['quote'])]
        if primary: direct[key]=(label,labelled or primary)
    def named(key):return atom(key,*direct[key])
    extra={
        'application_right_transfer':('全部或部分专利申请权转让范围',find(r'(?:本合同转让标的|转让标的)[^。；]{0,70}(?:全部|部分)专利申请权|(?:全部|部分)专利申请权[^。；]{0,30}(?:转让|转移)')),
        'transfer_registration_required':('申请权转让登记生效安排',find(r'专利申请权自[^。；]{0,55}(?:登记|变更)[^。；]{0,20}(?:转移|生效)|(?:申请权|专利申请权)[^。；]{0,40}(?:经|完成)登记[^。；]{0,15}生效')),
        'transfer_registration_party':('申请权转让登记办理主体',find(r'(?:应|负责)[^。；]{0,55}(?:提交|办理)[^。；]{0,35}(?:申请权转让登记|登记所需材料)')),
        'transfer_registration_deadline':('申请权转让登记提交期限',find(_DURATION+r'内[^。；]{0,55}(?:提交|办理)[^。；]{0,35}(?:转让登记|登记所需材料)')),
        'registration_failure_remedy':('登记失败时解除、退款及赔偿救济',find(r'(?:不予办理|无法完成)[^。；]{0,20}(?:转让登记|登记)[^。；]{0,100}(?:解除|返还|赔偿)')),
        'pre_registration_control':('登记前申请维持及程序控制',find(r'(?:仍作为|仍为)[^。；]{0,15}申请人[^。；]{0,25}(?:维持|负责)|(?:登记完成前|过渡期)[^。；]{0,70}(?:负责|维持)')),
        'post_registration_control':('登记后审查控制权',find(r'(?:后续审查意见)[^。；]{0,30}(?:决定|负责)[^。；]{0,20}(?:答复|策略)')),
        'withdrawal_prohibition':('未经同意不得撤回申请',find(r'不得[^。；]{0,25}撤回[^。；]{0,12}(?:专利)?申请')),
        'office_action_response_control':('审查意见答复方案及提交控制',find(r'(?:正式提交|提交答复)[^。；]{0,35}(?:书面确认|书面同意)|(?:负责|决定)[^。；]{0,20}(?:答复策略|答复方案)')),
        'claim_amendment_control':('权利要求修改及缩限控制',find(r'(?:负责决定|决定)[^。；]{0,15}修改权利要求|不得未经[^。；]{0,25}同意[^。；]{0,35}(?:权利要求|缩限)')),
        'reexamination_right':('复审决定权',find(r'(?:有权决定|负责决定|决定)[^。；]{0,15}(?:是否)?提出复审')),
        'reexamination_cost':('复审费用承担',find(r'复审官费[^。；]{0,40}(?:承担|支付)')),
        'substantive_examination_status':('当前实质审查状态',find(r'(?:已经进入|处于|当前状态[：:]|当前法律状态[：:])[^。；]{0,12}实质审查|实质审查中')),
        'office_action_received':('已收到审查意见通知书',find(r'(?:已|已经)收到[^。；]{0,20}审查意见通知书')),
        'office_action_deadline':('审查意见答复截止日期',find(r'答复截止(?:日|日期)[：:]\s*\d{4}年\d{1,2}月\d{1,2}日')),
        'office_action_response_pending':('审查意见尚待答复',find(r'当前尚未提交[^。；]{0,30}审查意见答复|审查意见状态[：:]待答复')),
        'rejection_risk':('正常审查驳回触发情形',find(r'如申请[^。；]{0,65}被[^。；]{0,20}驳回|(?:正常专利审查|正常审查)[^。；]{0,35}(?:未获得授权|无法授权)')),
        'deemed_withdrawal_risk':('逾期答复等导致视为撤回的责任',find(r'导致申请被视为撤回[^。；]{0,50}解除合同')),
        'authorization_uncertainty':('申请尚未授权的法律状态',find(r'(?:尚未|未)[^。；]{0,8}(?:取得|获得)授权',r'当前|标的')),
        'payment_before_registration':('登记前付款节点',find(r'合同生效后[^。；]{0,30}支付[^。；]{0,55}(?:元|%)',r'价款|付款')),
        'payment_after_registration':('转让登记完成后付款节点',find(r'(?:完成|办理)[^。；]{0,30}转让登记后[^。；]{0,55}支付[^。；]{0,55}(?:元|%)')),
        'payment_after_grant':('授权后付款节点',find(r'(?:获得授权|授予发明专利权通知书)[^。；]{0,55}支付[^。；]{0,55}(?:元|%)')),
        'claim_scope_shrinkage':('授权权利要求明显缩小的触发情形',find(r'(?:最终授权|权利要求保护范围)[^。；]{0,65}(?:明显缩小|显著缩小)')),
    }
    def extra_atom(key):return atom(key,*extra[key])
    if family=='application_identity':return [named(k) for k in direct]
    if family=='application_control':return [named('patent_application_identity'),named('current_applicant')]+[extra_atom(k) for k in (
        'application_right_transfer','transfer_registration_required','pre_registration_control','post_registration_control',
        'withdrawal_prohibition','office_action_response_control','claim_amendment_control','reexamination_right')]
    if family=='application_registration':return [extra_atom(k) for k in ('transfer_registration_required','transfer_registration_party','transfer_registration_deadline','registration_failure_remedy')]
    if family=='application_stage':return [extra_atom(k) for k in extra]
    if family=='application_outcomes':
        # A duty to negotiate is not a determinate refund/price-adjustment remedy.
        scopes=[c for c in clauses if re.search(r'驳回|授权范围|缩小|最终未获得授权',c.title+'\n'+c.text)]
        def remedy(pattern):
            return [q for q in sources(scopes,pattern,inherit_lists=True)
                    if not re.search(r'另行协商|未明确|未约定|应返还多少|是否返还|是否调整',q['quote'])]
        rows=[extra_atom(k) for k in ('rejection_risk','deemed_withdrawal_risk','reexamination_right','reexamination_cost',
            'substantive_examination_status','office_action_received','office_action_deadline','office_action_response_pending','authorization_uncertainty',
            'payment_before_registration','payment_after_registration','payment_after_grant','claim_scope_shrinkage')]
        # Context must identify normal examination, not the transferor-fault remedy.
        def normal_refund(q):
            return bool(re.search(r'正常[^。；]{0,25}审查[^。；]{0,60}(?:返还|退还)|(?:第一期|第二期|已支付转让价款)[^。；]{0,25}(?:应|须|不予|不)[^。；]{0,10}(?:返还|退还)',q))
        refunds=[q for q in remedy(r'(?:返还|退还)[^。；]{0,20}(?:元|价款|款项)|(?:价款|款项)[^。；]{0,20}(?:返还|退还)') if normal_refund(q['quote'])]
        rows += [atom('rejection_refund','正常审查最终驳回时已付款返还规则',refunds),
                 atom('remaining_payment_after_rejection','驳回后未到期价款处理',remedy(r'(?:价款|款项)[^。；]{0,15}(?:无需支付|不再支付|仍应支付|继续支付)')),
                 atom('reexamination_failure_refund','复审后仍驳回时已付款返还比例',remedy(r'复审后[^。；]{0,90}(?:返还|退还)[^。；]{0,25}(?:\d+|全部|比例)')),
                 atom('price_adjustment_on_scope_shrinkage','权利要求明显缩小时价款调整机制',remedy(r'(?:价款|价格)[^。；]{0,35}(?:调整为|减少|调减|退还|降低)|(?:应|须)[^。；]{0,20}(?:调减|退还)[^。；]{0,20}价款'))]
        return rows
    absence={
        'joint_applicant_disclosure':('共同申请人情况披露',negative_sources(clauses,r'共同申请人')),
        'prior_transfer_disclosure':('是否已整体转让的披露',find(r'未将本申请整体转让[^。；]+')),
        'transfer_restriction_disclosure':('限制本次申请权转让的协议披露',find(r'未签署[^。；]{0,35}限制[^。；]{0,25}转让[^。；]{0,20}协议')),
        'title_dispute_disclosure':('已收到的第三方权属争议通知披露',find(r'未收到第三方[^。；]{0,50}(?:诉讼|仲裁)通知')),
        'employee_invention_origin':('职务研发来源声明',find(r'(?:本申请|该申请)[^。；]{0,50}(?:履行职务|职务研发)[^。；]{0,20}(?:完成|形成)')),
    }
    if family=='application_warranty':return [named('current_applicant')]+[atom(k,*v) for k,v in absence.items()]
    if family=='application_liability':return [
        atom('transferor_title_fault_liability','让与方无权处分或隐瞒权属争议的责任',find(r'因[^。；]{0,15}(?:无权处分|隐瞒权属争议)[^。；]{0,60}承担责任')),
        atom('transferee_modification_liability','受让方自行新增或修改引发权利问题的责任',find(r'因[^。；]{0,30}自行[^。；]{0,15}(?:新增|修改)[^。；]{0,70}自行承担'))]
    if family=='application_proof':
        rows=[named(k) for k in direct]+[atom(k,*v) for k,v in absence.items()]
        rows += [atom('application_documents','专利申请文件交付安排',find(r'专利申请文件全套电子版',r'交付|清单')),
                 atom('acceptance_notice','受理通知书交付安排',find(r'受理通知书',r'交付|清单')),
                 atom('inventor_information','发明人名单',_inventor_sources(clauses))]
        incomplete=any(re.search(r'(?:无法提供|缺少)[^。]{0,120}(?:职务发明|职务成果)[^。]{0,35}(?:归属|确认)',c.text,re.S) for c in clauses)
        proof=find(r'(?:劳动合同|工资记录|项目任务|Git提交记录|职务成果归属材料完整|职务成果确认)',r'权属|来源|保证|归属')
        rows.append(atom('employee_invention_title_chain','职务发明权属证明链',proof,
            status='PARTIALLY_COVERED' if incomplete and proof else None,
            residuals=['离职发明人的完整职务发明权属确认材料'] if incomplete else None,
            evidence_level='DOCUMENTARY_PROOF',proof_requirement_level='DOCUMENTARY_PROOF'))
        for row in rows:row.setdefault('evidence_level','CONTRACTUAL_REPRESENTATION')
        # Keep established application-document requirements and canonical IDs.
        # Identity aliases reuse the same source, rather than searching delivery
        # headings for fields already stated in the application definition.
        from review_v2.engine import _technology_ip_proof_model, _APPLICATION_ENCUMBRANCE_DISCLOSURE_SPECS, _current_rights_disclosure_evidence, _clause_public_dict
        model=_technology_ip_proof_model({'primary_subtype':'TECHNOLOGY_TRANSFER','tertiary_subtype':'PATENT_APPLICATION_RIGHT_TRANSFER'})
        aliases={'application_invention_name':'patent_application_identity',
                 'application_review_status':'application_status',
                 'application_acceptance_document':'acceptance_notice'}
        by_id={r['element_id']:r for r in rows}
        disclosures={k for k,_,_ in _APPLICATION_ENCUMBRANCE_DISCLOSURE_SPECS}
        for key,label,terms in model['specs']:
            if key in by_id:continue
            proof=by_id[aliases[key]]['supporting_evidence'] if key in aliases else find('|'.join(re.escape(t) for t in terms))
            if key in disclosures:
                proof=_current_rights_disclosure_evidence([_clause_public_dict(c) for c in clauses],terms)
                proof=[r for r in proof if not re.search(r'改进|后续成果',r.get('quote') or r.get('text',''))]
            label=label.replace('已列入交付材料。','交付安排').replace('已有合同记载。','').replace('已有安排。','安排')
            if key=='application_coownership_disclosure':proof=proof or absence['joint_applicant_disclosure'][1]
            if key=='application_withdrawal_rejection_status':proof=proof or extra['substantive_examination_status'][1]
            rows.append(atom(key,label,proof))
        return rows
    return []


def _inventor_sources(clauses):
    # Label/value lists may span paragraphs. Keep the original label and values
    # together, rather than assigning unrelated delivery-list evidence.
    from review_v2.verified_source import exact_span
    rows=[]
    pattern=r'发明人(?:/设计人)?[：:]\s*[\u4e00-\u9fff·、， ]{2,40}(?:\n\s*[\u4e00-\u9fff·、， ]{2,40})*'
    for c in clauses:
        for m in re.finditer(pattern,c.text):
            quote=m[0].strip()
            original=getattr(c,'raw_text','') or c.text
            span=exact_span(original,quote)
            if span:
                rows.append(dict(clause_id=c.clause_id,quote=original[span[0]:span[1]],
                                 location=c.location,proposition_polarity='AFFIRMATIVE'))
    return rows
