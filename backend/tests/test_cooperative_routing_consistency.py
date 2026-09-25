from pathlib import Path
import pytest
from review_v2.clause_parser import parse_contract_clauses
from review_v2.technology_service_analysis import classify_technology_transaction
from review_v2.domain_selection import resolve_domain_selection
from review_v2.cooperative_arrangements import elements
from review_v2.proposition_scope import arrangement_matches, scoped_propositions
from review_v2.sale_evidence import extract
TEXT=(Path(__file__).parent/'fixtures/round34_cooperative.txt').read_text(encoding='utf8')

@pytest.mark.parametrize('title',['技术合作开发合同','联合研发协议','项目协议',''])
@pytest.mark.parametrize('selected',['technology','sale'])
def test_bilateral_research_routes_without_title_dependency(title,selected):
 text=TEXT.replace('技术合作开发合同',title).replace('本合同属于合作开发合同。','')
 classification=classify_technology_transaction(text)
 assert classification['primary_subtype']=='COOPERATIVE_DEVELOPMENT'
 result,_,route=resolve_domain_selection(selected,text,parse_contract_clauses(text),classification)
 assert route=='technology'
 assert result.selected_domain=='TECHNOLOGY'

@pytest.mark.parametrize('wording',['未明确','未约定','尚未约定','没有约定'])
def test_missing_list_scope_reaches_every_object(wording):
 text=wording+'：\n抗辩控制权；\n律师选择权；\n诉讼费用承担。'
 assert not list(arrangement_matches(r'控制权|选择权|承担',text))
 assert all(r['polarity']=='MISSING' for r in scoped_propositions(text))

@pytest.mark.parametrize('text',['诉讼费用如何承担。','诉讼费用由双方另行协商。','诉讼费用承担待确定。','未明确：\n谁负责控制诉讼；\n律师如何选择；\n诉讼费用如何承担。'])
def test_unresolved_enforcement_cost_is_not_covered(text):
 assert not extract('common_litigation_costs',parse_contract_clauses(text))

def test_disclosure_notice_does_not_establish_contract_notice():
 clauses=parse_contract_clauses('依法强制披露时：\n接收方应在法律允许范围内提前通知信息提供方。')
 assert not extract('common_notice_delivery',clauses)
 assert extract('common_notice_delivery',parse_contract_clauses('通知地址为双方合同首部所列地址。'))

def test_determined_court_is_direct_source():
 evidence=extract('common_jurisdiction',parse_contract_clauses(TEXT))
 assert {k for e in evidence for k in e['element_ids']}=={'dispute_resolution_path','specific_dispute_forum'}
 assert all('第二十四条' in e['location'] for e in evidence)

@pytest.mark.parametrize('family,key,expected',[
 ('joint_patent_procedure','patent_application_right','COVERED'),
 ('joint_patent_procedure','application_costs','COVERED'),
 ('joint_patent_procedure','withdrawal_prohibition','COVERED'),
 ('joint_patent_procedure','nonpayer_retained_share','MISSING'),
 ('joint_patent_procedure','nonpayer_share_change','MISSING'),
 ('joint_patent_procedure','nonpayer_license_revenue','MISSING'),
 ('joint_patent_procedure','nonpayer_abandonment_effect','MISSING'),
 ('joint_patent_procedure','patent_decision_deadlock','MISSING'),
 ('joint_secret_disposition','independent_use_right','COVERED'),
 ('joint_secret_disposition','external_license_consent','COVERED'),
 ('joint_secret_disposition','external_revenue_allocation','COVERED'),
 ('joint_secret_disposition','consent_reply_deadline','MISSING'),
 ('joint_secret_disposition','consent_silence_remedy','MISSING'),
 ('joint_secret_disposition','consent_refusal_remedy','MISSING'),
 ('joint_secret_disposition','undervalue_license_control','MISSING'),
 ('cooperative_exit','exit_notice_deadline','COVERED'),
 ('cooperative_exit','exit_pending_patent_cost','MISSING'),
 ('cooperative_improvement_notice','improvement_notice_deadline','COVERED'),
 ('cooperative_improvement_notice','priority_license_exercise_deadline','MISSING'),
 ('cooperative_claims','claim_cost_allocation','MISSING')])
def test_atomic_source_and_residuals(family,key,expected):
 clauses=parse_contract_clauses(TEXT)
 e=next(e for e in elements(family,clauses) if e['element_id']==key)
 assert e['status']==expected
 assert bool(e['supporting_evidence'])==(expected=='COVERED')
 for source in e['supporting_evidence']:
  clause=next(c for c in clauses if c.clause_id==source['clause_id'])
  assert source['quote'] in clause.text

def test_three_background_layers_do_not_replace_research():
 c=classify_technology_transaction(TEXT)
 kinds={r['type'] for r in c['transaction_layers']['sub_transactions']}
 assert kinds=={'PARTY_A_BACKGROUND_PATENT_LICENSE','PARTY_B_BACKGROUND_PATENT_LICENSE','JOINT_PATENT_APPLICATION','JOINT_TECHNICAL_SECRET','JOINT_IP_LICENSE','POST_PROJECT_IMPROVEMENT'}
 assert 'TECHNOLOGY_LICENSE' in c['active_transaction_types']
 assert c['primary_subtype']=='COOPERATIVE_DEVELOPMENT'


def test_same_worker_sale_development_sale_patent_no_stale_state():
 from review_v2.engine import review_contract_v2
 sale='买卖合同\n出卖人：甲公司\n买受人：乙公司\n第一条 甲方向乙方销售设备10台，每台单价100元，总价1000元。\n第二条 设备交付后所有权转移至乙方。'
 patent=(Path(__file__).parent/'fixtures/round33_patent_transfer.txt').read_text(encoding='utf8')
 reports=[review_contract_v2(t,'sale',use_llm=False) for t in (sale,TEXT,sale,patent)]
 assert [r['contract_type'] for r in reports]==['sale','technology','sale','technology']
 for report in (reports[0],reports[2]):
  assert not any(i['item_id'].startswith('TC-') for i in report['items'])
 for report in (reports[1],reports[3]):
  assert not any(i['item_id'].startswith('S-') for i in report['items'])
 assert {i['item_id']:i['coverage_status'] for i in reports[0]['items']}=={i['item_id']:i['coverage_status'] for i in reports[2]['items']}
 assert reports[1]['deterministic_analysis']['technology_classification']['primary_subtype']=='COOPERATIVE_DEVELOPMENT'
 assert reports[3]['deterministic_analysis']['technology_classification']['tertiary_subtype']=='PATENT_RIGHT_TRANSFER'
 assert reports[1]['release_quality_gate']['status']=='REPORT_READY'

 # Full registries and theme sets must rebuild, not merely the displayed label.
 assert reports[0]['contract_facts']==reports[2]['contract_facts']
 assert sorted(i['risk_group'] for i in reports[0]['risk_themes'])==sorted(i['risk_group'] for i in reports[2]['risk_themes'])
 assert not any(k.startswith('technology.cooperative.') for k in reports[2]['contract_facts']['facts'])
 assert any(k.startswith('technology.cooperative.') for k in reports[1]['contract_facts']['facts'])
 assert not any(k.startswith('technology.cooperative.') for k in reports[3]['contract_facts']['facts'])
