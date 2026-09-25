import pytest
from review_v2.engine import review_contract_v2


@pytest.mark.parametrize('text,rule', [
    ('双方依法履行劳动合同，依法解除。', 'EMP-16-01'),
    ('乙方离职后承担竞业限制义务，违反竞业限制支付违约金200000元。', 'EMP-14-01'),
    ('专项培训服务期违约金不得超过未履行服务期分摊的培训费用。', 'EMP-14-01'),
    ('乙方履职或主要利用公司资源形成的软件成果，其知识产权按照法律规定处理。', 'EMP-IP-01'),
])
def test_full_search_is_valid_negative_proof(text, rule):
    result = review_contract_v2('劳动合同\n' + text, 'labor', use_llm=False)
    item = next(i for i in result['items'] if i['item_id'] == rule)
    assert item['coverage_status'] == '通过'
    assert not item['needs_manual_review']
    assert item['decision_trace']['verified_pass_source_gate']['assessment'] == 'FULL_CORPUS_NO_ADVERSE_FACT'


def test_probation_summary_detail_have_same_proof():
    result = review_contract_v2('劳动合同\n合同期限自2027年2月1日至2029年1月31日。试用期自2027年2月1日至2027年4月30日。\n试用期工资为9500元。\n试用期内依法缴纳社保。', 'labor', use_llm=False)
    item = next(i for i in result['items'] if i['item_id'] == 'EMP-15-01')
    assert item['coverage_status'] == '风险条款'
    risks = [f for f in result['risk_findings'] if item['item_id'] in f['source_review_ids']]
    assert risks
    for finding in risks:
        for field in ['evidence', 'supporting_evidence']:
            assert finding[field]
            assert not any('工资' in str(e) or '社保' in str(e) for e in finding[field])
        assert not any('工资' in e['quoted_text'] or '社保' in e['quoted_text'] for e in finding['evidence_bundle']['items'])
    assert result['release_quality_gate']['status'] == 'REPORT_READY', result['release_quality_gate']['failures']
