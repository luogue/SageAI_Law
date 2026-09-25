from backend.tests.test_employment_rule_adapter import adaptation_only_engine
"""Final-report regressions: model labels cannot override verified facts."""
from copy import deepcopy
import pytest

from review_v2.clause_parser import parse_contract_clauses
from review_v2.employment_fact_store import FactStore
from review_v2.employment_fact_schema import CONCEPTS
from review_v2.fact_validation import FactExtractionError
from review_v2.fact_verification import verified_store, validate_projection
from backend.tests.test_employment_fact_pipeline import fact, packet, verified_packet

TEXT = '劳动合同\n第一条 薪酬\n正常月薪为人民币21,300元。\n第二条 支付\n每月十日发放。\n第三条 方式\n通过银行转账。'


def candidates():
    cs=parse_contract_clauses(TEXT)
    fs=[fact(cs,'salary.regular',{'amount_text':'21,300','unit':'CNY/MONTH'},'正常月薪为人民币21,300元。'),
        fact(cs,'salary.payment_date','每月十日','每月十日发放。'),
        fact(cs,'salary.payment_method','BANK','通过银行转账。')]
    return cs,fs


@pytest.mark.parametrize('count,expected',[(3,'通过'),(1,'部分覆盖'),(0,'缺失')])
def test_final_report_coverage_only_uses_verified_facts(monkeypatch,count,expected):
    from review_v2 import employment_fact_pipeline as p
    from review_v2.engine import review_contract_v2
    cs,fs=candidates()
    monkeypatch.setattr(p,'extract',lambda *a,**k:packet(cs,fs[:count]))
    monkeypatch.setattr(p,'verify',verified_packet)
    result=review_contract_v2(TEXT,'labor',use_llm=False)
    row=next(r for r in result['items'] if r['item_id']=='EMP-06-01')
    assert row['coverage_status']==expected
    assert result['release_quality_gate']['status']=='REPORT_READY'
    debug=result['structured_fact_debug']
    assert debug['rule_decisions']['EMP-06-01']['status']==expected
    if count==3:
        assert len({e['clause_id'] for e in row['evidence_clauses']})==3
    assert len(debug['rule_decisions']['EMP-06-01']['verified_fact_projection'])==3


def test_legacy_model_absent_cannot_erase_verified_explicit_fact():
    cs,fs=candidates(); extracted=FactStore(TEXT,cs,packet(cs,fs))
    v=verified_packet(cs,extracted)
    data=v['verification'];data.pop('searched_concepts');data.pop('verification_schema_version')
    data['coverage']={c:'ABSENT' for c in CONCEPTS}
    final=verified_store(extracted,v)
    assert final.element('employment_wage_1')
    assert final.coverage['salary.regular']=='EXTRACTED'
    assert len(final.coverage_reconciliation)==3
    assert final.facts[0]['origin_fact_id']==extracted.facts[0]['fact_id']


def test_inferred_addition_is_uncertain_not_explicit_or_missing():
    text='劳动合同\n每周工作四天，每天工作七小时。'
    cs=parse_contract_clauses(text); extracted=FactStore(text,cs,packet(cs,[]))
    v=verified_packet(cs,extracted)
    v['verification'].pop('searched_concepts');v['verification'].pop('verification_schema_version')
    v['verification']['coverage']={c:'ABSENT' for c in CONCEPTS}
    f=fact(cs,'working_hours.hours_per_week',28,'每周工作四天，每天工作七小时。')
    f['assertion']='INFERRED';v['verification']['additional_facts']=[f]
    final=verified_store(extracted,v)
    assert final.coverage['working_hours.hours_per_week']=='UNCERTAIN'
    assert not final.get('working_hours.hours_per_week')
    assert final.verification_states['working_hours.hours_per_week']['verification_state']=='VERIFIED_INFERRED_OR_LOW_CONFIDENCE'


