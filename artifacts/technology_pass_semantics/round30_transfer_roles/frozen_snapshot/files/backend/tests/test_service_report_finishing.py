import re
from review_v2.service_scenarios import PROFILES, project_checklist
from review_v2.service_contract_checklist import SERVICE_REVIEW_CHECKLIST

def test_payment_cycle_is_not_service_frequency():
    frequency=PROFILES['service_content_standard'][1][2]
    assert not re.search(frequency,'服务费按月支付，每月服务费用10000元。')
    assert re.search(frequency,'办公区域每日清洁一次。')

def test_customer_cooperation_is_not_service_content():
    content=PROFILES['service_content_standard'][0][2]
    assert not re.search(content,'甲方提供资料、信息、场地、设备，并支持乙方履行。')
    assert re.search(content,'乙方提供日常保洁和垃圾清运服务。')

def test_b2b_authorities_and_document_checks_are_projected_once():
    rules=project_checklist(SERVICE_REVIEW_CHECKLIST,'甲方：甲有限公司。企业购买办公保洁服务。')
    by_id={r.item_id:r for r in rules}
    assert '消费者权益保护法' not in by_id['SVC-08-01'].legal_basis
    assert '第577条' in by_id['SVC-08-01'].legal_basis
    assert 'SVC-02-03' in by_id and 'SVC-12-03' not in by_id
    consumer=project_checklist(SERVICE_REVIEW_CHECKLIST,'个人购买健身会员年卡。')
    assert any('消费者权益保护法' in r.legal_basis for r in consumer)
