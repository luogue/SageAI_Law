"""Independent component coverage and scoped arrangement polarity regressions."""
import pytest
from review_v2.clause_parser import parse_contract_clauses
from review_v2.proposition_scope import arrangement_matches
from review_v2.license_control_facts import elements
from review_v2.obligation_detail_elements import confidentiality_detail_elements
from review_v2.technology_service_analysis import analyze_technical_secret_loss_arrangement
from review_v2.engine import extract_semantic_field_value


@pytest.mark.parametrize('mode', ['普通', '非独占', '排他', '独占'])
@pytest.mark.parametrize('verb', ['', '使用', '实施'])
def test_license_mode_aliases(mode, verb):
    text = f'第三条 许可性质\n甲方授予乙方本合同项下技术秘密的{mode}{verb}许可。'
    row = next(e for e in elements('secret_license_scope', parse_contract_clauses(text)) if e['element_id'] == 'license_type')
    assert row['status'] == 'COVERED'
    assert row['supporting_evidence'][0]['quote'] in text


@pytest.mark.parametrize('statement', [
    '双方未明确约定普通使用许可。', '是否授予普通使用许可，双方未作明确约定。',
    '甲方不得授予普通使用许可。', '普通使用许可是指非独占地使用技术。',
    '甲方曾向第三方授予普通使用许可。',
])
def test_license_mode_requires_operative_declaration(statement):
    rows = elements('secret_license_scope', parse_contract_clauses('第三条 许可性质\n' + statement))
    assert next(e for e in rows if e['element_id'] == 'license_type')['status'] == 'MISSING'


@pytest.mark.parametrize('term', ['非独占实施许可', '非独占使用许可', '非独占、不可转让的专利实施许可'])
def test_nonexclusive_mode_keeps_its_prefix_under_grant_context(term):
    from review_v2.technology_service_analysis import analyze_patent_license_consistency
    result = analyze_patent_license_consistency('许可方授予接受方在中华人民共和国境内' + term + '。')
    assert result['license_type'] == 'NON_EXCLUSIVE'


@pytest.mark.parametrize('header', ['下列信息不属于本合同保密范围：', '以下信息不属于保密信息：', '下列信息不属于本合同项下保密信息：'])
def test_exception_components_remain_independent(header):
    text = '第八条 保密义务\n' + header + '\n接收方取得时已经公开的信息；\n非因接收方违反本合同而公开的信息；\n接收方从有权披露该信息的第三方合法取得的信息。'
    rows = confidentiality_detail_elements(parse_contract_clauses(text), extract_field=extract_semantic_field_value)
    row = next(r for r in rows if r['element_id'] == 'confidentiality_exceptions')
    assert row['status'] == 'PARTIALLY_COVERED'
    children = {r['required_fact']: r for r in row['component_coverage']}
    assert children['公开信息例外']['status'] == 'COVERED'
    assert children['合法取得信息例外']['status'] == 'COVERED'
    assert children['独立开发信息例外']['status'] == 'MISSING'
    assert children['依法披露例外']['status'] == 'MISSING'
    assert row['search_targets'] == ['独立开发信息例外', '依法披露例外']


@pytest.mark.parametrize('statement,expected', [
    ('对于秘密性丧失后是否继续支付许可费，双方未作明确约定。', False),
    ('是否继续支付许可费，双方未约定。', False),
    ('继续支付许可费的安排，双方未作明确约定。', False),
    ('乙方是否继续支付许可费。', False),
    ('双方未明确约定继续支付许可费。', False),
    ('双方未作约定：\n乙方继续支付许可费；\n乙方不得解除合同。', False),
    ('乙方不再继续支付许可费。', False),
    ('乙方无需继续支付许可费。', False),
    ('乙方不得继续支付许可费。', False),
    ('如技术秘密公开，乙方继续支付许可费。', True),
    ('若技术秘密丧失秘密性，乙方仍须支付尚未到期许可费。', True),
    ('乙方不得停止支付许可费。', True),
])
def test_arrangement_polarity_at_producer(statement, expected):
    text = '第十条 技术秘密公开\n技术秘密进入公开领域后，双方应协商。\n' + statement
    loss = analyze_technical_secret_loss_arrangement(text)
    assert loss['unconditional_future_payment'] is expected
    assert loss['fee_stop_or_reduction'] is False
    for fact in loss['fact_sources']['future_license_fee_continues']:
        assert fact['quote'] in text
    if statement.startswith(('如', '若')):
        assert loss['fact_sources']['future_license_fee_continues'][0]['condition']


def test_secret_loss_triggers_each_keep_their_source():
    text = """第十条 技术秘密公开及秘密性丧失
甲方主动向社会公开本合同核心技术秘密的，应及时通知乙方。
因第三方独立研究、反向工程或者其他非因甲乙双方违约的原因导致部分技术信息公开的，双方应协商相关技术的后续使用安排。
对于技术秘密全部丧失秘密性后乙方是否仍需继续支付尚未到期的固定许可费以及销售提成费，双方未作明确约定。
"""
    loss = analyze_technical_secret_loss_arrangement(text)
    assert loss['secret_loss_trigger'] is True
    assert loss['unconditional_future_payment'] is False
    assert loss['adverse'] is False
    children = {r['element_id']: r for r in loss['trigger_components']}
    for key in ('licensor_active_disclosure', 'independent_research_disclosure', 'reverse_engineering_disclosure', 'partial_disclosure'):
        assert children[key]['status'] == 'COVERED'
        assert all(s['quote'] in text for s in children[key]['supporting_evidence'])
    assert children['licensor_patent_disclosure']['status'] == 'MISSING'
    assert loss['secret_loss_notification'] is True


