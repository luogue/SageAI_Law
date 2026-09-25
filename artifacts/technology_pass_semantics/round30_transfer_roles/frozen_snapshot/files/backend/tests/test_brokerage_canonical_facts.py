import io
from copy import deepcopy
from collections import Counter
from pathlib import Path
from types import SimpleNamespace

import pytest

from layers.input_layer import InputLayer
from review_v2.clause_parser import parse_contract_clauses
from review_v2.engine import review_contract_v2
from review_v2.engine import _resolve_final_element_searches, _search_final_element, ReviewItemResult
from review_v2.brokerage_facts import requirements, consistency_failures
from review_v2.brokerage_adverse import scan, daily_rate
from review_v2.lease_semantics import corpus_facts, supports


HEADER = '中介合同\n甲方（委托人）：客户公司\n乙方（中介人）：咨询公司\n'
POSITIVE_BROKERAGE_TEXT = HEADER + '''第六条 甲方权利义务
（二）甲方应当向乙方提供自身与订立合同有关的真实信息。
（四）甲方有权要求乙方如实告知与订立合同有关的信息及情况。
（六）甲方应当对乙方提供必要的协助。
第七条 乙方义务
（四）乙方应当尽到必要、审慎的核实义务，向甲方提供与订立合同有关的完整、准确、真实的信息及情况。
第八条 违约责任
（一）乙方故意隐瞒与订立合同有关的重要事实或者提供虚假情况，损害甲方利益的，不得请求支付服务费用；甲方因此受损失的，乙方应当承担损失赔偿责任。
'''


@pytest.fixture(scope='module')
def current():
    p = Path(__file__).resolve().parents[2] / 'test_data/59 中介合同.docx'
    text, _ = InputLayer().extract_text_with_diagnostics(SimpleNamespace(filename=p.name, file=io.BytesIO(p.read_bytes())))
    return text, review_contract_v2(text, 'brokerage', use_llm=False)


@pytest.mark.parametrize('node,body', [
    ('truthful_report_obligation', '第七条 乙方义务\n（四）乙方应当向甲方如实报告有关订立合同的事项。'),
    ('truthful_report_obligation', '第七条 乙方义务\n（四）应当如实报告订约情况。'),
    ('truthful_report_obligation', '第六条 甲方权利\n（四）甲方有权要求乙方如实告知与订立合同有关的信息及情况。'),
    ('truthful_report_obligation', '第七条 乙方义务\n（四）乙方应向甲方提供与订立合同有关的完整、准确、真实的信息及情况。'),
    ('important_fact_disclosure', '第七条 乙方义务\n（四）乙方不得隐瞒与订立合同有关的重要事实。'),
    ('important_fact_disclosure', '第七条 乙方义务\n（四）乙方应向甲方提供与订立合同有关的完整、准确、真实的信息及情况。'),
    ('important_fact_disclosure', '第八条 违约责任\n（一）乙方故意隐瞒重要事实或者提供虚假情况的，不得请求支付服务费用，并承担损失赔偿责任。'),
    ('principal_information_accuracy', '第六条 甲方义务\n（二）甲方保证向乙方提供的材料真实、合法、准确。'),
    ('principal_information_accuracy', '第六条 甲方义务\n（二）保证提供的资料真实、合法、有效。'),
    ('principal_information_accuracy', '第六条 甲方义务\n（二）甲方应当向乙方提供自身与订立合同有关的真实信息。'),
    ('principal_cooperation_obligation', '第六条 甲方义务\n（六）甲方应当为乙方提供必要的协助。'),
    ('principal_cooperation_obligation', '第六条 甲方义务\n（六）甲方应当对乙方提供必要的协助。'),
    ('expense_evidence', '第四条 费用\n（三）应当按照乙方提供的实际支出凭证支付。'),
    ('expense_evidence', '第四条 费用\n（三）乙方应提交费用发票供甲方核验。'),
    ('truthful_report_breach_consequence', '第八条 违约责任\n（一）乙方故意隐瞒重要事实或者提供虚假情况的，不得请求支付报酬，并应承担赔偿责任。'),
    ('truthful_report_breach_consequence', '第八条 违约责任\n（一）乙方故意隐瞒重要事实或者提供虚假情况，损害甲方利益的，不得请求支付服务费用并应承担损失赔偿责任。'),
])
def test_positive_facts_recalled_with_exact_source(node, body):
    text = HEADER + body
    specs = requirements(text)[node]
    facts = corpus_facts(parse_contract_clauses(text), specs)
    assert all(facts[e['element_id']] for e in specs)
    for e in specs:
        item = SimpleNamespace(node_id=node, item_id='BR-test', decision_trace={'semantic_requirements': specs})
        audit = _search_final_element(item, {**e, 'status': 'MISSING'}, parse_contract_clauses(text))
        assert audit['result'] == 'FOUND'
        assert audit['supporting_evidence'] == facts[e['element_id']]
        for row in facts[e['element_id']]:
            assert row['text'] in text
            assert supports(e, row)
            assert row['location'].startswith(('第六条', '第七条', '第四条', '第八条'))


