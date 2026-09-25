"""Shared predicates survive enumeration and subtype projections."""
import json
from pathlib import Path
import pytest
from fastapi.testclient import TestClient
from auth.utils import create_access_token
from main import app
from review_v2.clause_parser import parse_contract_clauses
from review_v2.engine import _atomic_requirement_family
from review_v2.development_exit import development_exit_elements


def atoms(family, text):
    return {e['element_id']: e for e in _atomic_requirement_family(family, parse_contract_clauses(text))}


@pytest.mark.parametrize('numbered', [False, True])
def test_delivery_list_inherits_predicate_not_number_style(numbered):
    members = ['项目源代码', 'API接口文档', '安装部署文档', '用户使用指南', '测试结果报告']
    body = '\n'.join((str(i)+'. ' if numbered else '') + v + '；' for i,v in enumerate(members,1))
    text = '第一条 交付\n受托方应提交：\n' + body + '\n双方未约定缺陷清单交付。'
    rows = atoms('development_documents', text)
    assert rows['operation_document_delivery']['status'] == 'COVERED'
    assert rows['test_report_delivery']['status'] == 'COVERED'
    assert rows['defect_list_delivery']['status'] == 'MISSING'
    assert all(s['quote'] in text for e in rows.values() for s in e['supporting_evidence'])


def test_exceptions_keep_independent_development_and_last_member():
    rows = atoms('confidentiality_detail', '第一条 保密\n下列信息不属于保密信息：\n已合法公开的信息；\n从第三方合法取得的信息；\n接收方独立研发形成的信息；\n根据有权机关要求披露的信息。')
    assert rows['confidentiality_exceptions']['status'] == 'COVERED'


def test_scope_and_acceptance_consume_same_metric_span():
    text = '第一条 技术指标\n系统响应时间不超过3秒。'
    a=atoms('development_scope',text)['acceptance']; b=atoms('development_acceptance',text)['acceptance_metrics']
    assert a['status']==b['status']=='COVERED'
    assert a['source_fact_key']==b['source_fact_key']
    assert {s['quote'] for s in a['supporting_evidence']} == {s['quote'] for s in b['supporting_evidence']}


def test_component_outage_is_not_infringement_remedy():
    rows=atoms('technical_components','第一条 第三方服务\n乙方可使用第三方模型。第三方模型停止服务后乙方应提供替代方案。')
    assert rows['component_service_continuity']['status']=='COVERED'
    assert 'license_or_replacement_remedy' not in rows


def test_third_party_testing_fee_is_not_component_fee():
    rows=atoms('technical_components','第一条 验收\n双方委托第三方检测机构复测，检测费用由乙方承担。')
    assert rows['component_license_cost_allocation']['status']=='MISSING'


def test_improvement_notice_requires_actor_action_and_object():
    text='第一条 后续改进\n被许可方应在收到验收通知后5日内完成验收。许可方可以向第三方披露改进成果。'
    assert atoms('improvement_notification',text)['improvement_result_notification']['status']=='MISSING'
    text+='乙方形成改进成果后，应在10日内书面通知甲方。'
    row=atoms('improvement_notification',text)['improvement_result_notification']
    assert row['status']=='COVERED'
    assert all('书面通知甲方' in s['quote'] for s in row['supporting_evidence'])


def test_software_deliverables_do_not_exclude_embodied_project_samples():
    text='第一条 研发范围\n完成机器人系统集成及生产线验证。\n第二条 交付\n乙方应交付：\n源代码；部署说明。'
    row=next(e for e in development_exit_elements(parse_contract_clauses(text)) if e['element_id']=='exit_sample_handover')
    assert row['status']=='MISSING'


def test_absent_fee_basis_does_not_deny_secret_scope():
    from review_v2.report_state_consistency import _denied_secret_domains
    assert not _denied_secret_domains('合同已明确技术秘密范围，但未形成以技术秘密秘密性为独立对价基础的收费安排。')
    assert 'technical_secret' in _denied_secret_domains('合同未形成可识别的技术秘密范围。')


@pytest.mark.parametrize('text,state', [('双方未另行约定专利申请费用承担。','MISSING'),
                                      ('专利申请费用由双方另行协商承担。','PARTIALLY_COVERED')])
def test_absent_agreement_differs_from_future_consultation(text,state):
    assert atoms('entrusted_patent','第一条 专利\n'+text)['filing_cost_allocation']['status']==state


def test_data_disposal_does_not_invent_backup_deletion():
    from review_v2.material_disposition import material_disposition_elements
    text='第一条 项目结束\n乙方应返还或删除甲方提供的业务数据。双方未约定乙方删除备份数据后的书面证明程序。'
    rows={e['element_id']:e for e in material_disposition_elements(parse_contract_clauses(text),actor='乙方',material_owner='甲方')}
    assert rows['material_disposition']['status']=='PARTIALLY_COVERED'
    assert rows['backup_disposition']['status']=='MISSING'
    assert rows['material_disposal_confirmation']['status']=='MISSING'


