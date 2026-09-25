"""Generalized route/applicability regressions plus complete production HTTP upload."""
from pathlib import Path
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from review_v2.clause_parser import parse_contract_clauses
from review_v2.domain_selection import resolve_domain_selection, domain_selection_consistency_gate
from review_v2.engine import _is_checkpoint_applicable, review_contract_v2
from review_v2.sale_contract_checklist import get_sale_checklist

FORMATION = '''共同出资设立协议
双方联合出资设立海岚有限责任公司。注册资本300万元。
甲方以设备、原材料和技术成果出资180万元，乙方以现金出资120万元，股权比例为60%、40%。
公司设董事及监事。利润按出资比例分配，股东会决定重大事项。
双方在签订后15日内交付出资资产。经营范围：设备销售、原材料采购及技术服务。
'''
SALE = '''设备买卖合同
出卖人：海风机械有限公司。买受人：山川制造有限公司。
卖方向买方出售机床5台，货款50万元。签署后10日内交货至买方工厂，验收后支付货款。
质量标准依技术附件，质保期一年。包装须适于陆运，由卖方委托承运人运输。
'''

@pytest.mark.parametrize('text,selected,expected', [
    (SALE, 'sale', 'sale'),
    (SALE, 'investment', 'sale'),
    (FORMATION, 'sale', 'shareholders'),
    (FORMATION.replace('共同出资设立协议', '入股合作协议书'), 'investment', 'shareholders'),
    (FORMATION.replace('共同出资设立协议', '合作安排').replace('300万元', '900万元').replace('60%、40%', '70%、30%'), 'sale', 'shareholders'),
    ('增资扩股协议\n投资方向目标公司新增注册资本认缴500万元取得股权。设备、原材料作为出资。', 'sale', 'capital_increase'),
    ('股权转让协议\n转让方向受让方转让目标公司40%股权，转让价款100万元。公司经营范围：设备销售。', 'sale', 'equity_transfer'),
])
def test_primary_relationship_routes(text, selected, expected):
    result, domain, actual = resolve_domain_selection(selected, text, parse_contract_clauses(text))
    assert actual == expected
    if expected != 'sale':
        assert domain.contract_family == 'EQUITY_INVESTMENT'
        assert not any(pack.startswith('sale/') for pack in domain.selected_domain_packs)

@pytest.mark.parametrize('suffix,triggered', [
    ('', False), ('【测试用途：虚构主体信息】', False), ('本文件仅作测试用途。', False),
    ('本交易不设试用期。', False), ('设备无需试运行。', False),
    ('设备先试后买。', True), ('买受人享有试用期。', True), ('交付后试运行。', True),
])
def test_trial_requires_operative_trigger(suffix, triggered):
    text = SALE + suffix
    for checkpoint in get_sale_checklist():
        if checkpoint.node_id.startswith('sale_trial_'):
            assert _is_checkpoint_applicable(text, checkpoint, 'sale')[0] is triggered

def test_equity_scope_rejects_goods_specials_even_if_called_directly():
    for checkpoint in get_sale_checklist():
        if checkpoint.node_id.startswith('sale_'):
            assert not _is_checkpoint_applicable(FORMATION, checkpoint, 'shareholders')[0]

def test_trial_absence_cannot_become_missing_in_report():
    result = review_contract_v2(SALE + '\n【测试用途：虚构模拟数据】', 'sale', use_llm=False)
    for item in result['items']:
        if item['node_id'].startswith('sale_trial_'):
            assert item['coverage_status'] == '不适用'
            assert item['applicability']['applicable'] is False
            assert not item['suggested_clause_example']
    assert result['contract_type'] == 'sale'

