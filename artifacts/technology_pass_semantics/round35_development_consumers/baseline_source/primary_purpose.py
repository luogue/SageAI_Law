"""Transaction structure is primary; shared performance clauses are features only."""
import re

PROFILES = {
    'GUARANTEE': (r'(?:最高额)?保证合同|保证担保合同', {
        'parties': r'保证人', 'creditor_debtor': r'债权人|债务人',
        'secured_debt': r'主债权|主合同', 'undertaking': r'连带责任保证|承担保证责任|一般保证责任',
        'period': r'保证期间', 'scope': r'保证范围|担保的范围',
        'recourse': r'追偿|债务转移.{0,25}保证人'}),
    'HOUSE_LEASE': (r'(?:房屋|住宅|商铺)?租赁合同', {
        'lessor': r'出租[人方]', 'lessee': r'承租[人方]',
        'rent': r'租金', 'period': r'租赁期限|租期', 'return': r'退租|返还房屋'}),
    'SALE': (r'买卖合同|采购合同|购销合同|供货合同', {
        'seller': r'出卖人|卖方|供方', 'buyer': r'买受人|买方|需方',
        'goods': r'货物|产品|设备', 'payment': r'货款|价款', 'delivery': r'交货|交付|验收'}),
    'LABOR': (r'劳动合同|劳动用工合同', {
        'employer': r'用人单位', 'employee': r'劳动者', 'pay': r'工资|劳动报酬',
        'work': r'工作岗位|工作时间', 'insurance': r'社会保险|社保'}),
    'TECHNOLOGY': (r'技术服务合同|技术咨询合同', {
        'work': r'技术服务|技术咨询', 'obligation': r'委托|提供|负责',
        'payment': r'服务费|报酬', 'result': r'技术成果|技术报告|验收'}),
    'CONFIDENTIALITY': (r'保密协议|保密合同', {
        'information_flow': r'披露方[\s\S]{0,400}(?:接收方|接受方)|一方向另一方披露|双方向对方披露',
        'information': r'保密信息|商业秘密', 'use_restriction': r'仅.{0,25}(?:使用|用于)|不得.{0,15}(?:披露|泄露|使用)',
        'duration': r'保密期限|保密义务.{0,20}(?:年|终止|持续)',
        'return': r'返还.{0,15}(?:资料|信息)|销毁', 'remedy': r'违反.{0,20}保密|泄露.{0,25}赔偿'}),
}

def analyze(text, clauses):
    heading=next((s.strip() for s in text.splitlines() if s.strip()), '')[:100]
    heading=re.split(r'[。；]',heading)[0]
    evidence=[]; detected={}; scores={}; named=[]
    for family,(title,groups) in PROFILES.items():
        # Titles refer to the document heading, never an annex or a body reference.
        title_hit=bool(re.search(title,heading))
        if title_hit: named.append(family)
        hits=[]
        for name,pattern in groups.items():
            match=re.search(pattern,text)
            if not match: continue
            hits.append(name)
            evidence.append({'signal_type':name,'signal':match[0],'target_family':family,'weight':4,
                'source_clause_ids':[c.clause_id for c in clauses if re.search(pattern,c.text)][:8]})
        detected[family]=hits
        scores[family]=len(hits)*4+(12 if title_hit else 0)
    candidates=[]
    for family,hits in detected.items():
        if family=='CONFIDENTIALITY':
            qualifies={'information_flow','information'}<=set(hits) and len(hits)>=4
        else: qualifies=len(hits)>=(3 if family in named else 4)
        if qualifies:candidates.append(family)
    # Another named operative transaction keeps embedded guarantees/IP/secrecy secondary.
    titled=[f for f in candidates if f in named]
    if titled:candidates=titled
    elif (re.fullmatch(r'[\w（）()/\- ]{0,30}(?:合同|协议)(?:书)?',heading)
          and not re.search(r'签订|订立|主合同|本合同|双方|甲方|乙方|债权人|债务人',heading)
          and named!=['CONFIDENTIALITY']):
        candidates=[]  # An existing domain classifier handles other named transactions.
    ordered=sorted(candidates,key=lambda f:scores[f],reverse=True)
    primary=ordered[0] if ordered and (len(ordered)==1 or scores[ordered[0]]-scores[ordered[1]]>=4) else None
    secondary=[label for label,pattern in [('CONFIDENTIALITY',r'保密|商业秘密'),('NOTICE',r'通知|送达'),
        ('DISPUTE_RESOLUTION',r'争议解决|仲裁|管辖法院|人民法院'),('INTELLECTUAL_PROPERTY',r'知识产权|专利权|著作权')]
        if re.search(pattern,text) and label!=primary]
    return {'primary_family':primary,'confidence':'high' if primary else 'low','scores':scores,
        'classification_evidence':evidence,'secondary_clause_features':secondary,
        'guarantee_features_detected':detected['GUARANTEE'],'nda_primary_features_detected':detected['CONFIDENTIALITY']}
