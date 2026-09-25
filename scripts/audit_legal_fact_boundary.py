"""Reproducible same-file production-route A/B; preserve raw stage evidence."""
import collections
import hashlib
import json
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'backend')]
from fastapi import FastAPI
from fastapi.testclient import TestClient
from routers import review_v2 as route
from review_v2.legal_enrichment_boundary import enrichment_mode

def upload():
    app=FastAPI();app.include_router(route.router)
    app.dependency_overrides[route.get_current_user]=lambda:1
    source=ROOT/'test_data/82 保管合同.docx'
    with TestClient(app) as client:
        response=client.post('/review-v2/file',data={'contract_type':'safekeeping','use_llm':'false'},
            files={'file':(source.name,source.read_bytes(),'application/vnd.openxmlformats-officedocument.wordprocessingml.document')})
    assert response.status_code==200,response.text
    return response.json()

def business(item):
    keys=('status','coverage_status','risk_level','risk_severity','action_priority','issue_type',
          'applicability','coverage_elements','risk_point_description','formal_recommendation',
          'review_judgment','action_suggestion','residual_risk','needs_manual_review')
    data={k:item.get(k) for k in keys}
    data['evidence']=[{k:e.get(k) for k in ('evidence_id','clause_id','quote','supports','supporting_element_ids','source_span')}
                      for e in item.get('evidence_clauses',[])]
    data['search_audit']=item['decision_trace'].get('element_absence_searches')
    for key in ('shared_concept_facts','semantic_requirements','element_evidence_truth','narrative_elements'):
        data[key]=item['decision_trace'].get(key)
    return data

OUT=ROOT/'artifacts/factual-regression-ab'
OUT.mkdir(parents=True,exist_ok=True)
def write(name,value):
    (OUT/name).write_text(json.dumps(value,ensure_ascii=False,indent=2),encoding='utf-8')

reports=[]
for enabled in (False,True):
    name='on' if enabled else 'off'
    if '--summarize' in sys.argv:
        result=json.loads((OUT/('report-'+name+'.json')).read_text(encoding='utf-8'))
    else:
        with enrichment_mode(enabled): result=upload()
    write('report-'+name+'.json',result)
    (OUT/('report-'+name+'.md')).write_text(result['result'],encoding='utf-8')
    reports.append(result)

a,b=reports
diffs=[]
rows=[]
for x,y in zip(a['items'],b['items']):
    old,new=business(x),business(y)
    changed=[k for k in old if old[k]!=new[k]]
    rows.append({'rule_id':x['item_id'],'OFF':old,'ON':new,'DIFF':changed})
    if changed:diffs.append({'rule_id':x['item_id'],'fields':changed})
summary={'source_sha256':hashlib.sha256((ROOT/'test_data/82 保管合同.docx').read_bytes()).hexdigest(),
         'total':len(rows),'diff_count':len(diffs),'differences':diffs,
         'statistics':dict(collections.Counter(i['coverage_status'] for i in b['items'])),
         'legal_immutability_failures':[i['item_id'] for i in b['items'] if i['decision_trace']['legal_enrichment_boundary']['changed_fields']],
         'special_over_general_violation':sum(bool(i['decision_trace']['legal_basis_runtime_trace']['full_basis_audit']['special_over_general_violation']) for i in b['items']),
         'release_quality_gate':b['release_quality_gate']}
write('comparison.json',{'summary':summary,'rules':rows})

stable=json.loads((ROOT/'artifacts/basis-special-live/report.json').read_text(encoding='utf-8'))
current=json.loads((ROOT/'artifacts/factual-regression-current/live-before.json').read_text(encoding='utf-8'))
unavailable={'captured':False,'reason':'历史报告未保存该阶段独立快照；不从最终结果倒推或伪造。'}
def stages(item):
    trace=item['decision_trace'];legal=trace.get('legal_basis_runtime_trace',{})
    boundary=trace.get('legal_enrichment_boundary',{})
    return {
      '1_rule_config':legal.get('runtime_rule_metadata',unavailable),
      '2_required_elements':trace.get('semantic_requirements',legal.get('required_elements',unavailable)),
      '3_applicability':item.get('applicability'),
      '4_query':trace.get('element_absence_searches',trace.get('retrieval_trace',unavailable)),
      '5_positive_fact_pool':trace.get('shared_concept_facts',unavailable),
      '6_candidates':trace.get('evidence_assembly',unavailable),
      '7_SEARCH_AUDIT_input':[{k:v for k,v in a.items() if k not in ('result','supporting_evidence')} for a in trace.get('element_absence_searches',[])],
      '8_SEARCH_AUDIT_output':trace.get('element_absence_searches',unavailable),
      '9_aggregation_input':trace.get('element_evidence_truth',unavailable),
      '10_aggregation_output':{'coverage':item['coverage_status'],'elements':item['coverage_elements']},
      '11_before_legal':boundary.get('before',unavailable),
      '12_after_legal':boundary.get('after',unavailable),
      '13_final_renderer_input':{k:item.get(k) for k in ('coverage_status','coverage_elements','evidence_clauses','review_judgment','risk_point_description','formal_recommendation')},
      'initial_llm_reason':item.get('llm_raw_reason'),
      'legal_stage_trace':legal.get('stages'),
    }
diagnostic={}
for rid in ('D-07-03','D-11-03','D-12-02'):
    versions=[next(i for i in r['items'] if i['item_id']==rid) for r in (stable,current,b)]
    diagnostic[rid]={'STABLE_VERSION':stages(versions[0]),'CURRENT_VERSION_BEFORE_FIX':stages(versions[1]),
                     'CURRENT_VERSION_AFTER_FIX':stages(versions[2]),
                     'DIFF':{'coverage':[i['coverage_status'] for i in versions],
                             'required_elements':[[e['proposition'] for e in i['coverage_elements']] for i in versions]}}
    old_config=stages(versions[0])['1_rule_config'];new_config=stages(versions[1])['1_rule_config']
    diagnostic[rid]['DIFF']['pre_fix_business_rule_metadata_changes']=[k for k in set(old_config)|set(new_config)
        if k not in ('legal_basis','legal_basis_topics','legal_basis_domain') and old_config.get(k)!=new_config.get(k)]
diagnostic['version_provenance']={
    'STABLE_VERSION':{'artifact':'artifacts/basis-special-live/report.json','runtime':stable['production_path_trace']},
    'CURRENT_VERSION_BEFORE_FIX':{'artifact':'artifacts/factual-regression-current/live-before.json','runtime':current['production_path_trace']},
    'CURRENT_VERSION_AFTER_FIX':{'artifact':'artifacts/factual-regression-ab/report-on.json','runtime':b['production_path_trace']},
    'limitations':'旧版本只读取原始留存报告，没有伪造缺失阶段快照，也没有在共享工作区回滚其他任务。用户报告的36 PASS未完整复现；本轮旧路径实测38 PASS。'}
write('stage-diagnostic.json',diagnostic)
print(json.dumps(summary,ensure_ascii=False,indent=2))
