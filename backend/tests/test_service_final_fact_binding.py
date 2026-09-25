"""Service facts must survive exact final projection without changing polarity."""
from pathlib import Path
from types import SimpleNamespace
import json
import pytest
from review_v2.clause_parser import parse_contract_clauses
from review_v2.technology_service_elements import elements
from review_v2.technology_transaction_evidence import extract_elements
from review_v2.proposition_scope import arrangement_matches
from review_v2.confidentiality_remedies import canonical_confidentiality_remedies
from review_v2.data_use_scope import data_use_permissions


HEADER = '技术服务合同\n甲方（委托方）：甲公司\n乙方（服务方）：乙公司\n'


def rows(family, text):
    return {e['element_id']: e for e in elements(family, parse_contract_clauses(HEADER + text))}


@pytest.mark.parametrize('absence', ['未约定', '未明确约定', '没有约定', '未作明确约定'])
@pytest.mark.parametrize('separator', ['、', '，', '及'])
def test_parallel_claim_controls_inherit_absence(absence, separator):
    statement = '双方' + absence + '第三方索赔发生后的具体' + separator.join(['抗辩控制权','律师选择权','和解审批机制']) + '。'
    proof = rows('service_claims', '第十四条 第三方权利主张\n' + statement)
    for key, pattern in [('defense_control','抗辩控制权'),('lawyer_selection','律师选择权'),('settlement_authority','和解审批机制')]:
        assert proof[key]['status'] == 'MISSING'
        assert not proof[key]['supporting_evidence']
        assert not list(arrangement_matches(pattern, statement))


@pytest.mark.parametrize('term', ['合同终止后', '合同解除后', '许可期限届满后'])
@pytest.mark.parametrize('verb', ['返还或者删除', '返还或删除'])
def test_disposition_partial_components_do_not_erase_positive_duties(term, verb):
    text = f'第十七条 资料返还和删除\n{term}，甲方有权要求乙方{verb}甲方提供的程序、数据及其他保密资料。\n乙方应在收到书面要求后十五个工作日内完成处理。\n因正常备份机制暂时无法删除的资料，应继续受保密义务约束，不得继续用于项目之外的目的。\n双方未约定备份数据最终删除的具体期限。'
    proof = rows('material_exit', text)
    for key in ('termination_return_or_delete','processing_deadline','retained_backup_use_restriction'):
        assert proof[key]['status'] == 'COVERED'
        assert proof[key]['supporting_evidence']
    for key in ('confidential_copy_deletion','confidential_backup_deletion','confidential_disposal_confirmation'):
        assert proof[key]['status'] == 'MISSING'
        assert not proof[key]['supporting_evidence']


@pytest.mark.parametrize('conduct', ['相关行为', '泄密行为', '违约行为'])
@pytest.mark.parametrize('separator', ['。', '；'])
def test_incident_action_is_separate_from_absent_notification_deadline(conduct, separator):
    text = f'任何一方违反保密义务的，应立即停止{conduct}，并采取合理措施防止损失扩大{separator}双方未约定保密资料发生泄露后的具体通知期限。'
    proof = {e['element_id']:e for e in canonical_confidentiality_remedies(parse_contract_clauses(text))}
    assert proof['stop_disclosure']['status'] == 'COVERED'
    assert proof['mitigation_obligation']['status'] == 'COVERED'
    assert proof['incident_notification']['status'] == 'MISSING'


@pytest.mark.parametrize('activity', ['进行运行状态检测', '分析设备停机异常原因', '对PLC控制参数提出优化建议', '进行现场参数调整', '进行远程培训'])
def test_core_service_activity_has_its_own_source(activity):
    text = HEADER + '第一条 服务内容\n乙方向甲方提供以下技术服务：\n' + activity + '。'
    proof = next(e for e in extract_elements('technical_service_subject', parse_contract_clauses(text)) if e['element_id']=='technical_service_activities')
    assert proof['status']=='COVERED'
    assert any(activity in s['quote'] for s in proof['supporting_evidence'])


@pytest.mark.parametrize('negative', ['未经甲方书面同意，乙方不得将甲方原始生产数据用于训练面向其他客户的商业模型。', '双方未约定乙方可以将甲方原始生产数据用于模型训练。', '乙方不能将甲方原始生产数据用于其他客户项目。'])
def test_raw_data_prohibition_does_not_become_external_permission(negative):
    text = negative + '\n乙方可以保留已经无法识别甲方及具体经营情况的匿名化统计数据，用于改进其通用诊断方法。'
    facts = data_use_permissions(parse_contract_clauses(text))
    assert len(facts)==1
    assert facts[0]['data_object']=='ANONYMOUS_STATISTICS'
    assert facts[0]['purpose']=='改进其通用诊断方法'
    assert not facts[0]['external_use']


@pytest.mark.parametrize('purpose', ['模型训练','其他客户项目','产品优化'])
def test_real_raw_data_permission_remains_identified(purpose):
    facts=data_use_permissions(parse_contract_clauses(f'乙方可以将甲方原始生产数据用于{purpose}。'))
    assert facts and facts[0]['data_object']=='COUNTERPARTY_DATA' and facts[0]['external_use']


