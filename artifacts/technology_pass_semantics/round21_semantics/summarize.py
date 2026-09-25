"""Assert semantic acceptance independently of the release gate."""
import hashlib
import json
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path('F:/ai/Sage')
ART = ROOT / 'artifacts/technology_pass_semantics'
OUT = ART / 'round21_semantics'


def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def gate(report):
    actual = report['production_path_trace']['runtime_sources']['engine']['sha256']
    assert actual == hashlib.sha256((ROOT / 'backend/review_v2/engine.py').read_bytes()).hexdigest()
    g = report['release_quality_gate']
    checks = {k: v for k, v in g['gate_results'].items() if 'EVIDENCE' in k and 'MISMATCH' in k}
    result = dict(status=g['status'], raw_blockers=len(g['failures']),
                  expanded_blockers=sum(len(f.get('details') or f.get('mismatches') or [f]) for f in g['failures']),
                  evidence_mismatch_count=sum(v == 'FAIL' for v in checks.values()),
                  process_id=report['production_path_trace']['process_id'])
    assert result['status'] == 'REPORT_READY' and result['raw_blockers'] == result['expanded_blockers'] == result['evidence_mismatch_count'] == 0, result
    return result


def compare_subset(path):
    def tests(paths):
        return {c.get('classname') + '::' + c.get('name'): 'FAIL' if c.find('failure') is not None or c.find('error') is not None else 'SKIP' if c.find('skipped') is not None else 'PASS'
                for p in paths for c in ET.parse(p).iter('testcase')}
    before = tests((ART / 'round20_polarity').glob('full61_batch*.xml'))
    after = tests([path])
    result = dict(count=len(after), passed=sum(v == 'PASS' for v in after.values()),
                  failed=sum(v == 'FAIL' for v in after.values()),
                  newly_failing=[k for k, v in after.items() if v == 'FAIL' and before.get(k) == 'PASS'],
                  failures_without_baseline=[k for k, v in after.items() if v == 'FAIL' and k not in before],
                  recovered=[k for k, v in after.items() if v == 'PASS' and before.get(k) == 'FAIL'],
                  added=[k for k in after if k not in before])
    assert not result['newly_failing'], result['newly_failing']
    return result


def main():
    frozen = read(OUT / 'manifest.json')
    assert hashlib.sha256((ART / 'round19_secret_diagnosis/candidate_input/original.docx').read_bytes()).hexdigest() == frozen['current_contract_sha256']
    for path, digest in frozen['source_sha256'].items():
        assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == digest, path
    result = dict(current_contract={}, protections={})
    for party in ('licensee', 'licensor'):
        report = read(ART / f'round21_accepted_current_{party}/report.json')
        row = gate(report)
        items = {i['item_id']: i for i in report['items']}
        def elements(key):
            return {e['element_id']: e for e in items[key]['coverage_elements']}
        mode = elements('TC-07-01')['license_type']
        assert mode['status'] == 'COVERED' and any('普通使用许可' in s for s in mode['source_spans'])
        exceptions = elements('TC-11-02')['confidentiality_exceptions']
        states = {r['required_fact']: r['status'] for r in exceptions['component_coverage']}
        assert states == {'公开信息例外': 'COVERED', '合法取得信息例外': 'COVERED', '独立开发信息例外': 'MISSING', '依法披露例外': 'MISSING'}
        assert exceptions['search_targets'] == ['独立开发信息例外', '依法披露例外']
        assert exceptions['proposition'] == '已明确：公开信息例外、合法取得信息例外；未明确：独立开发信息例外、依法披露例外。'
        loss = elements('TC-12-03')
        assert loss['future_fee_after_secret_loss']['status'] == 'MISSING'
        assert loss['future_fee_after_secret_loss']['direction'] != 'ADVERSE'
        assert not loss['future_fee_after_secret_loss']['supporting_evidence']
        assert loss['secret_loss_trigger']['status'] == 'COVERED'
        assert '进入公共领域' not in loss['secret_loss_trigger']['proposition']
        assert '申请专利' not in loss['secret_loss_trigger']['proposition']
        triggers = {c['element_id']: c for c in loss['secret_loss_trigger']['component_coverage']}
        for key in ('licensor_active_disclosure', 'independent_research_disclosure', 'reverse_engineering_disclosure', 'partial_disclosure'):
            assert triggers[key]['status'] == 'COVERED'
            assert all(s['condition'] and s['event_polarity'] == 'CONDITIONAL' for s in triggers[key]['supporting_evidence'])
        assert items['TC-02-02']['coverage_status'] == '通过'
        assert not any(e['status'] == 'ADVERSE' for e in elements('TC-02-02').values())
        for key in ('litigation_handling', 'attorney_fee', 'litigation_cost'):
            assert elements('TC-12-02')[key]['status'] == 'MISSING'
        row.update(license_type=mode['status'], exception_components=states,
                   future_fee=loss['future_fee_after_secret_loss']['status'],
                   trigger_components={k: v['status'] for k, v in triggers.items()},
                   infringement_check=items['TC-02-02']['coverage_status'])
        result['current_contract'][party] = row
    names = ['cooperative_live', 'cross_article_live', 'patent_live', 'consulting_live', 'provider_live',
             'balanced_live', 'ancillary_live', 'patent_closed', 'entrusted', 'prior_patent', 'transfer']
    for name in names:
        path = ART / f'round21_accepted_{name}/report.json'
        assert path.exists(), name
        report = read(path)
        before = read(ART / f'round20_complete_{name}/report.json')
        row = gate(report)
        old = {f['risk_group'] for f in before['risk_findings']}
        new = {f['risk_group'] for f in report['risk_findings']}
        row.update(risk_groups_added=sorted(new-old), risk_groups_removed=sorted(old-new))
        assert not row['risk_groups_added'] and not row['risk_groups_removed'], (name, row)
        result['protections'][name] = row
    for name in ('focused8',):
        path = OUT / (name + '.xml')
        if path.exists():
            result[name] = compare_subset(path)
    path = OUT / 'full64_comparison.json'
    if path.exists():
        result['full_regression'] = read(path)
        assert not result['full_regression']['newly_failing'] and not result['full_regression']['removed']
        assert all(v['status'] == 'PASS' for v in result['full_regression']['added'].values())
    path = OUT / 'supplemental_comparison4.json'
    if path.exists():
        result['supplemental_legacy_modules'] = read(path)
        assert not result['supplemental_legacy_modules']['changes']
        assert not result['supplemental_legacy_modules']['added']
        assert not result['supplemental_legacy_modules']['removed']
    (OUT / 'acceptance.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({k: len(v) if k in ('current_contract', 'protections') else v for k, v in result.items() if k != 'full_regression'}, ensure_ascii=False))


if __name__ == '__main__':
    main()
