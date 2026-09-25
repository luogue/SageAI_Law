"""Round33: independent title, prior license and reverse-grant source bindings."""
from pathlib import Path
import pytest
from review_v2.engine import _operative_technology_clauses, review_contract_v2
from review_v2.patent_transfer_elements import elements, transaction_layers, RIGHT_DOMAINS
from review_v2.proposition_scope import listed_arrangement_matches
from review_v2.technology_service_analysis import classify_technology_transaction
from review_v2.user_profile import UserRiskProfile

TEXT=(Path(__file__).parent/'fixtures/round33_patent_transfer.txt').read_text(encoding='utf8')

SCOPE=('patent_right_identity','full_patent_right_transfer','transfer_effective_on_registration',
 'transferor_no_retransfer_before_registration','transferor_no_pledge_before_registration',
 'transferor_no_new_exclusive_license','existing_license_disclosed','existing_license_survives_transfer',
 'license_back_exists','license_back_term','license_back_territory','license_back_purpose',
 'license_back_no_assignment','license_back_no_sublicense','license_back_no_new_projects','license_back_expiry')

@pytest.mark.parametrize('key',SCOPE)
def test_current_rights_have_exact_nonpayment_sources(key):
 cs=_operative_technology_clauses(TEXT)
 e=next(e for e in elements('patent_transfer_scope',cs) if e['element_id']==key)
 assert e['status']=='COVERED'
 for s in e['supporting_evidence']:
  c=next(c for c in cs if c.clause_id==s['clause_id'])
  assert s['quote'] in (getattr(c,'raw_text','') or c.text)
  assert '转让价款及支付方式' not in c.location
  assert s['source_domain'] in RIGHT_DOMAINS|{'REGISTRATION'}

@pytest.mark.parametrize('payment',[
 '专利权全部转让后甲方应支付50万元。',
 '将全部专利权转让给甲方后十个工作日内支付60万元。',
 '甲方收到乙方专利权全部转让的通知后应支付款项。',
 '专利权全部转让时，甲方须支付第一期价款。',
])
def test_payment_antecedent_does_not_establish_title_disposition(payment):
 rows=elements('patent_transfer_scope',_operative_technology_clauses('第一条 付款\n'+payment))
 assert next(e for e in rows if e['element_id']=='full_patent_right_transfer')['status']=='MISSING'

@pytest.mark.parametrize('intro',['乙方不得：','转让方禁止：'])
@pytest.mark.parametrize('member',['将许可转让给他人；','分许可给第三方；','承接新的客户项目；'])
def test_prohibition_list_retains_operator_and_subject(intro,member):
 q=intro+'\n'+member
 rows=list(listed_arrangement_matches(r'转让|分许可|项目',q,introduction_pattern=r'不得|禁止'))
 assert rows and rows[0]['quote']==q

@pytest.mark.parametrize('intro',['双方未约定：','双方没有明确约定：','双方未作明确约定：'])
def test_missing_list_never_creates_prohibition(intro):
    assert not list(listed_arrangement_matches(r'分许可',intro+'\n乙方不得分许可。',introduction_pattern=r'约定|不得'))

@pytest.mark.parametrize('intro',['乙方不保证：','乙方未确认：','乙方没有声明：'])
def test_negated_introduction_cannot_assert_ownership(intro):
 assert not list(listed_arrangement_matches(r'专利权人',intro+'\n乙方为专利权人。',introduction_pattern=r'保证|确认|声明'))

