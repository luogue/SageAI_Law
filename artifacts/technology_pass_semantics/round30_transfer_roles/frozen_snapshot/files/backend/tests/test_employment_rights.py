"""Legal-effect boundaries, actor scope, and production risk evidence."""
import pytest
from pathlib import Path
from test_employment_fact_semantics import review, item
from review_v2.employment_rights import rights_evidence
from review_v2.clause_parser import parse_contract_clauses


@pytest.mark.parametrize('text', [
    '乙方应配合提交参保所需资料。',
    '乙方未提交参保资料造成的直接损失，仅按自身过错承担，甲方仍依法履行缴费义务。',
    '不得约定社会保险责任全部由劳动者承担。',
    '因乙方原因造成社会保险无法及时缴纳的责任由乙方承担，但甲方仍依法承担缴纳义务。',
])
def test_cooperation_and_limited_fault_not_blanket_transfer(text):
    assert item(review(text), 'EMP-13-01')['coverage_status'] == '通过'


@pytest.mark.parametrize('text,effect', [
    ('社会保险无法缴纳的全部责任由劳动者自行承担。', 'BLANKET_EMPLOYER_LIABILITY_TRANSFER'),
    ('乙方未提供社会保险资料时，甲方当然免责。', 'AUTOMATIC_EMPLOYER_EXEMPTION'),
    ('乙方不得因甲方未缴社保解除劳动合同或要求补偿。', 'STATUTORY_REMEDY_EXCLUSION'),
    ('第五条 甲方有下列情形之一的，乙方可以解除劳动合同：\n（一）未依法缴纳社会保险费的（乙方未提供材料的情形除外）。', 'STATUTORY_REMEDY_EXCLUSION'),
])
def test_exemption_or_remedy_exclusion_requires_effect(text, effect):
    result = review(text)
    row = item(result, 'EMP-13-01')
    assert row['coverage_status'] == '风险条款'
    assert effect in row['decision_trace']['priority_adverse_verification']['legal_effects']
    assert row['related_risks']
    assert result['release_quality_gate']['status'] == 'REPORT_READY'


@pytest.mark.parametrize('text', [
    '执行本单位任务或者主要利用本单位物质技术条件完成的发明依法认定为职务发明。',
    '在职期间仅限执行甲方任务取得的成果均属职务成果。',
    '在职期间取得的成果全部归甲方，非职务成果除外。',
    '非职务发明通过另行签订转让协议自愿转让归甲方。',
    '所有职务作品的著作财产权按合同约定归甲方，作者保留署名权。',
    '作者不得转让署名权。',
    '在职期间取得的成果并非均属职务成果。',
    '论文标注甲方为作者单位，不影响个人署名。',
    '本合同期内取得的成果不得全部归甲方。',
])
def test_lawful_ip_scope_and_personal_rights_not_adverse(text):
    row = item(review(text), 'EMP-IP-01')
    assert row['coverage_status'] == '通过'
    assert not row['related_risks']


@pytest.mark.parametrize('text,effect', [
    ('劳动者在任职期间取得的所有成果全部归用人单位。', 'TIME_ONLY_BLANKET_SERVICE_RESULTS'),
    ('乙方在合同期内所取得的研究成果一律认定为职务成果。', 'TIME_ONLY_BLANKET_SERVICE_RESULTS'),
    ('在职期间取得的成果，不论是否执行单位工作任务，皆归甲方。', 'TIME_ONLY_BLANKET_SERVICE_RESULTS'),
    ('乙方在任职期间的所有成果包括但不限于论文，都是职务成果。', 'TIME_ONLY_BLANKET_SERVICE_RESULTS'),
    ('非职务发明也归甲方所有。', 'NONSERVICE_RESULTS_APPROPRIATION'),
    ('乙方放弃作品署名权。', 'AUTHORSHIP_RIGHT_DEPRIVATION'),
    ('署名权全部归甲方。', 'AUTHORSHIP_RIGHT_DEPRIVATION'),
    ('乙方所有作品全部归甲方所有。', 'UNDIFFERENTIATED_COPYRIGHT_ALLOCATION'),
    ('专利、论文、科研经费及奖励全部归甲方。', 'MIXED_LEGAL_ASSETS_BLANKET_ALLOCATION'),
])
def test_blanket_ip_allocation_has_bound_adverse_fact(text, effect):
    result = review(text)
    row = item(result, 'EMP-IP-01')
    assert row['coverage_status'] == '风险条款'
    assert effect in row['decision_trace']['priority_adverse_verification']['legal_effects']
    assert row['related_risks']
    assert row['risk_severity'] == 'HIGH'
    assert result['release_quality_gate']['status'] == 'REPORT_READY'


def test_no_global_exemption_from_unrelated_legal_statement():
    clauses = parse_contract_clauses('第一条 依法认定职务成果。\n第二条 乙方在职期间的所有成果全部归甲方。')
    assert rights_evidence('employment_ip_ownership', clauses)


def test_current_document_four_risks_and_protective_exit_stay_stable():
    from layers.input_layer import InputLayer
    from starlette.datastructures import UploadFile
    source = Path(__file__).resolve().parents[2]/'test_data/63 劳动合同.docx'
    with source.open('rb') as f:
        text = InputLayer().extract_text_from_file(UploadFile(filename=source.name, file=f))
    result = review(text)
    assert len(result['items']) == 20
    for rule, status in [('EMP-01-01','部分覆盖'),('EMP-05-01','部分覆盖'),('EMP-08-01','缺失'),('EMP-10-01','风险条款')]:
        row = item(result,rule)
        assert row['coverage_status'] == status
        assert row['risk_severity'] == 'MEDIUM'
        assert row['action_priority'] == 'B_PRACTICAL'
    for rule in ['EMP-07-01','EMP-11-01']:
        assert item(result,rule)['coverage_status'] == '通过'
    for rule in ['EMP-13-01','EMP-IP-01']:
        assert item(result,rule)['coverage_status'] == '风险条款'
        assert item(result,rule)['related_risks']
    assert all('第二十二条' not in e['location'] for e in item(result,'EMP-10-01')['evidence_clauses'])
    assert result['release_quality_gate']['status'] == 'REPORT_READY'
