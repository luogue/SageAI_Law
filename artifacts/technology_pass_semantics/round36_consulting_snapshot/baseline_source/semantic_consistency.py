"""Fail closed before rendering if the canonical semantic proof was overwritten."""
from review_v2.lease_semantics import corpus_facts, supports


def validate(items, clauses):
    sources = {c.clause_id: c for c in clauses}
    failures = []
    checked = []
    def fail(item, key, reason):
        failures.append(dict(review_id=item.item_id, element_id=key,
                             code='CANONICAL_SEMANTIC_PROOF_MISMATCH',
                             root_cause=reason, responsible_function=__name__+'.validate'))
    for item in items:
        if not item.decision_trace.get('require_canonical_validation') or item.coverage_status == '不适用':
            continue
        specs = item.decision_trace['semantic_requirements']
        store = corpus_facts(clauses, specs)
        states = {e['element_id']: e for e in item.coverage_elements}
        audits = {e['element_id']: e for e in item.decision_trace.get('element_absence_searches', [])}
        found = 0
        for spec in specs:
            key = spec['element_id']
            has_fact = bool(store[key])
            found += has_fact
            state = states.get(key, {}).get('status')
            if state != ('COVERED' if has_fact else 'MISSING'):
                fail(item, key, 'Coverage disagrees with the canonical corpus evaluator')
            if has_fact and audits.get(key, {}).get('result') == 'NOT_FOUND':
                fail(item, key, 'Positive fact and NOT_FOUND coexist')
            proof = [e for e in item.evidence_clauses if supports(spec, e)]
            if has_fact and not proof:
                fail(item, key, 'A covered element has no directly supporting final evidence')
            for evidence in proof:
                source = sources.get(evidence.get('clause_id'))
                quote = evidence.get('quote') or evidence.get('text') or ''
                if (not source or evidence.get('location') != source.location
                        or not quote or quote not in source.text
                        or not supports(spec, {**evidence, 'text': quote})):
                    fail(item, key, 'Final quote/location does not prove the element at its canonical source')
                context_id = evidence.get('semantic_parent_context_id')
                if context_id:
                    context = sources.get(context_id)
                    if (not context or evidence.get('semantic_parent_context') != context.text
                            or evidence.get('semantic_parent_context_location') != context.location):
                        fail(item, key, 'Context proof was detached from its canonical source')
            checked.append(dict(review_id=item.item_id, element_id=key,
                                positive_fact=has_fact, final_status=state))
        expected = '通过' if found == len(specs) else '部分覆盖' if found else '缺失'
        if item.coverage_status != expected:
            fail(item, '', 'Final rule status disagrees with its individual element states')
        for evidence in item.evidence_clauses:
            if evidence.get('source_type') != 'SEARCH_AUDIT' and not any(supports(s, evidence) for s in specs):
                fail(item, '', 'Published evidence supports none of the rule required elements')
    return dict(status='BLOCKED' if failures else 'REPORT_READY', failures=failures,
                gate_results={'CANONICAL_SEMANTIC_PROOF_GATE': 'FAIL' if failures else 'PASS'},
                checked_elements=checked)
