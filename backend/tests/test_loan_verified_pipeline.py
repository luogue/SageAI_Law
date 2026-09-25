"""Protocol fixtures test consumers; live extraction is a separate acceptance run."""
from copy import deepcopy
import pytest
from review_v2.unified_facts import loan_pipeline, loan_rules, loan_bindings
from review_v2.unified_facts.loan import schema, migration_inventory
from review_v2.unified_facts.store import CandidateStore, commit
from review_v2.unified_facts.normalization import normalize
from review_v2.unified_facts.schema import Concept
from review_v2.fact_validation import FactExtractionError
from backend.tests.test_loan_verified_adapter import loan_store
from backend.tests.test_unified_fact_framework import SOURCE, CLAUSES, observation, packet, verification


def obs(key, value=True, state='PRESENT'):
    return observation(key, state=state, value=value)


def by_id(store):
    return {i.item_id: i for i in loan_rules.evaluate(store)[0]}


def test_all_48_nodes_are_explicitly_bound():
    from review_v2.loan_contract_checklist import LOAN_REVIEW_CHECKLIST
    assert len(LOAN_REVIEW_CHECKLIST) == 48
    assert migration_inventory()['unmapped_rule_nodes'] == []
    s = schema()
    for node in LOAN_REVIEW_CHECKLIST:
        keys = loan_bindings.node_concepts(node.node_id)
        assert keys and set(keys) <= set(s.concepts)


@pytest.mark.parametrize('node', sorted(loan_bindings.EXTRA))
def test_remaining_nodes_execute_with_verified_inputs_only(node, monkeypatch):
    from review_v2 import loan_facts, loan_costs, contract_facts, engine
    def forbidden(*a, **kw):
        pytest.fail('raw/legacy consumer reached')
    for module, names in [(loan_facts, ['units', '_context_units', '_party_kind', 'negative_scan', 'financing_charge']),
        (loan_costs, ['analyze_costs', 'external_assessment']), (contract_facts, ['extract_contract_fact_graph']),
        (engine, ['_review_contract_v2_legacy', '_judge_checkpoints_with_registry'])]:
        for name in names:
            monkeypatch.setattr(module, name, forbidden)
    result = loan_rules.evaluate(loan_store())[0]
    item = next(i for i in result if i.node_id == node)
    assert item.decision_trace['verified_factstore_only'] is True


@pytest.mark.parametrize('state,expected', [('ABSENT', '缺失'), ('UNKNOWN', '待核验'),
    ('UNCERTAIN', '待核验'), ('DEFERRED', '待核验'), ('EXPLICIT_NONE', '部分覆盖')])
def test_money_state_is_not_coerced_to_missing(state, expected):
    store = loan_store({'loan.principal': obs('loan.principal', state=state)})
    assert by_id(store)['L-03-01'].coverage_status == expected


def test_conflicting_money_is_not_selected_or_silently_coerced():
    s = schema()
    active = s.select([])
    rows = [obs(k, state='ABSENT') for k in active if k != 'loan.principal']
    rows += [obs('loan.principal', {'amount': n, 'currency': 'CNY'}) for n in (100, 200)]
    c = CandidateStore(SOURCE, CLAUSES, s, active, packet(rows, active))
    store = commit(c, verification(c))
    assert store.state('loan.principal') == 'CONFLICT'
    assert store.scalar('loan.principal', consumer='test') is None
    assert by_id(store)['L-03-01'].coverage_status == '待核验'


def test_partial_cross_clause_fact_is_not_total_absence():
    key = 'loan.element.loan_interest_base'
    store = loan_store({key: obs(key)})
    row = by_id(store)['L-05-01']
    assert row.coverage_status == '部分覆盖'
    assert row.evidence_clauses[0]['quote'] == '本金人民币壹万叁仟元。'
    other = 'loan.element.loan_interest_period'
    second = obs(other)
    second['evidence'] = [{'clause_id': 'C2', 'quote': CLAUSES[1].text}]
    store = loan_store({key: obs(key), other: second})
    row = by_id(store)['L-05-01']
    assert row.coverage_status == '通过'
    assert {e['clause_id'] for e in row.evidence_clauses} == {'C1', 'C2'}


@pytest.mark.parametrize('parent', ['guarantee', 'early_repayment', 'extension', 'spouse', 'charges'])
@pytest.mark.parametrize('state', ['ABSENT', 'UNKNOWN', 'EXPLICIT_NONE', 'DEFERRED'])
def test_child_scope_requires_verified_present_parent(parent, state):
    key = 'loan.' + parent
    store = loan_store({key: obs(key, state=state)})
    for module in schema().modules:
        if (key, True) in module.requires:
            assert not {c.key for c in module.concepts} & store.active_concepts


