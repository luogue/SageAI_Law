"""Only a verifier-committed store exposes facts to rule consumers."""
from contextvars import ContextVar
from contextlib import contextmanager
from copy import deepcopy
from hashlib import sha256
from uuid import uuid4
import json
import re
from review_v2.fact_validation import FactExtractionError
from review_v2.unified_facts.normalization import normalize, wire, accrual_scope

STATES = frozenset({'PRESENT', 'ABSENT', 'EXPLICIT_NONE', 'DEFERRED', 'NOT_APPLICABLE', 'UNCERTAIN', 'UNKNOWN'})
CURRENT = ContextVar('verified_contract_facts', default=None)
_VERIFIED = object()


def fail(code, field='', actual=None, expected=None):
    raise FactExtractionError(code, failed_stage='UNIFIED_FACT_VALIDATION', field=field,
                              actual=wire(actual), expected=expected, repairable=False)


def exact_scope(actual, expected, field):
    if not isinstance(actual, list) or not all(isinstance(v, str) for v in actual) or len(actual) != len(set(actual)) or set(actual) != set(expected):
        fail('INCOMPLETE_FACT_SCOPE', field, actual, sorted(expected))


def bind(source, clauses, refs):
    if not isinstance(refs, list) or not refs:
        fail('FACT_EVIDENCE_REQUIRED', 'evidence')
    result = []
    for ref in refs:
        if not isinstance(ref, dict):
            fail('INVALID_EVIDENCE', 'evidence', ref)
        clause = clauses.get(ref.get('clause_id'))
        quote = ref.get('quote')
        clause_source = (source[clause.start_offset:clause.end_offset]
            if clause is not None and 0 <= clause.start_offset < clause.end_offset else clause.text if clause is not None else '')
        if clause is None or not isinstance(quote, str) or not quote.strip() or quote not in clause_source:
            fail('EVIDENCE_NOT_IN_CLAUSE', 'evidence', ref)
        if str(clause.block_type) not in {'OPERATIVE_CLAUSE', 'ANNEX', 'PARTY_INFORMATION', 'SIGNATURE_BLOCK'}:
            fail('NON_OPERATIVE_EVIDENCE', 'evidence.block_type', str(clause.block_type))
        # Offsets are in the immutable input source. Never fuzzy-match a quote.
        positions = [m.start() for m in re.finditer(re.escape(quote), source)]
        if clause.start_offset >= 0 and clause.end_offset > clause.start_offset:
            positions = [p for p in positions if clause.start_offset <= p and p + len(quote) <= clause.end_offset]
        if 'source_start' in ref or 'source_end' in ref:
            start, end = ref.get('source_start'), ref.get('source_end')
            if type(start) is not int or type(end) is not int or start not in positions or end != start + len(quote):
                fail('INVALID_EVIDENCE_SPAN', 'evidence.span', ref)
        elif len(positions) == 1:
            start, end = positions[0], positions[0] + len(quote)
        else:
            fail('AMBIGUOUS_OR_MISSING_SOURCE_SPAN', 'evidence.span', ref)
        result.append({'clause_id': clause.clause_id, 'quote': quote, 'section': clause.location,
                       'source_start': start, 'source_end': end, 'block_type': clause.block_type,
                       'section_type': clause.section_type})
    return result


