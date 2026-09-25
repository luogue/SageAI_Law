import pytest
from review_v2.engine import review_contract_v2
from review_v2.prohibition_protection import requirements
from review_v2.construction_coverage import extract, supports
from review_v2.clause_parser import parse_contract_clauses

@pytest.mark.parametrize('text,expected',[
    ('乙方不得以任何形式再分包。','通过'),
    ('乙方不得再分包。','通过'),
    ('未经甲方书面同意，乙方不得再分包。','部分覆盖'),
    ('未经理事方批准，劳务分包人禁止再次分包。','部分覆盖'),
    ('经甲方同意，乙方可以再分包。','风险条款'),
    ('乙方按时完成劳务作业。','缺失'),
])
def test_full_pipeline_preserves_prohibition_evidence(text,expected):
    r=review_contract_v2('建设工程施工劳务分包合同\n第一条\n'+text,'construction',use_llm=False)
    i=next(i for i in r['items'] if i['item_id']=='CE-05-03')
    assert i['coverage_status']==expected
    if expected!='缺失':
        assert any(text==e['text'] for e in i['evidence_clauses'])
    if expected=='部分覆盖':
        states={e['element_id']:e['status'] for e in i['coverage_elements']}
        assert states=={'action_restriction':'COVERED','unconditional_prohibition':'MISSING'}
        assert not i['decision_trace']['direct_adverse_evidence']['positive']
        assert '合同未明确“再分包”事项' not in r['result']
    assert r['release_quality_gate']['status']=='REPORT_READY',r['release_quality_gate']['failures']

def test_protection_queries_are_reusable_and_do_not_consume_source():
    clauses=parse_contract_clauses('未经委托人批准，受托人不得再次委托。')
    req=requirements('再次委托','再次委托')
    first=extract('independent_review_a',clauses,req)
    second=extract('independent_review_b',clauses,req)
    assert first==second and first
    assert supports(req[0],first[0]['text'])
    assert not supports(req[1],first[0]['text'])

@pytest.mark.parametrize('text,expected',[
    ('乙方不得以任何形式转包或者再分包。','通过'),
    ('未经甲方书面同意，乙方不得转包或者再分包。','部分覆盖'),
    ('经甲方同意，乙方可以转包或者再分包。','风险条款'),
])
def test_group_shares_downstream_scope_without_proving_upstream_consent(text,expected):
    r=review_contract_v2('建设工程施工劳务分包合同\n第一条\n'+text,'construction',use_llm=False)
    items={i['item_id']:i for i in r['items']}
    for rid in ('CE-05-01','CE-05-03'):
        i=items[rid]
        assert i['coverage_status']==expected
        assert any(e['text']==text for e in i['evidence_clauses'])
        scope=i['decision_trace']['construction_evidence_scope']
        assert scope['actor_role']=='LABOR_SUBCONTRACTOR'
        assert scope['contract_level']=='DOWNSTREAM_SUBCONTRACT'
    assert items['CE-05-02']['coverage_status']=='不适用'
    assert not items['CE-05-02']['evidence_clauses']
    assert r['release_quality_gate']['status']=='REPORT_READY',r['release_quality_gate']['failures']
