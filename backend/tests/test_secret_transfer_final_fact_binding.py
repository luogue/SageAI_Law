"""Secret-transfer atomic facts, public scope inheritance and release invariants."""
import json
from copy import deepcopy
from pathlib import Path
from types import SimpleNamespace
import pytest
from review_v2.clause_parser import parse_contract_clauses
from review_v2.secret_transfer_elements import elements
from review_v2.confidentiality_remedies import canonical_confidentiality_remedies, confidentiality_binding_failures
from review_v2.technology_service_analysis import classify_technology_transaction

HEADER='技术秘密转让合同\n甲方（让与方）：甲公司\n乙方（受让方）：乙公司\n'
TEXT=Path(__file__).with_name('fixtures').joinpath('secret_transfer_final_fact_binding.txt').read_text(encoding='utf-8')

def atoms(family,text):
    return {e['element_id']:e for e in elements(family,parse_contract_clauses(HEADER+text))}

@pytest.mark.parametrize('title', ['技术秘密转让合同','专有技术转让合同','非公开技术转让合同','技术转让（技术秘密）合同','技术转让合同（技术秘密）'])
def test_secret_transfer_title_does_not_require_contiguous_generic_title(title):
    assert classify_technology_transaction(title+'\n甲方将技术秘密整体转让给乙方，乙方支付转让价款。')['tertiary_subtype']=='TECHNICAL_SECRET_TRANSFER'

@pytest.mark.parametrize('title', ['技术秘密许可合同','专有技术许可合同','非专利技术许可合同'])
def test_secret_license_is_not_transfer(title):
    c=classify_technology_transaction(title+'\n甲方授予乙方技术秘密普通使用许可，乙方支付许可费。')
    assert c['tertiary_subtype']=='TECHNICAL_SECRET_LICENSE'

@pytest.mark.parametrize('modal',['有权','可以','可'])
@pytest.mark.parametrize('party',['乙方','受让方'])
def test_granted_rights_keep_actor_and_payment_domain(modal,party):
    e=atoms('secret_transfer_scope',f'第二条 权利范围\n{party}{modal}自行使用、改进该技术并用于研发、生产及销售。')
    assert all(e[k]['status']=='COVERED' for k in ('transferee_use_right','transferee_improvement_right','production_commercialization_right'))

@pytest.mark.parametrize('text',['乙方使用技术后支付转让费。','乙方完成生产后支付40万元。','甲方有权自行使用、改进该技术并用于生产及销售。'])
def test_timing_or_opposite_actor_is_not_transferee_right(text):
    e=atoms('secret_transfer_scope',text)
    assert all(e[k]['status']=='MISSING' for k in ('transferee_use_right','transferee_improvement_right','production_commercialization_right'))

@pytest.mark.parametrize('absence',['未约定','没有约定','未明确约定'])
def test_parallel_absence_is_not_grant(absence):
    e=atoms('secret_transfer_scope',f'双方{absence}：\n乙方可以自行使用技术；\n乙方可以改进技术；\n乙方可以生产及销售。')
    assert all(e[k]['status']=='MISSING' for k in ('transferee_use_right','transferee_improvement_right','production_commercialization_right'))

@pytest.mark.parametrize('negative',['并非','不是','未通过'])
def test_lawful_source_warranty_is_not_infringement(negative):
    e=atoms('secret_transfer_warranty',f'甲方保证：\n该技术秘密{negative}盗窃、欺诈或者违反保密义务等方式取得。')
    assert e['lawful_source']['status']=='COVERED'

@pytest.mark.parametrize('condition',['如果','若','如'])
def test_hypothetical_authority_is_not_warranty(condition):
    e=atoms('secret_transfer_warranty',f'{condition}甲方有权处分并转让技术秘密，双方将进一步协商。')
    assert e['transferor_authority']['status']=='MISSING'

