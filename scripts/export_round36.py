"""Export exact final versions via the real authenticated API; reject old runs."""
import hashlib
import io
import json
import sqlite3
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(root/'backend'), str(root)]
from dotenv import load_dotenv
load_dotenv(root/'backend/.env')
from auth.utils import create_access_token
from docx import Document
import requests

out = root/'artifacts/technology_pass_semantics/round36_consulting_snapshot'
headers = {'Authorization':'Bearer '+create_access_token({'user_id':'1'})}
receipts = {}
for side in ('party_a','party_b'):
    folder = out/f'final_{side}'
    r = json.loads((folder/'report.json').read_text(encoding='utf8'))
    binding = r['final_review_snapshot']
    assert r['release_quality_gate']['status'] == 'REPORT_READY'
    for key in ('review_run_id','report_version','fact_snapshot_id','snapshot_hash'):
        assert r[key] == binding[key] == r['release_quality_gate'][key]
    receipts[side] = {}
    for format in ('docx','pdf'):
        response = requests.post('http://localhost:5173/review-v2/export-'+format,
            headers=headers, json={'final_review_snapshot':binding,'result':r['result'],
                                  'release_quality_gate':r['release_quality_gate']}, timeout=120)
        assert response.status_code == 200, response.text
        h = response.headers
        for key, name in [('review_run_id','X-Review-Run-Id'),('report_version','X-Report-Version'),
                          ('gate_version','X-Gate-Version'),('snapshot_hash','X-Snapshot-Hash')]:
            assert h[name] == binding[key]
        assert h['X-Export-Artifact-Hash'] == hashlib.sha256(response.content).hexdigest()
        (folder/f'export.{format}').write_bytes(response.content)
        if format == 'docx':
            from routers.review_v2 import _markdown_blocks, _strip_markdown_inline
            expected = [_strip_markdown_inline(b['text']) if b['type'] != 'separator' else ''
                        for b in _markdown_blocks(r['result'])]
            actual = [p.text for p in Document(io.BytesIO(response.content)).paragraphs]
            assert actual == expected, 'Exported DOCX is not the exact final report body'
        else:
            assert response.content.startswith(b'%PDF')
        receipts[side][format] = {k:v for k,v in h.items() if k.lower().startswith('x-')}
        receipts[side][format]['http_status'] = response.status_code
        with sqlite3.connect(root/'backend/data/review_snapshots.sqlite3') as db:
            stamp = db.execute('SELECT created_at FROM exports WHERE id=?',
                               (h['X-Export-Version'],)).fetchone()
        assert stamp
        receipts[side][format]['export_created_at'] = stamp[0]
    old = json.loads((out/f'intermediate_version_binding/final_{side}/report.json').read_text(encoding='utf8'))
    assert old['review_task_id'] == binding['review_task_id']
    bad_payloads = {
        'old_run': {'final_review_snapshot':old['final_review_snapshot']},
        'mixed_markdown': {'final_review_snapshot':binding,'result':'previous report'},
        'mixed_gate': {'final_review_snapshot':binding,'release_quality_gate':old['release_quality_gate']},
        'unversioned': {'result':r['result'],'release_quality_gate':{'status':'REPORT_READY'}},
    }
    receipts[side]['rejections'] = {}
    for name,payload in bad_payloads.items():
        response = requests.post('http://localhost:5173/review-v2/export-docx',headers=headers,json=payload,timeout=30)
        assert response.status_code == 409, (name,response.status_code)
        detail = response.json()['detail']
        assert detail['code'] == 'EXPORT_BLOCKED_STALE_REPORT'
        receipts[side]['rejections'][name] = detail
    print(side,'DOCX/PDF HTTP200; exact version/body verified; 4 stale cases HTTP409')
(out/'export_receipts.json').write_text(json.dumps(receipts,ensure_ascii=False,indent=2),encoding='utf8')
