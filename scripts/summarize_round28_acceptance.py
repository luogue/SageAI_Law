"""Freeze the final-source transfer review and compare the complete prior ledger."""
import ast
import difflib
import hashlib
import json
import re
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path
from compare_review_regressions import read
from summarize_round27_acceptance import comparison
from summarize_round22_acceptance import upload

ROOT=Path(__file__).resolve().parents[1]
ART=ROOT/'artifacts/technology_pass_semantics'
OUT=ART/'round28_secret_transfer_binding'
PRIOR=ART/'round27_consulting_binding'

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    result=dict(status='PENDING',current={},protection={},tests={},modified_files=[])
    result['original_gate_diagnostics']=json.loads((OUT/'before_diagnostics.json').read_text(encoding='utf-8'))
    for suite,previous,paths in (
        ('full',[PRIOR/f'full78_batch{i}.xml' for i in (0,1)],[OUT/f'full79_batch{i}.xml' for i in (0,1)]),
        ('focused',[PRIOR/'focused.xml'],[OUT/'focused.xml']),
        ('supplemental',[PRIOR/'supplemental.xml'],[OUT/'supplemental.xml']),
    ):
        result['tests'][suite]=comparison(read(previous),read(paths))
    targeted=read([OUT/'targeted.xml'])
    result['tests']['targeted']=dict(total=len(targeted),passed=sum(v['status']=='PASS' for v in targeted.values()),failed=sum(v['status']!='PASS' for v in targeted.values()))
    for party in ('transferor','transferee'):
        report,summary=upload(OUT/f'current_{party}/report.json')
        assert summary['contract_type']=='技术合同—技术转让合同—技术秘密转让合同'
        summary['rules']={}
        for item in report['items']:
            if item['item_id'] not in {'TC-01-03','TC-03-04','TC-06-01','TC-06-03','TC-11-01','TC-11-02','TC-11-04','TC-12-02','TC-12-03','TC-13-02'}:
                continue
            registry=item['decision_trace']['contract_fact_registry_consumption']['facts']
            bindings=[]
            for e in item['coverage_elements']:
                if e['status']=='COVERED':
                    assert e.get('source_fact_key') and registry[e['source_fact_key']]['status']=='FOUND',(item['item_id'],e)
                    assert e.get('supporting_evidence'),(item['item_id'],e)
                    compact=lambda s:re.sub(r'\s+','',s or '')
                    fact=registry[e['source_fact_key']]
                    # Claim-response sources publish their canonical key on
                    # the owning element, rather than repeating it on each SRC
                    # row. Verify that path against the registry's own exact
                    # clause and span; an ownership tag alone is insufficient.
                    def canonical_source(s):
                        keys=s.get('canonical_fact_keys',[])
                        return (e['source_fact_key'] in keys if keys else
                                s['clause_id'] in fact.get('source_clause_ids',[]) and
                                compact(s.get('quote')) in {compact(q) for q in fact.get('source_spans',[])})
                    direct=[s for s in item['evidence_clauses'] if e['element_id'] in s.get('supports_element_ids',[])
                            and canonical_source(s)
                            and any(s['clause_id']==f['clause_id'] and compact(s.get('quote'))==compact(f['quote']) for f in e['supporting_evidence'])]
                    assert direct and all(s['verified_original'] and s['support_type']=='DIRECT' for s in direct),(item['item_id'],e['element_id'])
                    for s in direct:
                        ref=s['source_ref']
                        assert s['raw_text'][ref['local_start']:ref['local_end']]==s['quote']
                        assert s['source_verification']['status']=='PASS'
                    bindings.append(dict(element_key=e['element_id'],canonical_fact_key=e['source_fact_key'],sources=[dict(evidence_id=s['evidence_id'],clause_id=s['clause_id'],quote=s['quote'],span=s['source_span']) for s in direct]))
                elif e['status']=='MISSING':
                    assert not e.get('supporting_evidence'),(item['item_id'],e)
            summary['rules'][item['item_id']]=dict(status=item['coverage_status'],elements={e['element_id']:e['status'] for e in item['coverage_elements']},bindings=bindings,narrative=item['risk_point_description'])
        result['current'][party]=summary
    for path in sorted(ART.glob('round28_accepted_*/report.json')):
        report,summary=upload(path)
        name=path.parent.name.removeprefix('round28_accepted_')
        prior_path=(PRIOR/f'current_{name.removeprefix("consulting_")}/report.json' if name in {'consulting_client','consulting_provider'} else ART/f'round27_accepted_{name}/report.json')
        prior=json.loads(prior_path.read_text(encoding='utf-8'))
        old={f['risk_group'] for f in prior['risk_findings']}
        new={f['risk_group'] for f in report['risk_findings']}
        summary.update(added_risk_groups=sorted(new-old),removed_risk_groups=sorted(old-new))
        result['protection'][name]=summary
    baseline=OUT/'baseline_source'
    frozen=json.loads((OUT/'full_start_source_hashes.json').read_text(encoding='utf-8'))
    result['source_hashes']={name:sha(ROOT/'backend/review_v2'/name) for name in frozen}
    assert result['source_hashes']==frozen
    assert not [name for name in frozen if (ROOT/'backend/review_v2'/name).stat().st_mtime>(OUT/'full_start_source_hashes.json').stat().st_mtime]
    result['source_unchanged_during_final_tests']=True
    result['fallback_code_deltas']=[]
    result['modified_gate_verifier_functions']=[]
    def functions(p):
        return {n.name:ast.dump(n,include_attributes=False) for n in ast.parse(p.read_text(encoding='utf-8-sig')).body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))}
    for name in frozen:
        p=ROOT/'backend/review_v2'/name
        prior=baseline/name
        if not prior.exists() or prior.read_bytes()!=p.read_bytes():
            result['modified_files'].append(str(p))
            old,new=(functions(prior) if prior.exists() else {}),functions(p)
            result['modified_gate_verifier_functions'] += [name+':'+k for k in old.keys() & new.keys() if old[k]!=new[k] and any(x in k for x in ('gate','verif','audit'))]
            result['fallback_code_deltas'] += [dict(file=name,line=line) for line in difflib.unified_diff(prior.read_text(encoding='utf-8-sig').splitlines() if prior.exists() else [],p.read_text(encoding='utf-8-sig').splitlines()) if line.startswith(('+','-')) and not line.startswith(('+++','---')) and 'fallback' in line.lower()]
    oldtests=json.loads((OUT/'baseline_test_hashes.json').read_text(encoding='utf-8-sig'))
    frozen_tests=json.loads((OUT/'full_start_test_hashes.json').read_text(encoding='utf-8'))
    assert all((ROOT/name).exists() and sha(ROOT/name)==digest for name,digest in oldtests.items())
    assert all(sha(ROOT/name)==digest for name,digest in frozen_tests.items())
    result['old_test_files']=dict(modified=[],removed=[],sha256=oldtests)
    result['test_artifact_provenance']={}
    for name in ('full79_batch0','full79_batch1','focused','supplemental','targeted'):
        path=OUT/(name+'.xml')
        suite=ET.parse(path).getroot().find('testsuite')
        assert path.stat().st_mtime>(OUT/'full_start_source_hashes.json').stat().st_mtime
        result['test_artifact_provenance'][name]=dict(sha256=sha(path),started_at=suite.get('timestamp'),tests=suite.get('tests'),duration_seconds=suite.get('time'),completed_at=datetime.fromtimestamp(path.stat().st_mtime,timezone.utc).isoformat())
    last_test=max((OUT/(n+'.xml')).stat().st_mtime for n in result['test_artifact_provenance'])
    replay=(OUT/'final_replay.out').read_text(encoding='utf-8-sig')
    for party,summary in result['current'].items():
        path=OUT/f'current_{party}/report.json'
        assert path.stat().st_mtime>last_test
        assert f'{party} HTTP=200 gate=REPORT_READY process={summary["process_id"]}' in replay
        summary.update(http_status=200,replayed_after_all_tests=True,report_sha256=sha(path))
    # Write a diagnostic draft before final assertions; never freeze a failed acceptance.
    (OUT/'acceptance.draft.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    assert len(result['protection'])==21
    assert all(not x['added_risk_groups'] and not x['removed_risk_groups'] for x in result['protection'].values())
    assert len({s['process_id'] for s in [*result['current'].values(),*result['protection'].values()]})==1
    assert not result['modified_gate_verifier_functions'] and not result['fallback_code_deltas']
    for suite in ('full','focused','supplemental'):
        x=result['tests'][suite]
        assert not x['newly_failing'] and not x['removed'] and not x['changed_status'],(suite,x)
        assert all(v=='PASS' for v in x['added'].values())
    assert result['tests']['full']['added_tests']==67
    assert result['tests']['targeted']==dict(total=67,passed=67,failed=0)
    result.update(status='ACCEPTED',finalized_at=datetime.now(timezone.utc).isoformat())
    dest=OUT/'acceptance.json'
    temp=OUT/'acceptance.tmp.json'
    temp.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    temp.replace(dest)
    (OUT/'acceptance.sha256').write_text(sha(dest)+'  acceptance.json\n',encoding='utf-8')
    print(json.dumps({k:result[k] for k in ('status','tests')},ensure_ascii=False,indent=2))

if __name__=='__main__':
    main()