@pytest.mark.parametrize('purpose', ['模型训练','其他客户项目','产品优化'])
def test_data_permission_narrative_keeps_only_the_granted_object_and_purpose(report, purpose):
    from copy import deepcopy
    from review_v2.engine import ReviewItemResult, _apply_service_confidentiality_party_semantics
    original = next(i for i in report['items'] if i['item_id']=='TC-11-02')
    item = ReviewItemResult(**{k:deepcopy(v) for k,v in original.items()
                              if k in ReviewItemResult.__dataclass_fields__})
    permission = f'乙方可以将甲方原始生产数据用于{purpose}。'
    text = HEADER + '第八条 保密义务\n双方应保守对方提供的生产数据。\n' + permission
    _apply_service_confidentiality_party_semantics([item], text)
    e = next(e for e in item.coverage_elements if e['element_id']=='party_b_external_data_use')
    assert e['status']=='ADVERSE'
    assert e['proposition']==permission.rstrip('。')
    assert e['supporting_evidence'] and e['evidence_ids']
    assert all(s['quote'].rstrip('。')==permission.rstrip('。') for s in e['supporting_evidence'])
    assert permission.rstrip('。') in item.risk_point_description
    assert all(p not in item.risk_point_description for p in ('模型训练','其他客户项目','产品优化') if p!=purpose)


@pytest.mark.parametrize('family,key,text', [
    ('service_claims','defense_control','如第三方索赔，乙方负责抗辩。'),
    ('service_claims','lawyer_selection','如第三方索赔，乙方负责选择律师。'),
    ('service_claims','settlement_authority','如第三方索赔，乙方拥有和解审批权。'),
])
def test_positive_claim_controls_are_not_lost(family,key,text):
    assert rows(family,text)[key]['status']=='COVERED'


@pytest.fixture(scope='module', params=['甲方/委托方', '乙方/服务方'])
def report(request):
    from review_v2.engine import review_contract_v2
    from review_v2.user_profile import UserRiskProfile
    text=Path(__file__).with_name('fixtures').joinpath('service_final_fact_binding.txt').read_text(encoding='utf-8')
    result=review_contract_v2(text,'technology',use_llm=False,profile=UserRiskProfile(user_identity=request.param))
    out=Path(__file__).resolve().parents[2]/'artifacts/technology_pass_semantics/round26_service_binding'
    out.mkdir(parents=True, exist_ok=True)
    (out/('local_client.json' if request.param.startswith('甲') else 'local_provider.json')).write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    return result


@pytest.mark.parametrize('rule,key', [('TC-09-01','core_contract_arrangement'),('TC-09-01','PRIMARY_EVIDENCE'),('TC-09-04','technical_service_remuneration'),('TC-09-04','PRIMARY_EVIDENCE')])
def test_four_actual_mismatches_have_direct_canonical_binding(report,rule,key):
    item=next(i for i in report['items'] if i['item_id']==rule)
    e=item['coverage_elements'][0] if key=='PRIMARY_EVIDENCE' else next(e for e in item['coverage_elements'] if e['element_id']==key)
    assert e['status']=='COVERED'
    assert e['source_fact_key']
    fact=item['decision_trace']['contract_fact_registry_consumption']['facts'][e['source_fact_key']]
    assert fact['status']=='FOUND'
    evidence=item['evidence_clauses'][0] if key=='PRIMARY_EVIDENCE' else next(s for s in item['evidence_clauses'] if s['evidence_id'] in e['evidence_ids'])
    assert evidence['support_type']=='DIRECT' and evidence['verified_original']
    assert e['element_id'] in evidence['supports_element_ids']


def test_final_service_report_semantics(report):
    assert report['report_context']['contract_type_label']=='技术合同—技术服务合同'
    assert report['release_quality_gate']['status']=='REPORT_READY', report['release_quality_gate']['failures']
    items={i['item_id']:i for i in report['items']}
    for rule in ('TC-11-03','TC-11-04','TC-09-02','TC-09-03'):
        assert items[rule]['coverage_status']=='部分覆盖'
    assert items['TC-11-02']['coverage_status']!='风险条款'
    exceptions = next(e for e in items['TC-11-02']['coverage_elements'] if e['element_id']=='confidentiality_exceptions')
    assert exceptions['status']=='COVERED'
    assert '用于模型、产品优化或其他客户项目' not in items['TC-11-02']['risk_point_description']
    controls={e['element_id']:e for e in items['TC-12-02']['coverage_elements']}
    assert all(controls[k]['status']=='MISSING' for k in ('defense_control','lawyer_selection','settlement_authority'))
    assert next(e for e in items['TC-01-03']['coverage_elements'] if e['element_id']=='technical_service_activities')['status']=='COVERED'


@pytest.mark.parametrize('corruption', ['absence_as_covered', 'covered_without_source',
    'positive_as_missing', 'stale_parent_narrative', 'missing_component_as_covered'])
