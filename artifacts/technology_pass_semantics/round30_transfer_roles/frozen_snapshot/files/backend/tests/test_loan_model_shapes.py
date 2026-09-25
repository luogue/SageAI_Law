"""Real-model protocol failures and independent variants; no network or rule changes."""
from copy import deepcopy
from decimal import Decimal
import pytest

from review_v2.fact_validation import FactExtractionError
from review_v2.unified_facts.normalization import normalize
from review_v2.unified_facts.schema import Concept, Module, Schema, CHARGE_SCOPE, CHARGE_SCOPE_POLICY
from review_v2.unified_facts.store import CandidateStore, commit, source_fact_view
from review_v2.unified_facts.pipeline import VERIFICATION
from backend.tests.test_unified_fact_framework import SOURCE, CLAUSES, observation, packet, verification


@pytest.mark.parametrize('raw,expected', [
    ('自2026年9月10日至2027年9月9日', {'start_date':'2026-09-10','end_date':'2027-09-09'}),
    ('从2028年2月29日到2028年3月31日止', {'start_date':'2028-02-29','end_date':'2028-03-31'}),
    ({'start_date':'2029-01-01','end_date':'2030-01-01'}, {'start_date':'2029-01-01','end_date':'2030-01-01'}),
    ('壹拾贰个月', {'amount':Decimal(12),'unit':'MONTH'}),
    ('5个工作日', {'amount':Decimal(5),'unit':'WORKING_DAY'}),
])
def test_explicit_terms_preserve_units_or_endpoints(raw, expected):
    assert normalize(Concept('x','term',''),raw) == expected


@pytest.mark.parametrize('raw', ['明年起一年', '自9月1日至次年9月1日', '约六个月',
    '自2027年2月29日至2028年3月1日', {'start_date':'2028-01-01'},
    {'start_date':'2028-01-01','end_date':'2027-01-01'}, {'amount':None,'unit':'MONTH'}])
def test_ambiguous_or_invalid_terms_remain_blocked(raw):
    with pytest.raises(ValueError):
        normalize(Concept('x','term',''),raw)


def test_interval_cannot_be_coerced_to_measured_duration():
    with pytest.raises(ValueError):
        normalize(Concept('x','duration',''),'自2026年9月10日至2027年9月9日')


def charge(kind='regular_interest', scope='UNTIL_REPAYMENT', key='ordinary'):
    return {'kind':kind,'charge_key':key,'base':'UNPAID_PRINCIPAL','scope':scope,
        'rate':{'state':'PRESENT','percent':'7.2','period':'YEAR'}}


def collection(rows):
    schema=Schema('test',(Module('root',(Concept('test.value','loan_charge','',multiple=True),)),),())
    return CandidateStore(SOURCE,CLAUSES,schema,schema.root_keys,packet(rows))


@pytest.mark.parametrize('values', [[charge()], [charge(),charge('overdue_interest','OVERDUE','late')]])
def test_array_and_repeated_observations_have_identical_verified_facts(values):
    array=collection([observation(value=values)])
    repeated=collection([observation(value=v) for v in values])
    assert array.observations == repeated.observations
    assert array.raw['observations'][0]['value'] == values
    assert array.normalization_events[0]['operation'] == 'EXPAND_COLLECTION'
    store=commit(array,verification(array))
    assert len(store.get('test.value',consumer='test')) == len(values)
    for fact in store.snapshot():
        for evidence in fact['evidence']:
            assert SOURCE[evidence['source_start']:evidence['source_end']] == evidence['quote']


def test_member_specific_evidence_and_metadata_are_not_lost():
    first=observation(value=charge())
    second=observation(value=charge('penalty','OVERDUE','penalty'))
    second['evidence']=[{'clause_id':'C2','quote':'仅按约定支付，无其他约定。'}]
    array=collection([observation(value=[{k:v for k,v in row.items() if k not in {'concept','state'}} for row in (first,second)])])
    assert array.observations == collection([first,second]).observations


def test_empty_absent_collection_still_requires_full_source_audit():
    row=observation(state='ABSENT');row['value']=[]
    c=collection([row])
    assert c.observations == collection([observation(state='ABSENT')]).observations
    v=verification(c);v['audits'][0]['omitted_facts']=['source contains a charge']
    with pytest.raises(FactExtractionError,match='FULL_TEXT_OMISSION'):
        commit(c,v)


@pytest.mark.parametrize('value', [[], [charge(),{'kind':'penalty'}], [{'value':charge(),'unknown':True}]])
def test_invalid_collection_does_not_discard_members_or_guess_absence(value):
    with pytest.raises(FactExtractionError):
        collection([observation(value=value)])


def test_every_expanded_member_needs_own_verifier_certificate():
    c=collection([observation(value=[charge(),charge('penalty','OVERDUE','penalty')])])
    v=verification(c);v['checks'].pop()
    with pytest.raises(FactExtractionError,match='VERIFICATION_RESPONSE_INVALID:FACT_IDS'):
        commit(c,v)


