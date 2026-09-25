"""Exact candidate identity checks, shared by transport batches and final commit."""
from collections import Counter
from review_v2.fact_validation import FactExtractionError

def check_ids(facts, checks, batch_id=None):
    expected={f['fact_id']:f for f in facts}
    ids=[c.get('fact_id') for c in checks if isinstance(c,dict) and isinstance(c.get('fact_id'),str)] if isinstance(checks,list) else []
    counts=Counter(ids)
    missing=sorted(set(expected)-set(ids));unexpected=sorted(set(ids)-set(expected),key=str)
    duplicate=[k for k,v in counts.items() if v>1]
    if missing or unexpected or duplicate or not isinstance(checks,list) or len(ids)!=len(checks):
        detail={'failed_stage':'VERIFICATION_SCHEMA','field':'checks.fact_id','validation_rule':'INCOMPLETE_FACT_VERIFICATION',
            'batch_id':batch_id,'expected_count':len(facts),'actual_count':len(ids),
            'missing_fact_ids':missing,'unexpected_fact_ids':unexpected,'duplicate_fact_ids':duplicate,
            'missing_facts':[{'fact_id':k,'fact_concept':expected[k]['concept'],'value':expected[k].get('normalized_value',expected[k].get('value')),'evidence':expected[k]['evidence']} for k in missing],
            'expected':len(facts),'actual':len(ids),'model_raw_value':{'missing':missing,'unexpected':unexpected,'duplicate':duplicate},
            'message':'核验结果必须与当前批次候选事实一一对应；历史诊断中的事实ID不得作为当前候选。','disposition':'BLOCK'}
        raise FactExtractionError('INCOMPLETE_FACT_VERIFICATION',diagnostics=[detail])

def batches(facts, size=20):
    ordered=sorted(facts,key=lambda f:f['fact_id'])
    return [ordered[i:i+size] for i in range(0,len(ordered),size)] or [[]]


def check_scope(required, actual, batch_id=None):
    values=actual if isinstance(actual,list) and all(isinstance(v,str) for v in actual) else []
    missing=sorted(set(required)-set(values));unexpected=sorted(set(values)-set(required))
    if missing or unexpected or not isinstance(actual,list) or len(values)!=len(actual):
        raise FactExtractionError('INCOMPLETE_VERIFICATION_SCOPE',diagnostics=[{
            'failed_stage':'VERIFICATION_SCHEMA','field':'searched_concepts','validation_rule':'INCOMPLETE_VERIFICATION_SCOPE',
            'batch_id':batch_id,'expected_count':len(set(required)),'actual_count':len(set(values)),
            'missing_concepts':missing,'unexpected_concepts':unexpected,'expected':len(set(required)),'actual':len(set(values)),
            'model_raw_value':{'missing_concepts':missing,'unexpected_concepts':unexpected},
            'message':'本批负责的概念必须全部经全文检索；未抽到事实也不能省略搜索声明。','disposition':'BLOCK'}])

def plan_scope(required, facts, concept_size=20, fact_size=20):
    """Schema-driven partitions include concepts with zero positive candidates."""
    unknown={f['concept'] for f in facts}-set(required)
    if unknown:
        raise FactExtractionError('UNKNOWN_CANDIDATE_CONCEPT',field='concept',actual=sorted(unknown))
    result=[];keys=[];rows=[]
    def flush():
        if keys:result.append({'concepts':list(keys),'facts':list(rows),'audit':True})
        keys.clear();rows.clear()
    for key in sorted(required):
        fs=sorted([f for f in facts if f['concept']==key],key=lambda f:f['fact_id'])
        if keys and (len(keys)>=concept_size or len(rows)+len(fs)>fact_size):flush()
        if len(fs)>fact_size:
            for i in range(0,len(fs),fact_size):result.append({'concepts':[key],'facts':fs[i:i+fact_size],'audit':i==0})
        else:
            keys.append(key);rows.extend(fs)
    flush()
    return result