@pytest.mark.parametrize('body,node', [
    ('第五条 保密\n客户名单、技术资料、交易条件属于保密信息。', 'principal_cooperation_obligation'),
    ('第六条 甲方义务\n甲方无需配合乙方提供材料。', 'principal_cooperation_obligation'),
    ('第六条 甲方义务\n甲方不必保证资料真实。', 'principal_information_accuracy'),
    ('第七条 乙方义务\n保证提供的资料真实。', 'principal_information_accuracy'),
    ('第三条 账户\n乙方收款账户为123456789。', 'accepted_service_evidence'),
])
def test_related_words_and_wrong_actor_do_not_prove_fact(body, node):
    text = HEADER + body
    specs = requirements(text)[node]
    assert not any(corpus_facts(parse_contract_clauses(text), specs).values())


def test_role_swap():
    text = '中介合同\n乙方（委托人）：客户公司\n甲方（中介人）：咨询公司\n第六条 乙方义务\n乙方保证资料真实准确。'
    specs = requirements(text)['principal_information_accuracy']
    assert all(corpus_facts(parse_contract_clauses(text), specs).values())


def test_independent_template_obligations_survive_full_pipeline():
    text = HEADER + '''第一条 服务
乙方向甲方提供订立合同的媒介服务。
第二条 服务期限
自2027年1月1日起至2027年6月1日止。
第三条 报酬
乙方促成甲方与第三人签订合同，甲方向乙方支付中介报酬。
第四条 中介费用
应当按照乙方提供的实际支出凭证支付。
第六条 甲方权利义务
（二）保证提供的资料真实、合法、有效。
（六）应当为乙方提供必要的协助。
第七条 乙方权利义务
（四）乙方应向甲方如实报告有关订立合同的事项，不得隐瞒重要事实。
第八条 违约责任
（一）乙方故意隐瞒重要事实或者提供虚假情况的，不得请求支付报酬，并应承担赔偿责任。
'''
    result = review_contract_v2(text, 'brokerage', use_llm=False)
    by = {i['item_id']: i for i in result['items']}
    for code in ('BR-03-01', 'BR-03-02', 'BR-04-02', 'BR-04-03', 'BR-08-04', 'BR-09-01'):
        assert by[code]['coverage_status'] == '通过', by[code]['coverage_elements']
        assert by[code]['evidence_clauses']
    assert result['release_quality_gate']['status'] == 'REPORT_READY', result['release_quality_gate']['failures']


def _missing_item_for_search_audit(node, code, text):
    specs = requirements(text)[node]
    rows = [
        {**spec, 'status': 'MISSING', 'bound_evidence_ids': [], 'risk_relevant': True}
        for spec in specs
    ]
    return ReviewItemResult(
        item_id=code,
        node_id=node,
        title=code,
        risk_level='中',
        status='缺失',
        risk_point_description='',
        suggested_clause_example='',
        legal_basis_index='',
        legal_consequence_if_missing='',
        applicable_if='',
        matched_terms=[],
        coverage_status='缺失',
        issue_type='完全缺失',
        evidence_clauses=[],
        evidence_location='',
        reasoning_summary='',
        decision_trace={'semantic_requirements': specs},
        coverage_elements=rows,
    )


