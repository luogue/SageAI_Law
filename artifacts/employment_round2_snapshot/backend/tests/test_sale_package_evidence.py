"""Layout-independent goods evidence and buyer-side conditional review."""
import json
from pathlib import Path
import pytest
from review_v2.clause_parser import parse_contract_clauses, BLOCK_ANNEX
from review_v2.sale_evidence import extract, has_title_retention, has_installment_acceleration, PROFILES, supports
from review_v2.engine import review_contract_v2, _element_supported_by_evidence
from review_v2.user_profile import UserRiskProfile


@pytest.mark.parametrize('text', [
    '货物于合同签订后45日内送达。',
    '附：商务条件\n交货时间：\n2027年3月15日。',
    '第二节 其他条款\n服务时间：\n生效后12日内完成全部货物供货。',
])
def test_delivery_layouts(text):
    assert extract('sale_delivery_time', parse_contract_clauses(text))


@pytest.mark.parametrize('text', ['验收后5个工作日内以书面形式向卖方提出异议。',
                                  '买方对质量有异议，应通过电子邮件提出。'])
def test_written_objection_variants(text):
    evidence = extract('sale_quality_remedy', parse_contract_clauses(text))
    assert any('quality_objection_form' in e['element_ids'] for e in evidence)
    assert not extract('sale_quality_remedy', parse_contract_clauses('双方书面通知变更地址。'))


@pytest.mark.parametrize('text', ['逾期超过30日的，甲方有权解除合同。',
                                  '乙方违法分包的，甲方可解除合同。'])
def test_termination_event_is_not_absent(text):
    from review_v2.canonical_claims import _build_goods_claims
    claims = _build_goods_claims(parse_contract_clauses(text))
    assert claims['contract.termination.trigger'].status == 'ASSERTED'
    assert claims['contract.termination.trigger'].source_spans
    assert _build_goods_claims(parse_contract_clauses('甲方有权解除合同。'))['contract.termination.trigger'].status == 'UNKNOWN'


@pytest.mark.parametrize('document', ['验收文件', '验收单', '签收单', '交接单'])
def test_signed_acceptance_document_is_receipt_record(document):
    evidence = extract('sale_delivery_method', parse_contract_clauses(f'双方签署{document}。'))
    assert any('goods_receipt_record' in e['element_ids'] for e in evidence)
    assert not any('goods_receipt_record' in e['element_ids'] for e in
                   extract('sale_delivery_method', parse_contract_clauses('双方无需签署验收文件。')))


def test_inspection_evaluation_uses_period_and_context_not_reasonableness_keyword():
    from review_v2.sale_evidence import inspection_period_context
    facts = inspection_period_context(parse_contract_clauses('安装调试后进行性能验收。验收后5个工作日内提出异议。隐蔽瑕疵适用质保期。'))
    assert '5个工作日' in facts['periods'][0]['quote']
    assert facts['acceptance_method'] and facts['latent_defects']
    unrelated = inspection_period_context(parse_contract_clauses(
        '验收后7日内支付货款。收到书面异议后7日内完成维修。'))
    assert not unrelated['periods']


def test_termination_conditional_elements_do_not_apply_to_every_sale():
    from review_v2.sale_evidence import termination_element_context
    from review_v2.common_sale import common_sale_coverage_requirement
    def requirements(text):
        return {e['element_id'] for e in common_sale_coverage_requirement(
            'common_termination_procedure', termination_element_context(text))['required_elements']}
    ordinary = requirements('一次性设备采购。□框架协议\n逾期超过30日，买方有权解除合同。违法分包可解除。')
    assert not ordinary.intersection({'convenience_termination_notice','existing_order_effect','cure_period'})
    assert 'notice_or_demand' in ordinary
    ongoing = requirements('长期合作按订单供货。经催告后仍未履行的可以解除合同。')
    assert {'convenience_termination_notice','existing_order_effect','cure_period'} <= ongoing


