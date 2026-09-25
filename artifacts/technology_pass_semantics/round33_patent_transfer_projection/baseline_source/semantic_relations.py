"""Compose bounded legal relations from slots, not checklist-title similarity.

Each alternative requires every slot in one sentence. Word order between
independent slots is immaterial; order inside a role/action slot is retained.
The generated patterns are consumed by the existing canonical evaluator,
absence audit and publication gate, rather than a second test-only matcher.
"""
import re


def relation(key, description, *alternatives, across_sentences=False, excluded=()):
    unit = r'[\s\S]' if across_sentences else r'[^。；;]'
    patterns = []
    for slots in alternatives:
        guards = ''.join(r'(?=' + unit + r'{0,600}(?:' + pattern + '))'
                         for pattern in slots.values())
        patterns.append(guards + unit + r'{1,700}')
    return dict(element_id=key, proposition=description,
                semantic_patterns=tuple(patterns), relation_slots=list(alternatives),
                excluded_patterns=list(excluded), evidence_unit='clause',
                quote_match_only=not across_sentences,
                preserve_full_quote=across_sentences)


def slot_trace(requirement, text):
    return [{name: [{'text': m.group(), 'start': m.start(), 'end': m.end()}
                    for m in re.finditer(pattern, text)]
             for name, pattern in alternative.items()}
            for alternative in requirement.get('relation_slots', [])]
