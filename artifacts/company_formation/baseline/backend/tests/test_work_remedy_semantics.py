"""User-supplied clauses are independent cases, never edits to the original file."""
import pytest
from review_v2.clause_parser import parse_contract_clauses
from review_v2.engine import review_contract_v2, _applicability_polarity_gates, _judgment_text
from review_v2.engine import ReviewItemResult
from review_v2.sale_evidence import extract
from review_v2.work_evidence import PROFILES, applicability
from tests.test_work_canonical_evidence import document


@pytest.mark.parametrize('text,keys', [
    ('定作方有权要求重作、修理、减少价款或退货。', ['defect_repair', 'defect_remake', 'reduce_remuneration']),
    ('定作方同意利用的，应当按质论价，酌减酬金或价款。', ['reduce_remuneration']),
    ('不同意利用的，应当负责修整或调换。', ['defect_repair']),
    ('由此造成的损失由承揽方赔偿。', ['defect_compensation']),
    ('质量不合格时应重新制作。', ['defect_remake']),
    ('质量不合格时应重新加工。', ['defect_remake']),
    ('质量不合格时应重做。', ['defect_remake']),
])
def test_positive_remedy_recall(text, keys):
    clauses = parse_contract_clauses('第三条 质量责任\n1. '+text)
    for key in keys:
        rows = extract('work_'+key, clauses, PROFILES)
        assert rows, (text, key)
        assert all(text in e['quote'] and '第三条' in e['location'] for e in rows)


@pytest.mark.parametrize('text,key', [
    ('质量不合格时负责调换。', 'defect_remake'),
    ('质量不合格时定作方不得要求修理。', 'defect_repair'),
    ('质量不合格时定作方无权要求重作。', 'defect_remake'),
    ('质量不合格时不得减少价款。', 'reduce_remuneration'),
    ('质量不合格时无需赔偿损失。', 'defect_compensation'),
])
def test_remedies_do_not_invent_rights(text, key):
    assert not extract('work_'+key, parse_contract_clauses(text), PROFILES)


def test_independent_work_contract_full_pipeline():
    result = review_contract_v2('''加工承揽合同
承揽方：甲制造有限公司
定作方：乙科技有限公司
第一条 定作方委托承揽方按照图纸生产加工外壳。
第三条 质量责任
1. 定作方有权要求重作、修理、减少价款或退货。
第十二条 违约责任
1. 定作方同意利用的，应当按质论价，酌减酬金或价款；不同意利用的，应当负责修整或调换。由此造成的损失由承揽方赔偿。''', 'work_contract', use_llm=False)
    assert result['contract_type'] == 'work_contract'
    assert result['release_quality_gate']['status'] == 'REPORT_READY', result['release_quality_gate']['failures']
    rows = {i['item_id']: i for i in result['items']}
    for key in ('W-08-01','W-08-02','W-08-03','W-08-04'):
        assert rows[key]['coverage_status'] == '通过'
        assert rows[key]['evidence_clauses']
    assert rows['W-02-02']['coverage_status'] == '不适用'


def test_current_file_locations_and_applicability():
    result = review_contract_v2(document('56 承揽合同.docx'), 'work_contract', use_llm=False)
    assert result['release_quality_gate']['status'] == 'REPORT_READY'
    rows = {i['item_id']: i for i in result['items']}
    assert rows['W-02-02']['coverage_status'] == '不适用'
    assert rows['W-03-04']['coverage_status'] == '通过'
    for row in result['items']:
        if row['evidence_clauses']:
            assert row['evidence_location'] == '；'.join(dict.fromkeys(e['location'] for e in row['evidence_clauses']))
        if row['coverage_status'] == '不适用':
            assert row['applicable_if'] != '始终适用'
            assert row['applicability'].get('condition') != 'ALWAYS_APPLICABLE'
            assert '始终适用' not in str(row['applicability'])
        if row['coverage_status'] == '通过' and row['decision_trace']['review_mode'] == 'ABSENCE_REQUIRED':
            narrative = _judgment_text(ReviewItemResult(**row), {'clause_number': '无对应条款'})
            assert '未发现' in narrative and '已覆盖' not in narrative
    corrupt = ReviewItemResult(**rows['W-02-02'])
    corrupt.applicability['condition'] = 'ALWAYS_APPLICABLE'
    gate = _applicability_polarity_gates([corrupt], [], [])
    assert gate['status'] == 'BLOCKED'
    assert gate['gate_results']['NOT_APPLICABLE_NARRATIVE_GATE'] == 'FAIL'
    assert gate['not_applicable_rows'][0]['not_applicable_always_conflict'] is True


@pytest.mark.parametrize('text,active', [
    ('承揽方加工普通工业机器人铝合金外壳。', False),
    ('承揽方制造压力容器。', True),
    ('承揽工作依法需要行政许可。', True),
])
def test_license_requires_regulated_work(text, active):
    assert applicability('work_professional_license', parse_contract_clauses(text))['applicable'] is active
