"""Operative loan propositions, with local polarity and typed operators.

No rule identifiers or fixture entities: callers bind these facts to their
own requirements. Returned quotes are unchanged source substrings.
"""
import re


REFERENCE_RATE = r'(?:本合同|合同|正常|原|执行|借期)(?:约定|正常|借款|贷款|执行|的|内)*利率'


def rate_adjustment(text):
    compact = re.sub(r'\s+', '', text)
    m = re.search(REFERENCE_RATE + r'(?:的|基础上|为基础)?(?:按)?(?P<op>上浮|加收|增加|下浮)?(?P<value>\d+(?:\.\d+)?)(?P<unit>倍|%|％)', compact)
    if not m or re.search(r'不按|不得按|不再按|禁止', compact[max(0,m.start()-12):m.start()]):
        return None
    value = float(m['value'])
    op = m['op']
    if op and m['unit']=='倍':
        return None  # Do not guess ambiguous "increase by N times".
    multiplier = value if m['unit']=='倍' else value/100
    if op:
        multiplier = 1-multiplier if op=='下浮' else 1+multiplier
    if multiplier < 0:
        return None
    return {'operator':'MULTIPLY_REFERENCE_RATE','multiplier':multiplier,
            'reference':'CONTRACT_REGULAR_RATE','expression':m.group(),
            'start':m.start(),'end':m.end(),
            'normalization_reason':'引用利率×倍率；百分比为比例，上浮/加收为增量'}


def segments(text):
    return [s.strip() for s in re.split(r'(?<=[。；;\n])|[，,](?=(?:但|不得|禁止))',text) if s.strip()]


def business_purposes(text):
    facts=[]
    purpose_context=None
    prohibited=False
    activity = r'生产经营|经营周转|资金周转|日常经营|流动资金|采购[^。；]{0,16}(?:设备|材料|原料|货物)|支付[^。；]{0,16}(?:货款|供应商|工资)'
    for sentence in segments(text):
        s=re.sub(r'\s+','',sentence)
        own_link=bool(re.search(r'(?:借款|贷款|资金)[^。；]{0,18}(?:用于|用作|用以|用途|为|因)|因[^。；]{0,35}(?:经营|采购)[^。；]{0,20}(?:资金|借款)',s))
        if re.search(r'(?:借款|贷款|资金)[^。；]{0,20}(?:用于|用途)[：:]$',s):
            purpose_context=sentence
            prohibited=bool(re.search(r'不得|禁止|不能|不用于',s))
            continue
        is_list=bool(re.match(r'[（(]?\d+[）).、]',s))
        linked=own_link or (purpose_context and is_list)
        negative=bool(re.search(r'不得|禁止|不能|不用于|无关|非经营',s)) or (prohibited and not own_link)
        if linked and re.search(activity,s) and not negative:
            quote=sentence
            if not own_link:
                # Include the governing purpose introduction, not a bare list noun.
                start=text.index(purpose_context)
                end=text.index(sentence,start)+len(sentence)
                quote=text[start:end]
            facts.append({'quote':quote,'polarity':'POSITIVE',
                          'directness':2 if re.search(r'用于|用作|用以',s) else 1,
                          'normalization_reason':'借款用途/需求与经营活动存在正向关系；排除禁止和无关用途'})
        if not is_list:
            purpose_context=None
            prohibited=False
    return facts


def payment_allocations(text):
    facts=[]
    for sentence in segments(text):
        s=re.sub(r'\s+','',sentence)
        context=bool(re.search(r'抵充|冲抵|清偿|偿还|还款|付款|支付的款项',s))
        order=bool(re.search(r'依次|顺序|顺位|先[^。；]{0,35}(?:再|后)|→|->',s))
        categories=sorted([p for p in ('费用','违约金','利息','本金') if p in s],key=s.index)
        if context and order and len(categories)>=2 and not re.search(r'不按|不适用|并非|仅为示例|尚未确定',s):
            if re.search(r'保险增信|保费',s) and not re.search(r'抵充|冲抵|不足以清偿|未注明',s):
                continue
            facts.append({'quote':sentence,'polarity':'POSITIVE','ordered_categories':categories,
                          'normalization_reason':'还款/清偿款项分配＋显式先后顺序＋多个债务类别'})
    # A list can be below its operative introduction within the same clause.
    if not facts and re.search(r'(?:抵充|冲抵|清偿顺序|偿还顺序)[：:]?\s*\n',text):
        s=re.sub(r'\s+','',text)
        if not re.search(r'不按|不适用|尚未确定|保险增信',s) and re.search(r'顺序|依次|→|->',s) and '本金' in s and '利息' in s:
            facts.append({'quote':text,'polarity':'POSITIVE',
                          'normalization_reason':'条款中的清偿顺序引言与连续列举共同证明分配顺位'})
    return facts


def concept_facts(concept,text):
    if concept=='business_purpose':
        return business_purposes(text)
    if concept=='payment_allocation':
        return payment_allocations(text)
    if concept=='overdue_rate':
        facts=[]
        for sentence in segments(text):
            s=re.sub(r'\s+','',sentence)
            if not re.search(r'逾期',s) or not re.search(r'利息|利率|罚息',s):
                continue
            if re.search(r'不计收|不收取|无需支付|不得计收|不按|不适用',s):
                continue
            adjustment=rate_adjustment(s)
            direct=bool(re.search(r'\d+(?:\.\d+)?[%％‰]|按[^。；]{0,12}(?:原|合同|执行)利率',s))
            if adjustment or direct:
                facts.append({'quote':sentence,'polarity':'POSITIVE',
                              'rate_adjustment':adjustment,
                              'normalization_reason':adjustment['normalization_reason'] if adjustment else '直接逾期费率或引用执行利率'})
        return facts
    if concept in {'overdue_base','overdue_period'}:
        facts=[]
        for sentence in segments(text):
            s=re.sub(r'\s+','',sentence)
            if not re.search(r'逾期',s) or not re.search(r'利息|利率|罚息',s):
                continue
            if re.search(r'不计收|不收取|无需支付|不得计收',s):
                continue
            matched=(re.search(r'逾期(?:借款|贷款)?本金|未偿(?:还)?(?:本金|借款)|未还借款|按本金',s) if concept=='overdue_base'
                     else re.search(r'自逾期|逾期之日起|到期次日',s) and re.search(r'清偿|付清|还清|实际偿还|实际归还',s))
            if matched:
                facts.append({'quote':sentence,'polarity':'POSITIVE',
                              'normalization_reason':'计算基数或起止期与逾期计息在同一命题中关联'})
        return facts
    return []
