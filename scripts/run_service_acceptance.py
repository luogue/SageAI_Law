"""Exercise the actual upload route and publish each service decision/evidence."""
import json, sys
from pathlib import Path
from fastapi import FastAPI
from fastapi.testclient import TestClient
from routers import review_v2 as route

def main():
    app=FastAPI()
    app.include_router(route.router)
    app.dependency_overrides[route.get_current_user]=lambda:{'id':1}
    path=Path(sys.argv[1] if len(sys.argv)>1 else 'test_data/70 服务合同.docx')
    with TestClient(app) as http:
        response=http.post('/review-v2/file',data={'contract_type':sys.argv[3] if len(sys.argv)>3 else 'service','use_llm':'false'},files={'file':(path.name,path.read_bytes())})
    response.raise_for_status()
    result=response.json()
    out=Path(sys.argv[2] if len(sys.argv)>2 else 'artifacts/service_acceptance')
    out.mkdir(parents=True,exist_ok=True)
    (out/'report.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    (out/'report.md').write_text(result['result'],encoding='utf-8')
    audit=[]
    for item in result['items']:
        audit.append({key:item.get(key) for key in (
            'item_id','item_name','applicable','applicable_if','coverage_status',
            'action_priority','risk_level','coverage_elements','evidence_clauses',
            'evidence_package','decision_trace')})
    (out/'rule_audit.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2),encoding='utf-8')
    for i in result['items']:
        print(i['item_id'],i['coverage_status'],i['action_priority'])
    print(result['coverage_summary'])
    print(result['release_quality_gate']['status'],result['release_quality_gate']['failures'])

if __name__=='__main__':
    main()
