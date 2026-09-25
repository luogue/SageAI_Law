from pathlib import Path
import pytest
from review_v2.clause_parser import parse_contract_clauses
from review_v2.technology_service_elements import elements
from review_v2.consulting_element_facts import elements as consulting_elements
from review_v2.penalty_base import analyze

TEXT=(Path(__file__).parent/'fixtures'/'round41_consulting.txt').read_text(encoding='utf8')
CLAUSES=parse_contract_clauses(TEXT)

def indexed(rows): return {r['element_id']:r for r in rows}

def test_confidentiality_purpose_and_compelled_notice_are_direct_facts():
    controls=indexed(elements('confidentiality_controls',CLAUSES))
    disclosure=indexed(elements('confidentiality_disclosure',CLAUSES))
    assert controls['purpose_limitation']['status']=='COVERED'
    assert disclosure['prior_notice_when_legally_permitted']['status']=='COVERED'
    assert '履行本合同以外' in controls['purpose_limitation']['supporting_evidence'][0]['quote']
    assert '法律允许范围内提前通知信息提供方' in disclosure['prior_notice_when_legally_permitted']['supporting_evidence'][0]['quote']

def test_material_exit_projects_data_copy_and_retention_atoms():
    rows=indexed(elements('material_exit',CLAUSES))
    for key in ('termination_return_or_delete','confidential_disposal_confirmation'):
        assert rows[key]['status']=='COVERED'
        assert rows[key]['supporting_evidence']
    components=indexed(rows['termination_return_or_delete']['component_coverage'])
    for key in ('service_end_disposition_trigger','original_data_return','original_data_deletion','identifiable_copy_deletion','retention_exception'):
        assert components[key]['status']=='COVERED'
        assert components[key]['supporting_evidence']
    assert rows['processing_deadline']['status']=='MISSING'
    assert rows['confidential_backup_deletion']['status']=='MISSING'

def test_consulting_families_share_verified_subject_quality_and_payment_facts():
    subject=indexed(consulting_elements('consulting_subject',CLAUSES))
    assert subject['consulting_project']['status']=='COVERED'
    assert subject['consulting_deliverable']['status']=='COVERED'
    assert subject['consulting_scope']['canonical_alias_of']=='consulting_quality.consulting_scope'
    assert subject['consulting_deliverable']['canonical_alias_of']=='consulting_quality.report_contents'
    for family, keys in {
        'consulting_quality':('consulting_scope','report_contents','delivery_form','acceptance_standard'),
        'consulting_decision':('qualified_consulting_decision_risk','consultant_fault_exception'),
        'consulting_inputs':('technical_materials','cooperation_conditions','truthfulness_completeness'),
        'consulting_remedy':('defect_trigger','correction_period','correction_remedy'),
        'consulting_payment':('consulting_fee_total','payment_milestones'),
    }.items():
        rows=indexed(consulting_elements(family,CLAUSES))
        assert all(rows[key]['status']=='COVERED' for key in keys)

def test_consulting_total_is_reused_by_penalty_base():
    rows=analyze(TEXT)
    total=next(r for r in rows if r['base']=='合同总价')
    assert total['status']=='DETERMINABLE'
    assert any('技术咨询费总额' in source and '420,000元' in source for source in total['definitions'])

@pytest.mark.parametrize('party',['甲方','乙方'])
def test_round41_final_projection_is_exact_and_force_majeure_is_not_confidentiality_evidence(party):
    from review_v2.engine import review_contract_v2
    from review_v2.user_profile import UserRiskProfile
    report=review_contract_v2(TEXT,'technology',use_llm=False,profile=UserRiskProfile(user_identity=party))
    assert report['release_quality_gate']['status']=='REPORT_READY',report['release_quality_gate']['failures']
    items={i['item_id']:i for i in report['items']}
    expected={
      'TC-11-01':('purpose_limitation',),
      'TC-11-02':('prior_notice_when_legally_permitted',),
      'TC-11-03':('termination_return_or_delete','confidential_disposal_confirmation'),
      'TC-01-03':('consulting_project','consulting_deliverable'),
      'TC-08-01':('consulting_scope','report_contents','delivery_form','acceptance_standard'),
      'TC-08-02':('qualified_consulting_decision_risk','consultant_fault_exception'),
      'TC-08-03':('technical_materials','cooperation_conditions','truthfulness_completeness'),
      'TC-08-04':('defect_trigger','correction_period','correction_remedy'),
      'TC-08-05':('consulting_fee_total','payment_milestones'),
    }
    for rule,keys in expected.items():
      item=items[rule]; rows=indexed(item['coverage_elements'])
      absent={x.get('element_id') for x in item['decision_trace'].get('element_absence_searches',[]) if x.get('result')=='NOT_FOUND'}
      for key in keys:
        e=rows[key]
        assert e['status']=='COVERED',(rule,key,e)
        assert key not in absent
        ev=[x for x in item['evidence_clauses'] if x.get('evidence_id') in e.get('evidence_ids',[])]
        assert ev and all(x['evidence_id'].startswith('SRC-') and x.get('support_type')=='DIRECT' and x.get('verified_original') for x in ev),(rule,key,e.get('evidence_ids'))
    common=items['COMMON-20-01']
    assert common['coverage_status'] in {'通过','PASS'}
    incident=items['TC-11-04']
    assert all('不可抗力' not in str(e.get('quote') or e.get('text') or '') for e in incident['evidence_clauses'])
    mitigation=next(e for e in incident['coverage_elements'] if e['element_id']=='mitigation_obligation')
    assert mitigation['status']=='MISSING'
    disposition=next(e for e in items['TC-11-03']['coverage_elements'] if e['element_id']=='termination_return_or_delete')
    components=indexed(disposition['component_coverage'])
    assert all(components[key]['status']=='COVERED' for key in
               ('service_end_disposition_trigger','original_data_return','original_data_deletion','identifiable_copy_deletion','retention_exception'))
    gates=report['release_quality_gate']['gate_results']
    assert gates['REVIEW_EVIDENCE_ELEMENT_MISMATCH']=='PASS'
    assert gates['EXACT_ELEMENT_REPORT_INVARIANT']=='PASS'
