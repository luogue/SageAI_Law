import pytest
from review_v2.clause_parser import parse_contract_clauses
from review_v2.employment_fact_store import FactStore
from review_v2.fact_dependencies import eligible, validate
from review_v2.fact_semantic_contracts import criteria, validate_checks
from review_v2.fact_validation import FactExtractionError
from backend.tests.test_employment_fact_pipeline import fact, packet, verified_packet


@pytest.mark.parametrize('concept,value', [
    ('nda.exception_public', True), ('nda.exception_prior', True),
    ('nda.remedies', '赔偿损失'), ('non_compete.arrangement', 'EXISTS'),
    ('non_compete.arrangement', 'DEFERRED'),
    ('non_compete.businesses', ['技术咨询']),
])
@pytest.mark.parametrize('invalid', ['missing', 'unsupported', 'foreign_evidence'])
def test_positive_verification_requires_own_proposition_and_evidence(concept, value, invalid):
    f = {'fact_id': 'f1', 'concept': concept, 'value': value, 'evidence': [{'quote': '原文'}]}
    checks = {k: {'supported': True, 'reason': '原文所约定的具体命题', 'evidence_indices': [0]}
              for k in criteria(concept, value)}
    key = next(iter(checks))
    if invalid == 'missing': checks.pop(key)
    elif invalid == 'unsupported': checks[key]['supported'] = False
    else: checks[key]['evidence_indices'] = [1]
    with pytest.raises(FactExtractionError, match='SEMANTIC_ENTAILMENT_INCOMPLETE'):
        validate_checks([f], {'checks': [{'fact_id': 'f1', 'supported': True, 'semantic_checks': checks}]})


def test_public_attestation_cannot_be_reused_as_prior_knowledge():
    f = {'fact_id': 'f1', 'concept': 'nda.exception_prior', 'value': True, 'evidence': [{'quote': '已公开的信息除外'}]}
    public = {k: {'supported': True, 'reason': '公开状态及例外', 'evidence_indices': [0]}
              for k in criteria('nda.exception_public', True)}
    with pytest.raises(FactExtractionError):
        validate_checks([f], {'checks': [{'fact_id': 'f1', 'supported': True, 'semantic_checks': public}]})
    # Rejecting the erroneous candidate is allowed, never auto-promoted.
    validate_checks([f], {'checks': [{'fact_id': 'f1', 'supported': False, 'reason': '公开不证明个人知悉'}]})


@pytest.mark.parametrize('parent', ['EXISTS', 'DEFERRED'])
def test_obligation_controls_children_but_missing_children_never_veto_parent(parent):
    roots = [{'concept': 'non_compete.arrangement', 'value': parent}]
    keys = ['non_compete.arrangement', 'non_compete.duration_months', 'non_compete.compensation']
    validate(roots, keys)
    assert eligible(keys, roots) == (keys if parent == 'EXISTS' else keys[:1])


@pytest.mark.parametrize('public', ['已进入公共领域的资料不属于秘密。', '受领之前已向公众合法开放的资料除外。'])
@pytest.mark.parametrize('restriction', ['离职后原则上不能从事竞争业务，具体期限与补偿另议。', '承诺离任后不加入竞争企业，限制细节待另签文件确定。'])
def test_final_report_keeps_three_semantic_boundaries(monkeypatch, public, restriction):
    from review_v2 import employment_fact_pipeline as p
    from review_v2.engine import review_contract_v2
    incident = '发现资料外泄应通知信息所有人并协助防止损失扩大。'
    liability = '违反保密义务造成损失，应承担损害赔偿责任。'
    text = '保密协议\n第一条\n甲方甲公司，乙方丙员工。保密信息包括技术资料。'+public+'\n第二条\n'+restriction+'\n第三条\n'+incident+'\n第四条\n'+liability
    cs = parse_contract_clauses(text)
    vals = [('nda.protected_information', '技术资料', '保密信息包括技术资料。'),
            ('nda.exception_public', True, public), ('non_compete.arrangement', 'EXISTS', restriction),
            ('nda.incident_response', '事件报告及减损', incident), ('nda.remedies', '损害赔偿', liability)]
    monkeypatch.setattr(p, 'extract', lambda *a, **k: packet(cs, [fact(cs,c,v,q) for c,v,q in vals]))
    monkeypatch.setattr(p, 'verify', verified_packet)
    r = review_contract_v2(text, 'confidentiality')
    rows = {i['item_id']: i for i in r['items']}
    scope = {e['element_id']: e['status'] for e in rows['NDA-01-01']['coverage_elements']}
    assert scope['nda_exception_public'] == 'COVERED'
    assert scope['nda_exception_prior'] == 'MISSING'
    assert all(rows[k]['coverage_status'] != '不适用' for k in ('NC-01-01','NC-02-01','NC-03-01'))
    debug = r['structured_fact_debug']['employment']['nda']
    assert debug['remedies'][0]['evidence'][0]['quote'] == liability
    assert debug['incident_response'][0]['evidence'][0]['quote'] == incident
    assert incident not in str(rows['NDA-04-01']['evidence_clauses'])
    assert liability in str(rows['NDA-04-01']['evidence_clauses'])
    assert r['release_quality_gate']['status'] == 'REPORT_READY', r['release_quality_gate']
