"""Operative rights must not be inferred from another duty's event/object."""
from pathlib import Path
import re
import pytest
from review_v2.clause_parser import parse_contract_clauses
from review_v2.technology_fact_ontology import license_scope_elements
from review_v2.license_control_facts import elements
from review_v2.proposition_scope import predicate_is_operative


def scope(text, secret=False):
    clauses = parse_contract_clauses('乙方（被许可方）：乙公司\n第三条 实施范围\n' + text)
    rows = elements('secret_license_scope', clauses) if secret else license_scope_elements(clauses)
    return next(e for e in rows if e['element_id'] == 'permitted_implementation_acts')


@pytest.mark.parametrize('secret', [False, True])
@pytest.mark.parametrize('text', [
    '乙方首台使用许可专利的设备完成生产后十个工作日内支付40万元。',
    '设备生产完成后付款。',
    '乙方使用专利后支付许可费。',
    '乙方使用许可专利生产设备后应返还保证金。',
    '乙方使用许可技术制造产品后结算费用。',
    '乙方应赔偿未经许可生产设备所造成的损失。',
    '乙方应通知甲方设备使用许可专利进行生产的情况。',
    '合同终止后乙方应停止使用许可专利生产设备。',
    '乙方应对使用许可技术生产设备过程中获悉的信息保密。',
    '乙方认可设备生产完成后应付款。',
    '乙方可能使用专利生产设备。',
    '除上述许可费外，乙方无需根据设备产量、销售额或者利润另行支付专利许可提成。',
    '甲方向乙方授予上述专利的普通实施许可。',
    '因甲方无权许可或者甲方明知涉案专利实施必然侵犯第三方在先权利而未披露，导致乙方承担赔偿责任的，由甲方承担乙方因此产生的合理直接损失。',
    '如因甲方无权许可相关技术而导致乙方不能按照本合同约定正常使用许可技术，甲方应退还受影响部分对应的许可费用，并赔偿乙方因此产生的直接经济损失。',
    '许可期限届满后，乙方继续使用相关技术的，应与甲方另行协商并签订书面协议。',
    '乙方可以生产设备后十个工作日内支付40万元。',
    '双方未约定乙方可以制造设备。',
    '乙方不得制造设备是否成立，双方未明确约定。',
])
def test_other_obligation_objects_are_not_implementation_rights(text, secret):
    row = scope(text, secret)
    assert row['status'] == 'MISSING'
    assert not row['supporting_evidence']


@pytest.mark.parametrize('secret', [False, True])
@pytest.mark.parametrize('text', [
    '乙方可以制造、使用、销售相关设备。',
    '乙方可制造、使用、销售相关设备。',
    '乙方有权在中国大陆制造相关设备。',
    '甲方授权乙方生产和销售许可产品。',
    '甲方授予乙方制造、使用和销售设备的许可。',
    '乙方不得利用本许可生产与自动化装配设备无关的其他产品。',
    '乙方支付首期款后，可以制造、使用设备。',
    '许可期限五年，许可地域为中国境内，仅限生产合同产品。',
    '被许可方仅可在中华人民共和国大陆地区，将本项技术秘密用于HV-R600系列工业视觉机器人控制系统的研发、生产和销售。',
])
def test_actual_permission_and_product_restrictions_survive(text, secret):
    row = scope(text, secret)
    assert row['status'] == 'COVERED'
    assert all(s['quote'] in text for s in row['supporting_evidence'])


@pytest.mark.parametrize('secret', [False, True])
def test_separate_payment_duty_is_not_displayed_as_grant_evidence(secret):
    row = scope('乙方可以制造、使用设备，并应支付40万元。', secret)
    assert row['status'] == 'COVERED'
    assert all('支付' not in s['quote'] for s in row['supporting_evidence'])


def test_list_permission_does_not_inherit_into_payment_condition():
    row = scope('乙方可以实施下列行为：\n制造设备；\n使用上述设备；\n生产完成后支付40万元。')
    assert row['status'] == 'COVERED'
    assert all('支付' not in s['quote'] for s in row['supporting_evidence'])
    assert any('使用上述设备' in s['quote'] for s in row['supporting_evidence'])


@pytest.mark.parametrize('text, term', [
    ('设备生产完成后付款。', '生产'),
    ('侵权发生后应赔偿损失。', '侵权'),
    ('专利失效后应通知乙方。', '失效'),
    ('甲方应通知乙方专利失效情况。', '失效'),
    ('乙方应赔偿超范围实施造成的损失。', '超范围实施'),
    ('乙方应停止使用许可专利。', '使用'),
    ('乙方不得披露生产技术资料。', '生产'),
])
def test_public_predicate_scope_does_not_promote_event_or_object(text, term):
    match = re.search(term, text)
    assert not predicate_is_operative(text, *match.span())


def test_current_source_retains_all_four_acts_and_product_boundary():
    root = Path(__file__).resolve().parents[2]
    text = (root/'artifacts/technology_pass_semantics/round25_candidate_scope/input/original.txt').read_text(encoding='utf-8')
    row = scope(text)
    proof = '\n'.join(s['quote'] for s in row['supporting_evidence'])
    assert row['status'] == 'COVERED'
    for act in ('制造使用', '使用上述设备', '销售、许诺销售', '售后维修', '无关的其他产品'):
        assert act in proof
    assert not re.search('支付|付款|许可费|违约金|结算', proof)


@pytest.mark.parametrize('newline', ['\n', '\n\n', '\n\n\n'])
def test_secret_grant_list_keeps_its_original_source(newline):
    text = '乙方可以将许可技术用于：' + newline + '工业视觉检测设备的研发；'
    row = scope(text, secret=True)
    assert row['status'] == 'COVERED'
    assert any('研发' in s['quote'] for s in row['supporting_evidence'])
    assert all(s['quote'] in text for s in row['supporting_evidence'])
