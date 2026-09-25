"""Verify quotations against parser-owned text, never against a model's raw_text."""
from copy import deepcopy
import hashlib
import re


def _hash(value):
    return hashlib.sha256(value.encode('utf-8')).hexdigest()


def exact_span(original, quote):
    start = original.find(quote)
    if start >= 0 and quote:
        return start, start + len(quote)
    # Inline emphasis is extraction presentation, not proposition content.
    # Preserve the original envelope while allowing parser-normalized quotes
    # to bind across paired Markdown emphasis markers.
    hidden = [False] * len(original)
    for marker in re.finditer(r'\*\*|__', original):
        for index in range(marker.start(), marker.end()):
            hidden[index] = True
    positions = [i for i, c in enumerate(original) if not hidden[i] and not c.isspace()]
    compact = ''.join(original[i] for i in positions)
    target = re.sub(r'(?:\*\*|__)|\s+', '', quote)
    start = compact.find(target) if target else -1
    if start >= 0:
        return positions[start], positions[start + len(target) - 1] + 1
    # Display normalization may collapse whitespace, but cannot alter words,
    # punctuation, ordering, omissions or join disjoint source spans.
    positions = [i for i,c in enumerate(original) if not c.isspace()]
    compact = ''.join(original[i] for i in positions)
    target = re.sub(r'\s+', '', quote)
    start = compact.find(target) if target else -1
    if start < 0:
        return None
    return positions[start], positions[start+len(target)-1]+1


def bind_original(evidence, clauses, document_text=None):
    row = deepcopy(evidence)
    row['verified_original'] = False
    row['source_verification'] = {'status':'FAIL','errors':[]}
    def fail(reason):
        row['source_verification']['errors'].append(reason)
        return row
    by_id = clauses if isinstance(clauses, dict) else {c.clause_id:c for c in clauses}
    source_id = str(row.get('clause_id') or '')
    clause = by_id.get(source_id)
    if str(row.get('evidence_id') or '').startswith(('SYN', 'SUMMARY')):
        return fail('DERIVED_EVIDENCE_ID_IS_NOT_ORIGINAL')
    if not clause or source_id.startswith(('SYN','SUMMARY')):
        return fail('NO_PARSER_OWNED_SOURCE')
    if row.get('source_type') in ('SEARCH_AUDIT','SYNTHETIC','MODEL_SUMMARY'):
        return fail('DERIVED_TEXT_IS_NOT_ORIGINAL')
    original = clause.raw_text or clause.text
    # A selected element span must not be expanded back to the whole clause.
    # ``text`` is often the retrieval context, while ``quote`` is the exact
    # proposition-bearing excerpt. Both still undergo parser-owned validation.
    quote = str(row.get('quote') or row.get('quoted_text') or row.get('text') or '')
    span = exact_span(original,quote)
    if span is None:
        return fail('QUOTE_NOT_IN_ORIGINAL')
    local_start,local_end = span
    quote = original[local_start:local_end]
    base = getattr(clause,'start_offset',-1)
    if document_text is not None:
        if base < 0 or document_text[base:base+len(original)] != original:
            occurrences = [m.start() for m in re.finditer(re.escape(original),document_text)]
            if len(occurrences)!=1:
                return fail('CLAUSE_NOT_UNIQUELY_BOUND_TO_DOCUMENT')
            base = occurrences[0]
    coordinate = 'DOCUMENT_TEXT' if base>=0 else 'CLAUSE_TEXT'
    start=(base if base>=0 else 0)+local_start
    end=start+len(quote)
    document_id=getattr(clause,'document_id','contract_package/main')
    identity=f'{document_id}|{source_id}|{local_start}|{local_end}|{_hash(original)}'
    source_ref={'document_id':document_id,'clause_id':source_id,
                'clause_sha256':_hash(original),'local_start':local_start,'local_end':local_end,
                'locator':clause.location}
    source_span={'start_offset':start,'end_offset':end,'raw_text':quote,'coordinate_system':coordinate}
    row.update(evidence_id='SRC-'+_hash(identity)[:20],clause_id=source_id,
        quote=quote,quoted_text=quote,text=quote,original_excerpt=quote,
        raw_text=original,location=clause.location,section=clause.location,
        document_id=document_id,original_document_reference=document_id,
        source_document=document_id,source_ref=source_ref,source_span=source_span,
        source_start=start,source_end=end,verified_original=True,derived_or_original='ORIGINAL',
        evidence_type='ATTACHMENT_TEXT' if clause.section_type=='附件' else 'CONTRACT_TEXT',
        source_verification={'status':'PASS','errors':[],'method':'EXACT_PARSER_SOURCE_SPAN'})
    row['evidence_source']={**row.get('evidence_source',{}),'document_id':document_id,
        'clause_id':source_id,'quote':quote,'section':clause.location,'source_span':deepcopy(source_span),
        'source_ref':deepcopy(source_ref),'verified_original':True,'derived_or_original':'ORIGINAL'}
    return row


def verify_binding(row, clauses):
    verified=bind_original(row,clauses)
    if not verified['verified_original']:
        return verified['source_verification']['errors']
    errors=[]
    if row.get('verified_original') is not True:errors.append('ORIGINAL_NOT_VERIFIED')
    for key in ('evidence_id','source_ref','source_span','quote','text','location',
                'source_start','source_end','evidence_source'):
        if row.get(key)!=verified.get(key):errors.append('SOURCE_BINDING_MISMATCH:'+key)
    return errors


def check_pass(evidence, clauses, requirements, entails):
    """No synthetic, unbound, or semantically unrelated material can prove PASS."""
    failures=[]
    if not evidence:
        failures.append({'reason':'NO_VERIFIED_ORIGINAL'})
    for row in evidence:
        errors=verify_binding(row,clauses)
        if errors:failures.append({'evidence_id':row.get('evidence_id'), 'reason':'INVALID_ORIGINAL','errors':errors})
        elif requirements and not any(entails(req,row) for req in requirements):
            failures.append({'evidence_id':row.get('evidence_id'),'reason':'IRRELEVANT_PASS_EVIDENCE'})
    mapping={}
    for requirement in requirements:
        key=requirement['element_id']
        matched=[r for r in evidence if not verify_binding(r,clauses) and entails(requirement,r)]
        mapping[key]=[r['evidence_id'] for r in matched]
        if not matched:failures.append({'element_id':key,'reason':'NO_VERIFIED_SEMANTIC_SUPPORT'})
        # Composite predicates can be proved by different original spans. Do
        # not let one invoice/one party/one parameter stand in for all limbs.
        components = {}
        for source in requirement.get('supporting_evidence', []):
            if source.get('component_key'):
                components.setdefault(source['component_key'], []).append(source)
        for component, sources in components.items():
            if not any(any(r.get('clause_id') == s.get('clause_id')
                           and re.sub(r'\s+', '', r.get('quote', '')) == re.sub(r'\s+', '', s.get('quote', ''))
                           for s in sources) for r in matched):
                failures.append({'element_id': key, 'component_key': component,
                                 'reason': 'NO_VERIFIED_COMPONENT_SUPPORT'})
    if not requirements:failures.append({'reason':'NO_VERIFIABLE_REQUIREMENTS'})
    return {'status':'BLOCKED' if failures else 'PASS','failures':failures,'element_evidence_ids':mapping}
