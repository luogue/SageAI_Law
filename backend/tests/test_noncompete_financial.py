import pytest
from backend.tests.test_employment_fact_pipeline import fact,packet
from review_v2.clause_parser import parse_contract_clauses
from review_v2.employment_fact_store import FactStore
from review_v2.noncompete_financial import assess

@pytest.mark.parametrize('months,ratio,base,penalty,status',[(6,50,20000,1000,'PASS'),(18,35,None,120000,'VERIFY'),(24,10,20000,1000,'VERIFY'),(6,50,None,120000,'VERIFY'),(6,50,10000,200000,'RISK')])
def test_financial_assessment(months,ratio,base,penalty,status):
 text=f'第一条\n竞业期限{months}个月。补偿为平均工资{ratio}%。竞业违约金{penalty}元。平均工资基数{base}元。'
 cs=parse_contract_clauses(text)
 vals=[('non_compete.duration_months',months,f'竞业期限{months}个月。'),('non_compete.compensation',{'formula':{'kind':'PERCENT_OF_BASE','percent':ratio,'base':'PREVIOUS_AVERAGE_SALARY'},'unit':'CNY/MONTH'},f'补偿为平均工资{ratio}%。'),('penalties.obligations',{'scope':'NON_COMPETE','imposed':True,'amount_text':str(penalty)},f'竞业违约金{penalty}元。')]
 if base is not None: vals.append(('non_compete.salary_base',{'amount_text':str(base),'unit':'CNY/MONTH','base':'PREVIOUS_AVERAGE_SALARY'},f'平均工资基数{base}元。'))
 s=FactStore(text,cs,packet(cs,[fact(cs,c,v,q) for c,v,q in vals]));r,_=assess(s)
 assert ('RISK' if r['risks'] else 'VERIFY' if r['checks'] else 'PASS')==status
 assert r['estimated_total_compensation']==(months*base*ratio/100 if base else None)

def test_floor_is_lower_bound_not_total():
 text='第一条\n竞业期限18个月。补偿为平均工资35%，每月不低于8000元。'
 cs=parse_contract_clauses(text); vals=[('non_compete.duration_months',18,'竞业期限18个月。'),('non_compete.compensation',{'formula':{'kind':'PERCENT_OF_BASE','percent':35,'base':'PREVIOUS_AVERAGE_SALARY'},'unit':'CNY/MONTH'},'补偿为平均工资35%，每月不低于8000元。'),('non_compete.compensation_floor',{'amount_text':'8000','unit':'CNY/MONTH'},'补偿为平均工资35%，每月不低于8000元。')]
 s=FactStore(text,cs,packet(cs,[fact(cs,c,v,q) for c,v,q in vals]));r,_=assess(s)
 assert r['estimated_total_compensation'] is None and r['total_lower_bound']==144000

@pytest.mark.parametrize('penalty,expected',[(1000,'通过'),(200000,'风险条款')])
def test_financial_final_rule(monkeypatch,penalty,expected):
 from backend.tests.test_part_time_proportionate_coverage import review
 text=f'劳动合同\n第一条\n约定离职竞业限制6个月。适用人员为研发主管，已实际知悉源代码。竞业业务为数据库软件，地域为杭州。月补偿5000元。竞业违约金{penalty}元。'
 vals=[('non_compete.arrangement','EXISTS','约定离职竞业限制6个月。'),('non_compete.duration_months',6,'约定离职竞业限制6个月。'),('non_compete.personnel','研发主管','适用人员为研发主管，已实际知悉源代码。'),('non_compete.actual_access',True,'适用人员为研发主管，已实际知悉源代码。'),('non_compete.businesses','数据库软件','竞业业务为数据库软件，地域为杭州。'),('non_compete.territories','杭州','竞业业务为数据库软件，地域为杭州。'),('non_compete.compensation',{'amount_text':'5000','unit':'CNY/MONTH'},'月补偿5000元。'),('penalties.obligations',{'scope':'NON_COMPETE','imposed':True,'amount_text':str(penalty)},f'竞业违约金{penalty}元。')]
 rows=review(monkeypatch,text,vals)
 assert rows['NC-03-01']['coverage_status']==expected
 assert rows['NC-01-01']['coverage_status']=='通过'
 assert rows['NC-02-01']['coverage_status']=='通过'
