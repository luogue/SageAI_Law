import pytest
from review_v2.engine import review_contract_v2

@pytest.mark.parametrize('fee, expected', [
    ('仓库租金按月包库制，每月每平方米____元，合计月租金为________元整。', '部分覆盖'),
    ('仓库租金按月包库制，每月每平方米45元，合计月租金为36000元整。', '通过'),
    ('仓储费按每吨每天3元计算。', '通过'),
    ('仓库800平方米，仓库租金按月包库制，每月每平方米____元，合计月租金为________元整。装卸费用300元。', '部分覆盖'),
    ('仓库租金每月每平方米＿ ＿ ＿元，合计月租金为（待填写）元。另收运输费600元。', '部分覆盖'),
    ('仓库租金每月每平方米45元，合计月租金为____元。', '通过'),
])
def test_warehouse_rent_is_storage_fee(fee, expected):
    r = review_contract_v2('仓储合同\n第一条 仓库租金计算\n1. ' + fee, 'warehouse', use_llm=False)
    row = next(i for i in r['items'] if i['item_id'] == 'WH-06-01')
    assert row['coverage_status'] == expected
    assert '第1项' in row['evidence_location']
    assert any(fee in e.get('quote', '') for e in row['evidence_clauses'])
    assert r['release_quality_gate']['status'] == 'REPORT_READY', r['release_quality_gate']['failures']
    if expected == '部分覆盖':
        states = {e['element_id']:e['status'] for e in row['coverage_elements']}
        assert states['storage_fee_arrangement'] == 'COVERED'
        assert states['storage_fee_value'] == 'MISSING'


def test_no_storage_fee_clause_is_missing():
    r = review_contract_v2('仓储合同。乙方负责保管仓储物，凭仓单出库。', 'warehouse', use_llm=False)
    row = next(i for i in r['items'] if i['item_id'] == 'WH-06-01')
    assert row['coverage_status'] == '缺失'


def test_full_contract_blank_fee_variant():
    from pathlib import Path
    from docx import Document
    from collections import Counter
    path = next((Path(__file__).resolve().parents[2] / 'test_data').glob('55 *.docx'))
    text = '\n'.join(p.text for p in Document(path).paragraphs)
    # User-reported blank variant; never overwrite the filled source file.
    text = text.replace('每月每平方米45元', '每月每平方米____元').replace('合计月租金为36,000元', '合计月租金为________元')
    r = review_contract_v2(text, 'warehouse', use_llm=False)
    rows = {i['item_id']: i for i in r['items']}
    fee = rows['WH-06-01']
    assert fee['coverage_status'] == '部分覆盖'
    assert fee['evidence_location'] == '一、第1项'
    assert any('每月每平方米____元' in e.get('quote', '') for e in fee['evidence_clauses'])
    assert all(rows[key]['coverage_status'] == '缺失' for key in ('WH-07-02', 'WH-09-03', 'WH-09-04'))
    counts = Counter(i['coverage_status'] for i in r['items'])
    assert sum(counts.values()) == len(r['items']) == 40
    assert r['release_quality_gate']['status'] == 'REPORT_READY', r['release_quality_gate']['failures']
    print('BLANK_FEE_REGRESSION', dict(counts), fee['coverage_status'], fee['evidence_location'], r['release_quality_gate']['status'])
