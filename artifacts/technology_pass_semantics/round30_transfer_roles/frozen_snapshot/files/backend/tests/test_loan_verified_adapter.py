from dataclasses import replace
import pytest
from review_v2.fact_validation import FactExtractionError
from review_v2.unified_facts.loan import schema, project_shared, evidence_for, element_concept, migration_inventory
from review_v2.unified_facts.store import CandidateStore, commit, rule_context, CURRENT
from backend.tests.test_unified_fact_framework import SOURCE, CLAUSES, observation, packet, verification


def loan_store(overrides=None):
    s=schema()
    overrides=overrides or {}
    roots=[]
    for key in s.root_keys:
        row=overrides.get(key,observation(key,state='ABSENT'))
        roots.append({**row,'normalized_value':row.get('value'),'verified':True})
    active=s.select(roots)
    rows=[overrides.get(key,observation(key,state='ABSENT')) for key in active]
    c=CandidateStore(SOURCE,CLAUSES,s,active,packet(rows,active))
    return commit(c,verification(c))


def test_loan_schema_has_no_labor_or_other_family_fields():
    s=schema()
    assert all(key.startswith(('common.','loan.')) for key in s.concepts)
    assert s.concepts['loan.principal'].kind=='money'
    assert s.concepts['loan.maturity_date'].kind=='date'
    assert 'loan.interest_formula' not in s.concepts
    assert s.concepts['loan.day_count_basis'].kind=='enum'
    active=s.select([])
    assert element_concept('loan_extension_application') not in active
    assert element_concept('loan_extension_guarantee') not in active


@pytest.mark.parametrize('guarantee,extension,expected', [(True,True,True),(True,False,False),(False,True,False)])
def test_child_needs_all_parent_facts(guarantee,extension,expected):
    roots=[{'concept':'loan.guarantee','normalized_value':guarantee},
           {'concept':'loan.extension','normalized_value':extension}]
    roots=[dict(r,state='PRESENT',verified=True,assertion='EXPLICIT',confidence=.95) for r in roots]
    active=schema().select(roots)
    assert (element_concept('loan_extension_guarantee') in active)==expected


def test_shared_applicability_reads_verified_facts_without_clause_scanning(monkeypatch):
    from review_v2 import loan_facts as legacy
    s=loan_store({'loan.lender_kind':observation('loan.lender_kind',value='natural'),
                  'loan.borrower_kind':observation('loan.borrower_kind',value='natural')})
    monkeypatch.setattr(legacy,'_party_kind',lambda *a,**k:pytest.fail('legacy extractor called'))
    monkeypatch.setattr(legacy,'units',lambda *a,**k:pytest.fail('legacy scanner called'))
    with rule_context(s):
        facts=legacy.LoanFacts.from_clauses(CLAUSES)
        assert facts.applicability('loan_natural_person_formation')['applicable'] is True
        assert facts.applicability('loan_financial_interest_compliance')['applicable'] is False
        assert facts.applicability('loan_extension_request')['applicable'] is False
    assert s.reads and CURRENT.get() is None
    trace=s.public()['rule_decisions']['loan_natural_person_formation'][0]
    assert trace['stage']=='APPLICABILITY'
    assert trace['decision']['applicable'] is True
    assert trace['input_fact_ids']


def test_uncertain_parent_is_not_treated_as_absence():
    s=loan_store({'loan.extension':observation('loan.extension',state='UNCERTAIN')})
    facts=project_shared(s)
    assert facts.applicability('loan_extension_request')['applicable'] is None
    assert facts.applicability('loan_extension_request')['status']=='UNCERTAIN'


def test_cross_clause_evidence_uses_one_fact_store(monkeypatch):
    from review_v2 import loan_facts as legacy
    key=element_concept('loan_interest_base')
    base=observation(key,value=True)
    base['evidence'].append({'clause_id':'C2','quote':CLAUSES[1].text})
    s=loan_store({key:base})
    monkeypatch.setattr(legacy,'_context_units',lambda *a:pytest.fail('raw scan called'))
    with rule_context(s):
        rows=legacy.extract('loan_interest_calculation_base',CLAUSES)
        assert {e['clause_id'] for e in rows}=={'C1','C2'}
        assert all('loan_interest_base' in e['supports_element_ids'] for e in rows)
        assert s.state(element_concept('loan_interest_period'))=='ABSENT'
        assert legacy.supports(legacy.PROFILES['loan_interest_calculation_base'][0],rows[0]['quote'])
        assert not legacy.supports(legacy.PROFILES['loan_interest_calculation_base'][1],rows[0]['quote'])


@pytest.mark.parametrize('stage',['graph','units','costs','negative'])
def test_unmigrated_raw_consumers_cannot_run_inside_verified_context(stage):
    from review_v2.contract_facts import extract_contract_fact_graph
    from review_v2.loan_facts import units,negative_scan
    from review_v2.loan_costs import analyze_costs
    functions={'graph':lambda:extract_contract_fact_graph(CLAUSES),'units':lambda:list(units(CLAUSES)),
               'costs':lambda:analyze_costs(CLAUSES),'negative':lambda:negative_scan('loan_interest_lpr_cap',CLAUSES)}
    with rule_context(loan_store()):
        with pytest.raises(FactExtractionError,match='RAW_FACT_REEXTRACTION_FORBIDDEN'):
            functions[stage]()
    assert CURRENT.get() is None


def test_all_loan_nodes_migrated_and_old_stages_remain_excluded():
    report=migration_inventory()
    assert report['consumer_migration_complete'] is True
    assert report['unmapped_rule_nodes'] == []
    assert 'loan_costs.analyze_costs' in report['blocked_legacy_stages']


def test_template_guidance_cannot_supply_present_facts():
    clauses=[replace(CLAUSES[0],block_type='TEMPLATE_GUIDANCE'),CLAUSES[1]]
    from backend.tests.test_unified_fact_framework import simple_schema
    with pytest.raises(FactExtractionError,match='NON_OPERATIVE_EVIDENCE'):
        CandidateStore(SOURCE,clauses,simple_schema(),('test.value',),packet([observation()]))
