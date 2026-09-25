"""Normal upload acceptance of final code; preserve every blocked report."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
from docx import Document

ROOT=Path(__file__).resolve().parents[1]
ART=ROOT/'artifacts/technology_pass_semantics'
PREFIX=os.environ.get('ROUND8_LIVE_PREFIX','round8_close')
cases=[
    ('patent',ART/'round6_patent/original.docx','sale','接受方'),
    ('guard',ROOT/'test_data/122 测试2.docx','technology','甲方'),
    ('consulting',ART/'round8_consulting_final/original.docx','technology','甲方'),
    ('industrial',ART/'round6_industrial/original.docx','service','甲方'),
]
for path in (ART/'round8_close_before').glob('*.json'):
    captured=json.loads(path.read_text(encoding='utf8'))
    test=captured['test_id']
    if 'balance_is_directional' in test:
        # This test runs both the baseline adverse and the balanced input.
        if '双方对在履行中取得' not in captured['raw_input']:
            continue
        name,party='balanced','甲方/被许可方'
    elif 'cross_article' in test:
        name,party='cross_article','甲方/被许可方'
    elif 'over_scope' in test:
        name,party='over_scope','甲方/被许可方'
    elif 'ancillary' in test:
        name,party='ancillary','甲方/技术秘密受让方'
    elif 'provider_does' in test:
        name,party='provider','甲方'
    else:
        continue
    folder=ART/('round8_close_input_'+name);folder.mkdir(exist_ok=True)
    source=folder/'original.docx'
    doc=Document()
    for line in captured['raw_input'].splitlines(): doc.add_paragraph(line)
    doc.save(source)
    (folder/'provenance.json').write_text(json.dumps({'capture':str(path),'test_id':test,
        'raw_input_sha256':hashlib.sha256(captured['raw_input'].encode()).hexdigest()},ensure_ascii=False,indent=2),encoding='utf8')
    cases.append((name,source,'technology',party))
manifest=[]
for name,source,kind,party in cases:
    output=ART/(PREFIX+'_'+name+'_live')
    with (ART/(PREFIX+'_'+name+'_live.out')).open('w',encoding='utf8') as log:
        run=subprocess.run([sys.executable,'-X','utf8',str(ROOT/'scripts/run_technology_live_acceptance.py'),
            str(source),str(output),'--user-id','1','--contract-type',kind,'--use-llm','false','--user-identity',party],
            cwd=ROOT,stdout=log,stderr=subprocess.STDOUT)
    row={'sample':name,'source':str(source),'exit_code':run.returncode}
    report_path=output/'report.json'
    if report_path.exists():
        report=json.loads(report_path.read_text(encoding='utf8'))
        row.update(gate=report['release_quality_gate'],runtime=report.get('production_path_trace'),report=str(report_path))
    else:
        row['gate']={'status':'NOT_VERIFIED'}
    manifest.append(row)
    (ART/(PREFIX+'_live_manifest.json')).write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf8')
    print(name,row['gate']['status'],flush=True)
