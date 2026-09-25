"""Bind secret-loss propositions to the original parser corpus."""
from review_v2.verified_source import exact_span


def bind_elements(elements, loss, clauses):
    facts = loss.get('fact_sources', {})
    mapping = {
        'secret_loss_trigger': [row['element_id'] for row in loss.get('trigger_components', [])],
        'future_fee_after_secret_loss': ['future_license_fee_continues', 'future_service_fee_continues',
                                       'royalty_continues', 'fee_stop_or_reduction'],
        'termination_after_secret_loss': ['termination_restricted', 'termination_available'],
    }

    def sources(keys):
        result = []
        for key in keys:
            for fact in facts.get(key, []):
                for clause in clauses:
                    span = exact_span(clause.text, fact['quote'])
                    if span:
                        row = dict(clause_id=clause.clause_id, quote=clause.text[slice(*span)],
                                   location=clause.location, condition=fact['condition'],
                                   arrangement_polarity=fact['arrangement_polarity'],
                                   event_polarity=fact['event_polarity'])
                        context = fact.get('condition_context')
                        if context:
                            row['condition_evidence'] = [
                                dict(clause_id=c.clause_id, quote=c.text[slice(*bound)], location=c.location)
                                for c in clauses if (bound := exact_span(c.text, context))]
                        if row not in result:
                            result.append(row)
                        break
        return result

    result = []
    for element in elements:
        key = element['element_id']
        if key not in mapping and key not in facts:
            result.append(element)
            continue
        rows = sources(mapping.get(key, [key]))
        element = dict(element, supporting_evidence=rows, source_fact_key='secret_loss.' + key,
                       bound_evidence_ids=[r['clause_id'] for r in rows])
        if key == 'secret_loss_trigger':
            # These are alternatives under the existing trigger requirement,
            # not seven new mandatory contractual obligations.
            element.update(component_quantifier='ANY', component_coverage=[
                dict(row, supporting_evidence=sources([row['element_id']]))
                for row in loss.get('trigger_components', [])])
        result.append(element)
    return result


def elements(clauses):
    """Publish arrangement existence, independently of its risk direction."""
    from review_v2.technology_service_analysis import analyze_technical_secret_loss_arrangement
    loss = analyze_technical_secret_loss_arrangement('\n'.join(c.text for c in clauses))
    keys = ['secret_loss_trigger', 'future_fee_after_secret_loss', 'termination_after_secret_loss',
            *loss.get('fact_sources', {})]
    rows = bind_elements([dict(element_id=key) for key in keys], loss, clauses)
    return [dict(row, status='COVERED' if row.get('supporting_evidence') else 'MISSING') for row in rows]
