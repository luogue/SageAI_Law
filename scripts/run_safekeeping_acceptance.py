import sys,json,hashlib,io
from pathlib import Path
from types import SimpleNamespace
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'backend'))
from fastapi import FastAPI
from fastapi.testclient import TestClient
from routers import review_v2 as route
from layers.input_layer import InputLayer
from review_v2.clause_parser import parse_contract_clauses
source=ROOT/'test_data/82 保管合同.docx'
app=FastAPI();app.include_router(route.router);app.dependency_overrides[route.get_current_user]=lambda:1
with TestClient(app) as client:
 response=client.post('/review-v2/file',data={'contract_type':'safekeeping','use_llm':'false'},files={'file':(source.name,source.read_bytes(),'application/vnd.openxmlformats-officedocument.wordprocessingml.document')})
 assert response.status_code==200,response.text
 r=response.json()
out=ROOT/'artifacts'/sys.argv[1];out.mkdir(parents=True,exist_ok=True)
text,diag=InputLayer().extract_text_with_diagnostics(SimpleNamespace(filename=source.name,file=io.BytesIO(source.read_bytes())))
clauses=parse_contract_clauses(text)
(out/'report.json').write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8')
(out/'report.md').write_text(r['result'],encoding='utf-8')
(out/'corpus.json').write_text(json.dumps({'file_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'text':text,'chunks':[c.to_public_dict() for c in clauses]},ensure_ascii=False,indent=2),encoding='utf-8')
targets={'D-04-04','D-08-01','D-08-03','D-07-02','D-01-03','D-02-03','D-04-03','D-07-01','D-09-03','D-12-04','COMMON-20-01'}
rows=[i for i in r['items'] if i['item_id'] in targets]
(out/'element-audit.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
for i in rows:print(i['item_id'],i['coverage_status'],[(e['proposition'],e['status']) for e in i['coverage_elements']])
print(r['release_quality_gate']['status'])
