from backend.tests.test_employment_rule_adapter import adaptation_only_engine
"""Public diagnostics, formatting-only alignment, quarantine and repair budget."""
from copy import deepcopy
import json
import pytest

from review_v2.clause_parser import parse_contract_clauses
from review_v2.deepseek_facts import FactExtractionError
from review_v2.fact_validation import bind_quote
from review_v2.employment_fact_store import FactStore
from backend.tests.test_employment_fact_pipeline import fact, packet, verified_packet


@pytest.mark.parametrize('source,model', [
    ('## 第三条 工资\n**月薪**：人民币18,750元／月。','第三条 工资\n月薪:人民币18,750元/月。'),
    ('单位办理社会保险\n手续，并依法\n承担缴费义务。','单位办理社会保险手续,并依法承担缴费义务。'),
    ('工资：人民币１８７５０元／月。','工资:人民币18750元/月.'),
    ('“安全教育”：由单位组织。','"安全教育":由单位组织。'),
    ('工资：19,250元/月。','**工资：19,250元/月。**'),
])
def test_typographic_alignment_maps_back_to_source(source,model):
    start,end,mode = bind_quote(source,model)
    assert source[start:end]
    assert mode == 'FORMATTING_NORMALIZED'
    from review_v2.fact_validation import canonical_view
    assert canonical_view(source[start:end])[0] == canonical_view(model)[0]


@pytest.mark.parametrize('source,forged', [
    ('不支付补偿。','支付补偿。依法办理离职。'),
    ('月薪19,250元。','月薪19,500元。'),
    ('工资账户：____________','工资账户：123456'),
    ('工资100元。不得扣除。','工资100元。允许扣除。'),
])
def test_formatting_normalization_cannot_invent_text(source,forged):
    with pytest.raises(FactExtractionError,match='EVIDENCE_NOT_IN_CLAUSE'):
        bind_quote(source,forged)


def test_redaction_markers_are_not_removed_as_markdown():
    from review_v2.fact_validation import canonical_view
    assert canonical_view('身份证：____________')[0] == '身份证:____________'


def test_cross_clause_fact_binding_survives_formatted_model_quotes():
    text = '劳动合同\n第一条\n**单位**办理参保手续。\n第二条\n单位缴费：依法承担。'
    cs = parse_contract_clauses(text)
    fs = [fact(cs,'social_insurance.employer_enrolls',True,'单位办理参保手续。'),
          fact(cs,'social_insurance.employer_pays',True,'单位缴费：依法承担。')]
    fs[0]['evidence'][0]['quote']='**单位**办理参保手续。'
    fs[1]['evidence'][0]['quote']='单位缴费:依法承担。'
    store=FactStore(text,cs,packet(cs,fs))
    bound=store.element('employment_insurance_1')
    assert len({e['clause_id'] for e in bound})==2
    assert all(e['quote'] in next(c.text for c in cs if c.clause_id==e['clause_id']) for e in bound)


@pytest.mark.parametrize('mutation,stage,field', [
    (lambda f:f.pop('value'),'FACT_SCHEMA','value'),
    (lambda f:f.update(value=[]),'NORMALIZATION','value'),
    (lambda f:f.update(evidence=[]),'EVIDENCE_BINDING','evidence'),
    (lambda f:f['evidence'][0].update(clause_id='missing'),'EVIDENCE_BINDING','evidence.clause_id'),
    (lambda f:f['evidence'][0].update(quote='原文不存在的工资条款'),'EVIDENCE_BINDING','evidence.quote'),
    (lambda f:f.update(confidence='high'),'FACT_SCHEMA','confidence'),
    (lambda f:f.update(assertion='TRUE'),'FACT_SCHEMA','assertion'),
])
def test_field_failures_have_complete_diagnostics(mutation,stage,field):
    text='劳动合同\n正常月薪18,750元。'
    cs=parse_contract_clauses(text)
    f=fact(cs,'salary.regular',{'amount_text':'18,750','unit':'CNY/MONTH'},'正常月薪18,750元。')
    mutation(f)
    with pytest.raises(FactExtractionError) as caught:
        FactStore(text,cs,packet(cs,[f]))
    d=caught.value.diagnostics[0]
    assert d['failed_stage']==stage and d['field']==field
    assert {'failed_stage','fact_id','field','validation_rule','model_raw_value','evidence','expected','actual'} <= d.keys()
    assert d['fact_id'] and d['disposition']=='BLOCK'


