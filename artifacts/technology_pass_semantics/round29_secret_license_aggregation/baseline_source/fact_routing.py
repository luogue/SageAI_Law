"""Resolve aliases and document classification before choosing a fact pipeline."""
from contextvars import ContextVar
from dataclasses import dataclass, replace
from hashlib import sha256

CURRENT_ROUTE = ContextVar('contract_fact_route', default=None)
TYPE_STAGES = ContextVar('contract_type_stages', default=None)


def record_stage(stage, kind):
    from review_v2.contract_registry import get_contract_meta
    stages = TYPE_STAGES.get()
    if stages is not None:
        stages[stage] = get_contract_meta(kind).key.value


def finalize(response):
    stages = dict(TYPE_STAGES.get() or {})
    record_stage('report', response.get('contract_type'))
    stages.update(TYPE_STAGES.get() or {})
    route = CURRENT_ROUTE.get()
    failures = []
    # A documented reclassification changes the execution type, not the
    # original request. Validate each stage against its own contract instead
    # of requiring the user's prior to equal the resolved document type.
    expected = {name: route.resolved_type for name in
                ('canonical', 'facts_pipeline', 'checklist', 'report')}
    expected['request'] = route.selected_type
    if any(stages.get(name) != kind for name, kind in expected.items()):
        failures.append({'requirement': 'CONTRACT_TYPE_CHAIN_CONFLICT',
            'current_status': 'FAIL', 'root_cause': '请求、规范类型、规则清单和报告类型不一致',
            'type_stages': stages, 'expected_type_stages': expected})
    response['contract_type_flow'] = {'stages': stages,
        'document_candidate': route.selection.classification_context.get('document_candidate', {}),
        'status': 'BLOCKED' if failures else 'PASS'}
    if failures:
        gate = response.setdefault('release_quality_gate', {})
        gate['status'] = 'BLOCKED'
        gate['failures'] = list(gate.get('failures') or []) + failures
        response['success'] = False
        response['result'] = '合同类型链路校验失败，正式报告未生成。'
        response['report_generation_decision'] = {'status': 'STOPPED_FATAL', 'report_generated': False, 'quality_status': 'BLOCKED'}
    return response


@dataclass(frozen=True)
class FactRoute:
    selected_type: str
    resolved_type: str
    source_sha256: str
    selection: object
    domain: object


def resolve(text, contract_type):
    from review_v2.contract_registry import get_contract_meta
    from review_v2.clause_parser import strip_non_contract_tail, parse_contract_clauses
    from review_v2.domain_selection import resolve_domain_selection
    from review_v2.technology_service_analysis import (
        begin_payment_analysis_session, begin_technology_classification_session,
        classify_technology_transaction,
    )
    selected = get_contract_meta(contract_type).response_key
    source = strip_non_contract_tail(text)
    clauses = parse_contract_clauses(source)
    begin_payment_analysis_session(source)
    begin_technology_classification_session(source)
    classification = classify_technology_transaction(source)
    selection, domain, resolved = resolve_domain_selection(selected, source, clauses,
        technology_classification=classification)
    # The comparable-domain resolver already decides whether the document's
    # operative transaction is strong enough to override a broad input prior.
    # Preserve that decision before specialist dispatch. Explicit selections of
    # separately scoped agreement families retain their existing manual policy;
    # they are not implicitly migrated by this comparable-domain boundary.
    comparable = {'sale', 'house_lease', 'service', 'technology'}
    if selected in comparable and resolved in comparable:
        candidate = selection.to_public_dict()
        selection = replace(selection, classification_context={
            **selection.classification_context, 'document_candidate': candidate})
        return FactRoute(selected, get_contract_meta(resolved).key.value,
                         sha256(source.encode()).hexdigest(), selection, domain)
    # This entry receives an explicit manual selection. Text classification is
    # diagnostic and must not silently replace it before fact dispatch.
    from review_v2.domain_resolution import resolve_contract_domain
    candidate = selection.to_public_dict()
    context = dict(selection.classification_context)
    context.update(document_candidate=candidate, primary_contract_type=selected.upper(),
                   primary_transaction={'type': selected},
                   classification_conflict={'detected': resolved != selected, 'selected': selected,
                                            'document': resolved, 'resolved': True})
    domain = resolve_contract_domain(selected, source, clauses,
        technology_classification=classification if selected == 'technology' else None)
    selection = replace(selection, selected_domain=selected.upper(),
        resolution='USER_SELECTION_ACCEPTED', compatibility='MANUAL_SELECTION',
        document_domain=domain.to_public_dict(), classification_context=context)
    return FactRoute(selected, get_contract_meta(selected).key.value,
                     sha256(source.encode()).hexdigest(), selection, domain)
