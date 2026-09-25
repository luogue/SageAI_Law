"""One verified FactStore; coverage is a projection, never a model verdict."""
from copy import deepcopy
from review_v2.fact_validation import FactExtractionError
from review_v2.employment_fact_schema import CONCEPTS, SCHEMA_VERSION, NONCRITICAL_FACTS, ABSENCE_SCOPES
from review_v2.employment_fact_store import FactStore

PROTOCOL = 'fact-verification-2'


def fail(rule, field, actual, expected):
    raise FactExtractionError(rule, failed_stage='VERIFICATION_SCHEMA', field=field,
                              model_raw_value=actual, actual=actual, expected=expected)


def _string_set(value, expected, field):
    if not isinstance(value,list) or not all(isinstance(v,str) for v in value) or set(value)!=set(expected):
        fail('INCOMPLETE_VERIFICATION_SCOPE',field,value,sorted(expected))


def projected_state(facts, *, rejected=False, unresolved=False):
    explicit = [f for f in facts if f['assertion']=='EXPLICIT' and f['confidence']>=.75]
    if explicit:
        return 'EXTRACTED', 'VERIFIED_PRESENT'
    if facts:
        return 'UNCERTAIN', 'VERIFIED_INFERRED_OR_LOW_CONFIDENCE'
    if rejected:
        return 'UNCERTAIN', 'VERIFICATION_REJECTED'
    if unresolved:
        return 'UNCERTAIN', 'UNRESOLVED'
    return 'ABSENT', 'VERIFIED_ABSENT'


def validate_projection(store):
    """Keep the conflict gate on canonical, source-validated state."""
    failures=[]
    for concept, state in store.verification_states.items():
        rows=[f for f in store.facts if f['concept']==concept]
        expected,_=projected_state(rows,rejected=bool(state['rejected_fact_ids']) and not state.get('absence_audit'),unresolved=state['unresolved'])
        if concept not in store.active_concepts and not rows:expected='NOT_APPLICABLE'
        if store.coverage.get(concept)!=expected:
            failures.append({'failed_stage':'VERIFIED_COVERAGE_AGGREGATION','fact_id':state['verified_fact_ids'],
                'field':'coverage.'+concept,'validation_rule':'VERIFICATION_COVERAGE_CONFLICT',
                'model_raw_value':state['model_coverage_advisory'],'evidence':[e for f in rows for e in f['evidence']],
                'expected':expected,'actual':store.coverage.get(concept),'disposition':'BLOCK'})
    if failures:
        raise FactExtractionError('VERIFICATION_COVERAGE_CONFLICT',diagnostics=failures)


