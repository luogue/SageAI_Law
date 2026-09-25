"""Real file endpoint acceptance for the two immutable DOCX files and a third fixture."""
import hashlib
import argparse
import io
import json
import runpy
import sys
from collections import Counter
from datetime import timedelta
from pathlib import Path

import requests
from docx import Document

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'backend'))
from auth.utils import create_access_token
parser=argparse.ArgumentParser()
parser.add_argument('--output',default='artifacts/agency-generalization')
parser.add_argument('--baseline',default='artifacts/agency80-before.json')
args=parser.parse_args()
OUT=ROOT/args.output
OUT.mkdir(exist_ok=True)

def post(name,content):
    response=requests.post('http://127.0.0.1:8016/review-v2/file',
        headers={'Authorization':'Bearer '+create_access_token({'user_id':'1'},timedelta(minutes=5))},
        files={'file':(name,content,'application/vnd.openxmlformats-officedocument.wordprocessingml.document')},
        data={'contract_type':'agency','use_llm':'false','include_low_risk':'true'},timeout=180)
    response.raise_for_status()
    return response.json()

commercial=runpy.run_path(str(ROOT/'backend/tests/test_agency_generalization.py'))['COMMERCIAL']
doc=Document()
for line in commercial.splitlines():doc.add_paragraph(line)
stream=io.BytesIO();doc.save(stream)
payloads=[(label,p.name,p.read_bytes(),p) for label,p in
          [('A',next((ROOT/'test_data').glob('77 *.docx'))),('B',next((ROOT/'test_data').glob('80 *.docx')))]]
payloads.append(('C','商业委托泛化回归.docx',stream.getvalue(),None))
summaries=[]
for label,name,content,path in payloads:
    digest=hashlib.sha256(content).hexdigest()
    result=post(name,content)
    (OUT/f'{label}-response.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8')
    (OUT/f'{label}-report.md').write_text(result['result'],encoding='utf8')
    rows={i['item_id']:i for i in result['items']}
    assert result['contract_type']=='agency'
    assert result['release_quality_gate']['status']=='REPORT_READY',result['release_quality_gate']['failures']
    for key in ['A-01-01','A-03-03','A-12-01','A-12-03','A-13-03']:
        assert rows[key]['coverage_status']=='通过',(label,key,rows[key]['coverage_status'])
    if label=='B':
        assert len(rows)==42
        for key in ['A-01-03','A-07-03']:assert rows[key]['coverage_status']=='通过'
        assert rows['A-04-02']['coverage_status']=='部分覆盖'
        assert rows['A-12-02']['coverage_status']=='通过'
        for key in ['A-04-01','A-08-03','A-14-01']:assert rows[key]['coverage_status']!='通过'
        assert rows['A-08-02']['coverage_status']=='通过'
    if label=='C':
        for key in ['A-01-03','A-04-02','A-07-03','A-12-02']:assert rows[key]['coverage_status']=='通过'
    if path:assert hashlib.sha256(path.read_bytes()).hexdigest()==digest
    summaries.append(dict(sample=label,file=name,sha256=digest,task_id=result['contract_review_trace_id'],
        worker_pid=result['production_path_trace']['process_id'],count=len(rows),
        counts=dict(Counter(i['coverage_status'] for i in rows.values())),gate=result['release_quality_gate']['status']))
    if label=='B':
        before=json.loads((ROOT/args.baseline).read_text(encoding='utf8'))
        old={i['item_id']:i for i in before['items']}
        diff=[dict(rule=key,title=i['title'],before=old[key]['coverage_status'],after=i['coverage_status'],
                   before_evidence=old[key]['evidence_clauses'],after_evidence=i['evidence_clauses'],
                   elements=i['coverage_elements']) for key,i in rows.items()]
        (OUT/'42-rule-diff.json').write_text(json.dumps(diff,ensure_ascii=False,indent=2),encoding='utf8')
        (OUT/'42-rule-diff.md').write_text('| 规则 | 审查项 | 修复前 | 修复后 |\n|---|---|---|---|\n'+
            '\n'.join(f"| {d['rule']} | {d['title']} | {d['before']} | {d['after']} |" for d in diff),encoding='utf8')
        trace={i['item_id']:dict(requirements=i['decision_trace'].get('semantic_requirements'),
            corpus_to_acceptance=i['decision_trace'].get('canonical_semantic_audit'),
            search_audit=i['decision_trace'].get('element_absence_searches'),
            final_elements=i['coverage_elements'],final_evidence=i['evidence_clauses'],final_status=i['coverage_status'])
            for i in rows.values() if i['decision_trace'].get('require_canonical_validation')}
        (OUT/'production-element-trace.json').write_text(json.dumps(trace,ensure_ascii=False,indent=2),encoding='utf8')
(OUT/'acceptance.json').write_text(json.dumps(summaries,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(summaries,ensure_ascii=False,indent=2))