def test_conditional_unknown_is_quarantined_not_missing_or_covered():
    text='劳动合同\n如岗位涉及职业危害，单位依法防护。'
    cs=parse_contract_clauses(text)
    f=fact(cs,'labor_protection.hazard_exists',None,'如岗位涉及职业危害，单位依法防护。')
    raw=packet(cs,[f])
    raw[0]['response']['coverage'][f['concept']]='UNCERTAIN'
    store=FactStore(text,cs,raw)
    assert not store.facts
    assert store.coverage[f['concept']]=='UNCERTAIN'
    assert store.validation_diagnostics[0]['disposition']=='QUARANTINE_AND_MANUAL_REVIEW'
    f['evidence'][0]['quote']='岗位实际存在粉尘危害。'
    with pytest.raises(FactExtractionError):
        FactStore(text,cs,packet(cs,[f]))


def test_scalar_array_representation_keeps_value_evidence_and_audit():
    text='劳动合同\n合同期满依法终止。'
    cs=parse_contract_clauses(text)
    f=fact(cs,'termination.grounds','合同期满依法终止','合同期满依法终止。')
    store=FactStore(text,cs,packet(cs,[f]))
    assert store.facts[0]['normalized_value']==['合同期满依法终止']
    assert store.element('employment_exit_1')
    assert store.normalization_events[0]['transformation']=='SINGLETON_ARRAY'
    f['value']=['合同期满',123]
    with pytest.raises(FactExtractionError,match='INVALID_LIST'):
        FactStore(text,cs,packet(cs,[f]))


def test_single_deepseek_repair_covers_post_verification_failure(monkeypatch):
    from review_v2 import employment_fact_pipeline as p
    text='劳动合同\n工资明确。'
    cs=parse_contract_clauses(text)
    good=packet(cs,[])
    valid=verified_packet(cs,FactStore(text,cs,good))
    bad=deepcopy(valid); bad['verification']['checks']=[{'fact_id':'unknown','supported':True}]
    calls=[]
    monkeypatch.setattr(p,'extract',lambda *a,**k:(calls.append(k) or good))
    answers=iter([bad,valid])
    monkeypatch.setattr(p,'verify',lambda *a:next(answers))
    result=p.run(text,'labor',adaptation_only_engine)
    assert len(calls)==2 and calls[1]['validation_feedback']
    assert len(result['structured_fact_debug']['validation_attempts'])==2
    assert result['structured_fact_debug']['validation_attempts'][0]['diagnostics'][0]['validation_rule']=='INCOMPLETE_FACT_VERIFICATION'


def test_repeated_invalid_json_stops_after_one_repair(monkeypatch):
    from review_v2 import employment_fact_pipeline as p
    calls=[]
    def broken(*a,**k):
        calls.append(k)
        raise FactExtractionError('INVALID_MODEL_JSON',failed_stage='EXTRACTION_JSON',field='message.content',model_raw_value='{',expected='JSON object')
    monkeypatch.setattr(p,'extract',broken)
    with pytest.raises(FactExtractionError) as caught:
        p.run('劳动合同','labor',lambda *a,**k:pytest.fail('must not run rules'))
    assert len(calls)==2 and len(caught.value.attempts)==2


def test_api_diagnostics_reach_the_business_response(monkeypatch):
    from routers import review_v2 as route
    from fastapi import HTTPException
    def fail(*a,**k):
        raise FactExtractionError('INVALID_ENUM',failed_stage='NORMALIZATION',fact_id='candidate-1',
            field='value',model_raw_value='unexpected',evidence=[],expected=['CURRENT','NONE','DEFERRED'],actual='unexpected')
    monkeypatch.setattr(route,'review_contract_v2',fail)
    with pytest.raises(HTTPException) as caught:
        route._review_with_fact_errors('劳动合同','labor')
    assert caught.value.status_code==503
    detail=caught.value.detail
    assert detail['failed_stage']=='NORMALIZATION' and detail['fact_id']=='candidate-1'
    assert detail['release_quality_gate']=='BLOCKED' and detail['diagnostics']


def test_markdown_json_fence_and_malformed_json_diagnostics():
    from review_v2.deepseek_facts import _model_json
    class Response:
        status_code=200
        content='```json\n{"facts": []}\n```'
        def json(self):
            return {'choices':[{'finish_reason':'stop','message':{'content':self.content}}]}
    response=Response()
    assert _model_json(response,'EXTRACTION')[1]=={'facts':[]}
    response.content='{"facts":'
    with pytest.raises(FactExtractionError) as caught:
        _model_json(response,'EXTRACTION')
    assert caught.value.diagnostics[0]['model_raw_value']==response.content
