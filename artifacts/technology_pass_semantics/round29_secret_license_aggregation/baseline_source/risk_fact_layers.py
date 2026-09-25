"""Typed provenance for final, adopted canonical facts (not candidate excerpts)."""
from review_v2.penalty_fact_binding import compact

SLOTS = ('obligor', 'beneficiary', 'trigger', 'period', 'rate', 'base', 'consequence')


def project(items, findings, graph):
    registry = {f.fact_id: f for f in graph.matching(['liability.penalty'])}
    for item in items:
        direction = item.decision_trace.get('liquidated_damages_direction')
        if not direction:
            continue
        adopted = []
        for element in item.coverage_elements:
            # Only already selected obligation nodes, not all quotes in a bundle.
            if not element['element_id'].startswith('penalty_obligation_'):
                continue
            fact = registry.get(element.get('source_fact_key'))
            if fact is None:
                continue  # Legacy/unresolved facts remain subject to the old gate.
            element['semantic_layer'] = 'SOURCE_FACT'
            element['fact_elements'] = [
                {'element_key': key, 'value': fact.value[key],
                 'source_fact_key': fact.fact_id} for key in SLOTS]
            adopted.append(element)
        if not adopted:
            continue
        source_keys = list(dict.fromkeys(e['source_fact_key'] for e in adopted))
        for element in item.coverage_elements:
            if element in adopted:
                continue
            if not (set(element.get('canonical_fact_keys', [])) & set(source_keys)
                    or element.get('claim_id') == item.item_id + '-ADVERSE-CLAIM'):
                continue
            element['semantic_layer'] = 'EVALUATION'
            element['provenance'] = {'source_fact_keys': source_keys, 'rule_id': item.item_id}
        for finding in findings:
            if item.item_id not in finding.source_review_ids:
                continue
            rows = finding.evidence_bundle.get('items', [])
            for element in adopted:
                fact = registry[element['source_fact_key']]
                exact = [r for r in rows if r.get('source_fact_key') == fact.fact_id
                         and element['element_id'] in r.get('supporting_element_ids', [])
                         and item.item_id in r.get('supporting_review_ids', [])
                         and r.get('source_type') == 'BODY'
                         and compact(r.get('quoted_text')) == compact(fact.value['raw_clause'])]
                for slot in element['fact_elements']:
                    slot['bound_evidence_ids'] = [r['evidence_id'] for r in exact]
                side = direction.get('review_party_side')
                review_party = {'PARTY_A': '甲方', 'PARTY_B': '乙方'}.get(side)
                element['orientation'] = {
                    'semantic_layer': 'ORIENTATION',
                    'value': ('BENEFIT' if review_party == fact.value['beneficiary'] else
                              'BURDEN' if review_party == fact.value['obligor'] else 'UNKNOWN'),
                    'provenance': {'review_context_key': 'liquidated_damages_direction.review_party_side',
                                   'review_party_side': side, 'source_fact_key': fact.fact_id,
                                   'element_key': 'beneficiary', 'beneficiary': fact.value['beneficiary']}}
                calibration = item.decision_trace.get('liquidated_damages_calibration', {})
                evaluated = [row for key, values in calibration.items() if key.startswith('high_')
                             and isinstance(values, list) for row in values
                             if compact(row.get('source_text')) == compact(fact.value['raw_clause'])]
                element['evaluation'] = {
                    'semantic_layer': 'EVALUATION',
                    'high_penalty': bool(evaluated),
                    'judicial_adjustment_risk': bool(evaluated),
                    'provenance': {'source_fact_key': fact.fact_id, 'rule_id': item.item_id,
                                   'decision_trace_key': 'liquidated_damages_calibration',
                                   'parameter_evaluation': evaluated,
                                   'legal_basis': finding.legal_basis}}
            # Use the existing final-adverse schema, not a parallel risk_facts array.
            by_key = {e['element_id']: e for e in item.coverage_elements}
            for final in finding.final_adverse_elements:
                source = by_key.get(final.get('element_id'))
                if source:
                    for key in ('semantic_layer', 'fact_elements', 'orientation', 'evaluation', 'provenance'):
                        if key in source:
                            final[key] = source[key]


def validate(item, element, sources):
    """Do not treat an evaluation as an assertion in the contract."""
    errors, debug = [], []
    source_nodes = {e.get('source_fact_key'): e for e in item.coverage_elements
                    if e.get('semantic_layer') == 'SOURCE_FACT'}
    if element.get('semantic_layer') == 'EVALUATION':
        provenance = element.get('provenance', {})
        if (provenance.get('rule_id') != item.item_id or not provenance.get('source_fact_keys')
                or any(key not in source_nodes for key in provenance.get('source_fact_keys', []))):
            errors.append('EVALUATION_WITHOUT_SOURCE_PROVENANCE')
        return errors, debug
    slots = element.get('fact_elements', [])
    if {s.get('element_key') for s in slots} != set(SLOTS):
        errors.append('SOURCE_FACT_SLOTS_INCOMPLETE')
    for slot in slots:
        ids = slot.get('bound_evidence_ids', [])
        matches = [r for r in sources if r.get('evidence_id') in ids
                   and r.get('source_type') == 'BODY'
                   and r.get('source_fact_key') == element.get('source_fact_key')
                   and element['element_id'] in r.get('supporting_element_ids', [])
                   and item.item_id in r.get('supporting_review_ids', [])
                   and compact(slot.get('value')) and compact(slot['value']) in compact(r.get('quoted_text'))]
        reason = None if matches else 'SOURCE_SLOT_WITHOUT_DIRECT_REPORT_EVIDENCE'
        if reason:
            errors.append(reason)
        debug.append({'rule_id': item.item_id, 'risk_fact_id': element['element_id'],
                      'source_fact_id': element.get('source_fact_key'),
                      'element_key': slot.get('element_key'), 'canonical_value': slot.get('value'),
                      'direct_report_evidence_id': ids, 'reject_reason': reason,
                      'orientation_provenance': element.get('orientation', {}).get('provenance'),
                      'evaluation_provenance': element.get('evaluation', {}).get('provenance')})
    orientation = element.get('orientation', {})
    origin = orientation.get('provenance', {})
    direction = item.decision_trace.get('liquidated_damages_direction', {})
    party = {'PARTY_A': '甲方', 'PARTY_B': '乙方'}.get(direction.get('review_party_side'))
    values = {s.get('element_key'): s.get('value') for s in slots}
    expected = ('BENEFIT' if party and party == values.get('beneficiary') else
                'BURDEN' if party and party == values.get('obligor') else 'UNKNOWN')
    if (origin.get('source_fact_key') != element.get('source_fact_key')
            or not origin.get('review_context_key')
            or orientation.get('value') != expected
            or origin.get('beneficiary') != values.get('beneficiary')
            or origin.get('review_party_side') != direction.get('review_party_side')):
        errors.append('ORIENTATION_WITHOUT_CONTEXT_PROVENANCE')
    evaluation = element.get('evaluation', {}).get('provenance', {})
    calibration = item.decision_trace.get('liquidated_damages_calibration', {})
    actual_evaluations = [r for k, v in calibration.items() if k.startswith('high_')
                          and isinstance(v, list) for r in v]
    if (evaluation.get('source_fact_key') != element.get('source_fact_key')
            or evaluation.get('rule_id') != item.item_id or not evaluation.get('legal_basis')
            or not evaluation.get('parameter_evaluation')
            or any(r not in actual_evaluations for r in evaluation.get('parameter_evaluation', []))):
        errors.append('EVALUATION_WITHOUT_LEGAL_PROVENANCE')
    return errors, debug
