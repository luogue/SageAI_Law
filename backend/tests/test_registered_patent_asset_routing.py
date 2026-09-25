"""Transfer assets, confidential supporting materials and exact claim sources."""
import pytest
from review_v2.technology_service_analysis import classify_technology_transaction
from review_v2.clause_parser import parse_contract_clauses
from review_v2.technology_patent_transfer_analysis import extract_third_party_claim_protection_facts


PATENT = '''专利权转让合同
甲方（转让方）：创新公司
乙方（受让方）：应用公司
第一条 标的
甲方将本项发明专利权全部转让给乙方。专利号：ZL202212345678.9。
授权公告日期：2024年5月6日。甲方为登记专利权人。
第二条 登记
双方共同办理专利权变更登记。乙方向甲方支付转让价款。
'''


@pytest.mark.parametrize('material', ['源代码', '算法文档', '非公开技术资料', '专有技术资料'])
def test_confidential_documents_do_not_replace_registered_transfer_asset(material):
    result = classify_technology_transaction(PATENT + f'第三条 保密\n双方不得向他人披露{material}，终止后返还{material}。')
    assert result['subtype'] == 'TECHNOLOGY_TRANSFER'
    assert result['tertiary_subtype'] == 'PATENT_RIGHT_TRANSFER'
    assert not result['independent_secret_transaction']


def test_independent_secret_grant_preserved_beside_patent():
    result = classify_technology_transaction(PATENT + '第三条 独立标的\n甲方将技术秘密全部转让给乙方，另行支付对价。')
    assert result['independent_secret_transaction']


@pytest.mark.parametrize('provider,recipient', [('甲方', '乙方'), ('乙方', '甲方')])
def test_claim_duties_follow_declared_roles_and_preserve_sources(provider, recipient):
    text = f'''{provider}（转让方）：出让公司
{recipient}（受让方）：受让公司
第一条 第三方主张
如第三方主张专利存在权属瑕疵，{provider}应在收到{recipient}通知后提供权属文件并协助处理。
如权属瑕疵导致无法取得专利权，{provider}应退还全部价款并赔偿直接损失。'''
    facts = extract_third_party_claim_protection_facts(parse_contract_clauses(text))
    for key in ['claim_trigger', 'claim_participation', 'claim_document_assistance', 'claim_refund', 'claim_damages']:
        assert facts.get(key), key
        assert all(row['quote'] in text for row in facts[key])
    assert not facts.get('claim_notice'), 'Receiving a notice is not a duty to give notice'
    assert not facts.get('claim_defense_cost')


def test_recipient_cost_obligation_not_assigned_to_provider():
    text = '甲方（转让方）：甲公司\n乙方（受让方）：乙公司\n第一条\n第三方提出侵权主张时，乙方应承担律师费和诉讼费。'
    facts = extract_third_party_claim_protection_facts(parse_contract_clauses(text))
    assert not facts.get('claim_defense_cost')


def test_claim_object_is_not_promoted_to_liability_subject():
    from review_v2.technology_service_analysis import extract_claim_response_facts
    text = '第一条\n第三方提出权利主张，甲方应返还乙方价款，并赔偿乙方直接损失。双方未明确约定抗辩控制权。'
    facts = extract_claim_response_facts(parse_contract_clauses(text), '甲方', '乙方')
    assert facts['damages_allocation'][0]['actor'] == 'LICENSOR'
    assert not facts.get('defense_control')


@pytest.mark.parametrize('action', ['警告', '投诉', '诉讼'])
def test_inbound_enforcement_event_owns_following_expense_allocation(action):
    from review_v2.technology_service_analysis import extract_claim_response_facts
    text = f'第一条\n甲方实施技术受到第三方{action}：\n甲方应自行处理；\n律师费和诉讼费由甲方承担。'
    facts = extract_claim_response_facts(parse_contract_clauses(text), '乙方', '甲方')
    assert facts['claim_cost_allocation'][0]['actor'] == 'LICENSEE'
    assert facts['claim_cost_allocation'][0]['quote'] in text


def test_registered_owner_contract_authority_is_a_representation():
    from review_v2.technology_patent_transfer_analysis import extract_transfer_authority_facts
    text = '甲方（转让方）：甲公司\n乙方（受让方）：乙公司\n第一条\n甲方为该专利登记专利权人，有权签订本合同。'
    facts = extract_transfer_authority_facts(parse_contract_clauses(text))
    assert facts and facts[0]['evidence_level'] == 'CONTRACTUAL_REPRESENTATION'
    assert facts[0]['quote'] in text


def test_missing_procedure_does_not_erase_neighboring_cost_duty():
    from review_v2.technology_service_analysis import extract_claim_response_facts
    text = '第一条\n如第三方提出侵权主张，双方未明确约定抗辩控制权，但甲方应承担律师费。'
    facts = extract_claim_response_facts(parse_contract_clauses(text), '甲方', '乙方')
    assert not facts.get('defense_control')
    assert facts['claim_cost_allocation'][0]['actor'] == 'LICENSOR'


def test_actual_patent_upload_routes_and_keeps_source_bound_report():
    import json
    from pathlib import Path
    from fastapi.testclient import TestClient
    from main import app
    from auth.utils import create_access_token
    root = Path(__file__).resolve().parents[2]
    source = root / 'artifacts/technology_pass_semantics/round15_patent_input/original.docx'
    with TestClient(app) as client:
        response = client.post('/review-v2/file',
            headers={'Authorization': 'Bearer '+create_access_token({'user_id': '1'})},
            data={'contract_type': 'technology', 'use_llm': 'false',
                  'profile_json': json.dumps({'user_identity': '乙方'})},
            files={'file': ('original.docx', source.read_bytes(),
                           'application/vnd.openxmlformats-officedocument.wordprocessingml.document')})
    assert response.status_code == 200
    report = response.json()
    (root / 'artifacts/technology_pass_semantics/round15_test_report.json').write_text(
        json.dumps(report, ensure_ascii=False), encoding='utf8')
    assert report['release_quality_gate']['status'] == 'REPORT_READY', report['release_quality_gate']['failures']
    items = {i['item_id']: i for i in report['items']}
    assert items['TC-12-03']['coverage_status'] == '不适用'
    assert items['TC-06-04']['coverage_status'] != '不适用'
    assert items['TC-12-02']['coverage_status'] == '部分覆盖'
    assert '已付转让费的20%' not in json.dumps(report['risk_findings'], ensure_ascii=False)
