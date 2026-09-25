"""IP report decisions consume verified relations, never schema descriptions."""
import pytest
from review_v2.clause_parser import parse_contract_clauses
from backend.tests.test_employment_fact_pipeline import fact, packet, verified_packet


@pytest.mark.parametrize('mode,expected', [('absent','缺失'), ('statutory','通过'),
                                         ('adverse','风险条款'), ('ambiguous','待核验')])
def test_ip_final_report_states(monkeypatch, mode, expected):
    from review_v2 import employment_fact_pipeline as pipeline
    from review_v2.engine import review_contract_v2
    text = '劳动合同\n第一条\n双方依法履行劳动合同。\n第二条 成果\n'
    quotes = {'statutory':'履职形成的成果依法律规定确定归属。',
              'adverse':'所有非职务成果自动归用人单位所有。',
              'ambiguous':'成果按照未提供的归属协议处理。'}
    text += quotes.get(mode, '双方协商处理其他事项。')
    cs = parse_contract_clauses(text)
    fs = [] if mode in {'absent','ambiguous'} else [fact(cs,'ip.allocations',{
        'scope':'NON_DUTY' if mode=='adverse' else 'DUTY_OR_RESOURCES',
        'beneficiary':'EMPLOYER' if mode=='adverse' else 'UNSPECIFIED',
        'mode':'AUTOMATIC' if mode=='adverse' else 'STATUTORY'},quotes[mode])]
    monkeypatch.setattr(pipeline,'extract',lambda *a,**kw:packet(cs,fs))
    def verify(clauses, store):
        result = verified_packet(clauses,store)
        if mode=='ambiguous':
            result['verification']['unresolved_concepts']=['ip.allocations']
        return result
    monkeypatch.setattr(pipeline,'verify',verify)
    result = review_contract_v2(text,'labor',include_low_risk=True)
    row = next(r for r in result['items'] if r['item_id']=='EMP-IP-01')
    assert row['coverage_status']==expected
    public = result['result']
    for token in ('DUTY_OR_RESOURCES','UNDIFFERENTIATED_RESULTS','beneficiary','ip.allocations','{scope:'):
        assert token not in public
    if mode=='absent':
        assert row['action_priority']=='C_OPTIMIZATION'
        assert not row['needs_manual_review']
        assert '可选优化' in public
    if fs:
        assert any(quotes[mode] in e.get('quote',e.get('text','')) for e in row['evidence_clauses'])
    assert result['release_quality_gate']['status']=='REPORT_READY', result['release_quality_gate']['failures']