def test_complete_report_retains_only_verified_evidence_and_blocks_drift(monkeypatch):
    from review_v2 import engine, loan_facts, loan_costs, loan_semantics, contract_facts
    monkeypatch.setattr(engine, '_review_contract_v2_legacy', lambda *a, **k: pytest.fail('legacy called'))
    monkeypatch.setattr(loan_facts, 'units', lambda *a: pytest.fail('rescan'))
    for module, names in ((loan_facts, ('_context_units', 'negative_scan', 'financing_charge', 'extract', 'supports')),
        (loan_costs, ('analyze_costs', 'external_assessment')), (loan_semantics, ('concept_facts', 'rate_adjustment')),
        (contract_facts, ('extract_contract_fact_graph',)), (engine, ('_apply_loan_shared_facts', '_judge_checkpoints_with_registry'))):
        for name in names:
            monkeypatch.setattr(module, name, lambda *a, **k: pytest.fail('old fact consumer called'))
    store = loan_store({'loan.principal': obs('loan.principal', {'amount': '壹万叁仟', 'currency': 'CNY'})})
    result = loan_pipeline.report(store)
    assert result['all_items_count'] == 48
    assert result['fact_migration']['mode'] == 'VERIFIED_FACTS'
    assert result['release_quality_gate']['status'] == 'REPORT_READY'
    assert result['statistics_consistency_gate']['status'] == 'REPORT_READY'
    assert len(result['structured_fact_debug']['rule_decisions']) >= 48
    items, _ = loan_rules.evaluate(store)
    item = next(i for i in items if i.item_id == 'L-03-01')
    item.evidence_clauses[0]['source_start'] += 1
    with pytest.raises(FactExtractionError, match='SPAN_DRIFT'):
        loan_pipeline.validate_report(store, items, [], [])


def test_v2_loan_ignores_legacy_option_and_never_falls_back(monkeypatch):
    from review_v2 import engine
    store = loan_store()
    monkeypatch.setattr(loan_pipeline, 'extract_verified', lambda *a, **k: store)
    monkeypatch.setattr(engine, '_review_contract_v2_legacy', lambda *a, **k: pytest.fail('legacy'))
    result = engine.review_contract_v2('借款合同\n出借人向借款人提供借款。', 'loan', use_llm=False)
    assert result['fact_migration']['mode'] == 'VERIFIED_FACTS'
    def rejected(*a, **k):
        raise FactExtractionError('TEST_VERIFIER_REJECTED')
    monkeypatch.setattr(loan_pipeline, 'extract_verified', rejected)
    with pytest.raises(FactExtractionError, match='TEST_VERIFIER_REJECTED'):
        engine.review_contract_v2('借款合同\n出借人向借款人提供借款。', 'loan', use_llm=False)


@pytest.mark.parametrize('rate,status', [(6, 'PASS'), (12, 'PASS'), (18, 'RISK')])
def test_cost_policy_uses_typed_store_and_existing_threshold(rate, status):
    from review_v2.unified_facts.loan_costs import analyze
    fields = {'loan.charges': obs('loan.charges'),
        'common.signing_date': obs('common.signing_date', '2025-05-25'),
        'loan.cost_components': obs('loan.cost_components', {'kind': 'regular_interest', 'charge_key': 'regular_interest',
            'base': 'PRINCIPAL', 'scope': 'LOAN_TERM', 'rate': {'state': 'PRESENT', 'percent': rate, 'period': 'YEAR'}})}
    costs = analyze(loan_store(fields))
    assert costs['judicial_protection']['status'] == status
    assert costs['judicial_protection']['cap_percent'] == 12


@pytest.mark.parametrize('change', [{'rate': {'state': 'PRESENT', 'percent': '待定', 'period': 'YEAR'}},
    {'rate': {'state': 'UNKNOWN', 'percent': 0}}, {'base': '本金'}, {'scope': None},
    {'rate': {'state': 'PRESENT', 'percent': True, 'period': 'YEAR'}}])
def test_charge_types_never_guess_or_fill_default(change):
    value = {'kind': 'regular_interest', 'charge_key': 'interest', 'base': 'PRINCIPAL', 'scope': 'LOAN_TERM',
        'rate': {'state': 'PRESENT', 'percent': 6, 'period': 'YEAR'}, **change}
    with pytest.raises(ValueError):
        normalize(Concept('loan.cost_components', 'loan_charge', ''), value)


