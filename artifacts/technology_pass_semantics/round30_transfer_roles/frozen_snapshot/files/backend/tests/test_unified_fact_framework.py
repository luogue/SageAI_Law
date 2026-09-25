"""No network: strict contract, scope, provenance and consumer regressions."""
from copy import deepcopy
from decimal import Decimal
from concurrent.futures import ThreadPoolExecutor
import pytest

from review_v2.clause_parser import ParsedClause
from review_v2.fact_module_registry import REGISTRY, UnknownFactFamily
from review_v2.fact_validation import FactExtractionError
from review_v2.unified_facts.schema import Concept, Module, Schema
from review_v2.unified_facts.normalization import normalize
from review_v2.unified_facts.store import CandidateStore, VerifiedFactStore, commit, CURRENT
from review_v2.unified_facts.pipeline import extract_verified


SOURCE = '第一条：本金人民币壹万叁仟元。\n第二条：仅按约定支付，无其他约定。'
CLAUSES = [ParsedClause('C1', '第一条', '金额', SOURCE.split('\n')[0], '正式合同条款', 1,
                       start_offset=0, end_offset=len(SOURCE.split('\n')[0])),
           ParsedClause('C2', '第二条', '约定', SOURCE.split('\n')[1], '正式合同条款', 1,
                       start_offset=len(SOURCE.split('\n')[0])+1, end_offset=len(SOURCE))]


def simple_schema(kind='number'):
    return Schema('test', (Module('root', (Concept('test.value', kind, '数值'),)),), ())


def observation(concept='test.value', state='PRESENT', value='13000'):
    row = {'concept': concept, 'state': state, 'confidence': .95, 'assertion': 'EXPLICIT',
           'evidence': [{'clause_id': 'C1', 'quote': '本金人民币壹万叁仟元。'}] if state in {'PRESENT','EXPLICIT_NONE','DEFERRED'} else []}
    if state == 'PRESENT':
        row['value'] = value
    return row


def packet(rows, active=None):
    return {'schema_version': 'contract-facts-1.0', 'searched_concepts': list(active) if active is not None else list(dict.fromkeys(r['concept'] for r in rows)),
            'reviewed_clause_ids': ['C1', 'C2'], 'observations': rows}


def verification(candidate):
    return {'candidate_snapshot_hash':candidate.snapshot_hash, 'reviewed_clause_ids': ['C1','C2'], 'searched_concepts': list(candidate.active),
            'checks': [{'fact_id': f['fact_id'], 'supported': True} for f in candidate.observations],
            'audits': [{'concept': c, 'reviewed_clause_ids': ['C1','C2'], 'complete': True,
                       'omitted_facts': [], 'reason': '测试协议响应：已核对全文'} for c in candidate.active]}


def candidate(rows=None, schema=None, active=None):
    schema = schema or simple_schema()
    active = active or schema.root_keys
    return CandidateStore(SOURCE, CLAUSES, schema, active, packet(rows or [observation()], active))


@pytest.mark.parametrize('family', [None, '', 'sale', 'guarantee', 'mortgage', 'unknown'])
def test_unknown_family_never_falls_back_to_labor(family):
    with pytest.raises(UnknownFactFamily):
        REGISTRY.family(family)


def test_registered_families_have_distinct_selectors_and_release_status():
    assert REGISTRY.family('labor').name == 'employment'
    assert REGISTRY.family('non_compete') is REGISTRY.family('confidentiality')
    assert REGISTRY.family('loan').migration_status == 'ACTIVE'
    assert REGISTRY.family('loan').selector != REGISTRY.family('labor').selector


@pytest.mark.parametrize('raw', ['13000', '13,000', '壹万叁仟', 13000, 13000.0])
def test_number_equivalence(raw):
    assert normalize(Concept('x', 'number', ''), raw) == Decimal('13000')


