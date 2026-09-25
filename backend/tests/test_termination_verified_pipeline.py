import pytest
from review_v2.clause_parser import parse_contract_clauses
from backend.tests.test_employment_fact_pipeline import fact, packet, verified_packet

def run(monkeypatch, vals, kind='employment_termination'):
 from review_v2 import employment_fact_pipeline as p
 from review_v2.engine import review_contract_v2
 text='协商终止协议\n'+ '\n'.join('第'+str(i)+'条\n'+q for i,q in enumerate(dict.fromkeys(q for _,_,q in vals),1))
 cs=parse_contract_clauses(text)
 monkeypatch.setattr(p,'extract',lambda *a,**kw:packet(cs,[fact(cs,c,v,q) for c,v,q in vals]))
 monkeypatch.setattr(p,'verify',verified_packet)
 result=review_contract_v2(text,kind)
 assert result['structured_fact_debug']['provider']=='deepseek'
 assert result['release_quality_gate']['status']=='REPORT_READY',result['release_quality_gate']
 return {r['item_id']:r for r in result['items']},result

IDENTITY=[('identity.employer_name','示例企业','甲方：示例企业。'),
 ('identity.employer_address','杭州市文三路','甲方住所：杭州市文三路。'),
 ('identity.employer_representative','李先生','负责人李先生。'),
 ('identity.worker_name','王女士','乙方：王女士，身份证320000XXXX。'),
 ('identity.worker_id','320000XXXX','乙方：王女士，身份证320000XXXX。')]

@pytest.mark.parametrize('address',[False,True])
def test_identity_atomic_verified_final_report(monkeypatch,address):
 vals=IDENTITY+([('identity.worker_address','南京市中山路','乙方住址：南京市中山路。')] if address else [])
 rows,r=run(monkeypatch,vals)
 assert rows['EMP-01-01']['coverage_status']==('通过' if address else '部分覆盖')
 assert r['structured_fact_debug']['employment']['identity']['worker_address']==([] if not address else r['structured_fact_debug']['employment']['identity']['worker_address'])
 if not address:
  el=next(e for e in rows['EMP-01-01']['coverage_elements'] if e['element_id']=='employment_identity_4')
  assert el['status']!='COVERED'

def test_cross_clause_recall_and_all_risk_consumers(monkeypatch):
 vals=IDENTITY+[
 ('non_compete.arrangement','EXISTS','乙方离职后受竞业限制。'),
 ('non_compete.person_scope','乙方','乙方离职后受竞业限制。'),
 ('non_compete.businesses',['数据库软件业务'],'不得从事数据库软件业务。'),
 ('non_compete.territories',['全国'],'地域覆盖全国。'),
 ('non_compete.duration_months',24,'竞业期为二十四个月。'),
 ('non_compete.compensation',{'amount_text':'3500','unit':'CNY/MONTH'},'竞业补偿每月3500元。'),
 ('economic_compensation.statutory',{'kind':'STATUTORY_PAY','basis':'解除补偿依法支付'},'解除补偿依法支付。'),
 ('exit_settlement.wage_deadline','工资于10月6日支付','工资于10月6日支付。'),
 ('exit_settlement.compensation_deadline','补偿交接后三个工作日支付','补偿交接后三个工作日支付。'),
 ('exit_settlement.compensation_after_handover_days',3,'补偿交接后三个工作日支付。'),
 ('exit_settlement.certificate','单位提供终止证明','单位提供终止证明。'),
 ('exit_settlement.social_transfer','办理社保转移','办理社保转移。'),
 ('exit_settlement.personnel_transfer','办理人事档案转移','办理人事档案转移。'),
 ('termination.handover','本周五前交接设备和资料','本周五前交接设备和资料。'),
 ('exit_settlement.remedy_waiver',True,'乙方不得再提起仲裁诉讼或向主管部门举报。'),
 ('penalties.obligations',{'scope':'OTHER','imposed':True,'amount_text':'70000','trigger':'违反协议任何义务'},'违反协议任何义务须支付七万元违约金。'),
 ]
 rows,r=run(monkeypatch,vals)
 for rule in ['NC-01-01','NC-02-01','EMP-11-01','ET-01-01']:
  assert rows[rule]['coverage_status']=='通过'
 for rule in ['ET-04-01','ET-06-01','EMP-14-01']:
  assert rows[rule]['coverage_status']=='风险条款'
  assert rows[rule]['evidence_clauses']
  assert rows[rule]['judge_source']=='structured_facts'
 assert len(rows['EMP-11-01']['evidence_clauses'])>=3
 assert 'ET-04-01' in rows['EMP-11-01']['action_suggestion']

@pytest.mark.parametrize('delay,waiver,risk',[(0,False,False),(5,True,True)])
def test_handover_compensation_and_negative_polarity(monkeypatch,delay,waiver,risk):
 vals=IDENTITY+[
 ('exit_settlement.compensation_after_handover_days',delay,'交接办结时支付补偿。' if delay==0 else '交接完成五日后支付补偿。'),
 ('exit_settlement.compensation_withholding',True,'未交接时暂缓补偿。'),
 ('exit_settlement.remedy_waiver',waiver,'乙方放弃仲裁权。' if waiver else '不限制乙方依法申请仲裁。')]
 rows,_=run(monkeypatch,vals)
 for rule in ['ET-04-01','ET-06-01']:
  assert rows[rule]['coverage_status']==('风险条款' if risk else '通过')

def test_active_scope_and_no_wrong_subtypes():
 from review_v2.fact_module_registry import REGISTRY
 from review_v2.employment_fact_schema import CONCEPTS
 from review_v2.termination_facts import CONCEPTS as ET
 roots=[{'concept':'non_compete.arrangement','value':'EXISTS'}]
 scope=REGISTRY.select('employment_termination',CONCEPTS,roots)
 assert set(ET)<=set(scope)
 assert 'non_compete.duration_months' in scope
 assert 'penalties.obligations' in scope
 assert not any(c.startswith(('dispatch.','part_time.','probation.')) for c in scope)
 assert not set(ET).intersection(REGISTRY.select('labor',CONCEPTS,roots))

@pytest.mark.parametrize('fact_present',[False,True])
def test_no_covered_claim_without_final_verified_evidence(monkeypatch,fact_present):
 from review_v2 import employment_fact_pipeline as p
 from review_v2.fact_validation import FactExtractionError
 text='解除协议\n乙方住址为苏州市观前街。' if fact_present else '解除协议\n乙方为王女士。'
 cs=parse_contract_clauses(text)
 fs=[fact(cs,'identity.worker_address','苏州市观前街','乙方住址为苏州市观前街。')] if fact_present else []
 monkeypatch.setattr(p,'extract',lambda *a,**kw:packet(cs,fs))
 monkeypatch.setattr(p,'verify',verified_packet)
 def stale_serializer(*a,**kw):
  return {'items':[{'item_id':'EMP-01-01','coverage_status':'通过','evidence_clauses':[],
     'coverage_elements':[{'element_id':'employment_identity_4','status':'COVERED'}]}]}
 with pytest.raises(FactExtractionError,match='VERIFIED_COVERAGE_EVIDENCE_CONFLICT'):
  p.run(text,'employment_termination',stale_serializer)
