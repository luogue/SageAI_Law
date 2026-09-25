from pathlib import Path
import pytest
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
    for key in ('CA-01-04', 'CA-02-02', 'CA-10-02'):
        assert rows[key]['coverage_status'] == '不适用'
    assert rows['CA-05-03']['coverage_status'] == '部分覆盖'
    assert rows['CA-10-04']['coverage_status'] == '缺失'
    assert rows['CA-05-04']['coverage_status'] == '缺失'
    assert rows['CA-08-04']['coverage_status'] == '部分覆盖'
    assert '第十二条' in rows['CA-08-04']['evidence_location']
    assert '第八条' not in rows['CA-08-04']['evidence_location']
    assert rows['CA-02-03']['coverage_status'] == '缺失'
    assert rows['CA-02-03']['risk_level'] == '低'
    assert rows['CA-02-03']['action_priority'] == 'C_OPTIMIZATION'
    assert rows['CA-08-01']['coverage_status'] == '部分覆盖'
    assert '第十条' in rows['CA-08-01']['evidence_location']
    assert rows['CA-08-02']['coverage_status'] == '通过'
    states = {e['element_id']: e['status'] for e in rows['CA-08-01']['coverage_elements']}
    assert states['third_party_default_notice'] == 'COVERED'
    assert states['third_party_default_mitigation'] == 'COVERED'
    assert states['third_party_default_compensation'] == 'MISSING'
    for key in ('CA-02-01', 'CA-09-03', 'CA-11-01'):
        assert rows[key]['coverage_status'] == '缺失'
    assert rows['CA-10-01']['coverage_status'] == '部分覆盖'
    assert '擅自处分' in rows['CA-10-01']['legal_consequence_if_missing']
    assert '验收节点' not in rows['CA-10-01']['legal_consequence_if_missing']
    assert '第二条' in rows['CA-10-01']['evidence_location']


def test_conditional_goods_and_written_contract():
    from review_v2.commission_agency_evidence import prerequisite
    assert not prerequisite('第一条 本合同委托销售工业设备。双方盖章。', 'oral_contract_evidence')[0]
    assert prerequisite('双方仅口头委托销售货物。', 'oral_contract_evidence')[0]
    assert not prerequisite('委托销售普通机床。', 'special_goods_license')[0]
    assert prerequisite('委托销售药品。', 'special_goods_license')[0]
    assert not prerequisite('委托销售工业设备。', 'perishable_goods_emergency_disposal')[0]
    assert prerequisite('委托物容易腐烂。', 'perishable_goods_emergency_disposal')[0]


def test_defect_liability_is_not_disclosure_and_report_is_not_instruction():
    _, rows = review('行纪合同\n第一条 委托人提供的货物存在质量缺陷造成损失，由委托人承担责任。\n'
                     '第二条 行纪人应在收到委托人要求后3个工作日内报告事务处理情况。')
    assert rows['CA-05-03']['coverage_status'] == '部分覆盖'
    assert rows['CA-10-04']['coverage_status'] == '缺失'
    assert rows['CA-05-04']['coverage_status'] == '缺失'


def test_explicit_information_and_disclosure():
    _, rows = review('行纪合同\n第一条 委托人应提供货物检验报告及权属证明。委托人应主动告知货物质量缺陷和权利限制。'
                     '委托人提供的货物存在质量缺陷造成损失，由委托人承担责任。')
    assert rows['CA-05-03']['coverage_status'] == '通过'
    assert rows['CA-10-04']['coverage_status'] == '通过'


def test_business_separation_is_not_own_name_trade():
    _, rows = review('行纪合同\n第一条 行纪人以自己的名义与第三方交易。\n第二条 行纪人应将委托物和交易资料与自营业务分别管理，将行纪价款与自营业务分别记账。')
    assert rows['CA-01-02']['coverage_status'] == '通过'
    assert rows['CA-02-03']['coverage_status'] == '通过'
    assert '第二条' in rows['CA-02-03']['evidence_location']


