"""Mandate relationships and operative clauses, independent of document names/amounts."""
import re
from review_v2.lease_semantics import requirement, corpus_facts
from review_v2.semantic_relations import relation

HIDDEN={'agency_undisclosed_principal_intervention','agency_disclose_third_party','agency_intervention_defense_continuation','agency_third_party_choice_right','agency_disclose_principal','agency_choice_defense_continuation'}
CONDITIONS={**dict.fromkeys(HIDDEN,'受托人以自己名义与第三人订约或存在隐名委托时适用'),
 'agency_unpaid_intent_gross_standard':'无偿委托或报酬性质尚待核实时适用',
 'agency_nature_distinction':'存在实质混合交易或委托性质不确定时适用'}

def facts(text):
    paid=bool(re.search(r'(?:固定服务报酬|报酬|服务费)[^。；\n]{0,20}[1-9]\d*(?:元|万)|本合同为有偿委托',text))
    hidden=any(not re.search(r'不涉及|不存在|不得|无权|禁止',re.split(r'[。；\n]',text[:m.start()])[-1])
               for m in re.finditer(r'以自己名义[^。；]{0,40}(?:订立|订约|签订)|隐名委托|第三人不知道委托关系',text))
    mandate=bool(re.search(r'(?:委托|受托)[^。]{0,35}处理[^。]{0,25}(?:事务|事宜)',text))
    mixed=bool(re.search(r'(?:本合同|本协议)[^。]{0,20}(?:兼具|同时包含|兼有)[^。]{0,20}(?:承揽|中介|行纪)|以自己名义[^。]{0,25}贸易',text))
    return dict(paid=paid,hidden=hidden,mandate=mandate,mixed=mixed)

def prerequisite(text,node):
    f=facts(text)
    if node in HIDDEN:return f['hidden'],CONDITIONS[node]
    if node=='agency_unpaid_intent_gross_standard':return not f['paid'],CONDITIONS[node]
    if node=='agency_nature_distinction':return f['mixed'] or not f['mandate'],CONDITIONS[node]
    return None

