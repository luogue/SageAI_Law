from copy import deepcopy
from pathlib import Path
from types import SimpleNamespace
import pytest
from review_v2.clause_parser import parse_contract_clauses
from review_v2.adverse_evidence import direct_evidence
from review_v2.adverse_consistency import gate
from review_v2 import monetary_consequences, penalty_base, contract_effects
from review_v2.construction_coverage import extract, PROFILES, supports
from review_v2.construction_applicability import tender_fact
from review_v2.construction_subtype import classify, applicability as subtype_applicability

@pytest.mark.parametrize('text',[
 '乙方不得再分包。', '转包行为发生时，甲方有权解除合同。',
 '存在违法再分包行为的，乙方承担赔偿责任。',
 '乙方违约责任：\n擅自再分包：合同价款百分之十的违约金；',
 '出现下列情形，委托人有权解除合同：\n受托人存在违法再分包行为；',
 '下列情形由乙方承担责任：\n乙方违法再分包；',
])
def test_protective_and_sanction_propositions(text):
    positive,counter=direct_evidence(parse_contract_clauses(text),(r'再分包|转包',))
    assert not positive
    assert counter

@pytest.mark.parametrize('text',['乙方可以再分包。','乙方不得再分包，但经书面批准可以再分包。','乙方可再分包，发生损失时承担赔偿责任。'])
def test_permission_and_exception_are_not_erased(text):
    assert direct_evidence(parse_contract_clauses(text),(r'再分包',))[0]

def adverse_item(audit='NOT_FOUND'):
    return dict(item_id='TEST',coverage_status='风险条款',evidence_clauses=[],
        coverage_elements=[dict(element_id='permission',status='ADVERSE')],
        decision_trace={'adverse_predicates':[r'再分包'], 'element_absence_searches':[
            dict(element_id='permission',result=audit,search_targets=['允许再分包'])]})

def test_audit_contradiction_blocks_even_if_original_is_positive():
    result=gate([adverse_item()],parse_contract_clauses('乙方可以再分包。'))
    assert result['status']=='BLOCKED'
    assert any(f['requirement']=='ADVERSE_SEARCH_AUDIT_CONTRADICTION' for f in result['failures'])

def test_affirmative_finding_with_sanction_source_is_blocked():
    assert gate([adverse_item('FOUND')],parse_contract_clauses('乙方再分包时，甲方有权解除。'))['status']=='BLOCKED'

def test_finding_cannot_escape_gate_by_leaving_item_pass():
    item=adverse_item();item['coverage_status']='通过'
    finding={'issue_type':'ADVERSE','source_review_ids':['TEST'],'evidence':[],'final_adverse_elements':[{'element_id':'permission','status':'ADVERSE'}]}
    assert gate([item],parse_contract_clauses('乙方可以再分包。'),[finding])['status']=='BLOCKED'

def test_consistent_affirmative_fact_is_allowed():
    assert gate([adverse_item('FOUND')],parse_contract_clauses('乙方可以再分包。'))['status']=='REPORT_READY'

def test_absence_of_prohibition_is_not_absence_of_permission():
    item=adverse_item()
    item['decision_trace']['element_absence_searches'][0]['search_targets']=['禁止再分包的约定']
    assert gate([item],parse_contract_clauses('乙方可以再分包。'))['status']=='REPORT_READY'

@pytest.mark.parametrize('event,amount,unit',[('工期延期','3,200','天'),('逾期竣工','500','日'),('交货延迟','12,000','次')])
def test_one_tariff_fact_is_reusable_without_consumption(event,amount,unit):
    text=f'乙方违约责任：\n{event}：{amount}元/{unit}；'
    clauses=parse_contract_clauses(text)
    rows=extract('delay_liability',clauses)
    assert rows and supports(PROFILES['delay_liability'][0],rows[0]['text'])
    analysis=penalty_base.analyze(text)
    assert any(r.get('fact_concept')=='delay' and r['status']=='DETERMINABLE' for r in analysis)
    assert rows==extract('delay_liability',clauses)

def test_price_list_without_breach_context_is_not_delay_liability():
    assert not monetary_consequences.facts('服务报价：\n工期延期：300元/天。')

@pytest.mark.parametrize('text',[
 '乙方对第三方财产损失负责，甲方不承担任何责任。',
 '甲方不得将服务委托第三方实施。第三方造成财产损失，甲方不承担赔偿责任。',
 '第三方发生事故由乙方赔偿，甲方免责。',
])
def test_no_delegation_no_delegation_waiver_rule(text):
    condition=contract_effects.applicability('common_delegated_service_waiver',parse_contract_clauses(text))
    assert condition['applicable'] is False
    assert not contract_effects.evidence('common_delegated_service_waiver',parse_contract_clauses(text))

def test_real_delegated_service_waiver_remains_adverse():
    text='乙方可以将保洁服务委托第三方实施。第三方在服务中造成财产损失，乙方不承担赔偿责任。'
    assert contract_effects.evidence('common_delegated_service_waiver',parse_contract_clauses(text))

def test_predicate_semantics_precede_legacy_keyword_priority(monkeypatch):
    from review_v2 import priority_contract_review, semantic_reviewer
    from review_v2.construction_contract_checklist import get_construction_checklist
    monkeypatch.setattr(priority_contract_review,'judge',lambda *a:SimpleNamespace(coverage_status='风险条款'))
    checkpoint=next(c for c in get_construction_checklist() if c.node_id=='no_re_subcontract')
    assert semantic_reviewer.judge_checkpoint(checkpoint,parse_contract_clauses('乙方违法再分包时，甲方有权解除合同。')).coverage_status=='通过'