def collection_rows(observations, schema, active, events):
    """Expand declared collections before typing/binding; every member is verified.

    Shared evidence is retained in full, never guessed or split heuristically.
    Member wrappers may instead carry their own evidence and assertion metadata.
    Empty PRESENT cannot certify absence; an explicit absence assertion is required.
    """
    for row in observations:
        if not isinstance(row, dict) or row.get('concept') not in active:
            yield row
            continue
        spec = schema.concepts[row['concept']]
        value = row.get('value')
        if not spec.multiple or not isinstance(value, list):
            yield row
            continue
        if not value:
            if row.get('state') != 'ABSENT' or row.get('evidence') != []:
                fail('EMPTY_COLLECTION_REQUIRES_EXPLICIT_ABSENCE', spec.key, row)
            converted = {k: deepcopy(v) for k, v in row.items() if k != 'value'}
            events.append({'concept': spec.key, 'operation': 'EMPTY_ABSENT_COLLECTION', 'raw_observation': deepcopy(row)})
            yield converted
            continue
        if row.get('state') != 'PRESENT':
            fail('STATE_MUST_NOT_OCCUPY_VALUE', spec.key, value)
        events.append({'concept': spec.key, 'operation': 'EXPAND_COLLECTION',
                       'member_count': len(value), 'raw_observation': deepcopy(row)})
        for member in value:
            converted = deepcopy(row)
            if isinstance(member, dict) and 'value' in member:
                if not member.keys() <= {'value', 'evidence', 'assertion', 'confidence'}:
                    fail('INVALID_COLLECTION_MEMBER_FIELDS', spec.key, member)
                converted.update(deepcopy(member))
            else:
                converted['value'] = deepcopy(member)
            yield converted


def source_fact_view(facts):
    """Verifier checks all source values; code validates deterministic projections.

    Retain the full candidate's fact_id (including projected scope), evidence and
    state. A certificate cannot be reused after either events or scope change.
    """
    result = deepcopy(facts)
    for fact in result:
        value = fact.get('normalized_value')
        if isinstance(value, dict) and 'accrual_window' in value:
            expected = accrual_scope(value['accrual_window'])
            if value.get('scope') != expected:
                fail('INVALID_DETERMINISTIC_SCOPE', fact['concept'], value)
            del value['scope']
        if isinstance(value,dict) and 'base_expression' in value:
            # The literal expression is independently verified. The normalized
            # ontology label is checked by deterministic validation, not guessed.
            from review_v2.unified_facts.ontology import validate_fact
            validate_fact(fact)
            del value['base']
    return wire(result)


class CandidateStore:
    def __init__(self, source, clauses, schema, active, packet, *, snapshot_id=None):
        self.source, self.clauses, self.schema = source, tuple(clauses), schema
        self.snapshot_id=snapshot_id or uuid4().hex
        self.active = tuple(active)
        if len(self.active) != len(set(self.active)) or not set(active) <= set(schema.concepts):
            fail('INVALID_ACTIVE_CONCEPTS', 'active_concepts', active)
        self.source_hash = sha256(source.encode()).hexdigest()
        self.raw = deepcopy(packet)
        if not isinstance(packet, dict) or packet.get('schema_version') != schema.version:
            fail('INVALID_FACT_SCHEMA_VERSION', 'schema_version')
        exact_scope(packet.get('reviewed_clause_ids'), [c.clause_id for c in clauses], 'reviewed_clause_ids')
        exact_scope(packet.get('searched_concepts'), active, 'searched_concepts')
        observations = packet.get('observations')
        if not isinstance(observations, list):
            fail('INVALID_OBSERVATIONS', 'observations')
        by_clause = {c.clause_id: c for c in clauses}
        self.observations = []
        self.normalization_events = []
        seen = set()
        for row in collection_rows(observations, schema, active, self.normalization_events):
            if not isinstance(row, dict) or row.get('concept') not in active:
                fail('OUT_OF_SCOPE_FACT', 'concept', row)
            concept, state = row['concept'], row.get('state')
            if state not in STATES or state == 'NOT_APPLICABLE':
                fail('INVALID_FACT_STATE', concept, state, 'active facts; NOT_APPLICABLE is code-derived')
            confidence = row.get('confidence')
            if type(confidence) not in (int, float) or not 0 <= confidence <= 1:
                fail('INVALID_CONFIDENCE', concept, confidence)
            if row.get('assertion') not in {'EXPLICIT', 'INFERRED'}:
                fail('INVALID_ASSERTION', concept, row.get('assertion'))
            normalized = {'concept': concept, 'state': state, 'confidence': confidence, 'assertion': row['assertion']}
            if state == 'PRESENT':
                try:
                    normalized['normalized_value'] = normalize(schema.concepts[concept], row.get('value'))
                except (ValueError, TypeError) as exc:
                    fail('INVALID_TYPED_FACT:' + str(exc), concept, row.get('value'))
                if wire(row.get('value')) != wire(normalized['normalized_value']):
                    self.normalization_events.append({'concept': concept, 'raw_value': row.get('value'),
                                                     'normalized_value': wire(normalized['normalized_value'])})
            elif 'value' in row:
                fail('STATE_MUST_NOT_OCCUPY_VALUE', concept, row['value'])
            refs = row.get('evidence', [])
            if state in {'PRESENT', 'EXPLICIT_NONE', 'DEFERRED'}:
                normalized['evidence'] = bind(source, by_clause, refs)
            elif refs:
                fail('ABSENCE_IS_NOT_QUOTED_FACT', concept, refs)
            else:
                normalized['evidence'] = []
            from review_v2.unified_facts.ontology import validate_fact
            try:
                validate_fact(normalized)
            except ValueError as exc:
                fail('INVALID_FACT_EVIDENCE:'+str(exc),concept,normalized)
            identity = json.dumps(wire(normalized), sort_keys=True, ensure_ascii=False)
            normalized['fact_id'] = 'CF-' + sha256((self.source_hash + identity).encode()).hexdigest()[:24]
            if normalized['fact_id'] in seen:
                fail('DUPLICATE_FACT', concept)
            seen.add(normalized['fact_id'])
            self.observations.append(normalized)
        if {f['concept'] for f in self.observations} != set(active):
            fail('UNATTESTED_CONCEPT_STATE', 'observations', sorted({f['concept'] for f in self.observations}), list(active))

    @property
    def snapshot_hash(self):
        # Recompute to detect any mutation after a certificate was requested.
        value = {'snapshot_id':self.snapshot_id,'source': self.source_hash, 'schema': self.schema.public(self.active),
                 'active': sorted(self.active),
                 'facts': sorted(self.observations, key=lambda f:f['fact_id'])}
        return sha256(json.dumps(wire(value),sort_keys=True,ensure_ascii=False).encode()).hexdigest()


