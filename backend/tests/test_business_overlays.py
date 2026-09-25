from types import SimpleNamespace
from review_v2.engine import review_contract_v2
from review_v2.business_overlays import active
from review_v2.settlement_formula import analyze
from review_v2.lease_semantics import consistency_failures

OP='甲方将营业部交由乙方承包经营。甲方授权乙方经营。经营费用由乙方承担。乙方向甲方上交管理费。'

def test_dangerous_overlay_keeps_primary_and_external_unknown():
    result=review_contract_v2('运输合同\n'+OP+'乙方经营危险品运输业务，车辆必须有证。','transportation',use_llm=False)
    assert result['contract_type']=='operating_cooperation'
    rows={r['item_id']:r for r in result['items']}
    assert not any(k.startswith('T-') for k in rows)
    assert all(rows[f'REG-0{i}-01']['coverage_status'] in {'待核验','INSUFFICIENT_CONTEXT'} for i in range(1,6))
    assert result['release_quality_gate']['status']=='REPORT_READY'
    row=rows['REG-02-01']; row['coverage_status']='通过'
    assert any(f['requirement']=='UNVERIFIED_EXTERNAL_FACT_PASSED' for f in consistency_failures([SimpleNamespace(**row)]))

def test_ordinary_logistics_no_dangerous_overlay():
    assert active('经营合作\n'+OP+'普通物流运输。')==[]

def test_food_franchise_overlay():
    assert active('加盟合同\n经营餐饮食品加盟业务。')==['FOOD_OPERATION']

def test_unique_shortfall_expression():
    row=analyze('年度基数1000万元，未完成部分按8%补足。')[0]
    assert row['status']=='RESOLVED'
    assert row['base']==10000000 and row['rate']==0.08
    assert row['formula']=='max(0, 1e+07 - actual_period_turnover) * 0.08'

def test_vague_loss_not_unique_formula():
    assert analyze('未完成应补足相应损失。') == []  # ordinary loss is not business-performance shortfall
    assert analyze('业务基数800万元，未完成上交部分补足。')[0]['status']=='AMBIGUOUS'

def test_contractual_penalty_direct_authority_and_protection():
    result=review_contract_v2(OP+'乙方按运输费用10倍赔偿。乙方按预接洽业务总额5%支付罚款。','transportation',use_llm=False)
    rows={r['item_id']:r for r in result['items']}
    for key in ['OP-06-01','OP-07-01']:
        assert rows[key]['coverage_status']=='风险条款'
        assert '585' in str(rows[key]['legal_basis_index'])
    assert result['release_quality_gate']['status']=='REPORT_READY'

def test_penalty_forms_do_not_share_automatic_severity():
    from review_v2.settlement_formula import penalty_expressions
    expressions=penalty_expressions('运输费用10倍赔偿。违约金为30000元。按合同额5%支付违约金。')
    assert [r['kind'] for r in expressions]==['MULTIPLE','FIXED','PERCENTAGE']
    assert expressions[0]['assessment']=='HIGH_MULTIPLE_REQUIRES_LOSS_REVIEW'
    assert all(r['assessment']=='LOSS_CONTEXT_REQUIRED' for r in expressions[1:])
    assert all('585' in r['legal_basis'] for r in expressions)
