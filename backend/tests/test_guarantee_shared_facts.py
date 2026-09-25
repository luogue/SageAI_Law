from pathlib import Path
import pytest

from review_v2.engine import review_contract_v2
from review_v2.clause_parser import parse_contract_clauses
from review_v2.guarantee_party_facts import extract_guarantee_parties, signature_mismatches
from review_v2.guarantee_contract_facts import extract
from review_v2.guarantee_prerequisites import prerequisite, JOINT_NODES


@pytest.mark.parametrize('body,kind,count,company,joint', [
    ('乙方（保证人）：赵明\n身份证号码：123\n', 'NATURAL_PERSON', 1, False, False),
    ('乙方（保证人）：远航有限公司\n统一社会信用代码：123\n', 'COMPANY', 1, True, False),
    ('保证人一：赵明\n身份证号码：123\n保证人二：孙华\n身份证号码：456\n', 'NATURAL_PERSON', 2, False, True),
])
def test_shared_party_gates(body,kind,count,company,joint):
    text='甲方（债权人）：信达有限公司\n'+body
    f=extract_guarantee_parties(text)
    assert (f['guarantee_party_type'], f['guarantor_count'])==(kind,count)
    for node in ('company_guarantor_authority','company_guarantee_resolution'):
        assert prerequisite(text,node)[0] is company
    for node in JOINT_NODES:
        assert prerequisite(text,node)[0] is joint


@pytest.mark.parametrize('extra', [
    '法律规定多个保证人可以共同保证。',
    '如果有共同保证人，应明确份额。',
    '原合同为共同保证。本合同仅一名保证人。',
    '保证人指上述主体及其权利义务承继人和受让人。',
])
def test_template_mentions_not_multiple_guarantors(extra):
    facts=extract_guarantee_parties('乙方（保证人）：赵明\n身份证号码：123\n'+extra)
    assert facts['guarantor_count']==1
    assert not facts['joint_guarantee']


@pytest.mark.parametrize('identity,signature,mismatch', [
    ('赵明\n身份证号码：123', '赵明（公章）\n法定代表人：赵明（签字）', True),
    ('赵明\n身份证号码：123', '赵明（签字）', False),
    ('远航有限公司\n统一社会信用代码：123', '远航有限公司（签字）', True),
    ('远航有限公司\n统一社会信用代码：123', '远航有限公司（公章）\n法定代表人：赵明（签字）', False),
])
def test_signing_identity_both_directions(identity,signature,mismatch):
    text='乙方（保证人）：'+identity+'\n第一条 保证事项\n乙方：'+signature
    assert bool(signature_mismatches(text,extract_guarantee_parties(text))) is mismatch


@pytest.mark.parametrize('body,expected', [
    ('借款本金为120000元。', '通过'),
    ('本合同为最高额保证。借款本金为120000元。', '缺失'),
    ('本合同为最高额保证。最高债权额为300000元。', '通过'),
])
def test_fixed_principal_is_not_maximum_cap(body,expected):
    report=review_contract_v2('保证合同\n乙方（保证人）：赵明\n身份证号码：123\n第一条 保证债权\n'+body,'guarantee',use_llm=False)
    item=next(i for i in report['items'] if i['item_id']=='GUA-07-02')
    assert item['coverage_status']==expected
    if expected=='通过':
        assert item['evidence_clauses']


def test_fixed_principal_ignores_other_small_print_amounts():
    text='费用小写：500元。借款本金为人民币120万元。'
    assert extract(text,parse_contract_clauses(text))['fixed_principal_amount']==1200000


def test_complete_change_clauses_with_bound_evidence():
    text=('保证合同\n乙方（保证人）：赵明\n身份证号码：123\n第九条 主合同变更\n'
          '主合同借款金额变更未经保证人同意，如果减轻债务，保证人仍对变更后的债务承担保证责任；'
          '如果加重债务，保证人对加重部分不承担保证责任。'
          '履行期限变更未经保证人书面同意，保证期间仍按原合同约定。')
    report=review_contract_v2(text,'guarantee',use_llm=False)
    for item in report['items']:
        if item['item_id'] in {'GUA-08-01','GUA-08-02','GUA-08-03'}:
            assert item['coverage_status']=='通过'
            assert all(e['quote'] in text and e['document_type']=='MAIN_CONTRACT' for e in item['evidence_clauses'])


@pytest.mark.parametrize('body,expected', [
    ('主合同变更须取得保证人书面同意。展期应由保证人书面确认。', '通过'),
    ('主合同变更无需保证人书面同意。展期无需保证人书面确认。', '缺失'),
])
def test_change_consent_positive_and_negative(body,expected):
    report=review_contract_v2('保证合同\n第一条 主合同变更\n'+body,'guarantee',use_llm=False)
    for item in report['items']:
        if item['item_id'] in {'GUA-08-01','GUA-08-03'}:
            assert item['coverage_status']==expected


def test_current_unchanged_docx_full_regression():
    from layers.input_layer import InputLayer
    path=next((Path(__file__).resolve().parents[2]/'test_data').glob('69 *.docx'))
    from fastapi import UploadFile
    with path.open('rb') as source:
        text=InputLayer().extract_text_from_file(UploadFile(filename=path.name,file=source))
    report=review_contract_v2(text,'guarantee',use_llm=False)
    rows={i['item_id']:i for i in report['items']}
    assert len(rows)==49
    facts=rows['GUA-07-02']['decision_trace']['guarantee_shared_facts']
    assert (facts['guarantee_party_type'],facts['guarantor_count'],facts['fixed_principal_amount'])==('NATURAL_PERSON',1,6000000)
    inactive={'GUA-01-04','GUA-12-01',*[f'GUA-10-0{i}' for i in range(1,5)]}
    assert all(rows[k]['coverage_status']=='不适用' for k in inactive)
    assert all(rows[k]['coverage_status']=='通过' for k in ('GUA-07-02','GUA-08-01','GUA-08-02','GUA-08-03'))
    assert not rows['GUA-01-01']['needs_manual_review']
    assert rows['GUA-01-01']['coverage_status']=='风险条款'
    assert any('公章' in e.get('quote','') for e in rows['GUA-01-01']['evidence_clauses'])
    assert all('仲裁' not in e.get('quote','') for e in rows['GUA-08-04']['evidence_clauses'])
    for risk in report['risk_findings']:
        assert not inactive.intersection(risk.get('source_review_ids', []))
    for item in rows.values():
        for evidence in item['evidence_clauses']:
            if evidence.get('source_type')=='SOURCE_CLAUSE' and evidence.get('section_type')=='正式合同条款':
                assert evidence['document_type']=='MAIN_CONTRACT'
    assert report['release_quality_gate']['status']=='REPORT_READY',report['release_quality_gate']
