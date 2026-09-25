"""Canonical positive facts must survive cooperative rule projection."""
import json
from pathlib import Path

import pytest
from docx import Document
from fastapi.testclient import TestClient
from auth.utils import create_access_token
from main import app
from review_v2.clause_parser import parse_contract_clauses
from review_v2.development_exit import development_exit_elements

SOURCE = Path(__file__).resolve().parents[2] / 'artifacts/technology_pass_semantics/round12_cooperative_input/original.docx'


@pytest.fixture(scope='module')
def uploaded():
    with TestClient(app) as client:
        response = client.post('/review-v2/file',
            headers={'Authorization': 'Bearer ' + create_access_token({'user_id': '1'})},
            data={'contract_type': 'technology', 'use_llm': 'false',
                  'profile_json': json.dumps({'user_identity': '甲方'})},
            files={'file': ('original.docx', SOURCE.read_bytes(),
                           'application/vnd.openxmlformats-officedocument.wordprocessingml.document')})
    assert response.status_code == 200
    result = response.json()
    # Diagnostic artifact, never a source for the review.
    (SOURCE.parent.parent / 'round12_offline_report.json').write_text(
        json.dumps(result, ensure_ascii=False, indent=2), encoding='utf8')
    return result


def element(report, rule, key):
    item = next(i for i in report['items'] if i['item_id'] == rule)
    return next(e for e in item['coverage_elements'] if e['element_id'] == key)


def test_fixed_confidentiality_term_survives_normal_upload(uploaded):
    row = element(uploaded, 'TC-11-02', 'confidentiality_period')
    assert row['status'] == 'COVERED', row
    assert any('自本合同生效之日起持续5年' in q for q in row['source_spans'])
    assert row['source_fact_key'] == 'confidentiality.confidentiality_duration'


def test_delay_termination_and_damages_survive_normal_upload(uploaded):
    row = element(uploaded, 'TC-05-04', 'development_delay_liability')
    assert row['status'] == 'COVERED', row
    original = '\n'.join(p.text for p in Document(SOURCE).paragraphs)
    assert all(q in original for q in row['source_spans'])
    assert any('解除合同' in q for q in row['source_spans'])
    assert any('直接经济损失' in q for q in row['source_spans'])


@pytest.mark.parametrize('remedy', ['守约方有权解除合同', '违约方应赔偿直接经济损失'])
def test_development_delay_non_penalty_remedies(remedy):
    text = f'第一条 研发任务\n双方共同开发设备。\n第二条 延期责任\n关键开发任务延期超过45日的，{remedy}。'
    rows = {e['element_id']: e for e in development_exit_elements(parse_contract_clauses(text))}
    assert rows['development_delay_liability']['status'] == 'COVERED'
    assert rows['payment_delay_liability']['status'] == 'MISSING'


def test_linked_delay_remedies_keep_separate_spans():
    text = '第一条 开发延期\n一方负责的研发任务延期的，应提交整改计划。延期超过六十日的，另一方有权终止合同。违约方应承担由此造成的损失。'
    row = next(e for e in development_exit_elements(parse_contract_clauses(text))
               if e['element_id'] == 'development_delay_liability')
    assert row['status'] == 'COVERED'
    assert any('损失' in s['quote'] for s in row['supporting_evidence'])
    assert all(s['quote'] in text for s in row['supporting_evidence'])


def test_payment_delay_cannot_supply_development_delay_remedy():
    text = '第一条 研发任务\n双方负责研究开发。\n第二条 付款\n延期支付费用超过20日的，收款人有权解除合同并要求赔偿损失。'
    row = next(e for e in development_exit_elements(parse_contract_clauses(text))
               if e['element_id'] == 'development_delay_liability')
    assert row['status'] == 'MISSING'


def test_unrelated_damages_cannot_complete_delay_fact():
    text = '第一条 开发进度\n开发任务可能延期。\n第二条 保密\n违反保密义务的，应赔偿损失。'
    row = next(e for e in development_exit_elements(parse_contract_clauses(text))
               if e['element_id'] == 'development_delay_liability')
    assert row['status'] == 'MISSING'


def test_fixed_term_does_not_invent_post_termination_survival():
    from review_v2.engine import _atomic_requirement_family
    text = '第一条 保密\n双方应对技术资料保密，保密义务自生效日起持续36个月。'
    rows = {r['element_id']: r for r in _atomic_requirement_family('confidentiality_detail', parse_contract_clauses(text))}
    assert rows['confidentiality_duration']['status'] == 'COVERED'
    assert rows['post_termination_confidentiality']['status'] == 'MISSING'


def test_unnumbered_exception_list_preserves_definition_relation():
    from review_v2.engine import _atomic_requirement_family
    text = ('第一条 保密\n下列信息不属于保密信息：\n已经公开的信息；\n'
            '接收方在披露前已经合法掌握的信息；\n从第三方合法取得的信息；\n'
            '根据法律要求必须披露的信息。\n保密义务持续七年。')
    row = next(r for r in _atomic_requirement_family('confidentiality_fields', parse_contract_clauses(text))
               if r['element_id'] == 'confidentiality_exceptions')
    assert row['status'] == 'PARTIALLY_COVERED'
    assert row['residual_gap'] == '独立开发信息例外'
    assert all(s['quote'] in text for s in row['supporting_evidence'])
