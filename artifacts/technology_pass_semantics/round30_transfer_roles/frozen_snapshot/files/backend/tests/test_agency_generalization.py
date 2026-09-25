"""Different syntax, polarity and deliberately unrelated evidence."""
from copy import deepcopy
from pathlib import Path
from types import SimpleNamespace
import pytest
from review_v2.agency_facts import specs
from review_v2.clause_parser import parse_contract_clauses
from review_v2.lease_semantics import corpus_facts, supports
from review_v2.engine import review_contract_v2, _search_final_element
from review_v2.semantic_consistency import validate


COMMERCIAL = '''商业委托协议
委托人：青松贸易有限公司
受托人：远帆咨询有限公司
第一条 工作
受托人接受委托人的委托，负责办理供应商调查工作，整理调查报告并辅助谈判；最终交易由委托人决定。
双方自愿签订本协议。各方具备民事行为能力，已经取得签约授权。
第二条 报酬
本合同为有偿委托。固定服务费为24000元，交付报告后十日内支付。
因不可归责于受托人致使事务不能完成的，按实际完成工作的比例支付服务费。
第三条 费用
受托人代垫的必要费用由委托人偿还。代垫费用不计利息。
第四条 退出
任何一方均可终止委托，应事先书面通知另一方。
因解除造成损失的，解除方应赔偿直接损失及合同履行后可以获得的利益。
合同终止后，受托人应提交结项报告，并移交文件和财产；终止后双方结算服务费及必要费用。
第五条 权限
受托人超出授权范围给委托人造成损失的，受托人应承担赔偿责任。
'''


def hits(node, text):
    requirements = specs()[node]
    return corpus_facts(parse_contract_clauses(text), requirements)


@pytest.mark.parametrize('text', [
    '双方均有权随时解除本合同。',
    '任何一方均可终止委托。',
    '委托人、受托人有权提前结束委托关系。',
    '根据法律规定，委托人和受托人均有权依法随时解除本合同。'])
def test_mutual_exit_paraphrases(text):
    assert hits('agency_arbitrary_termination',text)['mandate_mutual_exit']


@pytest.mark.parametrize('text',[
    '只有委托人有权解除合同。',
    '因不可抗力导致合同无法履行的，任何一方均有权解除合同。',
    '双方不得随时解除本合同。',
    '解除合同须经双方一致同意。',
    '任何一方违约时，另一方有权解除合同。'])
def test_conditional_or_negated_exit_not_mutual_discretion(text):
    assert not hits('agency_arbitrary_termination',text)['mandate_mutual_exit']


@pytest.mark.parametrize('node,text,element',[
    ('agency_unfinished_no_trustee_fault_remuneration','不可归责于受托人导致事务不能完成的，委托人按已经实际完成工作的比例支付委托费用。','mandate_proportional_remuneration'),
    ('agency_unfinished_no_trustee_fault_remuneration','因不可归责于乙方的原因解除合同，服务费根据实际履行月份据实结算。','mandate_proportional_remuneration'),
    ('agency_contract_type_identification','委托人委托受托人依本协议处理日常运营事务。','mandate_relationship'),
    ('agency_contract_type_identification','乙方接受甲方委托，负责办理采购事项。','mandate_relationship'),
    ('agency_final_report_after_termination','解除后十日内受托人提交截至解除日的工作报告。','mandate_final_report'),
    ('agency_final_report_after_termination','本合同终止时乙方应汇报事务处理结果。','mandate_final_report'),
    ('agency_termination_handover','终止本协议后返还财产、资料及工作文件。','mandate_exit_handover'),
    ('agency_expense_reimbursement_interest','受托人代垫支出按年利率3%计算利息。','mandate_advance_interest'),
    ('agency_expense_reimbursement_interest','垫付费用无需支付利息。','mandate_advance_interest'),
    ('agency_over_authority_liability','受托人超越委托权限造成委托人损失的，受托人应赔偿损失。','mandate_unauthorized_liability'),
    ('agency_over_authority_liability','乙方超越甲方授权范围，擅自签订合同造成甲方损失的，应当承担赔偿责任。','mandate_unauthorized_liability'),
    ('agency_termination_compensation_scope','因解除合同造成损失的，解除方应赔偿损失。本合同为有偿委托，赔偿包括合同履行后可以获得的合理利益。','mandate_exit_profit_scope'),
])
def test_composed_positive_relations(node,text,element):
    assert hits(node,text)[element]


