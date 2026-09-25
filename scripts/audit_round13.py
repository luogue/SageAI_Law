"""Read-only acceptance audit: source identity, blocker lineage and test-ID diffs."""
import hashlib
import json
from pathlib import Path
from compare_review_regressions import read

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / 'artifacts/technology_pass_semantics'


def load(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def risk_inventory(report):
    return {f['risk_group']: dict(rules=sorted(f['source_review_ids']),
        missing=sorted({e['element_id'] for e in f['final_missing_elements']}),
        adverse=sorted({e['element_id'] for e in f['final_adverse_elements']}))
        for f in report['risk_findings']}


def comparison(prefix):
    old = read(sorted(ART.glob(prefix + '_batch*.xml')))
    new = read(sorted(ART.glob('full31_batch*.xml')))
    shared = old.keys() & new.keys()
    return dict(before={s: sum(v['status'] == s for v in old.values()) for s in ('PASS', 'FAIL', 'SKIP')},
        after={s: sum(v['status'] == s for v in new.values()) for s in ('PASS', 'FAIL', 'SKIP')},
        recovered=sorted(k for k in shared if old[k]['status'] == 'FAIL' and new[k]['status'] == 'PASS'),
        newly_failing={k: new[k]['message'] for k in sorted(shared) if old[k]['status'] == 'PASS' and new[k]['status'] == 'FAIL'},
        added={k: new[k]['status'] for k in sorted(new.keys()-old.keys())},
        removed=sorted(old.keys()-new.keys()))


def main():
    before = load(ART / 'round13_before/report.json')
    after = load(ART / 'round13_final_cooperative_live/report.json')
    previous = load(ART / 'round12_final_summary.json')
    by_rule = {i['item_id']: i for i in after['items']}
    old_by_rule = {i['item_id']: i for i in before['items']}
    groups = []
    for group in previous['remaining_confirmed_mapping_gaps']:
        rid = group['rule_id']
        rows = []
        for key in group['elements']:
            old = next(e for e in old_by_rule[rid]['coverage_elements'] if e['element_id'] == key)
            new = next(e for e in by_rule[rid]['coverage_elements'] if e['element_id'] == key)
            rows.append(dict(element_id=key, before=old['status'], after=new['status'],
                evidence=new['source_spans'], clauses=new['source_clause_ids'],
                residual=new.get('residual_gap'), source_fact_key=new.get('source_fact_key')))
        groups.append(dict(rule_id=rid, closed=all(r['after'] in {'COVERED','PARTIALLY_COVERED'} and r['evidence'] for r in rows), elements=rows))
    causes = [
        '法定共有默认规则被标为合同正向事实；移至法律背景，未约定的合同要素保留检索审计。',
        '第三方组件候选未完整适配精确要素；后续聚合只认完整覆盖，漏掉部分事实。保留选择/说明及待协商费用，侵权责任缺项独立判断。',
        '法律评价被当作合同风险事实要求原文绑定；分离法律背景和合同要素。',
        '同第一项：法定默认事实与合同缺失并存导致单调性冲突。',
        '同第三项的重复门禁输出，不重复计作根因。',
        '六个展开项：保密条件前缀被截断、一般责任上限例外误作泄密赔偿；进度正向事实未消费导致错误/空目标审计；保密例外真实残余被旧文案覆盖。',
        '现行合作开发报告注入固定旧法/年份；依据真实签署时间选择法律背景，删除固定年份推断。',
    ]
    blockers = [dict(original_index=n+1, original=f, expanded_count=len(f.get('details') or [f]),
                     root_cause=causes[n], remaining=after['release_quality_gate']['failures'])
                for n, f in enumerate(before['release_quality_gate']['failures'])]
    engine_hash = hashlib.sha256((ROOT/'backend/review_v2/engine.py').read_bytes()).hexdigest()
    protections = []
    for sample in load(ART/'round13_final_live_manifest.json'):
        if sample.get('status') == 'NOT_VERIFIED':
            protections.append(sample)
            continue
        name=sample['sample']
        r=load(Path(sample['report']))
        old=load(ART/f'round12_verified_{name}_live/report.json')
        old_risks,new_risks=risk_inventory(old),risk_inventory(r)
        protections.append(dict(sample=name, gate=r['release_quality_gate']['status'],
            failures=r['release_quality_gate']['failures'],
            engine_hash_matches=r['production_path_trace']['runtime_sources']['engine']['sha256']==engine_hash,
            process_id=r['production_path_trace']['process_id'],
            missing_risk_groups=sorted(old_risks.keys()-new_risks.keys()),
            changed_risk_elements={k:dict(before=old_risks[k],after=new_risks[k]) for k in old_risks.keys()&new_risks.keys() if old_risks[k]!=new_risks[k]}))
    out=dict(engine_hash=engine_hash, original_blockers=blockers,
        original_raw_count=len(blockers), original_expanded_count=sum(b['expanded_count'] for b in blockers),
        final_gate=after['release_quality_gate']['status'], final_raw_count=len(after['release_quality_gate']['failures']),
        final_expanded_count=sum(len(f.get('details') or [f]) for f in after['release_quality_gate']['failures']),
        mapping_groups=groups, samples=protections, new_tests=0, migrations=0,
        fixture_change=previous['fixture_change'])
    out['fixture_change']['current_upload_observations'] = dict(
        confidentiality_coverage=by_rule['TC-11-02']['coverage_status'],
        gate=after['release_quality_gate']['status'],
        exit_findings=sum('TC-05-04' in f['source_review_ids'] for f in after['risk_findings']))
    out['business_modules'] = {name: hashlib.sha256((ROOT/'backend/review_v2'/name).read_bytes()).hexdigest()
        for name in ('engine.py','cooperative_element_facts.py','confidentiality_remedies.py','development_exit.py')}
    out['risk_and_evidence_checks'] = {k:v for k,v in after['release_quality_gate']['gate_results'].items()
        if any(term in k for term in ('EVIDENCE','FACT','POLARITY','ELEMENT'))}
    if len(list(ART.glob('full31_batch*.xml')))==2:
        out['versus_918_250']=comparison('full29')
        out['versus_turn_start']=comparison('full30')
    (ART/'round13_final_summary.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf8')
    print(json.dumps({k:out[k] for k in ('final_gate','final_raw_count','final_expanded_count','new_tests','migrations')},ensure_ascii=False))
    for row in protections:
        print(row['sample'],row.get('gate') or row.get('status'),row.get('missing_risk_groups'),row.get('changed_risk_elements'))
    if 'versus_turn_start' in out:
        for key in ('versus_918_250','versus_turn_start'):
            c=out[key]
            print(key,c['after'],'recovered',c['recovered'],'new failures',c['newly_failing'])


if __name__ == '__main__':
    main()
