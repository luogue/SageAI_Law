from copy import deepcopy
from types import SimpleNamespace

from review_v2.clause_parser import parse_contract_clauses
from review_v2.contract_facts import extract_contract_fact_graph
from review_v2.risk_fact_layers import project, validate, SLOTS


def fixture():
    text = '若因乙方原因导致迟延交付，每迟延一天，乙方应按照合同总金额的0.2%向甲方支付违约金。'
    graph = extract_contract_fact_graph(parse_contract_clauses(text))
    fact = graph.matching(['liability.penalty'])[0]
    source = {'element_id': 'penalty_obligation_1', 'status': 'ADVERSE',
              'source_fact_key': fact.fact_id, 'canonical_fact_keys': [fact.fact_id]}
    composite = {'element_id': 'evaluation', 'status': 'COVERED', 'claim_id': 'RULE-ADVERSE-CLAIM'}
    item = SimpleNamespace(item_id='RULE', coverage_elements=[source, composite], decision_trace={
        'liquidated_damages_direction': {'review_party_side': 'PARTY_A'},
        'liquidated_damages_calibration': {'high_daily_penalties': [{'source_text': text, 'potentially_excessive': True}]}})
    row = {'evidence_id': 'direct-report', 'source_type': 'BODY', 'source_fact_key': fact.fact_id,
           'supporting_element_ids': ['penalty_obligation_1'], 'supporting_review_ids': ['RULE'], 'quoted_text': text}
    finding = SimpleNamespace(source_review_ids=['RULE'], evidence_bundle={'items': [row]},
                              legal_basis=[{'article': '585'}], final_adverse_elements=[dict(source)])
    project([item], [finding], graph)
    return item, finding, source, composite


def test_three_layers_reuse_published_report_evidence():
    item, finding, source, composite = fixture()
    assert len(source['fact_elements']) == len(SLOTS)
    assert source['orientation']['value'] == 'BENEFIT'
    assert source['evaluation']['high_penalty']
    assert composite['semantic_layer'] == 'EVALUATION'
    assert not validate(item, source, finding.evidence_bundle['items'])[0]
    assert not validate(item, composite, finding.evidence_bundle['items'])[0]
    assert finding.final_adverse_elements[0]['fact_elements'] == source['fact_elements']


def test_package_presence_cannot_replace_explicit_slot_binding():
    item, finding, source, _ = fixture()
    source['fact_elements'][0]['bound_evidence_ids'] = []
    assert 'SOURCE_SLOT_WITHOUT_DIRECT_REPORT_EVIDENCE' in validate(item, source, finding.evidence_bundle['items'])[0]


def test_wrong_target_and_wrong_source_value_block():
    item, finding, source, _ = fixture()
    rows = deepcopy(finding.evidence_bundle['items'])
    rows[0]['supporting_element_ids'] = ['unrelated']
    assert validate(item, source, rows)[0]
    source['fact_elements'][0]['value'] = '丙方'
    assert validate(item, source, finding.evidence_bundle['items'])[0]


def test_orientation_requires_context_and_correct_beneficiary():
    item, finding, source, _ = fixture()
    source['orientation']['value'] = 'BURDEN'
    assert 'ORIENTATION_WITHOUT_CONTEXT_PROVENANCE' in validate(item, source, finding.evidence_bundle['items'])[0]


def test_evaluation_requires_rule_parameter_and_legal_provenance():
    item, finding, source, composite = fixture()
    source['evaluation']['provenance']['legal_basis'] = []
    assert 'EVALUATION_WITHOUT_LEGAL_PROVENANCE' in validate(item, source, finding.evidence_bundle['items'])[0]
    composite['provenance']['source_fact_keys'] = ['unadopted-candidate']
    assert validate(item, composite, finding.evidence_bundle['items'])[0]


def test_unadopted_package_candidates_do_not_become_final_facts():
    item, finding, source, _ = fixture()
    finding.evidence_bundle['items'].append({'evidence_id': 'candidate', 'quoted_text': '其他违约金'})
    assert len([e for e in item.coverage_elements if e.get('semantic_layer') == 'SOURCE_FACT']) == 1
    assert all(s['bound_evidence_ids'] == ['direct-report'] for s in source['fact_elements'])


def test_real_narrative_gate_blocks_missing_layer_provenance():
    from review_v2.narrative_evidence import narrative_evidence_gate
    item, finding, source, composite = fixture()
    item.risk_point_description = item.reasoning_summary = ''
    item.narrative_state = {}
    finding.finding_id, finding.issue = 'finding', ''
    assert narrative_evidence_gate([item], [finding])['mismatch_count'] == 0
    source['fact_elements'][0]['bound_evidence_ids'] = []
    result = narrative_evidence_gate([item], [finding])
    assert result['status'] == 'BLOCKED'
    assert any(row['reject_reason'] == 'SOURCE_SLOT_WITHOUT_DIRECT_REPORT_EVIDENCE'
               for row in result['risk_fact_layers'])
