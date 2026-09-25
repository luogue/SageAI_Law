from copy import deepcopy
from types import SimpleNamespace
import pytest
from review_v2.clause_parser import parse_contract_clauses
from review_v2.verified_source import bind_original,verify_binding,check_pass
from review_v2.adverse_evidence import direct_evidence
from review_v2.construction_coverage import extract,PROFILES,supports
from review_v2.construction_evidence import nature_evidence


def original(text):
    clauses=parse_contract_clauses(text)
    c=clauses[0]
    return clauses,bind_original({'clause_id':c.clause_id,'text':c.text},clauses,text)


def test_verified_original_supports_pass():
    clauses,row=original('受托人应保存交接记录。')
    gate=check_pass([row],clauses,[{'element_id':'records'}],lambda req,e:'应保存交接记录' in e['quote'])
    assert gate['status']=='PASS'
    assert row['quote']==row['source_span']['raw_text']
    assert row['quote']==row['raw_text'][row['source_ref']['local_start']:row['source_ref']['local_end']]


def test_synthetic_only_cannot_pass():
    clauses=parse_contract_clauses('受托人应保存交接记录。')
    row={'clause_id':'SYN-01','evidence_id':'SYN-01','text':'受托人应保存交接记录。','verified_original':True}
    row=bind_original(row,clauses)
    assert not row['verified_original']
    assert check_pass([row],clauses,[{'element_id':'records'}],lambda *_:True)['status']=='BLOCKED'


def test_synthetic_id_cannot_borrow_a_real_clause_id():
    clauses=parse_contract_clauses('受托人应保存交接记录。')
    row=bind_original({'clause_id':clauses[0].clause_id,'evidence_id':'SYN-01',
                       'text':clauses[0].text},clauses)
    assert not row['verified_original']


@pytest.mark.parametrize('field,value',[
 ('quote','模型生成的意思相近摘要'),('source_ref',{'clause_id':'WRONG'}),
 ('source_span',{'start_offset':100,'end_offset':110,'raw_text':'错误引文'}),
 ('evidence_id','unverified-id'),('verified_original',False),
 ('location','unrelated clause'),('source_start',999),
])
def test_any_binding_tamper_fails(field,value):
    clauses,row=original('受托人应保存交接记录。');row[field]=value
    assert verify_binding(row,clauses)


def test_quote_mismatch_must_not_fall_back_to_whole_clause():
    clauses=parse_contract_clauses('双方约定保存交接记录。')
    row=bind_original({'clause_id':clauses[0].clause_id,'text':'双方已完成交接并确认无异议。'},clauses)
    assert not row['verified_original']
    assert 'QUOTE_NOT_IN_ORIGINAL' in row['source_verification']['errors']


def test_whitespace_normalization_preserves_actual_source_span():
    text='第一条\n受托人应保存交接记录。'
    clauses=parse_contract_clauses(text)
    row=bind_original({'clause_id':clauses[0].clause_id,'quote':clauses[0].text.replace('\n',' ')},clauses,text)
    assert row['verified_original']
    assert row['quote']==row['source_span']['raw_text']
    assert text[row['source_start']:row['source_end']]==row['quote']


def test_original_but_semantically_unrelated_does_not_pass():
    clauses,row=original('电子邮件发送后视为送达。')
    assert check_pass([row],clauses,[{'element_id':'records'}],lambda _,e:'交接记录' in e['quote'])['status']=='BLOCKED'


def test_parser_keeps_original_whitespace_span():
    text='第一条\n  受托人应保存交接记录。\n\n  并提供查阅。\n第二条\n费用另行约定。'
    clauses=parse_contract_clauses(text)
    row=bind_original({'clause_id':clauses[0].clause_id,'text':clauses[0].text},clauses,text)
    assert row['verified_original']
    assert text[row['source_start']:row['source_end']]==row['quote']
    assert not verify_binding(row,clauses)


def test_context_cannot_repair_unrelated_pass_proof():
    clauses,row=original('双方地址如下。')
    assert check_pass([row],clauses,[{'element_id':'payment'}],lambda *_:False)['status']=='BLOCKED'


