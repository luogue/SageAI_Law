from tests.test_employment_fact_semantics import review, item


def test_only_noncompete_compensation_cannot_prove_settlement():
    result = review('第十条 竞业限制\n离职后两年内履行竞业限制。经济补偿标准及支付方式由双方离职时另行协商确定。违反竞业义务支付违约金90000元。')
    row = item(result, 'EMP-11-01')
    assert row['coverage_status'] == '缺失'
    assert not row['evidence_clauses']
    assert result['release_quality_gate']['status'] == 'REPORT_READY'


def test_statutory_settlement_has_original_proof():
    result = review('第六条 解除结算\n解除劳动合同时，甲方依法支付经济补偿。')
    row = item(result, 'EMP-11-01')
    assert row['coverage_status'] == '部分覆盖'
    assert row['coverage_elements'][0]['status'] == 'COVERED'
    assert row['evidence_clauses']
    assert all(e.get('verified_original') for e in row['evidence_clauses'])
