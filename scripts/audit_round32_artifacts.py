"""Record source provenance and original Gate evidence without altering reports."""
import ast,hashlib,json,shutil
from pathlib import Path
root=Path(__file__).resolve().parents[1]
out=root/'artifacts/technology_pass_semantics/round32_patent_application_transfer'
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
before=read(out/'before_transferee/report.json')
rule=next(i for i in before['items'] if i['item_id']=='TC-03-03')
element=next(e for e in rule['coverage_elements'] if e['element_id']=='creator_named_identity')
evidence=next(e for e in rule['evidence_clauses'] if 'creator_named_identity' in (e.get('supporting_element_ids') or e.get('element_ids') or []))
failure=next(f for f in before['release_quality_gate']['failures'] if f['requirement']=='REVIEW_EVIDENCE_ELEMENT_MISMATCH')
save('original_mismatch_diagnostic.json',{'raw_gate_failure':failure,'raw_final_element':element,'raw_published_evidence':evidence,
 'rule_id':'TC-03-03','component_key':'creator_named_identity','final_status':element['status'],
 'canonical_fact_key':element.get('required_fact_key'),'canonical_fact_value':element.get('fact_value'),
 'evidence_id':evidence.get('evidence_id'),'clause_id':evidence.get('clause_id'),
 'span':evidence.get('source_span'),'source_ref':evidence.get('source_ref'),
 'quote':evidence.get('quote'),'support_type':evidence.get('support_type'),
 'expected_binding':'creator_named_identity -> technology.creator.named_identity -> same-clause DIRECT verified evidence ID and exact quote',
 'actual_binding':{'element_evidence_refs':element.get('evidence_ids'),'published_evidence_id':evidence.get('evidence_id'),
                   'source_fact_key':element.get('source_fact_key'),'supporting_evidence':element.get('supporting_evidence')},
 'root_cause':'Registry adapter emitted clause-ID-only element refs and omitted the typed source_fact_key/supporting_evidence consumed by final exact binding.'})
print(json.dumps({'changed_files':list(changed),'changed_protected_functions':protected,'old_tests_modified':len(modified),'old_tests_removed':len(removed)},ensure_ascii=False))
