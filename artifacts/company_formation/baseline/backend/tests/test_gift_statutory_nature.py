import pytest
from .test_gift_semantics import review


def test_statutory_silence_is_not_missing_or_optional_edit():
    result=review('乙方自愿接受赠与。')
    items={i['item_id']:i for i in result['items']}
    for key in ['G-05-01','G-05-04','G-06-01','G-06-02','G-07-01','G-10-01','G-11-01']:
        item=items[key]
        assert item['coverage_status']=='法律提示', key
        assert item['action_priority']=='NONE'
        assert not item['suggested_clause_example']
        assert not item['related_risks']
    assert sum(result['coverage_summary'].values())==48


@pytest.mark.parametrize('text,key,status', [
    ('赠与人法定撤销权自知道撤销事由之日起一年内行使。','G-05-04','法律提示'),
    ('赠与人法定撤销权自知道撤销事由之日起三年内行使。','G-05-04','风险条款'),
    ('继承人的撤销权自知道撤销事由之日起六个月内行使。','G-06-02','法律提示'),
    ('继承人的撤销权自知道撤销事由之日起一年内行使。','G-06-02','风险条款'),
])
def test_actual_statutory_period_deviation_still_actionable(text,key,status):
    result=review(text)
    assert next(i for i in result['items'] if i['item_id']==key)['coverage_status']==status


def test_shared_waiver_action_and_body_provenance():
    result=review('乙方承诺自愿接受甲方赠与。双方永无反悔。')
    items={i['item_id']:i for i in result['items']}
    for key in ['G-04-01','G-04-03']:
        item=items[key]
        assert item['coverage_status']=='通过'
        assert 'G-04-04' in item['action_suggestion']
        assert '无需修改' not in item['action_suggestion']
        assert item['related_risks']
    assert items['G-04-04']['coverage_status']=='风险条款'
    assert items['G-01-03']['coverage_status']=='通过'
    assert '其他文件' not in result['result']
    assert result['release_quality_gate']['status']=='REPORT_READY'