def test_verification_schema_failure_blocks_pipeline_after_single_repair(monkeypatch):
    from review_v2 import employment_fact_pipeline as p
    cs,fs=candidates()
    monkeypatch.setattr(p,'extract',lambda *a,**k:packet(cs,fs))
    def broken(clauses,store):
        v=verified_packet(clauses,store);v['verification']['checks'][0]['fact_id']='unmapped-fact'
        return v
    monkeypatch.setattr(p,'verify',broken)
    with pytest.raises(FactExtractionError) as err:
        p.run(TEXT,'labor',lambda *a,**k:pytest.fail('no report on failed verification'))
    assert err.value.diagnostics[0]['validation_rule']=='INCOMPLETE_FACT_VERIFICATION'
    assert len(err.value.attempts)==2


def test_rejected_core_fact_blocks_never_missing_or_pass(monkeypatch):
    from review_v2 import employment_fact_pipeline as p
    from review_v2.engine import review_contract_v2
    cs,fs=candidates()
    monkeypatch.setattr(p,'extract',lambda *a,**k:packet(cs,fs))
    def reject(clauses,store):
        v=verified_packet(clauses,store)
        for c in v['verification']['checks']: c['supported']=False
        return v
    monkeypatch.setattr(p,'verify',reject)
    with pytest.raises(FactExtractionError,match='CORE_FACT_VERIFICATION_FAILED') as err:
        review_contract_v2(TEXT,'labor',use_llm=False)
    assert all(d['actual']['coverage_state']=='UNCERTAIN' for d in err.value.diagnostics)


@pytest.mark.parametrize('value',[False,None,''])
def test_false_is_verified_negative_while_null_and_empty_are_invalid(value):
    text='劳动合同\n员工个人部分无需代扣。';cs=parse_contract_clauses(text)
    f=fact(cs,'social_insurance.employee_withheld',value,'员工个人部分无需代扣。')
    if value is False:
        extracted=FactStore(text,cs,packet(cs,[f])); final=verified_store(extracted,verified_packet(cs,extracted))
        assert final.coverage[f['concept']]=='EXTRACTED'
        assert final.values(f['concept'])==[False]
        assert not final.get(f['concept'])
    else:
        with pytest.raises(FactExtractionError,match='FACT_STORE_VALIDATION_FAILED'):
            FactStore(text,cs,packet(cs,[f]))


def test_normalized_value_alias_is_boundary_only_and_conflicts_block():
    cs,fs=candidates(); f=deepcopy(fs[1]);f['normalized_value']=f.pop('value')
    extracted=FactStore(TEXT,cs,packet(cs,[f]));final=verified_store(extracted,verified_packet(cs,extracted))
    assert final.values('salary.payment_date')==['每月十日']
    f['value']='每月二十日'
    with pytest.raises(FactExtractionError) as e: FactStore(TEXT,cs,packet(cs,[f]))
    assert e.value.diagnostics[0]['validation_rule']=='CONFLICTING_VALUE_FIELDS'


def test_same_concept_multiple_evidence_preserved():
    text='劳动合同\n第一条\n每月十日发放。\n第二条\n次月十日结算奖金。';cs=parse_contract_clauses(text)
    fs=[fact(cs,'salary.payment_date',v,q) for v,q in [('每月十日','每月十日发放。'),('次月十日','次月十日结算奖金。')]]
    extracted=FactStore(text,cs,packet(cs,fs)); final=verified_store(extracted,verified_packet(cs,extracted))
    assert len(final.get('salary.payment_date'))==2
    assert len({e['clause_id'] for e in final.element('employment_wage_2')})==2


@pytest.mark.parametrize('reverse',[False,True])
def test_duplicate_fact_merge_cannot_reset_confirmed_state(reverse):
    cs,fs=candidates(); explicit=fs[1]; inferred=deepcopy(explicit)
    inferred.update(assertion='INFERRED',confidence=.6)
    rows=[explicit,inferred] if reverse else [inferred,explicit]
    extracted=FactStore(TEXT,cs,packet(cs,rows));final=verified_store(extracted,verified_packet(cs,extracted))
    assert len(final.facts)==1
    assert final.coverage['salary.payment_date']=='EXTRACTED'
    assert final.element('employment_wage_2')


