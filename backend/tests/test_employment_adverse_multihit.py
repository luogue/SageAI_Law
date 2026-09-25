from tests.test_employment_fact_semantics import review, item


def test_insurance_payment_does_not_hide_cash_substitution():
    text = '甲方依法为乙方办理社会保险。经劳动者申请，双方同意支付社保补贴，由劳动者自行办理保险。'
    row = item(review(text), 'EMP-13-01')
    assert row['coverage_status'] == '风险条款'
    assert any('补贴' in e.get('text', '') for e in row['evidence_clauses'])


def test_supplementary_welfare_is_not_substitution():
    assert item(review('甲方依法缴纳社会保险，并额外给予员工生活补贴。'), 'EMP-13-01')['coverage_status'] == '通过'


def test_all_ordinary_penalties_are_retained():
    source = '乙方违反保密义务应支付违约金8000元。\n乙方未提前通知而离职的，须向甲方支付两个月工资的违约金。'
    row = item(review(source), 'EMP-14-01')
    assert row['coverage_status'] == '风险条款'
    quotes = [e.get('text', '') for e in row['evidence_clauses']]
    assert any('保密义务' in q for q in quotes)
    assert any('离职' in q for q in quotes)


def test_noncompete_penalty_is_not_ordinary_exit_penalty():
    source = '劳动者离职后违反竞业限制义务的，应支付违约金。'
    assert item(review(source), 'EMP-14-01')['coverage_status'] == '通过'