def test_evaluation_core_citations_and_termination_conditions_in_production(report):
    rows = {r['item_id']:r for r in report['items']}
    assessment = rows['S-07-02']
    assert assessment['coverage_status'] == 'INSUFFICIENT_CONTEXT'
    periods = {e['quote'] for e in assessment['decision_trace']['inspection_period_assessment']['periods']}
    assert assessment['evidence_clauses']
    assert all((e.get('quote') or e.get('text')) in periods for e in assessment['evidence_clauses'])
    assert not any('含键盘' in (e.get('quote') or e.get('text','')) for e in assessment['evidence_clauses'])
    assert any(term in assessment['citation']['original_excerpt'] for term in ('7日内组织验收', '5个工作日内'))
    assert rows['S-00-02']['coverage_status'] == '部分覆盖'
    assert not {'convenience_termination_notice','existing_order_effect','cure_period'}.intersection(
        {e['element_id'] for e in rows['S-00-02']['coverage_elements']})


def test_pending_statistics_share_normalized_states(report):
    from copy import deepcopy
    from review_v2.report_statistics import COVERAGE_BUCKETS, statistics_gate
    pending = {r['item_id'] for r in report['all_rule_statuses'] if r['coverage_status'] == 'INSUFFICIENT_CONTEXT'}
    assert pending == {'S-00-07', 'S-01-04', 'S-07-02'}
    assert report['coverage_summary']['待核验'] == 3
    assert report['manual_review_summary']['manual_review_count'] == 3
    assert sum(report['coverage_summary'].get(k, 0) for k in COVERAGE_BUCKETS) == report['all_items_count'] == 56
    assert '- 待核验：3 项' in report['result']
    assert statistics_gate(report)['status'] == 'REPORT_READY'
    assert report['release_quality_gate']['status'] == 'REPORT_READY'
    broken = deepcopy(report)
    broken['coverage_summary']['待核验'] = 0
    assert statistics_gate(broken)['status'] == 'BLOCKED'
    broken = deepcopy(report)
    broken['result'] = broken['result'].replace('- 待核验：3 项', '- 待核验：0 项')
    assert statistics_gate(broken)['status'] == 'BLOCKED'


@pytest.mark.parametrize('prefix', ['S', 'TC', 'CE', 'HL'])
def test_pending_count_is_contract_type_independent(prefix):
    from types import SimpleNamespace
    from review_v2.report_statistics import coverage_counts
    from review_v2.engine import _coverage_summary, _needs_manual_review_record
    rows = [dict(item_id=f'{prefix}-{i}', coverage_status='INSUFFICIENT_CONTEXT',
                 needs_manual_review=False, coverage_elements=[]) for i in range(3)]
    objects = [SimpleNamespace(**r) for r in rows]
    assert coverage_counts(rows) == _coverage_summary(objects) == {'待核验': 3}
    assert all(_needs_manual_review_record(r) for r in objects)
    assert all(r.coverage_status == 'INSUFFICIENT_CONTEXT' for r in objects)


def test_annex_after_signatures_is_operative_and_traceable():
    text = '一、当事人\n乙方（供应商）：\n乙方盖章\n第二节 其他条款\n供货后验收。\n附：技术参数\n内存：64GB\n运输信息：\n货物送达指定地点签收后风险转移。'
    clauses = parse_contract_clauses(text)
    evidence = extract('sale_risk_transfer_delivery', clauses)
    assert evidence
    clause = next(c for c in clauses if c.clause_id == evidence[0]['clause_id'])
    assert clause.block_type == BLOCK_ANNEX
    assert evidence[0]['quote'] in clause.text


def test_topic_related_notice_does_not_prove_rights_disclosure():
    text = '第二节 条款\n货物不得存在权利瑕疵。\n保密信息不得向第三方披露。'
    assert not extract('sale_right_defect_notice', parse_contract_clauses(text))
    assert extract('sale_right_defect_notice', parse_contract_clauses('卖方须如实告知货物的权利瑕疵。'))


@pytest.mark.parametrize('text, expected', [
    ('合同分三期付款。', False), ('不采用所有权保留。', False),
    ('价款付清前货物所有权仍归卖方。', True), ('卖方保留货物所有权。', True),
])
def test_retention_requires_actual_arrangement(text, expected):
    assert has_title_retention(text) is expected


def test_negative_evidence_cannot_support_positive_element():
    row = PROFILES['sale_delivery_time'][0]
    status, _ = _element_supported_by_evidence(row, {'source_type':'SEARCH_AUDIT',
        'text':'未找到货物于30日内交付', 'entailment_status':'SUPPORTS'})
    assert status == 'MISSING'