@pytest.mark.parametrize('node,text,element',[
    ('agency_expense_reimbursement_interest','解除后结算已付委托费用和必要费用。','mandate_advance_interest'),
    ('agency_expense_reimbursement_interest','附件四：费用预算及报销标准。','mandate_expense_repayment'),
    ('agency_expense_reimbursement_interest','受托人申请报销时应提供合法有效的发票。','mandate_expense_repayment'),
    ('agency_expense_reimbursement_interest','委托人逾期支付服务费时承担利息。','mandate_advance_interest'),
    ('agency_over_authority_liability','因解除时间不当造成对方损失的，解除方应承担赔偿责任。','mandate_unauthorized_liability'),
    ('agency_over_authority_liability','受托人不得超越委托权限。','mandate_unauthorized_liability'),
    ('agency_affair_scope','全权委托：不适用。','mandate_affair_scope'),
    ('agency_contract_type_identification','委托合同。委托人。受托人。','mandate_relationship'),
    ('agency_final_report_after_termination','受托人每周提交工作报告。','mandate_final_report'),
    ('agency_unfinished_no_trustee_fault_remuneration','因受托人故意违约致使委托不能完成，仍按实际完成工作比例支付报酬。','mandate_proportional_remuneration'),
    ('agency_termination_handover','第一条 交货\n货物交接完成后双方结算费用。','mandate_exit_settlement'),
    ('agency_unfinished_no_trustee_fault_remuneration','因不可归责于委托人导致事务不能完成的，按实际完成工作比例支付报酬。','mandate_proportional_remuneration'),
    ('agency_unfinished_no_trustee_fault_remuneration','因不可归责于受托人导致事务不能完成的，无需支付与实际完成工作比例相应的报酬。','mandate_proportional_remuneration'),
    ('agency_final_report_after_termination','解除后受托人无需提交工作报告。','mandate_final_report'),
    ('agency_contract_type_identification','委托人不委托受托人处理事务。','mandate_relationship'),
    ('agency_over_authority_liability','受托人超越委托权限造成损失的，受托人无需承担赔偿责任。','mandate_unauthorized_liability'),
])
def test_unrelated_or_incomplete_relations(node,text,element):
    assert not hits(node,text)[element]


def test_audit_and_matcher_share_parent_context():
    text='第四条 报酬\n（一）因不可归责于乙方导致合同解除。\n1.固定服务报酬按照实际履行月份比例计算。'
    req=specs()['agency_unfinished_no_trustee_fault_remuneration'][0]
    clauses=parse_contract_clauses(text)
    item=SimpleNamespace(item_id='TEST',node_id='test',decision_trace={'semantic_requirements':[req]})
    audit=_search_final_element(item,req,clauses)
    assert audit['result']=='FOUND'
    assert any(r['accepted'] and r.get('semantic_parent_context_id') for r in audit['top_k_candidates'])
    assert audit['supporting_evidence']==corpus_facts(clauses,[req])[req['element_id']]


def test_exit_settlement_uses_explicit_handover_antecedent():
    text='第三条 结束\n（1）解除本合同后受托人完成财产交接。\n（2）交接完成后双方结算服务费。'
    assert hits('agency_termination_handover',text)['mandate_exit_settlement']


@pytest.fixture(scope='module')
def commercial_result():
    return review_contract_v2(COMMERCIAL,'agency',use_llm=False)


def test_short_commercial_end_to_end(commercial_result):
    rows={i['item_id']:i for i in commercial_result['items']}
    for key in ['A-01-01','A-01-03','A-02-01','A-03-03','A-04-02','A-07-03','A-12-01','A-12-02','A-12-03','A-13-03']:
        assert rows[key]['coverage_status']=='通过',key
    assert commercial_result['release_quality_gate']['status']=='REPORT_READY'


@pytest.mark.parametrize('corruption',['wrong_quote','wrong_location','false_missing','false_audit','false_pass'])
def test_publication_gate_rejects_corruption(commercial_result,corruption):
    row=deepcopy(next(i for i in commercial_result['items'] if i['item_id']=='A-12-01'))
    item=SimpleNamespace(**row)
    if corruption=='wrong_quote':
        item.evidence_clauses[0]['quote']='受托人每周报告。'
    elif corruption=='wrong_location':item.evidence_clauses[0]['location']='第一条'
    elif corruption=='false_missing':item.coverage_elements[0]['status']='MISSING'
    elif corruption=='false_audit':
        item.decision_trace['element_absence_searches']=[{'element_id':'mandate_mutual_exit','result':'NOT_FOUND'}]
    else:item.evidence_clauses=[]
    assert validate([item],parse_contract_clauses(COMMERCIAL))['status']=='BLOCKED'


def test_current_file_element_binding():
    from layers.input_layer import InputLayer
    p=next((Path(__file__).resolve().parents[2]/'test_data').glob('80 *.docx'))
    text=InputLayer()._extract_from_docx_content(p.read_bytes())
    r=review_contract_v2(text,'agency',use_llm=False)
    rows={i['item_id']:i for i in r['items']}
    for key in ['A-01-01','A-01-03','A-03-03','A-07-03','A-12-01','A-12-03','A-13-03']:
        assert rows[key]['coverage_status']=='通过',key
    assert rows['A-04-02']['coverage_status']=='部分覆盖'
    assert rows['A-12-02']['coverage_status']=='通过'
    assert '超越委托权限' in str(rows['A-07-03']['evidence_clauses'])
    assert all('不适用' not in e['text'] for e in rows['A-02-01']['evidence_clauses'])
    assert len(r['items'])==42
    assert r['release_quality_gate']['status']=='REPORT_READY',r['release_quality_gate']['failures']
