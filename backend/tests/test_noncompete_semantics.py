from copy import deepcopy
from types import SimpleNamespace
from pathlib import Path
import pytest
from review_v2.engine import review_contract_v2
from review_v2.clause_parser import parse_contract_clauses
from review_v2.noncompete_semantics import temporal_roles, consistency_failures
from review_v2.lease_semantics import consistency_failures as evidence_gate


def review(text):
    return review_contract_v2(text, 'non_compete', use_llm=False)


def item(result,key):
    return next(i for i in result['items'] if i['item_id']==key)


def test_masked_identity_has_positive_evidence_and_no_negative_audit():
    result=review('甲方：东岭软件有限公司，住所：杭州市文一路18号。乙方：李清，身份证号：33010619920304XXXX。')
    row=item(result,'EMP-01-01')
    assert row['coverage_status']=='通过'
    assert not any(a['result']=='NOT_FOUND' for a in row['decision_trace']['element_absence_searches'])
    bad=deepcopy(row)
    next(a for a in bad['decision_trace']['element_absence_searches'] if a['result']=='FOUND')['result']='NOT_FOUND'
    assert any(f['requirement']=='SEARCH_AUDIT_ELEMENT_CONFLICT' for f in evidence_gate([SimpleNamespace(**bad)]))


@pytest.mark.parametrize('text', ['甲方提前1个月书面通知可解除本竞业限制协议。', '乙方履行离职后竞业限制义务期间，甲方提前2个月书面通知可解除协议。'])
def test_notice_is_not_duration_and_compensation_remains_missing(text):
    result=review(text)
    row=item(result,'NC-02-01')
    assert row['coverage_status']=='缺失'
    assert all(a['result']=='NOT_FOUND' for a in row['decision_trace']['element_absence_searches'])
    assert item(result,'NC-03-01')['coverage_status']=='待核验'
    assert result['release_quality_gate']['status']=='REPORT_READY'


@pytest.mark.parametrize('months',[12,24])
def test_actual_duration_separate_from_notice(months):
    result=review(f'离职后{months}个月承担竞业限制。甲方提前1个月书面通知可解除协议。')
    row=item(result,'NC-02-01')
    assert row['coverage_status']=='部分覆盖'
    covered=[e for e in row['coverage_elements'] if e['status']=='COVERED']
    assert any(e['proposition']=='离职竞业限制期限' for e in covered)
    assert not any('通知' in e['text'] for e in row['evidence_clauses'])


def test_all_temporal_roles_and_definition_scope():
    clauses=parse_contract_clauses('第一条 竞业限制期限为24个月。\n第二条 甲方提前2个月通知解除协议。\n第三条 解除期限为10日。\n第四条 每月支付补偿。\n第五条 违约后5日内支付违约金。')
    roles={r['role'] for r in temporal_roles(clauses)}
    assert {'NONCOMPETE_DURATION','NOTICE_PERIOD','TERMINATION_PERIOD','PAYMENT_CYCLE','BREACH_PERFORMANCE_PERIOD'}<=roles


def test_prerequisite_conflict_gate_blocks_unconditional_pass():
    result=review('竞业限制的地域范围为全国。甲方提前3个月通知可解除本协议。')
    rows=[SimpleNamespace(**deepcopy(i)) for i in result['items']]
    consumer=next(i for i in rows if i.item_id=='NC-03-01')
    assert consumer.coverage_status=='待核验'
    consumer.coverage_status='通过'
    consumer.coverage_elements=[]
    consumer.needs_manual_review=False
    assert any(f['requirement']=='CROSS_RULE_PREREQUISITE_CONFLICT' for f in consistency_failures(rows))


def test_direct_adverse_not_lost_to_uncertainty():
    result=review('所有员工均须承担竞业限制。')
    assert item(result,'NC-03-01')['coverage_status']=='风险条款'


def test_actual_file_uses_actual_term_and_compensation():
    from docx import Document
    source=Path(__file__).resolve().parents[2]/'test_data/60 竞业限制协议.docx'
    result=review('\n'.join(p.text for p in Document(source).paragraphs))
    assert len(result['items'])==6
    assert item(result,'EMP-01-01')['coverage_status']=='通过'
    assert item(result,'NC-02-01')['coverage_status']=='通过'
    assert item(result,'NC-03-01')['coverage_status']=='待核验'
    assert result['release_quality_gate']['status']=='REPORT_READY'


def test_region_presence_does_not_prove_business_scope_or_proportionality():
    result=review('竞业限制的地域范围为全国。')
    scope=item(result,'NC-01-01')
    covered=[e['proposition'] for e in scope['coverage_elements'] if e['status']=='COVERED']
    assert covered==['明确约定竞业地域范围']
    assert not any('相称' in text for text in covered)
    assert item(result,'NC-03-01')['coverage_status']=='待核验'
    assert result['release_quality_gate']['status']=='REPORT_READY'


def test_sufficient_context_allows_assessment_without_equating_presence_to_reasonableness():
    result=review('乙方担任研发工程师。乙方实际接触公司的商业秘密。公司实际业务范围为工业控制软件研发。'
                  '竞业限制业务范围为工业控制软件研发。竞业限制地域范围为江苏省。'
                  '离职后12个月承担竞业限制。离职后每月支付补偿金人民币6000元。')
    consumer=item(result,'NC-03-01')
    assert consumer['decision_trace']['reasonableness_context']['ready_for_assessment']
    assert not any('相称' in e['proposition'] for e in item(result,'NC-01-01')['coverage_elements'])


def test_each_covered_element_is_rendered_with_its_own_proof():
    from review_v2.report_presentation import render_element_citations
    result=review('离职后24个月承担竞业限制。\n第二条 离职后每月支付补偿金人民币6000元。')
    row=item(result,'NC-02-01')
    assert row['coverage_status']=='通过'
    citations=row['presentation']['element_citations']
    assert any('24个月' in r['quoted_text'] for r in citations)
    assert any('6000元' in r['quoted_text'] for r in citations)
    rendered='\n'.join(render_element_citations(SimpleNamespace(**row)))
    assert '24个月' in rendered and '6000元' in rendered
    assert all(e['element_id'] in {k for r in citations for k in r['supporting_element_ids']}
               for e in row['coverage_elements'] if e['status']=='COVERED')


def test_two_covered_elements_with_only_one_proof_are_blocked():
    result=review('离职后24个月承担竞业限制。离职后每月支付补偿金人民币6000元。')
    row=deepcopy(item(result,'NC-02-01'))
    row['evidence_clauses']=[e for e in row['evidence_clauses'] if '6000元' not in e['text']]
    failures=evidence_gate([SimpleNamespace(**row)])
    assert any(f['requirement']=='SHARED_ELEMENT_EVIDENCE_CONFLICT' for f in failures)


def test_injected_proportionality_claim_conflicting_with_pending_review_is_blocked():
    result=review('竞业限制地域范围为华东地区。')
    rows=[SimpleNamespace(**deepcopy(i)) for i in result['items']]
    scope=next(i for i in rows if i.item_id=='NC-01-01')
    next(e for e in scope.coverage_elements if e['status']=='COVERED')['proposition']='与秘密保护相称的范围'
    assert any(f['requirement']=='REASONABLENESS_WITHOUT_PREREQUISITE_FACTS' for f in consistency_failures(rows))
