"""Source-preserving scope for declarations, conditions and absent arrangements."""
import re


_GAP = re.compile(r'(?:尚未|并未|没有|未)(?:作出?|作)?(?:特别|明确|具体|另行)?(?:约定|规定|明确)|(?:尚未|未能|未|无法|不能)(?:确认|认定|确定|证实|证明)')
_CONDITION = re.compile(r'(?:^|[，,：:])\s*(?:(?:如(?:果)?|假如|假设|若|倘若|一旦|仅在|只有)(?!实)[^，,。；;\n]+|(?:当|在)[^，,。；;\n]+(?:时|情况下))')
_NEGATION = re.compile(r'未发现|未发生|不存在|没有|并未|并非|不曾|未曾|否认|(?:不(?:会|再|曾)?|未|不得|不应当|不应|不能|禁止)(?=允许|同意|侵犯|侵害|构成|承担|负责|提供|赔偿)')
_INDEPENDENT = re.compile(r'(?:但(?:是)?|然而|不过)[，,\s]*(?:甲方|乙方|双方|许可方|被许可方)(?=应当|应|须|负责|承担|确认|同意)')


def scoped_propositions(text):
    """Yield exact spans; an absence-list introduction governs its members.

    New articles, full stops, and explicitly independent obligations close
    the list scope. Semicolons and paragraph breaks do not close an enumeration.
    Conditions qualify events but still permit their consequent obligations.
    """
    gap_context = ''
    for match in re.finditer(r'[^。；;！？\n]+[。；;！？]?', text or ''):
        quote = match[0].strip()
        if not quote:
            continue
        # An actor/action in a list member is still governed by the missing
        # introduction (e.g. "未约定：甲方承担律师费；...").
        if (re.match(r'第[一二三四五六七八九十百\d]+条|另行约定|现约定', quote)
                or _INDEPENDENT.match(quote)):
            gap_context = ''
        gap = _GAP.search(quote)
        condition = _CONDITION.search(quote)
        independent = _INDEPENDENT.search(quote)
        polarity = ('MISSING' if gap or gap_context else 'CONDITIONAL' if condition
                    else 'NEGATED' if _NEGATION.search(quote) else 'AFFIRMATIVE')
        yield dict(quote=quote, start=match.start(), end=match.end(), polarity=polarity,
                   condition=condition[0].strip() if condition else '',
                   affirmative_tail=quote[independent.start():] if independent else '',
                   inherited_missing=bool(gap_context),
                   scope_context=gap_context or (quote if gap else ''))
        if gap and quote.rstrip().endswith(('：', ':')):
            gap_context = quote
        elif quote.endswith(('。', '！', '？')):
            gap_context = ''


def event_polarity(text, start, end):
    """Resolve an event match without treating a conditional duty as occurrence."""
    boundaries = [match.start() for match in _INDEPENDENT.finditer(text) if match.start() <= start]
    scope_start = boundaries[-1] if boundaries else 0
    prefix = text[scope_start:start]
    if _GAP.search(text[scope_start:end]):
        return 'MISSING'
    condition = _CONDITION.search(text[scope_start:])
    if condition and condition.start() <= start - scope_start:
        return 'CONDITIONAL'
    if _NEGATION.search(text[scope_start:end]) or re.search(r'不(?:会|曾)?$', prefix):
        return 'NEGATED'
    return 'AFFIRMATIVE'
