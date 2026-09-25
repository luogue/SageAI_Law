"""Replay a local test upload through the UI proxy and its real worker.

Uses the application's development-test identity; no dependency override,
diagnostic mode, verifier configuration change or credential logging.
"""
import argparse
import hashlib
import json
import os
import sys
from pathlib import Path

import requests
from dotenv import load_dotenv


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('source', type=Path)
    parser.add_argument('output', type=Path)
    parser.add_argument('--user-id', type=int, required=True)
    parser.add_argument('--use-llm', choices=('true', 'false'), default='true')
    parser.add_argument('--contract-type', default='technology',
                        help='Original request prior, not the expected output classification')
    parser.add_argument('--user-identity')
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    source, output = args.source.resolve(), args.output.resolve()
    sys.path.insert(0, str(root / 'backend'))
    os.chdir(root / 'backend')
    load_dotenv(root / 'backend' / '.env')
    from auth.utils import create_access_token
    token = create_access_token({'user_id': str(args.user_id)})
    form = {'contract_type': args.contract_type, 'use_llm': args.use_llm, 'include_low_risk': 'true'}
    if args.user_identity:
        form['profile_json'] = json.dumps({'user_identity': args.user_identity}, ensure_ascii=False)
    response = requests.post('http://localhost:5173/review-v2/file',
        headers={'Authorization': 'Bearer ' + token},
        data=form,
        files={'file': (source.name, source.read_bytes(),
                       'application/vnd.openxmlformats-officedocument.wordprocessingml.document')}, timeout=600)
    print('HTTP', response.status_code)
    response.raise_for_status()
    report = response.json()
    output.mkdir(parents=True, exist_ok=True)
    (output / 'report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf8')
    (output / 'report.md').write_text(report['result'], encoding='utf8')
    print('SOURCE_SHA256', hashlib.sha256(source.read_bytes()).hexdigest())
    print('RUNTIME', json.dumps(report.get('production_path_trace'), ensure_ascii=False))
    print('GATE', json.dumps(report['release_quality_gate'], ensure_ascii=False))
    assert report['release_quality_gate']['status'] == 'REPORT_READY'
    assert not report['release_quality_gate']['failures']


if __name__ == '__main__':
    main()
