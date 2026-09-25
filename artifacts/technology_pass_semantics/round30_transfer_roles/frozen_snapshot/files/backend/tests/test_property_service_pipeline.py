"""Property service regressions: semantics, not province/article/value fixtures."""
import re
from copy import deepcopy
from pathlib import Path
from types import SimpleNamespace
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from review_v2.service_scenarios import resolve, PROFILES, UNIT_PRICE
from review_v2.clause_parser import parse_contract_clauses
from review_v2.utility_supply_evidence import _find_supports
from review_v2.contract_effects import active, evidence, consistency_failures
from review_v2.penalty_base import analyze

def test_property_subtype_from_body_not_title():
    text='综合协议。乙方为物业服务人，为全体业主维护共用部位，业主按月支付物业服务费。'
    assert resolve(text)['subtype']=='PROPERTY_SERVICE'
    assert resolve('甲方：甲公司。企业购买办公保洁服务。')['subtype']=='GENERAL_B2B_SERVICE'

def test_long_document_enumerated_scope_and_quantified_operations():
    text='第一条 服务范围\n1.房屋共用部位日常维护和管理；\n2.公共区域清洁卫生及生活垃圾收集。\n'+'双方通讯信息另见记录。\n'*150+'第二十条 标准\n公共区域每日清扫不少于3次；\n一般报修45分钟内响应。'
    clauses=parse_contract_clauses(text)
    for node in ['service_content_standard','service_quality_standard']:
        found,rows=_find_supports(clauses,node,PROFILES[node])
        assert found=={r[0] for r in PROFILES[node]}
        assert rows

@pytest.mark.parametrize('text',[
    '合同期限届满后继续有效，期限转为不定期。',
    '本合同无固定服务期限。',
])
def test_indefinite_continuation_triggers(text):
    assert resolve(text)['values']['indefinite']

@pytest.mark.parametrize('text,node',[
 ('乙方可以将服务委托第三方实施。乙方认为第三方具备资质后，对第三方服务造成的人身财产损失不承担赔偿责任。','common_delegated_service_waiver'),
 ('无论是否存在工作人员失职，乙方均不承担赔偿责任。','common_own_fault_waiver'),
 ('对于区域内发生的人身伤亡，只要安排巡逻，无论是否存在人员脱岗，乙方均不承担赔偿责任。','common_own_fault_waiver'),
 ('甲方提前解除应提前60日通知，并支付相当于4个月服务费的违约金。乙方提前7日通知可以解除合同，无需承担违约责任。','common_asymmetric_exit'),
 ('争议可以提交仲裁；任何一方也可以向人民法院提起诉讼。','common_elective_dispute_routes'),
])
def test_adverse_effects_not_presence_pass(text,node):
    clauses=parse_contract_clauses('第一条\n'+text)
    assert evidence(node,clauses)
    assert node in {r.node_id for r in active('第一条\n'+text)}

def test_protective_delegation_and_sequential_dispute_not_adverse():
    text='第一条 乙方委托第三方提供服务，仍向甲方承担合同责任。\n第二条 争议先协商；协商不成向人民法院起诉。'
    assert not active(text)

def test_symmetric_exit_and_invalid_award_litigation_not_conflict():
    text='第一条 甲方提前7日通知解除，无需承担违约责任。乙方提前7日通知解除，无需承担违约责任。\n第二条 仲裁裁决被撤销后，任何一方也可以向法院起诉。'
    assert not active(text)

def test_fee_allocation_and_office_address_are_not_service_proof():
    found,_=_find_supports(parse_contract_clauses('第一条 服务费主要用于清洁卫生、公共区域维护。'),'service_content_standard',PROFILES['service_content_standard'])
    assert 'service_content' not in found
    found,_=_find_supports(parse_contract_clauses('第一条 乙方通信地址：某市甲路12号。'),'service_schedule_and_place',PROFILES['service_schedule_and_place'])
    assert 'service_location' not in found

@pytest.mark.parametrize('base',['实际欠交物业费','欠交费用','实际侵占金额','挪用公共收益金额'])
def test_objective_variable_penalty_base(base):
    rows=analyze(f'按照{base}的15%支付违约金。')
    assert rows and all(r['status']=='DETERMINABLE' for r in rows)