def test_one_off_penalty_is_not_annualized():
    from review_v2.unified_facts.loan_costs import analyze
    store = loan_store({'loan.charges': obs('loan.charges'),
        'loan.cost_components': obs('loan.cost_components', {'kind': 'penalty', 'charge_key': 'one_off',
            'base': 'PRINCIPAL', 'scope': 'UNKNOWN', 'rate': {'state': 'PRESENT', 'percent': 20, 'period': 'ONCE'}})})
    costs = analyze(store)
    assert costs['components'][0]['percent'] == 20
    assert costs['components'][0]['annual_percent_estimate'] is None
    assert costs['judicial_protection']['status'] == 'PENDING'


@pytest.mark.parametrize('permission,prohibited,expected', [(True,False,'通过'),(False,True,'风险条款'),(True,True,'待核验')])
def test_permission_polarity_and_cross_fact_conflict(permission,prohibited,expected):
    store=loan_store({'loan.early_repayment':obs('loan.early_repayment'),
        'loan.early_permission':obs('loan.early_permission',permission),
        'loan.early_prohibited':obs('loan.early_prohibited',prohibited)})
    rows=by_id(store)
    assert rows['L-07-01'].coverage_status==expected
    assert rows['L-07-03'].coverage_status==expected
    if permission and prohibited:
        assert rows['L-07-01'].decision_trace['derived_fact_state']=='CONFLICT'


def test_final_repair_requires_new_verification_of_whole_snapshot():
    from backend.tests.test_unified_fact_framework import simple_schema
    from review_v2.unified_facts.pipeline import extract_verified
    calls=[]
    def transport(system,payload,*,stage):
        calls.append(stage)
        if stage in {'EXTRACTION','FINAL_REEXTRACTION'}:
            value='2' if stage=='FINAL_REEXTRACTION' else '1'
            return {},packet([observation(value=value)],payload['active_concepts'])
        first_final=stage=='FINAL_VERIFICATION' and calls.count('FINAL_VERIFICATION')==1
        return {},{'candidate_snapshot_hash':payload['candidate_snapshot_hash'],'reviewed_clause_ids':['C1','C2'],'searched_concepts':payload['active_concepts'],
            'checks':[{'fact_id':f['fact_id'],'supported':not first_final,**({'correction':observation(value='2')} if first_final else {})} for f in payload['candidates']],
            'audits':[{'concept':k,'reviewed_clause_ids':['C1','C2'],'complete':True,
                'omitted_facts':[],'reason':'protocol fixture'} for k in payload['active_concepts']]}
    store=extract_verified(SOURCE,CLAUSES,simple_schema(),transport=transport)
    assert store.scalar('test.value',consumer='test')==2
    assert calls[-1]=='REPAIRED_SNAPSHOT_VERIFICATION'
    assert store.debug['final_repairs'][0]['rejected_candidates'][0]['normalized_value']=='1'


def test_incomplete_final_audit_cannot_generate_a_report():
    from backend.tests.test_unified_fact_framework import simple_schema
    from review_v2.unified_facts.pipeline import extract_verified
    def transport(system,payload,*,stage):
        if stage in {'EXTRACTION','FINAL_REEXTRACTION'}:
            return {},packet([observation()],payload['active_concepts'])
        return {},{'candidate_snapshot_hash':payload['candidate_snapshot_hash'],'reviewed_clause_ids':['C1','C2'],'searched_concepts':payload['active_concepts'],
            'checks':[{'fact_id':f['fact_id'],'supported':True} for f in payload['candidates']],
            'audits':[{'concept':k,'reviewed_clause_ids':['C1','C2'],'complete':stage=='VERIFICATION',
                'omitted_facts':[],'reason':'omission test'} for k in payload['active_concepts']]}
    with pytest.raises(FactExtractionError,match='FULL_TEXT_OMISSION_OR_UNCERTAINTY'):
        extract_verified(SOURCE,CLAUSES,simple_schema(),transport=transport)