@pytest.mark.parametrize('text',[
 '乙方不得再分包。',
 '乙方存在违法再分包行为时，甲方有权解除合同。',
 '出现下列情形，委托方有权解除合同：\n承接方存在转包、违法再分包行为；\n承接方严重延误工期；',
 '发生以下情形之一，甲方有权解除合同：\n乙方存在转包、违法再分包行为；',
])
def test_sanction_context_is_not_permission(text):
    positive,counter=direct_evidence(parse_contract_clauses(text),(r'再分包|转包',))
    assert not positive
    assert counter


@pytest.mark.parametrize('text',[
 '乙方可以再分包。',
 '乙方不得再分包，但是经甲方同意可以再分包。',
 '发生以下情形，甲方有权解除合同：\n乙方延误工期；\n乙方经甲方同意可以再分包。',
 '发生以下情形，甲方有权解除合同：乙方延误工期。\n乙方可以再分包。',
])
def test_real_permissions_and_exceptions_remain_positive(text):
    assert direct_evidence(parse_contract_clauses(text),(r'再分包',))[0]


@pytest.mark.parametrize('text',[
 '乙方施工人员必须签订劳动合同并完成实名制登记。工人工资由甲方通过工资专户代发。',
 '施工人员应依法签订劳动合同，并实行实名制。分包人应按月支付工人工资。',
])
def test_worker_management_atomic_recall(text):
    clauses=parse_contract_clauses(text)
    found=extract('labor_subcontract_qualification',clauses)
    for req in PROFILES['labor_subcontract_qualification']:
        assert any(supports(req,r['text']) for r in found),req['element_id']
    assert all(bind_original(e,clauses,text)['verified_original'] for e in found)


def test_only_real_name_is_partial_not_missing():
    rows=extract('labor_subcontract_qualification',parse_contract_clauses('施工人员必须完成实名制登记。'))
    found=[req['element_id'] for req in PROFILES['labor_subcontract_qualification'] if any(supports(req,r['text']) for r in rows)]
    assert found==['labor_real_name']


@pytest.mark.parametrize('text',[
    '乙方应提交工资支付表。', '工人工资支付管理记录。', '工资由甲方无需代发。',
])
def test_wage_records_or_topic_are_not_payment_obligations(text):
    requirement=next(r for r in PROFILES['labor_subcontract_qualification'] if r['element_id']=='labor_wage_payment')
    assert not supports(requirement,text)


@pytest.mark.parametrize('title',['建设工程施工劳务分包合同','建筑劳务分包合同','EPC总承包合同'])
def test_contract_nature_is_real_source_not_company_metadata(title):
    clauses=parse_contract_clauses(title+'\n甲方：某企业。')
    kind,rows=nature_evidence(clauses)
    assert kind and rows
    assert all(bind_original(row,clauses)['verified_original'] for row in rows)
    assert all(title in row['text'] for row in rows)


def test_production_upload_current_contract_all_passes_are_verified():
    from pathlib import Path
    from fastapi import FastAPI
    from fastapi.testclient import TestClient
    from routers import review_v2 as route
    root=Path(__file__).resolve().parents[2]
    source=next((root/'test_data').glob('97 *.docx'))
    app=FastAPI();app.include_router(route.router);app.dependency_overrides[route.get_current_user]=lambda:1
    with TestClient(app) as client:
        response=client.post('/review-v2/file',data={'contract_type':'construction','use_llm':'false'},
           files={'file':(source.name,source.read_bytes(),'application/vnd.openxmlformats-officedocument.wordprocessingml.document')})
    assert response.status_code==200
    result=response.json();rows={i['item_id']:i for i in result['items']}
    assert len([r for r in rows if r.startswith('CE-')])==52
    assert sum(result['coverage_summary'].values())==len(rows)
    for rid in ('CE-01-01','CE-05-01','CE-05-03','CE-05-04'):
        assert rows[rid]['coverage_status']=='通过'
    for row in rows.values():
        if row['coverage_status']=='通过':
            assert row['evidence_clauses']
            assert row['decision_trace']['verified_pass_source_gate']['status']=='PASS'
            assert all(e['verified_original'] and e['quote']==e['source_span']['raw_text'] for e in row['evidence_clauses'])
    assert result['release_quality_gate']['status']=='REPORT_READY'
