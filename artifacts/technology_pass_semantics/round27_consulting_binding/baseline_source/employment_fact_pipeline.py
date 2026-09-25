"""Extract once, bind once, evaluate every EMP/NC consumer against one store."""
import json
from review_v2.clause_parser import parse_contract_clauses, strip_non_contract_tail
from review_v2.deepseek_facts import extract, verify, FactExtractionError
from review_v2.employment_fact_store import CURRENT, FactStore
from review_v2.fact_verification import verified_store, validate_projection
from review_v2.fact_dependencies import ROOTS, validate as validate_dependencies


def repair_snapshot(store, keys):
    from review_v2.employment_fact_schema import CONCEPTS, SCHEMA_VERSION
    retained=[f for f in store.facts if f['concept'] not in keys]
    return {'provider':'deepseek','model':store.verification.get('model'),
        'kind':'VERIFIED_REPAIR_SEED','active_concepts':list(store.active_concepts),'response':{
        'schema_version':SCHEMA_VERSION,'reviewed_clause_ids':[c.clause_id for c in store.clauses],
        'searched_concepts':[c for c in store.active_concepts if c not in keys],
        'unresolved_concepts':[c for c in CONCEPTS if c not in keys and store.coverage[c]=='UNCERTAIN'],
        'facts':[{'concept':f['concept'],'value':f['normalized_value'],
            'assertion':f['assertion'],'confidence':f['confidence'],
            'evidence':[{'clause_id':e['clause_id'],'quote':e['quote']} for e in f['evidence']]} for f in retained]}}


def run(text, contract_type, legacy_engine, **kwargs):
    from review_v2.fact_modules import AGREEMENT
    token=AGREEMENT.set((contract_type or 'labor').strip().lower())
    try:
        return _run(text,contract_type,legacy_engine,**kwargs)
    finally:
        AGREEMENT.reset(token)


