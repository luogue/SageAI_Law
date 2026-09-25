import pytest
from backend.tests.test_termination_verified_pipeline import run, IDENTITY

@pytest.mark.parametrize('duration', [None, '离职后三年', '至相关信息依法公开', '永久'])
def test_survival_is_not_duration(monkeypatch,duration):
 vals=IDENTITY+[
 ('exit_settlement.secret_scope','研发资料','对研发资料承担保密义务。'),
 ('exit_settlement.secret_continues',True,'此前的保密协议离职后继续有效。'),
 ('exit_settlement.secret_reference','此前保密协议','此前的保密协议离职后继续有效。')]
 if duration:vals.append(('exit_settlement.secret_duration',duration,'保密义务期限为'+duration+'。'))
 rows,r=run(monkeypatch,vals)
 row=rows['ET-08-01']
 assert row['coverage_status']==('通过' if duration else '部分覆盖')
 el={e['element_id']:e['status'] for e in row['coverage_elements']}
 assert el['termination_secrecy_2']=='COVERED'
 assert el['termination_secrecy_3']==('COVERED' if duration else 'MISSING')
 if duration:
  assert any('保密义务期限为' in e['quote'] for e in row['evidence_clauses'])

@pytest.mark.parametrize('condition,quote',[
 (True,'乙方交接并归还物品后，单位方予办理终止证明。'),
 (False,'未办理交接不得影响单位出具离职证明。'),
 (None,'单位在终止当日出具证明。劳动者另按约定完成交接。'),
])
def test_certificate_formal_coverage_and_condition_independent(monkeypatch,condition,quote):
 vals=IDENTITY+[
 ('exit_settlement.certificate',quote,quote),
 ('exit_settlement.social_transfer','办理社会保险转移','单位办理社会保险转移。'),
 ('exit_settlement.personnel_transfer','办理档案转移','单位办理档案转移。'),
 ('termination.handover','七日内移交工作资料','七日内移交工作资料。')]
 if condition is not None: vals.append(('exit_settlement.certificate_requires_handover',condition,quote))
 rows,r=run(monkeypatch,vals)
 assert rows['ET-01-01']['coverage_status']=='通过'
 assert rows['ET-09-01']['coverage_status']==('风险条款' if condition is True else '通过')
 if condition is True:
  assert 'ET-09-01' in rows['ET-01-01']['action_suggestion']
  assert any(e['quote']==quote for e in rows['ET-09-01']['evidence_clauses'])

def test_verifier_must_attest_actual_duration_not_just_survival():
 from review_v2.fact_semantic_contracts import validate_checks
 from review_v2.fact_validation import FactExtractionError
 candidate={'fact_id':'test-duration','concept':'exit_settlement.secret_duration',
    'evidence':[{'quote':'旧协议继续有效。'}]}
 with pytest.raises(FactExtractionError):
  validate_checks([candidate],{'checks':[{'fact_id':'test-duration','supported':True}]})
