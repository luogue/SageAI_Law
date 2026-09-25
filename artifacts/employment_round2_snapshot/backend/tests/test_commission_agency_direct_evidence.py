from pathlib import Path
from docx import Document
from review_v2.engine import review_contract_v2


def review(text):
    report = review_contract_v2(text, 'commission_agency', use_llm=False)
    return report, {i['item_id']: i for i in report['items']}


def test_normal_trade_is_not_intervention_or_collusion():
    report, rows = review('行纪合同\n第十二条 行纪人有权以自己的名义与第三方进行交易，但应遵守委托人的交易条件。\n'
                          '行纪人应通知委托人并按月结算报酬。行纪人不得恶意串通损害委托人利益。')
    assert rows['CA-01-02']['coverage_status'] == '通过'
    assert rows['CA-08-03']['coverage_status'] == '通过'
    assert all(rows[f'CA-07-0{i}']['coverage_status'] == '不适用' for i in range(1, 5))


def test_intervention_prerequisite_is_specific():
    from review_v2.commission_agency_evidence import prerequisite
    assert prerequisite('行纪人可以自己作为买受人参与交易。', 'intervention_notice_disclosure')[0]
    assert not prerequisite('行纪人自行买入货物后通知委托人。', 'intervention_notice_disclosure')[0]


def test_termination_settlement_direct_evidence():
    _, rows = review('行纪合同\n第八条 合同解除后双方应在10个工作日内完成货物、货款、报酬及费用清算。尚未出售货物应返还委托人，返还运输费用由委托人承担。')
    row = rows['CA-11-04']
    assert row['coverage_status'] == '通过'
    assert '第八条' in row['evidence_location']


def test_full_current_commission_contract():
    path = next((Path(__file__).resolve().parents[2] / 'test_data').glob('58 *.docx'))
    report, rows = review('\n'.join(p.text for p in Document(path).paragraphs))
    for key in ('CA-01-02', 'CA-11-04', 'CA-08-03'):
        assert rows[key]['coverage_status'] == '通过'
    assert all(rows[f'CA-07-0{i}']['coverage_status'] == '不适用' for i in range(1, 5))
    for key in ('CA-01-02', 'CA-11-04'):
        assert rows[key]['evidence_clauses']
        assert all(e['status'] == 'COVERED' for e in rows[key]['coverage_elements'])
    assert report['release_quality_gate']['status'] == 'REPORT_READY', report['release_quality_gate']['failures']
