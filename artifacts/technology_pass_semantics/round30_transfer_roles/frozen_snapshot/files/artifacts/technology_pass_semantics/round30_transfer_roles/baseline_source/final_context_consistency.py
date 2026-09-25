"""Verify mixed contract/external facts at the final report boundary."""
import re

def verify(report):
    failures, rows = [], []
    markdown = report.get('result', '')
    for item in report.get('items', []):
        # A shared source may support several atoms; none can remain absent
        # in a downstream search audit once its final positive binding exists.
        audits = item.get('decision_trace', {}).get('element_absence_searches', [])
        for element in item.get('coverage_elements', []):
            if element.get('status') in {'COVERED', 'FOUND'} and any(
                a.get('element_id') == element.get('element_id') and a.get('result') == 'NOT_FOUND'
                for a in audits
            ):
                failures.append(dict(rule_id=item['item_id'], element_id=element['element_id'],
                    final_element_status=element['status'], bound_evidence_id=element.get('evidence_ids', []),
                    report_fact=audits, reason='FOUND_ELEMENT_HAS_NOT_FOUND_SEARCH_AUDIT'))
        for assessment in item.get('decision_trace', {}).get('requirement_kind_assessments', []):
            if assessment.get('requirement_kind') == 'EXTERNAL_VERIFICATION' and assessment.get('external_fact_status') == 'VERIFIED':
                verification = assessment.get('external_verification') or {}
                if not verification.get('verified_by') or not verification.get('source_record_id') or verification.get('source_type') in {None, 'CONTRACT_TEXT', 'CONTRACT_STATEMENT'}:
                    failures.append(dict(rule_id=item['item_id'],element_id=assessment['element_id'],
                        final_element_status='VERIFIED',bound_evidence_id=[],report_fact=assessment,
                        reason='EXTERNAL_FACT_VERIFIED_WITHOUT_INDEPENDENT_VERIFICATION'))
        pending = [a for a in item.get('decision_trace', {}).get('requirement_kind_assessments', [])
                   if a.get('requirement_kind') == 'EXTERNAL_VERIFICATION' and a.get('status')=='PENDING_VERIFICATION']
        if not pending:
            continue
        match = re.search(r'^## [^\n]*' + re.escape(item['item_id']) + r'[^\n]*\n(.*?)(?=^## |\Z)', markdown, re.M|re.S)
        section = match.group(1) if match else ''
        for element in item.get('coverage_elements', []):
            ids = set(element.get('evidence_ids') or element.get('source_clause_ids') or [])
            evidence = [e for e in item.get('evidence_clauses', []) if
                        bool(ids.intersection(filter(None, (e.get('evidence_id'), e.get('clause_id')))))
                        and e.get('source_type')!='SEARCH_AUDIT']
            quotes = [str(e.get('quote') or e.get('text') or '') for e in evidence]
            record = dict(rule_id=item['item_id'], element_id=element['element_id'],
                final_element_status=element['status'], bound_evidence_id=sorted(ids), report_fact=section,
                source_quotes=quotes)
            rows.append(record)
            if element['status']=='COVERED' and (not quotes or not any(q and q in section for q in quotes)):
                failures.append({**record, 'reason':'FOUND_ELEMENT_QUOTE_MISSING_FROM_RULE_DETAIL'})
            if element['status']=='MISSING' and evidence:
                failures.append({**record, 'reason':'MISSING_ELEMENT_HAS_BOUND_POSITIVE_EVIDENCE'})
        if item.get('applicability', {}).get('applicable') is True and re.search(r'是否适用|无法确认.*适用', section):
            failures.append(dict(rule_id=item['item_id'],element_id=None,final_element_status='EXTERNAL_VERIFICATION',
                bound_evidence_id=[],report_fact=section,reason='EXTERNAL_FACT_CONFUSED_WITH_APPLICABILITY'))
        if '外部事实' not in section:
            failures.append(dict(rule_id=item['item_id'],element_id=None,final_element_status='EXTERNAL_VERIFICATION',
                bound_evidence_id=[],report_fact=section,reason='EXTERNAL_MATERIAL_DEFICIT_NOT_EXPLAINED'))
    return {'status':'BLOCKED' if failures else 'REPORT_READY', 'rows':rows,
        'failures':[{**f,'requirement':'FINAL_CONTEXT_EVIDENCE_CONSISTENCY','current_status':'FAIL',
                     'failure_stage':'Final report fact projection','root_cause':f['reason']} for f in failures]}
