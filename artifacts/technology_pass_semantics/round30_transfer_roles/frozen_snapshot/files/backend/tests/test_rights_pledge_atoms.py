import pytest
from review_v2.security_property_checklist import RIGHTS_PLEDGE_CHECKLIST
from review_v2.priority_checklist_helpers import PROFILES
from review_v2.security_context import resolve
from review_v2.lease_semantics import corpus_facts
from review_v2.clause_parser import parse_contract_clauses
from review_v2.sale_evidence import PROFILES as COMMON, supports

@pytest.mark.parametrize('node,index,text',[
 ('pledge_rights_asset',0,'出质人将其应收账款提供质押担保。'),
 ('pledge_rights_asset',0,'本合同质押标的为应收账款。'),
 ('pledge_rights_asset',1,'基础合同编号：SA-2048。'),
 ('pledge_rights_asset',2,'付款义务人为：某采购公司。'),
 ('pledge_rights_asset',3,'应收账款金额为人民币230000元。'),
 ('pledge_rights_asset',4,'应收账款到期日为2030年3月1日。'),
 ('pledge_rights_publicity',0,'应收账款质押登记由质权人办理。'),
 ('pledge_rights_publicity',1,'应收账款质押登记由质权人办理。'),
 ('pledge_rights_publicity',1,'出质人负责办理应收账款质押登记。'),
 ('pledge_rights_publicity',2,'通过统一登记公示系统申请登记。'),
 ('pledge_rights_publicity',3,'期限届满前应申请展期登记。'),
 ('pledge_rights_publicity',4,'合同签署后三个工作日内完成应收账款质押登记。'),
 ('pledge_rights_publicity',5,'质权人应提供登记凭证。'),
 ('security_title_authority',0,'出质人（以下简称乙方）：某公司。乙方以其享有的应收账款提供质押担保。'),
])
def test_independent_positive_atoms(node,index,text):
 specs=resolve(node,PROFILES[node],text);spec=specs[index]
 assert corpus_facts(parse_contract_clauses(text),[spec])[spec['element_id']]

@pytest.mark.parametrize('text', ['公司信息变更后七日内书面通知对方。','乙方应通知甲方。','发生违约后应书面通知。'])
def test_specific_notice_is_not_general_service(text):
 assert not any(supports(e,text) for e in COMMON['common_notice_delivery'])

def test_complete_general_service():
 text='本合同首部地址作为通知送达地址。所有通知应采用快递或电子邮件。地址变更应书面通知对方。拒收视为送达。'
 assert all(supports(e,text) for e in COMMON['common_notice_delivery'])

@pytest.mark.parametrize('node,index,text',[
 ('security_title_authority',0,'出质人不享有应收账款。'),
 ('pledge_rights_publicity',0,'应收账款质押无需办理登记。'),
 ('pledge_rights_publicity',4,'信息变更后七日内完成变更登记。'),
 ('pledge_rights_publicity',5,'应收账款质押登记由质权人办理。'),
 ('pledge_rights_publicity',1,'出质人应当提供办理质押登记所需的信息。'),
 ('pledge_rights_publicity',1,'乙方应配合甲方办理质押登记。'),
 ('pledge_rights_asset',1,'本合同为质押担保合同编号ZY-123的补充协议。'),
])
def test_related_fact_does_not_prove_other_atom(node,index,text):
 spec=resolve(node,PROFILES[node],text)[index]
 assert not corpus_facts(parse_contract_clauses(text),[spec])[spec['element_id']]

@pytest.mark.parametrize('body,node,expected',[
 ('出质人以其享有的应收账款提供质押担保。','pledge_rights_asset',[True,False,False,False,False]),
 ('应收账款质押登记由质权人办理。','pledge_rights_publicity',[True,True,True,False,False,False]),
])
def test_atomic_partial_preserves_found(body,node,expected):
 specs=resolve(node,PROFILES[node],body)
 first=corpus_facts(parse_contract_clauses(body),specs)
 assert [bool(first[s['element_id']]) for s in specs]==expected
 assert first==corpus_facts(parse_contract_clauses(body),specs)
 assert any(first.values()) and not all(first.values())

@pytest.mark.parametrize('body,rule_id,status',[
 ('出质人以其享有的应收账款提供质押担保。','RPL-01-01','部分覆盖'),
 ('应收账款质押登记由质权人办理。','RPL-02-01','部分覆盖'),
 ('公司信息变更后七日内书面通知对方。','S-00-03','缺失'),
 ('本合同首部地址作为通知送达地址。所有通知应采用快递或电子邮件。地址变更应书面通知对方。拒收视为送达。','S-00-03','通过'),
])
def test_final_engine_consumes_atomic_states(body,rule_id,status):
 from review_v2.engine import review_contract_v2
 report=review_contract_v2('应收账款质押合同\n第一条\n'+body,'rights_pledge',use_llm=False)
 item=next(i for i in report['items'] if i['item_id']==rule_id)
 assert item['coverage_status']==status
 for element in item['coverage_elements']:
  if element['status']=='COVERED':
   assert element['evidence_ids']
   assert element['proposition'] not in item['risk_point_description']
 assert report['release_quality_gate']['status']=='REPORT_READY',report['release_quality_gate']['failures']
