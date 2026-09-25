from types import SimpleNamespace
from review_v2.clause_parser import parse_contract_clauses
from review_v2.contract_facts import extract_contract_fact_graph
from review_v2.development_exit import development_exit_elements
from review_v2.penalty_fact_binding import bind, gate

TEXT = '3. 技术成果交付\n若因乙方原因导致迟延交付，每迟延一天，乙方应按照合同总金额的0.1%向甲方支付违约金。'


def test_shared_identity_and_development_coverage():
    clauses = parse_contract_clauses(TEXT)
    graph = extract_contract_fact_graph(clauses)
    fact = graph.matching(['liability.penalty'])[0]
    assert fact.value['base'] == '合同总金额'
    assert fact.value['obligor'] == '乙方'
    assert fact.value['period'] == '每迟延一天'
    assert fact.fact_id == extract_contract_fact_graph(clauses).matching(['liability.penalty'])[0].fact_id
    exit_element = next(e for e in development_exit_elements(clauses) if e['element_id'] == 'development_delay_liability')
    assert exit_element['status'] == 'COVERED'
    items = [SimpleNamespace(item_id=rule, evidence_clauses=[], coverage_elements=[{
        'element_id': rule + '_element', 'status': 'COVERED',
        'proposition': '违约金约定',
        'supporting_evidence': [{'clause_id': fact.source_clause_ids[0], 'quote': fact.value['raw_clause']}],
    }]) for rule in ['TC-05-04', 'COMMON-20-01', 'GEN-LIAB-03']]
    bind(items, graph)
    assert all(i.coverage_elements[0]['source_fact_key'] == fact.fact_id for i in items)
    for item in items:
        item.evidence_clauses = [{'source_fact_key': fact.fact_id, 'source_type': 'BODY',
            'quoted_text': fact.value['raw_clause'], 'evidence_id': 'direct',
            'supporting_review_ids': [item.item_id],
            'supporting_element_ids': [item.coverage_elements[0]['element_id']]}]
    assert gate(items, [], graph)['status'] == 'PASS'
    items[0].coverage_elements[0]['status'] = 'MISSING'
    conflict = gate(items, [], graph)
    assert conflict['cross_rule_fact_conflict'] == 1
    assert conflict['status'] == 'BLOCKED'
    items[0].coverage_elements[0]['status'] = 'COVERED'
    items[0].evidence_clauses[0]['source_fact_key'] = 'wrong'
    assert gate(items, [], graph)['risk_fact_direct_evidence_mismatch'] == 1


def test_goods_delivery_does_not_imply_development_delay():
    clauses = parse_contract_clauses(TEXT.replace('技术成果交付', '货物运输'))
    element = next(e for e in development_exit_elements(clauses) if e['element_id'] == 'development_delay_liability')
    assert element['status'] == 'MISSING'
