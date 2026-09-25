import pytest
from test_employment_fact_semantics import review, item

CORE = '实行标准工时制度，每日工作不超过8小时、每周不超过40小时。乙方依法享有带薪年休假，每周休息两日。'


@pytest.mark.parametrize('extra', ['', '休息日加班依法安排补休。', '不得约定加班不支付任何报酬。', '法定节假日加班不得仅以调休替代加班工资。', '月工资包含全部加班工资，不足部分依法补足。'])
def test_basic_hours_and_rest_sufficient(extra):
    result = review(CORE + extra)
    row = item(result, 'EMP-05-01')
    assert row['coverage_status'] == '通过'
    assert row['risk_severity'] == 'NONE'
    assert not row['related_risks']
    assert result['release_quality_gate']['status'] == 'REPORT_READY'


@pytest.mark.parametrize('adverse', ['加班不支付任何报酬。', '月工资当然包含全部加班工资。', '乙方放弃法定加班工资。', '甲方不支付加班费。', '法定节假日加班仅以调休替代。', '乙方每周七天均须工作。'])
def test_direct_adverse_overrides_basic_coverage(adverse):
    result = review(CORE + adverse)
    row = item(result, 'EMP-05-01')
    assert row['coverage_status'] == '风险条款'
    assert row['related_risks']
    assert any(adverse in e['text'] for e in row['evidence_clauses'])
    assert result['release_quality_gate']['status'] == 'REPORT_READY'


@pytest.mark.parametrize('text', ['乙方依法享有带薪年休假。', '实行标准工时制度。'])
def test_core_gaps_still_actionable(text):
    row = item(review(text), 'EMP-05-01')
    assert row['coverage_status'] == '部分覆盖'
    assert row['action_priority'] == 'B_PRACTICAL'
