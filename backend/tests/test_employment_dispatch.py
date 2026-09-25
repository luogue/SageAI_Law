"""Subtypes, role-bound facts, polarity and final report composition."""
import pytest
from review_v2.clause_parser import parse_contract_clauses
from review_v2.employment_fact_store import FactStore,CURRENT
from review_v2.employment_dispatch import classify,adverse,CHECKLIST
from backend.tests.test_employment_fact_pipeline import fact,packet,verified_packet


def store_for(text, values):
    clauses=parse_contract_clauses(text)
    fs=[fact(clauses,c,v,q) for c,v,q in values]
    return FactStore(text,clauses,packet(clauses,fs))


@pytest.mark.parametrize('form,term,expected',[
    ('DIRECT','FIXED','LABOR'),('DISPATCH','FIXED','LABOR_DISPATCH'),
    ('DIRECT','INDEFINITE','LABOR_INDEFINITE'),('DIRECT','TASK','LABOR_TASK'),
    ('PART_TIME','FIXED','LABOR_PART_TIME'),('DISPATCH','INDEFINITE','LABOR_DISPATCH')])
def test_form_and_term_are_independent(form,term,expected):
    text='劳动合同\n双方在本条约定用工形式及劳动合同期限。'
    s=store_for(text,[(c,v,'双方在本条约定用工形式及劳动合同期限。') for c,v in
                     [('contract.employment_form',form),('contract.type',term)]])
    assert classify(s)['subtype']==expected
    assert classify(s)['term_types']==[term]
    from review_v2.contract_registry import get_checklist
    token=CURRENT.set(s)
    try:
        ids={r.item_id for r in get_checklist('labor')}
        assert ('DSP-01-01' in ids)==(form=='DISPATCH')
        assert {'EMP-14-01','EMP-IP-01'}<=ids
        assert ('PT-01-01' if form=='PART_TIME' else 'EMP-15-01') in ids
    finally:
        CURRENT.reset(token)


@pytest.mark.parametrize('concept,value,node,expected',[
    ('dispatch.equal_pay','LOWER_ALLOWED','equal_pay',False),
    ('dispatch.equal_pay','EQUAL','equal_pay',False),
    ('dispatch.idle_pay','NONE','idle_pay',True),
    ('dispatch.idle_pay','MONTHLY_LOCAL_MINIMUM','idle_pay',False),
    ('dispatch.worker_charges','REQUIRED','charges',True),
    ('dispatch.worker_charges','PROHIBITED','charges',False),
    ('dispatch.refusal_termination','ANY_OFFER','return',True),
    ('dispatch.refusal_termination','MAINTAINED_CONDITIONS','return',False),
    ('dispatch.host_direct_dismissal',False,'return',False),
    ('dispatch.agreement_disclosure',False,'disclosure',True),
])
def test_protective_and_adverse_facts_are_distinct(concept,value,node,expected):
    text='劳动合同\n本条单独规定双方的权利义务。'
    s=store_for(text,[(concept,value,'本条单独规定双方的权利义务。')])
    assert bool(adverse(s,'employment_dispatch_'+node))==expected


@pytest.mark.parametrize('basis,expected',[('AUXILIARY',False),('SUBSTITUTE',False),('REGULAR_CORE',False),(None,False)])
def test_long_term_position_requires_context(basis,expected):
    text='劳动合同\n岗位性质在本条约定。'
    values=[('dispatch.long_term_position',True,'岗位性质在本条约定。')]
    if basis:
        values.append(('dispatch.position_basis',basis,'岗位性质在本条约定。'))
    assert bool(adverse(store_for(text,values),'employment_dispatch_position'))==expected


