"""Explicit absence is a disclosed fact, not evidence that an event occurred.

Keep the negative object and any closed-list exception on the source. These
facts satisfy disclosure requirements only; they never establish adverse acts.
"""
import re
from review_v2.proposition_scope import scoped_propositions


def negative_sources(clauses, object_pattern):
    rows = []
    for clause in clauses:
        for part in scoped_propositions(clause.text):
            quote = part['quote']
            if part['polarity'] in {'MISSING', 'CONDITIONAL'}:
                continue
            match = re.search(r'(?:不存在|没有|从未|未曾|未授予|无(?!权|需|须|法|效|偿|论))([^。；]{0,80})', quote)
            if not match or not re.search(object_pattern, match[1]):
                continue
            if re.search(r'未发现|未能|无法|不能|是否|可能|不保证', quote[:match.start()]):
                continue
            rows.append(dict(clause_id=clause.clause_id, quote=quote,
                location=clause.location, proposition_polarity='NEGATIVE_CONFIRMED',
                fact_value='EXPLICIT_NONE', evidence_level='CONTRACTUAL_REPRESENTATION',
                exception_scope=bool(re.search(r'除[^。；]{0,30}(?:以外|之外|外)', quote))))
    return rows


def historical_disclosure(clauses):
    """A stated closed list needs actual recipients/events, not just '上述'."""
    result = []
    for clause in clauses:
        none = negative_sources([clause], r'披露|第三方使用')
        if not none:
            continue
        events = []
        for part in scoped_propositions(clause.text):
            if part['polarity'] != 'AFFIRMATIVE':
                continue
            if re.search(r'(?:曾|此前|已经|已)(?:向|为)[^。；]{2,70}(?:演示|展示|检测服务|测试服务|披露|提供)', part['quote']):
                events.append(dict(clause_id=clause.clause_id, quote=part['quote'],
                                   location=clause.location, proposition_polarity='AFFIRMATIVE'))
        for row in none:
            if not row['exception_scope'] or events:
                result.extend(events + [row])
    return result