@pytest.mark.parametrize('kind,raw', [
    ('number', True), ('number', None), ('number','另行约定'), ('number','13,00'),
    ('number','一二三'), ('number','十百'), ('number','一亿三万'),
    ('number',float('nan')), ('number',float('inf')), ('boolean','false'),
    ('date','2026-02-30'), ('date','2026/09/12'), ('duration',{'amount':'未知','unit':'MONTH'}),
    ('duration',{'amount':1}), ('duration',{'amount':-1,'unit':'DAY'}),
    ('money',{'amount':13000}), ('money',{'amount':'13000','currency':'未知'}),
    ('money',{'amount':'13000','currency':'CNY','guessed':True}),
    ('formula',{'operator':'eval','operands':[{'number':1},{'number':2}]}),
    ('formula',{'operator':'MULTIPLY','operands':[{'expression':'1+1'},{'number':2}]}),
    ('formula',{'operator':'MULTIPLY','operands':[{'reference':'UNKNOWN'},{'number':2}]}),
])
def test_strict_types_reject_placeholders_defaults_and_coercion(kind, raw):
    with pytest.raises(ValueError):
        normalize(Concept('x',kind,''),raw)


@pytest.mark.parametrize('kind,value,expected', [
    ('money',{'amount':'壹万叁仟','currency':'CNY'},{'amount':Decimal('13000'),'currency':'CNY'}),
    ('date','2028-02-29','2028-02-29'),
    ('duration',{'amount':'6','unit':'MONTH'},{'amount':Decimal('6'),'unit':'MONTH'}),
    ('formula',{'operator':'MULTIPLY','operands':[{'reference':'PRINCIPAL'},{'number':'0.05'}]},
     {'operator':'MULTIPLY','operands':[{'reference':'PRINCIPAL'},{'number':Decimal('.05')}]}),
])
def test_valid_typed_values(kind,value,expected):
    assert normalize(Concept('x',kind,''),value)==expected


@pytest.mark.parametrize('state', ['ABSENT','EXPLICIT_NONE','DEFERRED','UNCERTAIN'])
def test_states_do_not_occupy_strong_type_fields(state):
    c=candidate([observation(state=state)])
    s=commit(c,verification(c))
    assert s.state('test.value')==('UNKNOWN' if state=='UNCERTAIN' else state)
    assert s.scalar('test.value',consumer='rule') is None
    bad=observation(state=state);bad['value']=state
    with pytest.raises(FactExtractionError,match='STATE_MUST_NOT_OCCUPY_VALUE'):
        candidate([bad])


def test_inactive_is_not_absent():
    schema=Schema('test',(Module('root',(Concept('parent','boolean',''),)),),
        (Module('child',(Concept('child','number',''),),(('parent',True),)),))
    c=candidate([observation('parent',state='ABSENT')],schema)
    s=commit(c,verification(c))
    assert schema.select(s.snapshot())==('parent',)
    assert s.state('child')=='NOT_APPLICABLE'


@pytest.mark.parametrize('mutation', ['wrong_quote','wrong_clause','wrong_span','missing_evidence'])
def test_evidence_binding_rejects_wrong_provenance(mutation):
    row=observation()
    if mutation=='wrong_quote':row['evidence'][0]['quote']='本金90000元'
    if mutation=='wrong_clause':row['evidence'][0]['clause_id']='C2'
    if mutation=='wrong_span':row['evidence'][0].update(source_start=0,source_end=3)
    if mutation=='missing_evidence':row['evidence']=[]
    with pytest.raises(FactExtractionError):candidate([row])


def test_evidence_spans_are_original_source_offsets():
    c=candidate();s=commit(c,verification(c));f=s.get('test.value',consumer='rule')[0]
    for e in f['evidence']:
        assert SOURCE[e['source_start']:e['source_end']]==e['quote']
        assert e['section']=='第一条'
    f['normalized_value']=999
    assert s.scalar('test.value',consumer='rule')==Decimal('13000')