def test_rejected_hypothesis_is_unknown_context_not_absence():
    cs,fs=candidates(); f=fs[1];f['assertion']='INFERRED'
    extracted=FactStore(TEXT,cs,packet(cs,[f]));v=verified_packet(cs,extracted)
    v['verification']['checks'][0]['supported']=False
    final=verified_store(extracted,v)
    assert final.coverage[f['concept']]=='UNCERTAIN'
    with pytest.raises(FactExtractionError,match='CANNOT_PROVE_ABSENCE'):final.absence_proof('employment_wage_2')


def test_rejected_negative_boolean_stays_unknown_for_manual_review():
    text='劳动合同\n单位承担保险费用。';cs=parse_contract_clauses(text)
    f=fact(cs,'social_insurance.waived',False,'单位承担保险费用。')
    extracted=FactStore(text,cs,packet(cs,[f]));v=verified_packet(cs,extracted)
    v['verification']['checks'][0]['supported']=False
    final=verified_store(extracted,v)
    assert final.coverage[f['concept']]=='UNCERTAIN'
    assert not final.get(f['concept'],positive=False)
    assert final.pending_reason('employment_illegal_waiver')


def test_conflict_gate_still_blocks_mutated_projection():
    cs,fs=candidates();extracted=FactStore(TEXT,cs,packet(cs,fs)); final=verified_store(extracted,verified_packet(cs,extracted))
    final.coverage['salary.regular']='ABSENT'
    with pytest.raises(FactExtractionError,match='VERIFICATION_COVERAGE_CONFLICT'): validate_projection(final)


def test_incomplete_or_unknown_verification_schema_does_not_fallback():
    cs,fs=candidates();extracted=FactStore(TEXT,cs,packet(cs,fs));v=verified_packet(cs,extracted)
    v['verification']['verification_schema_version']='unknown'
    with pytest.raises(FactExtractionError,match='UNSUPPORTED_VERIFICATION_SCHEMA'): verified_store(extracted,v)
    v=verified_packet(cs,extracted);v['verification']['searched_concepts'].remove('salary.regular')
    with pytest.raises(FactExtractionError,match='INCOMPLETE_VERIFICATION_SCOPE'): verified_store(extracted,v)


def test_extraction_search_attestation_derives_states_without_model_coverage():
    cs,fs=candidates();raw=packet(cs,fs[:1]);data=raw[0]['response']
    data.pop('coverage');data.update(searched_concepts=list(CONCEPTS),unresolved_concepts=[])
    store=FactStore(TEXT,cs,raw)
    assert store.coverage['salary.regular']=='EXTRACTED'
    assert store.coverage['salary.payment_date']=='ABSENT'
    final=verified_store(store,verified_packet(cs,store))
    assert final.element('employment_wage_1')
    assert not final.element('employment_wage_2')


def test_no_string_confidence_coercion():
    cs,fs=candidates();f=fs[1];f['confidence']='EXPLICIT'
    with pytest.raises(FactExtractionError) as err:FactStore(TEXT,cs,packet(cs,[f]))
    assert err.value.diagnostics[0]['validation_rule']=='INVALID_CONFIDENCE'


def test_verified_deferred_arrangement_remains_not_applicable(monkeypatch):
    from review_v2 import employment_fact_pipeline as p
    from review_v2.engine import review_contract_v2
    text='劳动合同\n如未来安排专项技术培训，双方届时另行签订服务期协议。'
    cs=parse_contract_clauses(text);fs=[fact(cs,'training.arrangement','DEFERRED',cs[-1].text)]
    monkeypatch.setattr(p,'extract',lambda *a,**k:packet(cs,fs))
    monkeypatch.setattr(p,'verify',verified_packet)
    r=review_contract_v2(text,'labor',use_llm=False)
    assert next(i for i in r['items'] if i['item_id']=='EMP-09-01')['coverage_status']=='不适用'


def test_pending_fact_names_are_readable_without_hiding_uncertainty():
    text='劳动合同\n单位承担保险费用。';cs=parse_contract_clauses(text)
    f=fact(cs,'social_insurance.waived',False,'单位承担保险费用。');f['assertion']='INFERRED'
    extracted=FactStore(text,cs,packet(cs,[f]));store=verified_store(extracted,verified_packet(cs,extracted))
    reason=store.pending_reason('employment_illegal_waiver')
    assert '需核验' in reason and 'social_insurance.' not in reason
    assert store.coverage[f['concept']]=='UNCERTAIN'


