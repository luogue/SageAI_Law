import pytest
from review_v2.clause_parser import parse_contract_clauses
from review_v2.construction_coverage import PROFILES, extract, supports
from review_v2.penalty_base import analyze, total_price_definitions


def covered(node,text):
    rows=extract(node,parse_contract_clauses(text))
    return {e['element_id'] for e in PROFILES[node] if any(supports(e,r['text']) for r in rows)}

@pytest.mark.parametrize('node,text,key',[
 ('construction_scope_and_site','工程内容：建设厂房及配套道路。','scope'),
 ('construction_scope_and_site','承包人依据经确认的图纸和技术要求承担约定范围的施工。','scope'),
 ('quality_standard_acceptance','乙方应向甲方提交竣工验收申请。','acceptance'),
 ('quality_standard_acceptance','承包人须提交完整的竣工验收资料并申请验收。','acceptance'),
 ('quality_deposit_return_period','缺陷责任期届满且修复完成后十五日内，将质保金退还承包人。','deposit_return'),
 ('quality_deposit_return_period','质量保证金应在缺陷责任期届满并修复后20日内返还。','deposit_return'),
 ('project_price_pricing_method','本工程实行工程量清单综合单价计价方式。','pricing'),
 ('project_price_pricing_method','工程价款按照固定单价方式计价。','pricing'),
 ('settlement_procedure','竣工结算审核完成后45日内，发包人支付尾款。','settlement_payment'),
])
def test_relationships_accept_paraphrase_and_argument_order(node,text,key):
    assert key in covered(node,text)

@pytest.mark.parametrize('reverse',[False,True])
def test_independent_elements_aggregate_across_sections(reverse):
    parts=['第一条\n工程地点：某市工业园。','第二条\n工程内容：新建库房和装卸平台。']
    if reverse: parts.reverse()
    assert covered('construction_scope_and_site','\n'.join(parts))=={'scope','site'}
    parts=['第三条\n工程质量标准：达到国家验收规范合格标准。','第四条\n乙方应向甲方提交竣工验收申请。']
    if reverse: parts.reverse()
    assert covered('quality_standard_acceptance','\n'.join(parts))=={'standard','acceptance'}

@pytest.mark.parametrize('prefix',['构成本合同的文件包括：','本合同文件由以下资料组成：','合同文件包括：'])
def test_document_membership_retains_list_scope(prefix):
    text=prefix+'\n工程量清单；\n经确认的施工图纸；\n技术标准及要求。'
    assert covered('drawing_technical_spec_attachment',text)=={'drawings','specifications'}
    assert covered('boq_pricing_attachment',text)=={'pricing_attachment'}

@pytest.mark.parametrize('reverse',[False,True])
def test_money_definition_and_formula_cross_chapters(reverse):
    parts=['第一条\n本合同暂定含税总价为人民币：\n￥7,350,000.00元。','第二条\n乙方按照合同暂定总价的0.04%每日向甲方支付违约金。']
    if reverse:parts.reverse()
    rows=analyze('\n'.join(parts))
    assert rows and all(r['status']=='DETERMINABLE' for r in rows)
    assert '7,350,000' in rows[0]['definitions'][0]

@pytest.mark.parametrize('text',[
 '合同最终总价为500元。',
 '合同暂定总价为500元。合同暂定总价为800元。',
 '合同暂定总价待另行确认。',
])
def test_price_qualifier_and_ambiguity_guard(text):
    assert not total_price_definitions('合同暂定总价',text)

@pytest.mark.parametrize('node,text',[
 ('quality_standard_acceptance','乙方无需提交竣工验收申请。'),
 ('quality_standard_acceptance','竣工验收合格后，乙方应提交竣工结算资料。'),
 ('quality_standard_acceptance','隐蔽工程完成后，乙方应通知甲方进行验收。'),
 ('boq_pricing_attachment','本工程采用工程量清单计价。单价由乙方提出价格组成，经甲方确认。'),
 ('project_price_pricing_method','尚未确定本工程采用何种计价方式。'),
 ('quality_deposit_return_period','质保金修复问题将在30日内商议。'),
 ('settlement_procedure','甲方收到结算审核意见后5日内提出异议。'),
 ('drawing_technical_spec_attachment','本工程施工时需参考图纸及技术标准。'),
])
def test_topic_overlap_is_not_positive_relation(node,text):
    assert not covered(node,text)


def test_source_quote_keeps_multiline_support_and_final_search_uses_same_requirement():
    from review_v2.engine import review_contract_v2
    r=review_contract_v2('建设工程施工合同\n第一条\n构成本合同的文件包括：\n合同协议书；\n工程量清单；\n施工图纸；\n技术标准及要求。','construction',use_llm=False)
    for i in r['items']:
        if i['item_id'] not in {'CE-13-01','CE-13-02'}:continue
        assert i['coverage_status']=='通过'
        assert all(e['status']=='COVERED' for e in i['coverage_elements'])
        assert all(e['verified_original'] and e['quote']==e['text'] for e in i['evidence_clauses'])
        assert not any(s['result']=='NOT_FOUND' for s in i['decision_trace'].get('element_absence_searches',[]))
    assert r['release_quality_gate']['status']=='REPORT_READY'


def test_current_document_production_entry_atomic_evidence_consistency():
    from pathlib import Path
    from fastapi import FastAPI
    from fastapi.testclient import TestClient
    from routers import review_v2 as route
    app=FastAPI();app.include_router(route.router)
    app.dependency_overrides[route.get_current_user]=lambda:1
    source=next((Path(__file__).resolve().parents[2]/'test_data').glob('103 *.docx'))
    with TestClient(app) as client:
        response=client.post('/review-v2/file',data={'contract_type':'construction','use_llm':'false'},files={'file':(source.name,source.read_bytes())})
    assert response.status_code==200,response.text[:500]
    r=response.json();items={i['item_id']:i for i in r['items']}
    targets=['CE-01-03','CE-08-01','CE-08-03','CE-09-01','CE-09-02','CE-13-01','CE-13-02','COMMON-20-01']
    for rid in targets:
        i=items[rid]
        assert i['coverage_status']==('部分覆盖' if rid=='CE-09-02' else '通过')
        found={e['element_id'] for e in i['coverage_elements'] if e['status']=='COVERED'}
        assert found
        assert not any(s['result']=='NOT_FOUND' and s['element_id'] in found for s in i['decision_trace'].get('element_absence_searches',[]))
        assert all(e['verified_original'] for e in i['evidence_clauses'])
    states={e['element_id']:e['status'] for e in items['CE-09-02']['coverage_elements']}
    assert states['settlement_review']=='MISSING'
    assert states['settlement_payment']=='COVERED'
    assert sum(r['coverage_summary'].values())==len(items)
    assert r['release_quality_gate']['status']=='REPORT_READY',r['release_quality_gate']['failures']
