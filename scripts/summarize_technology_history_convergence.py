"""Join completed regression identities and the live gate; never relabel FAIL as PASS."""
import argparse
from collections import Counter
import json
from pathlib import Path

from compare_review_regressions import read


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--baseline', nargs='+', type=Path, required=True)
    parser.add_argument('--current', nargs='+', type=Path, required=True)
    parser.add_argument('--secondary', type=Path, required=True)
    parser.add_argument('--triage', type=Path, required=True)
    parser.add_argument('--live', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    baseline, current = read(args.baseline), read(args.current)
    secondary = json.loads(args.secondary.read_text(encoding='utf8'))
    triage = json.loads(args.triage.read_text(encoding='utf8'))
    live = json.loads(args.live.read_text(encoding='utf8'))
    removed = sorted(baseline.keys() - current.keys())
    assert not removed, removed
    assert len(baseline) == 1054, 'Use the frozen 783/271 inventory, not a partial exploratory run.'
    recovered = [key for key in baseline if baseline[key]['status'] == 'FAIL' and current[key]['status'] == 'PASS']
    new_failures = [key for key in baseline if baseline[key]['status'] == 'PASS' and current[key]['status'] == 'FAIL']
    migrated = []
    for row in secondary['tests']:
        key = row['test_id']
        assert key in current
        migrated.append(dict(test_id=key, previous_bucket=row['category'],
            secondary_group=row['secondary_group'], current_status=current[key]['status'],
            current_assertion=current[key]['message']))
    actual_failures = sum(row['status'] == 'FAIL' for row in current.values())
    assert actual_failures == triage['total_failures']
    result = dict(
        baseline_counts=dict(Counter(row['status'] for row in baseline.values())),
        current_counts=dict(Counter(row['status'] for row in current.values())),
        historical_recovered=recovered, newly_failing=new_failures,
        added_tests={key: current[key] for key in current.keys() - baseline.keys()},
        removed_tests=removed, secondary_groups=secondary['groups'],
        secondary_method=secondary['method'], secondary_outcomes=migrated,
        remaining_first_failure_triage=triage['counts'],
        triage_caveat='Assertion-stage clusters are not proof that all failures share that causal module.',
        live_gate=live['release_quality_gate']['status'],
        live_gate_failures=live['release_quality_gate']['failures'],
        live_review_id=live.get('review_id'),
        live_runtime=live['production_path_trace']['process_id'],
    )
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf8')
    print(json.dumps(dict(counts=result['current_counts'], recovered=len(recovered),
        new_failures=len(new_failures), added=len(result['added_tests']),
        remaining_triage=triage['counts'], live_gate=result['live_gate']), ensure_ascii=False))


if __name__ == '__main__':
    main()
