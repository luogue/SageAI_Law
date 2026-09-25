"""Read saved results without rerunning reviews or modifying source."""
import json, hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
ART=ROOT/'artifacts/technology_pass_semantics'
OUT=ART/'round30_transfer_roles'
def protection():
    result={}
    for path in sorted(ART.glob('round30_accepted_*/report.json')):
        if path.stat().st_mtime<(OUT/'validation_source_hashes.json').stat().st_mtime:continue
        r=json.loads(path.read_text(encoding='utf8'));name=path.parent.name.removeprefix('round30_accepted_')
        expected=hashlib.sha256((ROOT/'backend/review_v2/engine.py').read_bytes()).hexdigest()
        if r['production_path_trace']['runtime_sources']['engine']['sha256']!=expected:continue
        prior=(ART/'round29_secret_license_aggregation'/('current_licensor' if name=='frozen_licensor' else 'current_licensee')/'report.json' if name.startswith('frozen_') else ART/('round29_accepted_'+name)/'report.json')
        old=json.loads(prior.read_text(encoding='utf8'))
        groups=lambda p:{x['risk_group'] for x in p['risk_themes']}
        result[name]=dict(gate=r['release_quality_gate']['status'],raw=len(r['release_quality_gate']['failures']),added=sorted(groups(r)-groups(old)),removed=sorted(groups(old)-groups(r)),report=str(path),baseline=str(prior))
    return result
if __name__=='__main__':
    p=protection();(OUT/'protection_comparison.json').write_text(json.dumps(p,ensure_ascii=False,indent=2),encoding='utf8')
    print('completed',len(p),'ready',sum(x['gate']=='REPORT_READY' for x in p.values()))
    for n,x in p.items():
        if x['added'] or x['removed'] or x['raw']: print(n,{k:x[k] for k in ['gate','raw','added','removed']})
