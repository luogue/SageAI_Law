"""Cost inputs come exclusively from the committed store; arithmetic stays in code."""
from datetime import date
from review_v2.lpr_protection import reference_for_date, assess_values
from review_v2.unified_facts.loan_bindings import COST_CONCEPTS
from review_v2.unified_facts.store import VerifiedFactStore, fail


def evidence(store, concepts, consumer):
    result = {}
    for key in concepts:
        for fact in store.get(key, consumer=consumer):
            for ref in fact['evidence']:
                identity = (fact['fact_id'], ref['source_start'], ref['source_end'])
                result[identity] = {**ref, 'text': ref['quote'], 'location': ref['section'],
                    'evidence_id': fact['fact_id'] + ':' + str(ref['source_start']),
                    'structured_fact_ids': [fact['fact_id']], 'source_type': 'VERIFIED_FACT',
                    'entailment_status': 'SUPPORTS', 'supports_element_ids': [key]}
    return list(result.values())


def analyze(store):
    if not isinstance(store, VerifiedFactStore) or store.schema.family != 'credit.loan':
        fail('VERIFIED_LOAN_STORE_REQUIRED')
    consumer = 'loan_cost_analysis'
    rows = store.get('loan.cost_components', consumer=consumer)
    components = []
    for f in rows:
        if f['state'] != 'PRESENT':
            continue
        value = f['normalized_value']
        rate = value['rate']
        period, percent = None, None
        if rate['state'] == 'PRESENT' and 'percent' in rate:
            period, percent = rate['period'], float(rate['percent'])
        component = {**value, 'period': period, 'percent': percent,
            'base': 'UNRESOLVED' if value['base'] == 'UNKNOWN' else value['base'],
            'scope': 'UNRESOLVED' if value['scope'] == 'UNKNOWN' else value['scope'],
            'annual_percent_estimate': round(percent * {'YEAR': 1, 'MONTH': 12, 'DAY': 365}[period], 6) if percent is not None and period in {'YEAR', 'MONTH', 'DAY'} else None,
            'evidence_id': f['fact_id'] + ':' + str(f['evidence'][0]['source_start']),
            'structured_fact_ids': [f['fact_id']]}
        components.append(component)
    regular = [c for c in components if c['kind'] == 'regular_interest']
    reference_rates = {(c['period'], c['percent']) for c in regular if c['percent'] is not None and c['period'] in {'YEAR', 'MONTH', 'DAY'}}
    for c in components:
        rate = c['rate']
        if 'multiplier' in rate and len(reference_rates) == 1:
            period, percent = next(iter(reference_rates))
            c.update(period=period, percent=percent * float(rate['multiplier']),
                annual_percent_estimate=round(percent * float(rate['multiplier']) * {'YEAR': 1, 'MONTH': 12, 'DAY': 365}[period], 6),
                reference_evidence_ids=[r['evidence_id'] for r in regular],
                structured_fact_ids=list(dict.fromkeys(c['structured_fact_ids'] + [i for r in regular for i in r['structured_fact_ids']])))
    get = lambda k: store.scalar('loan.' + k, consumer=consumer)
    cumulative = get('cost_cumulative') is True
    replacement = get('cost_replacement') is True
    exclusive = get('cost_exclusive') is True
    limited = bool(regular) and all(c['scope'] == 'LOAN_TERM' for c in regular)
    overdue = [c for c in components if c['kind'] == 'overdue_interest']
    replacement = replacement or bool(regular and overdue and limited)
    result = {'components': components, 'evidence': evidence(store, COST_CONCEPTS, consumer),
        'stacking': 'CUMULATIVE' if cumulative else 'REPLACEMENT' if replacement else 'AMBIGUOUS' if regular and overdue else 'SINGLE',
        'combined_contractual_cap': get('cost_combined_cap') is True,
        'regular_scope_explicit': limited,
        'conflicting_rates': any(len({(c['period'], c['percent']) for c in components if c['kind'] == k}) > 1 for k in ('regular_interest', 'overdue_interest')),
        'conflicting_scope': cumulative and replacement,
        'unquantified_components': [c for c in components if c['annual_percent_estimate'] is None]}
    formed = store.scalar('common.signing_date', consumer=consumer)
    benchmark = reference_for_date(date.fromisoformat(formed) if formed else None)
    # The old calculator's PRINCIPAL basis can represent an outstanding-
    # principal window only when every charge shares that SAME basis. Mixed
    # original/outstanding bases stay unresolved without an actual ledger.
    calculation = {**result, 'components': [dict(c) for c in components]}
    if components and {c['base'] for c in components} == {'UNPAID_PRINCIPAL'}:
        for c in calculation['components']:
            c.update(base='PRINCIPAL', original_base='UNPAID_PRINCIPAL',
                base_projection='COMMON_OUTSTANDING_PRINCIPAL_WINDOW')
    protection = assess_values(calculation, benchmark, exclusive=exclusive)
    unresolved = [k for k in COST_CONCEPTS if store.state(k) in {'UNKNOWN', 'CONFLICT', 'DEFERRED'}]
    # A verifier-attested unknown is not false and cannot justify a safe total.
    if not result['combined_contractual_cap'] and (unresolved or result['conflicting_scope'] or result['conflicting_rates']):
        protection.update(status='PENDING', existing_clause_risk=False,
            reason='收费事实、计收关系或成立日期存在未知/冲突，暂不能确定司法保护范围。')
    result.update(judicial_protection=protection, lpr_verification=benchmark['status'],
        calculation_status='NORMALIZED_BY_BASE_AND_PERIOD', potential_annual_percent_estimate=None,
        needs_check=protection['status'] == 'PENDING', existing_clause_risk=protection['existing_clause_risk'],
        reason=protection['reason'], unresolved_concepts=unresolved)
    store.record_decision(consumer, 'DETERMINISTIC_COST_CALCULATION', result, COST_CONCEPTS)
    return result
