import pytest
from types import SimpleNamespace
from review_v2.lease_semantics import consistency_failures
from review_v2.engine import review_contract_v2
from review_v2.penalty_base import analyze

def review(text):
    return review_contract_v2(text,'transportation',use_llm=False)

def test_partial_identity_period_and_waybill_not_precedence():
    result=review('委托方：测试贸易有限公司（甲方）。承运方：测试运输有限公司（乙方）。甲方提供托运单。乙方在运输过程中对货损承担责任。')
    rows={r['item_id']:r for r in result['items']}
    for key in ['T-01-02','T-01-04','T-05-04']:
        assert rows[key]['coverage_status']=='部分覆盖'
        assert any(e['status']=='COVERED' and e['evidence_ids'] for e in rows[key]['coverage_elements'])
    for key in ['T-07-03','T-07-04','T-10-01','T-10-02','T-10-03']:
        assert rows[key]['coverage_status']=='不适用'
    assert result['release_quality_gate']['status']=='REPORT_READY'

def test_explicit_precedence_pass():
    rows={r['item_id']:r for r in review('货物运输合同。双方填写托运单。托运单与合同不一致时，以合同正文为准。')['items']}
    assert rows['T-01-04']['coverage_status']=='通过'
    assert any('不一致' in e.get('quote',e.get('text','')) for e in rows['T-01-04']['evidence_clauses'])

@pytest.mark.parametrize('text,ids',[
 ('本合同为公铁联运，分段运输。',['T-10-01','T-10-02','T-10-03']),
 ('未保价货物最高赔偿不超过运费两倍。',['T-07-03']),
 ('本次运输危险品。',['T-03-02']),
])
def test_positive_prerequisite_activates(text,ids):
    rows={r['item_id']:r for r in review(text)['items']}
    assert all(rows[key]['coverage_status']!='不适用' for key in ids)

def test_declared_cargo_value_not_liability_cap():
    rows={r['item_id']:r for r in review('货物申报价值为800000元，本次公路运输。')['items']}
    assert rows['T-07-03']['coverage_status']=='不适用'

def test_cargo_identity_and_value_quotes_are_independent():
    result=review('主要运输货物包括机械零件和普通日用品。货物申报价值为人民币320000元。乙方在运输过程中对货物损失承担责任。')
    row=next(r for r in result['items'] if r['item_id']=='T-02-02')
    assert row['coverage_status']=='通过'
    assert all('损失承担' not in e.get('quote','') for e in row['evidence_clauses'])
    assert any('320000' in e.get('quote','') for e in row['evidence_clauses'])
    assert any('机械零件' in e.get('quote','') for e in row['evidence_clauses'])
    # A valid internal text must not rescue a false displayed quotation.
    row['evidence_clauses'][0]['quote']='运输过程中货物损失由乙方承担。'
    failures=consistency_failures([SimpleNamespace(**row)])
    assert any(f['requirement']=='DISPLAY_QUOTE_ELEMENT_CONFLICT' for f in failures)

def test_insurance_and_vehicle_safety_partial_facts():
    rows={r['item_id']:r for r in review('乙方提供的车辆技术性能良好，证照齐全、合法、有效，并购买交强险及物流责任险。乙方应提供保险卡。')['items']}
    assert rows['T-04-01']['coverage_status']=='部分覆盖'
    assert rows['T-12-03']['coverage_status']=='通过'
    assert rows['T-06-03']['coverage_status']=='法律提示'
    assert not rows['T-06-03']['related_risks']

def test_insurance_document_missing_is_partial_and_declared_value_conditional():
    rows={r['item_id']:r for r in review('乙方已购买货运险。本次办理保价。')['items']}
    assert rows['T-12-03']['coverage_status']=='部分覆盖'
    assert any(e['element_id']=='transport_declared_value_proof' and e['status']=='MISSING' for e in rows['T-12-03']['coverage_elements'])

def test_cargo_loss_liability_cannot_prove_nature_or_value():
    row=next(r for r in review('乙方在运输过程中对货物损失承担责任。')['items'] if r['item_id']=='T-02-02')
    assert row['coverage_status']=='缺失'

@pytest.mark.parametrize('clause',[
 '不可抗力仅限于战争及重大地震，不能履行时合同自动终止。',
 '不可抗力包括资金不足，发生后无须通知对方。',
])
def test_force_majeure_presence_does_not_override_adverse_terms(clause):
    result=review(clause)
    row=next(r for r in result['items'] if r['item_id']=='T-06-01')
    assert row['coverage_status']=='风险条款'
    assert result['release_quality_gate']['status']=='REPORT_READY'
    assert all(e['status']=='ADVERSE' for e in row['coverage_elements'])

def test_force_majeure_substantive_protections_pass():
    clause='不可抗力是不能预见、不能避免且不能克服的客观情况。不可抗力影响履行时，按实际影响部分或全部免除责任。不可抗力发生后应及时通知并提供证明。受影响方应采取措施防止损失扩大。'
    row=next(r for r in review(clause)['items'] if r['item_id']=='T-06-01')
    assert row['coverage_status']=='通过'

def test_handover_equivalent_documents_and_partial_fields():
    row=next(r for r in review('实际货物名称、数量和价值以对应托运单及出库单为准。')['items'] if r['item_id']=='T-12-02')
    assert row['coverage_status']=='部分覆盖'
    covered={e['element_id'] for e in row['coverage_elements'] if e['status']=='COVERED'}
    assert covered=={'transport_handover_names','transport_handover_quantity'}

def test_handover_document_title_alone_not_pass():
    row=next(r for r in review('附件：货物交接清单。')['items'] if r['item_id']=='T-12-02')
    assert row['coverage_status']=='缺失'

def test_transport_instructions_not_delivery_procedure():
    row=next(r for r in review('托运单记载装柜地点、卸货地点及联系人。')['items'] if r['item_id']=='T-08-01')
    assert row['coverage_status']=='缺失'

def test_delivery_procedure_partial_and_complete():
    text='承运人应将货物交付收货人。到货后通知收货人。'
    row=next(r for r in review(text)['items'] if r['item_id']=='T-08-01')
    assert row['coverage_status']=='部分覆盖'
    text+='交付前核验收货人身份及收货授权。收货人签署交接单。签收后视为交付完成。'
    row=next(r for r in review(text)['items'] if r['item_id']=='T-08-01')
    assert row['coverage_status']=='通过'

def test_adverse_clause_cannot_have_missing_clause_consequence():
    result=review('不可抗力仅指战争，无法履行时合同自动终止。')
    row=next(r for r in result['items'] if r['item_id']=='T-06-01')
    assert '未列明' not in row['legal_consequence_if_missing']
    row['legal_consequence_if_missing']='未列明不可抗力免责规则。'
    failures=consistency_failures([SimpleNamespace(**row)])
    assert any(f['requirement']=='EXISTING_ADVERSE_CLAUSE_ABSENCE_NARRATIVE' for f in failures)

def test_tariff_cross_clause_reference_requires_populated_schedule():
    ref='运输费用以双方签章确认的报价单为准。\n'
    tariff='甲地至乙地，20尺货柜运输费人民币1800元/柜；\n甲地至乙地，40尺货柜运输费人民币2300元/柜。\n'
    penalty='每迟延6小时按该柜的运输费用10%支付违约金。'
    assert analyze(ref+tariff+penalty)[0]['status']=='DETERMINABLE'
    assert analyze(ref+penalty)[0]['status']=='UNDEFINED'
    assert analyze(ref+tariff+'甲地至乙地，20尺货柜运输费人民币1900元/柜。\n'+penalty)[0]['status']=='UNDEFINED'
