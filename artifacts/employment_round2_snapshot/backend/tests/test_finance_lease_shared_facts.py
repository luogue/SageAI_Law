"""Source binding, scenario and report integration regressions."""
from pathlib import Path
from zipfile import ZipFile
from xml.etree import ElementTree as ET

import pytest

from review_v2.clause_parser import parse_contract_clauses
from review_v2.finance_lease_facts import FinanceLeaseFacts
from review_v2.engine import review_contract_v2, _check_legal_reference_freshness, _legal_reference_findings


def facts(text):
    return FinanceLeaseFacts(parse_contract_clauses(text))


@pytest.mark.parametrize("alias", ["乙方", "甲方"])
def test_claim_aliases_and_source_binding(alias):
    other = "甲方" if alias == "乙方" else "乙方"
    text = f"出租人：测试租赁公司（以下简称{other}）\n承租人：测试工厂（以下简称{alias}）\n第一条 索赔\n{alias}直接向供货方主张权利，{other}应提供必要协助。"
    evidence = facts(text).evidence("lessee_claim_against_seller")
    assert {x for e in evidence for x in e['supports_element_ids']} == {'fl_direct_seller_claim', 'fl_lessor_claim_assistance'}
    assert all(e['quote'] in text for e in evidence)


def test_supplier_repairs_do_not_prove_lessee_maintenance():
    f = facts("第一条 质量\n出租人协助承租人向供货方主张维修权利。")
    assert not f.evidence('insurance_and_maintenance')


@pytest.mark.parametrize("seller,extra,active", [("供应商", "", False), ("测试工厂", "", True), ("供应商", "本合同采用售后回租。", True), ("供应商", "本合同不属于售后回租。", False)])
def test_leaseback_gate(seller, extra, active):
    f = facts(f"承租人：测试工厂\n供货方：{seller}\n第一条 模式\n{extra}")
    for node in ['sale_leaseback_identification', 'sale_leaseback_asset_title', 'sale_leaseback_not_disguised_loan']:
        assert f.applicability(node)['applicable'] is active


@pytest.mark.parametrize("election,adverse", [("", True), ("上述两项救济只能择一。", False)])
def test_shared_remedy_election(election, adverse):
    f = facts("第一条 违约\n出租人可要求全部剩余租金。\n出租人可收回租赁物。" + election)
    assert f.double_remedy_risk is adverse


def test_expiry_return_does_not_prove_invalid_contract_return():
    f = facts("第一条 期满\n租赁期满承租人返还出租人，保持良好状态。")
    assert f.evidence('end_return_condition')
    assert not f.evidence('invalid_asset_ownership')


def test_multiple_repealed_laws_aggregate_without_matching_labor_contract_law():
    issues = _check_legal_reference_freshness("签订日期：2026年9月7日。依据《中华人民共和国担保法》和《合同法》。适用《劳动合同法》。")
    assert len(issues) == 2
    assert all(x['risk_type'] == 'outdated_law_reference' for x in issues)
    findings = _legal_reference_findings(issues)
    assert len(findings) == 1
    assert '担保法' in findings[0].recommendation
    assert '民法典' in findings[0].recommendation
    assert not _check_legal_reference_freshness('《担保法》已废止，不再引用。')


def test_explicit_fiction_and_refusal_override_are_not_silenced():
    r = review_contract_v2('第一条 租赁物\n双方虚构租赁物，本交易无真实设备，仅供融资。', 'finance_lease', use_llm=False)
    for item in r['items']:
        if item['item_id'] in {'FL-03-01', 'FL-03-02'}:
            assert item['coverage_status'] == '风险条款'
    r = review_contract_v2('第一条 交付\n无论设备是否严重不合格，承租人不得拒收。', 'finance_lease', use_llm=False)
    item = next(i for i in r['items'] if i['item_id'] == 'FL-06-02')
    assert item['coverage_status'] == '部分覆盖'
    assert item['evidence_clauses']


def test_rent_schedule_does_not_prove_registration_and_insurance():
    evidence = facts('第一条 附件\n租金支付表作为本合同附件。').evidence('rent_registration_insurance_attachment')
    assert {key for e in evidence for key in e['supports_element_ids']} == {'fl_rent_document'}