class VerifiedFactStore:
    def __init__(self, candidate, *, _seal=None):
        if _seal is not _VERIFIED:
            fail('VERIFIER_COMMIT_REQUIRED')
        self.schema = candidate.schema
        self.active_concepts = frozenset(candidate.active)
        self.source_hash = candidate.source_hash
        self.snapshot_hash = candidate.snapshot_hash
        self.snapshot_id = candidate.snapshot_id
        self.clause_ids = tuple(c.clause_id for c in candidate.clauses)
        self._facts = tuple(deepcopy(f) | {'verified': True} for f in candidate.observations)
        self.reads = []
        self.is_verified = True
        self.debug = {'raw_extraction': candidate.raw, 'normalization_events': candidate.normalization_events}

    def state(self, concept):
        if concept not in self.schema.concepts:
            fail('UNREGISTERED_RULE_CONCEPT', concept)
        if concept not in self.active_concepts:
            return 'NOT_APPLICABLE'
        rows = [f for f in self._facts if f['concept'] == concept]
        states = {f['state'] for f in rows}
        if len(states) != 1:
            return 'CONFLICT'
        if states == {'PRESENT'} and not self.schema.concepts[concept].multiple:
            values = {json.dumps(wire(f['normalized_value']), sort_keys=True) for f in rows}
            if len(values) > 1:
                return 'CONFLICT'
        if any(f['assertion'] != 'EXPLICIT' or f['confidence'] < .75 for f in rows):
            return 'UNKNOWN'
        state = next(iter(states))
        return 'UNKNOWN' if state == 'UNCERTAIN' else state

    def get(self, concept, *, consumer):
        if not consumer:
            fail('FACT_CONSUMER_ID_REQUIRED', concept)
        state = self.state(concept)
        self.reads.append({'consumer': consumer, 'concept': concept, 'state': state})
        if state not in {'PRESENT', 'EXPLICIT_NONE', 'DEFERRED'}:
            return []
        return [deepcopy(f) for f in self._facts if f['concept'] == concept]

    def scalar(self, concept, *, consumer):
        rows = self.get(concept, consumer=consumer)
        if self.state(concept) != 'PRESENT':
            return None
        values = [f['normalized_value'] for f in rows]
        if len({json.dumps(wire(v), sort_keys=True) for v in values}) != 1:
            fail('CONFLICTING_SCALAR_FACT', concept)
        return deepcopy(values[0])

    def snapshot(self):
        return deepcopy(list(self._facts))

    def record_decision(self, consumer, stage, decision, concepts):
        if not consumer or not set(concepts) <= set(self.schema.concepts):
            fail('INVALID_FACT_DECISION_TRACE', consumer, concepts)
        self.debug.setdefault('rule_decisions', {}).setdefault(consumer, []).append({
            'stage': stage, 'decision': wire(deepcopy(decision)),
            'input_concepts': list(concepts),
            'input_fact_ids': [f['fact_id'] for f in self._facts if f['concept'] in concepts],
        })

    def public(self):
        return wire({'schema_version': self.schema.version, 'family': self.schema.family,
            'candidate_snapshot_hash': self.snapshot_hash,
            'candidate_snapshot_id': self.snapshot_id,
            'source_sha256': self.source_hash, 'active_concepts': sorted(self.active_concepts),
            'facts': self.snapshot(), 'states': {c: self.state(c) for c in self.schema.concepts},
            'reads': deepcopy(self.reads), **self.debug})


