"""Rule-owned proof components survive canonical projection and theme grouping."""
import json
from pathlib import Path
from copy import deepcopy
from types import SimpleNamespace
import pytest
from review_v2.clause_parser import parse_contract_clauses
from review_v2.engine import _atomic_requirement_definitions, _reconcile_specialized_coverage_from_elements
from review_v2.requirement_entailment import technical_secret_identity_support

TEXT = Path(__file__).with_name('fixtures').joinpath('secret_license_proof_aggregation.txt').read_text(encoding='utf-8')

def proof(text):
    return {e['element_id']: e for e in _atomic_requirement_definitions('secret_transfer_proof', parse_contract_clauses(text))}

@pytest.mark.parametrize('name', ['技术秘密','专有技术','许可技术'])
@pytest.mark.parametrize('quote', ['', '”'])
def test_defined_technical_scope_alias(name, quote):
    assert technical_secret_identity_support(f'本合同所称{name}{quote}包括以下内容：设备标定参数、模型配置和非公开工艺流程。')['technical_scope']

@pytest.mark.parametrize('verb', ['应建立','应当建立','须建立','必须建立','将建立','拟建立'])
def test_prospective_controls_are_not_existing_proof(verb):
    e=proof(f'乙方{verb}技术资料访问权限控制。')['existing_confidentiality_measures']
    assert e['status']=='MISSING' and not e['supporting_evidence']

@pytest.mark.parametrize('verb', ['已建立','已经建立','已实施','已经采取'])
def test_existing_controls_keep_positive_evidence(verb):
    e=proof(f'甲方{verb}技术资料访问权限控制。')['existing_confidentiality_measures']
    assert e['status']=='COVERED' and e['supporting_evidence']

@pytest.mark.parametrize('text', [
    '本合同终止后，乙方仍应对尚未公开的技术秘密承担保密责任。',
    '非因乙方违反合同而进入公共领域的信息不承担保密义务。',
    '如果技术秘密已进入公共领域，应通知乙方。',
    '双方未明确技术秘密当前仍具秘密性。',
])
def test_duty_exception_hypothesis_and_absence_are_not_present_secret_status(text):
    e=proof(text)['current_secret_status']
    assert e['status']=='MISSING' and not e['supporting_evidence']

@pytest.mark.parametrize('status', ['尚未全部公开','尚未公开','仍具秘密性'])
def test_actual_status_representation_keeps_residual_proof_gap(status):
    e=proof(f'上述技术{status}。')['current_secret_status']
    assert e['status']=='PARTIALLY_COVERED' and e['supporting_evidence']

def test_same_article_sources_remain_owned_by_each_predicate():
    e=proof('第九条 权利保证\n甲方保证有权就本合同约定的许可技术向乙方提供许可。\n许可技术目前尚未公开。')
    a=e['disposition_authority']['supporting_evidence']
    b=e['current_secret_status']['supporting_evidence']
    assert a and b and a != b
    assert all('提供许可' in s['quote'] and '尚未公开' not in s['quote'] for s in a)
    assert all('尚未公开' in s['quote'] and '提供许可' not in s['quote'] for s in b)

@pytest.fixture(scope='module',params=['甲方/许可方','乙方/被许可方'])
def report(request):
    from review_v2.engine import review_contract_v2
    from review_v2.user_profile import UserRiskProfile
    return review_contract_v2(TEXT,'technology',use_llm=False,profile=UserRiskProfile(user_identity=request.param))

@pytest.mark.parametrize('rule', ['TC-03-04','TC-13-02'])
def test_real_contract_final_rule_owns_components_sources_and_narrative(report,rule):
    assert report['release_quality_gate']['status']=='REPORT_READY'
    item=next(i for i in report['items'] if i['item_id']==rule)
    assert item['coverage_presence']=='PARTIAL' and item['coverage_status']=='部分覆盖'
    assert '完全缺失' not in item['risk_point_description']
    assert '未找到对应约定' not in item['risk_point_description']
    elements={e['element_id']:e for e in item['coverage_elements']}
    assert elements['technical_secret_identity_and_delivery_scope']['status']=='COVERED'
    assert elements['disposition_authority']['status']==elements['current_secret_status']['status']=='PARTIALLY_COVERED'
    assert elements['existing_confidentiality_measures']['status']=='MISSING'
    for e in elements.values():
        if e['status'] in {'COVERED','PARTIALLY_COVERED'}:
            assert e['source_fact_key'] and e['supporting_evidence']
            for s in e['supporting_evidence']:
                direct=[q for q in item['evidence_clauses'] if q.get('quote')==s['quote'] and q['clause_id']==s['clause_id'] and e['element_id'] in q.get('supports_element_ids',[])]
                assert direct and all(q['verified_original'] and q['support_type']=='DIRECT' for q in direct)
        elif e['status']=='MISSING':
            assert not e.get('supporting_evidence')

@pytest.mark.parametrize('states,expected', [(['MISSING','MISSING'],'MISSING'),(['COVERED','MISSING'],'PARTIAL'),(['COVERED','COVERED'],'PRESENT'),(['PARTIALLY_COVERED','MISSING'],'PARTIAL')])
def test_component_rollup_is_rule_local(report,states,expected):
    item=SimpleNamespace(**deepcopy(next(i for i in report['items'] if i['item_id']=='TC-03-04')))
    item.coverage_elements=[dict(element_id=str(n),status=s,proposition='独立要素') for n,s in enumerate(states)]
    _reconcile_specialized_coverage_from_elements(item)
    assert item.coverage_presence==expected
    other=next(i for i in report['items'] if i['item_id']=='TC-13-02')
    assert other['coverage_presence']=='PARTIAL'
