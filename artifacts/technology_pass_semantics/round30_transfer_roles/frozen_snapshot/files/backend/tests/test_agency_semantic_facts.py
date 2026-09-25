from pathlib import Path
import pytest
from review_v2.agency_facts import prerequisite,specs
from review_v2.lease_semantics import corpus_facts
from review_v2.clause_parser import parse_contract_clauses
from review_v2.penalty_base import analyze
from review_v2.engine import review_contract_v2

@pytest.mark.parametrize('base',['逾期未付款项','应付款项','未付款项','已收款','实际损失'])
def test_dynamic_bases(base):
    assert analyze(f'按照{base}每日0.05%的标准支付违约金。')[0]['status']=='DETERMINABLE'

def test_unknown_base_stays_unknown():
    assert analyze('按照项目权益基数的5%支付违约金。')[0]['status']=='UNDEFINED'

@pytest.mark.parametrize('text,active',[
 ('固定服务报酬为50000元。',False),('本合同为有偿委托。',False),('本合同为无偿委托。',True)])
def test_paid_gate(text,active):
    assert prerequisite(text,'agency_unpaid_intent_gross_standard')[0] is active

@pytest.mark.parametrize('text,active',[
 ('受托人不得擅自转委托第三人。',False),('受托人以自己名义与第三人签订合同。',True)])
def test_hidden_gate(text,active):
    for node in ['agency_disclose_principal','agency_disclose_third_party','agency_third_party_choice_right']:
        assert prerequisite(text,node)[0] is active

def test_parent_condition_cannot_cross_next_subsection():
    s=specs()['agency_unfinished_no_trustee_fault_remuneration']
    text='第四条 报酬\n（一）不可归责于受托人的原因不能完成事务。\n（二）因受托人违约时按以下结算：\n1.报酬按实际履行月份比例计算。'
    assert not corpus_facts(parse_contract_clauses(text),s)[s[0]['element_id']]

def test_paraphrased_mandate():
    text='''委托合同
委托人委托受托人处理商户运营事务。
双方自愿协商达成本合同。
固定服务报酬为50000元。
第一条 报酬
不可归责于受托人导致事务不能完成时，报酬按已完成工作的比例结算。
第二条 费用
未经批准的费用由受托人自行承担。
第三条 受损
受托人处理事务时因无过错事由受损，有权请求委托人补偿合理损失。
第四条 退出
合同终止时受托人应汇报事务办理结果并交接工作文件；终止后双方结算费用并退还多收报酬。
'''
    r=review_contract_v2(text,'agency',use_llm=False)
    rows={i['item_id']:i for i in r['items']}
    for key in ['A-01-01','A-03-03','A-04-03','A-06-02','A-12-03','A-13-03']:
        assert rows[key]['coverage_status']=='通过',key
        assert rows[key]['evidence_clauses']
    assert rows['A-07-02']['coverage_status']=='不适用'

def test_original_file():
    from layers.input_layer import InputLayer
    p=next((Path(__file__).resolve().parents[2]/'test_data').glob('77 *.docx'))
    r=review_contract_v2(InputLayer()._extract_from_docx_content(p.read_bytes()),'agency',use_llm=False)
    assert len(r['items'])==43
    rows={i['item_id']:i for i in r['items']}
    for k in ['A-01-01','A-03-03','A-04-03','A-06-02','A-12-03','A-13-03','COMMON-20-01']:
        assert rows[k]['coverage_status']=='通过',k
    for k in ['A-01-02','A-07-02','A-11-02']:
        assert rows[k]['coverage_status']=='不适用'
    assert r['release_quality_gate']['status']=='REPORT_READY',r['release_quality_gate']['failures']
