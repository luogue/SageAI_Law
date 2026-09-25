"""Observe the real legal-basis pipeline; never infer a missing stage."""
from dataclasses import asdict
from copy import deepcopy
import sys

def snapshot(items, stage, checkpoints=()):
    by_node={c.node_id:c for c in checkpoints}
    for item in items:
        trace=item.decision_trace.setdefault('legal_basis_runtime_trace', {'stages':[]})
        c=by_node.get(item.node_id)
        if c:
            trace['runtime_rule_metadata']=asdict(c)
            trace['required_elements']=deepcopy(item.coverage_elements)
            sources=[m.__file__ for name,m in list(sys.modules.items()) if name.endswith('_checklist') and getattr(m,'__file__',None)
                     and any(isinstance(v,tuple) and any(x is c for x in v) for v in vars(m).values())]
            trace['rule_source']={'SOURCE_FILE':sources,'SOURCE_FIELD':'ReviewCheckpoint.legal_basis',
                'VALUE_BEFORE':c.legal_basis,'VALUE_AFTER':c.legal_basis}
        stages=trace['stages']
        before=stages[-1]['VALUE_AFTER'] if stages else (c.legal_basis if c else item.legal_basis_index)
        stages.append({'STAGE':stage,'SOURCE_FILE':'backend/review_v2/engine.py',
            'SOURCE_FIELD':'ReviewItemResult.legal_basis_index','VALUE_BEFORE':before,
            'VALUE_AFTER':item.legal_basis_index,
            'legal_references':[{k:r.get(k) for k in ('article','proposition','support_type','freshness_status','support_scope')} for r in item.legal_references or []]})

def candidates(item,specs):
    trace=item.decision_trace.setdefault('legal_basis_runtime_trace',{'stages':[]})
    trace['citation_specs']=specs
    trace.setdefault('legal_propositions',specs)

def display(item,value):
    trace=item.decision_trace.setdefault('legal_basis_runtime_trace',{'stages':[]})
    trace['renderer']={'SOURCE_FILE':'backend/review_v2/engine.py::_trusted_legal_basis_display',
        'SOURCE_FIELD':'legal_references -> support_type filter -> first 3 distinct authorities',
        'VALUE_BEFORE':item.legal_basis_index,'VALUE_AFTER':value}
    return value

def finish(items,public_items,report):
    import re
    by_id={i['item_id']:i for i in public_items}
    failures=[]
    for item in items:
        trace=item.decision_trace.get('legal_basis_runtime_trace',{})
        section=re.search(r'^## .*?[（(]'+re.escape(item.item_id)+r'[）)].*?$(.*?)(?=^## |\Z)',report,re.M|re.S)
        match=re.search(r'^- .*?法律依据.*?：([^\n]*)',section[1],re.M) if section else None
        actual=match[1] if match else ''
        trace['final_markdown']={'SOURCE_FILE':'backend/review_v2/engine.py::_format_markdown_v2',
          'SOURCE_FIELD':'Markdown.法律依据','VALUE_BEFORE':item.legal_basis_index,'VALUE_AFTER':actual}
        selected=trace.get('selected_basis')
        if selected is not None:
            from review_v2.legal_basis_selection import audit_result
            trace['full_basis_audit']=audit_result(item)
            if trace['full_basis_audit']['status']=='BLOCKED':
                failures.append({'requirement':'SPECIAL_OVER_GENERAL_AUDIT','root_cause':item.item_id,'current_status':'FAIL'})
        if selected is not None and not trace.get('selection_complete'):
            failures.append({'requirement':'LEGAL_BASIS_AUTHORITY_UNAVAILABLE','root_cause':item.item_id,'current_status':'FAIL'})
        # Existing renderer intentionally omits legal-basis lines for review-pending
        # items. Still validate the selected/result fields and full candidate audit.
        visible_status=by_id.get(item.item_id,{}).get('coverage_status',getattr(item,'coverage_status',''))
        rendered_status=re.search(r'^- 覆盖状态：([^\n]*)',section[1],re.M) if section else None
        if rendered_status:
            visible_status=rendered_status[1].strip()
        trace['rendered_coverage_status']=visible_status
        expected= '' if visible_status in ('待核验','INSUFFICIENT_CONTEXT') else selected
        trace['expected_report_basis']=expected
        if selected is not None and (actual != expected or item.legal_basis_index != selected):
            failures.append({'requirement':'LEGAL_BASIS_RUNTIME_PROJECTION','root_cause':item.item_id,'current_status':'FAIL'})
        if item.item_id in by_id:
            by_id[item.item_id]['decision_trace']['legal_basis_runtime_trace']=trace
    return {'status':'BLOCKED' if failures else 'REPORT_READY','failures':failures}
