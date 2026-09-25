"""Provider boundary, normalized values, original-source and final report tests."""
import pytest

from review_v2.clause_parser import parse_contract_clauses
from review_v2.deepseek_facts import FactExtractionError
from review_v2.employment_fact_schema import CONCEPTS, SCHEMA_VERSION
from review_v2.employment_fact_store import CURRENT, FactStore, number


def packet(clauses, facts):
    return [{'response':{'schema_version':SCHEMA_VERSION, 'reviewed_clause_ids':[c.clause_id for c in clauses],
        'coverage':{k:'EXTRACTED' if any(f['concept']==k for f in facts) else 'ABSENT' for k in CONCEPTS},
        'facts':facts}, 'provider':'deepseek','model':'test-fixture'}]


def verified_packet(clauses, store):
    return {'provider':'deepseek','model':'test-fixture','verification':{
        'verification_schema_version':'fact-verification-2',
        'checks':[{'fact_id':f['fact_id'],'supported':True} for f in store.facts],
        'searched_concepts':list(CONCEPTS),'unresolved_concepts':[],
        'reviewed_clause_ids':[c.clause_id for c in clauses],'additional_facts':[]}}


def fact(clauses, concept, value, quote):
    c = next(c for c in clauses if quote in c.text)
    return {'concept':concept,'value':value,'confidence':1,'assertion':'EXPLICIT',
            'evidence':[{'clause_id':c.clause_id,'quote':quote}]}


@pytest.mark.parametrize('text', ['13000','13,000','13，000','壹万叁仟','一万三千'])
def test_money_normalization(text):
    assert number(text) == 13000


def test_cross_clause_fact_composition_and_source_binding():
    text = '劳动合同\n第一条\n用工机构负责办理参保。\n第二条\n单位负担单位部分缴费。'
    cs = parse_contract_clauses(text)
    fs = [fact(cs,'social_insurance.employer_enrolls',True,'用工机构负责办理参保。'),
          fact(cs,'social_insurance.employer_pays',True,'单位负担单位部分缴费。')]
    store = FactStore(text,cs,packet(cs,fs))
    evidence = store.element('employment_insurance_1')
    assert len({e['clause_id'] for e in evidence}) == 2
    for ev in evidence:
        clause = next(c for c in cs if c.clause_id == ev['clause_id'])
        span = ev['evidence_span']
        assert clause.text[span['start']:span['end']] == ev['quote']


def test_full_extraction_attestation_required_before_absence():
    cs = parse_contract_clauses('劳动合同\n岗位另议。')
    raw = packet(cs,[])
    raw[0]['response']['coverage'].pop('salary.regular')
    with pytest.raises(FactExtractionError,match='INCOMPLETE_CONCEPT'):
        FactStore('劳动合同\n岗位另议。',cs,raw)


def test_fabricated_evidence_is_rejected():
    cs = parse_contract_clauses('劳动合同\n工资另议。')
    f = fact(cs,'salary.payment_method','BANK','工资另议。')
    f['evidence'][0]['quote'] = '银行转账支付工资。'
    with pytest.raises(FactExtractionError,match='EVIDENCE_NOT_IN_CLAUSE'):
        FactStore('劳动合同\n工资另议。',cs,packet(cs,[f]))


def test_repeated_quote_keeps_the_selected_clause_span():
    text = '劳动合同\n第一条 工资\n每月结算。\n第二条 补偿\n离职后依法支付补偿。每月结算。'
    cs = parse_contract_clauses(text)
    selected = next(c for c in cs if '离职后依法支付补偿' in c.text)
    f = fact(cs,'economic_compensation.settlement_deadline','每月结算','每月结算。')
    f['evidence'][0]['clause_id'] = selected.clause_id
    store = FactStore(text,cs,packet(cs,[f]))
    ev = store.facts[0]['evidence'][0]
    assert ev['clause_id'] == selected.clause_id
    assert selected.text[ev['source_start']:ev['source_end']] == '每月结算。'
    if ev['document_span']:
        assert ev['document_span']['start'] == text.rindex('每月结算。')


def test_invalid_model_date_fails_as_fact_validation():
    text = '劳动合同\n起始日期另议。'
    cs = parse_contract_clauses(text)
    f = fact(cs,'contract.start_date','2027-02-31','起始日期另议。')
    with pytest.raises(FactExtractionError,match='INVALID_FACT_VALUE'):
        FactStore(text,cs,packet(cs,[f]))


