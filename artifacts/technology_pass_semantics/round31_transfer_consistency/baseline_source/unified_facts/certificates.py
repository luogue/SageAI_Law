"""Current-snapshot verifier protocol. Invalid responses never repair facts."""
from copy import deepcopy
from review_v2.fact_validation import FactExtractionError
from review_v2.unified_facts.store import CandidateStore, source_fact_view, fail, exact_scope
from review_v2.unified_facts.ontology import validate_fact


def validate_response(candidate,response):
    try:
        if not isinstance(response,dict) or response.get('candidate_snapshot_hash')!=candidate.snapshot_hash:
            raise ValueError('SNAPSHOT_MISMATCH')
        ids=[f['fact_id'] for f in candidate.observations]
        checks=response.get('checks',[])
        actual=[c.get('fact_id') for c in checks]
        if len(actual)!=len(set(str(x) for x in actual)) or set(str(x) for x in actual)!=set(ids):
            raise ValueError('FACT_IDS')
        clause_ids=[c.clause_id for c in candidate.clauses]
        exact_scope(response.get('reviewed_clause_ids'),clause_ids,'certificate.clauses')
        exact_scope(response.get('searched_concepts'),candidate.active,'certificate.concepts')
        audits=response.get('audits',[])
        exact_scope([a.get('concept') for a in audits],candidate.active,'certificate.audits')
        by_id={f['fact_id']:f for f in candidate.observations}
        claims=[]
        for check in checks:
            if type(check.get('supported')) is not bool:
                raise ValueError('SUPPORTED_BOOLEAN_REQUIRED')
            if check['supported'] is False:
                claim=check.get('correction')
                if not isinstance(claim,dict) or claim.get('concept')!=by_id[check['fact_id']]['concept']:
                    raise ValueError('GROUNDED_CORRECTION_REQUIRED')
                claims.append(claim)
        for audit in audits:
            exact_scope(audit.get('reviewed_clause_ids'),clause_ids,'certificate.audit.clauses')
            if type(audit.get('complete')) is not bool or not isinstance(audit.get('omitted_facts'),list):
                raise ValueError('FULL_AUDIT_REQUIRED')
            for claim in audit['omitted_facts']:
                if not isinstance(claim,dict) or claim.get('concept')!=audit['concept']:
                    raise ValueError('STRUCTURED_OMISSION_REQUIRED')
                claims.append(claim)
        # Bind every correction/omission exactly like an extraction observation.
        # Reason text is diagnostic only and cannot create or override facts.
        for claim in claims:
            scope=[claim['concept']]
            packet={'schema_version':candidate.schema.version,'reviewed_clause_ids':clause_ids,
                    'searched_concepts':scope,'observations':[claim]}
            checked=CandidateStore(candidate.source,candidate.clauses,candidate.schema,scope,packet)
            for fact in checked.observations:validate_fact(fact)
        return response
    except (ValueError,TypeError,KeyError,AttributeError,FactExtractionError) as exc:
        fail('VERIFICATION_RESPONSE_INVALID:'+str(exc),'certificate')


def verify_current(candidate,payload,transport,system,stage):
    # A new request contains no old candidate IDs, no old certificates and no
    # quarantine history. History remains in local diagnostics, never in scope.
    clean={k:deepcopy(payload[k]) for k in ('family','concepts','document') if k in payload}
    clean.update(active_concepts=list(candidate.active),candidates=source_fact_view(candidate.observations),
        candidate_snapshot_hash=candidate.snapshot_hash,
        current_fact_ids=[f['fact_id'] for f in candidate.observations],
        all_clause_ids=[c.clause_id for c in candidate.clauses])
    clean['required_response_fields']=['candidate_snapshot_hash','reviewed_clause_ids','searched_concepts','checks','audits']
    # Cross-field context remains available but is explicitly non-certifiable.
    context=payload.get('known_facts_context_only',payload.get('known_verified_roots',[]))
    clean['context_facts']=[{k:v for k,v in f.items() if k not in {'fact_id','verified'}} for f in context]
    attempts=[]
    for attempt in range(3):
        body,response=transport('本轮JSON证书顶层必须包含 "candidate_snapshot_hash": "'+candidate.snapshot_hash+'"。\n'+system,clean,stage=stage)
        try:
            validate_response(candidate,response)
            candidate.verification_response_attempts=attempts
            # Local envelope metadata; the remote hash already binds this nonce.
            # Never fill or change the model-returned hash or its checks.
            response={**response,'candidate_snapshot_id':candidate.snapshot_id}
            return body,response
        except FactExtractionError as exc:
            attempts.append({'candidate_snapshot_hash':candidate.snapshot_hash,'response':response,'diagnostics':exc.diagnostics})
            exc.attempts=attempts
            if attempt==2:raise
            clean['response_validation_error']={'code':str(exc),
                'instruction':'响应无效。仅重新核验当前candidates和snapshot；不得重抽取或改写候选。所有否决/遗漏必须用correction/omitted_facts结构化观察并给逐字证据。'}