@pytest.mark.parametrize('code,node', [
    ('BR-03-01', 'truthful_report_obligation'),
    ('BR-03-02', 'important_fact_disclosure'),
    ('BR-04-02', 'principal_cooperation_obligation'),
    ('BR-04-03', 'principal_information_accuracy'),
    ('BR-09-01', 'truthful_report_breach_consequence'),
])
def test_semantic_search_audit_found_updates_missing_final_element(code, node):
    clauses = parse_contract_clauses(POSITIVE_BROKERAGE_TEXT)
    item = _missing_item_for_search_audit(node, code, POSITIVE_BROKERAGE_TEXT)
    _resolve_final_element_searches([item], clauses)
    audits = item.decision_trace['element_absence_searches']
    assert audits
    assert all(audit['result'] == 'FOUND' for audit in audits)
    assert all(audit['search_mode'] == 'SEMANTIC_REQUIREMENT' for audit in audits)
    assert all(audit['search_corpus_chunks'] for audit in audits)
    assert all(any(row['accepted'] for row in audit['top_k_candidates']) for audit in audits)
    assert all(row['status'] == 'COVERED' for row in item.coverage_elements)
    assert item.coverage_status == '通过'
    assert item.evidence_clauses
    for row in item.evidence_clauses:
        assert row['evidence_id']
        assert row['text'] in POSITIVE_BROKERAGE_TEXT
        assert row['location'].startswith(('第六条', '第七条', '第八条'))


def test_current_docx_status_follows_actual_positive_corpus(current):
    text, report = current
    by = {i['item_id']: i for i in report['items']}
    expected = {
        'BR-03-01': 'truthful_report_obligation',
        'BR-03-02': 'important_fact_disclosure',
        'BR-04-02': 'principal_cooperation_obligation',
        'BR-04-03': 'principal_information_accuracy',
        'BR-09-01': 'truthful_report_breach_consequence',
    }
    parsed = parse_contract_clauses(text)
    profiles = requirements(text)
    for code, node in expected.items():
        has_positive = all(corpus_facts(parsed, profiles[node])[spec['element_id']] for spec in profiles[node])
        assert by[code]['coverage_status'] == ('通过' if has_positive else '缺失')
        assert bool(by[code]['evidence_clauses']) is has_positive


def test_current_complete_report_and_canonical_locations(current):
    text, report = current
    assert report['contract_type'] == 'brokerage'
    assert len(report['items']) == 44
    assert report['release_quality_gate']['status'] == 'REPORT_READY', report['release_quality_gate']['failures']
    clauses = {c.clause_id: c for c in parse_contract_clauses(text)}
    for item in report['items']:
        rows = item['evidence_clauses']
        assert item['evidence_location'] == '；'.join(dict.fromkeys(e['location'] for e in rows))
        for row in rows:
            assert row['location'] == clauses[row['clause_id']].location
            assert row['text'] in clauses[row['clause_id']].text
            assert any(supports(e, row) for e in item['decision_trace'].get('semantic_requirements', []))
    assert dict(Counter(i['coverage_status'] for i in report['items'])) == report['coverage_summary']


def test_report_text_labels_economic_impact_and_missing_liability_limit(current):
    report_text = current[1]['result']
    assert '经济影响：高' in report_text or '经济影响：中' in report_text
    assert '\n高\n' not in report_text
    assert '\n中\n' not in report_text
    by = {i['item_id']: i for i in current[1]['items']}
    assert by['BR-09-04']['coverage_status'] == '缺失'
    assert '责任限制条款过宽' not in by['BR-09-04']['legal_consequence_if_missing']
    assert '未明确中介人责任限制' in by['BR-09-04']['legal_consequence_if_missing']



def test_current_receipts_exclusive_and_partial_proof(current):
    by = {i['item_id']: i for i in current[1]['items']}
    assert by['BR-08-04']['coverage_status'] == '通过'
    assert '实际支出凭证' in by['BR-08-04']['evidence_clauses'][0]['text']
    assert by['BR-10-01']['coverage_status'] == '通过'
    assert set(e['location'] for e in by['BR-10-01']['evidence_clauses']) == {'第一条（二）', '第二条 服务期限'}
    assert by['BR-11-02']['coverage_status'] == '部分覆盖'
    assert by['BR-11-02']['evidence_location'] == '第十四条第1项'


def test_nonexclusive_and_policy_rules_are_applicability_gated(current):
    by = {i['item_id']: i for i in current[1]['items']}
    assert by['BR-07-01']['coverage_status'] == '不适用'
    assert by['BR-07-01']['applicability']['triggered'] is False
    assert by['BR-07-03']['coverage_status'] == '不适用'
    assert by['BR-07-03']['applicability']['triggered'] is False

    nonexclusive = review_contract_v2(HEADER + '第一条 服务\n甲方 ☒是 可以委托其他中介人提供内容相同或者相近的中介服务。', 'brokerage', use_llm=False)
    assert {i['item_id']: i for i in nonexclusive['items']}['BR-07-01']['coverage_status'] != '不适用'

    policy = review_contract_v2(HEADER + '第一条 服务\n本交易需完成监管审批；因政策或审批原因未能交易的，甲方不支付报酬。', 'brokerage', use_llm=False)
    assert {i['item_id']: i for i in policy['items']}['BR-07-03']['coverage_status'] == '通过'


