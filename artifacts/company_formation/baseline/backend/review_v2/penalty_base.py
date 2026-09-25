"""Cross-domain percentage penalty bases; source existence is not determinability."""
import re
from decimal import Decimal
from dataclasses import replace
from review_v2.priority_checklist_helpers import required, PROFILES
from review_v2.lease_semantics import requirement

NODE='common_penalty_base_determinability'
LOAN_BASE_ALIASES = ('借款总额', '借款金额', '本金', '合同借款本金', '借款本金')


def loan_base_definitions(text):
    """Resolve an unqualified principal reference only to one unique amount."""
    candidates = []
    pattern = r'(?:' + '|'.join(map(re.escape, LOAN_BASE_ALIASES)) + r')\s*(?:为|是|指|等于|=|：|:)\s*[^。；\n]{0,100}'
    for match in re.finditer(pattern, text):
        amount = re.search(r'(?:￥|¥|人民币)?\s*([\d,，]+(?:\.\d+)?)\s*(万|亿)?元', match.group())
        if amount:
            value = Decimal(amount[1].replace(',', '').replace('，', ''))
            value *= {'万': 10000, '亿': 100000000, None: 1}[amount[2]]
            candidates.append((value, match.group()))
    return list(dict.fromkeys(q for _, q in candidates)) if len({v for v, _ in candidates}) == 1 else []


def tariff_base_definitions(base, text):
    """A unit freight reference resolves through an agreed, populated tariff.

    A bare 'see quotation' or a hypothetical example is insufficient. Different
    route/equipment rows are a verifiable pricing function, not competing totals.
    """
    if not re.fullmatch(r'(?:该|本|当|每)(?:柜|车|票|批|趟)(?:的)?(?:运输费用|运输费|运费)',base):
        return []
    reference=re.search(r'(?:运输费|运费)[^。\n]{0,100}(?:双方签章|双方签字|双方确认|签章确认)[^。\n]{0,40}(?:报价单|价格表|价目表)[^。\n]{0,15}为准',text)
    if not reference: return []
    rows=[]
    keys={}
    for line in text.splitlines():
        if re.search(r'例如|假设|如某',line): continue
        m=re.search(r'(.{3,100}?(?:运输费|运费)|.{3,100}?[：:])\s*(?:人民币)?\s*([\d,，]+(?:\.\d+)?)元\s*[/／每]\s*(柜|车|票|批|趟)',line)
        if m:
            key=re.sub(r'\s+','',m[1])
            value=Decimal(m[2].replace(',','').replace('，',''))
            if key in keys and keys[key]!=value: return []
            keys[key]=value
            rows.append(m.group())
    return [reference.group()]+rows if rows else []
def periodic_base_definitions(base, text):
    """Resolve an indexed period fee to its unit-price definition, not a total."""
    match=re.fullmatch(r'(?:当|本|该|每)(月|年|日)([^。；]{1,12}费)',base)
    if not match: return []
    period,fee=match.groups()
    pattern=re.escape(fee)+r'[^。；\n]{0,25}(?:每|按)'+period+r'(?:人民币)?\s*([\d,，]+(?:\.\d+)?)元'
    rows=[m for m in re.finditer(pattern,text) if not re.search(r'违约金|逾期|例如|假设',m.group())]
    values={Decimal(m[1].replace(',','').replace('，','')) for m in rows}
    return [m.group() for m in rows] if len(values)==1 else []

CHECKPOINT=required('COMMON', 20, NODE, '违约金计算基数可确定性', ('违约金','计算基数'),
    '《民法典》第510条、第577条、第585条', [
        ('违约金比例及对应基数约定', (r'\d+(?:\.\d+)?\s*[%％][^。；]{0,25}违约金',)),
        ('比例所引用基数的金额或确定方法', (r'(?!)',)),
    ], risk='中', suggestion='明确违约金引用基数的金额、对应交易或可验证计算方法，并与付款及结算条款衔接。')
CHECKPOINT = replace(CHECKPOINT, applicable_if='合同存在按比例计算的违约金，且计算依赖某一金额基数时适用。')