@pytest.mark.parametrize('absence',['未约定','未明确约定','没有约定'])
def test_price_absence_does_not_erase_loss_notice(absence):
    e=atoms('secret_transfer_loss',f'甲方知悉技术秘密可能已经公开时，应及时通知乙方，但双方{absence}具体通知期限。\n全部核心技术合法公开后，双方{absence}乙方是否仍应支付剩余转让价款。')
    assert e['secrecy_loss_notice']['status']=='COVERED'
    assert e['notice_deadline']['status']==e['remaining_price_after_total_loss']['status']=='MISSING'

@pytest.mark.parametrize('obligation',['仍应支付','无需支付','不再支付'])
def test_total_loss_price_is_an_arrangement_with_its_own_direction(obligation):
    e=atoms('secret_transfer_loss',f'即使全部核心技术已经公开，乙方{obligation}剩余转让价款。')
    assert e['remaining_price_after_total_loss']['status']=='COVERED'

@pytest.mark.parametrize('actor',['任何一方','甲方','乙方'])
@pytest.mark.parametrize('separator',['；\n',';\n'])
def test_leak_list_retains_condition_actor_modal_and_exact_span(actor,separator):
    text=f'第十四条 泄密处理\n{actor}发现技术秘密可能泄露时，应立即：\n'+separator.join(['停止继续披露','限制未经授权人员继续使用','控制扩散范围','保存有关日志和证据','通知另一方'])+'。\n双方未约定具体通知期限。'
    clauses=parse_contract_clauses(text)
    e={e['element_id']:e for e in canonical_confidentiality_remedies(clauses)}
    for k in ('stop_disclosure','stop_use','mitigation_obligation','evidence_preservation','incident_notification'):
        assert e[k]['status']=='COVERED'
        assert all(s['quote'] in text and '应立即' in s['quote'] for s in e[k]['supporting_evidence'])
    assert e['notification_deadline']['status']=='MISSING'
    assert not confidentiality_binding_failures(list(e.values()))

@pytest.mark.parametrize('component,asset', [('open_source_compliance','包含开源组件'),('software_copyright_proof','已取得软件著作权'),('third_party_code_authorization','包含第三方代码')])
def test_proof_categories_are_activated_by_actual_asset(component,asset):
    from review_v2.engine import _technical_secret_transfer_proof_results
    pure=HEADER+'第一条 技术秘密范围\n本合同转让的技术秘密包括：算法参数；设备校准流程。'
    plain=_technical_secret_transfer_proof_results(parse_contract_clauses(pure))[0]
    involved=_technical_secret_transfer_proof_results(parse_contract_clauses(pure+'\n合同技术'+asset+'。'))[0]
    assert next(e for e in plain if e['element_id']==component)['status']=='NOT_APPLICABLE'
    assert next(e for e in involved if e['element_id']==component)['status']=='MISSING'

@pytest.fixture(scope='module',params=['甲方/让与方','乙方/受让方'])
def report(request):
    from review_v2.engine import review_contract_v2
    from review_v2.user_profile import UserRiskProfile
    r=review_contract_v2(TEXT,'technology',use_llm=False,profile=UserRiskProfile(user_identity=request.param))
    out=Path(__file__).resolve().parents[2]/'artifacts/technology_pass_semantics/round28_secret_transfer_binding'
    out.mkdir(parents=True,exist_ok=True)
    out.joinpath('local_'+('transferor' if request.param.startswith('甲') else 'transferee')+'.json').write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8')
    return r