def commit(candidate, verification):
    """Exact candidate checks plus a separate full-source audit of every active concept."""
    source_fact_view(candidate.observations)  # validate every derived projection
    if not isinstance(verification, dict):
        fail('VERIFICATION_REQUIRED')
    if verification.get('candidate_snapshot_hash') != candidate.snapshot_hash:
        fail('VERIFICATION_RESPONSE_INVALID:SNAPSHOT_MISMATCH', 'candidate_snapshot_hash',
             verification.get('candidate_snapshot_hash'), candidate.snapshot_hash)
    exact_scope(verification.get('reviewed_clause_ids'), [c.clause_id for c in candidate.clauses], 'verifier.reviewed_clause_ids')
    exact_scope(verification.get('searched_concepts'), candidate.active, 'verifier.searched_concepts')
    checks, audits = verification.get('checks'), verification.get('audits')
    if not isinstance(checks, list) or not all(isinstance(r, dict) for r in checks):
        fail('INVALID_VERIFICATION_CHECKS')
    ids = [r.get('fact_id') for r in checks]
    expected_ids = [f['fact_id'] for f in candidate.observations]
    if len(ids) != len(set(str(i) for i in ids)) or set(str(i) for i in ids) != set(expected_ids):
        fail('VERIFICATION_RESPONSE_INVALID:FACT_IDS', 'checks.fact_id', ids, expected_ids)
    if any(r.get('supported') is not True for r in checks):
        fail('FACT_VERIFICATION_REJECTED', 'checks', checks)
    if not isinstance(audits, list) or not all(isinstance(r, dict) for r in audits):
        fail('FULL_TEXT_AUDITS_REQUIRED')
    exact_scope([r.get('concept') for r in audits], candidate.active, 'audits.concept')
    for audit in audits:
        exact_scope(audit.get('reviewed_clause_ids'), [c.clause_id for c in candidate.clauses], 'audit.reviewed_clause_ids')
        if audit.get('complete') is not True or audit.get('omitted_facts') != []:
            fail('FULL_TEXT_OMISSION_OR_UNCERTAINTY', audit['concept'], audit)
        if not isinstance(audit.get('reason'), str) or not audit['reason'].strip():
            fail('AUDIT_REASON_REQUIRED', audit['concept'])
    store = VerifiedFactStore(candidate, _seal=_VERIFIED)
    store.debug['verification'] = deepcopy(verification)
    return store


@contextmanager
def rule_context(store):
    if not isinstance(store, VerifiedFactStore) or not store.is_verified:
        fail('VERIFIED_STORE_REQUIRED')
    token = CURRENT.set(store)
    try:
        yield store
    finally:
        CURRENT.reset(token)
