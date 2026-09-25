"""Licence scope fields and remedies must retain the actual transaction actor."""
import pytest
from review_v2.clause_parser import parse_contract_clauses
from review_v2.technology_fact_ontology import license_scope_elements
from review_v2.license_control_facts import elements


@pytest.mark.parametrize('area,acts', [
    ('欧洲经济区', '制造、使用、销售'),
    ('中国大陆地区', '制造、使用、销售、许诺销售'),
])
def test_scope_enumeration_inherits_operative_context(area, acts):
    text = f'第四条 许可范围\n被许可方可以在下列范围内实施专利：\n地域：{area}；\n实施方式：{acts}。'
    rows = {r['element_id']: r for r in license_scope_elements(parse_contract_clauses(text))}
    for key in ('license_territory', 'permitted_implementation_acts'):
        assert rows[key]['status'] == 'COVERED'
        assert all(s['quote'] in text for s in rows[key]['supporting_evidence'])


def test_unrelated_address_does_not_supply_license_territory():
    rows = license_scope_elements(parse_contract_clauses('第二条 公司资料\n地域：中国大陆地区。'))
    assert next(r for r in rows if r['element_id'] == 'license_territory')['status'] == 'MISSING'


def test_term_is_not_negated_by_another_obligation_in_same_sentence():
    rows = license_scope_elements(parse_contract_clauses(
        '许可期限五年，甲方不得超出许可地域、用途或者许可方式实施本专利。'))
    assert next(r for r in rows if r['element_id'] == 'license_term')['status'] == 'COVERED'


@pytest.mark.parametrize('text', ['甲方违反排他许可约定，应赔偿损失。',
                                  '甲方曾向第三方授予独占许可，许可期限五年。'])
def test_breach_or_historical_grant_does_not_establish_current_license_type(text):
    rows = license_scope_elements(parse_contract_clauses(text))
    assert next(r for r in rows if r['element_id'] == 'license_type')['status'] == 'MISSING'


def test_element_audit_retains_public_fields_and_audit_identity():
    from types import SimpleNamespace
    from review_v2.element_evidence_projection import _audits
    item = SimpleNamespace(item_id='TC-07-03', risk_group='license_over_scope_liability',
        coverage_elements=[dict(element_id='damage_compensation', status='MISSING',
                                source_fact_key='license_control.damage_compensation')],
        decision_trace={'element_absence_searches': [dict(element_id='damage_compensation',
            result='NOT_FOUND', searched_document_hash='verified-corpus',
            search_targets=['超范围违约损失赔偿'], searched_clause_ids=['C0001'])]})
    row = _audits(item)[0]
    assert row['quote'] == row['quoted_text']
    assert row['location'] == row['source_type'] == 'SEARCH_AUDIT'
    assert row['derived_or_original'] == 'AUDIT'
    assert row['supporting_element_ids'] == ['damage_compensation']


@pytest.mark.parametrize('provider,recipient', [('甲方', '乙方'), ('乙方', '甲方')])
def test_exclusivity_compensation_is_not_sublicensee_compensation(provider, recipient):
    stop = f'{recipient}未经{provider}书面同意擅自向第三方进行分许可的，{provider}有权要求{recipient}停止分许可行为。'
    other = f'{provider}违反排他许可约定，在相同许可范围内再次向第三方提供许可的，{recipient}有权要求{provider}停止违约行为并赔偿因此造成的实际损失。'
    rows = {r['element_id']: r for r in elements('license_scope_remedies', parse_contract_clauses('第七条 违约责任\n' + stop + '\n' + other))}
    assert rows['over_scope_breach_remedy']['status'] == 'COVERED'
    assert rows['stop_breach_obligation']['status'] == 'COVERED'
    assert rows['damage_compensation']['status'] == 'MISSING'
    assert rows['stop_breach_obligation']['supporting_evidence'][0]['quote'] == stop
    assert all(s['quote'] != other for r in rows.values() for s in r['supporting_evidence'])


def test_sublicensee_explicit_compensation_is_preserved():
    text = '第七条 乙方未经甲方书面同意向第三方分许可的，乙方应停止分许可并赔偿甲方因此遭受的损失。'
    rows = {r['element_id']: r for r in elements('license_scope_remedies', parse_contract_clauses(text))}
    assert rows['damage_compensation']['status'] == 'COVERED'


def test_breach_reference_preserves_recipient_responsibility():
    text = '第八条 责任\n买方违反第三条关于许可范围及禁止擅自向第三方提供技术秘密的约定，应停止违约行为并赔偿卖方因此遭受的可证明损失。'
    rows = {r['element_id']: r for r in elements('license_scope_remedies', parse_contract_clauses(text))}
    assert rows['over_scope_breach_remedy']['status'] == 'COVERED'
    assert rows['damage_compensation']['status'] == 'COVERED'
    assert rows['stop_breach_obligation']['status'] == 'COVERED'


@pytest.mark.parametrize('provider,recipient', [('甲方', '乙方'), ('乙方', '甲方')])
def test_declared_provider_cannot_supply_recipient_breach_fact(provider, recipient):
    text = f'{provider}（许可方）：甲公司\n{recipient}（被许可方）：乙公司\n第三条\n{provider}超出许可范围实施时，应停止违约并赔偿损失。'
    rows = elements('license_scope_remedies', parse_contract_clauses(text))
    assert next(r for r in rows if r['element_id'] == 'over_scope_breach_remedy')['status'] == 'MISSING'


def test_registry_fields_in_same_article_keep_distinct_sources():
    from review_v2.contract_facts import extract_contract_fact_graph
    from review_v2.engine import _technology_registry_evidence
    clauses = parse_contract_clauses('第一条 专利信息\n专利名称：设备检测装置。\n专利号：ZL202211234567.8。\n专利权人：甲公司。')
    graph = extract_contract_fact_graph(clauses)
    name = _technology_registry_evidence(graph, clauses, 'technology.patent.name')
    number = _technology_registry_evidence(graph, clauses, 'technology.patent.number')
    assert name and number and name[0]['evidence_id'] != number[0]['evidence_id']
    assert '专利号' in number[0]['quote'] and '专利名称' not in number[0]['quote']


def test_normal_upload_preserves_license_element_ownership():
    import json
    from pathlib import Path
    from fastapi.testclient import TestClient
    from main import app
    from auth.utils import create_access_token
    source = Path(__file__).resolve().parents[2] / 'artifacts/technology_pass_semantics/round17_license_input/original.docx'
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
    items = {i['item_id']: i for i in report['items']}
    scope = {e['element_id']: e for e in items['TC-07-01']['coverage_elements']}
    assert scope['license_territory']['status'] == scope['permitted_implementation_acts']['status'] == 'COVERED'
    remedies = {e['element_id']: e for e in items['TC-07-03']['coverage_elements']}
    assert remedies['damage_compensation']['status'] == 'MISSING'
    assert remedies['stop_breach_obligation']['status'] == 'COVERED'
    assert all('甲方违反排他许可' not in span for e in remedies.values() for span in e.get('source_spans', []))
