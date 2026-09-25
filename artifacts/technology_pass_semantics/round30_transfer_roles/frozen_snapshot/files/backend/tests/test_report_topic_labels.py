from types import SimpleNamespace
from review_v2.report_topic_labels import project, gate, recommendation_topics

def fixture():
    f=SimpleNamespace(finding_id='f',title='old',evidence_bundle={'items':[{'support_labels':['old'],'quote':'evidence'}]})
    return f,[{'title':'final','member_finding_ids':['f']}]

def test_projection_preserves_source_and_uses_final_topic():
    f,t=fixture();p=project([f],t)
    assert f.title=='old' and f.evidence_bundle['items'][0]['support_labels']==['old']
    assert p[0].title=='final' and p[0].evidence_bundle['items'][0]['quote']=='evidence'
    assert gate(p,t,lambda f:'[支持：final]')['status']=='REPORT_READY'

def test_stale_evidence_label_blocks():
    f,t=fixture();p=project([f],t);p[0].evidence_bundle['items'][0]['support_labels']=['old']
    assert gate(p,t,lambda f:'')['status']=='BLOCKED'

def test_stale_rendered_label_blocks():
    f,t=fixture()
    assert gate(project([f],t),t,lambda f:'[支持：old]')['status']=='BLOCKED'

def test_recommendation_topic_blocks_on_mismatch():
    f,t=fixture();r=[{'source_finding_ids':['f']}];recommendation_topics(r,t)
    assert gate(project([f],t),t,lambda f:'',r)['status']=='REPORT_READY'
    r[0]['recommendation_topics']=['old']
    assert gate(project([f],t),t,lambda f:'',r)['status']=='BLOCKED'
