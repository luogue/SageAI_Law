"""Granted-patent transfer components with independent transaction scopes.

An existing third-party licence and a reverse grant are separate relations.
Payment conditions cannot establish a disposition or a licence entitlement.
"""
import re
from review_v2.technology_service_elements import sources
from review_v2.obligation_detail_elements import _element, _segments, _DURATION
from review_v2.proposition_scope import listed_arrangement_matches, event_polarity, predicate_is_operative
from review_v2.verified_source import exact_span

FAMILIES=('patent_transfer_scope','patent_transfer_delivery','patent_transfer_warranty',
          'patent_transfer_formalities','patent_transfer_materials','patent_transfer_confidentiality',
          'patent_transfer_improvement_sharing','patent_transfer_improvement_notice','patent_transfer_claims')
RULE_FAMILIES={'TC-06-01':FAMILIES[0],'TC-06-02':FAMILIES[1],'TC-06-03':FAMILIES[2],
              'TC-06-04':FAMILIES[3],'TC-13-01':FAMILIES[4],'TC-11-01':FAMILIES[5],
              'TC-10-02':FAMILIES[6],'TC-10-03':FAMILIES[7],'TC-12-02':FAMILIES[8]}
RIGHT_DOMAINS={'RIGHT_TRANSFER','SCOPE','RESERVATION','LICENSE_BACK','EXISTING_LICENSE'}
EVIDENCE_PRIORITY={**{k:0 for k in RIGHT_DOMAINS},'REGISTRATION':1,'DELIVERY':2,'PAYMENT':3}

def has_modeled_arrangement(family, rows):
    """Only replace a legacy candidate when this adapter models its arrangement.

    A price, an isolated registration reference, or an ancillary licence is
    insufficient to replace an already modeled title/disposition requirement.
    Existing specialised evaluations remain responsible for other arrangements.
    """
    covered={row['element_id'] for row in rows if row['status']=='COVERED'}
    anchors={
        'patent_transfer_scope': {'patent_right_identity','full_patent_right_transfer'},
        'patent_transfer_delivery': {'receipt_confirmation'},
        'patent_transfer_warranty': {'ownership_guarantee','transfer_authority'},
        'patent_transfer_formalities': {'registration_deadline','registration_responsible_party','registration_materials'},
        'patent_transfer_materials': {'final_delivery_list','receipt_confirmation'},
        'patent_transfer_confidentiality': {'confidential_information_scope'},
        'patent_transfer_improvement_sharing': {'no_automatic_coownership','no_automatic_free_license'},
        'patent_transfer_improvement_notice': {'improvement_notice_required'},
        'patent_transfer_claims': {'document_assistance'},
    }
    return anchors[family] <= covered

def _find(clauses, pattern, domain, *, field=False, introduction=None):
    rows=sources(clauses,pattern,inherit_lists=True)
    if domain in {'RIGHT_TRANSFER', 'LICENSE_BACK', 'REGISTRATION'} and not introduction:
        rows=[row for row in rows if any(
            predicate_is_operative(row['quote'],match.start(),match.end())
            for match in re.finditer(pattern,row['quote']))]
    if introduction:
        rows=[r for r in rows if re.search(introduction,r['quote'])]
    if field:
        for c,_,quote in _segments(clauses):
            match=re.search(pattern,quote)
            if match and event_polarity(quote,match.start(),match.end())=='AFFIRMATIVE':
                rows.append(dict(clause_id=c.clause_id,quote=quote,location=c.location))
    if introduction:
        for c in clauses:
            for row in listed_arrangement_matches(pattern,c.text,introduction_pattern=introduction):
                rows.append(dict(clause_id=c.clause_id,location=c.location,**row))
    by_id={c.clause_id:c for c in clauses};result=[]
    for r in rows:
        c=by_id[r['clause_id']];original=getattr(c,'raw_text','') or c.text
        span=exact_span(original,r['quote'])
        if not span:continue
        r={**r,'quote':original[span[0]:span[1]],'source_domain':domain}
        if not any((s['clause_id'],s['quote'])==(r['clause_id'],r['quote']) for s in result):result.append(r)
    return result

