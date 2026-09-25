"""Structured diagnostics and lossless, formatting-tolerant source alignment."""
import re


class FactExtractionError(RuntimeError):
    def __init__(self, rule, *, failed_stage='FACT_STORE', fact_id=None, field=None,
                 model_raw_value=None, evidence=None, expected=None, actual=None,
                 diagnostics=None, repairable=True):
        self.repairable = repairable
        self.diagnostics = diagnostics or [{
            'failed_stage': failed_stage, 'fact_id': fact_id, 'field': field,
            'validation_rule': rule, 'model_raw_value': model_raw_value,
            'evidence': evidence, 'expected': expected,
            'actual': actual if actual is not None else model_raw_value,
            'disposition': 'BLOCK',
        }]
        self.attempts = []
        self.raw_output = None
        super().__init__(rule + (': ' + '; '.join(d['validation_rule'] for d in diagnostics) if diagnostics else ''))


def canonical_view(text):
    """Return canonical characters and a reversible map into the ORIGINAL text.

    Only layout/typographic transformations are allowed: never delete ordinary
    words, negation, digits, redaction underscores, ellipses, or reorder text.
    """
    removed = set()
    for pattern in (r'(?m)^\s{0,3}#{1,6}[ \t]+', r'(?m)^\s{0,3}>[ \t]+'):
        for m in re.finditer(pattern, text):
            removed.update(range(m.start(), m.end()))
    for pattern in (r'(\*\*|__)(?=\S)(.+?)(?<=\S)\1', r'(`)([^`\n]+)\1'):
        for m in re.finditer(pattern, text):
            if not m[2].strip('*_`'):
                continue  # Blank/redacted fields are not emphasis content.
            removed.update(range(m.start(), m.start(2)))
            removed.update(range(m.end(2), m.end()))
    chars, offsets = [], []
    typography = {'“':'"','”':'"','‘':"'",'’':"'",'。':'.'}
    for i, c in enumerate(text):
        if i in removed or c.isspace():
            continue
        if 0xff01 <= ord(c) <= 0xff5e:
            c = chr(ord(c) - 0xfee0)
        # Do not turn punctuation between digits into a decimal value.
        if c != '。' or not (i > 0 and i + 1 < len(text) and text[i-1].isdigit() and text[i+1].isdigit()):
            c = typography.get(c, c)
        chars.append(c)
        offsets.append(i)
    return ''.join(chars), offsets


def bind_quote(text, quote):
    if not isinstance(quote, str) or not quote.strip():
        raise FactExtractionError('EMPTY_EVIDENCE', failed_stage='EVIDENCE_BINDING',
                                  field='evidence.quote', model_raw_value=quote, expected='non-empty source excerpt')
    start = text.find(quote)
    if start >= 0:
        return start, start + len(quote), 'EXACT'
    normalized, offsets = canonical_view(text)
    needle, _ = canonical_view(quote)
    start = normalized.find(needle) if needle else -1
    if start < 0:
        raise FactExtractionError('EVIDENCE_NOT_IN_CLAUSE', failed_stage='EVIDENCE_BINDING',
                                  field='evidence.quote', model_raw_value=quote, evidence=quote,
                                  expected='contiguous source text after formatting-only normalization', actual='NO_MATCH')
    if normalized.find(needle, start + 1) >= 0:
        raise FactExtractionError('AMBIGUOUS_EVIDENCE_SPAN', failed_stage='EVIDENCE_BINDING',
                                  field='evidence.quote', model_raw_value=quote, expected='unique span within selected clause', actual='MULTIPLE_MATCHES')
    end = start + len(needle)
    return offsets[start], offsets[end-1] + 1, 'FORMATTING_NORMALIZED'
