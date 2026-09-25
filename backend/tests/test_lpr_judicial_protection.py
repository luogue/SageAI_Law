from datetime import date
from pathlib import Path
import pytest
from review_v2.clause_parser import parse_contract_clauses as parse
from review_v2.loan_costs import analyze_costs
from review_v2.lpr_protection import reference_for, assess
from review_v2.engine import review_contract_v2

PARTIES = '出借方：远星有限公司。借款方：明川有限公司。'
DATE = '签署日期：2025年5月25日。'
CAP = '借期利息、逾期利息、违约金及其他融资费用合计不得超过合同成立时一年期LPR四倍。'
def analysis(text):
 return analyze_costs(parse(PARTIES+DATE+text))

@pytest.mark.parametrize('rate,status',[(5.1,'PASS'),(12,'PASS'),(18.6,'RISK')])
def test_known_rate_boundaries(rate,status):
 a=analysis(f'借款年利率为{rate}%。')
 assert a['judicial_protection']['status']==status
 assert a['judicial_protection']['cap_percent']==12
 assert not a['combined_contractual_cap']

@pytest.mark.parametrize('signed,status', [('2030-01-01','FUTURE_FORMATION_DATE'),('2024-01-01','REFERENCE_DATA_UNAVAILABLE')])
def test_reference_not_extrapolated(signed,status):
 a=reference_for('签署日期：'+signed,today=date(2026,9,10))
 assert a['status']==status and a['one_year_percent'] is None

def test_declared_lpr_is_not_official_data():
 a=analyze_costs(parse(PARTIES+'合同成立时一年期LPR为3%。借款年利率为4%。'))
 assert a['judicial_protection']['status']=='PENDING'
 assert a['judicial_protection']['reference']['status']=='FORMATION_DATE_UNKNOWN'

@pytest.mark.parametrize('reverse',[False,True])
def test_term_and_overdue_do_not_sum(reverse):
 parts=['第一条 利率\n借期内年利率为8%。','第二条 逾期\n逾期本金按年利率10%计息。']
 a=analysis('\n'.join(reversed(parts) if reverse else parts))
 assert a['judicial_protection']['status']=='PASS'
 assert a['judicial_protection']['normalized_totals']['overdue_principal_annual_percent']==10
 assert a['potential_annual_percent_estimate'] is None

@pytest.mark.parametrize('base,expected',[('逾期本金','RISK'),('应付未付利息','PENDING'),('届期未付利息','PENDING'),('到期未支付利息','PENDING')])
def test_different_bases(base,expected):
 a=analysis(f'逾期本金按照年利率10%计算逾期利息。按照{base}每日0.01%支付违约金。')
 assert a['judicial_protection']['status']==expected
 penalty=next(c for c in a['components'] if c['kind']=='penalty')
 assert penalty['base']==('PRINCIPAL' if base=='逾期本金' else 'UNPAID_INTEREST')

def test_explicit_concurrent_interest():
 a=analysis('借款年利率为8%。逾期本金按年利率10%计息。逾期利息与借期利息同时计收。')
 assert a['judicial_protection']['status']=='RISK'
 assert a['judicial_protection']['normalized_totals']['overdue_principal_annual_percent']==18

def test_cap_limits_actual_claim_even_when_nominal_rate_higher():
 a=analysis('借款年利率为19%。'+CAP)
 assert a['judicial_protection']['status']=='PASS'
 assert a['combined_contractual_cap']

@pytest.mark.parametrize('rate,expected',[(6,'通过'),(18,'风险条款')])
def test_full_pipeline_known_benchmark(rate,expected):
 r=review_contract_v2(PARTIES+DATE+f'第一条 利率\n借款年利率为{rate}%。', 'loan',use_llm=False)
 item=next(i for i in r['items'] if i['item_id']=='L-04-02')
 assert item['coverage_status']==expected
 assert r['release_quality_gate']['status']=='REPORT_READY',r['release_quality_gate']['failures']

def test_original_future_contract_and_independent_overdue_coverage():
 from layers.input_layer import InputLayer
 source=Path(__file__).resolve().parents[2]/'test_data'/'101 企业之间借款合同.docx'
 r=review_contract_v2(InputLayer()._extract_from_docx_content(source.read_bytes()),'loan',use_llm=False)
 rows={i['item_id']:i for i in r['items']}
 assert rows['L-04-02']['coverage_status']=='待核验'
 assert rows['L-05-02']['coverage_status']=='通过'
 assert rows['L-04-02']['action_priority']=='NONE'
 assert all(e['status']=='COVERED' for e in rows['L-05-02']['coverage_elements'])
 assert not any('L-05-02' in f['source_review_ids'] for f in r['risk_findings'])
 assert r['release_quality_gate']['status']=='REPORT_READY',r['release_quality_gate']['failures']

@pytest.mark.parametrize('interest,status',[(1000,'PASS'),(80000,'RISK')])
def test_interest_base_requires_actual_same_window_ratio(interest,status):
 a=analysis('逾期本金按年利率10%计算逾期利息。按应付未付利息每日0.01%支付违约金。')
 assert a['judicial_protection']['status']=='PENDING'
 result=assess(a,DATE,performance_facts={'principal':100000,'unpaid_interest':interest,'same_accrual_window':True})
 assert result['status']==status
 assert result['normalized_totals']['overdue_principal_annual_percent']==pytest.approx(10+3.65*interest/100000)


def test_unrelated_ledger_window_cannot_prove_combined_cost():
 a=analysis('逾期本金按年利率10%计算逾期利息。按应付未付利息每日0.01%支付违约金。')
 assert assess(a,DATE,performance_facts={'principal':100000,'unpaid_interest':1000,'same_accrual_window':False})['status']=='PENDING'


def test_single_interest_cap_and_no_cumulative_clause():
 a=analysis('借款年利率为19%。借款利率不得超过合同成立时一年期LPR四倍。')
 assert a['judicial_protection']['status']=='PASS'


def test_exclusive_claims_and_negative_cumulative_polarity():
 a=analysis('借款年利率为8%。逾期本金按年利率10%计息。逾期利息与借期利息不得同时计收。')
 assert a['judicial_protection']['status']=='PASS'
 assert a['stacking']!='CUMULATIVE'


@pytest.mark.parametrize('rate',[6,18])
def test_lpr_cannot_override_complete_overdue_text(rate):
 text=PARTIES+DATE+f'自逾期之日起，逾期本金按年利率{rate}%计收逾期利息，至实际清偿之日止。'
 r=review_contract_v2(text,'loan',use_llm=False)
 rows={i['item_id']:i for i in r['items']}
 assert rows['L-05-02']['coverage_status']=='通过'
 assert rows['L-04-02']['coverage_status']==('通过' if rate==6 else '风险条款')
 assert not any('L-05-02' in f['source_review_ids'] for f in r['risk_findings'])
 assert r['release_quality_gate']['status']=='REPORT_READY',r['release_quality_gate']['failures']
