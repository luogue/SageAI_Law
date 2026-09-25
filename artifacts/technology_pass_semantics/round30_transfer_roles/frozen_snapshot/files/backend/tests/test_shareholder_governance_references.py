"""Governance relationship, reference integrity and performance-stage regressions."""
from pathlib import Path
import pytest
from review_v2.clause_parser import parse_contract_clauses as parse
from review_v2.company_governance_facts import governance_evidence, contribution_requirements
from review_v2.company_formation_checklist import COMPANY_FORMATION_CHECKLIST
from review_v2.priority_checklist_helpers import PROFILES
from review_v2.contract_references import analyze, augment


@pytest.mark.parametrize('heading', ['5. 验收', '5.1 验收标准', '5．验收'])
def test_decimal_article_is_equivalent_reference_target(heading):
    rows = analyze(parse(heading + '\n验收标准为性能测试合格。\n6. 付款\n达到本合同第五条约定的验收条件后付款。'))['common_internal_references']
    reference = next(row for row in rows if row['reference'] == '本合同第五条')
    assert reference['status'] == 'VALID'
    assert reference['target_ids']
    assert reference['reference_audit']['referenced_target_unresolved'] is False


def test_unresolved_reference_has_independent_index_audit():
    rows = analyze(parse('第一条 付款\n按本合同第五条执行。'))['common_internal_references']
    reference = next(row for row in rows if row['reference'] == '本合同第五条')
    audit = reference['reference_audit']
    assert reference['status'] == 'INVALID'
    assert audit['source_type'] == 'REFERENCE_AUDIT'
    assert audit['cross_reference_exists'] is True
    assert audit['referenced_target_unresolved'] is True
    assert audit['target_number'] not in audit['indexed_article_numbers']
    assert audit['searched_clause_ids'] and not audit['target_clause_ids']
from review_v2.engine import review_contract_v2


@pytest.mark.parametrize('identity,arrangement,risk', [
    ('甲方出资70万元，乙方出资30万元。', '公司不设股东会。', True),
    ('公司只有一个股东。', '公司不设股东会。', False),
    ('甲方出资70万元，乙方出资30万元。', '全体股东书面一致决定，可不召开股东会会议。', False),
    ('甲方出资70万元，乙方出资30万元。', '公司不设股东会。每月召开股东例会。', True),
    ('甲方出资70万元，乙方出资30万元。若转让后变更为一人有限责任公司，办理登记。', '公司不设股东会。', True),
])
def test_company_organ_relationship(identity, arrangement, risk):
    assert bool(governance_evidence('formation_no_shareholder_organ', parse('有限责任公司\n'+identity+'\n'+arrangement))) is risk


@pytest.mark.parametrize('text,invalid', [
    ('第一条 违约责任按第九条处理。\n第九条 通知送达。', True),
    ('第一条 违约责任按第九条处理。\n第九条 违约方赔偿全部损失。', False),
    ('一、责任\n违约责任依本协议第六条第2款处理。\n六、送达\n1、通知地址见首页。', True),
    ('第一条 违约责任依本合同第六条第2款处理。\n第六条 责任\n1、双方友好协商。\n2、违约方赔偿损失。', False),
    ('第一条 违约责任按第八条处理。\n第二条 合同生效。', True),
    ('第一条 违约责任依本合同第六条第2款处理。\n第六条 责任\n1、通知送达。\n2、承担下列责任：\n（1）违约方赔偿损失。\n3、争议提交仲裁。', False),
])
def test_internal_reference_existence_and_semantics(text, invalid):
    rows = analyze(parse(text))['common_internal_references']
    assert rows
    assert any(r['status'] == 'INVALID' for r in rows) is invalid


@pytest.mark.parametrize('text,status', [
    ('重大事项由股东决定，包括《公司法》第三十八条规定的其他事项。', 'INVALID'),
    ('分公司登记按照《公司法》第38条办理。', 'VALID'),
    ('股东会职权依《公司法》第五十九条执行。', 'VALID'),
    ('违约责任按照《民法典》第五百八十五条处理。', 'UNVERIFIED'),
])
def test_statute_topic_and_version(text, status):
    assert analyze(parse(text))['common_legal_references'][0]['status'] == status


