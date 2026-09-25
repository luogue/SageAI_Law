import pytest
from review_v2.engine import review_contract_v2
from review_v2.guarantee_prerequisites import prerequisite, JOINT_NODES


@pytest.mark.parametrize('text, joint, waiver, general', [
    ('保证人：王某。保证人承担一般保证责任。', False, False, True),
    ('保证人一：王某。保证人二：李某。两人共同保证，承担一般保证责任。', True, False, True),
    ('保证人承担一般保证责任，未放弃先诉抗辩权。', False, False, True),
    ('保证人承担一般保证责任，自愿书面放弃先诉抗辩权。', False, True, True),
    ('保证人承担连带责任保证。', False, False, False),
])
def test_production_branches(text, joint, waiver, general):
    report = review_contract_v2('保证合同\n为借款债务提供保证。' + text, 'guarantee', use_llm=False)
    rows = {r['item_id']: r for r in report['items']}
    for number in range(1, 5):
        assert (rows[f'GUA-10-0{number}']['coverage_status'] == '不适用') == (not joint)
    for number in (1, 2):
        assert rows[f'GUA-06-0{number}']['coverage_status'] == ('法律提示' if general else '不适用')
    assert (rows['GUA-06-03']['coverage_status'] == '不适用') == (not waiver)
    if waiver:
        assert rows['GUA-06-03']['coverage_status'] != '缺失'
    assert rows['GUA-06-04']['coverage_status'] == '不适用'
    assert report['guarantee_mode_consistency_gate']['status'] == 'REPORT_READY'


@pytest.mark.parametrize('text', [
    '本合同仅有一个保证人，不涉及共同保证。',
    '法律规定多个保证人可以约定份额。保证人：张某。',
    '保证人：张某。债权人甲公司与债务人乙公司签约。',
])
def test_joint_mentions_are_not_parties(text):
    assert all(prerequisite(text, node)[0] is False for node in JOINT_NODES)
