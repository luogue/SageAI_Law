"""Presentation-only topic projection; evidence and verdicts remain unchanged."""
from copy import deepcopy

def project(findings, themes):
    names={fid:t['title'] for t in themes for fid in t.get('member_finding_ids', [t.get('finding_id')])}
    result=deepcopy(findings)
    for f in result:
        topic=names.get(f.finding_id, f.title)
        f.title=topic
        f.evidence_bundle=deepcopy(f.evidence_bundle or {})
        for row in f.evidence_bundle.get('items', []):
            row['support_labels']=[topic]
    return result

def recommendation_topics(recommendations, themes):
    names={fid:t['title'] for t in themes for fid in t.get('member_finding_ids', [t.get('finding_id')])}
    for row in recommendations:
        row['recommendation_topics']=list(dict.fromkeys(names[fid] for fid in row.get('source_finding_ids', []) if fid in names))

def gate(findings, themes, rendered_evidence, recommendations=()):
    names={fid:t['title'] for t in themes for fid in t.get('member_finding_ids', [t.get('finding_id')])}
    failures=[]
    for f in findings:
        topic=names.get(f.finding_id, f.title)
        labels=[label for row in (f.evidence_bundle or {}).get('items', []) for label in row.get('support_labels', [])]
        import re
        printed=re.findall(r'\[支持：([^\]]+)\]', rendered_evidence(f))
        if f.title!=topic or any(label!=topic for label in labels+printed):
            failures.append({'requirement':'REPORT_TOPIC_LABEL_CONSISTENCY','finding_id':f.finding_id,
                'current_status':'FAIL','failure_stage':'Report topic projection',
                'root_cause':'风险主题、发现名称或证据支持标签不一致。',
                'risk_topic':topic,'finding_title':f.title,'evidence_support_labels':labels,'rendered_support_labels':printed})
    for row in recommendations:
        expected=list(dict.fromkeys(names[fid] for fid in row.get('source_finding_ids', []) if fid in names))
        if row.get('recommendation_topics')!=expected:
            failures.append({'requirement':'REPORT_TOPIC_LABEL_CONSISTENCY','current_status':'FAIL',
                'failure_stage':'Recommendation topic projection','recommendation_id':row.get('recommendation_id'),
                'root_cause':'正式建议的关联主题与最终风险主题不一致。'})
    return {'status':'BLOCKED' if failures else 'REPORT_READY','failures':failures,
            'gate_results':{'REPORT_TOPIC_LABEL_CONSISTENCY':'FAIL' if failures else 'PASS'}}
