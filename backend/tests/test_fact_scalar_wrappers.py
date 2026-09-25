import pytest
from review_v2.employment_fact_store import normalize, FactStore
from review_v2.fact_validation import FactExtractionError
from review_v2.clause_parser import parse_contract_clauses
from backend.tests.test_employment_fact_pipeline import packet, fact

@pytest.mark.parametrize('key,value,expected',[
 ('ip.assignment_scope','DUTY_OR_RESOURCES','DUTY_OR_RESOURCES'),
 ('ip.assignment_scope',{'scope':'DUTY_OR_RESOURCES'},'DUTY_OR_RESOURCES'),
 ('working_hours.days_per_week',5,5),
 ('working_hours.days_per_week',{'days_per_week':5},5),
 ('probation.duration_months',{'months':3},3),
 ('contract.start_date',{'date':'2026-09-01'},'2026-09-01'),
 ('social_insurance.employer_pays',{'employer_pays':False},False),
 ('social_insurance.employer_pays',False,False),
])
def test_scalar_or_semantic_single_field(key,value,expected):
 assert normalize(key,value)==expected

@pytest.mark.parametrize('key,value',[
 ('ip.assignment_scope',{'type':'DUTY_OR_RESOURCES'}),
 ('ip.assignment_scope',{'scope':'DUTY_OR_RESOURCES','text':'description'}),
 ('ip.assignment_scope',{'scope':'UNKNOWN'}),
 ('ip.assignment_scope',{'scope':5}),
 ('working_hours.days_per_week',{'days_per_week':'five-ish'}),
 ('working_hours.days_per_week',{'days_per_week':True}),
 ('working_hours.days_per_week',{'days_per_week':-1}),
 ('working_hours.days_per_week',{'days_per_week':float('inf')}),
 ('working_hours.days_per_week',{'days_per_week':5,'unit':'days'}),
 ('working_hours.days_per_week',{'hours_per_week':5}),
 ('working_hours.days_per_week',{'days_per_week':{'value':5}}),
 ('social_insurance.employer_pays',{'employer_pays':'false'}),
 ('contract.start_date',{'date':'2026-02-30'}),
])
def test_invalid_wrapper_still_fails(key,value):
 with pytest.raises((FactExtractionError,ValueError)):normalize(key,value)

def test_unwrapping_does_not_bypass_evidence_validation():
 cs=parse_contract_clauses('每周工作五日。')
 f=fact(cs,'working_hours.days_per_week',{'days_per_week':5},'每周工作五日。')
 f['evidence'][0]['quote']='原文中不存在的证据'
 with pytest.raises(FactExtractionError,match='EVIDENCE_NOT_IN_CLAUSE'):FactStore('每周工作五日。',cs,packet(cs,[f]))
