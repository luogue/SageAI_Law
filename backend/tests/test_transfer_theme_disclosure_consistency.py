"""Final theme, disclosure and linked service facts retain their own meaning."""
from pathlib import Path
from types import SimpleNamespace as NS
import pytest
from review_v2.clause_parser import parse_contract_clauses, ParsedClause
from review_v2.disclosure_facts import negative_sources
from review_v2.theme_coverage import project, aggregate
from review_v2.engine import (_existing_technology_use_disclosure_results,
    _technical_secret_transfer_proof_results, _atomic_requirement_family,
    _register_atomic_family_facts, review_contract_v2)
from review_v2.contract_facts import ContractFactGraph
from review_v2.user_profile import UserRiskProfile


def clauses(text):
    return [ParsedClause('S','第四条','历史披露',text,'正式合同条款',1)]


@pytest.mark.parametrize('state,expected', [('通过','PASS'),('部分覆盖','PARTIAL'),
    ('缺失','MISSING'),('风险条款','ADVERSE'),('不适用','NOT_APPLICABLE'),('待核验','UNCERTAIN')])
def test_single_source_theme_preserves_final_rule(state,expected):
    theme={'source_rule_ids':['RULE']}
    project(theme,[NS(source_review_ids=['RULE'],legal_impact={'coverage':'缺失'},issue_type='MISSING')],
            [NS(item_id='RULE',coverage_status=state,coverage_elements=[])])
    assert theme['status']==expected
    assert theme['source_rule_statuses']=={'RULE':expected}


@pytest.mark.parametrize('states,expected', [(['COVERED','MISSING'],'PARTIAL'),
    (['PARTIALLY_COVERED','MISSING'],'PARTIAL'),(['MISSING','MISSING'],'MISSING'),
    (['COVERED','COVERED'],'PASS'),(['ADVERSE','COVERED'],'ADVERSE'),
    (['NOT_APPLICABLE'],'NOT_APPLICABLE')])
def test_component_rollup(states,expected):
    assert aggregate(states)==expected


@pytest.mark.parametrize('negative', ['不存在其他第三方使用、许可或披露。',
    '没有其他既有许可。','从未向第三方授予实施许可。','无既有许可。'])
def test_explicit_none_covers_disclosure_and_empty_dimensions(negative):
    rows,_=_existing_technology_use_disclosure_results(clauses(negative))
    license_rows=[e for e in rows if e['element_id'].startswith('existing_license_')]
    assert len(license_rows)==4
    assert all(e['status']=='COVERED' and e['fact_value']=='EXPLICIT_NONE' for e in license_rows)
    assert all(e['supporting_evidence'][0]['quote']==negative for e in license_rows)


@pytest.mark.parametrize('text', ['双方未约定是否存在其他许可。','如不存在其他第三方许可，应提供说明。',
    '未发现不存在其他第三方许可的证明。','无法确认不存在第三方许可。',
    '客户无权许可相关技术。','甲方无需提供许可。','甲方不得许可相关技术。'])
def test_unknown_conditional_or_prohibition_is_not_confirmed_absence(text):
    assert not negative_sources(clauses(text),r'许可')


def test_existing_license_does_not_lose_its_missing_term_to_no_other_license():
    rows,_=_existing_technology_use_disclosure_results(clauses('此前已向远川公司授予普通许可。除上述情况外，不存在其他第三方许可。'))
    by={e['element_id']:e for e in rows}
    assert by['existing_license_disclosure']['status']=='COVERED'
    assert by['existing_license_term']['status']=='MISSING'


@pytest.mark.parametrize('event',['曾向甲机构提供技术演示；演示仅包含运行结果，不包含底层参数。',
    '曾为乙企业提供检测服务；该客户仅获得检测结果，无权取得底层模型。'])
def test_closed_disclosure_list_is_not_documentary_proof(event):
    rows,_,_=_technical_secret_transfer_proof_results(clauses(event+'除上述情况外，不存在其他第三方使用、许可或披露。'))
    by={e['element_id']:e for e in rows}
    assert by['historical_disclosure_objects']['status']=='COVERED'
    assert by['historical_disclosure_scope']['status']=='COVERED'
    assert by['current_secret_status']['status']=='MISSING'
    assert by['existing_confidentiality_measures']['status']=='MISSING'


