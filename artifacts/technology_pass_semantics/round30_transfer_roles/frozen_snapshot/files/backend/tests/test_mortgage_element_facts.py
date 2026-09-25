from pathlib import Path
from collections import Counter
import pytest
from docx import Document
from review_v2.clause_parser import parse_contract_clauses
from review_v2.lease_semantics import corpus_facts
from review_v2.security_property_checklist import MORTGAGE_CHECKLIST
from review_v2.priority_checklist_helpers import PROFILES
from review_v2.engine import review_contract_v2
from review_v2.report_statistics import coverage_bucket

@pytest.mark.parametrize('text', [
    '本合同自签订后三日内，抵押双方当事人应持不动产权证及其他相关证件到不动产登记机构办理不动产抵押登记手续。',
    '抵押人应于签约后5个工作日内完成抵押登记。',
    '在合同生效后十天以内，双方当事人共同申请抵押登记。',
])
def test_registration_role_deadline_order_and_chinese_numerals(text):
    spec=PROFILES['mortgage_publicity'][0]
    assert corpus_facts(parse_contract_clauses(text),[spec])[spec['element_id']]

@pytest.mark.parametrize('text', [
    '贷款人应在借款人偿还全部款项后三日内协同抵押人到不动产登记机构办理抵押注销登记。',
    '借款本息全部清偿完毕后，债权人应配合办理注销抵押登记。',
    '债务人结清所有债务后，抵押权人应在五个工作日内办理抵押注销登记。',
])
def test_discharge_equivalent_expressions(text):
    spec=PROFILES['security_exercise_period'][1]
    assert corpus_facts(parse_contract_clauses(text),[spec])[spec['element_id']]

@pytest.mark.parametrize('text', [
    '双方应办理抵押登记。',
    '三日内借款人应还款。双方应办理抵押登记。',
    '双方应于三日内办理抵押注销登记。',
    '双方在三日内无需办理抵押登记。',
])
def test_registration_requires_same_event_complete_facts(text):
    spec=PROFILES['mortgage_publicity'][0]
    assert not corpus_facts(parse_contract_clauses(text),[spec])[spec['element_id']]

def test_full_mortgage_final_elements_and_absence_audit_agree():
    path=Path(__file__).resolve().parents[2]/'test_data/54 抵押合同.docx'
    text='\n'.join(p.text for p in Document(path).paragraphs)
    results=[review_contract_v2(text,'mortgage',use_llm=False) for _ in range(2)]
    r=results[0]; by={i['item_id']:i for i in r['items']}
    assert by['MTG-02-01']['coverage_status']=='通过'
    assert next(e for e in by['SEC-06-01']['coverage_elements'] if e['element_id']=='security_exercise_period_2')['status']=='COVERED'
    for item in r['items']:
        found={e['element_id'] for e in item['coverage_elements'] if e['status']=='COVERED'}
        missing={e['element_id'] for e in item['coverage_elements'] if e['status']=='MISSING'}
        audits=item['decision_trace'].get('element_absence_searches',[])
        assert not found & {a['element_id'] for a in audits if a['result']=='NOT_FOUND'}
        for a in audits:
            assert a['element_id'] in (missing if a['result']=='NOT_FOUND' else found)
            assert a['searched_clause_ids']
            if a.get('search_mode')=='SEMANTIC_REQUIREMENT':
                assert a['search_corpus_chunks']
    assert dict(Counter(coverage_bucket(i['coverage_status']) for i in r['items']))==r['coverage_summary']
    core=lambda report:[(i['item_id'],i['coverage_status'],i['coverage_elements']) for i in report['items']]
    assert core(results[0])==core(results[1])
