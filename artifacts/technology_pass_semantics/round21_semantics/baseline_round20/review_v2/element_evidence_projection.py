"""Reverse-project report proofs from canonical elements, never topic pools.

Uses the existing coverage, supporting_evidence and element_search schema.
Retrieval context remains available in decision_trace but is not report proof.
The audit is deliberately separate from projection, so corrupt output blocks.
"""
from copy import deepcopy
import re

from review_v2.verified_source import bind_original, exact_span

POSITIVE = {'COVERED', 'PARTIALLY_COVERED', 'ADVERSE', 'CONFLICTING'}


def atomic_leaves(elements):
    result = []
    for element in elements:
        children = element.get('child_elements') or []
        if children and all(isinstance(c, dict) and c.get('element_id') for c in children):
            result.extend(atomic_leaves(children))
        else:
            result.append(element)
    return result


def _text(row):
    return str(row.get('quote') or row.get('quoted_text') or row.get('text') or '')


def _key(row):
    return str(row.get('clause_id') or ''), re.sub(r'\s+', '', _text(row))


def positive_coverage_sources(item):
    """Only element-owned positive proof can contradict whole-rule MISSING.

    Retrieval scores, topic hits, legal context and absence evidence are not
    positive coverage. Exact/polarity verification remains a separate gate.
    """
    elements = {e['element_id']: e for e in item.coverage_elements
                if e['status'] in {'COVERED', 'PARTIALLY_COVERED'}}
    result = []
    for source in item.evidence_clauses:
        if source.get('source_type') in {'SEARCH_AUDIT', 'LEGAL_AUTHORITY'}:
            continue
        for key in source.get('supporting_element_ids', []):
            element = elements.get(key)
            if element is None:
                continue
            direct = element.get('supporting_evidence')
            if direct is None:
                direct = [dict(clause_id=cid, quote=span) for cid,span in zip(
                    element.get('source_clause_ids', []), element.get('source_spans', []))]
            if _text(source) and any(_key(s) == _key(source) for s in direct):
                result.append(source)
                break
    return result


def _eligible(item):
    return (item.item_id.startswith('TC-') and bool(item.coverage_elements)
            and item.coverage_status not in {'不适用', 'NOT_APPLICABLE'}
            and bool(item.decision_trace.get('atomic_requirement_family')
                     or item.decision_trace.get('shared_material_disposition_scope')))


def _expected(item, clauses):
    from review_v2.engine import _atomic_requirement_family, _shared_material_disposition_elements
    # Reproduce the modeled semantic predicate from the parser corpus. An
    # element ID stamped on an unrelated quote cannot validate that quote.
    family = item.decision_trace.get('atomic_requirement_family')
    elements = _atomic_requirement_family(family, clauses) if family else []
    scopes = item.decision_trace.get('shared_material_disposition_scope')
    if scopes:
        # A later shared-fact consumer adds independently scoped atoms to the
        # family; it must not lose them merely because its first family remains
        # recorded. Use the same actor/object parser used by that consumer.
        elements += _shared_material_disposition_elements(clauses, scopes if isinstance(scopes, list) else [scopes])
    return {e['element_id']: e for e in elements}


def _sources(element, expected, clauses):
    target = expected.get(element['element_id'])
    if target is None or element.get('status') not in POSITIVE:
        return []
    allowed = {_key(s) for s in target.get('supporting_evidence', []) if _text(s)}
    by_id = {c.clause_id: c for c in clauses}
    sources = element.get('supporting_evidence')
    if sources is None:
        sources = [dict(clause_id=cid, quote=span) for cid, span in zip(
            element.get('source_clause_ids', []), element.get('source_spans', []))]
    return [s for s in sources if _key(s) in allowed and s.get('clause_id') in by_id
            and exact_span(by_id[s['clause_id']].raw_text or by_id[s['clause_id']].text, _text(s))]


def normalize_partial_states(items, clauses):
    changes = []
    for item in items:
        if not _eligible(item):
            continue
        expected = _expected(item, clauses)
        for element in item.coverage_elements:
            if element.get('status') != 'PARTIALLY_COVERED' or _sources(element, expected, clauses):
                continue
            target = expected.get(element['element_id'])
            # Failed source binding is not proof of absence. MISSING requires
            # the independent full-corpus predicate to find nothing as well.
            if target is None or target.get('supporting_evidence'):
                continue
            changes.append(dict(review_id=item.item_id, element_id=element['element_id'],
                                before='PARTIALLY_COVERED', after='MISSING'))
            element.update(status='MISSING', proposition=target['required_fact'],
                           supporting_evidence=[], evidence_ids=[], supporting_evidence_ids=[],
                           source_clause_ids=[], source_spans=[], source_locations=[],
                           search_targets=target.get('search_targets') or [target['required_fact']],
                           residual_gap=target.get('residual_gap') or target['required_fact'])
        if any(c['review_id'] == item.item_id for c in changes):
            from review_v2.engine import _record_specialized_search_audit, _reconcile_specialized_coverage_from_elements
            _reconcile_specialized_coverage_from_elements(item)
            _record_specialized_search_audit(item, clauses,
                tuple(e['required_fact'] for e in expected.values()),
                [e['required_fact'] for e in item.coverage_elements if e['status'] == 'MISSING'])
            item.decision_trace['partial_source_corrections'] = [c for c in changes if c['review_id'] == item.item_id]
    return changes