def relations(clauses):
    """Keep relation ownership and original clauses; do not reclassify the main asset."""
    back=[c for c in clauses if re.search(r'回授|返授|反向许可',c.title+'\n'+c.text)
          and re.search(r'授予|给予|许可期限|许可用途',c.text)]
    back_ids={c.clause_id for c in back}
    history=[c for c in clauses if c.clause_id not in back_ids and re.search(
        r'历史.{0,12}许可|既有.{0,12}许可|已有许可|曾向[^。；]{0,65}授予[^。；]{0,12}许可|承继[^。；]{0,25}普通许可',c.text)]
    return back,history

def transaction_layers(clauses):
    back,history=relations(clauses)
    grant=_find(back,r'(?:同意|承诺)[^。；]{0,65}(?:授予|给予)[^。；]{0,25}(?:普通|非独占)[^。；]{0,8}许可','LICENSE_BACK')
    historical=_find(history,r'曾向[^。；]{0,70}授予[^。；]{0,15}许可|历史普通许可|既有普通许可','EXISTING_LICENSE')
    rows=[]
    if grant:rows.append(dict(type='PATENT_LICENSE_BACK',license_type='LIMITED_ORDINARY_LICENSE',sources=grant))
    if historical:rows.append(dict(type='EXISTING_THIRD_PARTY_ORDINARY_LICENSE',sources=historical))
    return rows