def test_late_polarity_inversion_stops_formal_report(monkeypatch):
    from review_v2 import engine
    original=engine._report_evidence_projection
    def inject(findings,items):
        item=next(i for i in items if i.node_id=='no_re_subcontract')
        item.coverage_status='风险条款'
        item.risk_point_description='合同允许再分包。'
        return original(findings,items)
    monkeypatch.setattr(engine,'_report_evidence_projection',inject)
    result=engine.review_contract_v2('建设工程施工合同\n第一条\n乙方不得再分包。','construction',use_llm=False)
    assert result['release_quality_gate']['status']=='BLOCKED'
    assert '风险证据极性一致性校验未通过，正式报告未生成' in result['result']
    assert '合同允许再分包' not in result['result']

def test_current_upload_full_chain():
    from fastapi import FastAPI
    from fastapi.testclient import TestClient
    from routers import review_v2 as route
    app=FastAPI();app.include_router(route.router);app.dependency_overrides[route.get_current_user]=lambda:1
    source=next((Path(__file__).resolve().parents[2]/'test_data').glob('97 *.docx'))
    with TestClient(app) as client:
        response=client.post('/review-v2/file',data={'contract_type':'construction','use_llm':'false'},files={'file':(source.name,source.read_bytes())})
    assert response.status_code==200
    report=response.json();items={i['item_id']:i for i in report['items']}
    for rid in ('CE-01-01','CE-05-04','CE-07-04'):
        assert items[rid]['coverage_status']=='通过',rid
    re_sub = items['CE-05-03']
    assert re_sub['coverage_status']=='部分覆盖'
    restriction = next(e for e in re_sub['coverage_elements'] if e['element_id']=='action_restriction')
    assert restriction['status']=='COVERED'
    shared = [e for e in re_sub['evidence_clauses'] if '再分包' in e['text']]
    assert shared and all(e.get('verified_original') for e in shared)
    assert items['CE-05-01']['coverage_status']=='部分覆盖'
    assert items['CE-05-02']['coverage_status']=='不适用'
    assert not items['CE-05-02']['evidence_clauses']
    for rid in ('CE-05-01',):
        assert {e['evidence_id'] for e in shared} & {e['evidence_id'] for e in items[rid]['evidence_clauses']}
    assert all(s['element_id']!='action_restriction' or s['result']=='FOUND'
               for s in re_sub['decision_trace'].get('element_absence_searches',[]))
    assert items['COMMON-40-01']['coverage_status']=='不适用'
    assert any(e['element_id'].endswith('_fixed_rate') and e['status']=='COVERED' for e in items['COMMON-20-01']['coverage_elements'])
    assert set(e['clause_id'] for e in items['CE-07-04']['evidence_clauses']) & set(e['clause_id'] for e in items['COMMON-20-01']['evidence_clauses'])
    assert sum(report['coverage_summary'].values())==len(items)
    assert report['release_quality_gate']['status']=='REPORT_READY',report['release_quality_gate']['failures']
    assert report['release_quality_gate']['gate_results']['ADVERSE_POLARITY_AUDIT_GATE']=='PASS'

@pytest.mark.parametrize('text',[
    '建设工程施工合同。中标通知书作为合同组成部分。',
    '建设工程施工合同。招标文件、投标文件已归档。',
])
def test_tender_fact_is_shared_across_dependent_rules(text):
    assert tender_fact(text)['triggered']

def test_no_tender_fact_disables_all_tender_dependents():
    assert not tender_fact('建设工程施工合同。双方直接协商签署。')['triggered']

def test_settlement_submission_is_partial_without_review_deadline():
    clauses=parse_contract_clauses('乙方完成作业并验收合格后，应在28日内向甲方提交完整结算资料。')
    rows=extract('settlement_procedure',clauses)
    ids={e['element_id'] for e in PROFILES['settlement_procedure'] if any(supports(e,r['text']) for r in rows)}
    assert 'settlement_submission' in ids
    assert 'settlement_review' not in ids

def test_audit_confirmation_is_not_review_deadline():
    clauses=parse_contract_clauses('每月按经甲方审核确认的已完成工程量计算当期劳务费。')
    rows=extract('settlement_procedure',clauses)
    assert not any(e['element_id']=='settlement_review' and supports(e,r['text']) for e in rows)

def test_labor_subcontract_subtype_and_roles():
    c = classify('建设工程施工劳务分包合同\n甲方（承包人）\n乙方（劳务分包人）')
    assert c['subtype'] == 'LABOR_SUBCONTRACT'
    assert c['party_roles']['甲方'] == 'UPSTREAM_CONTRACTOR_OR_LABOR_CLIENT'
    assert subtype_applicability('建设工程施工劳务分包合同', 'construction_license_and_approval')[0] is False

def test_downstream_consent_does_not_activate_current_professional_subcontract_review():
    assert subtype_applicability('建设工程施工劳务分包合同', 'subcontract_to_qualified_party')[0] is False
    assert subtype_applicability('建设工程专业分包合同', 'subcontract_to_qualified_party') is None

