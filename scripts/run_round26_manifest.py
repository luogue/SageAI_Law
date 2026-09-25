"""Run exact saved test identities without Windows command-line length limits."""
import json
import sys
from pathlib import Path

import pytest


if __name__ == '__main__':
    tests = json.loads(Path(sys.argv[1]).read_text(encoding='utf-8-sig'))
    raise SystemExit(pytest.main([*tests, '-q', '--tb=short', '--junitxml=' + sys.argv[2]]))
