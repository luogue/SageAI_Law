"""Role, list-scope and liability-condition preservation across transfer facts."""
import pytest
from review_v2.clause_parser import parse_contract_clauses
from review_v2.perspective_resolution import resolve_perspective
from review_v2.technology_patent_transfer_analysis import (
    extract_transfer_authority_facts, extract_third_party_claim_protection_facts,
)


@pytest.mark.parametrize('provider,recipient', [('甲方', '乙方'), ('乙方', '甲方')])
def test_declared_transfer_roles_drive_display_and_list_warranty(provider, recipient):
    text = f'{provider}（转让方）：甲公司\n{recipient}（受让方）：乙公司\n第六条 权利保证\n{provider}保证：\n其为本合同专利的合法专利权人；\n有权处分该专利权。'
    p = resolve_perspective(recipient, 'TECHNOLOGY', contract_subtype='PATENT_RIGHT_TRANSFER', contract_text=text)
    assert p.canonical_role == 'PATENT_TRANSFEREE'
    assert p.display_role == recipient + ' / 专利权受让方'
    rows = extract_transfer_authority_facts(parse_contract_clauses(text))
    assert rows and rows[0]['actor'] == provider
    assert all(row['quote'] in text for row in rows)
    assert '保证' in rows[0]['quote'] and '有权处分' in rows[0]['quote']


@pytest.mark.parametrize('provider,recipient', [('甲方', '乙方'), ('乙方', '甲方')])
def test_recipient_refund_right_is_not_lost_as_object_of_duty(provider, recipient):
    text = f'{provider}（转让方）：甲公司\n{recipient}（受让方）：乙公司\n第六条\n如{provider}隐瞒权利瑕疵导致无法取得或者正常实施专利权，{recipient}有权解除合同，并要求{provider}返还已支付转让款。'
    facts = extract_third_party_claim_protection_facts(parse_contract_clauses(text))
    assert facts['claim_refund'] and facts['claim_termination']
    assert facts['claim_refund'][0]['quote'] in text


def test_knowledge_condition_remains_attached_to_compensation_fact():
    text = '甲方（转让方）：甲公司\n乙方（受让方）：乙公司\n第十二条\n如第三方提出侵权主张，双方相互通知。如该争议系甲方在签约前已知但故意隐瞒的事实导致，甲方应承担因此给乙方造成的直接经济损失。'
    facts = extract_third_party_claim_protection_facts(parse_contract_clauses(text))
    assert facts['claim_damages']
    assert all(r['limited'] and '故意隐瞒' in r['condition'] for r in facts['claim_damages'])


def test_license_role_does_not_match_opposite_suffix():
    p = resolve_perspective('乙方', 'TECHNOLOGY', contract_subtype='PATENT_LICENSE',
                            contract_text='甲方（许可方）：甲公司\n乙方（被许可方）：乙公司')
    assert p.canonical_role == 'PATENT_LICENSEE'


def test_list_subject_does_not_cross_a_new_express_party():
    text = '甲方（转让方）：甲公司\n乙方（受让方）：乙公司\n第六条\n甲方保证：\n技术资料真实。\n乙方负责资料验收。\n有权处分该专利权。'
    assert not extract_transfer_authority_facts(parse_contract_clauses(text))


def test_future_invalidity_disclaimer_is_not_current_disclosure():
    from review_v2.engine import _current_rights_disclosure_evidence
    rows = [{'clause_id': 'C1', 'quote': '甲方不保证专利在未来任何无效程序中必然维持有效。'}]
    assert not _current_rights_disclosure_evidence(rows, ('无效',))


def test_upload_preserves_role_sources_and_conditional_coverage():
    import json
    from pathlib import Path
    from fastapi.testclient import TestClient
    from main import app
    from auth.utils import create_access_token
    source = Path(__file__).resolve().parents[2] / 'artifacts/technology_pass_semantics/round16_patent_input/original.docx'
    with TestClient(app) as client:
        response = client.post('/review-v2/file',
            headers={'Authorization': 'Bearer ' + create_access_token({'user_id': '1'})},
            data={'contract_type': 'technology', 'use_llm': 'false',
                  'profile_json': json.dumps({'user_identity': '乙方'})},
            files={'file': ('original.docx', source.read_bytes(),
                           'application/vnd.openxmlformats-officedocument.wordprocessingml.document')})
    assert response.status_code == 200
    report = response.json()
    assert report['release_quality_gate']['status'] == 'REPORT_READY', report['release_quality_gate']['failures']
    assert not report['release_quality_gate']['failures']
    assert '乙方 / 专利权受让方' in report['result']
    items = {i['item_id']: i for i in report['items']}
    def element(rule, key):
        return next(e for e in items[rule]['coverage_elements'] if e['element_id'] == key)
    authority = element('TC-06-03', 'transferor_title_and_authority')
    assert authority['status'] == 'COVERED'
    assert any('甲方保证' in span and '有权处分' in span for span in authority['source_spans'])
    refund = element('TC-12-02', 'refund_remedy')
    assert refund['status'] == 'COVERED'
    assert any('要求甲方返还' in span for span in refund['source_spans'])
    allocation = element('TC-12-01', 'liability_allocation_determinability')
    assert items['TC-12-01']['coverage_status'] == '部分覆盖'
    assert allocation['status'] == 'PARTIALLY_COVERED'
    assert allocation['source_fact_key'] == 'claim_fault_condition'
    assert all('故意隐瞒' in span for span in allocation['source_spans'])
    assert items['TC-11-01']['coverage_status'] == '通过'
