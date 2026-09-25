from pathlib import Path
import pytest
from docx import Document
from review_v2.requirement_kinds import partition
from review_v2.engine import review_contract_v2
from review_v2.report_statistics import statistics_gate
from review_v2.priority_contract_review import judge
from review_v2.security_property_checklist import REALIZE, PERIOD
from review_v2.clause_parser import parse_contract_clauses

def test_kind_is_explicit_not_inferred_from_citation():
    rows=[{'element_id':'x','proposition':'付款安排','legal_basis':'民法典'}]
    contract, others=partition(rows)
    assert contract==rows and not others
    rows[0].update(requirement_kind='STATUTORY_DEFAULT')
    with pytest.raises(ValueError):partition(rows)

@pytest.mark.parametrize('family',['保证','质押','买卖','租赁','抵押'])
def test_partition_does_not_depend_on_rule_or_contract_number(family):
    rows=[{'element_id':family+str(n),'proposition':family,'requirement_kind':kind,
           'statutory_protection':'已核对的直接法定规则','verification_instruction':'核验外部材料'}
          for n,kind in enumerate(['CONTRACT_TERM','STATUTORY_DEFAULT','EXTERNAL_VERIFICATION'])]
    contractual, assessments=partition(rows)
    assert len(contractual)==1
    assert [a['status'] for a in assessments]==['PROTECTED_BY_LAW','PENDING_VERIFICATION']
    assert all(a['contract_coverage_required'] is False for a in assessments)

@pytest.mark.parametrize('rule,text',[
    (PERIOD,'抵押权人放弃行使抵押权。'),
    (REALIZE,'抵押权人无权优先受偿。'),
    (REALIZE,'超额价款归贷款人所有。'),
])
def test_statutory_default_does_not_hide_direct_conflict(rule,text):
    assert judge(rule,parse_contract_clauses(text)).coverage_status=='风险条款'

def test_current_mortgage_drafting_and_diligence_are_separate():
    source=Path(__file__).resolve().parents[2]/'test_data/54 抵押合同.docx'
    text='\n'.join(p.text for p in Document(source).paragraphs)
    r=review_contract_v2(text,'mortgage',use_llm=False)
    by={i['item_id']:i for i in r['items']}
    for key in ['SEC-05-01','SEC-06-01']:
        assert by[key]['coverage_status']=='通过'
        assert by[key]['risk_level']=='低'
        assert by[key]['action_priority']=='NONE'
        assert '付款期限、逾期责任和对账依据' not in by[key]['legal_consequence_if_missing']
    ext=by['SEC-04-01']
    assert ext['coverage_status']=='INSUFFICIENT_CONTEXT'
    assert ext['needs_manual_review'] and ext['risk_level']=='低'
    assert all(e['status']=='COVERED' for e in ext['coverage_elements'])
    assert r['coverage_summary']['待核验']==1
    assert r['risk_finding_summary']['人工复核']==1
    assert statistics_gate(r)['status']=='REPORT_READY'
    assert not any(f['requirement']=='COVERAGE_ELEMENT_STATE_CONFLICT' for f in r['release_quality_gate']['failures'])
