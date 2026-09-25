"""Round32: transaction-owned facts and exact final evidence bindings."""
from pathlib import Path
import pytest
from review_v2.engine import _operative_technology_clauses, review_contract_v2
from review_v2.application_transfer_elements import elements
from review_v2.technology_service_analysis import classify_technology_transaction, build_technology_fact_registry
from review_v2.technology_patent_transfer_analysis import analyze_dispute_resolution_options
from review_v2.penalty_base import analyze
from review_v2.user_profile import UserRiskProfile

TEXT=(Path(__file__).parent/'fixtures/round32_patent_application_transfer.txt').read_text(encoding='utf8')

@pytest.mark.parametrize('title,body,expected',[
 ('专利申请权转让合同','申请号CN202610123456.1，尚未授权，处于实质审查。乙方将全部专利申请权转让给甲方。','PATENT_APPLICATION_RIGHT_TRANSFER'),
 ('技术转让合同','本合同转让标的为尚未授权专利申请。专利申请权自登记之日起转移。','PATENT_APPLICATION_RIGHT_TRANSFER'),
 ('专利权转让合同','专利号ZL202210123456.1，已取得授权。乙方将专利权转让给甲方，办理专利权转让登记。','PATENT_RIGHT_TRANSFER'),
 ('技术秘密转让合同','乙方向甲方转让其合法持有的技术秘密。技术秘密未申请专利。转让价款由甲方支付。','TECHNICAL_SECRET_TRANSFER'),
])
@pytest.mark.parametrize('attachment',['','\n附属未公开技术资料应保密；已公开专利申请文件不作为技术秘密保护。'])
def test_asset_routing_not_displaced_by_ancillary_confidentiality(title,body,expected,attachment):
 assert classify_technology_transaction(title+'\n甲方（受让方）乙方（转让方）\n'+body+attachment)['tertiary_subtype']==expected

@pytest.mark.parametrize('prefix',[
 '未收到第三方关于申请权归属的正式诉讼或仲裁通知。',
 '未提交仲裁委员会仲裁。',
 '双方未约定提交仲裁委员会仲裁。',
 '第三方提出仲裁请求后乙方应通知甲方。',
 '仲裁费由乙方承担。',
])
def test_claim_mentions_and_negative_arbitration_are_not_chosen_forum(prefix):
 facts=analyze_dispute_resolution_options(prefix+'协商不成，向甲方所在地有管辖权的人民法院提起诉讼。')
 assert not facts['arbitration_selected']
 assert facts['litigation_selected']

def test_actual_two_forums_remain_conflict():
 facts=analyze_dispute_resolution_options('争议提交北京仲裁委员会仲裁。争议向人民法院提起诉讼。')
 assert facts['arbitration_selected'] and facts['litigation_selected']

@pytest.mark.parametrize('amount',['800,000元','250万元','人民币3,400,000元','1200000元'])
@pytest.mark.parametrize('rate',['0.03%','5%'])
def test_inline_penalty_amount_is_determinable(amount,rate):
 result=analyze(f'违约方按合同总价{amount}的{rate}支付违约金。')
 assert result and all(r['status']=='DETERMINABLE' for r in result)

@pytest.mark.parametrize('gap',['双方未约定','双方未明确','双方没有约定'])
def test_missing_control_does_not_become_application_right(gap):
 rows=elements('application_control',_operative_technology_clauses('第一条 程序\n'+gap+'由甲方负责决定修改权利要求。'))
 assert next(e for e in rows if e['element_id']=='claim_amendment_control')['status']=='MISSING'

@pytest.mark.parametrize('layout',['发明人：王明、李红','发明人：\n王明\n李红','发明人/设计人：\n王明、李红'])
def test_multiline_inventor_field_keeps_original_span(layout):
 rows=elements('application_proof',_operative_technology_clauses('第一条 标的\n'+layout+'\n第二条 价款\n价款另行约定。'))
 row=next(e for e in rows if e['element_id']=='inventor_information')
 assert row['status']=='COVERED'
 assert row['supporting_evidence'][0]['quote'] in layout

def test_refund_gap_does_not_erase_explicit_future_payment_release():
 clauses=_operative_technology_clauses('第九条 审查结果\n2. 登记完成后\n因正常审查最终未获得授权的：\n已支付价款是否返还，由双方另行协商。\n第三期价款无需支付。')
 rows={e['element_id']:e for e in elements('application_outcomes',clauses)}
 assert rows['remaining_payment_after_rejection']['status']=='COVERED'
 assert rows['rejection_refund']['status']=='MISSING'

def test_title_claim_assistance_is_not_defense_control():
 r=build_technology_fact_registry('专利申请权转让合同\n甲方（受让方）\n乙方（转让方）\n第一条\n如第三方主张申请权归属，乙方应提供研发记录及申请来源证明。双方未约定抗辩控制权、律师选择权和和解审批权限。')['third_party_claim']['response_element_evidence']
 assert r.get('claim_assistance')
 assert not any(r.get(k) for k in ('defense_control','lawyer_selection','settlement_authority'))

@pytest.fixture(scope='module')
def report():
 return review_contract_v2(TEXT,'technology',use_llm=False,profile=UserRiskProfile(user_identity='甲方/受让方'))

def item(report,key):return next(i for i in report['items'] if i['item_id']==key)

def test_current_gate_and_original_creator_mismatch(report):
 assert report['release_quality_gate']['status']=='REPORT_READY',report['release_quality_gate']['failures']
 row=item(report,'TC-03-03')
 e=next(e for e in row['coverage_elements'] if e['element_id']=='creator_named_identity')
 assert e['status']=='COVERED'
 assert e['supporting_evidence'] and e['source_fact_key']=='technology.creator.named_identity'
 assert e['evidence_ids']

@pytest.mark.parametrize('key',['TC-01-03','TC-06-01','TC-06-04','COMMON-20-01'])
def test_current_core_states(report,key):assert item(report,key)['coverage_status']=='通过'

@pytest.mark.parametrize('key',['patent_application_identity','application_number','application_date','publication_number','application_status','current_applicant'])
def test_identity_uses_first_article(report,key):
 e=next(e for e in item(report,'TC-01-03')['coverage_elements'] if e['element_id']==key)
 assert e['status']=='COVERED'
 assert all('第一条' in s.get('location','') for s in e['supporting_evidence'])

@pytest.mark.parametrize('key',['TC-03-04','TC-13-02'])
def test_proof_keeps_employee_gap_without_secret_schema(report,key):
 row=item(report,key)
 assert row['coverage_status']=='部分覆盖'
 es={e['element_id']:e for e in row['coverage_elements']}
 assert es['employee_invention_title_chain']['status']=='PARTIALLY_COVERED'
 assert es['inventor_information']['status']=='COVERED'
 assert not set(es)&{'current_secret_status','historical_disclosure_objects','existing_confidentiality_measures'}

@pytest.mark.parametrize('key',['rejection_refund','reexamination_failure_refund','price_adjustment_on_scope_shrinkage'])
def test_real_application_outcome_gaps_are_retained(report,key):
 es={e['element_id']:e for e in item(report,'TECH-SHARED-APP-REJECTION-01')['coverage_elements']}
 assert es[key]['status']=='MISSING'
 assert es['remaining_payment_after_rejection']['status']=='COVERED'

def test_no_secret_loss_or_invented_arbitration_risk(report):
 assert item(report,'TC-12-03')['coverage_status']=='不适用'
 assert not any(i['item_id']=='TECH-GEN-02' and i.get('risk_status')=='ADVERSE' for i in report['items'])