def test_arrangement_scope_never_imports_neighboring_article_payment():
    loss = analyze_technical_secret_loss_arrangement('第一条 技术秘密公开\n甲方主动公开技术秘密的，应通知乙方。\n第二条 付款\n乙方继续支付许可费。')
    assert loss['secret_loss_trigger']
    assert not loss['unconditional_future_payment']


@pytest.mark.parametrize('party', ['甲方/许可方', '乙方/被许可方'])
def test_current_contract_final_semantic_states(party, tmp_path):
    from pathlib import Path
    import json
    from review_v2.engine import review_contract_v2
    from review_v2.user_profile import UserRiskProfile
    text = Path(__file__).with_name('fixtures').joinpath('technical_secret_component_contract.txt').read_text(encoding='utf-8')
    report = review_contract_v2(text, 'technology', use_llm=False, profile=UserRiskProfile(user_identity=party))
    (tmp_path / 'report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    items = {r['item_id']: r for r in report['items']}
    def rows(key):
        return {r['element_id']: r for r in items[key]['coverage_elements']}
    assert rows('TC-07-01')['license_type']['status'] == 'COVERED'
    exception = rows('TC-11-02')['confidentiality_exceptions']
    assert exception['status'] == 'PARTIALLY_COVERED'
    assert exception['search_targets'] == ['独立开发信息例外', '依法披露例外']
    assert exception['proposition'] == '已明确：公开信息例外、合法取得信息例外；未明确：独立开发信息例外、依法披露例外。'
    components = {r['required_fact']: r['status'] for r in exception['component_coverage']}
    assert components == {'公开信息例外': 'COVERED', '合法取得信息例外': 'COVERED', '独立开发信息例外': 'MISSING', '依法披露例外': 'MISSING'}
    loss = rows('TC-12-03')
    assert loss['future_fee_after_secret_loss']['status'] == 'MISSING'
    assert loss['future_fee_after_secret_loss']['direction'] != 'ADVERSE'
    assert loss['secret_loss_trigger']['status'] == 'COVERED'
    assert '进入公共领域' not in loss['secret_loss_trigger']['proposition']
    assert '申请专利' not in loss['secret_loss_trigger']['proposition']
    triggers = {r['element_id']: r['status'] for r in loss['secret_loss_trigger']['component_coverage']}
    assert triggers['licensor_active_disclosure'] == triggers['independent_research_disclosure'] == triggers['reverse_engineering_disclosure'] == 'COVERED'
    assert items['TC-02-02']['coverage_status'] == '通过'
    assert report['release_quality_gate']['status'] == 'REPORT_READY'


@pytest.mark.parametrize('text', [
    '双方未明确约定公开信息例外。',
    '双方未明确约定下列保密例外：\n已经公开的信息；\n第三方合法取得的信息。',
    '双方未约定：\n已经公开的信息不属于保密信息；\n独立开发的信息不属于保密信息。',
])
def test_missing_exception_lists_cannot_create_coverage(text):
    rows = confidentiality_detail_elements(parse_contract_clauses('第八条 保密\n' + text), extract_field=extract_semantic_field_value)
    row = next(r for r in rows if r['element_id'] == 'confidentiality_exceptions')
    assert row['status'] == 'MISSING'
    assert all(c['status'] == 'MISSING' for c in row['component_coverage'])


@pytest.mark.parametrize('statement', ['如技术秘密公开，乙方仍须继续支付许可费，不得解除合同。', '技术秘密被第三方公开后，乙方不得停止支付许可费，不得单方解除合同。'])
def test_actual_conditional_adverse_bargain_is_preserved(statement):
    loss = analyze_technical_secret_loss_arrangement('第十条 技术秘密公开\n' + statement)
    assert loss['adverse'] is True
    assert loss['unconditional_future_payment'] is True
    assert loss['termination_restricted'] is True
    assert loss['fee_stop_or_reduction'] is False


def test_conditional_list_preserves_event_scope_and_arrangement_existence():
    from review_v2.technology_adverse_evidence import has_actual_infringement
    assert not has_actual_infringement('如果发生下列情况：\n本技术被确认侵犯第三方专利；\n双方应协商解决。')
    loss = analyze_technical_secret_loss_arrangement('第十条 技术秘密公开\n即使技术秘密全部公开：\n乙方继续支付许可费；\n乙方不得解除合同。')
    assert loss['adverse']
    source = loss['fact_sources']['future_license_fee_continues'][0]
    assert source['condition_context'] == '即使技术秘密全部公开：'
    assert source['event_polarity'] == 'CONDITIONAL'
    assert source['arrangement_polarity'] == 'AFFIRMATIVE'


def test_heading_alone_does_not_establish_secret_loss_arrangement():
    loss = analyze_technical_secret_loss_arrangement('第十条 技术秘密丧失秘密性\n双方未明确约定。')
    assert not loss['secret_loss_trigger']
