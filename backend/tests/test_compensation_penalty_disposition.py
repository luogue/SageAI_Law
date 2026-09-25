import pytest
from backend.tests.test_employment_fact_pipeline import fact,packet,verified_packet
from backend.tests.test_part_time_proportionate_coverage import review
from review_v2.clause_parser import parse_contract_clauses
from review_v2.employment_fact_store import FactStore,normalize
from review_v2.fact_verification import verified_store
from review_v2.fact_validation import FactExtractionError

@pytest.mark.parametrize('quote,kind,positive',[
 ('解除后依法支付经济补偿。','STATUTORY_PAY',True),
 ('终止时无需支付任何经济补偿。','EXCLUDED',False),
 ('劳动者自愿放弃经济补偿。','WAIVED',False),
 ('补偿按工作年限和月工资计算。','CALCULATION_RULE',True),
])
def test_compensation_disposition(monkeypatch,quote,kind,positive):
 cs=parse_contract_clauses(quote)
 s=FactStore(quote,cs,packet(cs,[fact(cs,'economic_compensation.statutory',{'kind':kind,'basis':quote},quote)]))
 assert bool(s.get('economic_compensation.statutory')) is positive
 rows=review(monkeypatch,'劳动合同\n'+quote,[('economic_compensation.statutory',{'kind':kind,'basis':quote},quote)])
 assert (rows['EMP-11-01']['coverage_status']=='风险条款') is (not positive)

@pytest.mark.parametrize('quote,scope,amount,risk',[
 ('未按期完成研发任务支付5000元违约金。','PROJECT_TASK_PERFORMANCE','5000元',True),
 ('迟到三次支付500元违约金。','ATTENDANCE','500元',True),
 ('离职未提前30日支付1000元违约金。','RESIGNATION_NOTICE','1000元',True),
 ('违反竞业限制支付5万元违约金。','NON_COMPETE','5万元',False),
 ('违反专项培训服务期支付培训违约金。','TRAINING_SERVICE_PERIOD','培训费用',False),
])
def test_trigger_scope(monkeypatch,quote,scope,amount,risk):
 rows=review(monkeypatch,'劳动合同\n'+quote,[('penalties.obligations',{'scope':scope,'trigger':quote,'imposed':True,'amount_text':amount},quote)])
 assert (rows['EMP-14-01']['coverage_status']=='风险条款') is risk
 if risk:
  assert any(e.get('quote')==quote for e in rows['EMP-14-01']['evidence_clauses'])

@pytest.mark.parametrize('concept,value,quote',[
 ('economic_compensation.statutory',{'kind':'STATUTORY_PAY','basis':'无需支付'},'无需支付经济补偿。'),
 ('penalties.obligations',{'scope':'ORDINARY_DISCIPLINE','imposed':True,'amount_text':'5000元'},'项目任务逾期支付5000元违约金。'),
])
def test_incorrect_candidate_still_blocked(concept,value,quote):
 cs=parse_contract_clauses(quote);s=FactStore(quote,cs,packet(cs,[fact(cs,concept,value,quote)]))
 p=verified_packet(cs,s);p['verification']['checks'][0].update(supported=False,reason='候选极性或触发场景不符合原文')
 with pytest.raises(FactExtractionError,match='CORE_FACT_VERIFICATION_FAILED'):verified_store(s,p)

def test_no_default_compensation_disposition():
 with pytest.raises(FactExtractionError):normalize('economic_compensation.statutory',{'basis':'依法处理'})


def test_extraction_prompt_schema_version_matches_normalizer():
 from review_v2.deepseek_facts import SYSTEM
 from review_v2.employment_fact_schema import SCHEMA_VERSION
 assert '"schema_version":"'+SCHEMA_VERSION+'"' in SYSTEM
 assert '__CURRENT_FACT_SCHEMA__' not in SYSTEM