@pytest.mark.parametrize('known_omission',[False,True])
def test_quarantine_is_reverified_and_cannot_hide_known_omissions(known_omission):
    from backend.tests.test_unified_fact_framework import simple_schema
    from review_v2.unified_facts.pipeline import extract_verified
    stages=[]
    def transport(system,payload,*,stage):
        stages.append(stage)
        if stage=='EXTRACTION':
            return {},packet([observation()],payload['active_concepts'])
        return {},{'candidate_snapshot_hash':payload['candidate_snapshot_hash'],'reviewed_clause_ids':['C1','C2'],'searched_concepts':payload['active_concepts'],
            'checks':[{'fact_id':f['fact_id'],'supported':f['state']=='UNKNOWN',**({'correction':observation(state='UNKNOWN')} if f['state']!='UNKNOWN' else {})} for f in payload['candidates']],
            'audits':[{'concept':k,'reviewed_clause_ids':['C1','C2'],'complete':True,
                'omitted_facts':[observation()] if known_omission else [],
                'reason':'protocol fixture'} for k in payload['active_concepts']]}
    if known_omission:
        with pytest.raises(FactExtractionError,match='KNOWN_OMISSION_CANNOT_BE_QUARANTINED'):
            extract_verified(SOURCE,CLAUSES,simple_schema(),transport=transport)
        assert 'QUARANTINE_VERIFICATION' not in stages
    else:
        store=extract_verified(SOURCE,CLAUSES,simple_schema(),transport=transport)
        assert 'QUARANTINE_VERIFICATION' in stages
        assert store.state('test.value')=='UNKNOWN'
        assert store.get('test.value',consumer='test')==[]
        assert all('normalized_value' not in f for f in store.snapshot())
        assert store.debug['quarantines']


def test_partial_quote_binding_uses_raw_original_whitespace():
    from review_v2.clause_parser import parse_contract_clauses
    source = '借款合同\n第一条 金额\n本金人民币壹万叁仟元。\n\n第二条 期限\n借款期限六个月。'
    clauses = parse_contract_clauses(source)
    s = schema()
    active = s.select([])
    clause = next(c for c in clauses if '本金' in c.text)
    raw = source[clause.start_offset:clause.end_offset]
    rows = [obs(k, state='ABSENT') for k in active]
    row = next(r for r in rows if r['concept'] == 'loan.principal')
    row.update(state='PRESENT', value={'amount':'壹万叁仟','currency':'CNY'},
        evidence=[{'clause_id':clause.clause_id,'quote':raw}])
    packet = {'schema_version':s.version,'searched_concepts':list(active),
        'reviewed_clause_ids':[c.clause_id for c in clauses],'observations':rows}
    c = CandidateStore(source, clauses, s, active, packet)
    fact = next(f for f in c.observations if f['concept']=='loan.principal')
    for ref in fact['evidence']:
        assert source[ref['source_start']:ref['source_end']] == ref['quote'] == raw


def test_real_http_file_entry_uses_verified_loan_and_keeps_diagnostics(monkeypatch):
    from fastapi import FastAPI
    from fastapi.testclient import TestClient
    from routers import review_v2 as route
    from pathlib import Path
    def extraction(source, clauses, s):
        active = s.select([])
        ids = [c.clause_id for c in clauses]
        candidate = CandidateStore(source, clauses, s, active, {'schema_version':s.version,
            'reviewed_clause_ids':ids,'searched_concepts':list(active),
            'observations':[obs(k,state='ABSENT') for k in active]})
        v = {'candidate_snapshot_hash':candidate.snapshot_hash,'reviewed_clause_ids':ids,'searched_concepts':list(active),
            'checks':[{'fact_id':f['fact_id'],'supported':True} for f in candidate.observations],
            'audits':[{'concept':k,'reviewed_clause_ids':ids,'complete':True,'omitted_facts':[],
                'reason':'HTTP integration mock verifier, not a semantic acceptance claim'} for k in active]}
        return commit(candidate,v)
    monkeypatch.setattr(loan_pipeline,'extract_verified',extraction)
    monkeypatch.setattr(route.review_engine_module,'_review_contract_v2_legacy',lambda *a,**k:pytest.fail('legacy report'))
    app=FastAPI()
    app.include_router(route.router)
    app.dependency_overrides[route.get_current_user]=lambda:{'id':1}
    path=next((Path(__file__).resolve().parents[2]/'test_data').glob('72 *.docx'))
    with TestClient(app) as client:
        response=client.post('/review-v2/file',data={'contract_type':'loan','use_llm':'false'},
            files={'file':(path.name,path.read_bytes(),'application/vnd.openxmlformats-officedocument.wordprocessingml.document')})
    assert response.status_code==200,response.text
    data=response.json()
    assert data['fact_migration']['mode']=='VERIFIED_FACTS'
    assert data['all_items_count']==48
    assert data['structured_fact_debug']['facts']
    assert data['statistics_consistency_gate']['status']=='REPORT_READY'
    monkeypatch.setattr(loan_pipeline,'extract_verified',lambda *a,**k: (_ for _ in ()).throw(FactExtractionError('REJECTED_BY_VERIFIER')))
    with TestClient(app) as client:
        response=client.post('/review-v2/checklist',json={'contract_type':'loan','contract_text':'借款合同\n本金人民币一万元。'})
    assert response.status_code==503
    assert response.json()['detail']['release_quality_gate']=='BLOCKED'
    assert 'result' not in response.json()