@pytest.fixture(scope='module')
def current_review():
    source = Path(__file__).resolve().parents[2] / 'test_data' / '52 融资租赁合同.docx'
    with ZipFile(source) as z:
        root = ET.fromstring(z.read('word/document.xml'))
    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    text = '\n'.join(''.join(p.itertext()) for p in root.findall('.//w:p', ns))
    return review_contract_v2(text, 'finance_lease', use_llm=False)


def test_current_45_rule_review_and_report_closure(current_review):
    r = current_review
    by_id = {i['item_id']: i for i in r['items']}
    assert len(by_id) == 45
    for key in ['FL-07-03', 'FL-08-01', 'FL-09-01', 'FL-12-01', 'FL-12-02', 'FL-12-03', 'FL-15-01', 'FL-04-01', 'FL-04-03', 'FL-09-03']:
        assert by_id[key]['coverage_status'] == '通过', key
        assert by_id[key]['evidence_clauses'], key
    for key in ['FL-14-01', 'FL-14-02', 'FL-14-03']:
        assert by_id[key]['coverage_status'] == '不适用'
    for key in ['FL-03-01', 'FL-03-02']:
        assert by_id[key]['coverage_status'] == '待核验'
        assert by_id[key]['risk_severity'] == 'NONE'
    for key in ['FL-10-01', 'FL-10-02']:
        assert by_id[key]['coverage_status'] == '风险条款'
        assert by_id[key]['action_priority'] == 'A_CORE'
    remedy = [f for f in r['risk_findings'] if f['risk_group'] == 'finance_lease_remedy_election']
    assert len(remedy) == 1
    assert set(remedy[0]['source_review_ids']) == {'FL-10-01', 'FL-10-02'}
    assert len([f for f in r['risk_findings'] if f['risk_group'] == 'finance_lease_recovery_settlement']) == 1
    assert r['final_overview_summary']['priority_action'] == 2
    assert r['final_disposition_summary']['must_change'] == 2
    assert r['release_quality_gate']['status'] == 'REPORT_READY'
    assert not r['release_quality_gate']['failures']
    assert any('担保法' in x['law_name'] for x in r['legal_reference_issues'])


@pytest.mark.parametrize('scenario,active', [
    ('设备购买合同及验收文件为附件。', False),
    ('本合同不涉及技术许可或技术开发。', False),
    ('出租人同时提供技术许可，须交付工艺包和技术成果。', True),
    ('双方约定技术开发成果及源代码交付。', True),
])
def test_technical_attachment_scenario_gate(scenario, active):
    assert facts('第一条 交付\n' + scenario).applicability('technical_delivery_attachment')['applicable'] is active


def test_reminders_and_core_risks_survive_full_review(current_review):
    r = current_review
    for item in r['items']:
        if item['coverage_status'] == '法律提示':
            narrative = item['decision_trace']['effective_gap_narrative']['generated_narrative']
            assert '明确法定规则' in narrative
            assert '无需修改' in narrative
            assert '未识别到' not in str(item)
        if item['item_id'] == 'FL-15-02':
            assert item['coverage_status'] == '不适用'
            assert not item.get('risk_finding_ids')
    settlement = next(f for f in r['risk_findings'] if f['risk_group'] == 'finance_lease_recovery_settlement')
    assert settlement['severity'] == 'HIGH'
    assert settlement['priority'] == 'A_CORE'
    assert set(settlement['source_review_ids']) == {'FL-10-03', 'FL-13-01', 'FL-13-02', 'FL-13-03'}


def test_generic_reminder_renderer_does_not_require_finance_lease_node(current_review):
    from review_v2.engine import ReviewItemResult, _apply_default_law_narratives
    source = next(i for i in current_review['items'] if i['coverage_status'] == '法律提示')
    item = ReviewItemResult(**source)
    item.node_id, item.item_id = 'generic_default_rule', 'GENERIC-01'
    item.decision_trace = {'effective_gap': {'statutory_default': 'CLEAR_DEFAULT', 'statutory_default_elements': ['法定处理规则'], 'still_unprotected_elements': []}}
    narrative = _apply_default_law_narratives([item])[0]['generated_narrative']
    assert '明确法定规则' in narrative and '无需修改' in narrative
    assert item.legal_consequence_if_missing == narrative