def elements(family,clauses):
    if family not in FAMILIES:return []
    def atom(key,label,proof,**kw):return _element(key,label,proof,source_fact_key='technology.patent_transfer.'+key,**kw)
    def find(pattern,domain='RIGHT_TRANSFER',subset=None,**kw):return _find(clauses if subset is None else subset,pattern,domain,**kw)
    back,history=relations(clauses)
    if family=='patent_transfer_claims':
        from review_v2.technology_patent_transfer_analysis import extract_third_party_claim_protection_facts
        facts=extract_third_party_claim_protection_facts(clauses)
        specs=(('claim_trigger','claim_trigger','第三方权利主张触发场景'),
          ('notice_requirement','claim_notice','第三方主张通知义务'),('notice_deadline','claim_notice_deadline','第三方主张通知期限'),
          ('transferor_participation','claim_participation','让与方处理第三方主张的义务'),
          ('document_assistance','claim_document_assistance','权属和技术来源文件协助'),
          ('defense_control','claim_defense_control','第三方索赔抗辩控制权'),
          ('lawyer_selection','claim_lawyer_selection','第三方索赔律师选择机制'),
          ('settlement_authority','claim_settlement','第三方索赔和解决策权限'),
          ('defense_cost_allocation','claim_defense_cost','第三方索赔抗辩及法律费用承担'),
          ('damages_allocation','claim_damages','第三方索赔损失赔偿责任'),
          ('replacement_or_workaround','claim_replacement','第三方禁令的替代或绕开侵权方案'),
          ('rights_cure','claim_rights_cure','取得第三方授权或排除权利瑕疵'),
          ('refund_remedy','claim_refund','第三方权利瑕疵后的退款机制'),
          ('termination_remedy','claim_termination','第三方权利瑕疵后的解除机制'))
        from review_v2.technology_service_analysis import CLAIM_RESPONSE_ELEMENT_FACT_KEYS
        return [_element(key,label,facts.get(fact,[]),
                         source_fact_key=CLAIM_RESPONSE_ELEMENT_FACT_KEYS.get(key,'patent.protection.'+fact))
                for key,fact,label in specs]
    if family=='patent_transfer_scope':
        identity=find(r'专利(?:号|编号)[：:]\s*(?:ZL|CN)\s*\d[\d.]+','SCOPE',field=True)
        full=find(r'专利权(?:全部|整体)转让|转让的是[^。；]{0,20}全部专利权|(?:全部|整体)专利权[^。；]{0,12}转让|将其(?:合法)?拥有的[^。；]{0,40}专利权[^。；]{0,12}转让(?:给|至)')
        effective=find(r'专利权自[^。；]{0,45}(?:登记|公告)[^。；]{0,25}(?:转移|生效)','REGISTRATION')
        result=[atom('patent_right_identity','转让的专利权标的',identity),atom('full_patent_right_transfer','全部专利权转让',full),
                atom('transfer_effective_on_registration','专利权登记生效与转移',effective)]
        before=[c for c in clauses if re.search(r'登记(?:完成)?前|登记完成之前',c.text)]
        for key,label,p in (
            ('transferor_no_retransfer_before_registration','登记前不得再次转让',r'不得[^。；]{0,15}再次转让'),
            ('transferor_no_pledge_before_registration','登记前不得新增质押',r'不得[^。；]{0,35}质押'),
            ('transferor_no_new_exclusive_license','登记前不得新增独占或排他许可',r'不得[^。；]{0,65}(?:独占|排他)[^。；]{0,8}许可')):
            proof=find(p,'RESERVATION',before)
            # Preserve stated reservations; do not invent a universal new ban.
            if proof:result.append(atom(key,label,proof))
        if history:
            result.extend([atom('existing_license_disclosed','历史第三方普通许可披露',find(r'曾向[^。；]{0,70}授予[^。；]{0,15}许可|历史普通许可','EXISTING_LICENSE',history)),
                atom('existing_license_survives_transfer','历史许可在转让后承继及继续有效',find(r'专利权转让不影响[^。；]{0,60}继续有效|承继[^。；]{0,30}普通许可','EXISTING_LICENSE',history))])
        grant=find(r'(?:同意|承诺)[^。；]{0,65}(?:授予|给予)[^。；]{0,25}(?:普通|非独占)[^。；]{0,8}许可','LICENSE_BACK',back)
        if grant:
            result.append(atom('license_back_exists','转让后有限普通回授许可',grant))
            for key,label,p,field,intro in (
                ('license_back_term','回授许可期限',r'许可期限[：:]\s*[^。；]+',True,None),
                ('license_back_territory','回授许可地域',r'许可地域[：:]\s*[^。；]+',True,None),
                ('license_back_purpose','回授许可用途',r'许可用途[：:]\s*[^。；]+',True,None),
                ('license_back_no_assignment','回授许可不得转让',r'将许可转让|转让(?:该|本项)?许可',False,r'不得|禁止'),
                ('license_back_no_sublicense','回授许可不得分许可',r'分许可|再许可',False,r'不得|禁止'),
                ('license_back_no_new_projects','回授许可不得新增项目',r'承接新的[^。；]{0,25}项目|新增[^。；]{0,15}项目',False,r'不得|禁止'),
                ('license_back_expiry','回授许可到期停止实施',r'许可期届满后继续实施|到期[^。；]{0,15}停止实施',False,r'不得|禁止')):
                proof=find(p,'LICENSE_BACK',back,field=field,introduction=intro)
                result.append(atom(key,label,proof))
        # Final evidence is rebuilt from canonical elements. Preserve source
        # priority here as well as in the candidate evidence collection.
        return sorted(result, key=lambda e:min(
            (EVIDENCE_PRIORITY.get(s.get('source_domain'),9) for s in e['supporting_evidence']),
            default=9))
    delivery=[c for c in clauses if re.search(r'资料交付|交付资料|文件交付|交付文件',c.title) or re.search(r'(?:应|须)[^。；]{0,50}交付[：:]',c.text)]
    receipt=find(r'(?:收到|接收)资料后[^。；]{0,25}(?:出具|签署)[^。；]{0,12}(?:签收|验收)确认','DELIVERY',delivery)
    inventory=find(r'(?:技术资料|转让资料|交付资料|资料交付)(?:清单|目录)[^。；]{0,15}V\d+(?:\.\d+)*','DELIVERY',delivery,introduction=r'交付|提供|提交')
    if family in {'patent_transfer_delivery','patent_transfer_materials'}:
        common=[atom('delivery_document_list','专利及技术资料交付清单',inventory),
                atom('delivery_deadline','技术资料交付期限',find(_DURATION+r'内[^。；]{0,30}交付','DELIVERY',delivery)),
                atom('receipt_confirmation','技术资料书面签收确认',receipt)]
        if family=='patent_transfer_materials':
            return [atom('final_delivery_list','最终技术资料交付清单',inventory),common[-1],
                atom('file_version','交付文件版本号',find(r'(?:说明|清单)[^。；]{0,12}V\d+(?:\.\d+)*','DELIVERY',delivery,introduction=r'交付|提供')),
                atom('file_identifier','最终交付文件编号',find(r'(?:文件编号|资料编号)[：:]\s*\w+','DELIVERY',delivery)),
                atom('delivery_quantity','交付资料份数',find(r'(?:资料|文件)[^。；]{0,15}(?:[一二三四五六\d]+)(?:份|套)','DELIVERY',delivery)),
                atom('delivery_method','交付资料介质形式',find(r'扫描件及原件|电子版|纸质版|加密[^。；]{0,12}(?:交付|邮件)','DELIVERY',delivery,introduction=r'交付|提供'))]
        common.extend([atom('nonconforming_delivery_remedy','不合格资料补正义务',find(r'(?:资料|文件)[^。；]{0,25}(?:不合格|不符合)[^。；]{0,35}(?:应|须)[^。；]{0,15}(?:补正|补充|改正)','DELIVERY')),
          atom('delivery_remedy_deadline','不合格资料补正期限',find(r'(?:补正|补充|改正)[^。；]{0,15}'+_DURATION+'|'+_DURATION+r'内[^。；]{0,15}(?:补正|补充|改正)','DELIVERY',delivery)),
          atom('delivery_failed_cure_termination','资料补正失败后的解除机制',find(r'(?:补正|补救)[^。；]{0,20}(?:失败|仍不符合)[^。；]{0,35}解除','DELIVERY')),
          atom('delivery_failed_cure_refund','资料补正失败后的退款机制',find(r'(?:补正|补救)[^。；]{0,20}(?:失败|仍不符合)[^。；]{0,35}(?:返还|退款)','DELIVERY'))])
        return common
    if family=='patent_transfer_warranty':
        specs=(('ownership_guarantee','专利权属合同保证',r'(?:为|系)专利登记权利人|合法拥有[^。；]{0,20}专利权'),
          ('transfer_authority','签署及履行转让合同的权限',r'有权签(?:署|订)并履行本合同|(?:具有|享有)[^。；]{0,15}处分权'),
          ('co_owner_absence','共同权利人情况',r'不存在共有权人|无共有权人'),
          ('prior_transfer_absence','既有整体转让情况',r'未将专利整体转让[^。；]+'),
          ('pledge_status','质押现状披露',r'(?:当前)?不存在质押登记'),
          ('seizure_status','查封现状披露',r'(?:当前)?不存在(?:法院)?查封'),
          ('ownership_dispute_status','权属争议现状披露',r'不存在正在进行的专利权属诉讼'))
        result=[atom(k,label,find(p,'CONTRACTUAL_REPRESENTATION',introduction=r'保证|确认|声明'),evidence_level='CONTRACTUAL_REPRESENTATION') for k,label,p in specs]
        result.append(atom('existing_license_disclosure','既有许可披露',find(r'曾向[^。；]{0,70}授予[^。；]{0,15}许可','EXISTING_LICENSE',history)))
        invalidity=[c for c in clauses if re.search(r'专利.{0,12}无效|无效宣告',c.text)]
        pending=find(r'第三方[^。；]{0,35}提交了[^。；]{0,25}无效宣告请求|无效宣告程序尚未审结','INVALIDITY',invalidity)
        if pending:
            # A complete title representation does not settle the economics
            # of the separately disclosed pending invalidity proceeding.
            result.append(atom('invalidity_proceeding_disclosure','已发生且未审结的专利无效程序披露',pending))
            result.append(atom('total_invalidity_paid_refund','全部无效后的已付款返还及比例',
                find(r'(?:全部|整体)[^。；]{0,12}无效[^。；]{0,45}(?:应当|应|须)[^。；]{0,12}(?:退还|返还)[^。；]{0,15}(?:全部|[\d一二三四五六七八九十]+%)','INVALIDITY',invalidity)))
            partial=[c for c in invalidity if re.search(r'部分|独立权利要求',c.text)]
            if partial:
                for key,label,p in (
                    ('partial_invalidity_price_method','部分无效时重新定价方法',r'(?:定价|价款调整)(?:方法|公式|方式)(?:为|[：:])[^。；]+'),
                    ('partial_invalidity_valuation','部分无效时价值评估机构',r'(?:由|委托)[^。；]{1,30}(?:机构|公司)[^。；]{0,12}评估'),
                    ('partial_invalidity_deadlock','重新定价协商不成的处理',r'协商不(?:成|一致)[^。；]{0,20}(?:有权解除|退还|仲裁|诉讼)'),
                    ('partial_invalidity_paid_refund','部分无效对已付款的返还处理',r'(?:应|须|无需)[^。；]{0,12}(?:返还|退还)[^。；]{0,15}已(?:经)?支付')):
                    result.append(atom(key,label,find(p,'INVALIDITY',partial)))
                result.append(atom('independent_claim_value_adjustment','独立权利要求无效后的价款重估原则',
                    find(r'双方应重新协商[^。；]{0,15}转让价款','INVALIDITY',partial)))
        return result
    if family=='patent_transfer_formalities':
        formal=[c for c in clauses if re.search(r'(?:共同|负责)[^。；]{0,30}办理专利权转让登记|专利权自[^。；]{0,40}登记',c.text)]
        return [atom('registration_deadline','专利权转让登记期限',find(_DURATION+r'内[^。；]{0,20}办理专利权转让登记','REGISTRATION',formal)),
          atom('registration_responsible_party','共同办理专利权转让登记',find(r'双方应[^。；]{0,45}共同办理专利权转让登记','REGISTRATION',formal)),
          atom('registration_materials','登记材料准备义务',find(r'专利权转让证明文件|著录项目变更文件','REGISTRATION',formal,introduction=r'负责准备|应.{0,10}提供')),
          atom('registration_cost','登记费用承担',find(r'登记费用由[^。；]{0,15}承担','REGISTRATION',formal)),
          atom('registration_effect','登记公告时权利转移',find(r'专利权自[^。；]{0,45}(?:登记|公告)[^。；]{0,20}转移','REGISTRATION',formal))]
    if family=='patent_transfer_confidentiality':
        confidential=[c for c in clauses if re.search(r'保密',c.title)]
        scope=find(r'参数|数据|方案|报价|客户信息','CONFIDENTIALITY',confidential,introduction=r'非公开信息应保密|保密信息.{0,12}(?:包括|如下)')
        duty=find(r'非公开信息应保密|(?:应|须)[^。；]{0,15}(?:承担|履行)保密义务','CONFIDENTIALITY',confidential)
        restriction=find(r'未经[^。；]{0,25}书面同意[^。；]{0,25}不得向[^。；]{0,15}第三方披露','CONFIDENTIALITY',confidential)
        return [atom('confidential_information_scope','保密信息类别和范围',scope),atom('confidentiality_obligation','保密义务',duty or restriction),atom('third_party_disclosure_restriction','向无关第三方披露的限制',restriction)]
    improvement=[c for c in clauses if re.search(r'改进成果',c.title)]
    if family=='patent_transfer_improvement_sharing':
        return [atom('no_automatic_coownership','改进成果不自动共有',find(r'不当然共有[^。；]{0,15}改进成果','IMPROVEMENT',improvement)),
          atom('no_automatic_free_license','改进成果无自动免费许可',find(r'不当然取得[^。；]{0,25}免费许可','IMPROVEMENT',improvement)),
          atom('priority_transfer_right','改进成果同等条件优先受让权',find(r'享有[^。；]{0,20}优先受让权','IMPROVEMENT',improvement))]
    if family=='patent_transfer_improvement_notice':
        return [atom('improvement_notice_required','改进成果形成后的通知义务',find(r'改进方案[^。；]{0,35}(?:应|须)[^。；]{0,20}通知','IMPROVEMENT',improvement)),
          atom('notice_deadline','改进成果通知期限',find(_DURATION+r'内[^。；]{0,10}书面通知','IMPROVEMENT',improvement)),
          atom('priority_transfer_exercise_deadline','优先受让权行使期限',find(r'优先受让权[^。；]{0,20}'+_DURATION+'|'+_DURATION+r'内[^。；]{0,15}行使优先受让权','IMPROVEMENT',improvement))]
    return []
