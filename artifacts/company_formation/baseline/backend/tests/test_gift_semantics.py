import pytest
from review_v2.engine import review_contract_v2, parse_contract_clauses
from review_v2.gift_evidence import extract_facts


def review(text):
    return review_contract_v2('赠与合同。甲方为赠与人，乙方为受赠人。甲方无偿赠与乙方一套房屋。'+text,
                              'gift', use_llm=False)


@pytest.mark.parametrize('text', [
    '乙方承诺：自愿无偿接受甲方上述不动产赠与。',
    '受赠人表示接受本合同约定的房屋赠与。',
    '乙方同意接受赠与。',
])
def test_acceptance_with_intervening_object(text):
    result = review(text)
    item = next(i for i in result['items'] if i['item_id']=='G-01-03')
    assert item['coverage_status']=='通过'
    assert item['evidence_clauses']
    assert '接受' in str(item['evidence_clauses'])


def test_ordinary_gift_conditional_rules_na_and_no_manual_conflict():
    result = review('乙方自愿接受赠与。公证费及过户税费由乙方承担。')
    items = {i['item_id']:i for i in result['items']}
    for key in ['G-03-01','G-03-02','G-03-03','G-05-02','G-05-03',
                'G-08-01','G-08-02','G-09-01','G-09-02','G-09-03','G-09-04','G-10-04']:
        assert items[key]['coverage_status']=='不适用', key
        assert items[key]['applicability']['applicable'] is False
        assert '缺少可展示来源' not in items[key]['reasoning_summary']
    assert len(items)==48


@pytest.mark.parametrize('text,key', [
    ('本赠与已经公证。','notarized'),
    ('本赠与具有公益性质，用于救灾。','public_moral'),
    ('本合同为附义务赠与，乙方应赡养甲方。','attached'),
    ('乙方负有扶养义务。','support'),
])
def test_real_condition_activates(text,key):
    assert extract_facts(parse_contract_clauses(text))[key]['value'] is True


@pytest.mark.parametrize('text', ['公证费由乙方承担。','乙方支付税费。','乙方应配合提供登记资料。'])
def test_costs_not_notarization_or_attached_obligation(text):
    facts=extract_facts(parse_contract_clauses(text))
    assert facts['notarized']['value'] is False
    assert facts['attached']['value'] is False


@pytest.mark.parametrize('promise', ['永无反悔','永不反悔','不得以任何理由撤销','永久不得撤销'])
def test_unqualified_waiver_shared_semantics(promise):
    result=review('甲方承诺'+promise+'。')
    items={i['item_id']:i for i in result['items']}
    assert items['G-04-01']['coverage_status']=='通过'
    assert items['G-04-03']['coverage_status']=='通过'
    assert items['G-04-04']['coverage_status']=='风险条款'


def test_statutory_reservation_not_overbroad():
    result=review('甲方放弃任意撤销权，但保留法定撤销权。')
    item=next(i for i in result['items'] if i['item_id']=='G-04-04')
    assert item['coverage_status']=='通过'


def test_future_title_documents_not_attachment_entity():
    result=review('甲方应于过户前提供权属证明及相关资料。')
    item=next(i for i in result['items'] if i['item_id']=='G-12-02')
    assert item['coverage_status']!='通过'
    assert not item['evidence_clauses']


def test_actual_attachment_entity():
    result=review('附件一：不动产权证复印件，编号A123。')
    item=next(i for i in result['items'] if i['item_id']=='G-12-02')
    assert item['coverage_status']=='通过'


def test_registration_costs_do_not_prove_revocation_return_or_deadline():
    result=review('双方及时办理转移登记，相关税费由乙方承担。')
    items={i['item_id']:i for i in result['items']}
    assert items['G-08-04']['coverage_status']=='部分覆盖'
    assert items['G-11-01']['coverage_status']=='法律提示'
    assert items['G-11-04']['coverage_status']=='缺失'


def test_all_48_conditions_declared():
    from review_v2.gift_contract_checklist import GIFT_REVIEW_CHECKLIST
    assert len(GIFT_REVIEW_CHECKLIST)==48
    assert all(r.applicable_if for r in GIFT_REVIEW_CHECKLIST)
