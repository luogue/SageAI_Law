from pathlib import Path
import pytest
from review_v2.clause_parser import parse_contract_clauses as parse
from review_v2.loan_facts import PROFILES, extract, supports
from review_v2.loan_semantics import rate_adjustment, concept_facts
from review_v2.loan_costs import analyze_costs
from review_v2.engine import review_contract_v2

@pytest.mark.parametrize('expression,multiplier',[
 ('合同利率的1.5倍',1.5),('合同利率的150%',1.5),('合同利率上浮50%',1.5),
 ('正常借款利率的1.25倍',1.25),('执行利率基础上加收25%',1.25),('原利率的75%',.75),
])
def test_relative_rate(expression,multiplier):
 text=f'自逾期之日起，对逾期本金按{expression}计收逾期利息，直至实际清偿之日。'
 assert rate_adjustment(text)['multiplier']==pytest.approx(multiplier)
 assert all(supports(e,text) for e in PROFILES['loan_overdue_interest'])
 a=analyze_costs(parse('借款年利率为4.8%。'+text))
 c=next(c for c in a['components'] if c['kind']=='overdue_interest')
 assert c['annual_percent_estimate']==pytest.approx(4.8*multiplier)
 assert c['reference_evidence_ids']

@pytest.mark.parametrize('text',[
 '设备采购价格按原价格的1.5倍结算。',
 '逾期不按合同利率的150%计息。',
 '逾期利率将另行商定。',
])
def test_non_rate_or_unresolved_cannot_cover(text):
 assert not supports(PROFILES['loan_overdue_interest'][0],text)

@pytest.mark.parametrize('order',[
 '乙方付款未注明性质的，依次清偿费用、违约金、利息、本金。',
 '还款冲抵顺序：费用→违约金→利息→本金。',
 '还款先偿还费用，再支付利息，最后清偿本金。',
 '还款按以下清偿顺序：\n一、费用；\n二、利息；\n三、本金。',
])
def test_payment_allocation_forms(order):
 rows=extract('loan_repayment_offset_order',parse(order))
 assert rows and all(supports(PROFILES['loan_repayment_offset_order'][0],r['quote']) for r in rows)

@pytest.mark.parametrize('text',[
 '保险增信扣款顺序：保费→复利→罚息→利息→本金。',
 '费用、违约金、利息、本金均应偿还。',
 '还款不按费用→利息→本金的顺序清偿。',
 '管理费依次计收，但本金另行约定。',
])
def test_non_allocation_or_negated_order(text):
 assert not concept_facts('payment_allocation',text)

@pytest.mark.parametrize('positive',[
 '本借款用于采购生产设备及支付供应商货款。',
 '借款用于日常经营流动资金。',
 '本次借款确因生产经营需要。',
])
@pytest.mark.parametrize('negative_first',[False,True])
def test_positive_purpose_has_own_evidence(positive,negative_first):
 negative='不得将借款用于与企业正常生产经营无关的其他用途。'
 text=negative+positive if negative_first else positive+negative
 rows=extract('loan_enterprise_business_need',parse(text))
 assert rows
 assert all(r['quote']==positive for r in rows)
 assert all(r['semantic_normalization']['polarity']=='POSITIVE' for r in rows)
 assert not extract('loan_enterprise_business_need',parse(negative))

@pytest.mark.parametrize('reverse',[False,True])
def test_multiplier_reference_is_order_independent(reverse):
 parts=['第一条 利率\n借款年利率为4.8%。','第二条 逾期\n自逾期之日起，逾期本金按合同利率的150%计收逾期利息，至实际清偿之日止。']
 a=analyze_costs(parse('\n'.join(reversed(parts) if reverse else parts)))
 assert next(c['annual_percent_estimate'] for c in a['components'] if c['kind']=='overdue_interest')==pytest.approx(7.2)


def test_reference_rate_missing_is_not_invented():
 a=analyze_costs(parse('逾期本金按合同利率的1.5倍计收逾期利息。'))
 assert a['components'][0]['annual_percent_estimate'] is None
 assert a['judicial_protection']['status']=='PENDING'


def test_original_file_positive_binding_and_gate():
 from layers.input_layer import InputLayer
 source=Path(__file__).resolve().parents[2]/'test_data'/'104 企业借款.docx'
 text=InputLayer()._extract_from_docx_content(source.read_bytes())
 r=review_contract_v2(text,'loan',use_llm=False)
 rows={i['item_id']:i for i in r['items']}
 for key in ['L-02-04','L-05-02','L-06-03']:
  assert rows[key]['coverage_status']=='通过'
  assert all(e['quote'] in text for e in rows[key]['evidence_clauses'])
 assert '采购仓储设备' in rows['L-02-04']['evidence_clauses'][0]['quote']
 assert all('无关' not in e['quote'] and '不得' not in e['quote'] for e in rows['L-02-04']['evidence_clauses'])
 assert all('第十条' not in e['quote'] for e in rows['L-05-02']['evidence_clauses'])
 assert r['release_quality_gate']['status']=='REPORT_READY',r['release_quality_gate']['failures']


def test_short_list_retains_source_and_does_not_absorb_next_heading():
 text='还款按以下清偿顺序：\n一、费用；\n二、利息；\n三、本金。\n四、争议解决\n争议提交法院。'
 clauses=parse(text)
 assert clauses[0].text=='还款按以下清偿顺序：\n一、费用；\n二、利息；\n三、本金。'
 assert any('争议解决' in c.text and '本金' not in c.text for c in clauses)
 assert all(c.text in text for c in clauses)


def test_plain_headings_are_not_list_fragments():
 clauses=parse('说明：\n一、借款用途\n借款用于生产经营。\n二、还款期限\n期限一年。')
 assert len(clauses)>=3
 assert not any('借款用途' in c.text and '还款期限' in c.text for c in clauses)