def specs(paid=False):
    profiles = {
     'agency_unnecessary_expense_exclusion':[requirement('mandate_unapproved_expenses','未经同意的超额或非必要费用由受托人承担',r'(?:超过|超预算|非必要|不合理)[^。]{0,60}未经[^。]{0,20}同意[^。]{0,30}(?:乙方|受托人)自行承担',r'(?:非必要|不合理|未经批准)[^。]{0,30}费用[^。]{0,25}(?:不予报销|自行承担)')],
     'agency_principal_compensate_trustee_loss':[requirement('mandate_no_fault_loss','受托人不可归责受损时请求赔偿',r'(?:乙方|受托人)[^。]{0,60}(?:不可归责|无过错)[^。]{0,60}(?:损失|受损)[^。]{0,60}(?:赔偿|补偿)')],
    }
    # Role/action/object relations are shared between coverage and retrieval.
    # They tolerate modifiers and argument order without accepting title words.
    agent=r'(?:受托人|乙方)'
    principal=r'(?:委托人|甲方)'
    task=r'(?:事务|事宜|工作|事项)'
    fee=r'(?:报酬|委托(?:服务)?费用|服务报酬|服务费)'
    end=r'(?:解除|终止|结束)(?:本合同|本协议|合同|协议|委托(?:关系)?)?'
    completed=r'(?:已经|已|实际|已经实际)+(?:履行|完成)[^。；]{0,15}(?:工作|月份|天数|事务)?'
    compensation=r'(?:应|须|应当|承担|负责)[^。；]{0,25}(?:赔偿|补偿)'
    profiles.update({
      'agency_expense_advance':[relation('mandate_expense_prepayment','委托人事先提供处理事务所需费用',
          {'payer':principal+r'[^。；]{0,30}(?:预付|预拨|提前支付|事先支付)',
           'object':r'必要费用|事务费用|费用预算|备用金|处理事务[^。；]{0,15}费用'},
          excluded=(r'(?:无需|不予|不得|不必)[^。；]{0,8}(?:预付|预拨|提前支付)',))],
      'agency_sub_entrustment_liability':[relation('mandate_delegation_liability','经同意转委托后的选任及指示责任',
          {'delegation':r'转委托', 'consent':r'(?:经|取得)[^。；]{0,12}(?:同意|追认)',
           'selection':r'选任', 'instruction':r'指示', 'liability':r'承担[^。；]{0,8}责任'},
          excluded=(r'(?:不承担|(?<!不)免除)[^。；]{0,20}选任',))],
      'agency_emergency_sub_entrustment':[relation('mandate_emergency_delegation','紧急情况下为委托人利益交第三人处理事务',
          {'emergency':r'紧急|紧迫', 'purpose':r'维护[^。；]{0,15}利益|保护[^。；]{0,15}利益',
           'delegation':r'转委托[^。；]{0,12}第三[人方]|(?:交由|委托)第三[人方][^。；]{0,15}处理'},
          excluded=(r'(?:不得|禁止|不可)[^。；]{0,10}转委托',))],
      'agency_power_of_attorney_attachment':[relation('mandate_authorization_attachment','附件清单或文件正文载明授权委托书',
          {'inventory':r'附件[^。；\n]{0,20}[：:、一二三四五六七八九十0-9]',
           'document':r'授权委托书|代理授权书'},
          excluded=(r'(?:不提供|未提供|不包含|另行提供|应当提供)[^。；\n]{0,20}(?:授权委托书|代理授权书)',
                    r'(?:授权委托书|代理授权书)[^。；\n]{0,15}(?:不适用|未提供)',))],
      'agency_contract_type_identification':[relation('mandate_relationship','受托人为委托人处理事务的关系',
          {'delegation':principal+r'[^。；]{0,8}委托'+agent,
           'handling':agent+r'[^。；]{0,40}(?:处理|办理|开展)[^。；]{0,30}'+task},
          {'handling':agent+r'[^。；]{0,12}受托[^。；]{0,12}处理[^。；]{0,30}'+task},
          {'acceptance':agent+r'[^。；]{0,15}(?:接受|受)[^。；]{0,15}委托',
           'handling':r'(?:处理|办理|负责)[^。；]{0,50}'+task})],
      'agency_contract_effect_basis':[
          relation('mandate_voluntary_agreement','双方协商合意或理解合同含义',
              {'parties':r'(?:双方|甲.{0,4}乙双方)', 'assent':r'(?:自愿|意思表示真实|真实意思|含义认识一致|理解[^。；]{0,20}一致)'},
              {'assent':r'双方[^。；]{0,30}(?:理解|知悉)[^。；]{0,20}(?:条款|合同)',
               'agreement':r'(?:同意|接受)[^。；]{0,15}(?:约定|条款|合同)'}),
          relation('mandate_lawful_formation','签约主体及必要手续的合规声明',
              {'parties':r'双方', 'lawful_capacity':r'符合[^。；]{0,30}(?:签约|签订)[^。；]{0,30}(?:规定|要求)',
               'procedures':r'履行[^。；]{0,15}(?:必要|签约|批准|授权)(?:的)?手续'},
              {'capacity':r'(?:双方|各方)[^。；]{0,35}(?:民事行为能力|签约资格)',
               'authorization':r'(?:具备|取得|完成)[^。；]{0,15}(?:授权|手续)'})],
      'agency_affair_scope':[relation('mandate_affair_scope','具体列明受托处理的事务内容',
          {'responsibility':agent+r'[^。；]{0,16}(?:负责|承担|办理|处理)',
           'work':r'(?:调查|核实|谈判|信息收集|商务协调|运营|接洽|报告|采购)'},
          {'assignment':principal+r'[^。；]{0,12}委托'+agent,
           'work':r'(?:调查|核实|谈判|运营|采购|渠道|接洽|报告)'},
          {'assignment':r'(?:委托事项|委托事务|委托工作|受托工作)[^。；]{0,15}(?:包括|为|如下|限于)',
           'work':r'(?:调查|核实|谈判|信息收集|商务协调|运营|接洽|报告|采购)'})],
      'agency_unfinished_no_trustee_fault_remuneration':[relation('mandate_proportional_remuneration','不可归责未完成的相应报酬',
          {'remuneration':fee,'performance':completed,'allocation':r'(?:比例|天数|据实|相应|实际价值|按日)'})],
      'agency_arbitrary_termination':[relation('mandate_mutual_exit','委托双方均可任意结束委托关系',
          {'parties':r'(?:双方|任何一方|任[何一]*一方|委托人[、和或及与]+受托人|甲.{0,3}乙双方)',
           'right':r'(?:均可|可|有权)[^。；]{0,12}(?:随时|提前|任意)[^。；]{0,10}'+end},
          {'parties':r'(?:任何一方|双方)', 'right':r'(?:均可|均有权)[^。；]{0,12}(?:终止|结束)委托'} ,
          excluded=(r'(?:不得|无权|不能)[^。；]{0,10}(?:随时|任意|提前)?(?:解除|终止|结束)',
                    r'(?:只有|仅在|发生|如因|如果|导致)[^。；]{0,50}(?:有权|可)[^。；]{0,10}(?:解除|终止)'))],
      'agency_termination_compensation_scope':[
          relation('mandate_exit_loss_liability','因可归责解除造成损失时的赔偿责任',
              {'exit':end,'loss':r'(?:造成|导致)[^。；]{0,15}损失','liability':compensation}),
          relation('mandate_exit_profit_scope','有偿委托解除赔偿涵盖履行利益',
              {'exit':end,'liability':r'赔偿|补偿','scope':r'可得利益|履行后[^。；]{0,18}(?:利益|收益)|预期(?:利润|收益)'},
              {'continuation':r'赔偿(?:范围)?包括','scope':r'可得利益|履行后[^。；]{0,18}(?:利益|收益)|预期(?:利润|收益)'},
              across_sentences=True)],
      'agency_expense_reimbursement_interest':[
          relation('mandate_expense_repayment','受托人处理事务费用的偿还或报销',
              {'expense':r'(?:垫付|代垫|(?:必要|合理)[^。；]{0,40}(?:费用|费))',
               'repayment':principal+r'[^。；]{0,30}(?:偿还|报销|返还)|由'+principal+r'承担'}),
          relation('mandate_advance_interest','垫付费用的利息处理',
              {'advance':r'(?:垫付|代垫)[^。；]{0,15}(?:费用|支出|款)',
               'interest':r'利息|资金占用费|利率',
               'allocation':r'支付|计算|偿还|承担|不计|无需支付|免付'})],
      'agency_over_authority_liability':[relation('mandate_unauthorized_liability','超出委托授权造成损失的责任',
          {'actor':agent+r'[^。]{0,15}(?:擅自)?(?:超越|超出|越过)[^。]{0,10}(?:权限|授权|范围)',
           'loss':r'(?:造成|遭受)[^。]{0,20}损失',
           'liable_actor':agent+r'[^。]{0,15}(?:应|须)[^。]{0,20}赔偿|(?:造成|导致)'+principal+r'[^。]{0,8}损失的[，,](?:应|须)[^。]{0,20}赔偿'},
          across_sentences=True)],
      'agency_termination_handover':[
          relation('mandate_exit_handover','终止解除后移交资料或工作文件',
              {'exit':end,'handover':r'移交|交接|返还','object':r'资料|文件|财产|记录|事项'}),
          relation('mandate_exit_settlement','终止解除后费用或报酬结算',
              {'exit':end,'settlement':r'结算|结清|退还','payment':fee+r'|必要费用'},
              {'exit_handover':r'交接(?:完成)?后','settlement':r'结算|结清','payment':fee+r'|必要费用'})],
      'agency_final_report_after_termination':[relation('mandate_final_report','终止解除时报告委托事务处理结果',
          {'exit':end,'delivery':r'(?:提交|报告|汇报|提供)',
           'result':r'(?:工作|结果|最终|结项|事务)报告|(?:处理|办理|事务)结果'},
          {'end_of_term':r'委托期限届满后','delivery':r'提交|提供','result':r'最终[^。；]{0,10}报告'})],
    })
    profiles['agency_unfinished_no_trustee_fault_remuneration'][0]['preceding_context_pattern']=r'不可归责于(?:乙方|受托人)[^。]{0,60}(?:解除|不能完成)'
    # Polarity attaches to the operative act, not to every occurrence of 不:
    # 无权代理 and 不可归责 are triggers, not negated remedies.
    denials = {
        'mandate_relationship':r'(?:不委托|不负责|无需处理|不得处理)',
        'mandate_proportional_remuneration':r'(?:无须|无需|不必|不予|不再|不得|不)(?:向[^，。]{1,12})?(?:支付|结算)[^。]{0,20}'+fee,
        'mandate_exit_handover':r'(?:无须|无需|不必|不得|不予)[^。]{0,10}(?:移交|交接|返还)',
        'mandate_exit_loss_liability':r'(?:无须|无需|不必|不承担|免于|免除)[^。]{0,15}(?:赔偿|补偿)',
        'mandate_unauthorized_liability':r'(?:无须|无需|不承担|免于|免除)[^。]{0,15}赔偿',
        'mandate_final_report':r'(?:无须|无需|不必|不得)[^。]{0,10}(?:提交|报告|汇报|提供)',
    }
    for requirements in profiles.values():
        for spec in requirements:
            if spec['element_id'] in denials:
                spec.setdefault('excluded_patterns',[]).append(denials[spec['element_id']])
    profiles['agency_termination_handover'][1]['required_context']={
        'direct':end, 'anaphor':r'交接(?:完成)?后',
        'antecedent':r'(?:解除|终止)[^。]{0,150}(?:交接|移交)'}
    profiles['agency_termination_compensation_scope'][1]['required_context']={
        'direct':end,'anaphor':r'赔偿(?:范围)?包括',
        'antecedent':r'(?:解除|终止)[^。]{0,120}赔偿'}
    # A clause spelling out repayment never supplies the distinct interest atom.
    # Express statutory incorporation is distinct from spelling out the scope.
    # It supplies the paid mandate's scope only in an operative exit liability clause.
    if paid:
        statutory=relation('mandate_exit_profit_scope','有偿委托解除赔偿明示范围或明确援引法定范围',
            {'exit':end,'loss':r'(?:造成|导致)[^。；]{0,15}损失',
             'incorporation':r'(?:按照法律规定|依照法律规定|依法)[^。；]{0,12}(?:承担|予以)[^。；]{0,8}赔偿'})
        scope=profiles['agency_termination_compensation_scope'][1]
        scope['semantic_patterns']+=statutory['semantic_patterns']
        scope['relation_slots'].extend(statutory['relation_slots'])
        scope['proposition']=statutory['proposition']
        scope.setdefault('excluded_patterns',[]).extend([
            r'(?:不赔偿|不包括|不承担|排除)[^。；]{0,15}(?:可得利益|履行利益|预期利润)',
            r'(?:仅|只)[^。；]{0,8}赔偿[^。；]{0,8}直接损失'])
    return profiles