@pytest.mark.parametrize('rule,keys',[
    ('TC-01-03',['transferred_subject']),
    ('TC-06-01',['transferred_subject','transferee_use_right','transferee_improvement_right','production_commercialization_right','transferor_retransfer_restriction','transferor_post_transfer_use_restriction','retained_general_knowhow']),
    ('TC-06-03',['transferor_authority','lawful_source','no_conflicting_transfer','no_conflicting_exclusive_license','historical_use_disclosure']),
    ('TC-11-01',['confidential_information_scope','confidentiality_obligation','need_to_know_personnel','third_party_disclosure_restriction']),
    ('TC-11-02',['confidential_information_scope','compelled_disclosure_exception','prior_notice_when_legally_permitted']),
    ('TC-11-04',['stop_disclosure','stop_use','mitigation_obligation','evidence_preservation','incident_notification','breach_damage_liability']),
    ('TC-12-02',['notification_requirement','licensor_assistance','refund_or_termination_remedy','direct_damage']),
    ('TC-12-03',['secrecy_loss_trigger','transferor_fault_secrecy_loss_liability','lawful_public_domain_trigger','secrecy_loss_notice']),
])
def test_final_elements_own_direct_registered_evidence(report,rule,keys):
    item=next(i for i in report['items'] if i['item_id']==rule)
    for key in keys:
        e=next(e for e in item['coverage_elements'] if e['element_id']==key)
        assert e['status']=='COVERED'
        assert e['source_fact_key'] and e['supporting_evidence']
        proof=[s for s in item['evidence_clauses'] if key in s.get('supports_element_ids',[])]
        assert proof and all(s['verified_original'] and s['support_type']=='DIRECT' for s in proof)

def test_original_gate_roots_are_fixed_and_actual_gaps_remain(report):
    assert report['report_context']['contract_type_label']=='技术合同—技术转让合同—技术秘密转让合同'
    assert report['release_quality_gate']['status']=='REPORT_READY',report['release_quality_gate']['failures']
    by={i['item_id']:i for i in report['items']}
    for key in ('TC-03-04','TC-13-02'):
        e=by[key]['coverage_elements']
        assert by[key]['coverage_status']=='部分覆盖'
        assert any(x['status']=='COVERED' and x.get('evidence_ids') for x in e)
        assert not any(x['element_id']=='existing_ip_transaction_context' for x in e)
    for rule,key in [('TC-06-01','historical_customer_continued_use_boundary'),('TC-06-03','documentary_chain_proof'),('TC-12-03','remaining_price_after_total_loss'),('TC-12-03','notice_deadline')]:
        assert next(e for e in by[rule]['coverage_elements'] if e['element_id']==key)['status']=='MISSING'

@pytest.mark.parametrize('corruption',['missing_with_positive','covered_without_source','partial_without_source'])
def test_independent_gate_rejects_corrupt_final_states(report,corruption):
    from review_v2.element_evidence_projection import audit
    item=SimpleNamespace(**deepcopy(next(i for i in report['items'] if i['item_id']=='TC-06-01')))
    e=item.coverage_elements[0]
    if corruption=='missing_with_positive':
        e['status']='MISSING'
    else:
        e['status']='PARTIALLY_COVERED' if corruption.startswith('partial') else 'COVERED'
        e['supporting_evidence']=[]
    assert audit([item],[],parse_contract_clauses(TEXT))

def test_aggregate_absence_cannot_create_covered_ip_context(report):
    from review_v2.engine import _synchronize_canonical_risk_states
    item=SimpleNamespace(**deepcopy(next(i for i in report['items'] if i['item_id']=='TC-03-04')))
    item.decision_trace={}
    item.coverage_elements=[dict(element_id='complete_ip_proof_attachment', status='MISSING',
                                proposition='权属证明附件', evidence_ids=[], supporting_evidence=[])]
    item.evidence_clauses=[]
    finding=SimpleNamespace(**deepcopy(next(f for f in report['risk_findings'] if f['risk_group']=='technology_ip_rights_provenance')))
    finding.source_review_ids=['TC-03-04']
    finding.source_clause_ids=[]
    finding.evidence_bundle={'items':[dict(source_type='SEARCH_AUDIT',quoted_text='未找到权属证明附件')]}
    finding.issue_type='PARTIAL'
    _synchronize_canonical_risk_states([item],[finding],{})
    assert item.coverage_presence=='MISSING' and finding.issue_type=='MISSING'
    assert all(e['status']=='MISSING' for e in item.coverage_elements)