def verified_store(extracted, packet):
    data=packet.get('verification') if isinstance(packet,dict) else None
    if not isinstance(data,dict):
        fail('MISSING_FACT_VERIFICATION','verification',data,'per-fact checks and full-text search attestation')
    version=data.get('verification_schema_version')
    if version not in (None,PROTOCOL):
        fail('UNSUPPORTED_VERIFICATION_SCHEMA','verification_schema_version',version,PROTOCOL)
    _string_set(data.get('reviewed_clause_ids'),[c.clause_id for c in extracted.clauses],'reviewed_clause_ids')
    advisory={}
    if 'searched_concepts' in data:
        from review_v2.verification_batches import check_scope
        check_scope(extracted.active_concepts,data['searched_concepts'],'final_store')
        unresolved=data.get('unresolved_concepts',[])
        if not isinstance(unresolved,list) or not all(isinstance(c,str) and c in extracted.active_concepts for c in unresolved):
            fail('UNKNOWN_CONCEPT_KEY','unresolved_concepts',unresolved,list(CONCEPTS))
        unresolved=set(unresolved)
    else:
        # Stored v1 responses are supported only through this explicit boundary.
        # Their coverage column is advisory; it cannot veto supported facts.
        advisory=data.get('coverage')
        if not isinstance(advisory,dict) or set(advisory)!=extracted.active_concepts:
            fail('INCOMPLETE_VERIFICATION_SCOPE','coverage',advisory,list(CONCEPTS))
        if any(v not in ('EXTRACTED','ABSENT','UNCERTAIN') for v in advisory.values()):
            fail('INVALID_EXTRACTION_COVERAGE','coverage',advisory,['EXTRACTED','ABSENT','UNCERTAIN'])
        unresolved={c for c,v in advisory.items() if v in ('EXTRACTED','UNCERTAIN')}
    checks=data.get('checks')
    if not isinstance(checks,list) or not all(isinstance(c,dict) and isinstance(c.get('fact_id'),str) for c in checks):
        fail('INVALID_FACT_VERIFICATION','checks',checks,'array of fact_id + supported')
    ids=[c['fact_id'] for c in checks]
    from review_v2.verification_batches import check_ids
    check_ids(extracted.facts, checks, 'merged')
    if any(type(c.get('supported')) is not bool for c in checks):
        fail('INVALID_FACT_VERIFICATION','checks.supported',checks,'boolean')
    additions=data.get('additional_facts',[])
    if not isinstance(additions,list) or not all(isinstance(f,dict) for f in additions):
        fail('INVALID_ADDITIONAL_FACTS','additional_facts',additions,'array of source-bound facts')
    by_check={c['fact_id']:c for c in checks}
    accepted=[]
    rejected={c:[] for c in CONCEPTS}
    for f in extracted.facts:
        if not by_check[f['fact_id']]['supported']:
            rejected[f['concept']].append(f['fact_id'])
            continue
        accepted.append({'concept':f['concept'],'value':f['normalized_value'],'confidence':f['confidence'],
            'assertion':f['assertion'],'origin_fact_id':f['fact_id'],
            'evidence':[{'clause_id':e['clause_id'],'quote':e['quote']} for e in f['evidence']]})
    accepted.extend(deepcopy(additions))
    # All accepted/added candidates are source-bound and type-checked before
    # projecting any coverage. UNCERTAIN is a staging state, never a verdict.
    store=FactStore(extracted.source,extracted.clauses,[{'active_concepts':list(extracted.active_concepts),'response':{
        'schema_version':SCHEMA_VERSION,'reviewed_clause_ids':[c.clause_id for c in extracted.clauses],
        'coverage':{c:'UNCERTAIN' for c in extracted.active_concepts},'facts':accepted}}])
    unresolved |= store.quarantined_concepts | extracted.quarantined_concepts
    # A document-wide absence attestation is not a fabricated quoted fact.
    audits = {}
    audit_rows = data.get('absence_audits', [])
    if not isinstance(audit_rows, list) or not all(isinstance(a, dict) for a in audit_rows):
        fail('INVALID_ABSENCE_AUDIT', 'absence_audits', audit_rows, 'array of full-document absence attestations')
    for audit in audit_rows:
        concept = audit.get('concept')
        scope = tuple(c for c in ABSENCE_SCOPES.get(concept,()) if c in extracted.active_concepts)
        if concept not in ABSENCE_SCOPES or concept not in extracted.active_concepts or concept in audits:
            fail('INVALID_ABSENCE_AUDIT', 'absence_audits.concept', concept, list(ABSENCE_SCOPES))
        _string_set(audit.get('reviewed_clause_ids'), [c.clause_id for c in extracted.clauses], 'absence_audits.reviewed_clause_ids')
        _string_set(audit.get('searched_concepts'), [concept, *scope], 'absence_audits.searched_concepts')
        if audit.get('result') != 'ABSENT' or not isinstance(audit.get('reason'), str) or not audit['reason'].strip():
            fail('INVALID_ABSENCE_AUDIT', concept, audit, 'explicit ABSENT conclusion and full-text rationale')
        if unresolved.intersection([concept, *scope]) or any(f['concept'] == concept for f in store.facts):
            fail('CONFLICTING_ABSENCE_AUDIT', concept, audit, 'no unresolved or accepted arrangement facts')
        # Related positive facts must not disappear behind a NONE correction.
        from review_v2.employment_fact_schema import ABSENCE_CONTEXT_FACTS
        obligation_scope = set(scope) - ABSENCE_CONTEXT_FACTS.get(concept, set())
        if any(f['concept'] in obligation_scope or (concept == 'training.arrangement'
                   and f['concept'] == 'penalties.obligations'
                   and f['normalized_value'].get('scope') in {'SPECIAL_TRAINING','TRAINING_SERVICE_PERIOD'}
                   and f['normalized_value'].get('imposed') is True)
                   or (concept == 'non_compete.arrangement' and f['concept'] == 'penalties.obligations'
                       and f['normalized_value'].get('scope') == 'NON_COMPETE'
                       and f['normalized_value'].get('imposed') is True) for f in store.facts):
            fail('CONFLICTING_ABSENCE_AUDIT', concept, audit, 'related facts require separate arrangement verification')
        audits[concept] = deepcopy(audit)
    store.verification_states={}
    store.coverage_reconciliation=[]
    for concept in CONCEPTS:
        rows=[f for f in store.facts if f['concept']==concept]
        coverage,state=projected_state(rows,rejected=bool(rejected[concept]) and concept not in audits,unresolved=concept in unresolved)
        if concept not in store.active_concepts:coverage,state='NOT_APPLICABLE','NOT_APPLICABLE'
        store.coverage[concept]=coverage
        detail={'required_fact':concept,'factstore_state':state,
                'verification_state':state,'coverage_state':coverage,
                'verified_fact_ids':[f['fact_id'] for f in rows], 'rejected_fact_ids':rejected[concept],
                'unresolved':concept in unresolved,'model_coverage_advisory':advisory.get(concept),
                'extraction_state':extracted.coverage[concept], 'absence_audit':audits.get(concept),
                'verified_absence_value':('NOT_FOUND' if concept == 'non_compete.arrangement' else 'NONE') if concept in audits else None}
        if concept == 'non_compete.arrangement':
            detail['arrangement_state'] = ('UNKNOWN' if coverage == 'UNCERTAIN' else
                'EXISTS' if any(f['normalized_value'] == 'EXISTS' for f in rows) else
                'EXPLICIT_NONE' if any(f['normalized_value'] == 'EXPLICIT_NONE' for f in rows) else
                'DEFERRED' if rows else 'NOT_FOUND')
        store.verification_states[concept]=detail
        if advisory.get(concept) is not None and advisory[concept]!=coverage:
            store.coverage_reconciliation.append({**detail,'reason':'PROJECT_FROM_VERIFIED_FACTS_NOT_MODEL_LABEL'})
    store.verification=packet
    store.is_verified=True
    validate_projection(store)
    # A failed core verification is not an absence proof. Keep it in the
    # bounded repair/BLOCK path instead of emitting a misleading missing item.
    failures=[]
    for concept,state in store.verification_states.items():
        if state['rejected_fact_ids'] and concept not in NONCRITICAL_FACTS and concept not in audits:
            # Another accepted fact of this concept is not a correction of the
            # rejected one. Only an explicit verifier replacement of its source
            # proposition can close that rejection.
            def corrected(f):
                quotes={(e['clause_id'],e['quote']) for e in f['evidence']}
                return any(a.get('concept')==concept and a.get('corrects_fact_id')==f['fact_id'] and
                    quotes <= {(e.get('clause_id'),e.get('quote')) for e in a.get('evidence',[])}
                    for a in additions)
            rows=[extracted.by_id[i] for i in state['rejected_fact_ids'] if not corrected(extracted.by_id[i])]
            if not rows:continue
            # Rejecting an explicitly labelled hypothesis leaves an unknown
            # context, not a failed assertion of an explicit core fact.
            if not any(f['assertion']=='EXPLICIT' and f['confidence']>=.75
                       and f['normalized_value'] is not False for f in rows):
                continue
            failures.append({'failed_stage':'FACT_VERIFICATION','fact_id':state['rejected_fact_ids'],
                'field':concept,'validation_rule':'CORE_FACT_VERIFICATION_FAILED',
                'model_raw_value':[by_check[f['fact_id']] for f in rows],
                'evidence':[e for f in rows for e in f['evidence']],
                'expected':'supported, source-bound core fact or a verified correction',
                'actual':state,'disposition':'BLOCK'})
    if failures:
        error=FactExtractionError('CORE_FACT_VERIFICATION_FAILED',diagnostics=failures)
        error.partial_store=store
        raise error
    return store
