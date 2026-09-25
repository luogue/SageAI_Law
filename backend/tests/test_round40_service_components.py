from pathlib import Path

import pytest

from review_v2.clause_parser import parse_contract_clauses
from review_v2.technology_service_analysis import declared_service_provider
from review_v2.technology_service_elements import elements


def by_id(family, text):
    return {row['element_id']: row for row in elements(family, parse_contract_clauses(text))}


def test_commission_sentence_declares_provider_and_scopes_claim_duties():
    text = (
        '技术服务合同\n乙方接受甲方委托，提供节能技术服务。\n'
        '第八条 第三方软件及工具\n'
        '因乙方擅自使用无合法授权的软件导致第三方向甲方主张权利的，'
        '乙方应负责处理其自身使用行为引起的争议，并承担因此给甲方造成的合理直接损失。'
    )
    assert declared_service_provider(text) == '乙方'
    rows = by_id('service_claims', text)
    for key in ('claim_handling_responsibility', 'provider_infringement_liability', 'direct_damage'):
        assert rows[key]['status'] == 'COVERED'
        assert rows[key]['supporting_evidence']


def test_service_end_return_or_delete_has_independent_components():
    rows = by_id('material_exit',
        '技术服务合同\n服务结束后，乙方应根据甲方要求返还或删除甲方提供的原始业务数据；依法必须保存的除外。')
    disposition = rows['termination_return_or_delete']
    assert disposition['status'] == 'COVERED'
    states = {row['element_id']: row['status'] for row in disposition['component_coverage']}
    assert states == {
        'service_end_disposition_trigger': 'COVERED',
        'original_data_return': 'COVERED',
        'original_data_deletion': 'COVERED',
    }
    assert rows['confidential_backup_deletion']['status'] == 'MISSING'


@pytest.mark.parametrize('verb', ['修改', '完成修改', '整改', '补正'])
def test_defect_rectification_and_deadline_accept_common_verbs(verb):
    rows = by_id('service_quality',
        f'技术服务合同\n第六条 验收\n对于存在实质性缺陷的成果，甲方应说明具体问题，乙方应在收到意见后十个工作日内{verb}。')
    assert rows['rectification_mechanism']['status'] == 'COVERED'
    assert rows['rectification_deadline']['status'] == 'COVERED'


def test_survival_fact_is_separate_from_fixed_duration():
    from review_v2.engine import _atomic_requirement_family
    clauses = parse_contract_clauses('技术服务合同\n第十条 保密\n保密义务不因本合同终止而自动失效。')
    rows = {row['element_id']: row for row in _atomic_requirement_family('confidentiality_fields', clauses)}
    assert rows['post_termination_confidentiality']['status'] == 'COVERED'
    assert rows['confidentiality_period']['status'] == 'MISSING'


@pytest.mark.parametrize('party', ['甲方', '乙方'])
def test_round40_final_components_have_fact_and_direct_evidence(party):
    from review_v2.engine import review_contract_v2
    from review_v2.user_profile import UserRiskProfile

    text = (Path(__file__).parent / 'fixtures' / 'round40_service.txt').read_text(encoding='utf8')
    report = review_contract_v2(text, 'technology', use_llm=False,
        profile=UserRiskProfile(user_identity=party))
    assert report['release_quality_gate']['status'] == 'REPORT_READY', report['release_quality_gate']['failures']
    items = {row['item_id']: row for row in report['items']}
    expected = {
        'TC-12-02': ('claim_handling_responsibility', 'provider_infringement_liability', 'direct_damage'),
        'TC-11-03': ('termination_return_or_delete',),
        'TC-09-02': ('written_objection_mechanism', 'rectification_mechanism', 'rectification_deadline'),
        'TC-11-02': ('post_termination_confidentiality',),
    }
    for rule, keys in expected.items():
        item = items[rule]
        rows = {row['element_id']: row for row in item['coverage_elements']}
        missing_audits = {row['element_id'] for row in item['decision_trace'].get('element_absence_searches', [])
                          if row.get('result') == 'NOT_FOUND'}
        facts = item['decision_trace']['contract_fact_registry_consumption']['facts']
        for key in keys:
            element = rows[key]
            assert element['status'] == 'COVERED'
            assert key not in missing_audits
            assert facts[element['source_fact_key']]['status'] == 'FOUND'
            evidence = [row for row in item['evidence_clauses'] if row['evidence_id'] in element['evidence_ids']]
            assert evidence and all(row['support_type'] == 'DIRECT' and row['verified_original'] for row in evidence), (
                rule, key, element['evidence_ids'],
                [(row['evidence_id'], row.get('support_type')) for row in item['evidence_clauses']],
            )
    assert items['TC-11-03']['coverage_status'] == '部分覆盖'
    assert items['TC-09-02']['coverage_status'] == '部分覆盖'
    assert items['TC-11-02']['coverage_status'] == '部分覆盖'
    gate = report['release_quality_gate']['gate_results']
    assert gate['REVIEW_EVIDENCE_ELEMENT_MISMATCH'] == 'PASS'
    assert gate['EXACT_ELEMENT_REPORT_INVARIANT'] == 'PASS'
