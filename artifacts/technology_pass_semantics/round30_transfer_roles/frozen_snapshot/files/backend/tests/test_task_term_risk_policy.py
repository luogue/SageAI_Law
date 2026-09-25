import pytest
from backend.tests.test_part_time_proportionate_coverage import review

TASK='本合同以完成工作任务为期限，项目验收完成即终止。'
def base():return [('contract.type','TASK',TASK),('contract.task_end','项目验收完成',TASK)]
@pytest.mark.parametrize('arrangement,duration,status',[('CURRENT',1,'风险条款'),('CURRENT',None,'风险条款'),('NONE',None,'通过')])
def test_task_trial(monkeypatch,arrangement,duration,status):
 q='约定试用期一个月。' if arrangement=='CURRENT' else '双方不设试用期。'
 values=base()+[('probation.arrangement',arrangement,q)]
 if duration:values.append(('probation.duration_months',duration,q))
 item=review(monkeypatch,TASK+'\n'+q,values)['EMP-15-01']
 assert item['coverage_status']==status
 if status=='风险条款':
  assert item['risk_level']=='高' and item['action_priority']=='A_CORE'
  assert '不得约定试用期' in item['title']
  assert '不以缩短试用期' in item['suggested_clause_example']

@pytest.mark.parametrize('kind,quote,status',[('STATUTORY_PAY','任务完成终止后依法支付经济补偿。','通过'),('EXCLUDED','任务完成终止后无需支付经济补偿。','风险条款'),('WAIVED','任务完成终止时劳动者自愿放弃经济补偿。','风险条款')])
def test_task_compensation(monkeypatch,kind,quote,status):
 deadline='终止当日结清补偿和工资。'
 values=base()+[('economic_compensation.statutory',{'kind':kind,'basis':quote},quote),('economic_compensation.settlement_deadline','终止当日',deadline)]
 item=review(monkeypatch,TASK+'\n'+quote+'\n'+deadline,values)['EMP-11-01']
 assert item['coverage_status']==status
 if status=='风险条款':
  assert item['risk_level']=='高' and item['action_priority']=='A_CORE'
  assert '工作任务完成导致合同终止' in item['suggested_clause_example']

def test_fixed_trial_unaffected(monkeypatch):
 q='固定期限为两年，试用期一个月。'
 values=[('contract.type','FIXED',q),('contract.duration_months',24,q),('probation.duration_months',1,q),('probation.arrangement','CURRENT',q)]
 item=review(monkeypatch,q,values)['EMP-15-01']
 assert item['coverage_status']=='通过'