def test_final_gate_rejects_corrupted_binding(report, corruption):
    from copy import deepcopy
    from review_v2.element_evidence_projection import audit
    items = {i['item_id']: SimpleNamespace(**deepcopy(i)) for i in report['items']}
    if corruption == 'absence_as_covered':
        item = items['TC-12-02']
        e = next(e for e in item.coverage_elements if e['element_id'] == 'defense_control')
        e.update(status='COVERED', supporting_evidence=[dict(clause_id='C0017',
            quote='双方未约定第三方索赔发生后的具体抗辩控制权、律师选择权及和解审批机制。',
            proposition_polarity='AFFIRMATIVE')])
    else:
        item = items['TC-11-03']
        e = next(e for e in item.coverage_elements if e['element_id'] == 'termination_return_or_delete')
        if corruption == 'covered_without_source':
            e['supporting_evidence'] = []
        elif corruption == 'positive_as_missing':
            e['status'] = 'MISSING'
        elif corruption == 'stale_parent_narrative':
            item.narrative_state['coverage_status'] = '未覆盖'
        else:
            e['component_coverage'] = [dict(element_id='copy_deletion', status='MISSING')]
    text = Path(__file__).with_name('fixtures').joinpath('service_final_fact_binding.txt').read_text(encoding='utf-8')
    failures = audit(list(items.values()), [], parse_contract_clauses(text))
    assert failures, corruption


@pytest.mark.parametrize('qualifier', ['未使用', '没有使用', '不曾使用'])
def test_exception_negates_use_not_independent_development(qualifier):
    from review_v2.obligation_detail_elements import confidentiality_detail_elements
    from review_v2.engine import extract_semantic_field_value
    text = ('第十二条 保密义务\n下列信息不属于保密信息：\n'
            '接收时已经公开的信息；\n' + qualifier + '披露方信息而独立开发形成的信息。')
    result = confidentiality_detail_elements(parse_contract_clauses(text), extract_field=extract_semantic_field_value)
    children = next(e for e in result if e['element_id']=='confidentiality_exceptions')['component_coverage']
    assert next(e for e in children if e['required_fact']=='独立开发信息例外')['status']=='COVERED'


@pytest.mark.parametrize('object_phrase,expected', [('乙方生产数据','OWN_DATA'),
    ('数据','UNSPECIFIED_DATA'), ('甲方原始生产数据','COUNTERPARTY_DATA')])
def test_data_owner_is_not_inferred_from_sentence_actor(object_phrase, expected):
    facts = data_use_permissions(parse_contract_clauses('乙方可以将'+object_phrase+'用于训练商业模型。'))
    assert facts and facts[0]['data_object']==expected


@pytest.mark.parametrize('duty', ['乙方承担律师费和诉讼费', '乙方赔偿甲方直接损失', '乙方负责选择律师'])
def test_service_claim_keys_use_shared_entailment_schema(duty):
    from review_v2.technology_service_analysis import claim_response_entailment_failures
    clauses = parse_contract_clauses(HEADER + '如第三方索赔，' + duty + '。')
    atoms = elements('service_claims', clauses)
    assert any(e['status']=='COVERED' for e in atoms)
    assert not claim_response_entailment_failures(atoms, clauses, provider='乙方', recipient='甲方')


@pytest.mark.parametrize('right', ['有权', '可以'])
def test_right_to_require_binds_remedy_to_obligor(right):
    atoms = rows('service_claims', f'如第三方索赔，甲方{right}要求乙方取得第三方授权或提供替代方案。')
    for key in ('license_cure','replacement_remedy'):
        assert atoms[key]['status']=='COVERED'
        assert all(s['actor']=='LICENSOR' for s in atoms[key]['supporting_evidence'])


def test_basic_claim_lead_is_partial_not_full_defense_control():
    from copy import deepcopy
    from review_v2.technology_service_analysis import claim_response_entailment_failures, claim_requirement_entailment
    text = HEADER + '如第三方索赔，由乙方负责处理全部争议。'
    clauses = parse_contract_clauses(text)
    control = next(e for e in elements('service_claims',clauses) if e['element_id']=='defense_control')
    assert control['status']=='PARTIALLY_COVERED'
    assert control['bound_evidence_ids']==[s['clause_id'] for s in control['supporting_evidence']]
    assert [c['status'] for c in control['component_coverage']]==['COVERED','MISSING']
    assert not claim_response_entailment_failures([control],clauses,provider='乙方',recipient='甲方')
    invalid = deepcopy(control)
    invalid['status'] = 'COVERED'
    assert claim_response_entailment_failures([invalid],clauses,provider='乙方',recipient='甲方')
    quote = control['supporting_evidence'][0]['quote']
    assert claim_requirement_entailment('defense_control',quote,text,'乙方','甲方',support_status='PARTIALLY_COVERED')
    assert not claim_requirement_entailment('defense_control',quote,text,'乙方','甲方',support_status='COVERED')