def test_penalty_payment_is_not_a_purchase_instalment():
    assert not extract('sale_payment_schedule', parse_contract_clauses('卖方应在7日内支付5%的违约金。'))


def test_twenty_percent_instalment_is_not_a_default_acceleration_clause():
    assert not has_installment_acceleration('签约支付20%，验收后支付剩余全部价款。')
    assert not has_installment_acceleration('交货逾期超过30日，买方有权解除合同。')
    assert has_installment_acceleration('买方逾期付款经催告仍未支付的，卖方有权要求支付全部价款。')


def test_quality_certificate_and_software_license_do_not_prove_administrative_scope():
    from review_v2.engine import _is_checkpoint_applicable
    from review_v2.sale_contract_checklist import get_sale_checklist
    checkpoint=next(r for r in get_sale_checklist() if r.node_id=='sale_approval_license')
    applicable, reason=_is_checkpoint_applicable('交付合格证和正版软件授权证明。', checkpoint, 'sale')
    assert not applicable and '暂不确定' in reason
    assert _is_checkpoint_applicable('该设备须提供强制认证证书。', checkpoint, 'sale')[0]


@pytest.mark.parametrize('node, proposal', [
    ('sale_retention_agreement', '建议出卖人保留所有权。'),
    ('sale_retention_registration', '建议补充所有权保留登记手续。'),
    ('sale_retention_retake', '建议约定出卖人有权取回货物。'),
    ('sale_deemed_acceptance', '建议逾期未检验视为买受人认可。'),
    ('sale_liquidated_damages_adjustment', '建议将出卖人赔偿责任上限封顶。'),
])
def test_buyer_does_not_receive_automatic_seller_protection(node, proposal):
    from types import SimpleNamespace as NS
    from review_v2.recommendation_impact import evaluate_recommendations
    item = NS(item_id='ANY', node_id=node, coverage_elements=[], decision_trace={})
    finding = NS(finding_id='F', source_review_ids=['ANY'], risk_group='damages')
    rec = NS(recommendation_id='R', target_finding_ids=['F'], proposed_change=proposal, suggested_text=proposal)
    assert not evaluate_recommendations([rec], [finding], [item], 'BUYER')[0]
    assert evaluate_recommendations([rec], [finding], [item], 'SELLER')[0]


@pytest.fixture(scope='module')
def report():
    from fastapi.testclient import TestClient
    from main import app
    from auth.routes import get_current_user
    current = next((Path(__file__).resolve().parents[2] / 'test_data').glob('48 *.docx'))
    previous = app.dependency_overrides.get(get_current_user)
    app.dependency_overrides[get_current_user] = lambda: {'id':1,'phone':'test'}
    try:
        with TestClient(app) as client:
            response = client.post('/review-v2/file', files={'file':(current.name,current.read_bytes(),
                'application/vnd.openxmlformats-officedocument.wordprocessingml.document')},
                data={'contract_type':'sale','use_llm':'false','include_low_risk':'true',
                      'profile_json':json.dumps({'user_identity':'甲方/买方/采购人'},ensure_ascii=False)})
        assert response.status_code == 200, response.text
        return response.json()
    finally:
        if previous is None:
            app.dependency_overrides.pop(get_current_user, None)
        else:
            app.dependency_overrides[get_current_user] = previous


def test_full_production_recall(report):
    rows = {r['item_id']:r for r in report['items']}
    for key in ('S-02-03','S-03-01','S-03-02','S-03-03','S-03-04','S-04-01','S-04-02',
                'S-05-02','S-05-04','S-06-01','S-08-01','S-11-01','S-11-02','S-11-04','S-12-01','S-12-04'):
        assert rows[key]['coverage_status'] in {'通过','部分覆盖'}, (key,rows[key]['coverage_elements'])
        assert any(e['status']=='COVERED' for e in rows[key]['coverage_elements'])
    for key in ('S-09-01','S-09-02','S-09-03','S-09-04','S-07-04','S-10-01'):
        assert rows[key]['coverage_status']=='不适用', rows[key]
    assert rows['S-11-03']['coverage_status'] == '缺失'
    assert report['release_quality_gate']['status'] in {'PASSED','REPORT_READY'}, report['release_quality_gate']


