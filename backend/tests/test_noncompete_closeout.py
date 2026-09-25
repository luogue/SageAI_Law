from copy import deepcopy
from types import SimpleNamespace
import pytest
from review_v2.clause_parser import parse_contract_clauses
from review_v2.noncompete_reasonableness import assess
from review_v2.noncompete_semantics import consistency_failures
from test_noncompete_semantics import review, item


def checks(text):
    return {c['key']: c for c in assess(parse_contract_clauses(text))['checks']}


@pytest.mark.parametrize('region',['全国','全球'])
def test_broad_geography_requires_support(region):
    c=checks(f'竞业限制地域范围为{region}。')['broad_geography']
    assert c['status']=='REVIEW_REQUIRED'
    assert not c['supporting_business'] and not c['supporting_secrets']


def test_broad_geography_with_support_still_requires_proportionality_assessment():
    c=checks('竞业限制地域范围为全国。公司业务覆盖全国。乙方实际接触全国核心商业秘密。')['broad_geography']
    assert c['supporting_business'] and c['supporting_secrets']
    assert '真实性' in c['message']


@pytest.mark.parametrize('months,ratio,trigger',[(24,30,True),(18,40,True),(6,70,False),(6,10,True),(12,50,False),(24,60,False)])
def test_duration_times_compensation(months,ratio,trigger):
    c=checks(f'离职后{months}个月承担竞业限制。经济补偿金为离职前12个月平均工资的{ratio}%。')
    assert ('duration_compensation' in c)==trigger


def test_notice_has_independent_extra_compensation_consequence():
    c=checks('离职后24个月承担竞业限制。甲方提前2个月通知可解除本协议。')
    assert 'early_termination_compensation' in c
    assert '三个月' in c['early_termination_compensation']['message']


def test_extra_compensation_already_handled_not_flagged():
    c=checks('甲方提前2个月通知可解除本协议。解除后甲方额外支付三个月竞业补偿。')
    assert 'early_termination_compensation' not in c


def test_employee_remedy_is_not_employer_termination():
    c=checks('甲方未支付补偿时，乙方有权单方解除本协议。')
    assert 'early_termination_compensation' not in c


@pytest.mark.parametrize('text',['甲方竞争对手为其他公司。','竞争行为包括为甲方的客户提供服务。','甲方与乙方应配合履行。'])
def test_role_reference_not_name_evidence(text):
    r=item(review(text),'EMP-01-01')
    assert not any('employment_identity_name' in e.get('supports_element_ids',[]) for e in r['evidence_clauses'])


def test_explicit_name_has_only_definition_evidence():
    r=item(review('甲方：远岚有限公司。甲方竞争对手包括其他公司。'),'EMP-01-01')
    evidence=[e for e in r['evidence_clauses'] if 'employment_identity_name' in e.get('supports_element_ids',[])]
    assert evidence and all('甲方：远岚有限公司' in e['text'] for e in evidence)


def test_proportionality_warning_cannot_be_overwritten_by_pass():
    r=review('离职后24个月承担竞业限制。经济补偿金为离职前12个月平均工资的30%。')
    rows=[SimpleNamespace(**deepcopy(i)) for i in r['items']]
    consumer=next(i for i in rows if i.item_id=='NC-03-01')
    assert consumer.coverage_status=='待核验'
    consumer.coverage_status='通过'
    consumer.coverage_elements=[]
    assert consistency_failures(rows)


def test_actual_document_has_all_three_checks_and_clean_name_binding():
    from pathlib import Path
    from docx import Document
    source=Path(__file__).resolve().parents[2]/'test_data/60 竞业限制协议.docx'
    r=review('\n'.join(p.text for p in Document(source).paragraphs))
    consumer=item(r,'NC-03-01')
    assert {'broad_geography','duration_compensation','early_termination_compensation'} <= {c['key'] for c in consumer['decision_trace']['noncompete_proportionality']['checks']}
    identity=item(r,'EMP-01-01')
    assert identity['coverage_status']=='通过'
    assert not any(e['location'] in {'1.2','1.3'} for e in identity['evidence_clauses'])
    assert r['release_quality_gate']['status']=='REPORT_READY'
