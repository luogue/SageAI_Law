"""Explicit employment-form/term policy matrix over verified classifications."""
from dataclasses import replace
from review_v2.priority_checklist_helpers import required,forbidden

CONCEPTS={
 'working_hours.days_per_week':'约定每周工作天数（数值），与休息日不同；不得自行猜测',
 'salary.cycle_kind':'报酬结算支付周期 DAYS明确天数 / MONTHLY按自然月 / WEEKLY每周 / SEMIMONTHLY明确每半月结清 / PAY_DATES_ONLY仅列每月发薪次数或日期但未明确对应工资期间。每月两次支付不等于每半月结算；分段期间和支付日必须另逐段提取salary.settlement_period，不以概括频率覆盖具体区间。',
 'salary.cycle_days':'明确约定的工资结算支付间隔天数（数值），不是每月第几日发工资',
 'part_time.hourly_minimum':'合同明确承诺小时工资不低于用人单位所在地最低小时工资标准（布尔值）',
 'part_time.injury_insurance':'明确约定单位承担工伤保险义务（布尔值），明确免除、转嫁或替代工伤保险为false；仅笼统承诺依法处理社会保险，不等于明确写明工伤险，归入social_insurance.statutory_duties',
 'part_time.employee_notice_days':'非全日制劳动者终止前明确必须提前通知的天数（数值）；明示随时可为0，但依法通知且没有天数时不生成数值，不因未写天数标记不确定；限制是否存在另由part_time.exit_constraint全文核验',
 'part_time.exit_permission':'明确允许劳动者随时通知或依法通知终止非全日制用工（布尔值）；记录原文承诺，不据此生成通知天数0，也不抵消其他限制条款',
 'part_time.exit_constraint':'非全日制劳动者终止权的实际限制，每个限制分别提取：NOTICE_WAIT强制提前通知等待 / PENALTY未提前通知或离职需赔偿、支付违约金 / MINIMUM_SERVICE最低履行期间或到某日期才可终止 / APPROVAL须批准 / OTHER其他终止限制。全文没有限制时：facts中完全不创建本concept记录，但searched_concepts必须包含本concept，且不放入unresolved_concepts；不得创建value为ABSENT/NONE的记录。依法通知终止的保护承诺归exit_permission，不是限制；单位自愿提前通知、工资结清义务及一般合同期限本身不是劳动者终止限制；禁止限制的保护条款不得抽成实际限制',
 'part_time.employer_notice_days':'非全日制单位承诺提前通知天数（数值），这是单位承担的约定义务，不因对劳动者更有利就认定违法',
 'part_time.exit_approval':'劳动者终止非全日制关系是否必须经单位批准（布尔值），不得要求批准为false',
}
ENUMS={'salary.cycle_kind':{'DAYS','MONTHLY','WEEKLY','SEMIMONTHLY','PAY_DATES_ONLY'},
 'part_time.exit_constraint':{'NOTICE_WAIT','PENALTY','MINIMUM_SERVICE','APPROVAL','OTHER'}}

EXIT_SEARCH_CONCEPTS = ('part_time.exit_constraint', 'part_time.exit_approval',
                        'termination.employee_right_waived', 'penalties.obligations')
