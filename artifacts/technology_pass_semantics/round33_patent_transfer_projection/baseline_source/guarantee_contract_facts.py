"""Canonical guarantee coverage, separated from maximum-guarantee ceilings."""
import re
from review_v2.guarantee_party_facts import extract_guarantee_parties, signature_mismatches
from review_v2.lease_semantics import requirement, corpus_facts
from review_v2.guarantee_mode import extract_mode

PRINCIPAL_AMOUNT_PATTERN = r'(?:借款(?:本金|金额|人民币)|主债权(?:本金|金额)|本金)[^。\n\d]{0,40}(?:小写[:：]?\s*)?([\d,，]+(?:\.\d+)?)\s*([万亿]?)元'


def extract(text, clauses):
    facts=extract_guarantee_parties(text)
    facts['guarantee_type']=extract_mode(clauses)['mode']
    facts['amount_mode']='MAXIMUM' if re.search(r'最高额保证|最高债权额|最高额担保',text) else 'FIXED'
    matches=re.findall(PRINCIPAL_AMOUNT_PATTERN,text)
    facts['fixed_principal_amount']=(float(matches[0][0].replace(',','').replace('，','')) * {'':1,'万':10000,'亿':100000000}[matches[0][1]]) if matches and facts['amount_mode']=='FIXED' else None
    facts['signature_mismatches']=signature_mismatches(text,facts)
    return facts


def apply(items,clauses,text):
    from review_v2.engine import _set_item_pass, _set_item_missing
    facts=extract(text,clauses)
    amount_pattern=(r'(?:最高债权额|最高限额|最高保证额|最高额).{0,20}[\d,，]+(?:\.\d+)?\s*[万亿]?元' if facts['amount_mode']=='MAXIMUM'
                    else PRINCIPAL_AMOUNT_PATTERN)
    profiles={
      'written_guarantee_contract':[requirement('guarantee_written_instrument','保证合同以书面文书或合同签署机制体现',
          r'(?:本合同|本保证合同|本担保合同)[^。]{0,45}(?:当事人|双方|各方)?[^。]{0,15}(?:签字|签署|签名|盖章)[^。]{0,25}(?:生效|成立)',
          r'(?:保证合同|担保合同|本保证)(?:应当|应|须|必须)?(?:采用|以)书面形式')],
      'guarantee_period_agreed':[requirement('guarantee_period_duration','保证期间的起算及具体期限',
          r'(?:保证期间|保证期限|担保期限)[^。]{0,80}(?:届满|到期|之日)[^。]{0,20}[一二两三四五六七八九十\d]+(?:个)?(?:年|月|日)',
          r'(?:保证期间|保证期限)[^。]{0,20}自\d{4}年[^。]{0,40}(?:至|到)\d{4}年')],
      'debt_transfer_guarantor_consent':[requirement('guarantee_debt_transfer_written_consent','债务转移须经保证人书面同意',
          r'(?:债务转移|转移[^。；]{0,15}债务|转让[^。；]{0,25}债务)[^。；]{0,45}(?:应|须|需)[^。；]{0,12}保证人书面同意',
          r'未经保证人书面同意[^。]{0,45}(?:转移|转让)[^。]{0,30}债务[^。]{0,40}不承担保证责任')],
      'guarantee_principal_amount_cap':[requirement('guarantee_principal_amount','最高债权额明确' if facts['amount_mode']=='MAXIMUM' else '固定主债权本金明确',amount_pattern)],
      'main_contract_change_consent':[requirement('guarantee_change_consent','主合同变更同意机制或未经同意加重部分免责',r'未经保证人(?:书面)?同意[^。]{0,180}加重[^。]{0,60}不承担保证责任',r'(?:主合同.{0,20}变更|变更主合同)[^。；]{0,50}(?<!无)(?:应|须|需)[^。；]{0,10}保证人书面同意')],
      'debt_reduction_effect':[requirement('guarantee_debt_reduction','减轻债务后继续承担保证责任',r'减轻[^。；]{0,35}债务[^。；]{0,80}保证人仍[^。；]{0,50}承担保证责任')],
      'loan_extension_guarantor_consent':[requirement('guarantee_extension_period','展期书面确认或未经同意时保留原保证期间',r'(?:履行期限|展期|延期)[^。]{0,60}未经保证人书面同意[^。]{0,60}保证期间[^。]{0,50}(?:原合同|不受影响|原约定)',r'(?:履行期限|展期|延期)[^。；]{0,50}(?<!无)(?:应|须|需)[^。；]{0,10}保证人书面(?:确认|同意)')],
      'change_notice_record':[requirement('guarantee_change_notice_record','变更通知或全部合同文件往来的可留痕传递方式',r'(?:主合同|主债务)[^。]{0,25}变更[^。]{0,80}(?:通知|确认)[^。]{0,80}(?:书面|邮件|签收|补充协议|确认函)',r'(?:本合同|双方)[^。]{0,30}(?:全部|所有)通知[^。]{0,130}(?:快递|邮件|签收|书面送达)')],
    }
    for item in items:
        item.decision_trace['guarantee_shared_facts']=facts
        specs=profiles.get(item.node_id)
        if not specs: continue
        hits=corpus_facts(clauses,specs)
        item.decision_trace['semantic_requirements']=specs
        evidence=[e for s in specs for e in hits[s['element_id']]]
        if evidence:
            _set_item_pass(item,[], '原文已覆盖：'+'、'.join(s['proposition'] for s in specs),'已由绑定原文证据确认。')
        else:
            _set_item_missing(item,item.risk_level,'尚未找到：'+specs[0]['proposition'],'需补充对应明确约定。','全文语义检索')
        item.evidence_clauses=evidence
        item.evidence_location='；'.join(dict.fromkeys(e['location'] for e in evidence))
    # Signature classification is owned by guarantee_closure, using this shared snapshot.
    return items
