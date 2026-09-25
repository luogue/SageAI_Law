"""Open-ended duration and capability dismissal over verified facts only."""
from dataclasses import replace
from review_v2.priority_checklist_helpers import forbidden

CONCEPTS = {
 'contract.term_limit_mode':'合同本身约定的期限上限机制：TASK_COMPLETION以明确工作任务完成为终止事件；EMPLOYER_DETERMINED_COMPLETION单位自行决定任务是否完成；NONE明确无确定终止时间；CALENDAR_EXPIRY某日自动终止；MAXIMUM_DURATION最长履行期限；EMPLOYER_RENEWAL到期由单位决定续签。不是退休、法定终止事件或派遣期限；禁止设置上限为NONE。与contract.type声明独立提取，不因冲突改写声明类型',
 'contract.term_limit_date':'劳动合同自身固定终止或最长履行截止日期（YYYY-MM-DD），不是试用期或派遣期限',
 'contract.term_limit_months':'劳动合同自身约定的最长期限月数（数值），不是试用期限',
 'capability.ground':'不能胜任解除依据：RANK_ALONE仅凭绩效排名末位即认定；ASSESSED经工作能力实质考核；STATUTORY依法确认不能胜任。不得将排名低直接推断为不能胜任；明确禁止仅凭排名认定为STATUTORY',
 'capability.training':'不能胜任解除中是否要求先培训（布尔值），明确无须为false；与调岗二择一也为true；未提及不生成',
 'capability.reassignment':'不能胜任解除中是否要求先调整岗位（布尔值），明确无须为false；培训或调岗二择一为true；未提及不生成',
 'capability.reassessment':'不能胜任解除是否要求培训或调岗后仍不能胜任（布尔值）；直接认定后解除而明确跳过再次考核为false',
 'capability.notice':'不能胜任解除通知机制：NOTICE_OR_PAY提前三十日书面通知或额外一个月工资；IMMEDIATE_NO_ALTERNATIVE立即解除且无通知或代通知金替代；OTHER其他。立即解除但支付代通知金不属于排除通知；不得从严重违纪解除移用',
 'capability.compensation':'不能胜任解除的经济补偿：STATUTORY依法支付；WAIVED明确无需支付；不得将代通知金与经济补偿混同，不得从其他解除原因移用',
}
ENUMS = {'contract.term_limit_mode':{'NONE','CALENDAR_EXPIRY','MAXIMUM_DURATION','EMPLOYER_RENEWAL','TASK_COMPLETION','EMPLOYER_DETERMINED_COMPLETION'},
 'capability.ground':{'RANK_ALONE','ASSESSED','STATUTORY'},
 'capability.notice':{'NOTICE_OR_PAY','IMMEDIATE_NO_ALTERNATIVE','OTHER'},
 'capability.compensation':{'STATUTORY','WAIVED'}}
CHECKLIST = (replace(forbidden('OET',1,'employment_open_ended_limit','无固定期限合同设置固定终止日期或变相期限',(),
 '《劳动合同法》第14条、第44条',(),
 '删除无固定期限合同中固定到期、最长履行及到期由单位决定续签的限制；保留依法解除、终止的条件，不能将无固定期限变相改为固定期限。'),
 applicable_if='已验证合同声明为无固定期限劳动合同时适用'),)

def limit_adverse(store,node):
 if 'INDEFINITE' not in store.values('contract.type'): return []
 facts=store.get('contract.term_limit_mode',positive=False)
 bad=[f for f in facts if f['normalized_value']!='NONE']
 if not bad: return []
 rows=store.evidence(bad+store.get('contract.type')+store.get('contract.term_limit_date')+store.get('contract.term_limit_months'),node+'_adverse')
 for row in rows: row['reason']='合同声明无固定期限，却另设确定终止时间、最长履行期限或到期续签限制，形成变相固定期限。'
 return rows

def capability_adverse(store,node):
 rows=[]
 checks=[('capability.ground',lambda v:v=='RANK_ALONE','将绩效排名末位直接等同不能胜任工作，缺少实质认定。'),
 ('capability.reassessment',lambda v:v is False,'解除安排跳过培训或调岗后的再次不能胜任条件。'),
 ('capability.notice',lambda v:v=='IMMEDIATE_NO_ALTERNATIVE','不能胜任即立即解除，排除提前通知或代通知金的法定程序。'),
 ('capability.compensation',lambda v:v=='WAIVED','不能胜任解除明确排除法定经济补偿。')]
 if False in store.values('capability.training') and False in store.values('capability.reassignment'):
  checks += [(key,lambda v:v is False,'同时排除培训和调整岗位，跳过不能胜任解除的法定前置措施。') for key in ('capability.training','capability.reassignment')]
 for key,predicate,reason in checks:
  for f in store.get(key,positive=False):
   if predicate(f['normalized_value']): rows.extend({**e,'reason':reason} for e in store.evidence([f],node+'_adverse'))
 return rows
