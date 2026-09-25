"""Company-law checks distinct from the presence of drafting provisions.

Law version: Company Law 2023, effective 2024-07-01, articles 47 and 84.
https://www.samr.gov.cn/xyjgs/flfg/art/2024/art_d4e84936a8a744f8928ac7aec7594345.html
"""
import re
from datetime import date
from calendar import monthrange


def deadline_assessment(text):
    result = dict(contribution_deadline_present=False, contribution_deadline_compliant=None,
                  status='MISSING', basis='UNRESOLVED', evidence=[], legal_basis='《公司法》第47条')
    sentences = re.split(r'[。\n]',text)
    targets=[s for s in sentences if re.search(r'出资|认缴|注册资本',s) and re.search(r'缴足|缴付|缴纳|实缴',s)]
    for s in targets:
        relative=re.search(r'(?:公司)?成立(?:之日)?起?[^。]{0,8}([一二三四五六七八九十\d]+)年内',s)
        if relative:
            n=int(relative[1]) if relative[1].isdigit() else '零一二三四五六七八九十'.index(relative[1])
            result.update(contribution_deadline_present=True,contribution_deadline_compliant=n<=5,
                          status='PASS' if n<=5 else 'RISK',basis='RELATIVE_TO_ESTABLISHMENT',evidence=[s])
            return result
        m=re.search(r'(\d{4})年(?:(\d{1,2})月(?:(\d{1,2})日)?)?(?:前|内)?[^。]{0,10}(?:缴足|缴付|缴纳|实缴)',s)
        if m:
            try:end=date(int(m[1]),int(m[2] or 12),int(m[3] or (28 if m[2]=='2' else 30 if m[2] in {'4','6','9','11'} else 31)))
            except ValueError:continue
            result.update(contribution_deadline_present=True,status='UNKNOWN',deadline=end.isoformat(),evidence=[s])
            break
    if not result['contribution_deadline_present']:return result
    start=None
    for s in sentences:
        m=re.search(r'(?:公司[^。]{0,8}(?:于|拟于|计划于)?)(\d{4})年(?:(\d{1,2})月(?:(\d{1,2})日)?)?[^。]{0,8}(?:设立|成立)|(?:成立|设立)(?:日期|时间)?[为：:\s]*(\d{4})年',s)
        if m:
            year=int(m[1] or m[4]);lo=date(year,int(m[2] or 1),int(m[3] or 1));hi=date(year,int(m[2] or 12),int(m[3] or 28))
            if not m[2]:hi=date(year,12,31)
            start=(lo,hi);result.update(basis='EXPLICIT_ESTABLISHMENT',establishment_evidence=s);break
    if start is None and re.search(r'拟设|共同设立|出资成立',text):
        for s in sentences:
            if re.search(r'合作期限|正式营业',s) and (m:=re.search(r'(\d{4})年',s)):
                start=(date(int(m[1]),1,1),date(int(m[1]),12,31))
                result.update(basis='PLANNED_OPERATION_YEAR_INFERENCE',establishment_evidence=s);break
    if start:
        lo,hi=start
        result['establishment_range']=[lo.isoformat(),hi.isoformat()]
        if lo>=date(2024,7,1):
            # An interval, not the signing date, bounds unknown day/month.
            earliest=date(lo.year+5,lo.month,min(lo.day,monthrange(lo.year+5,lo.month)[1]))
            latest=date(hi.year+5,hi.month,min(hi.day,monthrange(hi.year+5,hi.month)[1]))
            compliant=True if end<=earliest else False if end>latest else None
            result.update(contribution_deadline_compliant=compliant,status='PASS' if compliant is True else 'RISK' if compliant is False else 'UNKNOWN')
    return result


def deadline_evidence(clauses):
    text='\n'.join(c.text for c in clauses if c.section_type in {'正式合同条款','附件'})
    a=deadline_assessment(text)
    if a['status'] not in {'RISK','UNKNOWN'}:return []
    reason=('已约定出资缴付期限，但按正文的成立/拟设时间，该截止时间超过成立起五年的原则上限；应核对登记成立日及法律、行政法规或国务院决定的特殊规定并调整。' if a['status']=='RISK' else '已约定出资缴付期限，成立日或适用期间尚不能可靠确定；期限合法性待核验，不能仅因存在日期即认定合法。')
    if a['basis']=='PLANNED_OPERATION_YEAR_INFERENCE':reason+='拟设年份据合作/营业安排推定，不将合作起日或签署日当作已登记成立日。'
    return [dict(c.to_public_dict(),text=s,quote=s,original_excerpt=s,reason=reason,deadline_assessment=a)
            for c in clauses for s in a['evidence'] if s in c.text]


def transfer_assessment(text):
    old=re.search(r'[^。\n]*(?:股东以外|对外转让)[^。\n]*(?:过半数|二分之一以上)同意[^。\n]*',text)
    charter=re.search(r'(?:公司)?章程[^。\n]{0,45}(?:明确|特别|另有|约定|规定)[^。\n]{0,70}(?:转让|过半数|同意)',text)
    return dict(old_consent_mechanism=bool(old),charter_special_arrangement=bool(charter),
                status='CHARTER_VERIFICATION' if old and charter else 'UPDATE_REQUIRED' if old else 'DEFAULT_PROCEDURE',
                evidence=old.group() if old else '')


def transfer_evidence(clauses):
    text='\n'.join(c.text for c in clauses)
    a=transfer_assessment(text)
    if a['status']!='UPDATE_REQUIRED':return []
    return [dict(c.to_public_dict(),text=a['evidence'],quote=a['evidence'],original_excerpt=a['evidence'],
                 reason='股权对外转让机制仍采用旧式过半数同意安排，未明确章程特别约定依据；需结合现行公司法第84条的书面通知、同等条件优先购买及公司章程核对并更新，不直接认定该约定无效。')
            for c in clauses if a['evidence'] in c.text]


def account_context(text):
    from review_v2.shareholder_transaction_facts import transaction_facts
    facts=[dict(f,polarity='NEUTRAL',evidence_role='TRIGGER_CONTEXT',protective_coverage=False) for f in transaction_facts(text) if f['fact_type']=='personal_subscription_account']
    return dict(personal_account_receiver_identified=bool(facts),evidence=facts,
                conclusion='已确认收款账户及资金保管主体为个人或筹备收款主体；该事实不证明资金安全保护已覆盖。' if facts else '')