SPECS=[
 ('hours','非全日制每日及每周工时','第68条',[('每日平均工时','working_hours.hours_per_day'),('每周累计工时','working_hours.hours_per_week')],'核对同一单位平均每日不超过四小时、每周累计不超过二十四小时；超出时应核实实际用工形式并调整。'),
 ('wage','非全日制小时计酬及十五日结算','第72条',[('计酬标准','salary.regular'),('工资结算支付周期','salary.cycle_kind')],'明确小时计酬标准不低于所在地最低小时工资，结算支付周期最长不超过十五日。'),
 ('insurance','非全日制工伤保险等法定义务','第68条；《社会保险法》第33条',[('依法处理社会保险并承担单位义务','social_insurance.statutory_duties'),('明确单位工伤保险义务','part_time.injury_insurance')],'一般依法处理社会保险的约定可以保留，可进一步明确单位工伤保险义务；文本未细化险种不等于免除义务，明确免责或替代缴费的约定应修改。'),
 ('settlement','非全日制已提供劳动的工资结算','第30条、第71条',[('已提供劳动的工资结清','economic_compensation.settlement_deadline')],'终止后及时结清已提供劳动的工资；不因缺少普通劳动合同经济补偿条款要求补写。'),
 ('engagement','非全日制用工关系与起始日期','第68条、第69条',[('非全日制用工形式','contract.employment_form'),('起始日期','contract.start_date')],'明确用工起点及非全日制安排，不要求设定固定到期日期。'),
]
ELEMENTS={f'employment_part_time_{node}_{i}':[(concept,)] for node,_,_,els,_ in SPECS for i,(_,concept) in enumerate(els,1)}
# Weekly total can also be calculated deterministically from agreed daily hours
# and weekly working days; the two source facts remain bound to that element.
ELEMENTS['employment_part_time_hours_2'].append(('working_hours.hours_per_day','working_hours.days_per_week'))
ELEMENTS['employment_part_time_wage_2'].append(('salary.cycle_days',))
ELEMENTS['employment_part_time_wage_2'].append(('salary.settlement_period',))
ELEMENTS['employment_part_time_insurance_1'] += [('part_time.injury_insurance',), ('social_insurance.employer_pays',), ('social_insurance.employer_enrolls',)]
CHECKLIST=tuple(replace(required('PT',i+2,'employment_part_time_'+node,title,(),'《劳动合同法》'+law,[(label,()) for label,_ in els],suggestion=suggestion,risk='高'),applicable_if='已验证非全日制用工时适用') for i,(node,title,law,els,suggestion) in enumerate(SPECS))
CHECKLIST=(replace(forbidden('PT',1,'employment_part_time_probation','非全日制不得约定试用期',(),'《劳动合同法》第70条',(),'删除非全日制试用期约定，不以补充试用工资使其合法化。'),applicable_if='已验证非全日制用工时适用'),)+CHECKLIST
CHECKLIST+=(replace(forbidden('PT',7,'employment_part_time_exit','非全日制劳动者随时通知终止权',(),'《劳动合同法》第71条',(),'保留劳动者随时通知终止的权利，不设置三十日等待或批准条件；单位自愿承诺较长通知不减损劳动者权利。'),applicable_if='已验证非全日制用工时适用'),)

# Drafting omissions and adverse waivers have distinct severity. Keep the
# checkpoint's adverse severity, while grading missing coverage independently.
from review_v2.priority_checklist_helpers import PROFILES
for _element in PROFILES['employment_part_time_insurance']:
 _element['gap_risk_level'] = '低'

REPLACEMENTS={'EMP-02-01':'PT-06-01','EMP-03-01':'PT-01-01','EMP-15-01':'PT-01-01','EMP-05-01':'PT-02-01','EMP-06-01':'PT-03-01','EMP-07-01':'PT-04-01','EMP-13-01':'PT-04-01','EMP-10-01':'PT-07-01','EMP-16-01':'PT-07-01','EMP-11-01':'PT-05-01'}

def adapt(store,base):
 from review_v2.employment_dispatch import CHECKLIST as DSP,classify
 from review_v2.employment_indefinite import CHECKLIST as OET
 if getattr(store,'agreement_type','labor')=='confidentiality':
  from review_v2.employment_contract_checklist import CONFIDENTIALITY_CHECKLIST
  return CONFIDENTIALITY_CHECKLIST,{'classification':{'agreement_type':'CONFIDENTIALITY'},'retained':[r.item_id for r in CONFIDENTIALITY_CHECKLIST],'disabled':{},'replaced':{},'added':[],'policy_version':'employment-agreement-adapter-1'}
 if getattr(store,'agreement_type','labor')=='non_compete':
  from review_v2.employment_contract_checklist import NON_COMPETE_CHECKLIST
  return NON_COMPETE_CHECKLIST,{'classification':{'agreement_type':'NON_COMPETE'},'retained':[r.item_id for r in NON_COMPETE_CHECKLIST],'disabled':{},'replaced':{},'added':[],'policy_version':'employment-agreement-adapter-1'}
 if getattr(store,'agreement_type','labor')=='employment_termination':
  from review_v2.employment_contract_checklist import TERMINATION_CHECKLIST
  return TERMINATION_CHECKLIST,{'classification':{'agreement_type':'EMPLOYMENT_TERMINATION'},'retained':[r.item_id for r in TERMINATION_CHECKLIST],'disabled':{},'replaced':{},'added':[],'policy_version':'employment-agreement-adapter-2'}
 c=classify(store); disabled={}; replacements={}; additions=()
 if c['employment_form']=='PART_TIME':
  disabled['EMP-17-01']='由非全日制小时计酬及结算专项替代普通报酬必备项'
  replacements=dict(REPLACEMENTS);additions=CHECKLIST
 else:
  if 'TASK' in c['term_types']: disabled['EMP-03-01']='任务期限不得约定试用期，保留EMP-15禁止性判断，不要求补试用工资'
  if c['employment_form']=='DISPATCH': additions+=DSP
  if 'INDEFINITE' in c['term_types']: additions+=OET
 kept=tuple(r for r in base if r.item_id not in replacements and r.item_id not in disabled)
 return kept+additions,{'classification':c,'retained':[r.item_id for r in kept], 'disabled':disabled,'replaced':replacements,'added':[r.item_id for r in additions],'policy_version':'employment-adapter-1'}