def test_composite_reuses_child_canonical_objects(current):
    by = {i['item_id']: i for i in current[1]['items']}
    parent = by['BR-06-01']['decision_trace']['brokerage_canonical_coverage']
    child_rows = [e for code in ('BR-06-02', 'BR-06-03', 'BR-06-04')
                  for e in by[code]['decision_trace']['brokerage_canonical_coverage']['evidence']]
    assert parent['status'] == 'PASS'
    assert parent['evidence'] == child_rows
    assert by['BR-06-01']['coverage_status'] == '通过'
    assert by['BR-06-04']['coverage_status'] == '风险条款'  # presence and content are independent


def test_six_adverse_predicates_are_visible_in_five_rules(current):
    report = current[1]
    scan_result = report['items'][0]['decision_trace']['adverse_clause_scan']
    assert len(scan_result['findings']) == 6
    assert len({f['node_id'] for f in scan_result['findings']}) == 5
    by = {i['node_id']: i for i in report['items']}
    for hit in scan_result['findings']:
        item = by[hit['node_id']]
        assert item['coverage_status'] == '风险条款'
        assert item['related_risks']
        assert any(item['item_id'] in f['source_review_ids'] for f in report['risk_findings'])
    daily = next(f for f in scan_result['findings'] if f['kind'] == 'daily_penalty')
    assert daily['assessment']['simple_annualized_rate'] == 1.095
    for code in ('BR-04-01', 'BR-06-04', 'BR-08-02', 'BR-10-02', 'BR-11-04'):
        item = next(i for i in report['items'] if i['item_id'] == code)
        assert item['economic_impact'] in {'medium', 'high'}
        assert item['economic_impact_detail']['exposures']
    tail = next(i for i in report['items'] if i['item_id'] == 'BR-11-04')
    assert any(row.get('months') == 24 for row in tail['economic_impact_detail']['exposures'])
    assert any(row.get('remuneration_ratio') == 0.08 for row in tail['economic_impact_detail']['exposures'])


@pytest.mark.parametrize('quote,expected', [('逾期每日千分之三支付违约金。', .003), ('逾期按日0.4%支付违约金。', .004), ('逾期每日万分之五支付违约金。', .0005)])
def test_numeric_normalization_not_sample_amount(quote, expected):
    assert daily_rate(quote) == expected


def test_adverse_variants_and_protective_negations():
    text = '第八条\n甲方逾期按日0.4%支付违约金。\n甲方违反独家中介约定，应支付人民币350000元违约金。\n单笔费用低于8000元，无须事先取得书面批准。'
    assert {f['kind'] for f in scan(parse_contract_clauses(text))['findings']} == {'daily_penalty', 'exclusive_fixed_penalty', 'unapproved_expenses'}
    protective = '第八条\n甲方逾期每日万分之五支付违约金。\n不得按每日0.4%支付违约金。\n单笔费用低于8000元，仍需事先取得书面批准。'
    assert not scan(parse_contract_clauses(protective))['findings']


@pytest.mark.parametrize('corruption,expected', [('missing', 'POSITIVE_FACT_REPORTED_MISSING'), ('location', 'CANONICAL_LOCATION_MISMATCH'), ('quote', 'PASS_EVIDENCE_NOT_ENTAILED'), ('scan', 'ADVERSE_SCAN_REQUIRED'), ('zero_risk', 'ADVERSE_FACT_LOST')])
def test_consistency_gate_rejects_corrupted_final_states(current, corruption, expected):
    rows = [SimpleNamespace(**deepcopy(i)) for i in current[1]['items']]
    item = next(i for i in rows if i.item_id == ('BR-04-01' if corruption == 'zero_risk' else 'BR-08-04'))
    if corruption == 'missing': item.coverage_status = '缺失'
    if corruption == 'location': item.evidence_location = '第五条'
    if corruption == 'quote': item.evidence_clauses[0]['text'] = '双方保密。'
    if corruption == 'scan': item.decision_trace.pop('adverse_clause_scan')
    if corruption == 'zero_risk': item.coverage_status = '通过'
    assert expected in {f['requirement'] for f in consistency_failures(rows)}
