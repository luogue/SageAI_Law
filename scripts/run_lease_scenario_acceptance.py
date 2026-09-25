"""Repeat the real multipart route in an isolated authenticated test app."""
import hashlib
import json
import sys
import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/lease_scenario_evidence'
sys.path.insert(0, str(ROOT / 'backend'))
from dotenv import load_dotenv
load_dotenv(ROOT / 'backend/.env')
from fastapi import FastAPI
from fastapi.testclient import TestClient
from routers import review_v2 as route
from review_v2.lease_semantics import supports


def main():
    global OUT
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, default=OUT)
    parser.add_argument('--expect-released', action='store_true')
    args = parser.parse_args()
    OUT = args.output.resolve()
    OUT.mkdir(parents=True, exist_ok=True)
    app = FastAPI()
    app.include_router(route.router)
    app.dependency_overrides[route.get_current_user] = lambda: 1
    path = ROOT / 'test_data/53 租赁合同.docx'
    results = []
    with TestClient(app) as client:
        for n in (1, 2):
            response = client.post('/review-v2/file', data={'contract_type': 'lease', 'use_llm': 'true'},
                files={'file': (path.name, path.read_bytes(), 'application/vnd.openxmlformats-officedocument.wordprocessingml.document')})
            response.raise_for_status()
            r = response.json()
            (OUT / f'run-{n}.json').write_text(json.dumps(r, ensure_ascii=False, indent=2), encoding='utf-8')
            results.append(r)
            print(n, r['coverage_summary'], flush=True)
    a, b = results
    core = lambda r: [(i['node_id'], i['coverage_status'], i['rule_evidence_package']) for i in r['items']]
    checks = {
        'release_policy_matches': (
            b['release_quality_gate']['status'] == 'REPORT_READY' and not b.get('release_hold', {}).get('active')
            if args.expect_released else
            b['release_quality_gate']['status'] == 'BLOCKED' and b['release_hold']['active']
        ),
        'coverage_and_evidence_deterministic': core(a) == core(b),
        'risk_summary_deterministic': all(a[k] == b[k] for k in ('risk_theme_summary', 'risk_theme_severity_summary')),
        'no_null_evidence_ids': '[None]' not in b['result'] and '证据ID：None' not in b['result'],
        'all_actionable_children': b['recommendation_children_gate']['status'] == 'REPORT_READY',
        'repair_scope_missing': next(i for i in b['items'] if i['node_id'] == 'reasonable_repair_cost')['coverage_status'] == '缺失',
        'deadline_and_preemption_pass': all(i['coverage_status'] == '通过' for i in b['items'] if i['node_id'] in {'deposit_return_deadline', 'sale_notice_preemption'}),
        'no_foreign_narrative': all(t not in b['result'] for t in ('下架', '出卖人追偿', '替换成本')),
    }
    target_items = [i for i in b['items'] if i['node_id'] in {'force_majeure', 'early_surrender'}]
    checks['displayed_evidence_proves_target_elements'] = all(
        any(supports(spec, {**row, 'text': row['quoted_text']})
            for row in item['rule_evidence_package']['items'])
        for item in target_items
        for spec in item['decision_trace']['semantic_requirements']
        if next(e for e in item['coverage_elements'] if e['element_id'] == spec['element_id'])['status'] == 'COVERED')
    early = next(i for i in target_items if i['node_id'] == 'early_surrender')
    checks['exit_condition_and_consequence_displayed'] = early['coverage_status'] == '通过' and any(
        '提前30日' in row['quoted_text'] and '两个月房屋租金' in row['quoted_text'] and '76,000元' in row['quoted_text']
        for row in early['rule_evidence_package']['items'])
    before_path = OUT / 'before.json'
    before = json.loads(before_path.read_text(encoding='utf-8')) if before_path.exists() else a
    audit_rows = b.get('observability', {}).get('default_law_debug_table', [])
    audit_columns = ('rule_id', 'target_element', 'legal_basis', 'direct_match', 'role_match',
        'scenario_match', 'legal_effect_match', 'statutory_fallback', 'actual_legal_exposure')
    audit = [{column: row.get(column) for column in audit_columns} for row in audit_rows]
    (OUT / 'statutory_fallback_audit.json').write_text(
        json.dumps(audit, ensure_ascii=False, indent=2), encoding='utf-8')
    header = '| ' + ' | '.join(audit_columns) + ' |\n'
    divider = '| ' + ' | '.join('---' for _ in audit_columns) + ' |\n'
    body = ''.join('| ' + ' | '.join(str(row.get(column, '')).replace('|', '\\|').replace('\n', ' ')
        for column in audit_columns) + ' |\n' for row in audit)
    (OUT / 'statutory_fallback_audit.md').write_text(header + divider + body, encoding='utf-8')
    validation = {'checks': checks, 'input_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
        'before_coverage': before['coverage_summary'], 'after_coverage': b['coverage_summary'],
        'release_quality_gate': b['release_quality_gate'], 'technical_quality_gate': b.get('technical_quality_gate', b['release_quality_gate']),
        'transport': 'real multipart router via isolated TestClient; test-only auth override; browser not refreshed'}
    (OUT / 'validation.json').write_text(json.dumps(validation, ensure_ascii=False, indent=2), encoding='utf-8')
    if args.expect_released:
        (OUT / 'acceptance.json').write_text(json.dumps({
            'release_quality_gate': 'PASSED' if all(checks.values()) else 'BLOCKED',
            'engine_quality_status': b['release_quality_gate']['status'],
            'checks': checks,
        }, ensure_ascii=False, indent=2), encoding='utf-8')
    (OUT / 'report.json').write_text(json.dumps(b, ensure_ascii=False, indent=2), encoding='utf-8')
    (OUT / 'report.md').write_text(b['result'], encoding='utf-8')
    print(json.dumps(validation, ensure_ascii=False), flush=True)
    assert all(checks.values()), checks


if __name__ == '__main__':
    main()
