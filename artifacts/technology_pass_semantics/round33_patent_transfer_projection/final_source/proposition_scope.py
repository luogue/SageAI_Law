"""Source-preserving scope for declarations, conditions and absent arrangements."""
import re

# A modal is a grammatical operator, not a character inside an object name
# (许可、认可、可能). Keep the actor/action relationship in candidate selection.
PERMISSION_MODAL = r'(?:仅可|可以|有权|获准|方可|(?<!许)(?<!认)可(?!能|靠|行|用性))'
_OPERATIVE_VERB = r'(?:支付|付款|返还|退还|结算|赔偿|承担|通知|告知|终止|解除|保密|披露|停止|限制|制造|生产|使用|销售|实施)'


def predicate_is_operative(text, start, end):
    """Do not promote a temporal antecedent or another verb's object to a duty.

    This concerns the matched predicate, not whether the complete sentence
    contains a financial word. A real grant can coexist with a payment duty.
    """
    tail = text[end:]
    if re.search(r'^[^。；;，,]*?(?:之后|以后|后|之时|时|的)(?:[一二两三四五六七八九十百\d]+个?(?:工作日|日|天|月|年)(?:内|后))?[，,\s]*(?:(?:甲方|乙方|双方|其)[\s]*)?(?:(?:应当|应|须|必须|需|及时|立即|仍|再|方可|可以|有权)[\s]*)*' + _OPERATIVE_VERB, tail):
        return False
    prefix = re.split(r'[，,。；;]', text[:start])[-1]
    if re.search(r'(?:无权|不能|不得|未获授权)$', prefix):
        return False
    if re.search(r'(?:通知|告知|赔偿|支付|返还|结算|保密|披露|停止|终止)[^，,。；;]*$', prefix):
        return False
    return True


def operative_arrangement_matches(pattern, text):
    """Select operative predicates while preserving exact source conditions."""
    for row in arrangement_matches(pattern, text):
        if not predicate_is_operative(row['quote'], row['match_start'], row['match_end']):
            continue
        # Separate an independently stated following duty; do not display that
        # duty as proof of this predicate. Preceding conditions stay attached.
        boundary = re.search(r'[，,](?:并且|并|且|同时)?\s*(?:(?:甲方|乙方|双方)\s*)?(?:应当|应|须|必须|需)' + _OPERATIVE_VERB,
                             row['quote'][row['match_end']:])
        if boundary:
            row = dict(row, quote=row['quote'][:row['match_end'] + boundary.start()])
        yield row


_GAP = re.compile(r'(?:尚未|并未|没有|未)(?:作出?|作)?(?:特别|明确|具体|另行)?(?:约定|规定|明确)|(?:尚未|未能|未|无法|不能)(?:确认|认定|确定|证实|证明)')
_CONDITION = re.compile(r'(?:^|[，,：:])\s*(?:(?:如(?:果)?|假如|假设|若|倘若|即使|一旦|仅在|只有)(?!实)[^，,。；;\n]+|(?:当|在)[^，,。；;\n]+(?:时|情况下))')
_NEGATION = re.compile(r'未发现|未发生|不存在|没有|并未|并非|不曾|未曾|否认|(?:不(?:会|再|曾)?|未|不得|不应当|不应|不能|禁止)(?=允许|同意|侵犯|侵害|构成|承担|负责|提供|赔偿)')
_INDEPENDENT = re.compile(r'(?:但(?:是)?|然而|不过)[，,\s]*(?:甲方|乙方|双方|许可方|被许可方)(?=应当|应|须|负责|承担|确认|同意)')
_IMPLICIT_CONDITION = re.compile(r'^[^，,。；;\n]+(?:的|后)[，,](?=[^。；;\n]{0,25}(?:应|须|有权|可以|不得))')


def _condition(text):
    return _CONDITION.search(text) or _IMPLICIT_CONDITION.search(text)


def scoped_propositions(text):
    """Yield exact spans; an absence-list introduction governs its members.

    New articles, full stops, and explicitly independent obligations close
    the list scope. Semicolons and paragraph breaks do not close an enumeration.
    Conditions qualify events but still permit their consequent obligations.
    """
    gap_context = ''
    condition_context = ''
    for match in re.finditer(r'[^。；;！？\n]+[。；;！？]?', text or ''):
        quote = match[0].strip()
        if not quote:
            continue
        # An actor/action in a list member is still governed by the missing
        # introduction (e.g. "未约定：甲方承担律师费；...").
        if (re.match(r'第[一二三四五六七八九十百\d]+条|另行约定|现约定', quote)
                or _INDEPENDENT.match(quote)):
            gap_context = ''
            condition_context = ''
        gap = _GAP.search(quote)
        condition = _condition(quote)
        independent = _INDEPENDENT.search(quote)
        polarity = ('MISSING' if gap or gap_context else 'CONDITIONAL' if condition or condition_context
                    else 'NEGATED' if _NEGATION.search(quote) else 'AFFIRMATIVE')
        yield dict(quote=quote, start=match.start(), end=match.end(), polarity=polarity,
                   condition=condition[0].strip() if condition else condition_context,
                   condition_context=condition_context,
                   affirmative_tail=quote[independent.start():] if independent else '',
                   inherited_missing=bool(gap_context),
                   scope_context=gap_context or (quote if gap else ''))
        if gap and re.search(r'[：:]', quote[gap.end():]) and not independent:
            # An inline first list member keeps the same absence scope as a
            # list starting on the next line; semicolons do not end the list.
            gap_context = quote
        if condition and quote.rstrip().endswith(('：', ':')):
            condition_context = quote
        if quote.endswith(('。', '！', '？')):
            gap_context = ''
            condition_context = ''


