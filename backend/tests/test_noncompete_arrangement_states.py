import pytest
from backend.tests.test_employment_fact_pipeline import fact,packet,verified_packet
from review_v2.clause_parser import parse_contract_clauses
from review_v2.employment_fact_store import FactStore
from review_v2.fact_verification import verified_store
from review_v2.employment_fact_schema import ABSENCE_SCOPES
from review_v2.fact_validation import FactExtractionError

KEY='non_compete.arrangement'
@pytest.mark.parametrize('text,value,state',[
 ('劳动者应保守商业秘密。',None,'NOT_FOUND'),
 ('保密义务不得限制正常就业。',None,'NOT_FOUND'),
 ('离职后二年不得从事竞争业务。','EXISTS','EXISTS'),
 ('双方不设离职竞业限制。','EXPLICIT_NONE','EXPLICIT_NONE'),
 ('劳动者保守秘密。离职后二年不得从事竞争业务。','EXISTS','EXISTS'),
])
def test_states_and_nc_applicability(text,value,state):
 cs=parse_contract_clauses(text)
 s=FactStore(text,cs,packet(cs,[fact(cs,KEY,value,cs[-1].text)] if value else []))
 v=verified_store(s,verified_packet(cs,s))
 assert v.verification_states[KEY]['arrangement_state']==state
 assert v.applicability('employment_noncompete_scope')[0]==(state=='EXISTS')
 if state=='NOT_FOUND':assert v.values(KEY)==[]


def test_rejected_false_none_needs_full_search_proof():
 text='保密不得妨碍正常就业。';cs=parse_contract_clauses(text)
 s=FactStore(text,cs,packet(cs,[fact(cs,KEY,'NONE',text)]))
 p=verified_packet(cs,s);p['verification']['checks'][0]['supported']=False
 with pytest.raises(FactExtractionError,match='CORE_FACT_VERIFICATION_FAILED'):verified_store(s,p)
 p['verification']['absence_audits']=[dict(concept=KEY,result='ABSENT',reason='全文仅有保密义务，没有离职从业限制。',reviewed_clause_ids=[c.clause_id for c in cs],searched_concepts=[KEY,*ABSENCE_SCOPES[KEY]])]
 v=verified_store(s,p)
 assert v.values(KEY)==['NOT_FOUND']
 assert v.get(KEY,positive=False)==[]
 assert v.verification_states[KEY]['arrangement_state']=='NOT_FOUND'
 assert v.verification_states[KEY]['rejected_fact_ids']


def test_unknown_is_not_verified_absence():
 text='竞业安排见未提供的附件。';cs=parse_contract_clauses(text)
 s=FactStore(text,cs,packet(cs,[]));p=verified_packet(cs,s);p['verification']['unresolved_concepts']=[KEY]
 v=verified_store(s,p)
 assert v.verification_states[KEY]['arrangement_state']=='UNKNOWN'
 with pytest.raises(FactExtractionError,match='UNRESOLVED_APPLICABILITY'):v.applicability('employment_noncompete_scope')


def test_final_report_without_none_fact(monkeypatch):
 from review_v2 import employment_fact_pipeline as pipeline
 from review_v2.engine import review_contract_v2
 text='劳动合同\n保密义务不得限制劳动者就业。';cs=parse_contract_clauses(text)
 monkeypatch.setattr(pipeline,'extract',lambda *a,**k:packet(cs,[]))
 monkeypatch.setattr(pipeline,'verify',verified_packet)
 r=review_contract_v2(text,'labor')
 assert all(x['coverage_status']=='不适用' for x in r['items'] if x['item_id'].startswith('NC-'))
 assert r['release_quality_gate']['status']=='REPORT_READY'
