"""Source-bound implementation rights, shared by patent and secret licences."""
import re
from review_v2.proposition_scope import PERMISSION_MODAL, operative_arrangement_matches
from review_v2.verified_source import exact_span

IMPLEMENTATION_ACT = r'(?:制造|生产|使用|销售|许诺销售|进口|出口|维修|更换|研发|复制|编译|调试|测试)'
_QUALIFIER = r'(?:(?!(?:支付|付款|赔偿|通知|告知|停止|终止|披露|保密|应|须|不得|不能|无需|无须|无权|许可费)).)'


def implementation_grants(text, recipient, *, source_text=None):
    """Require an actor's permission/restriction or an explicit grant object."""
    patterns = [
        recipient + _QUALIFIER + r'{0,18}' + PERMISSION_MODAL + _QUALIFIER + r'{0,65}' + IMPLEMENTATION_ACT,
        recipient + r'[^，,。；;]{1,40}(?:后|时)[，,]\s*' + PERMISSION_MODAL + _QUALIFIER + r'{0,35}' + IMPLEMENTATION_ACT,
        recipient + r'(?:不得|禁止)' + _QUALIFIER + r'{0,25}(?:利用|依据|按照)本许可' + _QUALIFIER + r'{0,15}' + IMPLEMENTATION_ACT,
        r'(?:授予|授权)' + _QUALIFIER + r'{0,25}' + recipient + _QUALIFIER + r'{0,65}' + IMPLEMENTATION_ACT,
        r'许可(?:给)?' + recipient + _QUALIFIER + r'{0,65}' + IMPLEMENTATION_ACT,
        r'(?:授予|授权)' + _QUALIFIER + r'{0,45}' + IMPLEMENTATION_ACT + _QUALIFIER + r'{0,35}(?:权利|权|许可)',
        r'实施方式[：:]\s*' + IMPLEMENTATION_ACT,
        r'许可(?:期限|地域|范围)[^。；;]{0,60}(?:仅限|限于)(?:用于)?' + IMPLEMENTATION_ACT,
    ]
    seen = set()
    # Parser-owned field/list spans may contain presentation line breaks
    # between a grant introduction and its first action. Match normalized
    # whitespace, but publish only the corresponding original source span.
    normalized = re.sub(r'\s+', '', text)
    original = source_text or text
    for pattern in patterns:
        for row in operative_arrangement_matches(pattern, normalized):
            span = exact_span(original, row['quote'])
            if not span:
                continue
            row = dict(row, quote=original[span[0]:span[1]])
            if row['quote'] not in seen:
                seen.add(row['quote'])
                yield row
