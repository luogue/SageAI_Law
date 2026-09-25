"""Report evidence is the reverse projection of exact element proof edges."""
from copy import deepcopy

import pytest

from review_v2.clause_parser import parse_contract_clauses
from review_v2.obligation_detail_elements import development_document_elements
from review_v2.engine import _project_atomic_requirement_state, _apply_element_level_narratives
from tests.test_technology_exact_truth_pipeline import make_item


@pytest.mark.parametrize('text', [
    '使用甲方提供技术资料产生的纠纷除外。',
    '甲方交付的开发文档存在错误时，乙方不承担赔偿责任。',
    '对第三方提交的测试报告真实性不作保证。',
])
def test_document_mention_in_liability_clause_is_not_delivery_performance(text):
    elements = development_document_elements(parse_contract_clauses('第一条 责任\n' + text))
    assert all(e['status'] == 'MISSING' for e in elements)


def test_invoice_does_not_make_account_partial():
    clauses = parse_contract_clauses('第一条 价款\n本合同总价为人民币800000元。乙方应提供增值税发票。')
    item = make_item(); item.item_id = 'TC-04-02'
    _project_atomic_requirement_state(item, 'development_funding', clauses, allow_empty=True)
    elements = {e['element_id']: e for e in item.coverage_elements}
    assert elements['invoice']['status'] == 'COVERED'
    assert elements['account']['status'] == 'MISSING'
    assert not elements['account']['supporting_evidence']
    _apply_element_level_narratives([item])
    assert '收款账户已有部分' not in item.narrative_state['judgment']


def _document_item():
    clauses = parse_contract_clauses('第一条 交付\n乙方应向甲方交付安装部署文档。\n第二条 责任\n违约应赔偿损失。')
    item = make_item(); item.item_id = 'TC-13-01'
    _project_atomic_requirement_state(item, 'development_documents', clauses, allow_empty=True)
    return item, clauses


def test_unrelated_pool_source_is_rejected_then_removed_from_report_projection():
    from review_v2.element_evidence_projection import project, audit
    item, clauses = _document_item()
    clause = next(c for c in clauses if '赔偿' in c.text)
    item.evidence_clauses.append(dict(evidence_id='unrelated', clause_id=clause.clause_id,
                                     quote=clause.text, source_type='BODY'))
    assert any(f['reason'] == 'EVIDENCE_POLLUTION' for f in audit([item], [], clauses))
    project([item], [], clauses)
    assert not any(r.get('evidence_id') == 'unrelated' for r in item.evidence_clauses)
    assert not audit([item], [], clauses)
    assert all(r.get('supporting_element_ids') for r in item.evidence_clauses)


def test_alias_evidence_keeps_exact_element_ownership_not_topic_ownership():
    from review_v2.element_evidence_projection import project, audit
    item, clauses = _document_item()
    project([item], [], clauses)
    positives = [r for r in item.evidence_clauses if r.get('source_type') != 'SEARCH_AUDIT']
    assert any({'deployment_document_delivery', 'installation_document_delivery'} <= set(r['supporting_element_ids']) for r in positives)
    row = positives[0]
    row['supporting_element_ids'].append('test_report_delivery')
    assert any(f['reason'] == 'EVIDENCE_ELEMENT_SEMANTIC_MISMATCH' for f in audit([item], [], clauses))


def test_negative_only_element_cannot_remain_partial():
    from review_v2.element_evidence_projection import normalize_partial_states
    item, clauses = _document_item()
    element = next(e for e in item.coverage_elements if e['element_id'] == 'test_report_delivery')
    element['status'] = 'PARTIALLY_COVERED'
    item.evidence_clauses.append(dict(source_type='SEARCH_AUDIT', evidence_id='audit',
                                     supporting_element_ids=[element['element_id']], search_targets=['测试报告交付']))
    fixes = normalize_partial_states([item], clauses)
    assert fixes and element['status'] == 'MISSING'
    assert not element['evidence_ids']


def test_partial_with_exact_positive_source_is_preserved():
    from review_v2.element_evidence_projection import normalize_partial_states
    item, clauses = _document_item()
    element = next(e for e in item.coverage_elements if e['element_id'] == 'deployment_document_delivery')
    element['status'] = 'PARTIALLY_COVERED'
    assert not normalize_partial_states([item], clauses)
    assert element['status'] == 'PARTIALLY_COVERED'


def test_search_audit_requires_single_exact_element_target():
    from review_v2.element_evidence_projection import project, audit
    item, clauses = _document_item()
    project([item], [], clauses)
    audits = [r for r in item.evidence_clauses if r.get('source_type') == 'SEARCH_AUDIT']
    assert audits
    assert all(len(r['supporting_element_ids']) == 1 and r['element_search']['element_id'] == r['supporting_element_ids'][0] for r in audits)
    audits[0]['supporting_element_ids'] = []
    assert any(f['reason'] == 'EVIDENCE_POLLUTION' for f in audit([item], [], clauses))


@pytest.mark.parametrize('elements', [[], [dict(element_id='affirmative_fact', status='NOT_APPLICABLE')]])
def test_negative_rule_search_context_is_not_positive_report_evidence(elements):
    from review_v2.technology_adverse_evidence import prepare_negative_audits, verify_negative_search
    from review_v2.element_evidence_projection import project, audit
    item = make_item(); item.item_id = 'TC-02-02'; item.coverage_status = '通过'; item.coverage_elements = elements
    clauses = parse_contract_clauses('第一条 侵权责任\n乙方负责处理第三方索赔。')
    item.evidence_clauses = [dict(clause_id=c.clause_id, quote=c.text) for c in clauses]
    prepare_negative_audits([item], clauses)
    assert audit([item], [], clauses)
    project([item], [], clauses)
    assert not item.evidence_clauses
    assert verify_negative_search(item, clauses)['status'] == 'PASS'
    assert not audit([item], [], clauses)


def test_shared_scoped_fact_is_not_lost_after_family_projection():
    from review_v2.engine import _project_shared_material_disposition
    from review_v2.element_evidence_projection import project, audit
    clauses = parse_contract_clauses('第一条 成果\n本项目开发形成的软件源代码归甲方所有。\n第二条 处置\n合同终止后，乙方应将甲方提供的技术资料全部删除，并提交书面删除确认函。')
    item = make_item(); item.item_id = 'TC-05-03'
    _project_atomic_requirement_state(item, 'development_result', clauses, allow_empty=True)
    _project_shared_material_disposition(item, clauses, [dict(actor='乙方', material_owner='甲方')], preserve_ownership=True)
    shared = next(e for e in item.coverage_elements if e['element_id'] == 'material_disposition')
    assert shared['supporting_evidence']
    project([item], [], clauses)
    assert any('material_disposition' in r.get('supporting_element_ids', []) and '全部删除' in r.get('quote', '') for r in item.evidence_clauses)
    assert not audit([item], [], clauses)
