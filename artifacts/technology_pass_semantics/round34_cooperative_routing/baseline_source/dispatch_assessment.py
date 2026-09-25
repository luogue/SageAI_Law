"""Deterministic legal thresholds over verified facts; uncertainty is not illegality."""
from datetime import date,timedelta

def position_state(s):
 b=set(s.values('dispatch.position_basis'))
 temporary=True if 'TEMPORARY' in b and any(0<x<=6 for x in s.values('dispatch.temporary_duration_months')) else False if True in s.values('dispatch.long_term_position') or any(x>6 for x in s.values('dispatch.temporary_duration_months')) else None
 auxiliary=False if False in s.values('dispatch.auxiliary_noncore') or 'REGULAR_CORE' in b else True if True in s.values('dispatch.auxiliary_noncore') and True in s.values('dispatch.auxiliary_procedure') else None
 substitute=True if True in s.values('dispatch.substitute') or 'SUBSTITUTE' in b else False if False in s.values('dispatch.substitute') else None
 states={'temporary':temporary,'auxiliary':auxiliary,'substitute':substitute}
 status='PASS' if any(v is True for v in states.values()) else 'RISK' if all(v is False for v in states.values()) else 'VERIFY'
 return {'status':status,'states':states,'concepts':['dispatch.position_basis','dispatch.long_term_position','dispatch.temporary_duration_months','dispatch.auxiliary_noncore','dispatch.auxiliary_procedure','dispatch.substitute'],
 'reason':'现有事实排除临时性、辅助性和替代性，派遣岗位不符合三性限制。' if status=='RISK' else '长期或常设仅影响临时性；需核实非主营服务岗位及辅助性认定程序、或替代暂时离岗人员的事实。'}

def pay_state(s):
 concepts=['salary.regular','dispatch.comparator_pay','dispatch.comparable_work','dispatch.equal_pay','dispatch.worker_pay_method','dispatch.comparator_pay_method']
 own=[v for v in s.values('salary.regular') if isinstance(v,dict) and v.get('component','TOTAL')=='TOTAL']
 other=[v for v in s.values('dispatch.comparator_pay') if isinstance(v,dict)]
 comparable=True in s.values('dispatch.comparable_work')
 for a in own:
  for b in other:
   if comparable and a.get('unit') in {'CNY/MONTH','CNY/HOUR','CNY/PIECE'} and a.get('unit')==b.get('unit') and a.get('component','TOTAL')==b.get('component','TOTAL') and a.get('amount') is not None and b.get('amount') is not None:
    if float(a['amount'])<float(b['amount']):return {'status':'RISK','concepts':concepts,'reason':f"被派遣劳动者正式工资{a['amount']}与同口径可比岗位工资{b['amount']}比较，约定报酬较低；两方工资及可比关系均已绑定原文。"}
 if comparable and s.get('dispatch.worker_pay_method') and s.get('dispatch.comparator_pay_method') and 'LOWER_ALLOWED' in s.values('dispatch.equal_pay'):
  return {'status':'RISK','concepts':concepts,'reason':'两方具体报酬分配办法及同岗可比关系均有原文，明确允许派遣劳动者适用较低待遇。'}
 if any(v in {'LOWER_ALLOWED','DIFFERENT_SYSTEM'} for v in s.values('dispatch.equal_pay')):
  known=[]
  if own:known.append('劳动者正式报酬')
  if other:known.append('对照岗位报酬')
  prefix='已识别'+ '及'.join(known)+'；' if known else ''
  return {'status':'VERIFY','concepts':concepts,'reason':prefix+'需核实双方是否采用相同工资组成、工作及计酬口径；不得只凭薪酬体系不同或单方工资推定实际低于。'}
 if 'EQUAL' in s.values('dispatch.equal_pay'):return {'status':'PASS','concepts':concepts,'reason':'存在同工同酬承诺；实际履行仍应按同口径核验。'}
 return {'status':'VERIFY','concepts':concepts,'reason':'需核实双方同岗位正式工资或报酬分配办法及可比口径，现有证据不足以判断实际差额。'}

def term_state(s):
 concepts=['contract.type','contract.duration_months','contract.start_date','contract.end_date']
 kinds=set(s.values('contract.type'))
 result={'concepts':concepts}
 if len(kinds)!=1:
  return {**result,'status':'VERIFY','reason':'需确认派遣劳动合同是否为固定期限，期限类型缺失或存在冲突。'}
 if kinds != {'FIXED'}:
  return {**result,'status':'RISK','reason':'劳务派遣应订立二年以上固定期限劳动合同，当前明确约定的期限类型不是固定期限。'}
 months=s.values('contract.duration_months')
 start=set(s.values('contract.start_date'));end=set(s.values('contract.end_date'))
 if any(m<24 for m in months):
  return {**result,'status':'RISK','reason':'已约定的固定期限劳动合同长度少于二年。'}
 if len(start)!=1 or len(end)!=1:
  return {**result,'status':'VERIFY','reason':'固定期限类型已确认，但劳动合同起止日期缺失或冲突，无法可靠完成两年期限校验；派遣期间不能代替劳动合同期间。'}
 from review_v2.employment_facts import add_months
 first=date.fromisoformat(next(iter(start)));last=date.fromisoformat(next(iter(end)))
 if last<first:
  return {**result,'status':'VERIFY','reason':'劳动合同终止日期早于起始日期，需核实有效日期后再校验期限。'}
 minimum=add_months(first,24)-timedelta(days=1)
 short=last<minimum
 return {**result,'status':'RISK' if short else 'PASS',
         'calculation':{'start_date':first.isoformat(),'end_date':last.isoformat(),'minimum_inclusive_end':minimum.isoformat(),'minimum_months':24},
         'reason':f'根据已验证劳动合同起止日期{first.isoformat()}至{last.isoformat()}（含终止日）计算，固定期限'+('少于二年。' if short else '不少于二年。')}

def assessment(s,node):
 if node=='employment_part_time_wage':
  from review_v2.part_time_settlement import assessment as settlement
  return settlement(s)
 return {'employment_dispatch_position':position_state,'employment_dispatch_equal_pay':pay_state,'employment_dispatch_identity':term_state}.get(node,lambda s:None)(s)
