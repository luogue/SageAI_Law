"""Judicial-protection assessment, separate from contractual completeness.

Reference intervals are evidence, not timeless constants. Unknown/future dates
never inherit the latest known quote. Different monetary bases remain symbolic
until a verified ledger supplies their ratio; percent numbers alone cannot add.
"""
import json
import os
import re
from datetime import date
from pathlib import Path


def reference_for(corpus, *, today=None, reference=None):
    today = today or date.today()
    hits = re.findall(r'(?:签署日期|签订日期|合同成立日期|成立日期|签约日期)[：:\s]*(\d{4})[年/-](\d{1,2})[月/-](\d{1,2})日?', corpus)
    dates = []
    for parts in hits:
        try:
            dates.append(date(*map(int, parts)))
        except ValueError:
            pass
    formed = max(dates) if dates else None
    return reference_for_date(formed, today=today, reference=reference)


def reference_for_date(formed, *, today=None, reference=None):
    """Same reference policy; the verified path supplies a typed date, never prose."""
    today = today or date.today()
    out = {'formation_date': formed.isoformat() if formed else None,
           'status': 'FORMATION_DATE_UNKNOWN', 'one_year_percent': None}
    if not formed:
        return out
    if formed > today:
        return dict(out, status='FUTURE_FORMATION_DATE')
    if reference is None:
        path = Path(os.environ.get('LPR_REFERENCE_FILE', Path(__file__).with_name('lpr_reference.json')))
        try:
            reference = json.loads(path.read_text(encoding='utf-8'))
        except (OSError, ValueError):
            return dict(out, status='REFERENCE_DATA_UNAVAILABLE')
    for entry in reference.get('intervals', []):
        if entry.get('source') and entry['effective_from'] <= formed.isoformat() < entry['valid_until_exclusive']:
            return dict(out, status='VERIFIED', one_year_percent=entry['one_year_percent'],
                        source=entry['source'], version=reference.get('version'), interval=entry)
    return dict(out, status='REFERENCE_DATA_UNAVAILABLE')


def assess(costs, corpus, *, today=None, reference=None, performance_facts=None):
    benchmark = reference_for(corpus, today=today, reference=reference)
    exclusive = bool(re.search(r'择一|选择其一|不得同时主张|不一并主张|不得同时计收|不同时计收', corpus))
    return assess_values(costs, benchmark, exclusive=exclusive, performance_facts=performance_facts)


def assess_values(costs, benchmark, *, exclusive, performance_facts=None):
    """Existing deterministic legal arithmetic, independent of fact extraction."""
    cap = benchmark['one_year_percent'] * 4 if benchmark['one_year_percent'] is not None else None
    components = costs['components']
    # A rate belongs to its own base and accrual period. Retain symbolic
    # amounts (e.g. unpaid_interest * daily_rate * overdue_days) for review.
    groups = {}
    unresolved = []
    normalized_components = []
    for original in components:
        c = dict(original)
        ledger = performance_facts or {}
        if c.get('base') == 'UNPAID_INTEREST' and ledger.get('same_accrual_window') is True and ledger.get('principal', 0) > 0 and ledger.get('unpaid_interest', -1) >= 0:
            ratio = ledger['unpaid_interest'] / ledger['principal']
            c['base'] = 'PRINCIPAL'
            c['normalization_ratio'] = ratio
            c['annual_percent_estimate'] = c['annual_percent_estimate'] * ratio if c.get('annual_percent_estimate') is not None else None
        normalized_components.append(c)
        if c.get('base') != 'PRINCIPAL' or c.get('annual_percent_estimate') is None:
            unresolved.append(c['evidence_id'])
            continue
        period = c['scope']
        if period not in {'LOAN_TERM', 'OVERDUE', 'UNTIL_REPAYMENT'}:
            unresolved.append(c['evidence_id'])
            continue
        groups.setdefault(period, []).append(c)
    regular = groups.get('LOAN_TERM', []) + groups.get('UNTIL_REPAYMENT', [])
    overdue = groups.get('OVERDUE', [])
    def total(rows):
        # Repeated quotations are alternatives, not separate charges.
        return sum(max(c['annual_percent_estimate'] for c in rows if c.get('charge_key',c['kind']) == key)
                   for key in {c.get('charge_key',c['kind']) for c in rows})
    regular_total, overdue_total = total(regular), total(overdue)
    joint = costs['stacking'] == 'CUMULATIVE'
    if exclusive:
        overdue_total = max((c['annual_percent_estimate'] for c in overdue), default=0)
    if joint and not exclusive:
        overdue_total += regular_total
    elif regular and overdue and costs['stacking'] not in {'REPLACEMENT'}:
        # Absence of an express replacement is not proof of accumulation.
        unresolved += [c['evidence_id'] for c in regular]
    totals = {'loan_term_principal_annual_percent': regular_total,
              'overdue_principal_annual_percent': overdue_total}
    capped = costs['combined_contractual_cap']
    exceeded = cap is not None and max(totals.values()) > cap + 1e-9 and not capped
    if capped:
        status, reason = 'PASS', '合同已明确以合同成立时一年期LPR四倍限制合计可主张金额；适用数值以成立时公布值为准。'
    elif exceeded:
        status, reason = 'RISK', '同基数、同期间可主张金额超过合同成立时一年期LPR四倍，超过司法保护上限的部分可能不获法院支持。'
    elif cap is None:
        status, reason = 'PENDING', '需以合同成立时一年期LPR四倍核验司法保护范围；成立日期或该期LPR尚未核实，未写上限兜底条款本身不构成合同缺陷。'
    elif unresolved or not components:
        status, reason = 'PENDING', '需结合实际本金、未付利息余额及计收期间核验同期间合计金额；不同计算基数的百分比不能直接相加。'
    else:
        status, reason = 'PASS', '已按合同成立时一年期LPR四倍核验可统一期间及基数的收费公式，未超过司法保护上限；无需另写兜底条款。'
    return {'status': status, 'reason': reason, 'reference': benchmark, 'cap_percent': cap,
            'normalized_components': normalized_components,
            'normalized_totals': totals, 'unresolved_evidence_ids': sorted(set(unresolved)),
            'contract_missing_risk': False, 'text_coverage': 'PASS' if components and all(c.get('annual_percent_estimate') is not None for c in components) else 'UNRESOLVED',
            'existing_clause_risk': exceeded, 'exclusive_claims': exclusive}
