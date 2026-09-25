"""Explicit live DeepSeek acceptance; isolated application DB, immutable DOCX inputs."""
import hashlib
import json
import sys
import time
from datetime import datetime
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / 'backend')]
from backend.test_database_bootstrap import install
install()
from review_v2 import engine
from review_v2.unified_facts import pipeline
from review_v2.deepseek_transport import request_json
from review_v2.fact_validation import FactExtractionError

OUT = ROOT / 'artifacts' / 'loan_verified_acceptance' / (datetime.now().strftime('%Y%m%d-%H%M%S') + '-' + '-'.join(sys.argv[1:] or ['all']))
OUT.mkdir(parents=True, exist_ok=True)
SOURCE_HASHES = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
    for p in sorted((ROOT / 'backend/review_v2/unified_facts').glob('*.py'))}


def docx_text(path):
    with zipfile.ZipFile(path) as z:
        root = ET.fromstring(z.read('word/document.xml'))
    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    return '\n'.join(''.join(t.text or '' for t in p.findall('.//w:t', ns)) for p in root.findall('.//w:p', ns))


def main():
    results = []
    for prefix in (sys.argv[1:] or ['72', '98', '101']):
        blind=prefix.startswith('blind-')
        path = ROOT/'artifacts/loan_blind_holdout'/f'{prefix}.json' if blind else next((ROOT / 'test_data').glob(prefix + ' *.docx'))
        if blind:
            manifest=json.loads((path.parent/'manifest.json').read_text(encoding='utf8'))
            expected_hash=next(r['sha256'] for r in manifest if r['id']==prefix)
            if hashlib.sha256(path.read_bytes()).hexdigest()!=expected_hash:
                raise RuntimeError('BLIND_HOLDOUT_CHANGED')
        target = OUT / prefix
        target.mkdir(exist_ok=True)
        calls = []
        def transport(system, payload, *, stage):
            n = len(calls) + 1
            print(f'{prefix} call={n} stage={stage} concepts={len(payload["active_concepts"])}', flush=True)
            started = time.monotonic()
            body, raw = request_json(system, payload, stage=stage)
            record = {'stage': stage, 'system_prompt': system, 'payload': payload, 'response': raw,
                'model': body.get('model'), 'usage': body.get('usage'), 'seconds': round(time.monotonic() - started, 2)}
            calls.append(record)
            (target / f'call-{n:02d}.json').write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding='utf8')
            print(f'{prefix} completed={n} seconds={record["seconds"]}', flush=True)
            return body, raw
        pipeline.request_json = transport
        source = json.loads(path.read_text(encoding='utf8'))['text'] if blind else docx_text(path)
        record = {'file': str(path), 'file_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
            'source_sha256': hashlib.sha256(source.encode()).hexdigest(), 'source_characters': len(source),
            'code_sha256': SOURCE_HASHES, 'sample_origin':'SEALED_DEEPSEEK_SYNTHETIC' if blind else 'EXISTING_DOCX'}
        try:
            result = engine.review_contract_v2(source, 'loan', use_llm=True)
            (target / 'report.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf8')
            (target / 'report.md').write_text(result['result'], encoding='utf8')
            record.update(status='PASS', gate=result['release_quality_gate'],
                coverage=result['coverage_summary'], rules=result['all_items_count'],
                active_concepts=result['structured_fact_debug']['active_concepts'])
        except Exception as exc:
            record.update(status='BLOCKED', error=type(exc).__name__ + ': ' + str(exc))
            if isinstance(exc, FactExtractionError):
                record.update(diagnostics=exc.diagnostics, attempts=exc.attempts)
        record['calls'] = len(calls)
        (target / 'result.json').write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding='utf8')
        results.append(record)
        print(json.dumps({k: record[k] for k in ('file', 'status', 'calls', 'error') if k in record}, ensure_ascii=False), flush=True)
    (OUT / 'summary.json').write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding='utf8')
    return 0 if all(r['status'] == 'PASS' for r in results) else 1


if __name__ == '__main__':
    raise SystemExit(main())