@pytest.mark.parametrize('mutation', ['missing_check','duplicate_check','rejected','missing_clause','missing_audit', 'audit_clause','omission','inactive_concept'])
def test_verifier_is_required_and_fail_closed(mutation):
    c=candidate();v=verification(c)
    if mutation=='missing_check':v['checks']=[]
    if mutation=='duplicate_check':v['checks']*=2
    if mutation=='rejected':v['checks'][0]['supported']=False
    if mutation=='missing_clause':v['reviewed_clause_ids']=['C1']
    if mutation=='missing_audit':v['audits']=[]
    if mutation=='audit_clause':v['audits'][0]['reviewed_clause_ids']=['C1']
    if mutation=='omission':v['audits'][0]['omitted_facts']=[{'value':3}]
    if mutation=='inactive_concept':v['searched_concepts'].append('other.value')
    with pytest.raises(FactExtractionError):commit(c,v)


def test_cannot_construct_verified_store_from_extraction():
    with pytest.raises(FactExtractionError,match='VERIFIER_COMMIT_REQUIRED'):
        VerifiedFactStore(candidate())


def test_contradictory_or_low_confidence_values_are_not_missing():
    c=candidate([observation(),observation(state='ABSENT')])
    assert commit(c,verification(c)).state('test.value')=='CONFLICT'
    row=observation();row['confidence']=.4
    c=candidate([row]);assert commit(c,verification(c)).state('test.value')=='UNKNOWN'
    c=candidate([observation(value='3'),observation(value='4')])
    s=commit(c,verification(c))
    assert s.state('test.value')=='CONFLICT'
    assert s.get('test.value',consumer='rule')==[]


def test_no_unattested_absence():
    with pytest.raises(FactExtractionError,match='UNATTESTED_CONCEPT_STATE'):
        CandidateStore(SOURCE,CLAUSES,simple_schema(),('test.value',),packet([],['test.value']))


@pytest.mark.parametrize('parent_state,parent_value,loaded', [('PRESENT',True,True),('PRESENT',False,False),('ABSENT',None,False),('DEFERRED',None,False),('UNCERTAIN',None,False)])
def test_dynamic_pipeline_verifies_parent_before_loading_child(parent_state,parent_value,loaded):
    schema=Schema('test',(Module('root',(Concept('parent','boolean',''),)),),
        (Module('child',(Concept('child','number',''),),(('parent',True),)),))
    calls=[]
    def transport(system,payload,*,stage):
        calls.append((stage,deepcopy(payload)))
        keys=payload['active_concepts']
        assert set(payload['concepts'])==set(keys)
        assert [c['clause_id'] for c in payload['document']]==['C1','C2']
        if stage=='EXTRACTION':
            rows=[observation(k,parent_state,parent_value) if k=='parent' else observation(k,value='2') for k in keys]
            return {'model':'test-deepseek'},packet(rows,keys)
        return {'model':'test-deepseek'},{'candidate_snapshot_hash':payload['candidate_snapshot_hash'],'reviewed_clause_ids':['C1','C2'],'searched_concepts':keys,
            'checks':[{'fact_id':f['fact_id'],'supported':True} for f in payload['candidates']],
            'audits':[{'concept':k,'reviewed_clause_ids':['C1','C2'],'complete':True,'omitted_facts':[],'reason':'fixture audit'} for k in keys]}
    store=extract_verified(SOURCE,CLAUSES,schema,transport=transport,batch_size=1)
    assert ('child' in store.active_concepts)==loaded
    assert calls[0][0]=='EXTRACTION' and calls[1][0]=='VERIFICATION'
    assert calls[-1][0]=='FINAL_VERIFICATION'
    assert all('child' not in p['concepts'] for stage,p in calls[:2])


def test_request_context_is_thread_local():
    def run(value):
        token=CURRENT.set(value)
        try:return CURRENT.get()
        finally:CURRENT.reset(token)
    with ThreadPoolExecutor(max_workers=2) as pool:
        assert list(pool.map(run,['loan','employment']))==['loan','employment']
    assert CURRENT.get() is None