def test_positive_and_conflicting_social_facts_coexist():
    text = '劳动合同\n单位缴纳社会保险。同时允许员工申请现金替代单位缴费。'
    cs = parse_contract_clauses(text)
    fs = [fact(cs,'social_insurance.employer_pays',True,'单位缴纳社会保险。'),
          fact(cs,'social_insurance.cash_replacement',True,'同时允许员工申请现金替代单位缴费。')]
    store = FactStore(text,cs,packet(cs,fs))
    assert store.get('social_insurance.employer_pays')
    assert store.adverse('employment_illegal_waiver')


def test_rule_consumes_all_penalties_and_respects_legal_scope():
    text = '劳动合同\n辞职约定违约金。保密约定违约金。竞业约定违约金。'
    cs = parse_contract_clauses(text)
    fs = [fact(cs,'penalties.obligations',{'scope':scope,'imposed':True,'amount_text':'一个月工资'},q) for scope,q in [
        ('ORDINARY_RESIGNATION','辞职约定违约金。'),('CONFIDENTIALITY','保密约定违约金。'),('NON_COMPETE','竞业约定违约金。')]]
    store = FactStore(text,cs,packet(cs,fs))
    evidence = store.adverse('employment_general_penalty')
    assert len(evidence) == 2
    assert all('竞业约定' not in e['text'] for e in evidence)


def test_final_report_uses_facts_not_lexical_recall(monkeypatch):
    from review_v2 import employment_fact_pipeline as pipeline
    from review_v2.engine import review_contract_v2
    text = '劳动合同\n第一条 工资\n试用阶段报酬壹万叁仟元每月。正常阶段每月壹万伍仟元。\n第二条 劳动保护\n配备劳动防护设施。'
    cs = parse_contract_clauses(text)
    fs = [fact(cs,'probation.arrangement','CURRENT','试用阶段报酬壹万叁仟元每月。'),
          fact(cs,'probation.salary',{'amount_text':'壹万叁仟','unit':'CNY/MONTH'},'试用阶段报酬壹万叁仟元每月。'),
          fact(cs,'salary.regular',{'amount_text':'壹万伍仟','unit':'CNY/MONTH'},'正常阶段每月壹万伍仟元。'),
          fact(cs,'labor_protection.measures','防护设施','配备劳动防护设施。')]
    monkeypatch.setattr(pipeline,'extract',lambda _:packet(cs,fs))
    monkeypatch.setattr(pipeline,'verify',verified_packet)
    result = review_contract_v2(text,'labor',use_llm=False)
    rows = {r['item_id']:r for r in result['items']}
    assert rows['EMP-03-01']['coverage_status'] == '部分覆盖'
    assert rows['EMP-06-01']['coverage_status'] == '部分覆盖'
    # Protection is covered; unwritten training is optional. Only the actual
    # existence of occupational hazards remains a separate verification.
    assert rows['EMP-08-01']['coverage_status'] == '待核验'
    assert rows['EMP-08-01']['action_priority'] == 'NONE'
    assert any(e['element_id'] == 'employment_safety_1' and e['status'] == 'COVERED'
               for e in rows['EMP-08-01']['coverage_elements'])
    assert rows['EMP-11-01']['coverage_status'] == '缺失'
    assert result['structured_fact_debug']['provider'] == 'deepseek'
    assert CURRENT.get() is None


def test_partial_conjunction_survives_to_final_report(monkeypatch):
    from review_v2 import employment_fact_pipeline as pipeline
    from review_v2.engine import review_contract_v2
    text = '劳动合同\n单位办理参保登记。'
    cs = parse_contract_clauses(text)
    fs = [fact(cs,'social_insurance.employer_enrolls',True,'单位办理参保登记。')]
    monkeypatch.setattr(pipeline,'extract',lambda _:packet(cs,fs))
    monkeypatch.setattr(pipeline,'verify',verified_packet)
    result = review_contract_v2(text,'labor')
    row = next(r for r in result['items'] if r['item_id']=='EMP-07-01')
    assert row['coverage_status'] == '部分覆盖'
    assert {'COVERED','MISSING'} <= {e['status'] for e in row['coverage_elements']}
    assert result['release_quality_gate']['status'] == 'REPORT_READY'


def test_uncertain_extraction_cannot_become_absence_audit():
    text = '劳动合同\n按另附标准执行。'
    cs = parse_contract_clauses(text)
    raw = packet(cs,[])
    raw[0]['response']['coverage']['salary.regular'] = 'UNCERTAIN'
    store = FactStore(text,cs,raw)
    with pytest.raises(FactExtractionError,match='CANNOT_PROVE_ABSENCE'):
        store.absence_proof('employment_wage_1')


