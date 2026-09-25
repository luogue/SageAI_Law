"""Read-only pytest diagnostics for the original Round7 newly failing IDs."""
import functools
import hashlib
import json
import os
from pathlib import Path

import pytest

ART = Path(__file__).resolve().parents[1] / 'artifacts/technology_pass_semantics'
current_node = None


@pytest.hookimpl(tryfirst=True)
def pytest_runtest_setup(item):
    global current_node
    current_node = item.nodeid


def pytest_configure(config):
    from review_v2 import engine
    original = engine.review_contract_v2
    baseline = json.loads((ART / 'round7_comparison_final.json').read_text(encoding='utf8'))
    targets = {key.split('::')[0].replace('.', '/') + '.py::' + key.split('::', 1)[1]
               for key in baseline['newly_failing']}

    @functools.wraps(original)
    def capture(*a, **kw):
        output = original(*a, **kw)
        if (current_node in targets or os.environ.get('ROUND8_CAPTURE_ALL') == '1') and isinstance(output, dict):
            digest = hashlib.sha256((str(current_node) + str(a[0])).encode()).hexdigest()[:16]
            folder = ART / os.environ.get('ROUND8_CAPTURE_FOLDER', 'round8_original_outputs')
            folder.mkdir(exist_ok=True)
            (folder / (digest + '.json')).write_text(json.dumps(
                {'test_id': current_node, 'raw_input': a[0], 'report': output},
                ensure_ascii=False, indent=2), encoding='utf8')
        return output
    engine.review_contract_v2 = capture
