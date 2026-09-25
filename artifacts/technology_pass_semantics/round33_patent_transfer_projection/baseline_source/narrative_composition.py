"""Presentation-only deduplication; preserve distinct qualifications and facts."""
import re


def key(text):
    value=re.sub(r'^(?:人工复核|复核提示|核验提示)\s*[:：]\s*','',text.strip())
    value=re.sub(r'^(?:请|建议|需要|需)\s*(?=核验|核实|确认)','',value)
    return re.sub(r'[\s。；;，,：:、]+','',value)


def dedupe(text):
    seen=set();parts=[]
    for sentence in re.split(r'(?<=[。；;])',text or ''):
        normalized=key(sentence)
        if normalized and normalized not in seen:
            seen.add(normalized);parts.append(sentence.strip())
    return ''.join(parts).rstrip('；;')


def compose_risk_fields(judgment,issue,consequence,exposure,components=None):
    """Reuse explicit producer fields, omit repeated content rather than invent facts."""
    fields=dict(judgment=judgment,issue=issue,consequence=consequence,exposure=exposure)
    fields.update({k:v for k,v in (components or {}).items() if k in fields and v})
    seen=set()
    for name in fields:
        value=dedupe(fields[name]);normalized=key(value)
        fields[name]=value if normalized not in seen else ''
        if normalized:seen.add(normalized)
    return fields
