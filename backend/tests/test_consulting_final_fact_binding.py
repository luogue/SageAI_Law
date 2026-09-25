"""Consulting duties retain atomic ownership, exact sources and independent gaps."""
from pathlib import Path
import json
import pytest
from review_v2.clause_parser import parse_contract_clauses
from review_v2.consulting_element_facts import elements as consulting
from review_v2.technology_service_elements import elements as shared
from review_v2.data_use_scope import data_use_permissions

HEADER = '技术咨询合同\n甲方（委托方）：甲公司\n乙方（咨询方）：乙公司\n'

def rows(family, text):
    fn = consulting if family.startswith('consulting_') else shared
    return {e['element_id']: e for e in fn(family, parse_contract_clauses(HEADER + text))}

@pytest.mark.parametrize('absence', ['未约定', '未明确约定', '没有约定'])
@pytest.mark.parametrize('sender,target', [('甲方','乙方'), ('乙方','甲方')])
def test_claim_notice_direction_and_parallel_missing(absence, sender, target):
    text = f'第十五条 第三方权利主张\n如第三方主张咨询报告侵犯其知识产权，{sender}应及时通知{target}并配合处理。\n双方{absence}第三方索赔的具体通知期限、抗辩控制权、律师选择权及和解审批机制。'
    e = rows('service_claims', text)
    assert e['notification_requirement']['status'] == 'COVERED'
    for k in ('notification_deadline','defense_control','lawyer_selection','settlement_authority'):
        assert e[k]['status']=='MISSING' and not e[k]['supporting_evidence']

@pytest.mark.parametrize('sender,target', [('甲方','乙方'), ('乙方','甲方')])
@pytest.mark.parametrize('duty', ['收到第三方索赔后，应在五日内通知', '应在收到第三方索赔后五日内通知', '收到第三方索赔后及时通知'])
def test_notice_subject_survives_receipt_and_timing_modifiers(sender,target,duty):
    e=rows('service_claims',f'第十五条 第三方索赔\n{sender}{duty}{target}。')
    assert e['notification_requirement']['status']=='COVERED'
    if '五日内' in duty:
        assert e['notification_deadline']['status']=='COVERED'

@pytest.mark.parametrize('days', ['七个工作日', '7个工作日', '十日'])
@pytest.mark.parametrize('defect', ['遗漏', '缺漏', '错误'])
def test_correction_duties_survive_absent_reacceptance(days, defect):
    e=rows('consulting_remedy', f'第八条 报告验收\n甲方认为报告存在{defect}的，应书面提出。\n乙方应在收到书面意见后{days}内合理补充。\n双方未约定补充完成后的再次验收期限。')
    for k in ('defect_trigger','correction_period','correction_remedy'):
        assert e[k]['status']=='COVERED' and e[k]['supporting_evidence']
    assert e['reinspection_deadline']['status']=='MISSING'

@pytest.mark.parametrize('risk', ['决策责任', '决策风险', '商业风险'])
@pytest.mark.parametrize('fault', ['故意', '重大过错', '重大过失'])
def test_decision_allocation_and_fault_exception_are_independent(risk, fault):
    e=rows('consulting_decision',f'甲方根据乙方咨询意见作出采购决策，最终{risk}由甲方承担。\n乙方因{fault}提供虚假数据导致甲方损失的，应承担赔偿责任。')
    assert all(e[k]['status']=='COVERED' for k in ('qualified_consulting_decision_risk','consultant_fault_exception'))

@pytest.mark.parametrize('criterion', ['完成约定咨询事项','提交完整报告','列明主要分析依据','对主要技术问题作出分析'])
def test_acceptance_dimensions_are_operative_criteria(criterion):
    text=f'第八条 报告验收\n验收主要检查：\n是否{criterion}。'
    e=rows('consulting_quality',text)['acceptance_standard']
    assert e['status']=='COVERED'
    assert all('验收主要检查' in s['quote'] for s in e['supporting_evidence'])

@pytest.mark.parametrize('employee', ['员工','人员'])
@pytest.mark.parametrize('modal', ['仅可', '只可'])
def test_need_to_know_is_a_personnel_boundary(employee, modal):
    e=rows('confidentiality_controls', f'第十三条 保密义务\n接收方{modal}允许确有知悉必要的{employee}接触相关信息。')
    assert e['need_to_know_personnel']['status']=='COVERED'

@pytest.mark.parametrize('duration', ['六年','6年','三年'])
def test_duration_and_legally_permitted_prior_notice(duration):
    e=rows('confidentiality_disclosure',f'第十三条 保密义务\n保密期限为有关信息披露之日起{duration}。\n根据法律法规或者有权机关要求必须披露的，可以在必要范围内依法披露，并应在法律允许时提前通知另一方。')
    for k in ('confidentiality_period','compelled_disclosure_exception','prior_notice_when_legally_permitted'):
        assert e[k]['status']=='COVERED'

