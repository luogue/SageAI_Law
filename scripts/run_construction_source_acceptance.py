"""Same construction source through the upload router, with immutable input hash."""
import sys,json,hashlib,io
from pathlib import Path
from types import SimpleNamespace
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'backend'))
from fastapi import FastAPI
from fastapi.testclient import TestClient
from routers import review_v2 as route
from layers.input_layer import InputLayer
source=next((ROOT/'test_data').glob('97 *.docx'))
app=FastAPI();app.include_router(route.router)
app.dependency_overrides[route.get_current_user]=lambda:1
with TestClient(app) as client:
 response=client.post('/review-v2/file',data={'contract_type':'construction','use_llm':'false'},files={'file':(source.name,source.read_bytes(),'application/vnd.openxmlformats-officedocument.wordprocessingml.document')})
 assert response.status_code==200,response.text
 result=response.json()
out=ROOT/'artifacts'/sys.argv[1];out.mkdir(parents=True,exist_ok=True)
text,diag=InputLayer().extract_text_with_diagnostics(SimpleNamespace(filename=source.name,file=io.BytesIO(source.read_bytes())))
(out/'report.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8')
(out/'report.md').write_text(result['result'],encoding='utf8')
(out/'source.txt').write_text(text,encoding='utf8')
print('SOURCE_SHA256',hashlib.sha256(source.read_bytes()).hexdigest())
for i in result['items']:
 if i['item_id'] in ('CE-01-01','CE-05-01','CE-05-03','CE-05-04'):
  print(i['item_id'],i['coverage_status'])
print(json.dumps(result['release_quality_gate'],ensure_ascii=False))
