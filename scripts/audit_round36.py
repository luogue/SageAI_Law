"""Record source/test integrity relative to the captured pre-change code."""
import ast
import hashlib
import json
import shutil
from pathlib import Path

root = Path(__file__).resolve().parents[1]
out = root/'artifacts/technology_pass_semantics/round36_consulting_snapshot'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()

def functions(p):
    tree = ast.parse(p.read_text(encoding='utf-8-sig'))
    return {n.name: ast.dump(n,include_attributes=False) for n in tree.body
            if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))}

changed = {}
protected = []
for before in (out/'baseline_source').glob('*.py'):
    after = root/'backend/review_v2'/before.name
    if sha(before) == sha(after):
        continue
    a,b = functions(before),functions(after)
    names = [n for n in a.keys()|b.keys() if a.get(n)!=b.get(n)]
    changed[str(after.relative_to(root))] = sorted(names)
    protected += [f'{before.name}:{n}' for n in names
                  if any(word in n.lower() for word in ('gate','verifier','verify','fallback'))]
changed['backend/review_v2/final_snapshot.py'] = 'NEW: immutable final snapshot / export authorization'
for path,old in [('backend/routers/review_v2.py','baseline_router.py'),
                 ('frontend/src/views/ContractReviewV2.vue','baseline_frontend.vue')]:
    if sha(root/path)!=sha(out/old):
        changed[path] = 'Review/export run binding'
changed['frontend/src/utils/api.js'] = 'Task id propagation and exported version verification'
old_tests = json.loads((out.parent/'round35_development_consumers/baseline_test_hashes.json').read_text(encoding='utf8'))
modified = [p for p,h in old_tests.items() if (root/p).exists() and sha(root/p)!=h]
removed = [p for p in old_tests if not (root/p).exists()]
assert not protected and not modified and not removed,(protected,modified,removed)
paths = [*list((root/'backend/review_v2').glob('*.py')),root/'backend/routers/review_v2.py',
         root/'frontend/src/views/ContractReviewV2.vue',root/'frontend/src/utils/api.js']
data = dict(changed_sources=changed,changed_gate_verifier_fallback_functions=protected,
            modified_existing_tests=modified,removed_existing_tests=removed,
            source_hashes={str(p.relative_to(root)):sha(p) for p in paths})
(out/'source_audit.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf8')
for path in changed:
    target=out/'final_source'/path
    target.parent.mkdir(parents=True,exist_ok=True)
    shutil.copy2(root/path,target)
print('Audited source functions; protected changes=0; existing test modifications/removals=0')
