"""Compare frozen live samples with their Round18 reports, without waivers."""
import hashlib
import json
import argparse
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / 'artifacts/technology_pass_semantics'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--prefix', default='round19_final')
    parser.add_argument('--output', default='guards.json')
    args = parser.parse_args()
    engine_hash = hashlib.sha256((ROOT / 'backend/review_v2/engine.py').read_bytes()).hexdigest()
    result = {}
    names = ['patent_closed', 'cooperative_live', 'cross_article_live', 'patent_live',
             'consulting_live', 'provider_live', 'balanced_live', 'ancillary_live',
             'entrusted', 'prior_patent', 'transfer']
    for name in names:
        current = json.loads((ART / (args.prefix + '_' + name) / 'report.json').read_text(encoding='utf8'))
        old_dir = 'round18_final6' if name == 'patent_closed' else 'round18_final6_' + name
        old = json.loads((ART / old_dir / 'report.json').read_text(encoding='utf8'))
        before = {row['risk_group'] for row in old['risk_findings']}
        after = {row['risk_group'] for row in current['risk_findings']}
        result[name] = dict(gate=current['release_quality_gate']['status'],
                            failures=current['release_quality_gate']['failures'],
                            risk_groups_added=sorted(after-before), risk_groups_removed=sorted(before-after),
                            process_id=current['production_path_trace']['process_id'],
                            engine_hash_matches=current['production_path_trace']['runtime_sources']['engine']['sha256'] == engine_hash)
    (ART / 'round19_secret_diagnosis' / args.output).write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf8')
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
