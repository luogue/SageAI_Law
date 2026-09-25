"""Role-owned transfer facts and projections; no case-specific provider assumptions."""
from pathlib import Path
import pytest
from review_v2.clause_parser import parse_contract_clauses
from review_v2.secret_transfer_elements import elements
from review_v2.technology_adverse_evidence import independent_research_restriction_sources, has_competition_restriction
from review_v2.penalty_base import total_price_definitions, analyze
from review_v2.technology_service_analysis import analyze_technology_subtransactions

TEXT=Path(__file__).with_name('fixtures').joinpath('secret_transfer_roles_projection.txt').read_text(encoding='utf8')

def atoms(family,text,provider='乙方',recipient='甲方'):
    header=f'技术秘密转让合同\n{provider}（转让方）：某公司\n{recipient}（受让方）：另一公司\n'
    return {e['element_id']:e for e in elements(family,parse_contract_clauses(header+text))}

@pytest.mark.parametrize('provider,recipient',[('甲方','乙方'),('乙方','甲方')])
@pytest.mark.parametrize('verb',['取得','有权'])
def test_recipient_grant_keeps_party_direction(provider,recipient,verb):
    phrase=f'{recipient}{verb}使用本合同技术秘密。' if verb=='有权' else f'{recipient}取得本合同技术秘密的使用、改进及商业实施权。'
    e=atoms('secret_transfer_scope',phrase,provider,recipient)
    assert e['transferee_use_right']['status']=='COVERED'
    other=atoms('secret_transfer_scope',phrase.replace(recipient,provider),provider,recipient)
    assert other['transferee_use_right']['status']=='MISSING'

@pytest.mark.parametrize('intro',['技术秘密具体包括：','技术秘密包括：','技术秘密范围：'])
def test_identity_shared_across_subject_and_scope(intro):
    text='技术秘密名称为“工业控制配置技术”。\n'+intro+'\n非公开算法参数；\n部署配置文件；\n工艺流程。'
    a=atoms('secret_transfer_subject',text)['transferred_subject']
    b=atoms('secret_transfer_scope',text)['transferred_subject']
    assert a['status']==b['status']=='COVERED'
    assert a['source_fact_key']==b['source_fact_key']

@pytest.mark.parametrize('text',['甲方使用技术后支付转让价款。','甲方生产设备后支付费用。','双方未约定甲方取得技术秘密的使用、改进及商业实施权。'])
def test_timing_and_absence_are_not_grants(text):
    e=atoms('secret_transfer_scope',text)
    assert all(e[k]['status']=='MISSING' for k in ['transferee_use_right','transferee_improvement_right','production_commercialization_right'])

@pytest.mark.parametrize('provider,recipient',[('甲方','乙方'),('乙方','甲方')])
@pytest.mark.parametrize('asset',['已经删除、返还的转让技术','已转让的技术秘密'])
def test_transferor_asset_use_limit_is_not_recipient_research_ban(provider,recipient,asset):
    text=f'技术秘密转让合同\n{provider}（转让方）：某公司\n{recipient}（受让方）：另一公司\n{provider}不得基于{asset}继续开发实质相同的商业版本。\n{provider}独立研发的新成果归其所有。'
    assert not list(independent_research_restriction_sources(text))
    assert not has_competition_restriction(text)

@pytest.mark.parametrize('actor',['甲方','乙方','受让方','转让方'])
def test_actual_independent_research_prohibition_keeps_source_actor(actor):
    source=f'{actor}不得独立研发竞争性技术。'
    evidence=list(independent_research_restriction_sources(source))
    assert evidence and all(actor in s for s in evidence)
    assert has_competition_restriction(source)

@pytest.mark.parametrize('absence',['未约定','没有约定','未明确'])
def test_missing_disposal_does_not_cover(absence):
    e=atoms('secret_material_disposal',f'双方{absence}：乙方应删除完整副本；销毁纸质文件。')
    assert e['confidential_material_return_destroy']['status']=='MISSING'

