import os
import shutil
import subprocess
from pathlib import Path

root=Path(__file__).resolve().parents[1]
out=root/'artifacts/technology_pass_semantics/round36_consulting_snapshot'
node=shutil.which('node')
assert node
flags=(subprocess.IDLE_PRIORITY_CLASS | subprocess.CREATE_NO_WINDOW) if os.name=='nt' else 0
with (out/'frontend_build.log').open('w',encoding='utf8') as log:
    result=subprocess.run([node,'node_modules/vite/bin/vite.js','build'],cwd=root/'frontend',
                          stdout=log,stderr=log,creationflags=flags)
assert result.returncode==0
with (out/'frontend_tests.log').open('w',encoding='utf8') as log:
    result=subprocess.run([node,'--test','tests/factDiagnostics.test.mjs','tests/finalSnapshotExport.test.mjs'],
                          cwd=root/'frontend',stdout=log,stderr=log,creationflags=flags)
assert result.returncode==0
print('Frontend production build PASS (single CPU, idle priority inherited)')