def test_canonical_registry_retains_explicit_none_value_and_original_quote():
    c=clauses('不存在其他第三方使用、许可或披露。');g=ContractFactGraph()
    _register_atomic_family_facts(g,'secret_transfer_proof',c)
    facts=g.facts['technology.secret_transfer_proof.existing_license_disclosure']
    assert facts[0].normalized_value=='EXPLICIT_NONE'
    assert facts[0].source_spans==[c[0].text]


@pytest.mark.parametrize('action',['部署','安装','调试','配置'])
def test_main_acceptance_links_only_matching_service_activity(action):
    c=parse_contract_clauses(f'第一条 技术服务\n乙方应提供现场{action}服务。\n第二条 验收\n验收标准：完成指定设备{action}；连续运行48小时无重大故障。甲方应在10日内完成验收。乙方应在5日内整改。甲方有权进行第二次验收。')
    rows=_atomic_requirement_family('ancillary_service_quality',c);by={e['element_id']:e for e in rows}
    assert by['objective_acceptance_standard']['status']=='COVERED'
    assert by['rectification_deadline']['status']=='COVERED'
    assert by['reinspection_procedure']['status']=='COVERED'
    assert by['reinspection_deadline']['status']=='MISSING'


@pytest.mark.parametrize('standard',['文件齐全且可读取','算法准确率达到98%','甲方自行完成部署'])
def test_asset_acceptance_without_provider_service_output_does_not_cross_scope(standard):
    c=parse_contract_clauses(f'第一条 技术服务\n乙方应提供线上培训。\n第二条 验收\n验收标准：{standard}。')
    assert not _atomic_requirement_family('ancillary_service_quality',c)


def test_high_severity_with_lower_priority_exposes_existing_reason():
    theme={'source_rule_ids':['RULE']}
    project(theme,[NS(source_review_ids=['RULE'],legal_impact={'coverage':'部分覆盖'},issue_type='MISSING')],[],
            [NS(downgrade_reason='重大风险行动降级依据：counter_evidence。')])
    assert '合同已有保护性约定或反向证据' in theme['action_priority_reason']


@pytest.fixture(scope='module')
def report():
    text=(Path(__file__).parent/'fixtures/secret_transfer_roles_projection.txt').read_text(encoding='utf8')
    return review_contract_v2(text,'technology',use_llm=False,profile=UserRiskProfile(user_identity='甲方/受让方'))


@pytest.mark.parametrize('key',['TC-01-03','TC-06-01','TC-02-01','TC-11-03','TC-12-01','COMMON-20-01','TC-10-01','TC-10-02','TC-10-04'])
def test_existing_passes_are_preserved(report,key):
    assert next(i for i in report['items'] if i['item_id']==key)['coverage_status']=='通过'


def test_current_proof_retains_only_unproved_materials(report):
    for key in ['TC-03-04','TC-13-02']:
        item=next(i for i in report['items'] if i['item_id']==key)
        assert item['coverage_status']=='部分覆盖'
        assert '完整的历史披露对象清单' not in item['risk_point_description']
        assert '既有许可相对方' not in item['risk_point_description']
        assert any(e['element_id']=='staff_assignment' and e['status']=='MISSING' for e in item['coverage_elements'])


def test_current_service_has_no_duplicate_residual_and_reuses_deployment(report):
    by={i['item_id']:i for i in report['items']}
    assert by['TC-09-01']['risk_point_description'].count('现场部署及培训的履行期限')==1
    assert by['TC-09-01']['narrative_state']['issue'].count('现场部署及培训的履行期限')==1
    assert by['TC-09-01']['narrative_state']['issue'].count('培训及远程答疑的交付标准')==1
    assert by['TC-09-02']['coverage_status']=='部分覆盖'
    elements={e['element_id']:e for e in by['TC-09-02']['coverage_elements']}
    assert elements['objective_acceptance_standard']['status']=='COVERED'
    assert elements['reinspection_deadline']['status']=='MISSING'
    for theme in report['risk_themes']:
        if len(theme['source_rule_ids'])==1:
            key=theme['source_rule_ids'][0]
            assert theme['status']==theme['source_rule_statuses'][key]


def test_deployment_only_service_has_no_invented_training_gap():
    c=parse_contract_clauses('第一条 技术服务\n乙方应提供现场部署服务。\n第二条 验收\n验收标准：完成指定设备部署。')
    e=next(e for e in _atomic_requirement_family('ancillary_service_content',c) if e['element_id']=='service_delivery_standard')
    assert e['status']=='COVERED'
    assert not e.get('residuals')