@pytest.mark.parametrize('action',['删除服务器中的完整副本','销毁非依法必须保存的纸质文件','删除可复制技术资料'])
def test_disposal_lists_inherit_operative_obligation(action):
    e=atoms('secret_material_disposal',f'乙方应在交付完成后20日内：\n{action}；\n出具书面确认。')
    assert e['confidential_material_return_destroy']['status']=='COVERED'

@pytest.mark.parametrize('label',['技术秘密转让总价款','技术转让总价款','交易总价款'])
@pytest.mark.parametrize('amount',['180000元','18万元'])
def test_agreed_total_alias_and_newline_are_determinable(label,amount):
    assert total_price_definitions('合同总价',f'{label}为：\n人民币{amount}。')

def test_conflicting_totals_remain_unresolved():
    assert not total_price_definitions('合同总价','交易总价款为18万元。合同总价为20万元。')

@pytest.mark.parametrize('base',['对应逾期未付款金额','逾期未付款金额','逾期未付金额'])
def test_overdue_ledger_base_is_deterministically_derived(base):
    rows=analyze(f'受让方逾期付款的，每日按{base}的0.05%支付违约金。')
    assert rows and all(r['status']=='DETERMINABLE' for r in rows)

def test_bundled_services_are_active_without_separate_fee():
    facts=analyze_technology_subtransactions('第一条 技术服务\n乙方应提供两次现场部署支持、三次线上培训、20个工作日远程技术答疑。上述服务费用包含在转让价款内。')
    assert facts['structured_facts']['technical_service']['content']

@pytest.fixture(scope='module')
def report():
    from review_v2.engine import review_contract_v2
    from review_v2.user_profile import UserRiskProfile
    return review_contract_v2(TEXT,'technology',use_llm=False,profile=UserRiskProfile(user_identity='甲方/受让方'))

@pytest.mark.parametrize('rule,state',[('TC-01-03','通过'),('TC-06-01','通过'),('TC-06-03','部分覆盖'),('TC-02-01','通过'),('TC-11-03','通过'),('TC-12-01','通过'),('TC-12-03','部分覆盖'),('COMMON-20-01','通过'),('TC-10-01','通过'),('TC-10-02','通过'),('TC-10-03','不适用'),('TC-10-04','通过')])
def test_current_final_rule_projection(report,rule,state):
    item=next(i for i in report['items'] if i['item_id']==rule)
    assert item['coverage_status']==state
    if rule=='TC-02-01':
        assert '合同专利' not in item['risk_point_description']
        assert '受让方被禁止' not in item['risk_point_description']

def test_receipt_and_residual_identifier_are_separate(report):
    item=next(i for i in report['items'] if i['item_id']=='TC-13-01')
    e={e['element_id']:e for e in item['coverage_elements']}
    assert e['receipt_confirmation']['status']=='COVERED'
    assert e['file_identifier']['status']=='MISSING'

@pytest.mark.parametrize('rule',['TC-09-01','TC-09-02','TC-09-04'])
def test_ancillary_service_activates_applicable_reviews(report,rule):
    assert next(i for i in report['items'] if i['item_id']==rule)['coverage_status']!='不适用'

def test_service_without_independent_results_does_not_activate_result_ownership(report):
    assert next(i for i in report['items'] if i['item_id']=='TC-09-03')['coverage_status']=='不适用'

def test_partial_object_specific_retention_is_not_erased_by_coarse_disposal():
    from review_v2.engine import review_contract_v2
    from review_v2.user_profile import UserRiskProfile
    text=Path(__file__).with_name('fixtures').joinpath('secret_transfer_final_fact_binding.txt').read_text(encoding='utf8')
    r=review_contract_v2(text,'technology',use_llm=False,profile=UserRiskProfile(user_identity='乙方/受让方'))
    item=next(i for i in r['items'] if i['item_id']=='TC-11-03')
    assert item['coverage_status']=='部分覆盖'
    assert any(e['status']=='MISSING' and '数据' in str(e.get('required_fact') or e.get('proposition')) for e in item['coverage_elements'])

