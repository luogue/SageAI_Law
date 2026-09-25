const fs=require('fs'),path=require('path'),assert=require('assert'),crypto=require('crypto');
const art='F:/ai/Sage/artifacts/technology_pass_semantics',out=path.join(art,'round25_candidate_scope');
const read=p=>JSON.parse(fs.readFileSync(p,'utf8').replace(/^\uFEFF/,''));
const gate=r=>{const g=r.release_quality_gate;assert.equal(g.status,'REPORT_READY');assert.equal(g.failures.length,0);for(const k of ['RISK_EVIDENCE_MISMATCH','REVIEW_EVIDENCE_ELEMENT_MISMATCH'])assert.equal(g.gate_results[k],'PASS');assert.equal(r.production_path_trace.process_id,17548);return {gate:g.status,raw_blockers:0,expanded_blockers:0,evidence_mismatch:0}};
const result={current:{},guards:{}};
for(const party of ['licensor','licensee']){
 const r=read(path.join(out,`current_${party}/report.json`)),old=read(path.join(art,`round24_patent_consistency/current_${party}/report.json`));
 const states=x=>Object.fromEntries(x.items.filter(i=>/^(TC-07|TC-11|TC-12)/.test(i.item_id)).map(i=>[i.item_id,[i.coverage_status,Object.fromEntries(i.coverage_elements.map(e=>[e.element_id,e.status]))]]));assert.deepStrictEqual(states(r),states(old));
 const item=r.items.find(i=>i.item_id==='TC-07-01'),e=item.coverage_elements.find(e=>e.element_id==='permitted_implementation_acts');
 assert.equal(e.status,'COVERED');const bound=item.evidence_clauses.filter(s=>e.evidence_ids.includes(s.evidence_id));assert.equal(bound.length,e.evidence_ids.length);assert.equal(bound.length,5);
 for(const s of bound){assert(s.verified_original);assert.equal(s.source_verification.status,'PASS');assert(s.supports_element_ids.includes(e.element_id));assert(!/支付|付款|费用|违约金|结算/.test(s.quote));assert.equal(s.source_span.raw_text,s.quote)}
 const fact=item.decision_trace.contract_fact_registry_consumption.facts[e.source_fact_key];assert.deepStrictEqual([...fact.source_spans].sort(),[...e.source_spans].sort());assert.deepStrictEqual([...fact.source_spans].sort(),bound.map(s=>s.quote).sort());
 result.current[party]={...gate(r),scope:item.coverage_status,implementation:e.status,related_state_changes:0,evidence:bound.map(s=>({quote:s.quote,location:s.location,evidence_id:s.evidence_id}))};
}
for(const name of fs.readdirSync(art).filter(n=>n.startsWith('round25_accepted_'))){const r=read(path.join(art,name,'report.json')),old=read(path.join(art,name.replace('round25_','round24_'),'report.json'));const groups=x=>[...new Set(x.risk_findings.map(f=>f.risk_group))].sort();assert.deepStrictEqual(groups(r),groups(old));result.guards[name]={...gate(r),risk_group_changes:0}}
assert.equal(Object.keys(result.guards).length,15);fs.writeFileSync(path.join(out,'live_acceptance.json'),JSON.stringify(result,null,2));
const manifest=read(path.join(out,'run_manifest.json'));manifest.backend_pid=17548;for(const f of Object.keys(manifest.source_hashes))manifest.source_hashes[f]=crypto.createHash('sha256').update(fs.readFileSync(path.join('F:/ai/Sage/backend/review_v2',f))).digest('hex');fs.writeFileSync(path.join(out,'run_manifest.json'),JSON.stringify(manifest,null,2));
console.log('Final source: both parties consistent; 15 guards unchanged; all 17 READY, blockers/mismatch=0.');