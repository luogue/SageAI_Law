from copy import deepcopy
from pathlib import Path
import pytest
from review_v2.engine import RiskFinding, _user_visible_risk_themes, _is_checkpoint_applicable
from review_v2.company_formation_checklist import COMPANY_FORMATION_CHECKLIST


def atom(fact='authority', evidence='C1', remedy='restore', scope='company-a'):
    return dict(fact=fact, scope=scope, actor='shareholders', object='decisions', legal_exposure=fact,
                remedy=remedy, evidence_ids=[evidence], title='权利安排', parent_title='共同治理',
                summary='已确认的权利安排冲突', recommendation='恢复合法权利')


def finding(name, rows, severity='MEDIUM', priority='B_PRACTICAL'):
    return RiskFinding(finding_id=name, risk_group=name, title='相似名称', severity=severity, priority=priority,
        source_review_ids=[name], facts=[], evidence=[], source_clause_ids=[e for r in rows for e in r['evidence_ids']],
        aggregation_signals={'adverse_fact_atoms':rows}, evidence_bundle={'items':[{'clause_id':r['evidence_ids'][0]} for r in rows]})


def test_parent_specific_merge_preserves_maxima_and_provenance():
    rows=[finding('parent',[atom()]),finding('specific',[atom()], 'HIGH','A_CORE')]
    themes=_user_visible_risk_themes(rows)
    assert len(rows)==2 and len(themes)==1
    theme=themes[0]
    assert theme['severity']=='HIGH' and theme['priority']=='A_CORE'
    assert theme['related_rule_ids']==['parent','specific']
    assert 'C1' in theme['evidence_ids'] and len(theme['evidence_packages'])==2
    assert theme['recommendation'].count('恢复合法权利')==1


def test_similar_titles_different_facts_do_not_merge():
    assert len(_user_visible_risk_themes([finding('a',[atom('authority')]),finding('b',[atom('capital')])]))==2


def test_same_exposure_and_remedy_at_different_locations_retains_both():
    themes=_user_visible_risk_themes([finding('a',[atom(evidence='C10')]),finding('b',[atom(evidence='C50')])])
    assert len(themes)==1
    assert {'C10','C50'} <= set(themes[0]['evidence_ids'])


def test_same_clause_independent_exposure_or_remedy_stays_separate():
    assert len(_user_visible_risk_themes([finding('a',[atom()]),finding('b',[atom(remedy='delete')])]))==2
    assert len(_user_visible_risk_themes([finding('a',[atom()]),finding('b',[atom(scope='company-b')])]))==2


def test_parent_connects_atoms_without_losing_specialist_findings():
    rows=[finding('a',[atom('organ')]),finding('b',[atom('authority')]),finding('p',[atom('organ'),atom('authority')])]
    themes=_user_visible_risk_themes(rows)
    assert len(themes)==1 and themes[0]['underlying_finding_count']==3
    assert set(themes[0]['source_rule_ids'])=={'a','b','p'}


@pytest.mark.parametrize('text,expected',[
    ('有限责任公司，甲方出资六万元，乙方出资四万元。公司不设股东会。',True),
    ('一人有限责任公司，只有一名股东。公司不设股东会。',False),
    ('有限责任公司，甲方出资六万元，乙方出资四万元。全体股东书面一致决定，可不召开股东会会议。',False),
    ('有限责任公司，甲方出资六万元，乙方出资四万元。',False),
    ('合伙企业，两名股东。公司不设股东会。',False),
])
def test_organ_prerequisites_and_metadata(text,expected):
    checkpoint=next(c for c in COMPANY_FORMATION_CHECKLIST if c.node_id=='formation_no_shareholder_organ')
    assert checkpoint.applicable_if!='始终适用'
    assert checkpoint.kind=='forbidden'
    assert _is_checkpoint_applicable(text,checkpoint,'shareholders')[0] is expected


@pytest.mark.parametrize('identity,arrangement', [
    ('公司只有一名股东。', '公司不设股东会。'),
    ('甲方出资六万元，乙方出资四万元。', '全体股东一致书面同意的，可以不召开股东会会议。'),
])
def test_nontriggered_organ_rule_in_full_report(identity,arrangement):
    from review_v2.engine import review_contract_v2
    result=review_contract_v2('股东合作协议\n有限责任公司\n'+identity+'\n'+arrangement,'shareholders',use_llm=False)
    row=next(i for i in result['items'] if i['item_id']=='CF-15-01')
    assert row['coverage_status']=='不适用'
    assert row['applicability']['applicable'] is False
    assert row['applicable_if']!='始终适用'
    assert not row['suggested_clause_example']


def test_original_production_themes_detail_and_renderer():
    from fastapi import FastAPI
    from fastapi.testclient import TestClient
    from routers import review_v2 as route
    app=FastAPI(); app.include_router(route.router)
    app.dependency_overrides[route.get_current_user]=lambda:{'id':'theme-closure'}
    source=Path(__file__).resolve().parents[2]/'test_data'/'83 投资协议.docx'
    with TestClient(app) as client:
        response=client.post('/review-v2/file',data={'contract_type':'investment','use_llm':'false','include_low_risk':'true'},files={'file':(source.name,source.read_bytes(),'application/vnd.openxmlformats-officedocument.wordprocessingml.document')})
    assert response.status_code==200,response.text
    r=response.json(); details={i['item_id']:i for i in r['items']}
    assert r['contract_type']=='shareholders'
    assert r['report_context']['scenario_label']=='股东合作协议' and r['report_context']['user_role'] in {'equity_party','shareholder'}
    assert r['release_quality_gate']['status']=='REPORT_READY',r['release_quality_gate']['failures']
    for key in ['CF-05-01','CF-12-01','CF-15-01']:
        assert details[key]['coverage_status']=='风险条款'
    themes=[t for t in r['risk_themes'] if set(t['source_rule_ids']) & {'CF-05-01','CF-12-01','CF-15-01'}]
    assert len(themes)==1
    assert {'CF-05-01','CF-12-01','CF-15-01'}<=set(themes[0]['source_rule_ids'])
    assert r['risk_theme_count']<len(r['risk_findings'])
    overview=r['final_overview_summary']
    assert sum(overview[k] for k in ['major_risk','medium_risk','low_risk'])==r['risk_theme_count']
    assert overview['priority_action']==r['risk_theme_summary']['must_change']
    assert overview['recommended_action']==r['risk_theme_summary']['should_change']
    from review_v2.report_statistics import statistics_gate
    corrupted=deepcopy(r)
    next(t for t in corrupted['risk_themes'] if len(t['source_rule_ids'])>1)['severity']='LOW'
    assert any(f['requirement']=='THEME_MAX_SEVERITY' for f in statistics_gate(corrupted)['failures'])
    assert themes[0]['severity']=='HIGH' and themes[0]['priority']=='A_CORE'
    assert details['CF-15-01']['applicable_if']!='始终适用'
    assert details['CF-15-01']['applicable_if'] in r['result']
    for title in ['核心风险摘要','建议优先修改']:
        section=r['result'].split('、'+title,1)[1].split('\n## ',1)[0]
        assert section.count(themes[0]['title'])==1