def test_ancillary_content_and_bundled_payment_have_direct_evidence(report):
    items={i['item_id']:i for i in report['items']}
    for rule,keys in [('TC-09-01',['service_scope','service_content']),('TC-09-04',['service_fee_amount','service_payment_schedule'])]:
        item=items[rule];atoms={e['element_id']:e for e in item['coverage_elements']}
        for key in keys:
            e=atoms[key]
            assert e['status']=='COVERED' and e['source_fact_key']
            assert e['supporting_evidence']
            assert any(key in s.get('supports_element_ids',[]) and s.get('verified_original') and s.get('support_type')=='DIRECT' for s in item['evidence_clauses'])
    assert '未找到支持任何必要要素' not in items['TC-09-01']['risk_point_description']

@pytest.mark.parametrize('text',[
    '乙方不得从其他渠道获得类似技术。',
    '乙方不得绕开合同专利开发替代方案。',
    '竞争技术的研发限制在合同终止后继续有效5年。',
    '被许可方必须将独立形成的改进成果及知识产权无偿转让给许可方。',
])
def test_negative_competition_search_preserves_other_existing_adverse_families(text):
    assert has_competition_restriction(text)

@pytest.mark.parametrize('text',[
    '双方不得限制受让方从第三方获得其他技术。',
    '双方未约定乙方不得从第三方购买技术。',
])
def test_protective_and_missing_competition_clauses_are_not_adverse(text):
    assert not has_competition_restriction(text)

@pytest.mark.parametrize('text,expected',[
    ('甲方不得限制乙方独立研发其他技术。',False),
    ('许可方不得限制被许可方独立研发竞争性技术。',False),
    ('甲方不得独立研发其他技术。',True),
    ('双方未约定：\n乙方不得独立改进本技术；\n其改进成果必须无偿转让。',False),
    ('双方未明确是否禁止乙方独立改进技术。',False),
    ('甲方不得限制乙方独立改进技术，但乙方不得独立研发竞争性技术。',True),
    ('甲方不得转让原始技术秘密，但甲方独立改进成果不受限制。',False),
    ('甲方不得转让原始技术，但乙方必须无偿转让改进成果给许可方。',True),
])
def test_outer_operator_and_parallel_scope(text,expected):
    assert has_competition_restriction(text)==expected

@pytest.mark.parametrize('separator',['，',''])
def test_consent_condition_actor_does_not_swallow_operative_research_subject(separator):
    text=f'未经甲方书面同意{separator}乙方不得自行开发与本项目相同的软件产品。'
    assert list(independent_research_restriction_sources(text))
    assert has_competition_restriction(text)

@pytest.mark.parametrize('qualifier,owner',[
    ('','甲'),('基于本项目成果形成的改进。',None),('双方另行协商对价。',None),
])
def test_existing_universal_assignment_fact_keeps_its_scope_exceptions(qualifier,owner):
    from review_v2.technology_adverse_evidence import uncompensated_universal_assignment_owner
    text='后续改进成果无论由哪一方完成，知识产权均归甲方所有。'+qualifier
    assert uncompensated_universal_assignment_owner(text)==owner


@pytest.mark.parametrize("text,expected", [
    ("被许可方未经许可方书面同意，不得自行研发类似产品。", True),
    ("受让方未取得让与方事先批准，不得独立开发类似技术。", True),
    ("未经许可方书面同意，被许可方不得自行研发类似产品。", True),
    ("被许可方未经许可方书面同意，不得限制转让方独立研发类似技术。", False),
])
def test_consent_holder_does_not_replace_restricted_actor(text, expected):
    from review_v2.technology_adverse_evidence import independent_research_restriction_sources
    assert bool(list(independent_research_restriction_sources(text))) is expected
