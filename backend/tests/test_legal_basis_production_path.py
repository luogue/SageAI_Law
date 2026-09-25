"""Exercise the upload route, not a renderer-only fixture."""
import json
from pathlib import Path
from types import SimpleNamespace
from dataclasses import replace
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from routers import review_v2 as route
from review_v2 import engine
from review_v2.legal_basis_selection import select
from review_v2.legal_basis_trace import finish

ROOT=Path(__file__).resolve().parents[2]
EXPECTED={'D-04-02':['889','902','509'], 'D-04-03':['509','510'],
          'D-09-02':['450','453','903'], 'D-09-04':['450','448','903']}

def upload():
    app=FastAPI(); app.include_router(route.router)
    app.dependency_overrides[route.get_current_user]=lambda:1
    source=ROOT/'test_data/82 保管合同.docx'
    with TestClient(app) as client:
        response=client.post('/review-v2/file',data={'contract_type':'safekeeping','use_llm':'false'},
            files={'file':(source.name,source.read_bytes(),'application/vnd.openxmlformats-officedocument.wordprocessingml.document')})
    assert response.status_code==200,response.text
    return response.json()

@pytest.fixture(scope='module')
def production():return upload()

@pytest.mark.parametrize('rule',EXPECTED)
def test_upload_selected_basis_matches_final_markdown(production,rule):
    item=next(i for i in production['items'] if i['item_id']==rule)
    trace=item['decision_trace']['legal_basis_runtime_trace']
    expected='；'.join('《中华人民共和国民法典》第'+a+'条' for a in EXPECTED[rule])
    assert trace['selected_basis']==item['legal_basis_index']==expected
    assert trace['final_markdown']['VALUE_AFTER']==expected
    assert trace['selection_complete']
    assert trace['candidate_articles'] and trace['rule_source']['SOURCE_FILE']

@pytest.mark.parametrize('rule',EXPECTED)
def test_unit_and_upload_use_identical_runtime_metadata(production,rule):
    row=next(i for i in production['items'] if i['item_id']==rule)
    trace=row['decision_trace']['legal_basis_runtime_trace']
    item=SimpleNamespace(legal_basis_index='legacy',coverage_status=row['coverage_status'],decision_trace={'legal_basis_runtime_trace':{'stages':[]}})
    select(item,SimpleNamespace(**trace['runtime_rule_metadata']))
    assert item.legal_basis_index==row['legal_basis_index']

def test_runtime_metadata_change_is_consumed_by_upload(monkeypatch):
    original=engine.get_checklist_for_resolution
    def changed(*args,**kwargs):
        return tuple(replace(c,legal_basis_topics=('remuneration_payment',)) if 'remuneration_payment' in c.legal_basis_topics else c for c in original(*args,**kwargs))
    monkeypatch.setattr(engine,'get_checklist_for_resolution',changed)
    result=upload()
    item=next(i for i in result['items'] if i['item_id']=='D-04-02')
    assert item['legal_basis_index']=='《中华人民共和国民法典》第902条'
    assert result['production_path_trace']['cache']['status']=='MISS'

def test_renderer_cannot_select_legacy_references():
    item=SimpleNamespace(legal_basis_index='selected',decision_trace={'legal_basis_runtime_trace':{'selected_basis':'selected'}},
        legal_references=[{'article':'第903条','support_type':'DIRECT_SUPPORT'}])
    assert engine._trusted_legal_basis_display(item)=='selected'

@pytest.mark.parametrize('tamper',['result','markdown'])
def test_post_selection_overwrite_is_blocked(tamper):
    item=SimpleNamespace(item_id='X',legal_basis_index='old' if tamper=='result' else 'selected',
        decision_trace={'legal_basis_runtime_trace':{'selected_basis':'selected','selection_complete':True}})
    report='## Example（X）\n- 【法律依据】：'+('old' if tamper=='markdown' else 'selected')+'\n'
    assert finish([item],[{'item_id':'X','decision_trace':{}}],report)['status']=='BLOCKED'

def test_new_legal_modules_participate_in_source_drift_guard(monkeypatch):
    loaded=dict(route._LOADED_DEPENDENCY_SOURCES)
    loaded['legal_basis_selection']={**loaded['legal_basis_selection'],'sha256':'stale'}
    monkeypatch.setattr(route,'_LOADED_DEPENDENCY_SOURCES',loaded)
    assert route._runtime_source_drift_status('safekeeping')['status']!='CURRENT'

def test_unrelated_fee_keyword_does_not_select_lien(production):
    for row in production['items']:
        if row['item_id'] not in ('D-04-02','D-04-03'):continue
        trace=row['decision_trace']['legal_basis_runtime_trace']
        candidate=next(c for c in trace['candidate_articles'] if c['article']=='第903条')
        assert candidate['relevance_score']==0 and not candidate['matched_propositions']
        assert '第903条' not in row['legal_basis_index']
