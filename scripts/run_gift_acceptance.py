"""Production multipart gift report, including all 48 applicability/evidence rows."""
import json
from pathlib import Path
from fastapi import FastAPI
from fastapi.testclient import TestClient
from routers import review_v2 as route

def main():
    app = FastAPI()
    app.include_router(route.router)
    app.dependency_overrides[route.get_current_user] = lambda: {'id': 1}
    path = Path('test_data/65 赠与合同.docx')
    with TestClient(app) as http:
        response = http.post('/review-v2/file', data={'contract_type':'gift','use_llm':'false'},
                             files={'file': (path.name, path.read_bytes())})
    response.raise_for_status()
    result = response.json()
    out = Path('artifacts/gift_acceptance')
    out.mkdir(parents=True, exist_ok=True)
    (out/'report.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    (out/'report.md').write_text(result['result'],encoding='utf-8')
    rows = [{k:i.get(k) for k in ['item_id','applicability','evidence_clauses',
            'rule_evidence_package','coverage_status','risk_level','action_priority','reasoning_summary']}
            for i in result['items']]
    (out/'all_rules.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
    for row in rows:
        print(row['item_id'],row['coverage_status'],row['risk_level'],row['action_priority'])
    print('SUMMARY',result['coverage_summary'])
    print('GATE',json.dumps(result['release_quality_gate'],ensure_ascii=False))

if __name__ == '__main__':
    main()
