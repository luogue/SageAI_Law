"""Fail closed when an affirmative risk contradicts source/audit polarity."""
import re
from review_v2.adverse_evidence import direct_evidence, proposition_polarity

def value(row,key,default=None):
    return row.get(key,default) if isinstance(row,dict) else getattr(row,key,default)

def gate(items,clauses,findings=()):
    failures=[]
    checked=list(items)
    by_id={value(i,'item_id'):i for i in items}
    for finding in findings:
        if value(finding,'issue_type') not in {'ADVERSE','风险条款'}:
            continue
        for rid in value(finding,'source_review_ids',[]) or []:
            if rid in by_id:
                checked.append({'item_id':rid,'coverage_status':'RISK_CLAUSE',
                    'decision_trace':value(by_id[rid],'decision_trace',{}),
                    'coverage_elements':value(finding,'final_adverse_elements',[]) or value(by_id[rid],'coverage_elements',[]),
                    'evidence_clauses':value(finding,'evidence',[]),
                    'rule_evidence_package':value(finding,'evidence_bundle',{})})
    for item in checked:
        if value(item,'coverage_status') not in {'风险条款','RISK_CLAUSE','RISK'}:
            continue
        trace=value(item,'decision_trace',{}) or {}
        predicates=trace.get('adverse_predicates',[])
        evidence=value(item,'evidence_clauses',[]) or []
        atoms=value(item,'coverage_elements',[]) or []
        affirmed={str(e.get('element_id')) for e in atoms if e.get('status') in {'ADVERSE','COVERED','FOUND'}}
        audits=list(trace.get('element_absence_searches',[]) or [])
        package=value(item,'rule_evidence_package',{}) or {}
        for row in evidence+list(package.get('items',[]) or []):
            if row.get('evidence_type')=='SEARCH_AUDIT' or row.get('source_type')=='SEARCH_AUDIT':
                audits.append(row)
        for audit in audits:
            if audit.get('result') not in {'NOT_FOUND','no_positive_fact','NO_POSITIVE_FACT'}:
                continue
            ids={str(audit.get('element_id') or audit.get('target_element') or '')}
            ids.update(audit.get('supports_element_ids',[]) or [])
            target=' '.join(map(str,audit.get('search_targets',[]) or []))+' '+str(audit.get('query_semantic_target') or '')
            # Absence of a prohibition is not absence of permission. Compare
            # the same proposition *and* its semantic direction, not topic words.
            matches=[m for p in predicates if (m:=re.search(p,target))]
            if matches and all(proposition_polarity(target,m.start('act') if 'act' in m.groupdict() else m.start(),
                    m.end('act') if 'act' in m.groupdict() else m.end())!='AFFIRMED' for m in matches):
                continue
            if ids & affirmed or (predicates and any(re.search(p,target) for p in predicates)):
                failures.append({'requirement':'ADVERSE_SEARCH_AUDIT_CONTRADICTION','rule_id':value(item,'item_id'),
                    'element_id':audit.get('element_id'),'root_cause':str(value(item,'item_id'))+': 肯定风险结论与同一要素的 NOT_FOUND 审计冲突。','current_status':'FAIL'})
        if predicates:
            positive,counter=direct_evidence(clauses,predicates)
            if not positive:
                failures.append({'requirement':'ADVERSE_SOURCE_POLARITY_CONTRADICTION','rule_id':value(item,'item_id'),
                    'root_cause':str(value(item,'item_id'))+': 原文无肯定风险证据，禁止/制裁条款不能支持风险断言。',
                    'source_clause_ids':[r['clause_id'] for r in counter],'current_status':'FAIL'})
            for row in evidence:
                if row.get('polarity') in {'NEGATED','PREVENTIVE','PROHIBITION','BREACH_TRIGGER','TERMINATION_TRIGGER','PENALTY_CLAUSE'}:
                    failures.append({'requirement':'ADVERSE_SUPPORT_POLARITY_CONTRADICTION','rule_id':value(item,'item_id'),
                        'evidence_id':row.get('evidence_id'),'root_cause':str(value(item,'item_id'))+': 支持风险的证据极性为禁止或制裁。','current_status':'FAIL'})
    return {'status':'BLOCKED' if failures else 'REPORT_READY','failures':failures,
            'gate_results':{'ADVERSE_POLARITY_AUDIT_GATE':'FAIL' if failures else 'PASS'}}
