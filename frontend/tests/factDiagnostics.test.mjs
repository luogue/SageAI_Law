import test from 'node:test'
import assert from 'node:assert/strict'
import { createDiagnosticSession, saveFailure, readFailures } from '../src/utils/factDiagnostics.mjs'
const memory = () => { const data=new Map(); return {getItem:k=>data.get(k),setItem:(k,v)=>data.set(k,v)} }
const failure = (id) => ({task_id:id,trace_id:`trace-${id}`,diagnostics:[{field:'value'}],release_quality_gate:'BLOCKED'})
test('A fails, B upload clears A, B succeeds, A history remains restorable',()=>{
 const storage=memory(),key='test',ui=createDiagnosticSession(storage,key)
 const a=saveFailure(storage,key,failure('A'),'A.docx')[0]
 ui.show(a,ui.generation,true);assert.equal(ui.current.trace_id,'trace-A');assert.equal(ui.expanded,true)
 ui.reset();assert.equal(ui.current,null);assert.equal(ui.expanded,false)
 // A successful B has no failure to publish.
 assert.equal(createDiagnosticSession(storage,key).current,null)
 ui.restore(readFailures(storage,key)[0]);assert.equal(ui.current.filename,'A.docx');assert.equal(ui.expanded,false)
 ui.toggle();assert.equal(ui.expanded,true);ui.toggle();assert.equal(ui.expanded,false)
})
test('stale request cannot publish diagnostics into a replacement document',()=>{
 const ui=createDiagnosticSession(memory(),'test');const old=ui.generation;ui.reset()
 assert.equal(ui.show(failure('A'),old,true),false);assert.equal(ui.current,null)
})
test('retry clears old trace, displays only latest failure, success clears current only',()=>{
 const storage=memory(),ui=createDiagnosticSession(storage,'test')
 ui.show(saveFailure(storage,'test',failure('first'),'same.docx')[0],ui.generation,true)
 ui.reset();assert.equal(ui.current,null)
 ui.show(saveFailure(storage,'test',failure('second'),'same.docx')[0],ui.generation,true)
 assert.equal(ui.current.trace_id,'trace-second');ui.toggle();assert.equal(ui.expanded,false)
 ui.reset();assert.equal(ui.current,null);assert.equal(readFailures(storage,'test').length,2)
})
test('refresh restores only selected task, folded by default',()=>{
 const storage=memory(),ui=createDiagnosticSession(storage,'test');ui.show(failure('A'),ui.generation,true)
 const restored=createDiagnosticSession(storage,'test');assert.equal(restored.current.task_id,'A');assert.equal(restored.expanded,false)
})
test('saving new failure does not remove existing history',()=>{
 const storage=memory();for(let i=0;i<25;i++)saveFailure(storage,'test',failure(String(i)),`${i}.docx`)
 assert.equal(readFailures(storage,'test').length,25)
})

test('verification set diagnostics survive history restore with compact differences',()=>{
 const storage=memory(),key='batch';const d={validation_rule:'INCOMPLETE_FACT_VERIFICATION',batch_id:2,expected_count:20,actual_count:19,missing_fact_ids:['missing'],unexpected_fact_ids:[],duplicate_fact_ids:[],missing_facts:[{fact_concept:'job.position',value:'工程师',evidence:['原文']}]}
 saveFailure(storage,key,{...failure('A'),diagnostics:[d]},'A.docx')
 const ui=createDiagnosticSession(storage,key);ui.restore(readFailures(storage,key)[0])
 assert.deepEqual(ui.current.diagnostics[0],d)
})

test('scope difference diagnostics persist without the full schema list',()=>{
 const storage=memory(),key='scope';const d={validation_rule:'INCOMPLETE_VERIFICATION_SCOPE',field:'searched_concepts',expected_count:119,actual_count:118,missing_concepts:['worker.security_payment'],unexpected_concepts:[]}
 saveFailure(storage,key,{...failure('S'),diagnostics:[d]},'S.docx')
 assert.deepEqual(readFailures(storage,key)[0].diagnostics[0],d)
})
