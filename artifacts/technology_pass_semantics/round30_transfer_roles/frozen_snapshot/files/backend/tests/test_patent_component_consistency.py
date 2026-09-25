"""Patent licence predicates and their final consumers share source truth."""
from pathlib import Path
import pytest
from review_v2.clause_parser import parse_contract_clauses
from review_v2.technology_service_analysis import analyze_payment_schedule, extract_claim_response_facts
from review_v2.technology_fact_ontology import license_scope_elements, patent_support_sources, patent_support_details, operative_secret_context
from review_v2.license_control_facts import elements


@pytest.mark.parametrize('trigger', ['本合同生效', '合同签署', '合同签订', '协议生效', '双方盖章', '双方签字'])
def test_first_equal_payment_is_not_lost_or_deduplicated(trigger):
    text = f'合同总价为人民币120万元。\n{trigger}后十日内支付40万元；\n完成首轮技术说明后支付40万元；\n设备完成生产后支付40万元。'
    fact = analyze_payment_schedule(text)
    assert len(fact['nodes']) == 3
    assert fact['amount_total'] == fact['contract_total'] == 1200000
    assert fact['percentage_total'] == 100
    assert fact['amount_delta'] == 0
    assert all(g['status'] == 'CONSISTENT' for g in fact['payment_groups'])


@pytest.mark.parametrize('amount', ['30', '50'])
def test_real_payment_discrepancy_remains(amount):
    fact = analyze_payment_schedule(f'合同总价为人民币120万元。\n合同生效后支付{amount}万元；\n完成技术说明后支付40万元；\n设备完成生产后支付40万元。')
    assert fact['amount_delta'] != 0
    assert any(g['status'] == 'INCONSISTENT' for g in fact['payment_groups'])


@pytest.mark.parametrize('link', ['为', '：', '限于', '包括'])
def test_territory_declarative_aliases(link):
    text = f'许可地域{link}中华人民共和国大陆地区。'
    row = next(e for e in license_scope_elements(parse_contract_clauses(text)) if e['element_id']=='license_territory')
    assert row['status'] == 'COVERED'
    assert row['supporting_evidence'][0]['quote'] == text


@pytest.mark.parametrize('separator', ['\n', '\n\n', '\n\n\n'])
def test_implementation_list_inherits_only_positive_grant(separator):
    text = '乙方（被许可方）：乙公司\n第三条 实施范围\n乙方可以实施下列行为：' + separator + ('；'+separator).join(['制造装配设备','使用上述设备','销售、许诺销售上述设备','为售后维修目的更换零部件']) + '。'
    row = next(e for e in license_scope_elements(parse_contract_clauses(text)) if e['element_id']=='permitted_implementation_acts')
    assert row['status'] == 'COVERED'
    assert all(s['quote'] in text and '可以实施' in s['quote'] for s in row['supporting_evidence'])
    assert any('维修' in s['quote'] for s in row['supporting_evidence'])


@pytest.mark.parametrize('text', ['双方未约定许可地域为中国大陆。', '许可地域是否为中国大陆，双方未明确。'])
def test_absent_territory_is_not_a_declaration(text):
    assert next(e for e in license_scope_elements(parse_contract_clauses(text)) if e['element_id']=='license_territory')['status']=='MISSING'


@pytest.mark.parametrize('text', [
    '因乙方故意超范围实施给甲方造成可证明实际损失的，乙方依法承担赔偿责任。',
    '乙方超范围实施造成甲方损失的，乙方负责赔偿。',
    '乙方超范围实施，应赔偿甲方实际损失。',
])
def test_compensation_action_and_loss_order(text):
    row=next(e for e in elements('license_scope_remedies',parse_contract_clauses(text)) if e['element_id']=='damage_compensation')
    assert row['status']=='COVERED'
    assert row['supporting_evidence'][0]['quote']==text


@pytest.mark.parametrize('service', ['实施指导','实施协助','技术指导','技术支持','技术服务'])
def test_limited_support_is_an_existing_obligation(service):
    text=f'自资料交付日起六个月内，甲方提供累计不超过30小时的远程{service}。'
    assert patent_support_sources(text)['technology.license.licensor_support']==[text]


