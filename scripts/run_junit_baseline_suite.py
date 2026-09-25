"""Run every original baseline module, plus explicit new guards, in bounded workers."""
import argparse
import json
from pathlib import Path
import subprocess
import sys
import time
import xml.etree.ElementTree as ET


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--baseline', nargs='+', type=Path, required=True)
    p.add_argument('--add', nargs='*', type=Path, default=[])
    p.add_argument('--output-prefix', type=Path, required=True)
    p.add_argument('--workers', type=int, default=6)
    args = p.parse_args()
    root = Path(__file__).resolve().parents[1]
    costs = {}
    for path in args.baseline:
        for case in ET.parse(path).iter('testcase'):
            module = Path(case.get('classname').replace('.', '/') + '.py')
            if not (root / module).is_file():
                raise ValueError(f'Original module missing: {module}')
            costs[module] = costs.get(module, 0) + float(case.get('time', 0))
    for module in args.add:
        costs.setdefault(module, 1)
    batches = [[] for _ in range(args.workers)]
    weights = [0.] * args.workers
    for module in sorted(costs, key=costs.get, reverse=True):
        i = min(range(args.workers), key=weights.__getitem__)
        batches[i].append(module)
        weights[i] += costs[module]
    prefix = args.output_prefix.resolve()
    prefix.parent.mkdir(parents=True, exist_ok=True)
    handles, processes = [], []
    for i, modules in enumerate(batches):
        out = open(f'{prefix}_batch{i}.out', 'w', encoding='utf8')
        err = open(f'{prefix}_batch{i}.err', 'w', encoding='utf8')
        handles += [out, err]
        command = [sys.executable, '-X', 'utf8', '-m', 'pytest', *map(str, modules),
                   '-q', '--tb=short', f'--junitxml={prefix}_batch{i}.xml']
        processes.append(subprocess.Popen(command, cwd=root, stdout=out, stderr=err,
                         creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0)))
    manifest = {'modules': [[str(m) for m in b] for b in batches],
                'pids': [x.pid for x in processes], 'baseline': list(map(str, args.baseline))}
    Path(f'{prefix}_manifest.json').write_text(json.dumps(manifest, indent=2), encoding='utf8')
    print(json.dumps({'started': manifest['pids'], 'modules': len(costs)}), flush=True)
    while any(x.poll() is None for x in processes):
        time.sleep(2)
    for handle in handles:
        handle.close()
    print(json.dumps({'exit_codes': [x.returncode for x in processes]}), flush=True)


if __name__ == '__main__':
    main()
