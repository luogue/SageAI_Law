"""Scenario and economic impact calculation for review v2."""

from __future__ import annotations

import re
from typing import Any, Dict, Optional


def numeric_amount(value: Optional[str]) -> Optional[float]:
    if not value:
        return None
    cleaned = str(value).replace(",", "").replace("，", "")
    match = re.search(r"\d+(?:\.\d+)?", cleaned)
    return float(match.group(0)) if match else None


def penalty_scenarios(formula: Dict[str, Any], monthly_rent_value: Optional[str], *, daily_rent_value: Optional[str] = None) -> Dict[str, Any]:
    monthly_rent = numeric_amount(monthly_rent_value)
    if not formula or not monthly_rent:
        return {}

    multiplier = formula.get("multiplier") or 1
    base = formula.get("base")
    explicit_daily_rent = numeric_amount(daily_rent_value)
    daily_rent = explicit_daily_rent or monthly_rent / 30
    estimated = explicit_daily_rent is None
    scenarios: Dict[str, float] = {}
    cases = []

    if base in {"remaining_days_rent", "remaining_term_rent"}:
        for days in (30, 90, 180, 300):
            estimated_penalty = round(daily_rent * days * multiplier, 2)
            remaining_rent = round(daily_rent * days, 2)
            scenarios[f"remaining_{days}_days"] = estimated_penalty
            cases.append(
                {
                    "remaining_days": days,
                    "estimated_penalty": estimated_penalty,
                    "monthly_rent_multiple": round(estimated_penalty / monthly_rent, 2),
                    "penalty_monthly_rent_multiple": round(estimated_penalty / monthly_rent, 2),
                    "penalty_to_monthly_rent_ratio": round(estimated_penalty / monthly_rent, 2),
                    "remaining_rent_ratio": round(estimated_penalty / remaining_rent, 2) if remaining_rent else None,
                    "penalty_remaining_rent_ratio": round(estimated_penalty / remaining_rent, 2) if remaining_rent else None,
                    "penalty_to_remaining_rent_ratio": round(estimated_penalty / remaining_rent, 2) if remaining_rent else None,
                    "estimated": estimated,
                    "calculation_basis": "monthly_rent / 30" if estimated else "contract_daily_rent",
                    "calculation_note": "按月租金/30估算日租金，非合同精确金额。" if estimated else "按合同明确日租金计算。",
                }
            )
    elif base == "monthly_rent":
        estimated_penalty = round(monthly_rent * multiplier, 2)
        scenarios["monthly_rent_multiplier"] = estimated_penalty
        cases.append(
            {
                "remaining_days": None,
                "estimated_penalty": estimated_penalty,
                "monthly_rent_multiple": round(estimated_penalty / monthly_rent, 2),
                "penalty_monthly_rent_multiple": round(estimated_penalty / monthly_rent, 2),
                "penalty_to_monthly_rent_ratio": round(estimated_penalty / monthly_rent, 2),
                "remaining_rent_ratio": None,
                "penalty_remaining_rent_ratio": None,
                "penalty_to_remaining_rent_ratio": None,
                "estimated": False,
                "calculation_basis": "monthly_rent",
                "calculation_note": "按合同月租金倍数计算。",
            }
        )

    return {
        "formula": formula,
        "monthly_rent": monthly_rent,
        "scenarios": scenarios,
        "cases": cases,
        "estimation_method": "若合同未单列日租金，使用月租金/30估算；估算值仅用于风险校准。",
    }


def economic_impact_for_penalty(scenarios: Dict[str, Any]) -> str:
    values = list((scenarios.get("scenarios") or {}).values())
    monthly_rent = scenarios.get("monthly_rent") or 0
    if not values or not monthly_rent:
        return "none"
    max_penalty = max(values)
    if max_penalty >= monthly_rent * 8:
        return "high"
    if max_penalty >= monthly_rent * 3:
        return "medium"
    return "low"


def economic_impact_detail_for_penalty(scenarios: Dict[str, Any]) -> Dict[str, Any]:
    cases = scenarios.get("cases") or []
    monthly_rent = scenarios.get("monthly_rent") or 0
    values = [case.get("estimated_penalty") for case in cases if case.get("estimated_penalty") is not None]
    if not values or not monthly_rent:
        return {"level": "none"}
    max_penalty = max(values)
    max_case = max(cases, key=lambda case: case.get("estimated_penalty") or 0)
    contract_value = monthly_rent * 12
    level = economic_impact_for_penalty(scenarios)
    if max_penalty >= monthly_rent * 12:
        level = "critical"
    return {
        "estimated_max_loss": max_penalty,
        "amount_estimate": max_penalty,
        "relative_to_monthly_payment": round(max_penalty / monthly_rent, 2),
        "relative_to_contract_value": round(max_penalty / contract_value, 2) if contract_value else None,
        "time_amplifying": bool((scenarios.get("formula") or {}).get("base") in {"remaining_term_rent", "remaining_days_rent"}),
        "uncapped": False,
        "level": level,
        "max_case": max_case,
    }
