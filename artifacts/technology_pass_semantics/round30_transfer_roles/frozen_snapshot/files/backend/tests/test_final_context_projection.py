from copy import deepcopy
from pathlib import Path
from types import SimpleNamespace
import pytest
from docx import Document
from review_v2.engine import (review_contract_v2, _synchronize_evidence_support_to_final_elements,
    _context_deficit_description, _requirement_source_entailment_failures)

@pytest.fixture(scope='module')
def report():
    p=Path(__file__).resolve().parents[2]/'test_data/54 抵押合同.docx'
    return review_contract_v2('\n'.join(p.text for p in Document(p).paragraphs),'mortgage',use_llm=False)

def test_external_pending_preserves_contract_truth_and_quote(report):
    i=next(i for i in report['items'] if i['item_id']=='SEC-04-01')
    assert i['applicability']['applicable'] is True
    assert i['coverage_status']=='INSUFFICIENT_CONTEXT'
    assert i['coverage_elements'][0]['status']=='COVERED'
    quote=i['coverage_elements'][0]['source_spans'][0]
    assert quote in i['citation']['original_excerpt'] and quote in report['result']
    assert i['narrative_state']['covered_elements']
    assert '外部事实尚未核验' in i['narrative_state']['judgment']
    assert '是否适用' not in i['narrative_state']['judgment']
    manual=next(m for m in report['manual_review_items'] if m['item_id']=='SEC-04-01')
    assert '外部事实尚未核验' in manual['review_instruction']

def test_bound_later_sentence_survives_first_sentence_projection(report):
    i=next(i for i in report['items'] if i['item_id']=='S-00-01')
    assert '签字或盖章后生效' in i['citation']['original_excerpt']
    assert not _requirement_source_entailment_failures([SimpleNamespace(**i)],[])
    broken=deepcopy(i)
    broken['evidence_clauses'][0]['quote']='合同各方已理解合同内容。'
    failures=_requirement_source_entailment_failures([SimpleNamespace(**broken)],[])
    assert failures
    assert {'rule_id','element_id','final_element_status','bound_evidence_id','report_fact'} <= failures[0].keys()

def test_source_binding_repair_is_independent_of_rule_number():
    full='当事人确认阅读。双方签字后生效。'
    item=SimpleNamespace(coverage_elements=[dict(element_id='custom',status='COVERED',evidence_ids=['c9'],
        source_clause_ids=['c9'],source_spans=[full],proposition='生效条件')],
        evidence_clauses=[dict(clause_id='c9',text=full,raw_text=full,quote='当事人确认阅读。')])
    _synchronize_evidence_support_to_final_elements(item)
    assert item.evidence_clauses[0]['quote']==full

def test_optional_candidate_is_not_final_action_without_recommendation(report):
    i=next(i for i in report['items'] if i['item_id']=='S-00-03')
    assert i['action_priority']=='NONE'
    assert i['decision_trace']['candidate_action_priority']=='C_OPTIMIZATION'
    assert not i['decision_trace']['recommendation_display_state']['has_active_recommendation']
    assert report['risk_theme_summary']['optional_improvement']==0

def test_final_gate_passes_with_no_suppressed_failure(report):
    assert report['release_quality_gate']['status']=='REPORT_READY'
    assert not report['release_quality_gate']['failures']

def test_gate_rejects_removed_quote_and_applicability_template(report):
    from review_v2.final_context_consistency import verify
    row=next(i for i in report['items'] if i['item_id']=='SEC-04-01')
    broken=deepcopy(report)
    broken['result']=broken['result'].replace(row['coverage_elements'][0]['source_spans'][0], '')
    assert verify(broken)['status']=='BLOCKED'
    broken=deepcopy(report)
    broken['result']=broken['result'].replace('该事项适用，但外部事实尚未核验', '无法确认该事项是否适用')
    assert verify(broken)['status']=='BLOCKED'