def test_undefined_penalty_base_is_not_accepted():
    assert analyze('按照服务管理基数的15%支付违约金。')[0]['status']=='UNDEFINED'

@pytest.mark.parametrize('text',['住宅：3.70元/月·平方米。','车位：80元/月/个。'])
def test_unit_pricing_does_not_require_fixed_total(text):
    assert re.search(UNIT_PRICE,text)

def test_effect_gate_blocks_lost_risk_or_wrong_quote():
    item=SimpleNamespace(item_id='X',coverage_status='通过',decision_trace={'effect_source_quotes':['因自身过错亦免责。']},evidence_clauses=[])
    assert {f['requirement'] for f in consistency_failures([item])}=={'ADVERSE_LEGAL_EFFECT_LOST','ADVERSE_EFFECT_SOURCE_OMITTED'}

def test_source_positive_cannot_be_overwritten_by_absence():
    item=SimpleNamespace(item_id='X',coverage_status='缺失',coverage_elements=[{'element_id':'service_content','status':'MISSING'}],
        decision_trace={'service_positive_source_facts':[{'element_id':'service_content','quotes':['公共区域每日清洁。']}]},evidence_clauses=[])
    assert consistency_failures([item])[0]['requirement']=='POSITIVE_SERVICE_FACT_REPORTED_ABSENT'

@pytest.fixture(scope='module')
def production_report():
    from routers import review_v2 as route
    app=FastAPI(); app.include_router(route.router)
    app.dependency_overrides[route.get_current_user]=lambda:{'id':1}
    path=Path(__file__).resolve().parents[2]/'test_data/87 物业服务合同.docx'
    with TestClient(app) as client:
        response=client.post('/review-v2/file',data={'contract_type':'service','use_llm':'false'},files={'file':(path.name,path.read_bytes())})
    response.raise_for_status()
    return response.json()

def test_same_file_production_classification_and_all_item_statistics(production_report):
    report=production_report
    assert report['report_context']['subtype']=='PROPERTY_SERVICE'
    assert report['report_context']['contract_type_label']=='物业服务合同'
    assert report['contract_type_name']=='物业服务合同'
    assert sum(report['coverage_summary'].values())==len(report['items'])
    assert report['release_quality_gate']['status']=='REPORT_READY',report['release_quality_gate']['failures']

def test_same_file_source_elements_and_adverse_projections(production_report):
    items={i['item_id']:i for i in production_report['items']}
    for key in ['SVC-03-01','SVC-03-02','SVC-12-01','SVC-12-02','COMMON-20-01']:
        assert items[key]['coverage_status']=='通过',key
    assert '第八条' in items['SVC-03-01']['evidence_location']
    assert '第十四条' in items['SVC-03-02']['evidence_location']
    for key in ['SVC-11-01','COMMON-40-01','COMMON-41-01','COMMON-42-01','COMMON-43-01']:
        assert items[key]['coverage_status']=='风险条款',key
        assert any(e['status']=='ADVERSE' for e in items[key]['coverage_elements'])
    assert '6个月' in str(items['COMMON-42-01']['evidence_clauses'])
    assert '15日' in str(items['COMMON-42-01']['evidence_clauses'])
    assert '90日' in str(items['COMMON-42-01']['evidence_clauses'])

def test_same_file_change_remedy_and_stage_bindings(production_report):
    items={i['item_id']:i for i in production_report['items']}
    for key in ['SVC-07-01','SVC-07-04']:
        assert items[key]['coverage_status']=='缺失'
        assert not any(e.get('source_type')=='SOURCE_CLAUSE' for e in items[key]['evidence_clauses'])
    item=items['SVC-08-02']
    assert item['coverage_status']=='部分覆盖'
    quotes=str([e for e in item['evidence_clauses'] if e.get('source_type')=='SOURCE_CLAUSE'])
    assert '第三十条' in quotes and '第二十七条' not in quotes
    assert '乙方经甲方书面催告3次' in quotes
    item=items['SVC-06-04']
    assert item['coverage_status']=='部分覆盖'
    assert '第十一条' in str(item['applicability']['trigger_evidence'])
    assert '期限转为不定期' in str(item['applicability']['trigger_evidence'])
    assert '90日' not in str(item['evidence_clauses'])
    assert 'common_asymmetric_exit' != item.get('risk_group')

