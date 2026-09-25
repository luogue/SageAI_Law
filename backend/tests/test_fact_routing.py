import pytest
from review_v2 import engine
from review_v2 import employment_fact_pipeline
from review_v2.fact_routing import CURRENT_ROUTE
from review_v2.contract_registry import get_contract_meta


@pytest.fixture(autouse=True)
def isolate_dispatch_test_finalizer(monkeypatch):
    # These tests mock pipeline output; final report reconciliation is exercised
    # with actual type stages in test_manual_type_chain.py.
    monkeypatch.setattr('review_v2.fact_routing.finalize', lambda response: response)


@pytest.mark.parametrize('alias', ['labor','employment','labor_contract','劳动合同'])
def test_alias_is_normalized_before_fact_dispatch(monkeypatch,alias):
    calls=[]
    def run(text,kind,legacy,**kwargs):
        calls.append(kind);assert CURRENT_ROUTE.get().resolved_type=='labor'
        return {'kind':kind}
    monkeypatch.setattr(employment_fact_pipeline,'run',run)
    assert engine.review_contract_v2('合同原文',alias,use_llm=False)=={'kind':'labor'}
    assert calls==['labor'] and CURRENT_ROUTE.get() is None


@pytest.mark.parametrize('selected,resolved', [('labor','labor'),('non_compete','non_compete'),('confidentiality','confidentiality')])
def test_reclassified_type_enters_matching_pipeline(monkeypatch,selected,resolved):
    monkeypatch.setattr(employment_fact_pipeline,'run',lambda text,kind,*a,**k:{'kind':kind})
    assert engine.review_contract_v2('合同原文',selected)['kind']==resolved


def test_selected_sale_does_not_extract_labor(monkeypatch):
    monkeypatch.setattr(employment_fact_pipeline,'run',lambda *a,**k:pytest.fail('labor must not run'))
    monkeypatch.setattr(engine,'_review_contract_v2_legacy',lambda text,kind,**k:{'kind':kind})
    assert engine.review_contract_v2('合同原文','sale')['kind']=='sale'


def test_failure_clears_routing_context(monkeypatch):
    def fail(*a,**kw):raise ValueError('test failure')
    monkeypatch.setattr(employment_fact_pipeline,'run',fail)
    with pytest.raises(ValueError,match='test failure'):engine.review_contract_v2('合同','labor')
    assert CURRENT_ROUTE.get() is None


def test_active_loan_cannot_be_returned_to_legacy_by_candidate_flag(monkeypatch):
    from review_v2.unified_facts import loan_pipeline
    monkeypatch.setenv('REVIEW_V2_VERIFIED_FACT_CANDIDATES','loan')
    monkeypatch.setattr(engine,'_review_contract_v2_legacy',lambda *a,**k:pytest.fail('no fallback'))
    monkeypatch.setattr(loan_pipeline,'run',lambda *a,**k:{'mode':'VERIFIED_FACTS'})
    assert engine.review_contract_v2('合同','loan') == {'mode':'VERIFIED_FACTS'}


@pytest.mark.parametrize('kind',['employment','labor_contract','non_compete','confidentiality'])
def test_status_and_source_guard_follow_canonical_family(monkeypatch,kind):
    import asyncio
    from routers import review_v2 as route
    monkeypatch.setattr(route.deepseek_facts,'status',lambda:{'available':True,'provider':'deepseek'})
    monkeypatch.setattr(route,'get_llm_review_status',lambda:pytest.fail('legacy model status'))
    status=asyncio.run(route.review_v2_llm_status(kind,{'id':1}))
    assert status['priority']=='deepseek'
    scope=route._runtime_source_dependency_scope(kind)
    assert 'review_v2.deepseek_transport' in scope
    assert 'review_v2.employment_fact_pipeline' in scope


def test_response_model_preserves_legacy_migration_disclosure():
    from routers.review_v2 import ReviewV2Result
    assert 'fact_migration' in ReviewV2Result.model_fields