@pytest.mark.parametrize('family,covered,missing',[
 ('patent_transfer_delivery',{'delivery_deadline','receipt_confirmation','delivery_document_list'},
  {'nonconforming_delivery_remedy','delivery_remedy_deadline','delivery_failed_cure_termination','delivery_failed_cure_refund'}),
 ('patent_transfer_warranty',{'ownership_guarantee','transfer_authority','co_owner_absence','prior_transfer_absence',
  'pledge_status','seizure_status','ownership_dispute_status','existing_license_disclosure'},set()),
 ('patent_transfer_formalities',{'registration_deadline','registration_responsible_party','registration_materials','registration_cost','registration_effect'},set()),
 ('patent_transfer_materials',{'final_delivery_list','receipt_confirmation','file_version','delivery_method'},{'file_identifier','delivery_quantity'}),
 ('patent_transfer_confidentiality',{'confidential_information_scope','confidentiality_obligation','third_party_disclosure_restriction'},set()),
 ('patent_transfer_improvement_sharing',{'no_automatic_coownership','no_automatic_free_license','priority_transfer_right'},set()),
 ('patent_transfer_improvement_notice',{'improvement_notice_required','notice_deadline'},{'priority_transfer_exercise_deadline'}),
])
def test_facts_and_remaining_gaps_are_independent(family,covered,missing):
 rows={e['element_id']:e for e in elements(family,_operative_technology_clauses(TEXT))}
 for key in covered:assert rows[key]['status']=='COVERED' and rows[key]['supporting_evidence']
 for key in missing:assert rows[key]['status']=='MISSING' and not rows[key]['supporting_evidence']

@pytest.mark.parametrize('changed',[
 TEXT,
 TEXT.replace('甲方','替换方').replace('乙方','甲方').replace('替换方','乙方'),
 TEXT.replace('4,000,000','7,600,000').replace('ZL202210876543.2','ZL202010111222.4'),
])
def test_main_asset_not_replaced_by_reverse_or_historical_license(changed):
 c=classify_technology_transaction(changed)
 assert c['tertiary_subtype']=='PATENT_RIGHT_TRANSFER'
 layers=c['transaction_layers']
 assert layers['main_transaction']=='PATENT_RIGHT_TRANSFER'
 assert {r['type'] for r in layers['sub_transactions']}=={'PATENT_LICENSE_BACK','EXISTING_THIRD_PARTY_ORDINARY_LICENSE'}
 rows=layers['sub_transactions']
 assert set(s['clause_id'] for s in rows[0]['sources']).isdisjoint(s['clause_id'] for s in rows[1]['sources'])

@pytest.fixture(scope='module')
def report():
 return review_contract_v2(TEXT,'technology',use_llm=False,profile=UserRiskProfile(user_identity='甲方/受让方'))

def test_final_evidence_and_gate_use_current_components(report):
 assert report['release_quality_gate']['status']=='REPORT_READY'
 items={x['item_id']:x for x in report['items']}
 scope=items['TC-06-01']
 assert scope['coverage_status']=='通过'
 assert {e['element_id'] for e in scope['coverage_elements']}==set(SCOPE)
 assert scope['evidence_clauses'][0]['source_domain'] in RIGHT_DOMAINS
 domains=[e['source_domain'] for e in scope['evidence_clauses']]
 assert max(i for i,d in enumerate(domains) if d in RIGHT_DOMAINS) < domains.index('REGISTRATION')
 assert all(e['support_type']=='DIRECT' for e in scope['evidence_clauses'])
 assert items['TC-10-02']['decision_trace']['pass_evidence_audit']['status']=='PASS'
 assert items['TC-11-01']['decision_trace']['pass_evidence_audit']['status']=='PASS'

def test_real_residuals_survive_projection(report):
 items={x['item_id']:x for x in report['items']}
 assert items['TC-06-02']['coverage_status']=='部分覆盖'
 assert items['TC-10-03']['coverage_status']=='部分覆盖'
 assert items['TC-12-02']['coverage_status']=='部分覆盖'
 assert items['TC-11-02']['coverage_status']!='通过'
 assert items['TC-13-01']['coverage_status']=='部分覆盖'
 assert items['TC-06-03']['coverage_status']=='部分覆盖'
 warranty={e['element_id']:e for e in items['TC-06-03']['coverage_elements']}
 assert warranty['invalidity_proceeding_disclosure']['status']=='COVERED'
 assert warranty['total_invalidity_paid_refund']['status']=='MISSING'
 assert warranty['partial_invalidity_price_method']['status']=='MISSING'
 assert warranty['independent_claim_value_adjustment']['status']=='COVERED'