def test_dispatch_final_report_separates_unproven_comparisons_from_risks(monkeypatch):
    from review_v2 import employment_fact_pipeline as pipeline
    from review_v2.engine import review_contract_v2
    text=('劳动合同\n第一条\n雇主招用后派往客户单位，由客户安排工作。\n'
          '第二条\n岗位属于持续存在的主营业务职位。\n第三条\n相同工作可以采用比客户员工更低的工资。\n'
          '第四条\n待派阶段工资停发。\n第五条\n不接受任何另派工作即无补偿解约。')
    cs=parse_contract_clauses(text)
    fs=[fact(cs,c,v,q) for c,v,q in [
        ('contract.employment_form','DISPATCH','雇主招用后派往客户单位，由客户安排工作。'),
        ('dispatch.position_basis','REGULAR_CORE','岗位属于持续存在的主营业务职位。'),
        ('dispatch.equal_pay','LOWER_ALLOWED','相同工作可以采用比客户员工更低的工资。'),
        ('dispatch.idle_pay','NONE','待派阶段工资停发。'),
        ('dispatch.refusal_termination','ANY_OFFER','不接受任何另派工作即无补偿解约。'),
        ('dispatch.refusal_compensation_waived',True,'不接受任何另派工作即无补偿解约。')]]
    monkeypatch.setattr(pipeline,'extract',lambda *a,**k:packet(cs,fs))
    monkeypatch.setattr(pipeline,'verify',verified_packet)
    result=review_contract_v2(text,'labor',include_low_risk=True)
    items={r['item_id']:r for r in result['items']}
    from review_v2.employment_contract_checklist import LABOR_CHECKLIST
    assert set(items)=={r.item_id for r in LABOR_CHECKLIST+CHECKLIST}
    assert result['contract_type_name']=='劳务派遣劳动合同'
    assert result['report_context']['contract_subtype']=='LABOR_DISPATCH'
    for rule in ('DSP-02-01','DSP-03-01'):
        assert items[rule]['coverage_status'] in ('待核验','INSUFFICIENT_CONTEXT')
    for rule in ('DSP-04-01','DSP-06-01'):
        row=items[rule]
        assert row['coverage_status']=='风险条款'
        assert row['evidence_clauses']
        assert all(e.get('structured_fact_id') and e.get('quote') in text for e in row['evidence_clauses'])
    assert result['release_quality_gate']['status']=='REPORT_READY',str(result['release_quality_gate']['failures'])
    from routers.review_v2 import ReviewV2Result
    public=ReviewV2Result(**result).dict()
    assert public['employment_classification']['subtype']=='LABOR_DISPATCH'
    assert public['report_context']['contract_subtype']=='LABOR_DISPATCH'


@pytest.mark.parametrize('form,term,label',[
    ('DIRECT','FIXED','普通劳动合同'),('DIRECT','INDEFINITE','无固定期限劳动合同'),
    ('DIRECT','TASK','以完成一定工作任务为期限劳动合同'),('PART_TIME','FIXED','非全日制用工')])
def test_direct_employment_does_not_load_dispatch_rules(monkeypatch,form,term,label):
    from review_v2 import employment_fact_pipeline as pipeline
    from review_v2.engine import review_contract_v2
    text='劳动合同\n双方直接建立劳动关系，不实行劳务派遣。'
    cs=parse_contract_clauses(text)
    fs=[fact(cs,c,v,'双方直接建立劳动关系，不实行劳务派遣。') for c,v in
        [('contract.employment_form',form),('contract.type',term)]]
    monkeypatch.setattr(pipeline,'extract',lambda *a,**k:packet(cs,fs))
    monkeypatch.setattr(pipeline,'verify',verified_packet)
    result=review_contract_v2(text,'labor',include_low_risk=True)
    assert not any(r['item_id'].startswith('DSP-') for r in result['items'])
    assert result['contract_type_name']==label
    assert result['release_quality_gate']['status']=='REPORT_READY'


def test_unverified_employment_form_cannot_default_to_direct():
    from review_v2.fact_validation import FactExtractionError
    text='劳动合同\n用工关系依另附协议确定。'
    s=store_for(text,[])
    s.coverage['contract.employment_form']='UNCERTAIN'
    with pytest.raises(FactExtractionError,match='UNRESOLVED_EMPLOYMENT_FORM'):
        classify(s)


def test_positive_equal_pay_does_not_hide_conflicting_discount():
    text='劳动合同\n实行相同报酬办法。\n另条约定员工接受较低工资。'
    s=store_for(text,[('dispatch.equal_pay','EQUAL','实行相同报酬办法。'),
                      ('dispatch.equal_pay','LOWER_ALLOWED','另条约定员工接受较低工资。')])
    rows=adverse(s,'employment_dispatch_equal_pay')
    assert not rows  # 差别表述不再替代两方实际报酬证据。
    from review_v2.dispatch_assessment import pay_state
    assert pay_state(s)['status']=='VERIFY'


@pytest.mark.parametrize('imposed,expected',[(False,False),(True,True)])
def test_penalty_scope_mention_is_not_an_imposed_obligation(imposed,expected):
    quote='未提前通知辞职须支付一个月薪资违约金。' if imposed else '不设普通辞职违约金。'
    text='劳动合同\n'+quote
    value={'scope':'ORDINARY_RESIGNATION','amount_text':'一个月薪资','imposed':True} if imposed else {'kind':'EXPLICIT_ABSENCE','scope':'普通辞职违约金','basis':quote}
    s=store_for(text,[('penalties.obligations' if imposed else 'penalties.exclusions',value,quote)])
    assert bool(s.adverse('employment_general_penalty'))==expected


@pytest.mark.parametrize('beneficiary,expected',[('EMPLOYEE',False),('EMPLOYER',True),('HOST',True)])
def test_existing_ip_ownership_remains_relational(beneficiary,expected):
    text='劳动合同\n既有成果的权利人依本条确定。'
    s=store_for(text,[('ip.allocations',{'scope':'PRE_EXISTING','beneficiary':beneficiary,
        'mode':'AUTOMATIC'},'既有成果的权利人依本条确定。')])
    assert s.element('employment_ip_ownership_1')
    assert bool(s.adverse('employment_ip_ownership'))==expected