def _audits(item):
    from review_v2.engine import _absence_proposition_evidence
    elements = {e['element_id']: e for e in item.coverage_elements}
    rows = []
    for search in item.decision_trace.get('element_absence_searches', []):
        key = search.get('element_id')
        element = elements.get(key)
        if (not element or element['status'] not in {'MISSING', 'PARTIALLY_COVERED', 'UNCERTAIN'}
                or search.get('result') != 'NOT_FOUND' or not search.get('searched_document_hash')):
            continue
        row, _ = _absence_proposition_evidence(risk_group=item.risk_group,
            searched_scope=['合同正文及全部已提供附件'], required_elements=search['search_targets'],
            related_clause_ids=search['searched_clause_ids'])
        if not row:
            continue
        # Public evidence rows share display fields, including typed audits.
        # This is the audit's text, not a newly invented contract quotation.
        row.update(quote=row['quoted_text'], location='SEARCH_AUDIT',
                   supporting_review_ids=[item.item_id], supporting_element_ids=[key], element_ids=[key],
                   searched_absent_element_ids=[key], element_search=deepcopy(search),
                   source_fact_key=element.get('source_fact_key'), evidence_polarity='SUPPORTS_ABSENCE')
        rows.append(row)
    return rows


def project(items, findings, clauses):
    from review_v2.engine import _assign_final_evidence_bundle
    from review_v2.technology_adverse_evidence import verify_negative_search
    selected = {i.item_id: i for i in items if _eligible(i)}
    changes = []
    for item in items:
        if (item.coverage_status in {'通过', 'PASS'} and not any(e['status'] in POSITIVE for e in item.coverage_elements)
                and verify_negative_search(item, clauses)):
            # Successful absence-of-adverse checks own the independently
            # reproduced corpus audit, not the topic retrieval candidates.
            context = deepcopy(item.evidence_clauses)
            changes.extend(dict(review_id=item.item_id, evidence_id=r.get('evidence_id'),
                                clause_id=r.get('clause_id'), quote=_text(r), reason='NEGATIVE_SEARCH_CONTEXT_NOT_ELEMENT_PROOF')
                           for r in context)
            item.decision_trace['excluded_report_context'] = context
            item.evidence_clauses = []
            item.evidence_location = ''
    for item in selected.values():
        expected = _expected(item, clauses)
        if 'element_absence_searches' not in item.decision_trace:
            from review_v2.engine import _search_final_element
            item.decision_trace['element_absence_searches'] = [
                _search_final_element(item, e, clauses) for e in item.coverage_elements
                if e['status'] in {'MISSING', 'PARTIALLY_COVERED', 'UNCERTAIN'}]
        rows = {}
        for element in item.coverage_elements:
            for source in _sources(element, expected, clauses):
                identity = _key(source)
                row = rows.get(identity)
                if row is None:
                    row = bind_original(dict(source, source_type='BODY', quote=_text(source)), clauses)
                    if not row['verified_original']:
                        continue
                    row.update(review_id=item.item_id, supporting_review_ids=[item.item_id],
                               supporting_element_ids=[], element_ids=[], supports_element_ids=[],
                               canonical_fact_keys=[], support_summary='', support_type='DIRECT', entailment_status='SUPPORTS')
                    rows[identity] = row
                for field in ('supporting_element_ids', 'element_ids', 'supports_element_ids'):
                    if element['element_id'] not in row[field]:
                        row[field].append(element['element_id'])
                fact_key = element.get('source_fact_key')
                if fact_key and fact_key not in row['canonical_fact_keys']:
                    row['canonical_fact_keys'].append(fact_key)
                # The source-specific proposition belongs to the verified
                # atomic mapping, not the whole rule or another actor's gap.
                target = expected[element['element_id']]
                canonical_source = next(s for s in target.get('supporting_evidence', [])
                                        if _key(s) == identity)
                summary = canonical_source.get('proposition') or (
                    target.get('required_fact', '') if target['status'] == 'COVERED' else '')
                parts = row['support_summary'].split('；') if row['support_summary'] else []
                if summary and summary not in parts:
                    row['support_summary'] = '；'.join([*parts, summary])
        removed = [r for r in item.evidence_clauses if r.get('source_type') != 'SEARCH_AUDIT' and _key(r) not in rows]
        changes.extend(dict(review_id=item.item_id, evidence_id=r.get('evidence_id'),
                            clause_id=r.get('clause_id'), quote=_text(r), reason='NO_VERIFIED_ELEMENT_OWNER') for r in removed)
        item.decision_trace['excluded_report_context'] = deepcopy(removed)
        item.evidence_clauses = list(rows.values()) + _audits(item)
        item.decision_trace['element_report_projection'] = {'producer': 'CANONICAL_ELEMENT_REVERSE_PROJECTION',
                                                           'excluded_count': len(removed)}
    for finding in findings:
        owners = [selected[k] for k in finding.source_review_ids if k in selected]
        # Do not drop another rule's proven adverse facts in a mixed finding.
        # Only rebuild a wholly migrated owner set here.
        if not owners or len(owners) != len(finding.source_review_ids):
            continue
        if any(i.coverage_status == '风险条款' for i in owners):
            continue
        rows = []
        for item in owners:
            source_index = {_key(r): r for r in item.evidence_clauses if r.get('source_type') != 'SEARCH_AUDIT'}
            for existing in (finding.evidence_bundle or {}).get('items', []):
                if existing.get('source_type') == 'SEARCH_AUDIT':
                    continue
                source = source_index.get(_key(existing))
                if not source:
                    continue
                row = deepcopy(existing)
                for field in ('supporting_element_ids', 'element_ids', 'canonical_fact_keys', 'support_summary'):
                    row[field] = deepcopy(source[field])
                row['supporting_review_ids'] = [item.item_id]
                rows.append(row)
            rows.extend(_audits(item))
        bundle = finding.evidence_bundle or {}
        _assign_final_evidence_bundle(finding, rows,
            missing_elements=bundle.get('missing_elements'), absence_evidence=bundle.get('absence_evidence'))
        finding.evidence_bundle['unresolved_requirements'] = deepcopy(finding.final_missing_elements)
        finding.evidence = deepcopy(finding.evidence_bundle['items'])
        finding.supporting_evidence = deepcopy(finding.evidence_bundle['items'])
    return changes


