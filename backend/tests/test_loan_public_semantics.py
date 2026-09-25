from review_v2.clause_parser import parse_contract_clauses
from review_v2.loan_facts import LoanFacts, extract, financing_charge, negative_scan
from review_v2.penalty_base import analyze


def test_party_types_are_shared_and_gate_special_rules():
    facts = LoanFacts.from_clauses(parse_contract_clauses(
        '贷款人：张三。借款人：李四。张三身份证号：110101199001010011；李四居民身份证：110101199002020022。'))
    assert facts.values['party_type'] == 'natural_person'
    assert facts.applicability('loan_enterprise_business_need')['applicable'] is False
    assert facts.applicability('loan_financial_interest_compliance')['applicable'] is False
    assert facts.applicability('loan_interest_lpr_cap')['applicable'] is True


def test_cross_clause_evidence_uses_clause_context():
    clauses = parse_contract_clauses(
        '第五条 提前还款\n已归还本金自到账日起不再计息。\n'
        '第七条 结清\n结清截至实际还款日已产生利息，提前五个工作日通知贷款人。')
    assert extract('loan_early_repayment_interest', clauses)
    assert extract('loan_early_repayment_notice', clauses)


def test_negative_polarity_does_not_create_financing_fee_risk():
    assert financing_charge('本合同不收取手续费、管理费或其他融资费用。') is False


def test_dynamic_formula_is_determinable():
    rows = analyze('逾期未付利息的5%违约金；未偿还本金、年利率10.8%及实际计息期间确定未付利息。')
    assert rows and rows[-1]['status'] == 'DETERMINABLE'
