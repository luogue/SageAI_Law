"""Calendar-exact wage intervals from verified facts, never frequency averaging."""
from datetime import date
from calendar import monthrange

CONCEPTS=['salary.settlement_period','salary.cycle_kind','salary.cycle_days']

def calendar_interval(value):
 required={'earning_period_start_day','earning_period_end_day','payment_deadline_day','earning_period_end_month_offset','payment_month_offset'}
 if not required<=value.keys():return {'status':'VERIFY','reason':'工资区间或支付截止日未完整约定'}
 offsets=[value[k] for k in ('earning_period_end_month_offset','payment_month_offset')]
 if any(type(x) not in (int,float) or x!=int(x) or not 0<=x<=120 for x in offsets):
  return {'status':'VERIFY','reason':'相对月份无法可靠计算'}
 def resolve(y,m,offset,day):
  total=y*12+m-1+int(offset);yy,mm=divmod(total,12);mm+=1
  return date(yy,mm,monthrange(yy,mm)[1] if day=='MONTH_END' else int(day))
 samples=[]
 # Complete Gregorian repetition: includes every 28/29/30/31-day month.
 for year in range(2000,2400):
  for month in range(1,13):
   try:
    start=resolve(year,month,0,value['earning_period_start_day'])
    end=resolve(year,month,offsets[0],value['earning_period_end_day'])
    pay=resolve(year,month,offsets[1],value['payment_deadline_day'])
   except ValueError:return {'status':'VERIFY','reason':'约定日期在部分月份不存在，不能自行改成月末'}
   if not start<=end<=pay:return {'status':'VERIFY','reason':'工资区间与支付日期顺序无法确认'}
   samples.append(((pay-start).days,start,end,pay))
 worst=max(samples,key=lambda x:x[0]);best=min(x[0] for x in samples)
 return {'status':'RISK' if worst[0]>15 else 'PASS','max_days':worst[0],'min_days':best,
         'earning_period_start':str(worst[1]),'earning_period_end':str(worst[2]),'payment_deadline':str(worst[3]),
         'calculation_basis':'支付截止日减工资期间起始日的日历日差；覆盖完整格里高利历400年周期'}

def assessment(store):
 base={'concepts':CONCEPTS}
 periods=store.get('salary.settlement_period')
 calculations=[dict(calendar_interval(f['normalized_value']),fact_id=f['fact_id']) for f in periods]
 kinds=set(store.values('salary.cycle_kind'));days=store.values('salary.cycle_days')
 if any(c['status']=='RISK' for c in calculations) or 'MONTHLY' in kinds or any(n>15 for n in days):
  maximum=max([c.get('max_days',0) for c in calculations]+days+[31 if 'MONTHLY'in kinds else 0])
  return {**base,'status':'RISK','calculation':calculations,'max_days':maximum,
          'reason':f'按各工资期间至最迟支付日分别核验，最长结算支付间隔可达{maximum:g}日，超过十五日；不能用每月支付次数替代期间计算。'}
 if periods:
  if all(c['status']=='PASS' for c in calculations) and store.coverage['salary.settlement_period']!='UNCERTAIN':
   maximum=max(c['max_days'] for c in calculations)
   return {**base,'status':'PASS','calculation':calculations,'max_days':maximum,'reason':f'各段工资归属期间至最迟支付日的最长日历间隔为{maximum}日，均不超过十五日。'}
  return {**base,'status':'VERIFY','calculation':calculations,'reason':'分段结算存在不完整或无法解释的日期，需要确认各工资期间及最迟支付日。'}
 if any(store.coverage[c]=='UNCERTAIN' for c in CONCEPTS):
  return {**base,'status':'VERIFY','reason':'工资期间或结算支付周期尚无法确认，不能仅按发薪次数认定不超过十五日。'}
 if 'PAY_DATES_ONLY' in kinds:
  return {**base,'status':'VERIFY','reason':'仅明确发薪次数或日期，未明确对应工资期间，需核验最长结算支付周期。'}
 limits=days+([7] if 'WEEKLY'in kinds else [])+([15] if 'SEMIMONTHLY'in kinds else [])
 if limits:
  return {**base,'status':'PASS','max_days':max(limits),'proof':'EXPLICIT_CYCLE',
          'reason':f'原文明确结算周期最长{max(limits):g}日，不超过十五日；未推定具体工资起止日期。'}
 return {**base,'status':'VERIFY','reason':'没有可验证的工资结算周期或完整期间，需补充核验，不能仅凭支付安排通过。'}