@pytest.mark.parametrize('event', ['放弃专利权','专利被无效','专利被撤销','专利权终止','专利法律状态变化'])
def test_notice_and_missing_deadline_are_independent(event):
    text=f'如发生{event}，甲方应及时通知乙方。\n双方未约定具体通知期限。'
    assert len(patent_support_sources(text)['technology.patent.status_change_notice'])==1
    assert patent_support_details(parse_contract_clauses(text))[1]['status']=='MISSING'


@pytest.mark.parametrize('text', ['甲方无需提供实施指导。','双方未约定甲方提供实施协助。','如专利被无效，甲方无需通知乙方。'])
def test_negative_support_is_not_a_positive_fact(text):
    sources=patent_support_sources(text)
    assert not sources['technology.license.licensor_support']
    assert not sources['technology.patent.status_change_notice']


@pytest.mark.parametrize('verb', ['取得','获取','获得'])
def test_lawful_third_party_acquisition_component(verb):
    from review_v2.obligation_detail_elements import confidentiality_detail_elements
    from review_v2.engine import extract_semantic_field_value
    text=f'下列信息不属于保密信息：\n已经公开的信息；\n接收方从合法第三方{verb}的信息；\n独立开发的信息。'
    rows=confidentiality_detail_elements(parse_contract_clauses(text),extract_field=extract_semantic_field_value)
    row=next(e for e in rows if e['element_id']=='confidentiality_exceptions')
    child=next(e for e in row['component_coverage'] if e['element_id']=='confidentiality_exception_lawful_acquisition')
    assert child['status']=='COVERED'
    assert row['status']=='PARTIALLY_COVERED'


@pytest.mark.parametrize('harm', ['承认侵权','停止全部生产','向第三方承担额外付款义务'])
def test_concrete_settlement_protection_not_an_adverse_allocation(harm):
    text=f'第十条 第三方权利主张\n如第三方主张乙方侵权，甲方应负责交涉。\n未经乙方书面同意，甲方不得以要求乙方{harm}为条件达成和解。'
    facts=extract_claim_response_facts(parse_contract_clauses(text),'甲方','乙方')
    assert facts.get('settlement_non_prejudice')
    assert not any(s.get('actor')=='LICENSEE' for s in facts.get('liability_responsible_party',[]))


def test_liability_in_compensation_premise_does_not_reassign_the_duty():
    text='第一条 第三方权利主张\n如第三方主张乙方侵权，甲方负责交涉。\n因甲方无权许可，导致乙方承担赔偿责任的，由甲方承担乙方因此产生的合理直接损失。'
    facts=extract_claim_response_facts(parse_contract_clauses(text),'甲方','乙方')
    assert not any(s.get('actor')=='LICENSEE' for s in facts.get('liability_responsible_party',[]))
    assert facts.get('damages_allocation')


@pytest.mark.parametrize('text', ['资料交付不代表甲方向乙方许可任何未公开技术秘密。','乙方未使用甲方额外未公开技术资料形成的独立改进成果归乙方。'])
def test_excluded_secret_is_not_a_licensed_secret_premise(text):
    assert not operative_secret_context(text)


@pytest.mark.parametrize('text', [
    '双方未约定乙方超范围实施造成损失时承担赔偿责任。',
    '乙方超范围实施造成甲方损失的，乙方不承担赔偿责任。',
    '乙方超范围实施造成甲方损失的，乙方无需承担赔偿责任。',
])
def test_compensation_absence_and_negation_remain_distinct(text):
    row=next(e for e in elements('license_scope_remedies',parse_contract_clauses(text)) if e['element_id']=='damage_compensation')
    assert row['status']=='MISSING'


def test_execution_content_does_not_disappear_with_missing_response_deadline():
    text='第八条 实施指导\n甲方提供六个月远程实施指导。\n指导内容限于设备适配及安装问题。'
    row,_=patent_support_details(parse_contract_clauses(text))
    assert row['status']=='PARTIALLY_COVERED'
    assert row['component_coverage'][0]['status']=='COVERED'
    assert '具体内容范围' not in row['residual_gap']