@pytest.mark.parametrize('scope', ['UNTIL_REPAYMENT','LOAN_TERM'])
def test_charge_scope_is_preserved_not_rewritten_by_separate_overdue_charge(scope):
    c=collection([observation(value=[charge(scope=scope),charge('overdue_interest','OVERDUE','late')])])
    store=commit(c,verification(c))
    assert store.snapshot()[0]['normalized_value']['scope'] == scope
    # Scope disagreement cannot be cleared by a normalizer or code whitelist.
    rejected=verification(c);rejected['checks'][0]['supported']=False
    with pytest.raises(FactExtractionError,match='FACT_VERIFICATION_REJECTED'):
        commit(c,rejected)


def test_same_scope_definitions_are_available_to_extraction_and_full_source_verifier():
    public=Concept('x','loan_charge','',multiple=True).public()
    assert public['scope_definitions'] == CHARGE_SCOPE
    assert CHARGE_SCOPE_POLICY in public['verification_policy']
    assert 'verification_policy' in VERIFICATION
    assert '逐字证据' in VERIFICATION
    assert 'accrual_window' in public['value_schema']['properties']
    assert 'scope' not in public['value_schema']['properties']


@pytest.mark.parametrize('start,end,expected', [
    ('FUNDING','PRINCIPAL_REPAID','UNTIL_REPAYMENT'),
    ('FUNDING','MATURITY','LOAN_TERM'),
    ('OVERDUE','PRINCIPAL_REPAID','OVERDUE'),
    ('OVERDUE','INTEREST_PAID','OVERDUE'),
    ('UNKNOWN','PRINCIPAL_REPAID','UNKNOWN'),
    ('BREACH','UNKNOWN','UNKNOWN'),
])
def test_event_scope_projection_is_deterministic_and_only_source_fields_reach_verifier(start,end,expected):
    raw=charge();raw.pop('scope')
    raw['accrual_window']={'start_event':start,'end_event':end}
    c=collection([observation(value=raw)])
    view=source_fact_view(c.observations)
    assert view[0]['fact_id'] == c.observations[0]['fact_id']
    assert view[0]['normalized_value']['accrual_window'] == raw['accrual_window']
    assert 'scope' not in view[0]['normalized_value']
    store=commit(c,verification(c))
    assert store.snapshot()[0]['normalized_value']['scope'] == expected
    rejected=verification(c);rejected['checks'][0]['supported']=False
    with pytest.raises(FactExtractionError,match='FACT_VERIFICATION_REJECTED'):
        commit(c,rejected)


def test_inconsistent_projected_scope_is_never_admitted():
    raw=charge(scope='LOAN_TERM')
    raw['accrual_window']={'start_event':'FUNDING','end_event':'PRINCIPAL_REPAID'}
    with pytest.raises(FactExtractionError,match='SCOPE_CONFLICTS'):
        collection([observation(value=raw)])
    raw.pop('scope')
    c=collection([observation(value=raw)])
    c.observations[0]['normalized_value']['scope']='LOAN_TERM'
    with pytest.raises(FactExtractionError,match='INVALID_DETERMINISTIC_SCOPE'):
        commit(c,verification(c))


def test_same_events_with_cross_clause_evidence_share_value_but_keep_all_source_spans():
    raw=charge();raw.pop('scope')
    raw['accrual_window']={'start_event':'FUNDING','end_event':'PRINCIPAL_REPAID'}
    row=observation(value=raw)
    row['evidence'].append({'clause_id':'C2','quote':'仅按约定支付，无其他约定。'})
    c=collection([row]);v=source_fact_view(c.observations)[0]
    assert len(v['evidence']) == 2
    assert v['evidence'] == c.observations[0]['evidence']


def test_public_and_loan_terms_both_preserve_an_explicit_calendar_interval():
    from review_v2.unified_facts.loan import schema
    s=schema()
    value={'start_date':'2026-04-03','end_date':'2027-04-02'}
    assert normalize(s.concepts['common.term'],value)==value
    assert normalize(s.concepts['loan.duration'],value)==value


def test_live_pipeline_verifier_payload_uses_events_and_full_audits_at_every_stage():
    from review_v2.unified_facts.pipeline import extract_verified
    spec=Schema('test',(Module('root',(Concept('test.value','loan_charge','',multiple=True),)),),())
    raw=charge();raw.pop('scope')
    raw['accrual_window']={'start_event':'FUNDING','end_event':'PRINCIPAL_REPAID'}
    stages=[]
    def transport(system,payload,*,stage):
        if stage=='EXTRACTION':
            return {},packet([observation(value=[raw])])
        stages.append(stage)
        assert len(payload['document'])==2
        assert payload['candidates'][0]['normalized_value']['accrual_window']==raw['accrual_window']
        assert 'scope' not in payload['candidates'][0]['normalized_value']
        return {},{'candidate_snapshot_hash':payload['candidate_snapshot_hash'],'reviewed_clause_ids':['C1','C2'],'searched_concepts':['test.value'],
            'checks':[{'fact_id':f['fact_id'],'supported':True} for f in payload['candidates']],
            'audits':[{'concept':'test.value','reviewed_clause_ids':['C1','C2'],
                      'complete':True,'omitted_facts':[],'reason':'full source fixture'}]}
    store=extract_verified(SOURCE,CLAUSES,spec,transport=transport)
    assert stages==['VERIFICATION','FINAL_VERIFICATION']
    assert store.snapshot()[0]['normalized_value']['scope']=='UNTIL_REPAYMENT'
