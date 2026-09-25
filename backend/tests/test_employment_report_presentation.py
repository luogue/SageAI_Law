import json
from copy import deepcopy
from pathlib import Path
from types import SimpleNamespace

from review_v2.report_presentation import PASS_ONLY, render_projection
from test_employment_fact_semantics import review, item


def test_projection_is_read_only_and_preserves_required_absence():
    rows = [SimpleNamespace(item_id='P', node_id='passed', coverage_status='通过', legal_consequence_if_missing='', narrative_state={}),
            SimpleNamespace(item_id='R', node_id='other', coverage_status='风险条款', title='不利约定', legal_consequence_if_missing=PASS_ONLY, narrative_state={'consequence': PASS_ONLY})]
    risk = SimpleNamespace(source_review_ids=['R'], consequence=PASS_ONLY, evidence_bundle={'items':[
        {'source_type':'SEARCH_AUDIT', 'claim_id':'passed:absence_search'},
        {'source_type':'SEARCH_AUDIT', 'claim_id':'missing:absence_search'},
        {'source_type':'CONTRACT_TEXT', 'claim_id':'passed:fact'}]})
    before = deepcopy(risk.__dict__)
    projected, findings = render_projection(rows, [risk])
    assert risk.__dict__ == before
    assert rows[1].legal_consequence_if_missing == PASS_ONLY
    assert PASS_ONLY not in projected[1].legal_consequence_if_missing
    assert [e['claim_id'] for e in findings[0].evidence_bundle['items']] == ['missing:absence_search', 'passed:fact']


def test_current_contract_presentation_and_decisions():
    root = Path(__file__).resolve().parents[2]
    baseline = json.loads((root/'artifacts/bnu_rights/result.json').read_text(encoding='utf-8'))
    text = (root/'artifacts/bnu_rights/normalized_input.txt').read_text(encoding='utf-8')
    result = review(text)
    fields = ['coverage_status', 'risk_severity', 'action_priority']
    assert {r['item_id']: [r.get(k) for k in fields] for r in result['items']} == {r['item_id']: [r.get(k) for k in fields] for r in baseline['items']}
    assert result['final_disposition_summary'] == baseline['final_disposition_summary']
    assert result['release_quality_gate']['status'] == 'REPORT_READY'
    assert PASS_ONLY not in result['result']
    assert '未找到以下正向事实：法定个人缴费' not in result['result']
    assert 'SEARCH_AUDIT' in json.dumps(result['risk_findings'], ensure_ascii=False)
    for key in ['EMP-13-01', 'EMP-IP-01']:
        assert item(result,key)['presentation']['legal_consequence']
        assert PASS_ONLY not in item(result,key)['presentation']['legal_consequence']