@pytest.mark.parametrize('key,bad_quote',[
    ('SVC-08-02','甲方严重违反合同义务，经乙方书面催告仍不改正，乙方有权解除合同。'),
    ('SVC-06-04','甲方提前90日书面通知并支付违约金，乙方提前15日通知可以解除合同。'),
])
def test_final_gate_rejects_wrong_party_or_unscoped_evidence(production_report,key,bad_quote):
    from review_v2.lease_semantics import consistency_failures as final_gate
    item=SimpleNamespace(**deepcopy(next(i for i in production_report['items'] if i['item_id']==key)))
    for row in item.evidence_clauses:
        if row.get('source_type')=='SOURCE_CLAUSE':
            row['quote']=bad_quote
    assert any(f['requirement']=='DISPLAY_QUOTE_ELEMENT_CONFLICT' for f in final_gate([item]))

def test_no_training_or_prepaid_requirements_in_property(production_report):
    for item in production_report['items']:
        if item['item_id'].startswith(('SVC-04-','SVC-09-','SVC-10-')):
            assert item['coverage_status']=='不适用'

def test_property_indefinite_authority_and_optional_notice(production_report):
    item=next(i for i in production_report['items'] if i['item_id']=='SVC-06-04')
    assert '948' in item['legal_basis_index']
    assert '730' not in str(item['legal_references'])
    assert '948' in str(item['legal_references'])
    assert item['action_priority']=='C_OPTIMIZATION'
    assert '法定' in item['legal_consequence_if_missing']
    assert '60日书面通知对方' in item['suggested_clause_example']
    assert '第730条' not in production_report['result']
    assert any(r.get('article')=='第948条' and r.get('support_type')=='DIRECT_SUPPORT' for r in item['legal_references'])
    section=production_report['result'].split('（SVC-06-04）')[1].split('\n## ')[0]
    assert '【法律依据】：《中华人民共和国民法典》第948条' in section
    assert '责任边界不够明确' not in section
    assert '合同未复述不影响该法定通知规则适用' in section

def test_property_wrong_authority_is_blocked(production_report):
    from review_v2.lease_semantics import consistency_failures
    item=SimpleNamespace(**deepcopy(next(i for i in production_report['items'] if i['item_id']=='SVC-06-04')))
    item.legal_basis_index='《民法典》第730条'
    assert any(f['requirement']=='SCENARIO_LEGAL_BASIS_CONFLICT' for f in consistency_failures([item]))

@pytest.mark.parametrize('clause',[
    '不定期物业服务合同解除可提前十日书面通知对方。',
    '转为不定期后，乙方解除合同无需通知对方。',
])
def test_property_explicit_notice_conflict_is_not_optional(production_report,clause):
    from review_v2.service_scenarios import apply_property_indefinite_law
    item=SimpleNamespace(**deepcopy(next(i for i in production_report['items'] if i['item_id']=='SVC-06-04')))
    apply_property_indefinite_law(item,parse_contract_clauses('第一条 '+clause))
    assert item.coverage_status=='风险条款'
    assert '948' in item.legal_basis_index

def test_old_omissions_cannot_pass_new_gate(production_report):
    from review_v2.domain_selection import domain_selection_consistency_gate
    resolution=SimpleNamespace(**deepcopy(production_report['domain_selection_resolution']))
    ids=[i['item_id'] for i in production_report['items'] if not i['item_id'].startswith(('COMMON-40','COMMON-41','COMMON-42','COMMON-43'))]
    resolution.document_domain['contract_subtype']='GENERAL_SERVICE'
    gate=domain_selection_consistency_gate(resolution,ids)
    assert gate['status']=='BLOCKED'
    assert {'UNREVIEWED_ADVERSE_LEGAL_EFFECT','PROPERTY_SERVICE_SUBTYPE_LOST'} <= {f['requirement'] for f in gate['failures']}
