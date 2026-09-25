"""Replay an unchanged document through multipart production routing/response model."""
import argparse
import hashlib
import io
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'backend'))


def run(source, output, use_llm):
    if use_llm:
        from dotenv import load_dotenv
        load_dotenv(ROOT / 'backend' / '.env')
    from fastapi import FastAPI
    from fastapi.testclient import TestClient
    from starlette.datastructures import UploadFile
    from routers import review_v2 as route
    from review_v2.clause_parser import strip_non_contract_tail
    from review_v2.engine import _is_checkpoint_applicable
    from review_v2.sale_contract_checklist import get_sale_checklist

    original = source.read_bytes()
    extracted = route.input_layer.extract_text_from_file(UploadFile(filename=source.name, file=io.BytesIO(original)))
    normalized = strip_non_contract_tail(extracted)
    app = FastAPI()
    app.include_router(route.router)
    app.dependency_overrides[route.get_current_user] = lambda: {'id': 'company-formation-acceptance'}
    with TestClient(app) as client:
        response = client.post('/review-v2/file', data={
            'contract_type': 'investment', 'include_low_risk': 'true', 'use_llm': str(use_llm).lower(),
            'profile_json': json.dumps({'user_identity': '个人租客/买方', 'contract_scenario': '商品买卖'}, ensure_ascii=False),
        }, files={'file': (source.name, original, 'application/vnd.openxmlformats-officedocument.wordprocessingml.document')})
        response.raise_for_status()
        result = response.json()
    audit = [{
        'node_id': checkpoint.node_id, 'applicable_if': checkpoint.applicable_if,
        'equity_scope': _is_checkpoint_applicable(normalized, checkpoint, result['contract_type']),
        'sale_trigger_only': _is_checkpoint_applicable(normalized, checkpoint, 'sale'),
    } for checkpoint in get_sale_checklist() if checkpoint.node_id.startswith('sale_')]
    summary = {
        'source': str(source.resolve()), 'sha256': hashlib.sha256(original).hexdigest(),
        'normalized_sha256': hashlib.sha256(normalized.encode()).hexdigest(),
        'extracted_length': len(extracted), 'normalized_length': len(normalized),
        'transport': 'FastAPI multipart /review-v2/file; production handler, input extraction and response model; isolated test authentication',
        'use_llm_requested': use_llm, 'llm_status': result.get('llm_status'),
        'contract_type': result['contract_type'], 'contract_type_name': result['contract_type_name'],
        'report_context': result['report_context'], 'perspective_resolution': result.get('perspective_resolution'),
        'release_quality_gate': result['release_quality_gate'],
        'production_path_trace': result.get('production_path_trace'),
        'loaded_rules': [i['node_id'] for i in result['items']],
        'sale_rule_count': sum(i['node_id'].startswith('sale_') for i in result['items']),
        'conditional_sale_audit': audit,
    }
    output.mkdir(parents=True, exist_ok=True)
    for name, content in [('result.json', result), ('summary.json', summary)]:
        (output / name).write_text(json.dumps(content, ensure_ascii=False, indent=2), encoding='utf-8')
    (output / 'normalized_input.txt').write_text(normalized, encoding='utf-8')
    (output / 'report.md').write_text(result['result'], encoding='utf-8')
    assert source.read_bytes() == original
    assert result['contract_type'] == 'shareholders'
    assert summary['sale_rule_count'] == 0
    assert all(not r['sale_trigger_only'][0] for r in audit if r['node_id'].startswith('sale_trial_'))
    assert '交货时间' not in result['result']
    assert result['release_quality_gate']['status'] == 'REPORT_READY', result['release_quality_gate']['failures']
    print(json.dumps({k: summary[k] for k in ('contract_type', 'report_context', 'sha256', 'sale_rule_count')}, ensure_ascii=False))
    print('release_quality_gate=REPORT_READY')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, default=ROOT / 'test_data' / '83 投资协议.docx')
    parser.add_argument('--output', type=Path, default=ROOT / 'artifacts/company_formation/http')
    parser.add_argument('--use-llm', action='store_true')
    args = parser.parse_args()
    run(args.source, args.output, args.use_llm)