def _run(text, contract_type, legacy_engine, **kwargs):
    source = strip_non_contract_tail(text)
    clauses = parse_contract_clauses(source)
    attempts = []
    feedback = ''
    repair_seed = None
    repair_keys = None
    for attempt in range(2):
        raw, verification = None, None
        try:
            if repair_seed is not None:
                raw = [repair_seed] + extract(clauses,validation_feedback=feedback,concept_keys=repair_keys)
            else:
                raw = extract(clauses, validation_feedback=feedback) if feedback else extract(clauses)
            extracted = FactStore(source, clauses, raw)
            extracted.verification_feedback = feedback
            verification = verify(clauses, extracted)
            store = verified_store(extracted, verification)
            from review_v2.employment_fact_schema import CONCEPTS
            from review_v2.fact_modules import select
            if any('active_concepts' in packet for packet in raw):
                expected_scope=set(select(CONCEPTS,store.facts,(contract_type or 'labor').strip().lower()))
                if store.active_concepts != expected_scope:
                    repair_seed,repair_keys=None,None
                    raise FactExtractionError('VERIFIED_MODULE_SCOPE_CHANGED',failed_stage='MODULE_APPLICABILITY',
                        field='active_concepts',expected=sorted(expected_scope),actual=sorted(store.active_concepts),
                        model_raw_value=[f for f in store.facts if f['concept'] in ROOTS])
            validate_dependencies(store.facts, CONCEPTS)
            if attempt == 0:
                # Spend the existing single repair budget on unresolved required
                # facts too. Re-extract with diagnostics; never guess a value or
                # turn an unresolved verification into an absence proof.
                from review_v2.employment_fact_schema import NONCRITICAL_FACTS
                unresolved = {c for key, options in store.element_specs.items() if store.unresolved(key)
                              for option in options for c in option
                              if store.coverage[c]=='UNCERTAIN' and c not in NONCRITICAL_FACTS}
                if unresolved:
                    repair_keys = sorted(unresolved | set(ROOTS))
                    repair_seed = repair_snapshot(store,repair_keys)
                    raise FactExtractionError('REQUIRED_FACT_VERIFICATION_UNRESOLVED',
                        failed_stage='FACT_VERIFICATION',field='required_facts',
                        model_raw_value={c:store.verification_states[c] for c in sorted(unresolved)},
                        expected='recheck the full source and concept definitions; preserve genuine uncertainty without inventing facts',
                        actual=sorted(unresolved))
            store.validation_diagnostics = extracted.validation_diagnostics + store.validation_diagnostics
            store.normalization_events = extracted.normalization_events + store.normalization_events
            store.raw = raw
            store.verification = verification
            store.validation_attempts = attempts + [{'attempt':attempt+1,'status':'VALIDATED',
                'diagnostics':store.validation_diagnostics}]
            break
        except FactExtractionError as exc:
            attempts.append({'attempt':attempt+1,'status':'BLOCKED','diagnostics':exc.diagnostics,
                             'raw_extraction':raw,'raw_verification':verification,'verification_batches':exc.raw_output})
            exc.attempts = attempts
            if attempt == 1 or not exc.repairable or str(exc).startswith(('DEEPSEEK_NOT_CONFIGURED','DOCUMENT_')):
                raise
            if getattr(exc,'partial_store',None) is not None:
                repair_keys = sorted({d['field'] for d in exc.diagnostics} | set(ROOTS))
                repair_seed = repair_snapshot(exc.partial_store,repair_keys)
            # Exactly one repair budget for the whole extraction/binding/
            # verification chain. No nested repair loop or provider fallback.
            feedback = json.dumps({'repair_instructions':'重新通读原文，按诊断修正结构化输出。未知不是空值事实；未确认事实标UNCERTAIN且不伪造取值。保持证据真实。若NONE候选引用不支持，核验阶段必须独立执行absence_scopes全文审计：无任何相关安排时返回absence_audits，不得再次用无关正向原文填NONE；存在相关事实则准确提取并保留不确定性。',
                                   'diagnostics':exc.diagnostics},ensure_ascii=False)
    store.agreement_type = (contract_type or '').strip().lower()
    token = CURRENT.set(store)
    try:
        # The old per-rule LLM reviewer must never run in this pipeline. It can
        # call other providers and return verdicts instead of structured facts.
        kwargs['use_llm'] = False
        validate_projection(store)
        result = legacy_engine(text, contract_type, **kwargs)
        validate_projection(store)
        for row in result.get('items', []):
            if row['item_id'].startswith(('EMP-','NC-','DSP-','OET-','PT-','NDA-','ET-')):
                element_states = []
                for element in row.get('coverage_elements', []):
                    key = element.get('element_id', '')
                    # Reconcile the serialized claim with the same verified
                    # projection consumed by coverage. Never preserve a PASS
                    # after source filtering has removed a required element.
                    if element.get('status') == 'COVERED' and key in store.element_specs:
                        if not store.element(key) or not any(store.supports({'element_id':key}, e)
                                for e in row.get('evidence_clauses', [])):
                            raise FactExtractionError('VERIFIED_COVERAGE_EVIDENCE_CONFLICT',
                                failed_stage='REPORT_PROJECTION',field=key,
                                model_raw_value={'rule_id':row['item_id'],'status':row['coverage_status']},
                                expected='each covered element has verified applicable source evidence in the final item',
                                actual={'verified_evidence_count':len(store.element(key))},repairable=False)
                    concepts = sorted({c for option in store.element_specs.get(key,[]) for c in option})
                    element_states.append({'element_id':key,'coverage_status':element.get('status'),
                        'required_facts':[store.verification_states[c] for c in concepts]})
                store.decisions[row['item_id']] = {
                    'status':row['coverage_status'], 'coverage_elements':row.get('coverage_elements', []),
                    'verified_fact_projection':element_states,
                    'evidence':row.get('evidence_clauses', []), 'trace':row.get('decision_trace', {})}
        from review_v2.deepseek_facts import status
        from review_v2.employment_dispatch import classify
        result['employment_classification'] = (
            {'subtype':'NON_COMPETE','label':'竞业限制协议','agreement_type':'NON_COMPETE','basis':'RESOLVED_AGREEMENT_TYPE'}
            if store.agreement_type=='non_compete' else
            {'subtype':'EMPLOYMENT_TERMINATION','label':'劳动关系解除/终止协议','agreement_type':'EMPLOYMENT_TERMINATION'} if store.agreement_type=='employment_termination' else
            {'subtype':'CONFIDENTIALITY','label':'保密协议','agreement_type':'CONFIDENTIALITY'} if store.agreement_type=='confidentiality' else classify(store))
        from review_v2.employment_rule_adapter import adapt
        from review_v2.employment_contract_checklist import LABOR_CHECKLIST
        selected, adaptation = adapt(store,LABOR_CHECKLIST)
        expected = {r.item_id for r in selected}
        actual = {r['item_id'] for r in result.get('items',[]) if r['item_id'].startswith(('EMP-','NC-','DSP-','OET-','PT-','NDA-','ET-'))}
        if expected != actual:
            raise FactExtractionError('EMPLOYMENT_RULE_ADAPTATION_MISMATCH',failed_stage='RULE_ADAPTATION',
                field='rule_ids',expected=sorted(expected),actual=sorted(actual),repairable=False,
                model_raw_value={'upstream_gate':result.get('release_quality_gate'),
                    'verified_facts':store.public()})
        result['employment_rule_adaptation'] = adaptation
        result['release_quality_gate'].setdefault('gate_results',{})['EMPLOYMENT_RULE_ADAPTATION']='PASS'
        result.update(structured_fact_debug=store.public(), llm_enabled=True, llm_status=status(),
                      global_fallback_reason='', judge_source_summary={'structured_facts':len(store.decisions)})
        return result
    finally:
        CURRENT.reset(token)
