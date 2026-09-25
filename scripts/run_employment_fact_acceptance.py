"""Capture real DeepSeek extraction, normalized facts and final business response."""
import argparse
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'backend'))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('source', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--replay-extraction', type=Path)
    parser.add_argument('--replay-verification', type=Path)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    from review_v2 import employment_fact_pipeline as pipeline
    original = pipeline.extract
    def captured(clauses, **kwargs):
        raw = (json.loads(args.replay_extraction.read_text(encoding='utf8'))
               if args.replay_extraction else original(clauses, **kwargs))
        (args.output / 'deepseek-raw.json').write_text(json.dumps(raw, ensure_ascii=False, indent=2), encoding='utf8')
        return raw
    pipeline.extract = captured
    original_verify = pipeline.verify
    def captured_verify(clauses, store):
        raw = (json.loads(args.replay_verification.read_text(encoding='utf8'))
               if args.replay_verification else original_verify(clauses,store))
        (args.output/'deepseek-verification.json').write_text(json.dumps(raw,ensure_ascii=False,indent=2),encoding='utf8')
        return raw
    pipeline.verify = captured_verify
    from fastapi import FastAPI
    from fastapi.testclient import TestClient
    from routers import review_v2 as route
    app = FastAPI()
    app.include_router(route.router)
    app.dependency_overrides[route.get_current_user] = lambda: {'id':'local-acceptance'}
    with TestClient(app) as client:
        response = client.post('/review-v2/file', data={'contract_type':'labor','include_low_risk':'true','use_llm':'false'},
            files={'file':(args.source.name,args.source.read_bytes(),'application/vnd.openxmlformats-officedocument.wordprocessingml.document')})
        if response.status_code != 200:
            (args.output / 'error.json').write_text(response.text,encoding='utf8')
            print(response.text[:1500])
        response.raise_for_status()
        result = response.json()
    (args.output / 'result.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf8')
    (args.output / 'report.md').write_text(result['result'],encoding='utf8')
    audit = {'source_sha256':hashlib.sha256(args.source.read_bytes()).hexdigest(),
             'transport':'FastAPI multipart business route', 'fresh_deepseek':not bool(args.replay_extraction),
             'gate':result['release_quality_gate'],
             'items':[{k:i.get(k) for k in ('item_id','coverage_status','coverage_elements')} for i in result['items']]}
    (args.output / 'acceptance.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2),encoding='utf8')
    print('GATE',result['release_quality_gate']['status'])


if __name__ == '__main__':
    main()