@pytest.mark.parametrize('source_type,expected',[('BODY',False),('ATTACHMENT',True),('APPENDIX',True)])
def test_proof_requirement_uses_document_provenance(source_type,expected):
    from review_v2.engine import _source_meets_requirements, _PATENT_PROOF_SOURCE_REQUIREMENTS
    assert _source_meets_requirements(dict(source_type=source_type,text='专利权人甲公司；授权日2025年；法律状态有效；年费已缴。'),_PATENT_PROOF_SOURCE_REQUIREMENTS) is expected


@pytest.mark.parametrize('party',['甲方/许可方','乙方/被许可方'])
def test_final_patent_report_consistency(party):
    from review_v2.engine import review_contract_v2
    from review_v2.user_profile import UserRiskProfile
    text=Path(__file__).with_name('fixtures').joinpath('patent_license_component_consistency.txt').read_text(encoding='utf-8')
    report=review_contract_v2(text,'technology',use_llm=False,profile=UserRiskProfile(user_identity=party))
    assert report['release_quality_gate']['status']=='REPORT_READY'
    assert not report['release_quality_gate']['failures']
    items={i['item_id']:i for i in report['items']}
    assert 'GEN-PAY-01' not in items
    expected={'TC-07-01':['permitted_implementation_acts','license_territory'],
              'TC-07-03':['damage_compensation'],
              'TC-07-04':['on_demand_technical_service','patent_status_change_notice'],
              'TC-11-02':['confidentiality_exceptions'], 'TC-12-02':['settlement_non_prejudice']}
    for key, ids in expected.items():
        atoms={e['element_id']:e for e in items[key]['coverage_elements']}
        for eid in ids:
            assert atoms[eid]['status']=='COVERED'
            assert atoms[eid]['evidence_ids']

    for item in items.values():
        registry=item['decision_trace'].get('contract_fact_registry_consumption',{}).get('facts',{})
        for atom in item['coverage_elements']:
            if atom['status']=='COVERED':
                assert registry.get(atom.get('source_fact_key'),{}).get('status')!='MISSING'
    for key in ('TC-07-01','TC-07-04','TC-12-01','TC-12-02'):
        facts=items[key]['decision_trace']['contract_fact_registry_consumption']['facts']
        for atom in items[key]['coverage_elements']:
            canonical=facts[atom['source_fact_key']]
            assert canonical['status']==('MISSING' if atom['status']=='MISSING' else 'FOUND')

    for key in ('TC-07-01','TC-11-02'):
        item=items[key]
        narrative=item['narrative_state']
        assert item['risk_point_description']==(narrative['issue'] or narrative['judgment'])
        assert '尚未覆盖' not in item['risk_point_description']
        assert item['applicability']['status']=='APPLICABLE'


@pytest.mark.parametrize('breaks',['\n','\n\n'])
def test_support_list_preserves_operative_introduction(breaks):
    sources=patent_support_sources('出让方应提供：'+breaks+'远程技术支持、系统部署指导、技术培训。')
    assert sources['technology.license.licensor_support']


def test_settlement_prohibition_keeps_preceding_actual_allocation():
    text='第十条 第三方权利主张\n如第三方主张乙方侵权，甲方负责交涉。甲方承担赔偿责任，未经乙方书面同意，甲方不得以要求乙方承担额外付款义务为条件达成和解。'
    facts=extract_claim_response_facts(parse_contract_clauses(text),'甲方','乙方')
    assert any(s.get('actor')=='LICENSOR' for s in facts.get('liability_responsible_party',[]))
    assert not any(s.get('actor')=='LICENSEE' for s in facts.get('liability_responsible_party',[]))


@pytest.mark.parametrize('prefix',['双方未明确约定出让方应提供：','出让方无需提供：'])
def test_absent_or_negated_support_list_never_becomes_affirmative(prefix):
    assert not patent_support_sources(prefix+'\n远程技术支持、实施指导。')['technology.license.licensor_support']
