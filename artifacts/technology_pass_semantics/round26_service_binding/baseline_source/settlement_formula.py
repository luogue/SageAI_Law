"""Symbolic shortfall expressions keep unknown actual turnover as an input."""
import re
from review_v2.priority_checklist_helpers import required as R

def penalty_expressions(text):
    """Do not equate a computable amount with a proportionate penalty."""
    results=[]
    for s in re.split(r'[。\n]',text):
        if not re.search(r'违约金|赔偿|罚款',s): continue
        multiple=re.search(r'(运输费用|运费|合同价款)(?:的)?(\d+(?:\.\d+)?)倍',s)
        rate=re.search(r'(合同额|合同总额|业务总额)(?:的)?(\d+(?:\.\d+)?)[%％]',s)
        fixed=re.search(r'违约金(?:为|人民币|：|:)?\s*(\d+(?:\.\d+)?)(万)?元',s)
        if multiple:
            value=float(multiple[2]); kind='MULTIPLE'; formula=f'{multiple[1]} * {value:g}'
            assessment='HIGH_MULTIPLE_REQUIRES_LOSS_REVIEW' if value>=2 else 'LOSS_CONTEXT_REQUIRED'
        elif rate:
            value=float(rate[2])/100;kind='PERCENTAGE';formula=f'{rate[1]} * {value:g}';assessment='LOSS_CONTEXT_REQUIRED'
        elif fixed:
            value=float(fixed[1])*(10000 if fixed[2] else 1);kind='FIXED';formula=str(value);assessment='LOSS_CONTEXT_REQUIRED'
        else: continue
        results.append({'quote':s,'kind':kind,'formula':formula,'assessment':assessment,
          'legal_basis':'《民法典》第584条、第585条；合同编通则司法解释第65条',
          'legal_nature':'约定违约责任，不是行政处罚','external_inputs':['可证明损失','履行利益','履约情况及过错']})
    return results

def analyze(text):
    rows=[]
    for match in re.finditer(r'[^。\n]*(?:补足|保底|最低收益)[^。\n]*',text):
        quote=match.group()
        if not re.search(r'最低(?:业绩|采购|销售|收入|收益)|保底|业绩承诺|业务(?:额|基数)|销售额|收入额|收益额|年度基数|采购额',quote):
            continue
        base=re.search(r'(?:基数|保底|最低收益)[^\d]{0,10}([\d,.]+)\s*(万)?元?',quote)
        rate=re.search(r'(?:未完成部分|差额)[^。\n]{0,15}按\s*(\d+(?:\.\d+)?)\s*[%％][^。\n]{0,8}补足',quote)
        value=float(base[1].replace(',',''))*(10000 if base[2] else 1) if base else None
        resolved=bool(base and rate)
        rows.append({'quote':quote,'status':'RESOLVED' if resolved else 'AMBIGUOUS','base':value,
          'rate':float(rate[1])/100 if rate else None,'formula':f'max(0, {value:g} - actual_period_turnover) * {float(rate[1])/100:g}' if resolved else None,
          'required_inputs':['actual_period_turnover'],'reason':'需核验实际业务额及对账数据' if resolved else '未明确补足对象及其与业务基数、收益比例的关系，不能唯一构造补足公式'})
    return rows

CHECKPOINT=R('COMMON',23,'common_shortfall_formula','差额补足金额计算及确认机制',('补足','基数'), '《民法典》第510条、第511条、第584条、第585条',[
 ('补足义务安排',(r'补足|保底|最低收益',)),
 ('补足对象、基数及适用比例形成唯一公式',(r'(?:基数)[^。\n]{0,30}\d+[^。\n]{0,40}(?:未完成部分|差额)[^。\n]{0,15}按\s*\d+(?:\.\d+)?[%％][^。\n]{0,8}补足',)),
 ('业务额统计及争议确认机制',(r'(?:业务额|收入|基数)[^。\n]{0,50}(?:对账|核对)[^。\n]{0,50}(?:异议|确认)',))])
def augment(checklist,text):
    return tuple(checklist)+(CHECKPOINT,) if re.search(r'补足|保底|最低收益',text) and not any(c.node_id==CHECKPOINT.node_id for c in checklist) else tuple(checklist)


def applicability(text):
    facts=analyze(text)
    return {'status':'APPLICABLE' if facts else 'NOT_APPLICABLE',
      'applicable':bool(facts),'triggered':bool(facts),'condition':'BUSINESS_PERFORMANCE_SHORTFALL',
      'trigger_evidence':facts,
      'reason':'存在业务金额承诺及补差机制。' if facts else '未发现最低业绩或业务金额补差机制；普通清偿不足的债务余额不适用业务额补差规则。'}
