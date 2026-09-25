from pathlib import Path
from dataclasses import replace
import pytest
from review_v2.clause_parser import parse_contract_clauses
from review_v2.domain_selection import resolve_domain_selection, domain_selection_consistency_gate
from review_v2.lease_semantics import requirement, corpus_facts
from review_v2.nda_semantics import resolve

GUARANTEE='保证合同\n债权人与债务人签订主合同。保证人承担连带责任保证。保证期间为三年，保证范围包括主债权及利息，承担责任后享有追偿权。'
NDA='披露方：甲公司\n接收方：乙公司\n保密信息是研发资料，接收方仅用于合作评估，不得披露；保密期限三年。合作结束应返还资料并销毁副本。违反保密义务应赔偿损失。'
SECRECY='\n第十二条 保密\n双方对商业秘密承担保密义务，不得披露保密信息。'

@pytest.mark.parametrize('text,expected',[
 (GUARANTEE+SECRECY,'guarantee'),
 ('房屋租赁合同\n出租人与承租人约定租金每月三千元，租赁期限一年，期满返还房屋。'+SECRECY,'house_lease'),
 ('劳动合同\n用人单位聘用劳动者，约定工作岗位和工资，依法缴纳社会保险。'+SECRECY+'知识产权归单位。','labor'),
 ('技术服务合同\n委托乙方提供技术服务，交付技术报告并验收，甲方支付服务费。'+SECRECY,'technology'),
 ('保密协议\n'+NDA,'confidentiality'),
 (NDA,'confidentiality'),
 ('买卖合同\n出卖人向买受人交付设备，买受人支付价款。\n保证人对债务人所欠主债权承担连带责任保证，保证期间一年，享有追偿权。','sale'),
 (GUARANTEE.split('\n',1)[1]+SECRECY,'guarantee'),
])
def test_primary_over_ancillary(text,expected):
    s,domain,routed=resolve_domain_selection('confidentiality' if expected!='confidentiality' else 'sale',text,parse_contract_clauses(text))
    assert routed==expected
    assert s.classification_context['primary_contract_type']==s.selected_domain

def remedy_hits(text):
    specs=resolve('confidentiality_remedies',[requirement('remedy','保密违反的停止侵害或损失赔偿',r'赔偿')],text)
    return corpus_facts(parse_contract_clauses(text),specs)['remedy']

@pytest.mark.parametrize('clause',[
 '违反本保密条款的，应赔偿损失。',
 '泄露保密信息造成损失的，应承担赔偿责任。',
 '未经授权披露保密信息应支付违约金。',
 '任何一方违反第十二条保密义务，应赔偿因此造成的损失。',
 '第十二条 保密违约责任\n违约方应赔偿实际损失。',
])
def test_confidentiality_linked_remedy(clause):
    assert remedy_hits(clause)
    assert resolve_domain_selection('confidentiality',GUARANTEE+'\n'+clause,parse_contract_clauses(GUARANTEE+'\n'+clause))[2]=='guarantee'

@pytest.mark.parametrize('clause',[
 '保证范围包括损害赔偿金。',
 '要求保证人赔偿债权人的实际损失。',
 '第十二条 保密\n不得泄露资料。\n第十三条 违约责任\n保证人应赔偿债权人的损失。',
 '第十二条 保密\n双方应保密。保证人对逾期借款赔偿实际损失。',
 '违反保密义务无需赔偿损失。',
])
def test_unrelated_or_negated_remedy(clause):
    assert not remedy_hits(clause)

def test_gate_blocks_wrong_rule_pack():
    s,_,_=resolve_domain_selection('confidentiality',GUARANTEE,parse_contract_clauses(GUARANTEE))
    assert domain_selection_consistency_gate(s,['NDA-04-01'])['status']=='BLOCKED'
    assert domain_selection_consistency_gate(replace(s,selected_domain='CONFIDENTIALITY'),['NDA-04-01'])['status']=='BLOCKED'

def test_original_guarantee_routing():
    from fastapi import UploadFile
    from layers.input_layer import InputLayer
    from review_v2.engine import review_contract_v2
    from review_v2.user_profile import UserRiskProfile
    p=next((Path(__file__).resolve().parents[2]/'test_data').glob('69 *.docx'))
    with p.open('rb') as f: text=InputLayer().extract_text_from_file(UploadFile(filename=p.name,file=f))
    r=review_contract_v2(text,'confidentiality',use_llm=False,profile=UserRiskProfile.from_dict({'contract_scenario':'保密协议'}))
    assert r['contract_type']=='guarantee'
    assert all(not i['item_id'].startswith(('NDA-','NC-')) for i in r['items'])
    assert r['profile']['contract_scenario']!='保密协议'
    assert r['release_quality_gate']['status']=='REPORT_READY',r['release_quality_gate']['failures']