def event_polarity(text, start, end):
    """Resolve an event match without treating a conditional duty as occurrence."""
    boundaries = [match.start() for match in _INDEPENDENT.finditer(text) if match.start() <= start]
    scope_start = boundaries[-1] if boundaries else 0
    prefix = text[scope_start:start]
    if _GAP.search(text[scope_start:end]):
        return 'MISSING'
    condition = _condition(text[scope_start:])
    if condition and condition.start() <= start - scope_start:
        return 'CONDITIONAL'
    if _NEGATION.search(text[scope_start:end]) or re.search(r'不(?:会|曾)?$', prefix):
        return 'NEGATED'
    return 'AFFIRMATIVE'


def arrangement_matches(pattern, text, *, inherit_lists=False):
    """Yield source-bound assertions about arrangements, including conditions.

    Unlike an event occurrence, an operative conditional duty is an existing
    arrangement. A question governed by a trailing absence declaration is not.
    Negation outside the predicate negates it; negation *inside* a predicate
    (e.g. a prohibition) belongs to that predicate's business meaning.
    """
    introduction = None
    for row in scoped_propositions(text):
        quote = row['quote']
        if inherit_lists:
            if quote.endswith(('：', ':')):
                introduction = (row['start'] if row['polarity'] in {'AFFIRMATIVE', 'CONDITIONAL'}
                                and re.search(r'(?:应当|应|须|提供|包括|如下|下列)[^。；]{0,20}[：:]$', quote) else None)
            elif introduction is not None:
                if row['polarity'] in {'AFFIRMATIVE', 'CONDITIONAL'}:
                    quote = text[introduction:row['end']].strip()
                    row = {**row, 'quote': quote, 'start': introduction}
                else:
                    introduction = None
            if quote.endswith(('。', '！', '？')):
                introduction = None
        if row['inherited_missing'] or re.fullmatch(r'第[一二三四五六七八九十百\d]+条[^，,。；;：:\n]{0,40}', quote):
            continue
        for match in re.finditer(pattern, quote, re.I):
            independent = [m.start() for m in _INDEPENDENT.finditer(quote) if m.start() <= match.start()]
            begin = independent[-1] if independent else 0
            boundaries = [m.end() + begin for m in re.finditer(r'[，,]', quote[begin:match.start()])]
            prefix = quote[boundaries[-1] if boundaries else begin:match.start()]
            gap = _GAP.search(quote, begin)
            if re.search(r'是否|能否|要不要|何时|如何', quote[begin:match.end()]):
                continue
            if gap and (gap.start() < match.end() or re.fullmatch(
                    r'(?:的?(?:事项|安排|问题))?[，,\s]*(?:双方|各方)?', quote[match.end():gap.start()])):
                continue
            if re.search(r'(?:不(?:应当|应|得|能|再|会|必|须)?|无需|无须|未|没有|并非|未曾|不曾|否认)[^，,。；;]{0,6}$', prefix):
                continue
            yield {**row, 'match_start': match.start(), 'match_end': match.end(),
                   'arrangement_polarity': 'AFFIRMATIVE',
                   'event_polarity': 'CONDITIONAL' if row['condition_context'] else event_polarity(quote, match.start(), match.end())}


def component_states(specs):
    """Independent source-backed states for a compound requirement."""
    return [dict(element_id=key, required_fact=label,
                 status='COVERED' if sources else 'MISSING',
                 supporting_evidence=sources)
            for key, label, sources in specs]


def listed_arrangement_matches(pattern, text, *, introduction_pattern):
    """A list member inherits its own operative introduction, not a neighbour.

    Preserve the contiguous original span, including a prohibition/condition.
    A missing-list introduction never establishes an operative arrangement.
    """
    introduction = None
    for row in scoped_propositions(text):
        quote = row['quote']
        if quote.endswith(('：', ':')):
            introduction = row if (any(arrangement_matches(introduction_pattern, quote))
                                   and row['polarity'] != 'MISSING') else None
            continue
        if introduction is None:
            continue
        if row['polarity'] == 'MISSING' or re.match(r'第[一二三四五六七八九十百\d]+条', quote):
            introduction = None
            continue
        if re.search(pattern, quote):
            yield dict(quote=text[introduction['start']:row['end']].strip(),
                       member_quote=quote, introduction=introduction['quote'],
                       condition=introduction.get('condition', ''),
                       arrangement_polarity='AFFIRMATIVE')
        if quote.endswith(('。', '！', '？')):
            introduction = None


def component_proposition(element):
    """A compound's prose must name only its independently resolved facts."""
    rows = element.get('component_coverage') or []
    covered = [row['required_fact'] for row in rows if row['status'] == 'COVERED']
    if not covered:
        return element['proposition']
    parts = ['已明确：' + '、'.join(covered)]
    if element.get('component_quantifier') != 'ANY':
        missing = [row['required_fact'] for row in rows if row['status'] == 'MISSING']
        partial = [row['required_fact'] for row in rows if row['status'] == 'PARTIALLY_COVERED']
        if partial:
            parts.append('部分明确：' + '、'.join(partial))
        if missing:
            parts.append('未明确：' + '、'.join(missing))
    return '；'.join(parts) + '。'