def analyze(text):
    result=[]
    amount=r'(?:人民币)?\s*[\d,，]+(?:\.\d+)?\s*(?:万|亿)?元'
    for m in re.finditer(r'(?:按(?:照)?|支付|承担)?(?P<base>[\u4e00-\u9fff]{2,18}?)(?:的)?\s*(?P<rate>\d+(?:\.\d+)?)\s*[%％][^。；\n]{0,20}违约金',text):
        sentence=re.split(r'[。；\n]',text[:m.start()])[-1]
        if re.search(r'例如|假设|举例',sentence):
            continue  # An illustration is not a second operative percentage base.
        base=m['base'].removeprefix('还应').removeprefix('应当').removeprefix('支付')
        base=re.split(r'按照|按',base)[-1]
        base=base.removesuffix('的')
        base=re.sub(r'(?:每日|每天|按日|每月|按月)$','',base)
        definitions=[]
        if re.fullmatch(r'(?:应付未付|逾期未付|尚未支付|未付|未支付|应付|已付|已收)(?:款项|款|金额|款金额)|实际损失|合同价款|合同总价款',base):
            definitions.append(m.group())
        pattern=re.escape(base)+r'\s*(?:为|是|指|等于|=|：|:)\s*[^。；\n]{0,100}'
        for d in re.finditer(pattern,text):
            if re.search(amount,d.group()):
                definitions.append(d.group())
            else:
                expression=re.split(r'为|是|指|等于|=|：|:',d.group(),maxsplit=1)[-1]
                operands=re.split(r'加上|减去|扣除|乘以|[+\-×]',expression)
                if len(operands)>1 and all(re.search(re.escape(term.strip())+r'\s*(?:为|是|：|:)?\s*'+amount,text) for term in operands):
                    definitions.append(d.group())
        if re.fullmatch(r'(?:尚未支付款项|未付款金额|未付金额|未支付款项|欠款金额)',base):
            totals=re.search(r'(?:合同总价|合同金额|总价款|应付款项|应付款金额)\s*(?:为|：|:)?\s*'+amount,text)
            payment=re.search(r'(?:已付|已支付|已付款|付款记录|付款凭证|支付凭证)',text)
            if totals and payment:
                definitions.append(totals.group()+'；存在付款金额或记录，可据此计算未付款余额')
        # Standard contract price aliases share a defined total, arbitrary fees do not.
        if base in {'合同金额','合同总价','合同总价款','合同价款'}:
            d=re.search(r'(?:合同金额|合同总价|合同总价款|合同价款)\s*(?:为|：|:)?\s*'+amount,text)
            if d: definitions.append(d.group())
        if base in LOAN_BASE_ALIASES:
            definitions = loan_base_definitions(text)
        periodic=periodic_base_definitions(base,text)
        if periodic: definitions=periodic
        tariff=tariff_base_definitions(base,text)
        if tariff: definitions=tariff
        result.append({'base':base,'rate':float(m['rate']),'quote':m.group(),'start':m.start(),'end':m.end(),
                       'definitions':definitions,'status':'DETERMINABLE' if definitions else 'UNDEFINED'})
    return result


def augment(checklist,text):
    if analyze(text) and not any(c.node_id==NODE for c in checklist):
        return tuple(checklist)+(CHECKPOINT,)
    return checklist


def resolve(text):
    all_rows=analyze(text)
    if all_rows and all(r['status']=='DETERMINABLE' for r in all_rows):
        return [requirement(NODE+'_ratio','违约金比例及对应基数约定',*(re.escape(r['quote']) for r in all_rows)),
                requirement(NODE+'_definition','比例基数有金额或可验证动态计算方法',*(re.escape(d) for r in all_rows for d in r['definitions']))]
    unresolved=[r for r in analyze(text) if r['status']=='UNDEFINED']
    return [requirement(NODE+'_ratio','违约金比例及对应基数约定',*(re.escape(r['quote']) for r in unresolved)),
            requirement(NODE+'_definition','违约金基数（'+'、'.join(dict.fromkeys(r['base'] for r in unresolved))+'）的金额或可验证确定方法',
                *(re.escape(r['base'])+r'\s*(?:为|是|指|等于|=|：|:)\s*(?:人民币)?\s*[\d,，]+(?:\.\d+)?\s*(?:万|亿)?元' for r in unresolved))]