def adverse(store,node):
 out=[]
 def pick(k,p,reason):
  for f in store.get(k,positive=False):
   if p(f['normalized_value']):out.extend({**e,'reason':reason} for e in store.evidence([f],node+'_adverse'))
 if node.endswith('_probation'):pick('probation.arrangement',lambda v:v=='CURRENT','非全日制用工不得约定试用期。')
 if node.endswith('_hours'):
  pick('working_hours.hours_per_day',lambda v:v>4,'约定平均每日工时超过四小时，需核实是否符合非全日制用工。')
  pick('working_hours.hours_per_week',lambda v:v>24,'约定每周累计工时超过二十四小时。')
  for daily in store.get('working_hours.hours_per_day'):
   for days in store.get('working_hours.days_per_week'):
    if daily['normalized_value']*days['normalized_value']>24:
     out.extend({**e,'reason':'每日工时乘每周工作天数所得周工时超过二十四小时。'} for e in store.evidence([daily,days],node+'_adverse'))
 if node.endswith('_wage'):
  from review_v2.part_time_settlement import assessment
  result=assessment(store)
  if result['status']=='RISK':
   out.extend({**e,'reason':result['reason']} for e in store.evidence([f for c in result['concepts'] for f in store.get(c,positive=False)],node+'_adverse'))
  pick('salary.cycle_kind',lambda v:v=='MONTHLY','按月结算支付超过非全日制最长十五日周期。')
  pick('salary.cycle_days',lambda v:v>15,'工资结算支付周期超过十五日。')
  pick('part_time.hourly_minimum',lambda v:v is False,'明确排除最低小时工资保障。')
 if node.endswith('_insurance'):
  pick('part_time.injury_insurance',lambda v:v is False,'非全日制身份不能免除单位依法承担的工伤保险义务。')
  for key in ('cash_replacement','waived','employer_share_shifted'):
   pick('social_insurance.'+key,lambda v:v is True,'明确替代、免除或转嫁单位法定社会保险义务，不能因一般依法处理条款而消除该冲突。')
 if node.endswith('_exit'):
  pick('part_time.exit_constraint',lambda v:True,'约定提前等待、离职金钱责任、最低履行期间或其他条件，限制非全日制劳动者通知终止权。')
  pick('part_time.employee_notice_days',lambda v:v>0,'强制劳动者提前通知并等待，限制随时通知终止的权利。')
  pick('part_time.exit_approval',lambda v:v is True,'以单位批准限制非全日制劳动者终止权。')
  pick('termination.employee_right_waived',lambda v:v is True,'明确排除劳动者依法终止的权利。')
  pick('penalties.obligations',lambda v:v.get('imposed',True) is True and v.get('scope') in {'ORDINARY_RESIGNATION','RESIGNATION_NOTICE'},'以离职或未提前通知为由要求劳动者支付违约金，限制通知终止权。')
 if node.endswith('_settlement'):pick('salary.withheld_for_handover',lambda v:v is True,'以交接为由扣留已经挣得的工资。')
 return out
