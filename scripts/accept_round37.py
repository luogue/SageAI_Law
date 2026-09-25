import ast,hashlib,json,sqlite3,sys,xml.etree.ElementTree as ET
from pathlib import Path
root=Path(__file__).resolve().parents[1]
out=root/'artifacts/technology_pass_semantics/round37_export_blockers'
db=sqlite3.connect('file:'+str(root/'backend/data/review_snapshots.sqlite3')+'?mode=ro',uri=True)
binding=json.loads((out/'original_binding.json').read_text(encoding='utf8'))
run=db.execute('select latest_run from tasks where id=?',(binding['review_task_id'],)).fetchone()[0]
payload,final_binding=db.execute('select payload,binding from runs where id=?',(run,)).fetchone()
r=json.loads(payload);b=json.loads(final_binding)
g=r['release_quality_gate']
assert run!=binding['review_run_id']
assert g['status']=='REPORT_READY' and not g['failures'] and not g['blocking_rules']
assert g['gate_results']['REVIEW_EVIDENCE_ELEMENT_MISMATCH']=='PASS'
(out/'final_report.json').write_text(payload,encoding='utf8')
(out/'final_binding.json').write_text(final_binding,encoding='utf8')
changed={}
for name in ('engine.py','technology_service_elements.py'):
    a=ast.parse((out/'baseline_source'/name).read_text(encoding='utf-8-sig'))
    path=root/'backend/review_v2'/name
    z=ast.parse(path.read_text(encoding='utf-8-sig'))
    funcs=lambda tree:{n.name:ast.dump(n,include_attributes=False) for n in tree.body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))}
    old,new=funcs(a),funcs(z)
    changed[name]=[k for k in old.keys()|new.keys() if old.get(k)!=new.get(k)]
    assert not any(any(w in k.lower() for w in ('gate','verifier','verify','fallback')) for k in changed[name])
    (out/('final_'+name)).write_bytes(path.read_bytes())
integrity=json.loads((out/'test_source_integrity.json').read_text(encoding='utf8'))
assert integrity['unchanged']
assert all(hashlib.sha256((root/p).read_bytes()).hexdigest()==h for p,h in integrity['after'].items())
tests=list(ET.parse(out/'regression.xml').iter('testcase'))
assert all(t.find('failure') is None and t.find('error') is None for t in tests)
data={'status':'REVIEW_READY_EXPORT_PENDING','original_run':binding['review_run_id'],'final_binding':b,
      'gate':'REPORT_READY','blockers':0,'evidence_mismatch':0,'tests':len(tests),'failed':0,
      'changed_functions':changed,'gate_verifier_fallback_changed':False,
      'full_suite':'NOT_RUN','protection_scope':'Existing service binding and Round36 snapshot/consulting tests',
      'source_hashes':integrity['after']}
(out/'acceptance.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({k:v for k,v in data.items() if k not in ('source_hashes','final_binding')},ensure_ascii=False))
