"""Transaction, legal relationship and proposition scope remain independent."""
from pathlib import Path
import pytest
from review_v2.clause_parser import parse_contract_clauses
from review_v2.technology_service_analysis import classify_technology_transaction, analyze_technical_secret_loss_arrangement
from review_v2.license_control_facts import elements
from review_v2.obligation_detail_elements import confidentiality_detail_elements


@pytest.mark.parametrize('separator', ['。', '；', '\n'])
@pytest.mark.parametrize('claim', ['如第三方主张乙方使用许可技术侵犯其专利权', '若第三方声称乙方使用技术侵犯专利权'])
def test_claim_cannot_complete_a_patent_grant(separator, claim):
    text = '技术秘密许可合同\n甲方授予乙方非独占使用许可。\n乙方许可费用已付，甲方应退还许可费' + separator + claim + '，甲方应协助。'
    assert classify_technology_transaction(text)['tertiary_subtype'] == 'TECHNICAL_SECRET_LICENSE'


@pytest.mark.parametrize('unrelated', [
    '如双方希望使用对方后续改进成果，应另行协商许可费用。',
    '改进成果许可费人民币30万元。',
    '甲方应退还许可费人民币30万元。',
    '双方未明确约定固定许可费人民币30万元。',
])
def test_main_fee_does_not_consume_another_relationship(unrelated):
    clauses = parse_contract_clauses('第一条 许可费用\n乙方支付固定许可费人民币80万元。\n第二条 后续安排\n' + unrelated)
    atom = elements('main_license_fee', clauses)[0]
    assert atom['status'] == 'COVERED'
    assert [r['quote'] for r in atom['supporting_evidence']] == ['乙方支付固定许可费人民币80万元。']
    assert elements('main_license_fee', parse_contract_clauses(unrelated))[0]['status'] == 'MISSING'


@pytest.mark.parametrize('amount', ['1,800,000元', '180万元', '１，８００，０００元'])
@pytest.mark.parametrize('separator', ['\n', ' '])
def test_main_fee_field_value_preserves_amount_and_source(amount, separator):
    text = '第十一条 使用费\n技术秘密使用费总额：' + separator + '人民币' + amount + '。'
    atom = elements('main_license_fee', parse_contract_clauses(text))[0]
    assert atom['status'] == 'COVERED'
    assert all(row['quote'] in text for row in atom['supporting_evidence'])


@pytest.mark.parametrize('continuation', ['此后并非因接收方违约而进入公共领域的信息；', '其后合法公开的信息；'])
def test_exception_list_keeps_independent_development(continuation):
    text = '第八条 保密\n下列信息不属于保密信息：\n接收方取得时已经合法公开的信息；\n' + continuation + '\n接收方未使用披露方保密信息而独立开发取得的信息。'
    from review_v2.engine import extract_semantic_field_value
    rows = confidentiality_detail_elements(parse_contract_clauses(text), extract_field=extract_semantic_field_value)
    exception = next(r for r in rows if r['element_id'] == 'confidentiality_exceptions')
    component = next(r for r in exception['component_coverage'] if r['element_id'] == 'confidentiality_exception_independent_development')
    assert component['status'] == 'COVERED'
    assert all(r['quote'] in text for r in component['supporting_evidence'])


@pytest.mark.parametrize('payment', ['仍应', '仍须', '仍需', '继续'])
@pytest.mark.parametrize('exit_right', ['', '如核心技术全部丧失秘密性，乙方有权解除合同。'])
def test_complete_exit_terms_do_not_swallow_adverse_fee(payment, exit_right):
    text = exit_right + f'即使核心技术在许可期限内全部丧失秘密性，乙方{payment}按照原付款计划支付全部尚未到期的固定许可费，甲方无须退还已经收取的任何许可费。'
    loss = analyze_technical_secret_loss_arrangement(text)
    assert loss['adverse']
    assert loss['unconditional_future_payment']