def test_explicit_default_compensation_is_required_for_full_coverage():
    _, rows = review('行纪合同\n第一条 第三人不履行义务时行纪人应及时通知委托人并采取催收、保全措施。第三人不履行义务致委托人受损时，行纪人应向委托人承担赔偿责任。')
    assert rows['CA-08-01']['coverage_status'] == '通过'


def test_related_topics_do_not_prove_special_rights():
    _, rows = review('行纪合同\n第一条 一方被吊销营业执照时另一方有权解除合同。合同解除后返还剩余货物。'
                     '行纪人可以对外销售及处分货物。严重违约时守约方可以通知解除。')
    for key in ('CA-02-01', 'CA-09-03', 'CA-10-01', 'CA-11-01'):
        assert rows[key]['coverage_status'] == '缺失'


def test_direct_special_rights_are_recalled():
    _, rows = review('行纪合同\n第一条 行纪人保证具备本交易所需经营资格。\n'
                     '第二条 委托人拒绝取回货物时，行纪人有权依法提存。\n'
                     '第三条 委托物有瑕疵时行纪人应通知委托人。瑕疵物经委托人同意可处分。瑕疵物处分所得转交委托人。\n'
                     '第四条 任何一方可以随时解除合同。')
    for key in ('CA-02-01', 'CA-09-03', 'CA-10-01', 'CA-11-01'):
        assert rows[key]['coverage_status'] == '通过'


@pytest.mark.parametrize('key, clause', [
    ('CA-02-01', '一方被吊销营业执照时可解除合同。'),
    ('CA-09-03', '合同解除后返还剩余货物并清算费用。'),
    ('CA-10-01', '行纪人可以按指定价格销售并处分货物。'),
    ('CA-11-01', '一方严重违约时守约方有权解除合同。'),
])
def test_four_false_positive_mappings_individually(key, clause):
    _, rows = review('行纪合同\n第一条 ' + clause)
    assert rows[key]['coverage_status'] == '缺失'
    assert not any(e.get('source_type') == 'SOURCE_CLAUSE' for e in rows[key]['evidence_clauses'])


def test_file_entrypoint_actual_evaluator(monkeypatch):
    import hashlib
    import json
    import review_v2.commission_agency_evidence as evaluator
    from fastapi.testclient import TestClient
    from main import app
    from auth.routes import get_current_user
    calls = []
    original = evaluator.apply
    def traced(items, clauses):
        result = original(items, clauses)
        calls.append(True)
        return result
    monkeypatch.setattr(evaluator, 'apply', traced)
    path = next((Path(__file__).resolve().parents[2] / 'test_data').glob('58 *.docx'))
    previous = app.dependency_overrides.get(get_current_user)
    app.dependency_overrides[get_current_user] = lambda: 1
    try:
        with TestClient(app) as client:
            response = client.post('/review-v2/file', files={'file': (path.name, path.read_bytes(),
                'application/vnd.openxmlformats-officedocument.wordprocessingml.document')},
                data={'contract_type': 'commission_agency', 'use_llm': 'true'})
        assert response.status_code == 200, response.text[:500]
        report = response.json()
        assert calls, 'Production file route did not execute the modified evaluator'
        print('EXECUTED', evaluator.__file__, hashlib.sha256(Path(evaluator.__file__).read_bytes()).hexdigest())
        expected = {'CA-02-01': '缺失', 'CA-09-03': '缺失', 'CA-10-01': '部分覆盖', 'CA-11-01': '缺失'}
        for row in report['items']:
            if row['item_id'] in expected:
                print(json.dumps({k: row.get(k) for k in ('item_id', 'coverage_status', 'coverage_elements', 'evidence_location', 'evidence_clauses')}, ensure_ascii=False))
                assert row['coverage_status'] == expected[row['item_id']]
        assert report['release_quality_gate']['status'] == 'REPORT_READY', report['release_quality_gate']['failures']
    finally:
        if previous is None:
            app.dependency_overrides.pop(get_current_user, None)
        else:
            app.dependency_overrides[get_current_user] = previous
