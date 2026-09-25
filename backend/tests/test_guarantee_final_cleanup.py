import pytest
from review_v2.engine import review_contract_v2
from review_v2.narrative_composition import dedupe, compose_risk_fields

def review(clause, key):
    result=review_contract_v2('保证合同\n乙方（保证人）：周明\n身份证号码：123\n第九条 债权转让\n'+clause,'guarantee',use_llm=False)
    return next(i for i in result['items'] if i['item_id']==key)

@pytest.mark.parametrize('clause',[
 '债权转让后，保证人在原保证范围内继续承担责任。',
 '债权转让后，保证人在本合同担保范围内继续承担责任。',
 '债权转让不改变保证范围。',
 '保证责任不因债权转让而扩大。',
 '受让人取得的保证权利以原保证范围为限。',
])
def test_original_scope(clause):
    item=review(clause,'GUA-09-03')
    assert item['coverage_status']=='通过'
    assert item['evidence_clauses']
    assert all(clause in e['quote'] and e['quote'] in '第九条 债权转让\n'+clause for e in item['evidence_clauses'])

@pytest.mark.parametrize('clause,expected',[
 ('债权转让应当通知保证人。','通过'),
 ('债权人可转让债权。','法律提示'),
 ('债权转让无需通知保证人即可对保证人发生效力。','风险条款'),
])
def test_notice_nature(clause,expected):
    item=review(clause,'GUA-09-01')
    assert item['coverage_status']==expected
    if expected=='法律提示':
        assert not item['related_risks']
        assert item['action_priority']=='NONE'

@pytest.mark.parametrize('clause',[
 '债权可以转让，保证责任可以扩大。',
 '债权转让后，保证人不在原保证范围内继续承担责任。',
 '保证责任因债权转让而扩大。',
])
def test_scope_negative(clause):
    assert review(clause,'GUA-09-03')['coverage_status']!='通过'

def test_instruction_dedup():
    assert dedupe('核验查询资格；建议核验查询资格；核验报送资格。')=='核验查询资格；核验报送资格。'
    assert dedupe('应当通知；不得通知。')=='应当通知；不得通知。'
    assert dedupe('核验100万元；核验200万元。')=='核验100万元；核验200万元。'

def test_duplicate_fields_not_repeated():
    fields=compose_risk_fields('发现签署错误。','发现签署错误。','可能造成身份混乱。','可能造成身份混乱。')
    assert fields==dict(judgment='发现签署错误。',issue='',consequence='可能造成身份混乱。',exposure='')
