"""Shared existing decimal/Chinese-number normalization; no source retrieval."""
from decimal import Decimal, InvalidOperation
import re
from review_v2.fact_validation import FactExtractionError


def number(value):
    text = str(value).replace(',', '').replace('，', '').strip()
    text = re.sub(r'\s*(?:元)?[/／](?:月|件)\s*$', '', text)
    text = text.removeprefix('人民币').removesuffix('元整').removesuffix('元').removesuffix('整')
    try:
        return Decimal(text)
    except InvalidOperation:
        digits = dict(zip('零〇一二两三四五六七八九壹贰叁肆伍陆柒捌玖', [0,0,1,2,2,3,4,5,6,7,8,9,1,2,3,4,5,6,7,8,9]))
        units = {'十':10,'拾':10,'百':100,'佰':100,'千':1000,'仟':1000,'万':10000,'萬':10000,'亿':100000000}
        total = section = n = 0
        for char in text:
            if char in digits:
                n = digits[char]
            elif char in units:
                unit = units[char]
                if unit < 10000:
                    section += (n or 1) * unit
                else:
                    total += (section + n) * unit
                    section = 0
                n = 0
            else:
                raise FactExtractionError('INVALID_NUMERIC_NORMALIZATION')
        if not text:
            raise FactExtractionError('EMPTY_NUMERIC_NORMALIZATION')
        return Decimal(total + section + n)