def test_added_scope_separate_price_is_fee_adjustment():
    rows=atoms('development_funding','第一条 费用\n如新增系统功能模块，双方应另行确认费用及研发周期。')
    assert rows['fee_adjustment']['status']=='COVERED'


def test_improvement_negative_ownership_not_positive_assignment():
    rows=atoms('improvement_ownership','第一条 后续改进\n乙方独立开发的通用技术升级不当然属于甲方所有。')
    assert rows['licensee_improvement_ownership']['status']=='MISSING'
    assert rows['licensor_improvement_ownership']['status']=='PARTIALLY_COVERED'


def test_bounded_use_rights_preserve_actor_object_and_scope():
    text='第一条 成果\n通用技术组件归乙方，但甲方享有免费且不可撤销的项目使用权。乙方有权继续使用不包含甲方专有信息的通用技术经验。'
    rows=atoms('development_result',text)
    assert rows['commissioning_party_use_right']['status']=='PARTIALLY_COVERED'
    assert rows['developer_use_restriction']['status']=='PARTIALLY_COVERED'
    assert rows['third_party_disclosure_transfer']['status']=='MISSING'
    assert all(s['quote'] in text for e in rows.values() for s in e['supporting_evidence'])


def test_explicit_nonagreement_is_not_positive_notice():
    row=atoms('improvement_notification','第一条 后续改进\n双方未约定完成改进成果后必须通知另一方。')['improvement_result_notification']
    assert row['status']=='MISSING'
    assert not row['supporting_evidence']
    assert row['explicit_absence_evidence']


def test_phase_delay_links_termination_without_penalty():
    text='第一条 技术开发\n乙方研发平台。\n第二条 项目延期\n关键阶段延期超过12日应整改。延期超过40日，甲方有权解除合同。因乙方违约造成直接损失的应承担赔偿责任。'
    row=next(e for e in development_exit_elements(parse_contract_clauses(text)) if e['element_id']=='development_delay_liability')
    assert row['status']=='COVERED'
    assert any('解除' in s['quote'] for s in row['supporting_evidence'])
    assert any('直接损失' in s['quote'] for s in row['supporting_evidence'])


def test_client_caused_delay_exemption_is_not_developer_remedy():
    text='第一条 技术开发\n乙方开发系统。\n第二条 项目延期\n因甲方迟延提供资料造成延期，乙方不承担迟延责任。'
    row=next(e for e in development_exit_elements(parse_contract_clauses(text)) if e['element_id']=='development_delay_liability')
    assert row['status']=='MISSING'


def test_positive_gate_requires_exact_element_ownership():
    from types import SimpleNamespace
    from review_v2.element_evidence_projection import positive_coverage_sources
    source=dict(clause_id='C1',quote='应支付API费用',support_type='DIRECT',matched_terms=['费用'])
    item=SimpleNamespace(coverage_elements=[dict(element_id='notice',status='MISSING')],evidence_clauses=[source])
    assert not positive_coverage_sources(item)
    source['supporting_element_ids']=['fee']
    item.coverage_elements.append(dict(element_id='fee',status='COVERED',supporting_evidence=[dict(source)]))
    assert positive_coverage_sources(item)==[source]


@pytest.fixture(scope='module')
def uploaded():
    root=Path(__file__).resolve().parents[2]
    source=root/'artifacts/technology_pass_semantics/round14_entrusted_input/original.docx'
    with TestClient(app) as client:
        response=client.post('/review-v2/file',headers={'Authorization':'Bearer '+create_access_token({'user_id':'1'})},
            data={'contract_type':'technology','use_llm':'false','profile_json':json.dumps({'user_identity':'甲方'})},
            files={'file':('original.docx',source.read_bytes(),'application/vnd.openxmlformats-officedocument.wordprocessingml.document')})
    assert response.status_code==200
    report=response.json()
    (root/'artifacts/technology_pass_semantics/round14_offline_report.json').write_text(json.dumps(report,ensure_ascii=False),encoding='utf8')
    return report


def test_upload_preserves_partial_component_and_exact_gaps(uploaded):
    item=next(i for i in uploaded['items'] if i['item_id']=='TC-12-02')
    assert item['coverage_status']=='部分覆盖'
    rows={e['element_id']:e for e in item['coverage_elements']}
    assert rows['component_selection_control']['status']=='COVERED'
    assert rows['license_or_replacement_remedy']['status']=='MISSING'
    assert rows['claim_notice']['status']=='MISSING'


def test_upload_shared_lists_and_acceptance(uploaded):
    items={i['item_id']:i for i in uploaded['items']}
    for rid,key in [('TC-04-01','acceptance'),('TC-05-04','development_delay_liability'),
                    ('TC-11-02','confidentiality_exceptions'),('TC-13-01','operation_document_delivery'),
                    ('TC-13-01','test_report_delivery'),('TC-13-03','test_report_delivery')]:
        row=next(e for e in items[rid]['coverage_elements'] if e['element_id']==key)
        assert row['status']=='COVERED',(rid,row)
        assert row['source_spans'] and row['source_clause_ids']


def test_whole_upload_gate(uploaded):
    assert uploaded['release_quality_gate']['status']=='REPORT_READY',uploaded['release_quality_gate']['failures']
