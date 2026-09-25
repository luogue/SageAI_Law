"""Replay identical model output against pre-change and final source, sequentially."""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[1]
out = root / 'artifacts/technology_pass_semantics/round36_consulting_snapshot'
cases = {
    'entrusted': ('round14_entrusted_input', '甲方/委托方'),
    'granted_transferee': ('round33_patent_transfer_projection', '甲方/受让方'),
    'granted_transferor': ('round33_patent_transfer_projection', '乙方/让与方'),
    'application_transferee': ('round32_patent_application_transfer', '甲方/受让方'),
    'application_transferor': ('round32_patent_application_transfer', '乙方/让与方'),
    'secret_transferee': ('round31_transfer_consistency', '甲方/受让方'),
    'secret_transferor': ('round31_transfer_consistency', '乙方/让与方'),
    'secret_licensor': ('round29_secret_license_aggregation', '甲方/许可方'),
    'secret_licensee': ('round29_secret_license_aggregation', '乙方/被许可方'),
    'patent_licensor': ('round24_patent_consistency', '甲方/许可方'),
    'patent_licensee': ('round24_patent_consistency', '乙方/被许可方'),
    'cooperative_a': ('round34_cooperative_routing', '甲方'),
    'cooperative_b': ('round34_cooperative_routing', '乙方'),
    'service_client': ('round26_service_binding', '甲方/委托方'),
    'service_provider': ('round26_service_binding', '乙方/服务方'),
    'consulting_client': ('round27_consulting_binding', '甲方/委托方'),
    'consulting_provider': ('round27_consulting_binding', '乙方/咨询方'),
}
read = lambda p: json.loads(p.read_text(encoding='utf8'))
hashes = lambda: {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
                  for p in (root / 'backend/review_v2').glob('*.py')}
before = hashes()
progress = read(out / 'protection_progress.json')
results = {}
for name, diff in progress.items():
    if not (diff['added'] or diff['removed'] or diff['states']):
        continue
    round_name, role = cases[name]
    for mode in ('baseline', 'final'):
        with (out / f'{name}_fixed_{mode}.log').open('w', encoding='utf8') as log:
            subprocess.run([sys.executable, '-X', 'utf8', str(root/'scripts/check_round36_fixed_protection.py'),
                            mode, name, round_name, role], cwd=root, stdout=log,
                           stderr=subprocess.STDOUT, check=True)
    a = read(out / f'{name}_fixed_baseline.json')
    b = read(out / f'{name}_fixed_final.json')
    states = lambda r: {i['item_id']: i['coverage_status'] for i in r['items']}
    groups = lambda r: sorted(i['risk_group'] for i in r['risk_themes'])
    results[name] = {'states_equal': states(a)==states(b), 'risk_groups_equal': groups(a)==groups(b),
                     'gates': [a['release_quality_gate']['status'], b['release_quality_gate']['status']]}
    (out/'protection_controls.json').write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding='utf8')
    print(name, json.dumps(results[name], ensure_ascii=False), flush=True)
after = hashes()
assert before == after
(out/'protection_control_source_integrity.json').write_text(
    json.dumps({'before': before, 'after': after, 'unchanged': before==after}, indent=2), encoding='utf8')
