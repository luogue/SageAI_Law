from pathlib import Path

import pytest

from review_v2.clause_parser import parse_contract_clauses
from review_v2.consulting_element_facts import elements


def rows(family, text):
    return {e['element_id']: e for e in elements(family, parse_contract_clauses(text))}


@pytest.mark.parametrize('breaks', ['\n', '\n\n', ''])
def test_fee_label_and_nodes_keep_remuneration_scope(breaks):
    text = '技术咨询合同\n第一条 咨询费用\n合同总价：' + breaks + '人民币930000元。\n合同生效后6个工作日内支付30%，即279000元。'
    atoms = rows('consulting_payment', text)
    for key in ('consulting_fee_total', 'payment_milestones'):
        assert atoms[key]['status'] == 'COVERED'
        assert '咨询费用' in atoms[key]['supporting_evidence'][0]['quote']


def test_penalty_base_cannot_prove_primary_consulting_fee():
    atoms = rows('consulting_payment', '技术咨询合同\n第一条 违约责任\n按合同总价人民币500000元的0.01%支付违约金。')
    assert atoms['consulting_fee_total']['status'] == 'MISSING'


@pytest.mark.parametrize('verb', ['应', '须'])
def test_deliverables_list_and_non_numeric_quality(verb):
    text = f'技术咨询合同\n第一条 咨询成果\n乙方{verb}向甲方交付：\n《风险报告》；\n《技术方案》。\n第二条 质量标准\n最终报告{verb}：\n明确分析依据；\n说明技术风险。'
    atoms = rows('consulting_quality', text)
    assert atoms['report_contents']['status'] == 'COVERED'
    assert atoms['acceptance_standard']['status'] == 'COVERED'


def test_missing_deliverables_list_never_covered():
    atoms = rows('consulting_quality', '技术咨询合同\n第一条 咨询成果\n双方未约定：\n乙方应提交报告；\n乙方应交付方案。')
    assert atoms['report_contents']['status'] == 'MISSING'


@pytest.mark.parametrize('party', ['甲方', '委托方', '委托人'])
def test_normal_risk_and_professional_fault_exception(party):
    text = f'技术咨询合同\n第一条 正常决策风险\n{party}应自行承担正常商业决策风险。\n第二条 错误咨询责任\n如果乙方存在以下情况：\n伪造数据；\n计算存在重大基础错误；\n并因此造成损失：\n乙方应承担赔偿责任。'
    atoms = rows('consulting_decision', text)
    assert all(atoms[k]['status'] == 'COVERED' for k in ('qualified_consulting_decision_risk', 'consultant_fault_exception'))


def test_multiline_project_and_consulting_object():
    text = '技术咨询合同\n第一条 项目名称\n甲方委托乙方就：\n“仓储自动化改造项目”\n提供专项技术咨询。\n第二条 咨询范围\n乙方咨询范围包括：\n评估设备利用率；\n分析数据接口。'
    atoms = rows('consulting_subject', text)
    assert atoms['consulting_project']['status'] == 'COVERED'
    assert atoms['technical_question_or_object']['status'] == 'COVERED'


@pytest.mark.parametrize('header', ['下列信息除外：', '以下信息除外：', '下列信息不属于保密范围：'])
def test_confidentiality_exception_list_does_not_end_after_public_item(header):
    from review_v2.technology_service_elements import elements as service_elements
    text = ('技术咨询合同\n第一条 保密\n双方应对生产数据承担保密义务。\n' + header +
            '\n已公开信息；\n从有权第三方合法取得的信息；\n独立开发的信息；\n依法必须披露的信息。\n保密义务在合同终止后继续有效3年。')
    atoms = {e['element_id']:e for e in service_elements('confidentiality_disclosure',parse_contract_clauses(text))}
    assert all(atoms[k]['status'] == 'COVERED' for k in ('public_information_exception', 'lawful_third_party_source_exception', 'independent_development_exception', 'compelled_disclosure_exception', 'confidentiality_period'))