def test_relative_reference_scope_and_attachment_verification():
    rows = analyze(parse('第一条 责任\n1、通知送达地址由双方确认。\n2、违约责任按照前款处理。\n3、技术资料详见附件2。'))['common_internal_references']
    assert next(r for r in rows if r['reference']=='按照前款')['status'] == 'INVALID'
    assert next(r for r in rows if '附件' in r['reference'])['status'] == 'UNVERIFIED'


@pytest.mark.parametrize('text,external', [
    ('双方共同投资设立公司，应于签署后20日内缴付出资。', False),
    ('双方已经完成实缴。', True),
])
def test_paid_evidence_is_not_drafting_requirement(text, external):
    rows = contribution_requirements(PROFILES['formation_contributions'], text)
    proof = [r for r in rows if r['element_id'] == 'formation_contributions_4']
    assert bool(proof) is external
    if proof:
        assert proof[0]['requirement_kind'] == 'EXTERNAL_VERIFICATION'


def test_equity_common_and_special_composition():
    nodes = {c.node_id for c in COMPANY_FORMATION_CHECKLIST}
    assert {'common_general_breach','common_contract_termination','common_enforcement_costs','common_attachment_effect','formation_governance'} <= nodes
    assert not any(n.startswith('sale_') for n in nodes)
    from review_v2.contract_registry import get_checklist_for_resolution
    from types import SimpleNamespace
    ordinary = get_checklist_for_resolution('shareholders', SimpleNamespace(domain_attributes={}))
    assert {'common_general_breach', 'formation_no_shareholder_organ', 'equity_governance'} <= {c.node_id for c in ordinary}


def test_completed_payment_remains_external_in_production():
    text = '股东合作协议\n甲方与乙方共同投资设立有限责任公司。注册资本100万元。\n甲方出资60万元，乙方出资40万元，均为现金出资。双方已经完成实缴。股权比例60%、40%。公司设董事、监事；利润由股东分配。'
    result = review_contract_v2(text, 'shareholders', use_llm=False)
    item = next(i for i in result['items'] if i['node_id']=='formation_contributions')
    assert all(e['element_id'] != 'formation_contributions_4' for e in item['coverage_elements'])
    assessments = item['decision_trace']['requirement_kind_assessments']
    assert any(e['status']=='PENDING_VERIFICATION' and e['contract_coverage_required'] is False for e in assessments)


def test_sale_production_also_executes_reference_audit():
    text = '设备买卖合同\n卖方向买方出售机器，买方支付价款十万元。\n第一条 违约责任按第九条处理。\n第九条 通知送达地址由双方确认。'
    result = review_contract_v2(text, 'sale', use_llm=False)
    item = next(i for i in result['items'] if i['node_id']=='common_internal_references')
    assert result['contract_type'] == 'sale'
    assert item['coverage_status'] == '风险条款'


def test_original_report_governance_and_reference_consistency():
    from fastapi import FastAPI
    from fastapi.testclient import TestClient
    from routers import review_v2 as route
    app = FastAPI(); app.include_router(route.router)
    app.dependency_overrides[route.get_current_user] = lambda: {'id':'governance-regression'}
    source = Path(__file__).resolve().parents[2] / 'test_data' / '83 投资协议.docx'
    with TestClient(app) as client:
        response = client.post('/review-v2/file', data={'contract_type':'investment','use_llm':'false','include_low_risk':'true'},
            files={'file':(source.name,source.read_bytes(),'application/vnd.openxmlformats-officedocument.wordprocessingml.document')})
    assert response.status_code == 200
    result = response.json(); nodes = {i['node_id']:i for i in result['items']}
    assert result['contract_type'] == 'shareholders'
    assert result['release_quality_gate']['status'] == 'REPORT_READY', result['release_quality_gate']['failures']
    assert not any(n.startswith('sale_') for n in nodes)
    for node in ['formation_no_shareholder_organ','formation_governance','formation_unilateral_control','formation_capital_increase','common_internal_references','common_legal_references']:
        assert nodes[node]['coverage_status'] == '风险条款', node
    assert '第九条第2款' in nodes['common_internal_references']['risk_point_description']
    assert 'formation_contributions_4' not in [e['element_id'] for e in nodes['formation_contributions']['coverage_elements']]
    assert 'common_general_breach' in nodes and 'common_contract_termination' in nodes