@pytest.mark.parametrize('fee, expected', [
    ('固定许可费', '尚未到期的固定许可费'),
    ('技术服务费', '尚未到期的技术服务费'),
    ('提成费', '尚未发生的提成费'),
])
def test_adverse_description_uses_only_the_asserted_payment_object(fee, expected):
    from review_v2.engine import _secret_loss_fee_subject
    text = f'如核心技术全部丧失秘密性，乙方仍应支付全部尚未到期的{fee}。甲方提供培训和技术指导。'
    loss = analyze_technical_secret_loss_arrangement(text)
    assert _secret_loss_fee_subject(text, loss=loss) == expected


@pytest.mark.parametrize('ordinary', [
    '甲方违反实施范围或者擅自转让技术秘密的，支付转让费50%的违约金。',
    '乙方违反交付技术秘密的义务，应赔偿甲方损失。',
    '乙方违反技术秘密使用范围，应停止超范围实施并赔偿损失。',
])
def test_technology_object_does_not_change_the_breached_obligation(ordinary):
    from review_v2.confidentiality_remedies import canonical_confidentiality_remedies
    rows = canonical_confidentiality_remedies(parse_contract_clauses('第一条 违约责任\n甲方违反保密义务，应赔偿乙方损失。\n' + ordinary))
    assert any(row['supporting_evidence'] for row in rows)
    assert all(ordinary not in proof['quote'] for row in rows for proof in row['supporting_evidence'])


@pytest.mark.parametrize('party', ['甲方/许可方', '乙方/被许可方'])
def test_scoped_secret_contract_end_to_end(party):
    from review_v2.engine import review_contract_v2
    from review_v2.user_profile import UserRiskProfile
    text = Path(__file__).with_name('fixtures').joinpath('technical_secret_scoped_license.txt').read_text(encoding='utf-8')
    # Alternate classification requests in the same process before review.
    patent = '专利实施许可合同\n许可方授予被许可方专利实施许可，许可使用费人民币50万元。'
    assert classify_technology_transaction(patent)['tertiary_subtype'] == 'PATENT_LICENSE'
    report = review_contract_v2(text, 'technology', use_llm=False, profile=UserRiskProfile(user_identity=party))
    assert classify_technology_transaction(text)['tertiary_subtype'] == 'TECHNICAL_SECRET_LICENSE'
    assert report['release_quality_gate']['status'] == 'REPORT_READY'
    items = {r['item_id']: r for r in report['items']}
    def atoms(key):
        return {r['element_id']: r for r in items[key]['coverage_elements']}
    scope = atoms('TC-07-01')
    for key in ['licensed_secret_subject', 'permitted_implementation_acts', 'license_territory', 'license_term', 'license_type']:
        assert scope[key]['status'] == 'COVERED'
    assert not any('patent' in key for key in scope)
    assert atoms('TC-07-02')['main_license_fee_arrangement']['status'] == 'COVERED'
    assert all('改进' not in (r.get('quote') or r.get('text') or '') for r in items['TC-07-02']['evidence_clauses'])
    assert any('80万元' in (r.get('quote') or r.get('text') or '') for r in items['TC-07-02']['evidence_clauses'])
    assert atoms('TC-11-02')['confidentiality_exceptions']['status'] == 'COVERED'
    for key in ['stop_disclosure', 'stop_use', 'mitigation_obligation', 'incident_notification']:
        assert atoms('TC-11-04')[key]['status'] == 'COVERED'
    assert atoms('TC-12-03')['future_fee_after_secret_loss']['status'] == 'ADVERSE'
    assert atoms('TC-12-03')['termination_after_secret_loss']['status'] == 'COVERED'
    assert atoms('TC-12-03')['secret_loss_trigger']['status'] == 'COVERED'
    assert atoms('TC-12-03')['technical_secret_consideration']['status'] == 'COVERED'
    assert '尚未到期的固定许可费' in items['TC-12-03']['risk_point_description']
    assert '未履行服务对应价款' not in items['TC-12-03']['risk_point_description']
    assert '提成费' not in items['TC-12-03']['risk_point_description']
