import pytest
from review_v2.clause_parser import parse_contract_clauses
from review_v2.employment_fact_store import FactStore
from review_v2.employment_fact_schema import ABSENCE_SCOPES
from review_v2.fact_verification import verified_store, validate_projection
from review_v2.fact_validation import FactExtractionError
from backend.tests.test_employment_fact_pipeline import fact, packet, verified_packet


def setup(text, specs):
    cs=parse_contract_clauses(text)
    fs=[fact(cs,k,v,q) for k,v,q in specs]
    store=FactStore(text,cs,packet(cs,fs))
    return cs,store,verified_packet(cs,store)


def absence(cs):
    return {'concept':'training.arrangement','result':'ABSENT','reason':'全文未约定专项培训、费用、服务期或相应违约金',
        'searched_concepts':['training.arrangement',*ABSENCE_SCOPES['training.arrangement']],
        'reviewed_clause_ids':[c.clause_id for c in cs]}


def test_rejected_general_training_none_corrected_by_full_document_audit():
    q='单位提供入职消防教育和岗位安全指导。'
    cs,s,p=setup('用工协议\n'+q,[('training.arrangement','NONE',q),('labor_protection.training',True,q)])
    p['verification']['checks'][0]['supported']=False
    p['verification']['absence_audits']=[absence(cs)]
    final=verified_store(s,p);validate_projection(final)
    assert final.values('training.arrangement')==['NONE']
    assert not final.get('training.arrangement',positive=False)
    assert final.values('labor_protection.training')==[True]
    assert final.verification_states['training.arrangement']['rejected_fact_ids']
    assert final.coverage['training.arrangement']=='ABSENT'


def test_rejection_without_full_document_proof_still_blocks():
    q='提供安全培训。';cs,s,p=setup(q,[('training.arrangement','NONE',q)])
    p['verification']['checks'][0]['supported']=False
    with pytest.raises(FactExtractionError,match='CORE_FACT_VERIFICATION_FAILED'):verified_store(s,p)
    audit=absence(cs);audit['reviewed_clause_ids']=[];p['verification']['absence_audits']=[audit]
    with pytest.raises(FactExtractionError):verified_store(s,p)


@pytest.mark.parametrize('specs,expected',[
 ([('training.arrangement','NONE','双方不约定专项培训服务期。')],['NONE']),
 ([('training.technical','数据库技术课程','单位提供数据库专项技术课程。')],[]),
 ([('training.technical','技术进修','技术进修费用由单位承担，服务期24个月。'),('training.cost','凭票承担','技术进修费用由单位承担，服务期24个月。'),('training.arrangement','CURRENT','技术进修费用由单位承担，服务期24个月。'),('training.duration_months',24,'技术进修费用由单位承担，服务期24个月。')],['CURRENT']),
 ([('training.arrangement','CURRENT','违反培训服务期应按未履行比例承担培训违约金。'),('training.service_penalty','按剩余比例','违反培训服务期应按未履行比例承担培训违约金。')],['CURRENT'])])
def test_distinct_training_semantics(specs,expected):
    text='劳动协议\n'+'\n'.join(dict.fromkeys(x[2] for x in specs));cs,s,p=setup(text,specs)
    final=verified_store(s,p)
    assert final.values('training.arrangement')==expected
    assert len(final.facts)==len(specs)


def test_absence_cannot_erase_accepted_service_arrangement():
    q='培训后应履行两年服务期。';cs,s,p=setup(q,[('training.arrangement','CURRENT',q)])
    p['verification']['absence_audits']=[absence(cs)]
    with pytest.raises(FactExtractionError,match='CONFLICTING_ABSENCE_AUDIT'):verified_store(s,p)


def test_uncertain_related_training_cannot_be_defaulted_to_none():
    q='提供入职安全教育。';cs,s,p=setup(q,[('training.arrangement','NONE',q)])
    p['verification']['checks'][0]['supported']=False
    p['verification']['absence_audits']=[absence(cs)]
    p['verification']['unresolved_concepts']=['training.cost']
    with pytest.raises(FactExtractionError,match='CONFLICTING_ABSENCE_AUDIT'):verified_store(s,p)


def test_repair_feedback_reaches_verifier(monkeypatch):
    from review_v2 import employment_fact_pipeline as pipeline
    from backend.tests.test_employment_rule_adapter import adaptation_only_engine
    q='单位组织消防教育。'
    cs,s,p=setup(q,[('training.arrangement','NONE',q)])
    monkeypatch.setattr(pipeline,'extract',lambda *args,**kwargs:packet(cs,[fact(cs,'training.arrangement','NONE',q)]))
    calls=[]
    def verifier(clauses,store):
        feedback=getattr(store,'verification_feedback','')
        calls.append(feedback)
        reply=verified_packet(clauses,store)
        reply['verification']['checks'][0]['supported']=False
        if feedback:reply['verification']['absence_audits']=[absence(clauses)]
        return reply
    monkeypatch.setattr(pipeline,'verify',verifier)
    result=pipeline.run(q,'labor',adaptation_only_engine)
    assert len(calls)==2 and calls[1]
    assert result['structured_fact_debug']['verification_states']['training.arrangement']['verification_state']=='VERIFIED_ABSENT'


def test_verified_employment_form_cannot_be_overridden_by_legacy_classifier(monkeypatch):
    from review_v2 import domain_selection as routing
    from review_v2.employment_fact_store import CURRENT
    q='双方建立非全日制用工关系。'
    cs,s,p=setup(q,[('contract.employment_form','PART_TIME',q)])
    store=verified_store(s,p)
    monkeypatch.setattr(routing,'_classify_document_family',lambda *a,**k:('SALE','high',[],{'SALE':30},{}))
    token=CURRENT.set(store)
    try:
        resolution,domain,routed=routing.resolve_domain_selection('labor',q,cs)
        assert routed=='labor'
    finally:CURRENT.reset(token)