def test_inbound_consulting_claim_keeps_notice_assistance_and_conditional_liability():
    from review_v2.technology_service_analysis import extract_claim_response_facts
    text = ('技术咨询合同\n第一条 第三方知识产权主张\n如第三方主张乙方咨询报告侵犯知识产权：\n'
            '乙方应及时通知甲方并配合处理。\n因乙方未经授权使用第三方材料导致的责任：\n由乙方承担。\n'
            '合同未明确：\n诉讼控制权；\n律师选择；\n和解权限。')
    facts = extract_claim_response_facts(parse_contract_clauses(text),'乙方','甲方')
    assert facts['claim_trigger'] and facts['notification_requirement'] and facts['claim_assistance']
    assert facts['liability_responsible_party'][0]['actor'] == 'LICENSOR'
    assert '未经授权' in facts['liability_responsible_party'][0]['quote']
    assert not any(facts.get(k) for k in ('defense_control','lawyer_selection','settlement_authority'))


def test_construction_exclusions_are_arrangements_not_missing():
    atoms = rows('consulting_boundary','技术咨询合同\n第一条 范围边界\n乙方不直接承包生产线建设，不负责设备采购，也不直接开发完整生产管理软件。')
    assert all(e['status'] == 'COVERED' for e in atoms.values())


@pytest.mark.parametrize('predicate',['不负责','不包括','不包含'])
def test_shared_exclusion_predicate_applies_to_each_parallel_object(predicate):
    atoms = rows('consulting_boundary', f'技术咨询合同\n第一条 范围边界\n乙方{predicate}项目施工、设备采购、安装调试、软件开发或者实际运行维护。')
    assert all(e['status'] == 'COVERED' for e in atoms.values())


@pytest.mark.parametrize('joiner',['，但','但','；'])
def test_exclusion_scope_ends_before_a_new_positive_obligation(joiner):
    atoms = rows('consulting_boundary', f'技术咨询合同\n第一条 范围边界\n乙方不负责设备采购{joiner}负责软件开发。')
    assert atoms['excluded_software_implementation']['status'] == 'MISSING'


@pytest.mark.parametrize('provider,recipient',[('甲方','乙方'),('乙方','甲方')])
@pytest.mark.parametrize('declaration',['{provider}（咨询方）：某公司','{provider}为技术服务提供方。','咨询方：{provider}'])
def test_party_declaration_is_not_overridden_by_plan_or_method(provider, recipient, declaration):
    from review_v2.technology_service_analysis import analyze_technical_service_core_facts
    text=declaration.format(provider=provider)+f'\n{recipient}实施咨询方案。\n{recipient}使用服务方法。'
    facts=analyze_technical_service_core_facts(text)['liability']
    assert facts['service_provider_party']==provider
    assert facts['service_recipient_party']==recipient


@pytest.mark.parametrize('provider,recipient',[('甲方','乙方'),('乙方','甲方')])
def test_notice_sender_does_not_inherit_recipient_assistance(provider, recipient):
    from review_v2.technology_service_analysis import extract_claim_response_facts
    text=f'技术咨询合同\n第一条 第三方索赔\n如第三方提出索赔，{provider}应通知{recipient}，{recipient}配合处理。'
    facts=extract_claim_response_facts(parse_contract_clauses(text),provider,recipient)
    assert not facts.get('claim_assistance')


def test_current_final_consumers_and_gate():
    from review_v2.engine import review_contract_v2
    from review_v2.user_profile import UserRiskProfile
    text = (Path(__file__).parent/'fixtures/round36_consulting.txt').read_text(encoding='utf8')
    report = review_contract_v2(text,'technology',use_llm=False,profile=UserRiskProfile(user_identity='甲方'))
    assert report['release_quality_gate']['status'] == 'REPORT_READY', report['release_quality_gate']['failures']
    items = {i['item_id']:i for i in report['items']}
    for key in ('TC-01-03','TC-01-04','TC-08-01','TC-08-02','TC-08-05'):
        assert items[key]['coverage_status'] == '通过'
    assert items['TC-12-02']['coverage_status'] == '部分覆盖'
    assert items['TC-12-02']['applicability']['triggered'] is True
    claims={e['element_id']:e for e in items['TC-12-02']['coverage_elements']}
    assert claims['necessary_assistance']['status']=='COVERED'
    assert all(s['actor']=='LICENSOR' for s in claims['provider_infringement_liability']['supporting_evidence'])
    assert items['TC-08-03']['coverage_elements'][0]['status'] == 'COVERED'