@pytest.mark.parametrize('node,suffix,expected', [
    ('sale_retention_registration', '', False),
    ('sale_retention_registration', '分三期支付货款。', False),
    ('sale_retention_registration', '付清货款前，卖方保留货物所有权。', True),
    ('sale_installment_payment', '', False),
    ('sale_installment_payment', '货款分三期支付。', True),
    ('sale_sample_quality', '设备有展示样品。', False),
    ('sale_sample_quality', '凭样品买卖，以样品为准。', True),
    ('sale_risk_goods_in_transit', '卖方负责运输。', False),
    ('sale_risk_goods_in_transit', '本次买卖在途货物，标的已发运。', True),
    ('sale_risk_carrier_delivery', '', False),
    ('sale_risk_carrier_delivery', '卖方委托承运人运输。', True),
])
def test_conditional_sale_branches(node, suffix, expected):
    checkpoint = next(c for c in get_sale_checklist() if c.node_id == node)
    base = '设备买卖合同\n卖方向买方出售机器一台，买方支付货款30万元。'
    assert _is_checkpoint_applicable(base+suffix, checkpoint, 'sale')[0] is expected

def test_exact_original_through_multipart_production_entry():
    from routers import review_v2 as route
    app = FastAPI()
    app.include_router(route.router)
    app.dependency_overrides[route.get_current_user] = lambda: {'id': 'formation-regression'}
    source = Path(__file__).resolve().parents[2] / 'test_data' / '83 投资协议.docx'
    with TestClient(app) as client:
        response = client.post('/review-v2/file', data={
            'contract_type': 'investment', 'include_low_risk': 'true', 'use_llm': 'false',
            'profile_json': '{"user_identity":"个人租客/买方","contract_scenario":"商品买卖"}',
        }, files={'file': (source.name, source.read_bytes(), 'application/vnd.openxmlformats-officedocument.wordprocessingml.document')})
    assert response.status_code == 200, response.text
    result = response.json()
    assert result['contract_type'] == 'shareholders'
    assert result['report_context']['family'] == 'EQUITY_INVESTMENT'
    assert result['report_context']['scenario_label'] != '商品买卖'
    assert result['report_context']['user_role'] not in ('buyer', 'BUYER')
    assert result['release_quality_gate']['status'] == 'REPORT_READY', result['release_quality_gate']['failures']
    assert not any(i['node_id'].startswith('sale_') for i in result['items'])
    by_node = {i['node_id']: i for i in result['items']}
    for node in ('formation_unsuitable_assets','formation_unilateral_control','formation_return_capital','formation_transfer_effect'):
        assert by_node[node]['coverage_status'] == '风险条款'
    contributions = by_node['formation_contributions']
    deadline = next(e for e in contributions['coverage_elements'] if e['element_id'] == 'formation_contributions_3')
    assert deadline['status'] == 'COVERED'
    assert '交货时间' not in result['result']
    assert by_node['formation_deadlock']['coverage_status'] == '部分覆盖'
    assert result['production_path_trace']['runtime_source_drift']['status'] == 'CURRENT'

def test_scenario_gate_rejects_accidental_sale_rule_injection():
    resolution, _, _ = resolve_domain_selection('investment', FORMATION, parse_contract_clauses(FORMATION))
    assert domain_selection_consistency_gate(resolution, ['CF-01-01', 'S-10-02'])['status'] == 'BLOCKED'

def test_unknown_applicability_is_not_false():
    from review_v2.engine import _applicability_result_for_checkpoint
    checkpoint = next(c for c in get_sale_checklist() if c.node_id == 'sale_approval_license')
    applies, reason = _is_checkpoint_applicable(SALE, checkpoint, 'sale')
    result = _applicability_result_for_checkpoint(checkpoint, parse_contract_clauses(SALE), applies, reason, contract_type_key='sale')
    assert result['applicable'] is None
    assert result['applicability_state'] == 'CONDITIONAL_UNRESOLVED'

def test_employment_termination_prefix_does_not_disable_lease_notice():
    from review_v2.contract_registry import get_checklist
    for checkpoint in get_checklist('house_lease'):
        if checkpoint.node_id in {'termination_period', 'termination_notice'}:
            assert _is_checkpoint_applicable('房屋租赁合同，出租人将房屋出租给承租人。', checkpoint, 'lease')[0]
    identity = next(c for c in get_checklist('labor') if c.node_id == 'employment_identity')
    assert _is_checkpoint_applicable('劳动合同，用人单位与劳动者建立劳动关系。', identity, 'labor')[0]
