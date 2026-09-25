from copy import deepcopy
from pathlib import Path
from types import SimpleNamespace
import pytest
from review_v2.domain_selection import resolve_domain_selection, domain_selection_consistency_gate
from review_v2.clause_parser import parse_contract_clauses
from review_v2.engine import review_contract_v2


@pytest.mark.parametrize('domain, role, blocked', [
    ('WAREHOUSE', 'OTHER', False), ('WAREHOUSE', '合同当事人', False),
    ('TECHNOLOGY', 'OTHER', True), ('TECHNOLOGY', 'COMMISSIONING_PARTY', False),
])
def test_role_gate_scoped_to_accepted_domain(domain, role, blocked):
    resolution = SimpleNamespace(selected_domain=domain, resolution='USER_SELECTION_ACCEPTED',
        classification_context={'primary_transaction': {'type': 'commissioned_development'}})
    gate = domain_selection_consistency_gate(resolution, [], {'canonical_role': role})
    assert (gate['status'] == 'BLOCKED') == blocked


def test_rejected_candidate_does_not_supply_execution_context(monkeypatch):
    candidate = {'primary_transaction': {'type': 'commissioned_development'},
        'primary_transaction_model': {'type': 'ENTRUSTED_DEVELOPMENT'},
        'secondary_transactions': ['TECHNICAL_SERVICE'], 'ancillary_obligations': ['TECHNICAL_SUPPORT']}
    original = deepcopy(candidate)
    monkeypatch.setattr('review_v2.domain_selection._classify_document_family',
        lambda *args: ('TECHNOLOGY', 'high', [], {'TECHNOLOGY': 20}, candidate))
    text = '仓储合同，保管人负责保管存货人的仓储物。'
    resolution, _, routed = resolve_domain_selection('warehouse', text, parse_contract_clauses(text))
    assert routed == 'warehouse'
    assert resolution.classification_context['primary_transaction'] == {'type': 'warehouse'}
    for key in ('secondary_transactions', 'ancillary_obligations', 'primary_transaction_model'):
        assert not resolution.classification_context[key]
    assert candidate == original


def test_sequential_reviews_do_not_leak_primary_context():
    development = '技术开发（委托）合同。甲方委托乙方研发新的工业机器人自适应控制系统，甲方支付研发经费和报酬，乙方承担研究开发任务，交付新技术成果。'
    first = review_contract_v2(development, 'technology', use_llm=False)
    previous = deepcopy(first['domain_selection_resolution'])
    second = review_contract_v2('仓储合同。存货人甲公司将货物交保管人乙公司保管，按月支付仓储费，保管人签发仓单并凭仓单交付货物。', 'warehouse', use_llm=False)
    assert second['domain_selection_resolution']['classification_context']['primary_transaction']['type'] == 'warehouse'
    assert second['domain_selection_consistency_gate']['status'] == 'REPORT_READY'
    assert first['domain_selection_resolution'] == previous


def test_current_warehouse_file_production():
    from fastapi.testclient import TestClient
    from main import app
    from auth.routes import get_current_user
    path = next((Path(__file__).resolve().parents[2] / 'test_data').glob('55 *.docx'))
    old = app.dependency_overrides.get(get_current_user)
    app.dependency_overrides[get_current_user] = lambda: {'id': 1, 'phone': 'test'}
    try:
        with TestClient(app) as client:
            response = client.post('/review-v2/file', files={'file': (path.name, path.read_bytes(),
                'application/vnd.openxmlformats-officedocument.wordprocessingml.document')},
                data={'contract_type': 'warehouse', 'use_llm': 'false'})
        assert response.status_code == 200, response.text
        report = response.json()
        assert report['domain_selection_resolution']['selected_domain'] == 'WAREHOUSE'
        for row in report['items']:
            if row['item_id'] in {'WH-07-02', 'WH-09-03', 'WH-09-04'}:
                assert row['coverage_status'] == '缺失'
        assert report['domain_selection_resolution']['classification_context']['primary_transaction']['type'] == 'warehouse'
        assert report['release_quality_gate']['status'] == 'REPORT_READY', report['release_quality_gate']
    finally:
        if old is None:
            app.dependency_overrides.pop(get_current_user, None)
        else:
            app.dependency_overrides[get_current_user] = old
