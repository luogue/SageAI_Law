"""The original processing contract and independent sale/binding regressions."""
from pathlib import Path
from zipfile import ZipFile
from xml.etree import ElementTree as ET
import pytest

from review_v2.engine import review_contract_v2, _element_supported_by_evidence
from review_v2.clause_parser import parse_contract_clauses
from review_v2.domain_selection import resolve_domain_selection
from review_v2.sale_evidence import PROFILES, extract, supports, inspection_period_context
from review_v2.work_evidence import FORBIDDEN


def document(name):
    with ZipFile(Path(__file__).resolve().parents[2] / 'test_data' / name) as z:
        root = ET.fromstring(z.read('word/document.xml'))
    return '\n'.join(''.join(p.itertext()) for p in root.findall('.//{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p'))


@pytest.fixture(scope='module')
def work():
    return review_contract_v2(document('56 承揽合同.docx'), 'sale', use_llm=False)


@pytest.mark.parametrize('roles', [('承揽方','定作方'),('承揽人','定作人')])
def test_commissioned_result_controls_incidental_goods_words(roles):
    a,b=roles
    text=f'{a}：制造公司。{b}：客户公司。{b}委托{a}加工零件，按照图纸和样品生产加工。产品价款、交付和验收依约。'
    result, _, route = resolve_domain_selection('sale', text, parse_contract_clauses(text))
    assert route == 'work_contract'
    assert result.resolution == 'DOCUMENT_OVERRIDE'


def test_current_work_full_route_and_each_positive_element(work):
    assert work['contract_type'] == 'work_contract'
    assert work['contract_type_name'] == '承揽合同'
    assert len(work['items']) == 44
    assert all(i['item_id'].startswith('W-') for i in work['items'])
    assert work['release_quality_gate']['status'] == 'REPORT_READY'
    assert not work['release_quality_gate']['failures']
    clauses = {c.clause_id:c for c in parse_contract_clauses(document('56 承揽合同.docx'))}
    for item in work['items']:
        if item['node_id'] in FORBIDDEN or item['coverage_status'] == '不适用':
            continue
        requirements = {r['element_id']:r for r in item['decision_trace']['work_required_elements']}
        for element in item['coverage_elements']:
            requirement = requirements[element['element_id']]
            positive = [e for e in item['evidence_clauses'] if supports(requirement, e['quote'])]
            if element['status'] == 'COVERED':
                assert positive, (item['item_id'], element)
                assert all(e['quote'].replace('\n','') in clauses[e['clause_id']].text.replace('\n','') for e in positive)
                for binding in element.get('supporting_evidence', []):
                    assert supports(requirement, binding['quote'])
            elif element['status'] == 'MISSING':
                assert not positive
                # Check the entire source corpus, not only the row's selected
                # evidence packet, before accepting an absence conclusion.
                assert not extract(item['node_id'], list(clauses.values()), {item['node_id']: [requirement]})
        if item['coverage_status'] in {'通过','部分覆盖'}:
            assert item['evidence_clauses']


def test_warranty_quantity_effective_date_and_shared_acceptance_sources(work):
    store = work['deterministic_analysis']['canonical_work_source_facts']['facts']
    def selected(key): return [e for e in store if key in e['supported_elements']]
    assert any('12个月' in e['quote'] and '第二条' in e['location'] for e in selected('goods_warranty_duration'))
    assert any('5000套' in e['quote'] for e in selected('goods_subject_quantity'))
    assert not any('18吨' in e['quote'] for e in selected('goods_subject_quantity'))
    assert any('2026年9月8日' in e['quote'] for e in selected('contract_effective_condition'))
    acceptance = selected('goods_inspection_deadline')
    assert all(e['location'] == '第六条第3项' for e in acceptance)
    item = next(i for i in work['items'] if i['item_id']=='W-07-03')
    assert any(e['evidence_id'] == acceptance[0]['evidence_id'] for e in item['evidence_clauses'])
    assert any(e['element_id']=='goods_warranty_duration' and e['status']=='COVERED' for i in work['items'] if i['item_id']=='W-07-01' for e in i['coverage_elements'])


def test_raw_clause_cannot_lend_support_to_unrelated_quote():
    element=PROFILES['sale_quality_remedy'][2]
    source={'quote':'未经同意不得更换材料型号。','text':'质量不合格应免费修理或更换。'}
    assert _element_supported_by_evidence(element, source)[0] == 'MISSING'
    assert not supports(element, source['quote'])


def test_sale_warranty_and_inspection_are_independent_of_payment_and_materials():
    clauses=parse_contract_clauses(document('56 承揽合同.docx'))
    period=extract('sale_inspection_period', clauses)
    shared=inspection_period_context(clauses)['periods']
    assert all(p['location']=='第六条第3项' for p in period)
    assert any(p['evidence_id']==s['evidence_id'] for p in period for s in shared)
    assert not any('quality_remedy_method' in e['supported_elements'] for e in extract('sale_quality_remedy',clauses))
    assert any('goods_warranty_duration' in e['supported_elements'] for e in extract('sale_warranty_period',clauses))


def test_normal_sale_contract_stays_sale():
    r=review_contract_v2(document('2 买卖合同.docx'), 'sale', use_llm=False)
    assert r['contract_type']=='sale'
    assert all(i['item_id'].startswith('S-') for i in r['items'])
    assert r['release_quality_gate']['status']=='REPORT_READY', r['release_quality_gate']['failures']
