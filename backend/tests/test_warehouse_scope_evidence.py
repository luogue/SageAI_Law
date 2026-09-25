import pytest
from review_v2.engine import review_contract_v2

@pytest.mark.parametrize('body, expected', [
    ('货物入库前乙方负责检查。保管不妥造成损失由乙方赔偿。', '缺失'),
    ('存货人有权检查仓储物并提取样品，保管人应配合。仓储物部分毁损时，未损部分返还，损坏部分赔偿。因保管不善导致价值减损的，按减损价值赔偿。', '通过'),
])
def test_scoped_evidence_not_broad_mentions(body, expected):
    report = review_contract_v2('仓储合同。' + body, 'warehouse', use_llm=False)
    for row in report['items']:
        if row['item_id'] in {'WH-07-02', 'WH-09-03', 'WH-09-04'}:
            assert row['coverage_status'] == expected
            if expected == '通过':
                assert any(e.get('source_type') == 'SOURCE_CLAUSE' for e in row['evidence_clauses'])

def test_role_gate_has_no_coverage_side_effect(monkeypatch):
    text = '仓储合同。货物入库前乙方负责检查。保管不妥造成损失由乙方赔偿。'
    first = review_contract_v2(text, 'warehouse', use_llm=False)
    monkeypatch.setattr('review_v2.engine.domain_selection_consistency_gate',
        lambda *a, **kw: {'status': 'REPORT_READY', 'failures': []})
    second = review_contract_v2(text, 'warehouse', use_llm=False)
    assert [(r['item_id'], r['coverage_status']) for r in first['items']] == [(r['item_id'], r['coverage_status']) for r in second['items']]