def audit(items, findings, clauses):
    from review_v2.technology_adverse_evidence import verify_negative_search
    selected = {i.item_id: i for i in items if _eligible(i)}
    expected = {key: _expected(i, clauses) for key, i in selected.items()}
    failures = []
    for item in items:
        if (item.coverage_status in {'通过', 'PASS'} and not any(e['status'] in POSITIVE for e in item.coverage_elements)
                and verify_negative_search(item, clauses)):
            failures.extend(dict(review_id=item.item_id, evidence_id=r.get('evidence_id'),
                                 reason='EVIDENCE_POLLUTION') for r in item.evidence_clauses)

    def inspect(row, owners, **context):
        relevant = [key for key in owners if key in selected]
        if not relevant or len(relevant) != len(owners):
            return
        ids = row['supporting_element_ids'] if 'supporting_element_ids' in row else row.get('element_ids') or row.get('supports_element_ids') or []
        owner_elements = {(key, e['element_id']): e for key in relevant for e in selected[key].coverage_elements}
        if not ids:
            failures.append(dict(**context, reason='EVIDENCE_POLLUTION', evidence_id=row.get('evidence_id')))
            return
        for element_id in ids:
            links = [(key, e) for (key, eid), e in owner_elements.items() if eid == element_id]
            valid = False
            for key, element in links:
                if row.get('source_type') == 'SEARCH_AUDIT':
                    search = row.get('element_search') or {}
                    valid |= (len(ids) == 1 and search.get('element_id') == element_id
                              and search.get('review_id') == key and search.get('result') == 'NOT_FOUND'
                              and bool(search.get('searched_document_hash'))
                              and element['status'] in {'MISSING', 'PARTIALLY_COVERED', 'UNCERTAIN'}
                              and search in selected[key].decision_trace.get('element_absence_searches', []))
                else:
                    valid |= any(_key(s) == _key(row) for s in _sources(element, expected[key], clauses))
            if not valid:
                failures.append(dict(**context, reason='EVIDENCE_ELEMENT_SEMANTIC_MISMATCH',
                                     element_id=element_id, evidence_id=row.get('evidence_id')))
    for key, item in selected.items():
        for row in item.evidence_clauses:
            inspect(row, [key], review_id=key)
        for e in item.coverage_elements:
            if e['status'] == 'PARTIALLY_COVERED' and not _sources(e, expected[key], clauses):
                failures.append(dict(review_id=key, element_id=e['element_id'], reason='PARTIAL_WITHOUT_DIRECT_POSITIVE_SOURCE'))
    for finding in findings:
        owners = finding.source_review_ids
        if any(selected[k].coverage_status == '风险条款' for k in owners if k in selected):
            continue
        for row in (finding.evidence_bundle or {}).get('items', []):
            inspect(row, owners, finding_id=finding.finding_id)
    return failures
