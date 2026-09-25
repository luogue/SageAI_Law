"""Replay any employment DOCX through the real upload handler and retain diagnostics."""
import argparse
import asyncio
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'backend'))


async def run(args):
    from review_v2 import priority_contract_review
    actual_rule_inputs = {}
    actual_applicability_inputs = {}
    actual_element_inputs = {}
    original_judge = priority_contract_review.judge
    original_applicability = priority_contract_review.applicability
    def traced_applicability(text, checkpoint, contract_type):
        verdict = original_applicability(text, checkpoint, contract_type)
        actual_applicability_inputs[checkpoint.item_id] = {'corpus': text, 'verdict': verdict}
        return verdict
    def traced_judge(checkpoint, clauses, **kwargs):
        actual_rule_inputs[checkpoint.item_id] = [c.to_public_dict() for c in clauses]
        from review_v2.priority_checklist_helpers import PROFILES
        from review_v2.employment_facts import resolve_requirements
        from review_v2.lease_semantics import corpus_facts
        judgment = original_judge(checkpoint, clauses, **kwargs)
        if checkpoint.node_id in PROFILES:
            elements, conditions = resolve_requirements(checkpoint.node_id, PROFILES[checkpoint.node_id], clauses)
            actual_element_inputs[checkpoint.item_id] = {
                'corpus': '\n'.join(c.text for c in clauses),
                'element_queries': elements, 'conditions': conditions,
                'candidate_evidence': corpus_facts(clauses, elements),
                'judge_evidence': judgment.evidence_clauses if judgment else [],
            }
        return judgment
    priority_contract_review.judge = traced_judge
    priority_contract_review.applicability = traced_applicability
    from starlette.datastructures import UploadFile
    from routers.review_v2 import review_v2_file, ReviewV2PdfInput, _build_docx, _build_pdf
    if args.http:
        from fastapi import FastAPI
        from fastapi.testclient import TestClient
        from routers import review_v2 as route
        app = FastAPI()
        app.include_router(route.router)
        app.dependency_overrides[route.get_current_user] = lambda: {'id': 'local-acceptance'}
        with TestClient(app) as client:
            response = client.post('/review-v2/file', data={'contract_type': args.contract_type,
                'include_low_risk': 'true', 'use_llm': str(args.use_llm).lower()},
                files={'file': (args.source.name, args.source.read_bytes(), 'application/vnd.openxmlformats-officedocument.wordprocessingml.document')})
            response.raise_for_status()
            result = response.json()
    else:
        with args.source.open('rb') as stream:
            result = await review_v2_file(file=UploadFile(filename=args.source.name, file=stream),
                contract_type=args.contract_type, include_low_risk=True, use_llm=args.use_llm,
                profile_json='{}', current_user={'id': 'local-acceptance'})
    args.output.mkdir(parents=True, exist_ok=True)
    for row in result['items']:
        trace = actual_element_inputs.setdefault(row['item_id'], {})
        trace['final_evidence'] = row['evidence_clauses']
        trace['search_audits'] = row['decision_trace'].get('element_absence_searches', [])
        trace['negative_audit_condition'] = '适用要素在声明的检索范围内无正向匹配时记为 NOT_FOUND；FOUND 与要素证据不一致时由 SEARCH_AUDIT_ELEMENT_CONFLICT 门禁拦截。非强制要素的缺失不等于实际风险。'
    (args.output / 'actual_element_inputs.json').write_text(json.dumps(actual_element_inputs, ensure_ascii=False, indent=2), encoding='utf-8')
    (args.output / 'actual_rule_chunks.json').write_text(json.dumps(actual_rule_inputs, ensure_ascii=False, indent=2), encoding='utf-8')
    (args.output / 'actual_applicability_inputs.json').write_text(json.dumps(actual_applicability_inputs, ensure_ascii=False, indent=2), encoding='utf-8')
    from layers.input_layer import InputLayer
    from review_v2.clause_parser import strip_non_contract_tail
    with args.source.open('rb') as stream:
        normalized = strip_non_contract_tail(InputLayer().extract_text_from_file(UploadFile(filename=args.source.name, file=stream)))
    (args.output / 'normalized_input.txt').write_text(normalized, encoding='utf-8')
    (args.output / 'result.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    (args.output / 'report.md').write_text(result['result'], encoding='utf-8')
    payload = ReviewV2PdfInput(**result)
    (args.output / 'report.docx').write_bytes(_build_docx(payload))
    (args.output / 'report.pdf').write_bytes(_build_pdf(payload))
    summary = {
        'source': str(args.source.resolve()),
        'transport': 'FastAPI TestClient multipart, isolated test authentication' if args.http else 'direct production upload handler',
        'source_sha256': hashlib.sha256(args.source.read_bytes()).hexdigest(),
        'normalized_sha256': hashlib.sha256(normalized.encode('utf-8')).hexdigest(),
        'release_quality_gate': result['release_quality_gate'],
        'runtime_source_drift': result['production_path_trace']['runtime_source_drift']['status'],
        'reviews': [{
            'rule_id': row['item_id'], 'applicability': row['applicability'],
            'polarity': row['decision_trace'].get('review_polarity'),
            'actual_status': row['coverage_status'], 'reason': row['reasoning_summary'],
            'coverage_elements': row['coverage_elements'],
            'negative_clause_check': row['decision_trace'].get('negative_clause_check'),
            'element_absence_searches': row['decision_trace'].get('element_absence_searches', []),
            'evidence_clauses': row['evidence_clauses'],
            'termination_classification': row['decision_trace'].get('employment_exit_classification', []),
        } for row in result['items']],
    }
    states = {'通过': 'PASS', '部分覆盖': 'PARTIAL', '缺失': 'MISSING', '风险条款': 'RISK', '不适用': 'N/A'}
    lines = ['# 劳动合同逐项证据诊断', '', f"输入文件：{args.source.name}", f"输入 SHA256：{summary['source_sha256']}",
             f"normalized SHA256：{summary['normalized_sha256']}", '', '| rule_id | 最终状态 | 理由 |', '|---|---|---|']
    absent = []
    for row in summary['reviews']:
        lines.append(f"| {row['rule_id']} | {states.get(row['actual_status'], row['actual_status'])} | {row['reason']} |")
        absent.extend({'rule_id': row['rule_id'], **audit} for audit in row['element_absence_searches'] if audit.get('result') == 'NOT_FOUND')
    lines.extend(['', '## 全部 SEARCH_AUDIT NOT FOUND', '', '```json', json.dumps(absent, ensure_ascii=False, indent=2), '```'])
    for row in summary['reviews']:
        lines.extend(['', '## ' + row['rule_id'], '', '```json', json.dumps(row, ensure_ascii=False, indent=2), '```'])
    lines.extend(['', '## release_quality_gate', '', '```json', json.dumps(summary['release_quality_gate'], ensure_ascii=False, indent=2), '```'])
    (args.output / 'diagnostics.md').write_text('\n'.join(lines), encoding='utf-8')
    (args.output / 'not_found.json').write_text(json.dumps(absent, ensure_ascii=False, indent=2), encoding='utf-8')
    (args.output / 'summary.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({'status': result['release_quality_gate']['status'],
                      'failures': result['release_quality_gate']['failures'],
                      'output': str(args.output.resolve())}, ensure_ascii=False))
    return 0 if result['release_quality_gate']['status'] == 'REPORT_READY' else 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('--output', type=Path, default=ROOT / 'artifacts/employment_file_acceptance')
    parser.add_argument('--use-llm', action='store_true')
    parser.add_argument('--contract-type', default='labor')
    parser.add_argument('--http', action='store_true', help='Use multipart HTTP and the production response model in an isolated test app')
    raise SystemExit(asyncio.run(run(parser.parse_args())))
