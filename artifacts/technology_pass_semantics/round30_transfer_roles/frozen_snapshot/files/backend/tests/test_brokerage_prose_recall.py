import pytest
from review_v2.brokerage_facts import requirements
from review_v2.clause_parser import parse_contract_clauses
from review_v2.lease_semantics import corpus_facts

HEADER = '中介合同\n甲方（委托人）：客户公司\n乙方（中介人）：服务公司\n'

@pytest.mark.parametrize('node,index,text,expected', [
    ('principal_cooperation_obligation',0,'甲方应提供必要协助与配合。',True),
    ('principal_cooperation_obligation',0,'甲方应根据服务开展的合理需要，及时提供资料、参加沟通并确认交易信息。',True),
    ('principal_cooperation_obligation',0,'乙方应提供必要协助与配合。',False),
    ('principal_cooperation_obligation',0,'甲方无需提供协助。',False),
    ('principal_cooperation_obligation',0,'甲方有权要求乙方提供协助。',False),
    ('truthful_report_breach_consequence',0,'乙方隐瞒重要事实的，无权请求中介报酬。',True),
    ('truthful_report_breach_consequence',0,'乙方提供虚假情况的，已收取的中介报酬应退还。',True),
    ('truthful_report_breach_consequence',0,'交易失败的，已收取的中介报酬应退还。',False),
    ('truthful_report_breach_consequence',0,'乙方隐瞒重要事实的，仍有权请求中介报酬。',False),
    ('truthful_report_breach_consequence',0,'乙方隐瞒重要事实的，已收取的中介报酬无需退还。',False),
    ('truthful_report_breach_consequence',1,'乙方隐瞒重要事实造成损失的应承担赔偿责任。',True),
    ('remuneration_amount_method',0,'甲方按交易总金额的2%支付中介费。',True),
    ('remuneration_amount_method',0,'甲方按交易总金额的2%支付税费。',False),
    ('service_period_and_area',0,'本合同自2026年9月8日起12个月内有效。',True),
    ('service_period_and_area',0,'保密义务自2026年9月8日起12个月内有效。',False),
])
def test_prose_semantic_support(node,index,text,expected):
    corpus=HEADER+text
    spec=requirements(corpus)[node][index]
    assert bool(corpus_facts(parse_contract_clauses(corpus),[spec])[spec['element_id']]) is expected


def test_unchanged_67_file_final_evidence():
    import io
    import hashlib
    from pathlib import Path
    from types import SimpleNamespace
    from layers.input_layer import InputLayer
    from review_v2.engine import review_contract_v2, _search_final_element
    source=Path(__file__).resolve().parents[2]/'test_data/67 中介.docx'
    data=source.read_bytes()
    assert hashlib.sha256(data).hexdigest() == '646cce04dca0b0920c152eb8a288d6bb28094759c531054335c83af80600e5ae'
    text,_=InputLayer().extract_text_with_diagnostics(SimpleNamespace(filename=source.name,file=io.BytesIO(data)))
    report=review_contract_v2(text,'brokerage',use_llm=False)
    items={r['item_id']:r for r in report['items']}
    for code in ('BR-04-02','BR-09-01','BR-05-02','BR-05-01','BR-05-03',
                 'BR-01-01','BR-01-03','BR-02-02','BR-06-01','BR-06-03','BR-06-04',
                 'BR-04-04','BR-02-03','BR-03-03'):
        row=items[code]
        assert row['coverage_status']=='通过'
        for trace in row['decision_trace'].get('concept_search_audits', []):
            assert trace['result']=='FOUND'
            assert any(c['accepted'] for c in trace['top_k_candidates'])
        for spec in row['decision_trace']['semantic_requirements']:
            item=SimpleNamespace(item_id=code,node_id=row['node_id'],decision_trace=row['decision_trace'])
            audit=_search_final_element(item,{**spec,'status':'MISSING'},parse_contract_clauses(text))
            assert audit['result']=='FOUND'
            assert all(e['text'] in text for e in audit['supporting_evidence'])
    assert items['BR-02-03']['decision_trace']['brokerage_canonical_coverage']['missing']==[]
    assert items['BR-11-02']['coverage_status']=='部分覆盖'
    for code in ('BR-03-04','BR-04-03','BR-07-02','BR-07-04','BR-08-01','BR-08-02',
                 'BR-08-03','BR-08-04','BR-09-02','BR-09-03','BR-09-04','BR-11-03'):
        assert items[code]['coverage_status']=='缺失'
    assert report['release_quality_gate']['status']=='REPORT_READY'
