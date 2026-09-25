"""Record source provenance and original Gate evidence without altering reports."""
import ast,hashlib,json,shutil
from pathlib import Path
root=Path(__file__).resolve().parents[1]
out=root/'artifacts/technology_pass_semantics/round35_development_consumers'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf8'))
def save(name,data):(out/name).write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf8')
def functions(p):
 return {n.name:ast.dump(n,include_attributes=False) for n in ast.parse(p.read_text(encoding='utf-8-sig')).body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef))}
changed={}
protected=[]
for p in (root/'backend/review_v2').glob('*.py'):
 old=out/'baseline_source'/p.name
 if not old.exists() or sha(old)!=sha(p):
  oldfn=functions(old) if old.exists() else {}
  nowfn=functions(p)
  changed[str(p.relative_to(root))]=[k for k in nowfn if oldfn.get(k)!=nowfn[k]]
  if old.exists():
   protected += [k for k in nowfn if any(t in k.lower() for t in ('gate','verifier','fallback')) and k in oldfn and oldfn[k]!=nowfn[k]]
 else:
  continue
for path in changed:
 dest=out/'final_source'/Path(path).name
 dest.parent.mkdir(exist_ok=True)
 shutil.copy2(root/path,dest)
tests=read(out/'baseline_test_hashes.json')
removed=[p for p in tests if not (root/p).exists()]
modified=[p for p,v in tests.items() if (root/p).exists() and sha(root/p)!=v]
save('source_audit.json',{'changed_source_functions':changed,'changed_gate_verifier_fallback_functions':protected,
 'modified_existing_tests':modified,'removed_existing_tests':removed,
 'final_source_hashes':{p:sha(root/p) for p in changed},
 'frozen_round30_acceptance_sha256':sha(out.parent/'round30_transfer_roles/acceptance.json')})

print(json.dumps({'changed_files':list(changed),'changed_protected_functions':protected,'old_tests_modified':len(modified),'old_tests_removed':len(removed)},ensure_ascii=False))
