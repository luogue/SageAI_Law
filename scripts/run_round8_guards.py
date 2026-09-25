"""Run original Round7 regressions and both directions of nonregression guards."""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / 'artifacts/technology_pass_semantics'
baseline = json.loads((ART / 'round7_comparison_final.json').read_text(encoding='utf8'))
ids = baseline['newly_failing'] + baseline['recovered']
ids = [v if isinstance(v, str) else v['test_id'] for v in ids]
nodes = [name.split('::', 1)[0].replace('.', '/') + '.py::' + name.split('::', 1)[1] for name in ids]
nodes += ['backend/tests/test_technology_verified_decision_boundary.py']
prefix = sys.argv[1] if len(sys.argv) > 1 else 'round8_guards'
with (ART / (prefix + '.out')).open('w', encoding='utf8') as stream:
    result = subprocess.run([sys.executable, '-X', 'utf8', '-m', 'pytest', *nodes,
                             '-q', '--tb=short', '--junitxml=' + str(ART / (prefix + '.xml'))],
                            cwd=ROOT, stdout=stream, stderr=subprocess.STDOUT)
print(result.returncode)
