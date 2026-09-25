import pytest
from review_v2.engine import review_contract_v2
from review_v2.service_scenarios import qualification_conditions

@pytest.mark.parametrize('text,expected',[
 ('企业办公保洁，普通室内清洁。',False),
 ('企业购买普通IT运维服务，按年付款。',False),
 ('乙方提供高空外墙清洗服务。',True),
 ('乙方提供律师服务。',True),
 ('乙方提供诊疗服务，由执业医师负责。',True),
 ('注册会计师承担审计工作。',True),
 ('工作人员必须持有指定资格证。',True),
])
def test_qualification_prerequisite(text,expected):
    assert qualification_conditions(text)['qualified_staff']==expected

def test_body_content_satisfies_optional_document():
    r=review_contract_v2('甲方：甲有限公司。乙方：乙有限公司。服务内容：提供办公清洁、垃圾清运。每日清洁一次。服务费用总计人民币120000元。按月支付。','service',use_llm=False)
    items={i['item_id']:i for i in r['items']}
    for key in ['SVC-12-01','SVC-12-02']:
        assert items[key]['coverage_status']=='通过'
        assert items[key]['evidence_clauses']
    assert items['SVC-02-02']['coverage_status']=='不适用'
    for i in r['items']:
        if i['coverage_status']!='不适用':
            assert '消费者' not in i.get('legal_consequence_if_missing','')

def test_explicit_missing_attachment_not_substituted():
    r=review_contract_v2('甲方：甲有限公司。服务费用总计人民币120000元，收费标准详见附件，附件未提供。','service',use_llm=False)
    i=next(i for i in r['items'] if i['item_id']=='SVC-12-02')
    assert i['coverage_status']!='通过'
