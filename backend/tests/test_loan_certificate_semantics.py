from copy import deepcopy
from decimal import Decimal
import pytest
from review_v2.fact_validation import FactExtractionError
from review_v2.unified_facts.certificates import verify_current,validate_response
from review_v2.unified_facts.store import CandidateStore,commit,source_fact_view
from review_v2.unified_facts.ontology import principal_basis,evidence_supports
from review_v2.unified_facts.normalization import normalize
from review_v2.unified_facts.schema import Concept,Module,Schema
from review_v2.unified_facts.loan_formulas import expression
from review_v2.clause_parser import parse_contract_clauses
from backend.tests.test_unified_fact_framework import candidate,observation,verification


def test_old_certificate_never_certifies_changed_candidate():
    old=candidate();cert=verification(old)
    current=candidate([observation(value='14000')])
    assert old.snapshot_hash!=current.snapshot_hash
    with pytest.raises(FactExtractionError,match='SNAPSHOT_MISMATCH'):commit(current,cert)
    cert['candidate_snapshot_hash']=current.snapshot_hash
    with pytest.raises(FactExtractionError,match='FACT_IDS'):commit(current,cert)


def test_mutating_candidate_after_request_invalidates_snapshot():
    c=candidate();cert=verification(c)
    c.observations[0]['normalized_value']=Decimal('14000')
    with pytest.raises(FactExtractionError,match='SNAPSHOT_MISMATCH'):commit(c,cert)


def test_even_identical_reextraction_has_a_distinct_candidate_generation():
    old=candidate();current=candidate()
    assert old.observations==current.observations
    assert old.snapshot_hash!=current.snapshot_hash
    with pytest.raises(FactExtractionError,match='SNAPSHOT_MISMATCH'):
        commit(current,verification(old))


def test_invalid_response_retries_same_snapshot_without_reextraction_or_old_context():
    c=candidate();calls=[]
    payload={'quarantine_context':{'fact_id':'OLD'},'validation_feedback':{'fact_id':'OLD'},
             'known_facts_context_only':[{'fact_id':'OLD','concept':'elsewhere','state':'ABSENT'}]}
    def transport(system,payload,*,stage):
        calls.append(deepcopy(payload))
        assert stage=='VERIFICATION'
        assert 'OLD' not in repr(payload)
        cert=verification(c)
        if len(calls)==1:cert['checks'][0]['fact_id']='STALE'
        return {},cert
    _,cert=verify_current(c,payload,transport,'JSON','VERIFICATION')
    assert len(calls)==2
    assert calls[0]['candidate_snapshot_hash']==calls[1]['candidate_snapshot_hash']==c.snapshot_hash
    assert calls[0]['candidates']==calls[1]['candidates']
    assert commit(c,cert).snapshot_hash==c.snapshot_hash


@pytest.mark.parametrize('field', ['candidate_snapshot_hash','checks'])
def test_invalid_response_is_bounded_and_never_accepted(field):
    c=candidate();calls=[]
    def transport(*args,**kwargs):
        calls.append(1);r=verification(c);r.pop(field);return {},r
    with pytest.raises(FactExtractionError,match='VERIFICATION_RESPONSE_INVALID'):
        verify_current(c,{},transport,'JSON','VERIFICATION')
    assert len(calls)==3


@pytest.mark.parametrize('text', ['实际占用本金','实际占用借款本金','实际占用本金余额',
    '尚未偿还的借款本金','未清偿本金','正常本金余额','分期归还后的剩余本金'])
def test_unpaid_principal_ontology_variants(text):
    assert principal_basis(text)=='UNPAID_PRINCIPAL'


@pytest.mark.parametrize('text', ['原始借款总额','借款总金额','本金全额'])
def test_original_total_is_not_outstanding(text):
    assert principal_basis(text)=='PRINCIPAL'


def test_base_projection_requires_literal_bound_evidence():
    source='借款合同\n第一条 利息\n利息按照实际占用借款本金计收。'
    clauses=parse_contract_clauses(source);clause=next(c for c in clauses if '计收' in c.text)
    spec=Schema('test',(Module('root',(Concept('charge','loan_charge',''),)),),())
    value={'kind':'regular_interest','charge_key':'interest','base_expression':'实际占用借款本金',
        'accrual_window':{'start_event':'UNKNOWN','end_event':'UNKNOWN'},
        'rate':{'state':'PRESENT','percent':6,'period':'YEAR'}}
    row={'concept':'charge','state':'PRESENT','value':value,'confidence':.99,'assertion':'EXPLICIT',
         'evidence':[{'clause_id':clause.clause_id,'quote':'利息按照实际占用借款本金计收。'}]}
    packet={'schema_version':spec.version,'searched_concepts':['charge'],
            'reviewed_clause_ids':[c.clause_id for c in clauses],'observations':[row]}
    c=CandidateStore(source,clauses,spec,spec.root_keys,packet)
    assert c.observations[0]['normalized_value']['base']=='UNPAID_PRINCIPAL'
    assert source_fact_view(c.observations)[0]['normalized_value']['base_expression']=='实际占用借款本金'
    row['value']['base_expression']='原始借款总额'
    with pytest.raises(FactExtractionError,match='BASE_EXPRESSION_NOT_IN_EVIDENCE'):
        CandidateStore(source,clauses,spec,spec.root_keys,packet)


