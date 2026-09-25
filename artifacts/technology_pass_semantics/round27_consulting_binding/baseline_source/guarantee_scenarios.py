"""Guarantee prerequisites use transaction facts, never absence of boilerplate."""
import re
from datetime import date
from review_v2.guarantee_party_facts import extract_guarantee_parties

CONDITIONS = {
    'state_org_guarantor_forbidden': '保证人为机关法人时适用',
    'public_nonprofit_guarantor_forbidden': '保证人为公益非营利主体时适用',
    'single_written_guarantee': '存在独立保证函、担保函或单方保证文件时适用',
    'main_debt_limitation_disclosure': '既有或已到期债务可能涉及诉讼时效时适用',
    'guarantee_scope_exclusions': '存在限额、比例、部分债务或费用排除等限制保证意图时适用',
    'assignment_transfer_attachment': '实际发生债权转让、债务转移或明确存在相应文件时适用',
    'guarantee_attachment_integrity': '正文引用需核验的附件或实际存在附件结构时适用',
    'credit_reporting_eligibility': '约定征信查询或报送时适用',
}


def operative(text):
    for p in re.split(r'[。；\n]',text):
        if not re.search(r'如果|如发生|若|拟|将来|未来|可以|有权|可将|法律规定|例如|不涉及|未发生',p):
            yield p


def attachment_inventory(text):
    # A reference is not an uploaded attachment. Only separately delimited,
    # substantive annex text counts as supplied content in the same package.
    headings=list(re.finditer(r'(?m)^\s*附件\s*[一二三四五六七八九十\d]+\s*[:：、.\s]\s*([^\n]+)',text))
    actual=[]
    for n,h in enumerate(headings):
        body=text[h.end():headings[n+1].start() if n+1<len(headings) else len(text)]
        complete=(len(body.strip())>100 and len(re.findall(r'第[一二三四五六七八九十\d]+条',body))>=2
                  and not re.search(r'待提供|未提供|另行提供|仅列目录|正文略',body[:150]))
        actual.append({'name':h[1].strip(),'source':'UPLOADED_ANNEX_BODY','complete':complete,
                       'start':h.start(),'length':len(body)})
    references=list(dict.fromkeys(re.findall(r'《([^》]*(?:协议|合同|保证函|通知书)[^》]*)》',text)))
    required=bool(re.search(r'附件|主合同',text))
    return {'references':references,'provided_documents':actual,'required':required,
            'status':'VERIFIED' if actual and all(d['complete'] for d in actual) and all(any(r in d['name'] for d in actual) for r in references)
                     else 'PENDING_VERIFICATION' if required else 'NOT_APPLICABLE'}


def extract(text, as_of=None):
    f=extract_guarantee_parties(text)
    now=as_of or date.today()
    date_pattern=r'(\d{4})年(\d{1,2})月(\d{1,2})日'
    period=re.search(r'(?:借款期限|主债务.{0,8}期限)[^。\n]{0,35}?'+date_pattern+r'\s*(?:至|到)\s*'+date_pattern,text)
    maturity=None
    if period:
        try: maturity=date(*map(int,period.groups()[3:]))
        except ValueError: pass
    historical=any(re.search(r'既有债务|历史债务|已逾期|已到期|时效已届满|超过诉讼时效',p) for p in operative(text))
    status='HISTORICAL_OR_OVERDUE' if historical or maturity and maturity<now else 'UNMATURED' if maturity else 'UNKNOWN'
    unilateral=bool(re.search(r'^\s*(?:保证函|担保函|保证书|单方保证声明)',text)) or any(
        re.search(r'(?:已出具|另行出具|出具了|附件[一二三\d：: ]).{0,20}(?:保证函|担保函|承诺函|保证书|单方保证声明)',p) for p in operative(text))
    transfer=any(re.search(r'(?:已签订|已签署|已经签署|附件.{0,12})(?:.{0,15})(?:债权转让|债务转移|债务承担|承继|转让通知)(?:协议|文件|书)?|(?:债权|债务)已(?:经)?(?:转让|转移)',p) for p in operative(text))
    limited=bool(re.search(r'限额保证|部分保证|保证比例|最高额保证|最高保证(?:金额|额)|保证责任(?:上限|比例)|仅(?:对|就).{0,30}(?:特定|部分|编号).{0,20}(?:债务|债权)|不(?:担保|承担).{0,15}(?:利息|罚息|费用)|保证.{0,15}\d+\s*%',text))
    inventory=attachment_inventory(text)
    f.update(main_contract_status=status,maturity_date=maturity.isoformat() if maturity else None,
             guarantee_scope_type='LIMITED' if limited else 'FULL' if re.search(r'全部.{0,12}本金|保证人全部承担',text) else 'UNSPECIFIED',
             unilateral_guarantee_document_detected=unilateral,transfer_document_detected=transfer,
             attachment_inventory=inventory,credit_activity=bool(re.search(r'征信|金融信用信息基础数据库',text)))
    return f


def applicable(node,f):
    if node not in CONDITIONS:return None
    kind=f['guarantee_party_type']
    return {
        'state_org_guarantor_forbidden':kind in {'STATE_ORGAN','MIXED','UNKNOWN'},
        'public_nonprofit_guarantor_forbidden':kind in {'PUBLIC_NONPROFIT','MIXED','UNKNOWN'},
        'single_written_guarantee':f['unilateral_guarantee_document_detected'],
        'main_debt_limitation_disclosure':f['main_contract_status']=='HISTORICAL_OR_OVERDUE',
        'guarantee_scope_exclusions':f['guarantee_scope_type']=='LIMITED',
        'assignment_transfer_attachment':f['transfer_document_detected'],
        'guarantee_attachment_integrity':f['attachment_inventory']['required'],
        'credit_reporting_eligibility':f['credit_activity'],
    }[node]
