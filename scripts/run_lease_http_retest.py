"""Capture two serialized HTTP upload responses in an isolated authenticated test app."""
import hashlib
import json
import sys
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/lease_http_retest'
sys.path.insert(0, str(ROOT / 'backend'))
from dotenv import load_dotenv
load_dotenv(ROOT / 'backend/.env')
from fastapi import FastAPI
from fastapi.testclient import TestClient
from routers import review_v2 as route
from review_v2.lease_semantics import PROFILES


def core(r):
    return {i['node_id']: [i['coverage_status'], sorted((e['element_id'], e['status'],
        e.get('source_locations', []), e.get('source_spans', [])) for e in i['coverage_elements'])]
        for i in r['items'] if i['node_id'] in PROFILES}


def main():
    app = FastAPI()
    app.include_router(route.router)
    app.dependency_overrides[route.get_current_user] = lambda: 1  # isolated test application only
    path = ROOT / 'test_data/53 租赁合同.docx'
    results = []
    with TestClient(app) as http:
        for index in (1, 2):
            response = http.post('/review-v2/file', data={'contract_type': 'lease', 'use_llm': 'true'},
                                 files={'file': (path.name, path.read_bytes(), 'application/vnd.openxmlformats-officedocument.wordprocessingml.document')})
            response.raise_for_status()
            r = response.json()
            (OUT / f'http-run-{index}.json').write_text(json.dumps(r, ensure_ascii=False, indent=2), encoding='utf-8')
            results.append(r)
            print(f'HTTP run {index}: {r["coverage_summary"]}', flush=True)
    a, r = results
    cases = {}
    for filename in ('regression.xml', 'http-regression.xml'):
        for case in ET.parse(OUT / filename).iter('testcase'):
            cases[(case.get('classname'), case.get('name'))] = case
    failed = [name for (_, name), c in cases.items() if c.find('failure') is not None or c.find('error') is not None]
    validation = {'release_quality_gate': r['release_quality_gate']['status'],
        'technical_quality_gate': r['technical_quality_gate']['status'], 'test_count': len(cases), 'failed_tests': failed,
        'core_evidence_equal': core(a) == core(r),
        'all_rule_states_equal': {i['node_id']: i['coverage_status'] for i in a['items']} == {i['node_id']: i['coverage_status'] for i in r['items']},
        'input_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
        'coverage': r['coverage_summary'], 'children_gate': r['recommendation_children_gate'],
        'transport': 'FastAPI TestClient: real multipart route and response model; test-only authentication override',
        'browser_refreshed': False}
    (OUT / 'report.json').write_text(json.dumps(r, ensure_ascii=False, indent=2), encoding='utf-8')
    (OUT / 'report.md').write_text(r['result'], encoding='utf-8')
    (OUT / 'validation.json').write_text(json.dumps(validation, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(validation, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
