import pytest
from pathlib import Path
from docx import Document
from review_v2.penalty_base import analyze, NODE
from review_v2.engine import review_contract_v2


@pytest.mark.parametrize('text', [
    '协议双方应当保守商业秘密。',
    '违约方应赔偿实际损失。',
    '违约方应支付违约金人民币5000元。',
    '服务费按合同金额的10%支付。',
])
def test_no_percentage_penalty_has_no_base_gap(text):
    from review_v2.penalty_base import CHECKPOINT, augment
    from review_v2.priority_contract_review import applicability
    assert augment((), text) == ()
    for kind in ('confidentiality', 'sale'):
        assert applicability(text, CHECKPOINT, kind)[0] is False
    result = review_contract_v2('保密协议\n' + text, 'confidentiality', use_llm=False)
    assert not any(i['node_id'] == NODE for i in result['items'])


def test_percentage_penalty_condition_and_metadata():
    from review_v2.penalty_base import CHECKPOINT
    from review_v2.priority_contract_review import applicability
    assert CHECKPOINT.applicable_if != '始终适用'
    assert '金额基数' in CHECKPOINT.applicable_if
    assert applicability('按项目费用的15%支付违约金。', CHECKPOINT, 'sale')[0] is True


@pytest.mark.parametrize('text,status',[
    ('合同总价为100万元。违约方应按合同总价的20%支付违约金。','DETERMINABLE'),
    ('合同总价为100万元，已支付20万元。按尚未支付款项的10%支付违约金。','DETERMINABLE'),
    ('项目投资额为人民币100万元。按项目投资额20%支付违约金。','DETERMINABLE'),
    ('按所应投资额20%支付违约金。','UNDEFINED'),
    ('按相关费用的30%承担违约金。','UNDEFINED'),
    ('约定预算为人民币50万元。按约定预算的15%支付违约金。','DETERMINABLE'),
    ('按尚未支付款项的10%支付违约金。','DETERMINABLE'),
    ('计费额为预算额减去减免额。按计费额15%支付违约金。','UNDEFINED'),
])
def test_percentage_base_resolution(text,status):
    assert analyze(text)[0]['status']==status


@pytest.mark.parametrize('kind,title',[('confidentiality','保密协议'),('sale','买卖合同')])
def test_generic_rule_is_not_nda_only(kind,title):
    r=review_contract_v2(title+'\n第一条 按相关费用的30%承担违约金。',kind,use_llm=False)
    row=next(i for i in r['items'] if i['node_id']==NODE)
    assert row['coverage_status']=='部分覆盖'
    assert row['evidence_clauses']
    assert any(e['status']=='MISSING' for e in row['coverage_elements'])


def test_actual_nda_preserves_eight_reviews_and_adds_one_common_gap():
    p=Path(__file__).resolve().parents[2]/'test_data/71 保密协议.docx'
    r=review_contract_v2('\n'.join(x.text for x in Document(p).paragraphs),'confidentiality',use_llm=False)
    items={i['item_id']:i for i in r['items']}
    for key in ['NDA-01-01','NDA-03-01','NDA-04-01']: assert items[key]['coverage_status']=='通过'
    assert items['NDA-02-01']['coverage_status']=='部分覆盖'
    for key in ['EMP-14-01','NC-01-01','NC-02-01','NC-03-01']: assert items[key]['coverage_status']=='不适用'
    assert items['COMMON-20-01']['coverage_status']=='部分覆盖'
    assert '所应投资额' in items['COMMON-20-01']['reasoning_summary']
    definition=items['NDA-01-01']['evidence_clauses']
    assert any('第一章' in e['location'] for e in definition if '明确受保护' in str(e) or 'employment_secret_scope_1' in e.get('supports_element_ids',[]))
    assert not any('信息披露方是指' in e['text'] for e in items['NDA-03-01']['evidence_clauses'] if 'confidentiality_parties_2' in e.get('supports_element_ids',[]))
    assert r['release_quality_gate']['status']=='REPORT_READY',r['release_quality_gate']['failures']