def test_transport_calls_only_deepseek_and_no_fallback(monkeypatch):
    from review_v2 import deepseek_facts as transport
    calls = []
    monkeypatch.setattr(transport,'configuration',lambda:{'key':'test-only','url':'https://api.deepseek.com/v1/chat/completions','model':'deepseek-chat'})
    class Response:
        status_code = 429
    def post(url,**kwargs):
        calls.append(url)
        return Response()
    monkeypatch.setattr(transport.requests,'post',post)
    with pytest.raises(FactExtractionError,match='DEEPSEEK_HTTP_429'):
        transport.extract(parse_contract_clauses('劳动合同'))
    assert calls == ['https://api.deepseek.com/v1/chat/completions']


def test_failures_do_not_fall_back_to_old_verdict_engine(monkeypatch):
    from review_v2 import employment_fact_pipeline as pipeline
    def unavailable(*args,**kwargs):
        raise FactExtractionError('DEEPSEEK_NOT_CONFIGURED')
    monkeypatch.setattr(pipeline,'extract',unavailable)
    def forbidden(*args,**kwargs):
        pytest.fail('Legacy verdict engine must not run without extracted facts')
    with pytest.raises(FactExtractionError):
        pipeline.run('劳动合同','labor',forbidden)
    assert CURRENT.get() is None


def test_unquantified_variable_pay_cannot_cover_wage():
    from review_v2.employment_fact_store import normalize
    value = normalize('salary.regular',{'amount_text':'绩效工资','formula':'按公司制度执行'})
    assert value['determinate'] is False
    assert normalize('salary.regular',{'formula':'按2028年度工资制度'})['determinate'] is False
    assert normalize('probation.salary',{'formula':{'kind':'PERCENT_OF_BASE','percent':80,'base':'REGULAR_SALARY'},'unit':'CNY/MONTH'})['determinate'] is True


@pytest.mark.parametrize('beneficiary,mode,expected', [
    ('EMPLOYER','AUTOMATIC',True),('EMPLOYEE','AUTOMATIC',False),
    ('EMPLOYER','SEPARATE_AGREEMENT',False),('UNSPECIFIED','STATUTORY',False),
])
def test_ip_risk_uses_relational_fact_not_subject_mention(beneficiary,mode,expected):
    text = '劳动合同\n成果的范围、权利人及处置方式按本条明确约定。'
    cs = parse_contract_clauses(text)
    f = fact(cs,'ip.allocations',{'scope':'NON_DUTY','beneficiary':beneficiary,'mode':mode},
             '成果的范围、权利人及处置方式按本条明确约定。')
    store = FactStore(text,cs,packet(cs,[f]))
    assert bool(store.adverse('employment_ip_ownership')) is expected


@pytest.mark.parametrize('concept,value,node,expected', [
    ('working_hours.rest_days_per_week',0,'employment_hours',True),
    ('working_hours.rest_days_per_week',2,'employment_hours',False),
    ('social_insurance.employer_underpays',True,'employment_illegal_waiver',True),
    ('social_insurance.employee_remedy_excluded',True,'employment_illegal_waiver',True),
    ('economic_compensation.statutory_percentage',60,'employment_compensation',True),
    ('economic_compensation.statutory_percentage',100,'employment_compensation',False),
    ('economic_compensation.payment_delay_months',6,'employment_compensation',True),
])
def test_existing_adverse_thresholds_consume_values(concept,value,node,expected):
    text = '劳动合同\n双方就本项标准作出明确约定。'
    cs = parse_contract_clauses(text)
    f = fact(cs,concept,value,'双方就本项标准作出明确约定。')
    store = FactStore(text,cs,packet(cs,[f]))
    assert bool(store.adverse(node)) is expected


def test_task_contract_cannot_gain_probation_allowance_from_its_dates():
    text = '劳动合同\n本合同以完成约定任务为期限。预计从2027年1月1日至2029年12月31日。约定试用一个月。'
    cs = parse_contract_clauses(text)
    fs = [fact(cs,'contract.type','TASK','本合同以完成约定任务为期限。'),
          fact(cs,'contract.start_date','2027-01-01','预计从2027年1月1日至2029年12月31日。'),
          fact(cs,'contract.end_date','2029-12-31','预计从2027年1月1日至2029年12月31日。'),
          fact(cs,'probation.duration_months',1,'约定试用一个月。')]
    store = FactStore(text,cs,packet(cs,fs))
    assert store.adverse('employment_probation_limit')
