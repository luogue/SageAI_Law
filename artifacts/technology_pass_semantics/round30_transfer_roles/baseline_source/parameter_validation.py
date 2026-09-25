"""Source-preserving numeric extraction and condition-aware comparisons.

Thresholds belong to callers, not to number extraction. Unknown conditions and
working-day durations are deliberately not converted into a compliant result.
"""
import re

NUMBER = r"(?:\d{1,3}(?:[,，]\d{3})+(?:\.\d+)?|\d+(?:\.\d+)?|[零〇一二两三四五六七八九十百千万]+)"


def number(text):
    try:
        return float(text.replace(",", "").replace("，", ""))
    except ValueError:
        digits = dict(zip("零〇一二两三四五六七八九", [0, 0, 1, 2, 2, 3, 4, 5, 6, 7, 8, 9]))
        total = section = current = 0
        for char in text:
            if char in digits:
                current = digits[char]
            elif char in "十百千":
                section += (current or 1) * {"十": 10, "百": 100, "千": 1000}[char]
                current = 0
            elif char == "万":
                total += (section + current) * 10000
                section = current = 0
        return float(total + section + current)


def extract_parameters(text):
    rows = []
    patterns = {
        "duration": rf"(?P<number>{NUMBER})(?:个)?(?P<unit>工作日|小时|分钟|日|天)",
        "ratio": rf"(?:(?P<prefix>百分之|千分之|万分之)(?P<cn>{NUMBER})|(?P<number>{NUMBER})(?P<unit>%|％|‰))",
        "amount": rf"(?P<number>{NUMBER})(?P<unit>万元|元)",
        "count": rf"(?P<number>{NUMBER})(?P<unit>次)",
    }
    for kind, pattern in patterns.items():
        for match in re.finditer(pattern, text):
            data = match.groupdict()
            value = number(data.get("number") or data.get("cn"))
            unit = data.get("unit") or data.get("prefix")
            normalized = value
            if kind == "ratio":
                normalized /= {"百分之": 100, "千分之": 1000, "万分之": 10000, "%": 100, "％": 100, "‰": 1000}[unit]
            elif kind == "duration":
                normalized *= {"小时": 1, "分钟": 1 / 60, "日": 24, "天": 24, "工作日": 24}[unit]
            elif unit == "万元":
                normalized *= 10000
            rows.append(dict(kind=kind, value=value, unit=unit, normalized=normalized,
                             quote=match.group(), start=match.start(), end=match.end(),
                             calendar_uncertain=unit == "工作日"))
    return rows


def compare(parameter, maximum, *, condition=True):
    if condition is not True or maximum is None:
        return "CONDITION_UNRESOLVED"
    if parameter["normalized"] > maximum:
        return "ADVERSE"
    if parameter.get("calendar_uncertain"):
        return "CONDITION_UNRESOLVED"
    return "COVERED"
