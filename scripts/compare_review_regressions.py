"""Compare complete JUnit runs without hiding newly failing or removed tests."""
import argparse
import json
from pathlib import Path
import xml.etree.ElementTree as ET


def read(paths):
    rows = {}
    for path in paths:
        for case in ET.parse(path).iter('testcase'):
            key = case.get('classname') + '::' + case.get('name')
            if key in rows:
                raise ValueError('Duplicate test identity: ' + key)
            failure = case.find('failure')
            if failure is None:
                failure = case.find('error')
            rows[key] = {'status': 'FAIL' if failure is not None else
                         'SKIP' if case.find('skipped') is not None else 'PASS',
                         'message': failure.get('message', '') if failure is not None else ''}
    return rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--baseline', nargs='+', type=Path, required=True)
    parser.add_argument('--current', nargs='+', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    before, after = read(args.baseline), read(args.current)
    common = before.keys() & after.keys()
    changes = {key: {'before': before[key], 'after': after[key]} for key in sorted(common)
               if before[key]['status'] != after[key]['status']}
    result = {
        'baseline': {status: sum(row['status'] == status for row in before.values()) for status in ('PASS', 'FAIL', 'SKIP')},
        'current': {status: sum(row['status'] == status for row in after.values()) for status in ('PASS', 'FAIL', 'SKIP')},
        'recovered': [key for key in sorted(common) if before[key]['status'] == 'FAIL' and after[key]['status'] == 'PASS'],
        'newly_failing': [key for key in sorted(common) if before[key]['status'] == 'PASS' and after[key]['status'] == 'FAIL'],
        'added': {key: after[key] for key in sorted(after.keys() - before.keys())},
        'removed': sorted(before.keys() - after.keys()),
        'changes': changes,
    }
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf8')
    print(json.dumps({key: value if key in ('baseline', 'current') else len(value)
                      for key, value in result.items()}, ensure_ascii=False))


if __name__ == '__main__':
    main()
