"""Observe the original cap protection pipeline without modifying its facts."""
from copy import deepcopy
from pathlib import Path
import json
import os
events=[]
def snapshot(items):
    if hasattr(items,'item_id'): items=[items]
    item=next((i for i in items if i.item_id==os.environ.get('ROUND8_TRACE_RULE','TC-07-03')),None)
    return deepcopy(dict(status=item.coverage_status,elements=item.coverage_elements,
                         evidence=item.evidence_clauses)) if item else None
def pytest_configure(config):
    from review_v2 import engine
    for name in ('_set_multi_element_state','_protect_deterministic_semantic_evidence',
                 '_verified_pass_sources','_apply_element_level_narratives',
                 '_attach_evidence_traceability','_apply_review_evidence_ownership',
                 '_apply_factual_grounding_gate','_enrich_evidence_sources',
                 '_apply_final_technology_fact_projection','_apply_technology_transaction_evidence_consistency'):
        old=getattr(engine,name)
        def traced(items,*a,_name=name,_old=old,**kw):
            before=snapshot(items);result=_old(items,*a,**kw);after=snapshot(items)
            if before!=after:events.append(dict(stage=_name,before=before,after=after))
            return result
        setattr(engine,name,traced)
    old_review=engine.review_contract_v2
    def capture(*a,**kw):
        report=old_review(*a,**kw)
        path=Path(__file__).resolve().parents[1]/'artifacts/technology_pass_semantics'/os.environ.get('ROUND8_TRACE_FILE','round8_cap_stages.json')
        path.write_text(json.dumps(dict(events=events,report=report),ensure_ascii=False,indent=2),encoding='utf8')
        return report
    engine.review_contract_v2=capture