@pytest.mark.parametrize('days', ['十个工作日','10个工作日'])
@pytest.mark.parametrize('end', ['合同终止后','合同解除后'])
def test_material_exit_refinements_do_not_erase_duties(days,end):
    e=rows('material_exit',f'第十八条 资料返还和删除\n{end}，甲方有权要求乙方返还或者删除非公开项目资料及原始数据。\n乙方应在收到书面通知后{days}内完成处理。\n依法必须保存或者因系统备份暂时不能删除的资料，应继续受到保密义务限制，不得用于本项目之外的目的。\n双方未约定备份最终删除期限和删除确认方式。')
    for k in ('termination_return_or_delete','processing_deadline','retained_backup_use_restriction'):
        assert e[k]['status']=='COVERED'
    for k in ('confidential_backup_deletion','confidential_disposal_confirmation'):
        assert e[k]['status']=='MISSING'

@pytest.mark.parametrize('noun', ['汇总统计信息','统计数据','匿名化统计数据'])
def test_anonymous_object_does_not_inherit_prohibited_raw_data_use(noun):
    text=f'未经甲方书面同意，乙方不得使用甲方原始项目数据训练面向其他客户的商业模型。\n乙方可以保留无法识别甲方、项目位置、具体设备和经营情况的{noun}，用于改善其通用分析方法。'
    facts=data_use_permissions(parse_contract_clauses(text))
    assert len(facts)==1
    assert facts[0]['actor']=='乙方' and facts[0]['data_object']=='ANONYMOUS_STATISTICS'
    assert not facts[0]['external_use']

def test_permission_actor_is_not_the_condition_owner():
    facts=data_use_permissions(parse_contract_clauses('经甲方书面同意，乙方可以将甲方原始数据用于模型训练。'))
    assert facts[0]['actor']=='乙方' and facts[0]['data_owner']=='甲方'
    assert facts[0]['external_use']

@pytest.fixture(scope='module',params=['甲方/委托方','乙方/咨询方'])
def report(request):
    from review_v2.engine import review_contract_v2
    from review_v2.user_profile import UserRiskProfile
    text=Path(__file__).with_name('fixtures').joinpath('consulting_final_fact_binding.txt').read_text(encoding='utf-8')
    report=review_contract_v2(text,'technology',use_llm=False,profile=UserRiskProfile(user_identity=request.param))
    out=Path(__file__).resolve().parents[2]/'artifacts/technology_pass_semantics/round27_consulting_binding'
    out.mkdir(parents=True,exist_ok=True)
    (out/('local_client.json' if request.param.startswith('甲') else 'local_provider.json')).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    return report

@pytest.mark.parametrize('original_element', ['claim_notice_and_participation','PRIMARY_EVIDENCE'])
def test_original_gate_mismatches_use_direct_registered_fact(report,original_element):
    item=next(i for i in report['items'] if i['item_id']=='TC-12-02')
    e=next(e for e in item['coverage_elements'] if e['element_id']=='notification_requirement')
    assert e['status']=='COVERED' and e['source_fact_key']
    assert item['decision_trace']['contract_fact_registry_consumption']['facts'][e['source_fact_key']]['status']=='FOUND'
    evidence=[item['evidence_clauses'][0]] if original_element=='PRIMARY_EVIDENCE' else [s for s in item['evidence_clauses'] if e['element_id'] in s.get('supports_element_ids',[])]
    assert evidence and all(s['support_type']=='DIRECT' and s['verified_original'] for s in evidence)

@pytest.mark.parametrize('rule,keys', [
    ('TC-01-03',['consulting_project','consulting_scope']),
    ('TC-08-01',['consulting_scope','acceptance_standard']),
    ('TC-08-02',['qualified_consulting_decision_risk','consultant_fault_exception']),
    ('TC-08-04',['defect_trigger','correction_period','correction_remedy']),
    ('TC-08-05',['consulting_fee_total','payment_milestones']),
    ('TC-11-01',['need_to_know_personnel']),
    ('TC-11-02',['confidentiality_period','compelled_disclosure_exception','prior_notice_when_legally_permitted']),
    ('TC-11-03',['termination_return_or_delete','processing_deadline','retained_backup_use_restriction']),
    ('TC-11-04',['stop_disclosure','mitigation_obligation']),
])
def test_current_components_have_owned_verified_sources(report,rule,keys):
    item=next(i for i in report['items'] if i['item_id']==rule)
    elements={e['element_id']:e for e in item['coverage_elements']}
    for key in keys:
        e=elements[key]
        assert e['status']=='COVERED'
        assert e['source_fact_key'] and e['supporting_evidence']
        direct=[s for s in item['evidence_clauses'] if key in s.get('supports_element_ids',[]) and e['source_fact_key'] in s.get('canonical_fact_keys',[])]
        assert direct and all(s['support_type']=='DIRECT' and s['verified_original'] for s in direct)

def test_final_report_keeps_gaps_and_data_boundaries(report):
    assert report['report_context']['contract_type_label']=='技术合同—技术咨询合同'
    assert report['release_quality_gate']['status']=='REPORT_READY',report['release_quality_gate']['failures']
    items={i['item_id']:i for i in report['items']}
    for k in ('TC-08-04','TC-11-03','TC-11-04'):
        assert items[k]['coverage_status']=='部分覆盖'
    assert items['TC-11-02']['coverage_status']!='风险条款'
    assert all(e['status']=='MISSING' for e in items['TC-12-02']['coverage_elements'] if e['element_id'] in ('defense_control','lawyer_selection','settlement_authority','notification_deadline'))