def test_four_closure_results_through_file_pipeline(report):
    rows = {r['item_id']:r for r in report['items']}
    for rule, key in [('S-06-03','quality_objection_form'),
                      ('S-03-03','goods_receipt_record')]:
        element = next(e for e in rows[rule]['coverage_elements'] if e['element_id'] == key)
        assert element['status'] == 'COVERED', element
    termination = rows['S-00-02']
    trigger = [e for e in termination['coverage_elements'] if 'trigger' in e['element_id']]
    assert trigger and all(e['status'] == 'COVERED' for e in trigger), termination['coverage_elements']
    assessment = rows['S-07-02']
    assert assessment['coverage_status'] == 'INSUFFICIENT_CONTEXT', assessment
    assert assessment['needs_manual_review']
    assert assessment['decision_trace']['inspection_period_assessment']['periods']
    assert not any(e.get('source_type') == 'SEARCH_AUDIT' for e in assessment['evidence_clauses'])


def test_sale_profile_binding_entails_each_covered_element(report):
    for row in report['items']:
        requirements = {e['element_id']:e for e in PROFILES.get(row['node_id'],[])}
        evidence = {e.get('evidence_id') or e.get('clause_id'):e for e in row['evidence_clauses']}
        for element in row['coverage_elements']:
            if element['status']!='COVERED' or element['element_id'] not in requirements:
                continue
            quotes = element.get('supporting_evidence') or [
                evidence[k] for k in element.get('evidence_ids',[]) if k in evidence]
            assert quotes, (row['item_id'],element)
            assert all(supports(requirements[element['element_id']],q.get('quote') or q.get('text','')) for q in quotes)


def test_published_wrong_quote_cannot_borrow_same_clause_support(report):
    from copy import deepcopy
    from dataclasses import fields
    from review_v2 import engine
    row = deepcopy(next(r for r in report['items'] if r['item_id']=='S-11-04'))
    item = engine.ReviewItemResult(**{f.name:row[f.name] for f in fields(engine.ReviewItemResult) if f.name in row})
    evidence = next(e for e in item.evidence_clauses if e.get('supporting_element_ids'))
    evidence.update(quote='甲方应提供安装场地。', text='甲方应提供安装场地。')
    failures = engine._requirement_source_entailment_failures([item], [])
    assert any(f['reason']=='SALE_REQUIREMENT_NOT_ENTAILED_BY_SOURCE' for f in failures)


def test_positive_pass_without_source_is_rejected(report):
    from copy import deepcopy
    from dataclasses import fields
    from review_v2 import engine
    row = deepcopy(next(r for r in report['items'] if r['item_id']=='S-11-04'))
    item = engine.ReviewItemResult(**{f.name:row[f.name] for f in fields(engine.ReviewItemResult) if f.name in row})
    for element in item.coverage_elements:
        element['supporting_evidence']=[]
        element['source_spans']=[]
    failures = engine._exact_element_report_invariants([item], [])
    assert any(f['reason']=='POSITIVE_PASS_WITHOUT_DIRECT_EVIDENCE' for f in failures)


def test_display_fields_follow_final_elements_not_stale_llm_judgment(report):
    from copy import deepcopy
    from dataclasses import fields
    from review_v2 import engine
    for key in ('S-05-04','S-11-04'):
        row=deepcopy(next(r for r in report['items'] if r['item_id']==key))
        item=engine.ReviewItemResult(**{f.name:row[f.name] for f in fields(engine.ReviewItemResult) if f.name in row})
        item.reasoning_summary='旧模型判断全部覆盖'
        item.risk_point_description='旧模型未找到条款'
        item.evidence_location='错误旧定位'
        engine._apply_element_level_narratives([item])
        assert item.reasoning_summary==item.narrative_state['judgment']
        assert '旧' not in item.reasoning_summary+item.risk_point_description+item.evidence_location
        if key=='S-05-04':
            assert '税费' in item.legal_consequence_if_missing
            assert '未约定发票' not in item.legal_consequence_if_missing
        item.reasoning_summary='旧结论重新污染'
        assert any(f['reason']=='SALE_DISPLAY_STATE_MISMATCH'
                   for f in engine._exact_element_report_invariants([item], []))
