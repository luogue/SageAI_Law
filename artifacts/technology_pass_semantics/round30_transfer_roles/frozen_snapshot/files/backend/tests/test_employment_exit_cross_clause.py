from review_v2.engine import review_contract_v2


def test_exit_requirements_can_be_satisfied_across_clauses():
    text = ('劳动合同\n第七条：乙方严重违反公司规章制度、严重失职、营私舞弊或者给甲方造成重大损害的，甲方可以依法解除劳动合同。\n'
            '第十二条：甲乙双方解除或者终止劳动合同，应按照国家法律法规办理。乙方主动辞职应提前三十日书面通知并完成工作交接。')
    result = review_contract_v2(text, 'labor', use_llm=False)
    row = next(i for i in result['items'] if i['item_id'] == 'EMP-10-01')
    assert row['coverage_status'] == '通过'
    assert all(e['status'] == 'COVERED' for e in row['coverage_elements'])
    assert result['release_quality_gate']['status'] == 'REPORT_READY', result['release_quality_gate']['failures']
