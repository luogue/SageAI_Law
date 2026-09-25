from pathlib import Path
import pytest
from docx import Document
from review_v2.service_scenarios import resolve, CONDITIONS
from review_v2.engine import review_contract_v2


@pytest.mark.parametrize('text,subtype,consumer,prepaid,training',[
 ('甲方：甲有限公司。乙方：乙有限公司。企业购买办公保洁服务，按月支付。','GENERAL_B2B_SERVICE',False,False,False),
 ('甲方：张三。个人购买健身会员年卡，预付3000元。','PREPAID_CONSUMER_SERVICE',True,True,False),
 ('学员姓名：张三。个人报名教育培训，购买60课时包，预付5000元。','TRAINING_EDUCATION_SERVICE',True,True,True),
 ('甲方：甲有限公司。企业购买年度IT运维服务，按年预付10000元。','GENERAL_B2B_SERVICE',False,False,False),
 ('甲方：甲有限公司。乙方：乙有限公司。依据消费者权益保护法，分期付款购买维护服务。','GENERAL_B2B_SERVICE',False,False,False),
])
def test_scenario_prerequisites(text,subtype,consumer,prepaid,training):
    facts=resolve(text)
    assert facts['subtype']==subtype
    assert facts['values']['consumer']==consumer
    assert facts['values']['prepaid_consumer']==prepaid
    assert facts['values']['training']==training


@pytest.fixture(scope='module')
def actual_report():
    path=Path(__file__).resolve().parents[2]/'test_data/70 服务合同.docx'
    text='\n'.join(p.text for p in Document(path).paragraphs)
    return review_contract_v2(text,'service',use_llm=False)


def test_b2b_positive_facts_and_conditional_na(actual_report):
    items={i['item_id']:i for i in actual_report['items']}
    for key in CONDITIONS:
        if CONDITIONS[key]=='qualification_documents':
            continue
        assert items[key]['coverage_status']=='不适用',key
    for key in ['SVC-03-01','SVC-03-02','SVC-03-03']:
        assert items[key]['coverage_status']=='通过',key
        assert items[key]['evidence_clauses']
        assert not any(e['status']=='MISSING' for e in items[key]['coverage_elements'])
    trace=items['SVC-03-01']['decision_trace']
    assert trace['service_scenario']['subtype']=='GENERAL_B2B_SERVICE'
    assert '120,000' in str(trace['service_fee_facts'])
    assert '10,000' in str(trace['service_fee_facts'])
    assert actual_report['release_quality_gate']['status']=='REPORT_READY'
    assert sum(actual_report['coverage_summary'].values())==47
    themes=str([(f.get('title'),f.get('recommendation')) for f in actual_report['risk_findings']])
    assert '培训服务范围' not in themes
    assert '消费者解除' not in themes
    assert '课时' not in themes
    assert items['SVC-12-01']['coverage_status']=='通过'
    assert items['SVC-12-02']['coverage_status']=='通过'
    qualification_themes=[f for f in actual_report['risk_findings']
                          if set(f.get('source_review_ids',[])) & {'SVC-02-03','SVC-12-03'}]
    assert len(qualification_themes)==1
    assert qualification_themes[0]['source_review_ids']==['SVC-02-03']
    assert 'SVC-12-03' not in items


def test_force_majeure_not_termination_or_complete_absence(actual_report):
    items={i['item_id']:i for i in actual_report['items']}
    assert items['SVC-11-01']['coverage_status']=='缺失'
    item=items['SVC-11-04']
    assert item['coverage_status']=='部分覆盖'
    elements={e['element_id']:e['status'] for e in item['coverage_elements']}
    assert elements['force_majeure_event']=='COVERED'
    assert elements['force_majeure_relief']=='COVERED'
    assert elements['force_majeure_notice']=='MISSING'
    assert elements['force_majeure_proof']=='MISSING'


def test_prepaid_refund_cannot_use_quality_evidence():
    text='服务合同。甲方：张三，个人购买健身会员年卡，预付3000元。服务质量：场馆地面无污渍。'
    result=review_contract_v2(text,'service',use_llm=False)
    item=next(i for i in result['items'] if i['item_id']=='SVC-04-03')
    assert item['coverage_status']=='缺失'
    assert not item['evidence_clauses']