def apply(items,clauses,text):
    from review_v2.engine import _set_item_pass,_set_item_partial,_set_item_missing,_set_item_not_applicable
    shared=facts(text)
    for i in items:
        i.decision_trace['agency_shared_facts']=shared
        gate=prerequisite(text,i.node_id)
        if gate is not None:
            active,condition=gate
            i.applicable_if=condition
            i.applicability.update(condition=condition,applicable=active,triggered=active,status='APPLICABLE' if active else 'NOT_APPLICABLE')
            if not active:
                _set_item_not_applicable(i,condition+'；当前未触发。');i.related_risks=[];continue
        # Coverage refinement must not reactivate a branch the applicability
        # stage already excluded (e.g. an express absence of subdelegation).
        if i.coverage_status=='不适用':continue
        requirements=specs(paid=shared['paid']).get(i.node_id)
        if not requirements:continue
        for s in requirements:s['evidence_unit']='clause'
        audit={}
        hits=corpus_facts(clauses,requirements,audit=audit)
        i.decision_trace['canonical_semantic_audit']=audit
        i.decision_trace['require_canonical_validation']=True
        covered=[s for s in requirements if hits[s['element_id']]]
        i.decision_trace['semantic_requirements']=requirements
        if len(covered)==len(requirements):_set_item_pass(i,[],'原文已覆盖：'+'、'.join(s['proposition'] for s in covered),'绑定条款直接支持。')
        elif covered:_set_item_partial(i,[],i.risk_level,'部分约定已有原文支持。','尚需补充未覆盖要素。')
        else:_set_item_missing(i,i.risk_level,'未找到相应正向事实。','需补充对应约定。','全文语义检索')
        i.evidence_clauses=[e for s in requirements for e in hits[s['element_id']]]
        i.evidence_location='；'.join(dict.fromkeys(e['location'] for e in i.evidence_clauses))
    return items
