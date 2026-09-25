"""Deterministic formula parsing for review v2."""

from __future__ import annotations

import re
from typing import Any, Dict, Optional


def _compact(text: str) -> str:
    return re.sub(r"\s+", "", text or "")


def _numeric_amount(raw: str) -> float:
    return float(str(raw).replace(",", "").replace("，", ""))


def _multiplier(compacted: str) -> Optional[int]:
    match = re.search(r"(\d+|[一二两三四五六七八九十]+)倍", compacted)
    if not match:
        return None
    value = match.group(1)
    if value.isdigit():
        return int(value)
    mapping = {"一": 1, "二": 2, "两": 2, "三": 3, "四": 4, "五": 5, "六": 6, "七": 7, "八": 8, "九": 9, "十": 10}
    return mapping.get(value)


def _month_count_multiplier(compacted: str) -> Optional[int]:
    match = re.search(r"(\d+|[一二两三四五六七八九十]+)个?月租金", compacted)
    if not match:
        return None
    value = match.group(1)
    if value.isdigit():
        return int(value)
    mapping = {"一": 1, "二": 2, "两": 2, "三": 3, "四": 4, "五": 5, "六": 6, "七": 7, "八": 8, "九": 9, "十": 10}
    return mapping.get(value)


def parse_penalty_formula(text: str, *, default_party: str = "unspecified") -> Optional[Dict[str, Any]]:
    """Parse common liquidated-damages formulas into a stable structure."""

    compacted = _compact(text)
    if not ("违约金" in compacted or "赔偿金" in compacted or "滞纳金" in compacted):
        return None

    if any(term in compacted for term in ("乙方", "承租人")):
        party = "tenant"
    elif any(term in compacted for term in ("甲方", "出租人")):
        party = "landlord"
    else:
        party = default_party
    beneficiary = "landlord" if party == "tenant" else "tenant" if party == "landlord" else "unspecified"
    direction = "tenant_to_landlord" if party == "tenant" else "landlord_to_tenant" if party == "landlord" else "unspecified"

    fixed_amount_match = re.search(r"(?:违约金|赔偿金)(?:人民币)?(\d[\d,，.]*)元", compacted)
    if fixed_amount_match:
        return {
            "type": "fixed_amount",
            "base": "fixed_amount",
            "amount": _numeric_amount(fixed_amount_match.group(1)),
            "party": party,
            "beneficiary": beneficiary,
            "direction": direction,
        }

    min_max_match = re.search(
        r"(?:最低|不少于)(?:人民币)?(\d[\d,，.]*)元.{0,16}(?:最高|不超过|上限)(?:人民币)?(\d[\d,，.]*)元",
        compacted,
    )
    if min_max_match:
        return {
            "type": "min_max_formula",
            "base": "fixed_amount_range",
            "min_amount": _numeric_amount(min_max_match.group(1)),
            "max_amount": _numeric_amount(min_max_match.group(2)),
            "party": party,
            "beneficiary": beneficiary,
            "direction": direction,
        }

    capped_match = re.search(r"(?:最高(?:不)?超过|上限|累计不超过|不得超过)(?:人民币)?(\d[\d,，.]*)元", compacted)
    if capped_match:
        rate_match = re.search(r"(?:合同总价|总价款|合同价款|未付金额|未付款|欠款|欠付金额)[^，。；;]{0,16}?(?:的)?(\d+(?:\.\d+)?)\s*[%％]", compacted)
        return {
            "type": "capped_amount",
            "base": "capped_amount",
            "cap_amount": _numeric_amount(capped_match.group(1)),
            "rate": float(rate_match.group(1)) / 100 if rate_match else None,
            "party": party,
            "beneficiary": beneficiary,
            "direction": direction,
        }

    month_count = _month_count_multiplier(compacted)
    if month_count:
        return {
            "type": "monthly_rent_multiplier",
            "base": "monthly_rent",
            "multiplier": month_count,
            "party": party,
            "beneficiary": beneficiary,
            "direction": direction,
        }

    multiplier = _multiplier(compacted)
    if multiplier:
        if any(term in compacted for term in ("提前退租天数", "剩余租期", "剩余期间", "对应租金", "未履行期间租金")):
            source = "early_surrender_days" if "提前退租天数" in compacted else "remaining_term"
            return {
                "type": "remaining_term_rent_multiplier",
                "base": "remaining_term_rent",
                "multiplier": multiplier,
                "time_base_source": source,
                "party": party,
                "beneficiary": beneficiary,
                "direction": direction,
            }
        if any(term in compacted for term in ("日租金", "每日租金", "每天租金")):
            return {
                "type": "daily_rent_multiplier",
                "base": "daily_rent",
                "multiplier": multiplier,
                "party": party,
                "beneficiary": beneficiary,
                "direction": direction,
            }
        if any(term in compacted for term in ("个月租金", "月租金", "一月租金", "两月租金")):
            return {
                "type": "monthly_rent_multiplier",
                "base": "monthly_rent",
                "multiplier": multiplier,
                "party": party,
                "beneficiary": beneficiary,
                "direction": direction,
            }
        return {
            "type": "rent_multiplier",
            "base": "rent",
            "multiplier": multiplier,
            "party": party,
            "beneficiary": beneficiary,
            "direction": direction,
        }

    daily_wan_match = re.search(r"(?:每日|每天|按日|日)[^，。；;]{0,16}(?:万分之|萬分之)(\d+(?:\.\d+)?)", compacted)
    if daily_wan_match:
        return {
            "type": "daily_percentage",
            "base": "unpaid_amount",
            "rate": float(daily_wan_match.group(1)) / 10000,
            "party": party,
            "beneficiary": beneficiary,
            "direction": direction,
        }

    daily_rate_match = re.search(r"(?:每日|每天|按日|逾期天数|逾期日数)[^，。；;]{0,20}(?:的)?(\d+(?:\.\d+)?)\s*[%％]", compacted)
    if daily_rate_match:
        return {
            "type": "daily_percentage",
            "base": "unpaid_amount",
            "rate": float(daily_rate_match.group(1)) / 100,
            "party": party,
            "beneficiary": beneficiary,
            "direction": direction,
        }

    total_price_match = re.search(r"(?:合同总价|总价款|合同价款)[^，。；;]{0,12}(?:的)?(\d+(?:\.\d+)?)\s*[%％]", compacted)
    if total_price_match:
        return {
            "type": "contract_value_percentage",
            "base": "contract_value",
            "rate": float(total_price_match.group(1)) / 100,
            "party": party,
            "beneficiary": beneficiary,
            "direction": direction,
        }

    unpaid_match = re.search(r"(?:欠款|未付金额|未付款|欠付金额|应付未付金额)[^，。；;]{0,12}(?:的)?(\d+(?:\.\d+)?)\s*[%％]", compacted)
    if unpaid_match:
        return {
            "type": "unpaid_amount_percentage",
            "base": "unpaid_amount",
            "rate": float(unpaid_match.group(1)) / 100,
            "party": party,
            "beneficiary": beneficiary,
            "direction": direction,
        }

    return None