@pytest.mark.parametrize('quotes,supported', [
    (['应提前五个工作日通知甲方。'],False),
    (['提前还款应以电子邮件通知。'],True),
    (['应提前七日通过短信告知提前还款。'],True),
    (['提前通知甲方。'],False),
    (['提前还款应提前三日通知。','本合同所有通知均以书面方式送达。'],True),
])
def test_notice_channel_is_distinct_from_period(quotes,supported):
    assert evidence_supports('loan.element.loan_early_channel',True,[{'quote':q} for q in quotes]) is supported


def test_hallucinated_omission_cannot_override_candidate():
    source='借款合同\n第一条 提前还款\n应提前五个工作日通知甲方。'
    clauses=parse_contract_clauses(source);clause=next(c for c in clauses if '五个工作日' in c.text)
    key='loan.element.loan_early_channel'
    spec=Schema('test',(Module('root',(Concept(key,'boolean','通知渠道'),)),),())
    row={'concept':key,'state':'ABSENT','confidence':.9,'assertion':'EXPLICIT','evidence':[]}
    packet={'schema_version':spec.version,'searched_concepts':[key],
            'reviewed_clause_ids':[c.clause_id for c in clauses],'observations':[row]}
    c=CandidateStore(source,clauses,spec,spec.root_keys,packet)
    cert={'candidate_snapshot_hash':c.snapshot_hash,'searched_concepts':[key],
          'reviewed_clause_ids':packet['reviewed_clause_ids'],
          'checks':[{'fact_id':c.observations[0]['fact_id'],'supported':True}],
          'audits':[{'concept':key,'reviewed_clause_ids':packet['reviewed_clause_ids'],
                    'complete':False,'reason':'声称短信微信邮件渠道','omitted_facts':[{**row,'state':'PRESENT','value':True,
                    'evidence':[{'clause_id':clause.clause_id,'quote':'应提前五个工作日通知甲方。'}]}]}]}
    with pytest.raises(FactExtractionError,match='EVIDENCE_DOES_NOT_SUPPORT_ATTRIBUTE'):validate_response(c,cert)
    cert['audits'][0]['omitted_facts'][0]['evidence'][0]['quote']='通过短信微信通知'
    with pytest.raises(FactExtractionError,match='EVIDENCE_NOT_IN_CLAUSE'):validate_response(c,cert)


@pytest.mark.parametrize('text,expected', [
    ('扣款顺序依次为复利、罚息、利息、本金。',False),
    ('对未付利息按每月利率0.5%计收复利。',True),
    ('借款人同意复利，但计算方式另行协商。',False),
])
def test_compound_requires_calculation_arrangement(text,expected):
    assert evidence_supports('loan.compound',True,[{'quote':text}]) is expected


@pytest.mark.parametrize('text,expected', [
    ('预计放款日期为明日，以受托支付方式发至贷款账户。',False),
    ('借款人授权银行从还款账户自动扣收。',False),
    ('银行出具放款回单，作为本金交付证明。',True),
    ('系统放款记录作为双方确认的支付凭证。',True),
])
def test_credential_mechanism_is_not_payment_arrangement(text,expected):
    assert evidence_supports('loan.voucher_mechanism',True,[{'quote':text}]) is expected


@pytest.mark.parametrize('quote',['借 条','放 款 回 单','电子\n凭证','转 账 凭 证'])
def test_typographic_spacing_does_not_erase_credential_ontology(quote):
    refs=[{'quote':quote}]
    assert evidence_supports('loan.debt_instrument',True,refs)
    assert refs[0]['quote']==quote


def test_payment_acknowledgement_channel_cannot_prove_early_repayment_channel():
    refs=[{'quote':'收到贷款后以短信或微信通知甲方。','section':'借款交付'}]
    assert not evidence_supports('loan.element.loan_early_channel',True,refs)
    refs=[{'quote':'应提前五个工作日书面通知甲方。','section':'提前还款'}]
    assert evidence_supports('loan.element.loan_early_channel',True,refs)


@pytest.mark.parametrize('basis,divisor', [('ACT_360','360'),('ACT_365','365'),('ACT_ACT','对应年度实际天数')])
def test_annual_daily_conversion_is_explicit_and_not_defaulted(basis,divisor):
    r=expression(Decimal('7.2'),'YEAR','DAY',basis,'实际未偿本金')
    assert r['state']=='PRESENT' and '÷ '+divisor in r['expression']
    assert r['day_count_divisor']==divisor


def test_unknown_convention_and_compound_are_not_fabricated():
    assert expression(6,'YEAR','DAY',None,'本金')['state']=='UNKNOWN'
    assert expression(6,'YEAR',None,'ACT_365','本金')['state']=='UNKNOWN'
    assert expression(.02,'DAY','DAY',None,'欠息')['day_count_divisor'] is None
    assert expression(.8,'MONTH','MONTH',None,'本金')['state']=='PRESENT'
