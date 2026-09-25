from pathlib import Path
from collections import Counter
import pytest
from review_v2.engine import review_contract_v2
from review_v2.lease_semantics import corpus_facts, requirement
from review_v2.clause_parser import parse_contract_clauses

@pytest.mark.parametrize('rule,text',[
 ('GUA-02-01','保证人应以书面形式通知债权人。'),
 ('GUA-02-01','应取得保证人书面同意并提供书面材料。'),
 ('GUA-02-01','在担保合同或其他合同项下发生违约事件时，其将立即以书面形式通知债权人。'),
 ('GUA-05-01','第四条 保证期间'),
 ('GUA-09-02','主债务提前到期，保证人承担连带保证责任。'),
])
def test_false_friends_do_not_prove_fact(rule,text):
    r=review_contract_v2('保证合同\n第一条 保证事项\n'+text,'guarantee',use_llm=False)
    item=next(i for i in r['items'] if i['item_id']==rule)
    assert item['coverage_status']!='通过'
    assert not item['evidence_clauses']

def test_direct_clause_outranks_heading():
    spec=requirement('duration','明确期限',r'保证期间')
    hits=corpus_facts(parse_contract_clauses('保证合同\n第一条 保证期间\n第二条 责任期限\n保证期间自债务届满之日起两年。'),[spec])['duration']
    assert '两年' in hits[0]['quote']
    assert hits[0]['selection_reason']=='DIRECT_OPERATIVE_WITH_VALUE'

def test_current_contract_evidence_and_unchanged_states():
    from layers.input_layer import InputLayer
    p=next((Path(__file__).resolve().parents[2]/'test_data').glob('69 *.docx'))
    text=InputLayer()._extract_from_docx_content(p.read_bytes())
    r=review_contract_v2(text,'guarantee',use_llm=False)
    assert r['contract_type']=='guarantee'
    assert Counter(i['coverage_status'] for i in r['items'])=={'通过':20,'缺失':1,'不适用':20,'法律提示':5,'风险条款':1,'待核验':2}
    for key,quote in [('GUA-02-01','本合同自各方当事人签字或加盖公章之日生效'),('GUA-05-01','之日起两年'),('GUA-09-02','应当取得保证人书面同意')]:
        item=next(i for i in r['items'] if i['item_id']==key)
        assert item['coverage_status']=='通过'
        assert quote in item['evidence_clauses'][0]['quote']
        assert item['evidence_clauses'][0]['entailment_score']>=95
    assert r['release_quality_gate']['status']=='REPORT_READY',r['release_quality_gate']['failures']