def test_unresolved_required_fact_gets_one_diagnostic_recheck(monkeypatch):
    from review_v2 import employment_fact_pipeline as p
    cs,fs=candidates();calls=[]
    def extract(*args,**kwargs):
        calls.append(kwargs)
        if not kwargs:return scoped_labor_packet(cs,fs[1:])
        from review_v2.fact_dependencies import ROOTS
        assert set(kwargs['concept_keys'])=={'salary.regular', *ROOTS}
        raw=packet(cs,fs[:1]);raw[0]['response'].pop('coverage')
        raw[0]['response'].update(searched_concepts=kwargs['concept_keys'],unresolved_concepts=[])
        return raw
    def verify(clauses,store):
        v=verified_packet(clauses,store)
        v['verification']['searched_concepts']=list(store.active_concepts)
        if not store.get('salary.regular'):v['verification']['unresolved_concepts']=['salary.regular']
        return v
    monkeypatch.setattr(p,'extract',extract);monkeypatch.setattr(p,'verify',verify)
    result=p.run(TEXT,'labor',adaptation_only_engine)
    assert len(calls)==2 and 'salary.regular' in calls[1]['validation_feedback']
    assert result['structured_fact_debug']['verified_coverage']['salary.regular']=='EXTRACTED'
    assert result['structured_fact_debug']['verified_coverage']['salary.payment_date']=='EXTRACTED'
    assert result['structured_fact_debug']['deepseek_raw_results'][0]['kind']=='VERIFIED_REPAIR_SEED'


def test_full_document_topic_batches_share_uncertainty_without_losing_facts():
    cs,fs=candidates();keys=list(CONCEPTS);groups=[keys[:35],keys[35:]]
    raw=[]
    for group in groups:
        raw.append({'response':{'schema_version':packet(cs,[])[0]['response']['schema_version'],
            'reviewed_clause_ids':[c.clause_id for c in cs],'searched_concepts':group,
            'unresolved_concepts':['salary.payment_date'],
            'facts':[f for f in fs[:1] if f['concept'] in group]}})
    store=FactStore(TEXT,cs,raw)
    assert store.coverage['salary.regular']=='EXTRACTED'
    assert store.coverage['salary.payment_date']=='UNCERTAIN'


def test_failed_core_fact_repair_retains_other_verified_facts(monkeypatch):
    from review_v2 import employment_fact_pipeline as p
    cs,fs=candidates();calls=[];bad=deepcopy(fs);bad[0]['value']['amount_text']='999'
    def extract(*args,**kwargs):
        calls.append(kwargs)
        if not kwargs:return scoped_labor_packet(cs,bad)
        from review_v2.fact_dependencies import ROOTS
        assert set(kwargs['concept_keys'])=={'salary.regular', *ROOTS}
        raw=packet(cs,fs[:1]);raw[0]['response'].pop('coverage')
        raw[0]['response'].update(searched_concepts=kwargs['concept_keys'],unresolved_concepts=[])
        return raw
    def verify(clauses,store):
        v=verified_packet(clauses,store)
        for c in v['verification']['checks']:
            f=store.by_id[c['fact_id']]
            if f['concept']=='salary.regular':c['supported']=f['normalized_value']['amount']==21300
        v['verification']['searched_concepts']=list(store.active_concepts)
        return v
    monkeypatch.setattr(p,'extract',extract);monkeypatch.setattr(p,'verify',verify)
    r=p.run(TEXT,'labor',adaptation_only_engine)['structured_fact_debug']
    assert len(calls)==2
    assert r['verified_coverage']['salary.payment_date']=='EXTRACTED'
    assert r['employment']['salary']['regular'][0]['normalized_value']['amount']==21300


def scoped_labor_packet(clauses, facts):
    from review_v2.fact_modules import select
    active=list(select(CONCEPTS,facts,'labor'))
    raw=packet(clauses,facts)
    raw[0]['active_concepts']=active
    raw[0]['response']['coverage']={k:v for k,v in raw[0]['response']['coverage'].items() if k in active}
    return raw
