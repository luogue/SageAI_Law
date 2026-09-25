"""Text-bound financing costs. Annualizations are estimates, not verified LPR.

No current LPR is substituted for the rate at contract formation. A contractual
ceiling is distinguished from external verification of the applicable ceiling.

Legal reference: SPC private lending interpretation, articles 28–29 (2020
December revision), https://www.court.gov.cn/zixun/xiangqing/282621.html.
"""
import re

from review_v2.loan_facts import compact, units, financing_charge
from review_v2.loan_semantics import rate_adjustment, concept_facts


EXTERNAL_FACT_NODES = {
    "loan_relending_bank_loan_invalid": r"套取.{0,12}(?:金融机构|银行).{0,12}(?:转贷|转借)|(?:银行|金融机构)贷款.{0,12}(?:转贷|转借)",
    "loan_professional_lender_invalid": r"职业放贷|经常性.{0,15}(?:放贷|发放贷款)|向不特定.{0,12}(?:放贷|出借)",
    "loan_illegal_purpose_known_invalid": r"明知.{0,20}(?:违法|犯罪)|借款用于.{0,12}(?:赌博|走私|贩毒)",
}
COST_NODES = {"loan_interest_lpr_cap"}
COLLECTION_NODES = {"loan_collection_ack_limitation_interruption", "loan_collection_record_attachment"}


def row(clause, quote, index):
    return {"clause_id": clause.clause_id, "text": quote, "quote": quote,
            "location": clause.location, "section_type": clause.section_type,
            "block_type": clause.block_type, "source_type": "CONTRACT_TEXT",
            "evidence_id": f"{clause.clause_id}-COST-{index}",
            "entailment_status": "SUPPORTS", "semantic_score": 1.0}


def analyze_costs(clauses):
    components, evidence, seen = [], [], set()
    relative_rates = []
    source = list(units(clauses))
    corpus = "".join(compact(q) for _, q in source)
    # Period belongs to the nearby rate, not to the whole document.
    rate_re = re.compile(r"(?:(年|月|日)利率|每(?:逾期)?一?(日|天)|按(日|月|年)|月息|年息)[^。；;\n%％‰]{0,24}?(\d+(?:\.\d+)?)\s*([%％‰])")
    for clause, quote in source:
        text = compact(quote)
        related = False
        adjustment = rate_adjustment(quote)
        if adjustment and concept_facts('overdue_rate',quote):
            relative_rates.append((clause,quote,adjustment))
        for match in rate_re.finditer(text):
            if adjustment and match.start()<adjustment['end'] and match.end()>adjustment['start']:
                continue  # 150% of another rate is not a 150% annual rate.
            period = next((x for x in match.groups()[:3] if x), "月" if "月息" in match.group() else "年")
            period = "日" if period == "天" else period
            prefix = text[max(0, match.start()-24):match.start()]
            local_start = max(text.rfind("，", 0, match.start()), text.rfind(",", 0, match.start())) + 1
            local_end = re.search(r"[，,]", text[match.end():])
            local = text[local_start:match.end() + local_end.start() if local_end else len(text)]
            overdue = bool(re.search(r"逾期|罚息|违约", local))
            kind = "overdue_interest" if overdue else "regular_interest"
            if "违约金" in local:
                kind = "penalty"
            elif financing_charge(local):
                kind = "financing_fee"
            fee_name = re.search(r"服务费|管理费|咨询费|手续费|综合费率|融资费|账户维护费", local)
            charge_key = fee_name.group() if kind == "financing_fee" and fee_name else kind
            value = float(match.group(4)) / (10 if match.group(5) == "‰" else 1)
            base = 'UNPAID_INTEREST' if re.search(r'(?:应付未付|届期未付|到期未支付|逾期未付|未付|未支付)利息', text) else 'PRINCIPAL' if ('本金' in text or kind in {'regular_interest','overdue_interest'}) else 'UNRESOLVED'
            scope = 'OVERDUE' if overdue else 'LOAN_TERM'
            if kind == 'regular_interest' and re.search(r'利息自[^。；]{0,60}(?:本金|借款)[^。；]{0,8}(?:归还|清偿|还款)', compact(clause.text)):
                scope = 'UNTIL_REPAYMENT'
            key = (kind, charge_key, period, value, base, scope)
            if key not in seen:
                components.append({"kind": kind, "period": period, "percent": value,
                                   "charge_key": charge_key,
                                   "annual_percent_estimate": round(value * {"年": 1, "月": 12, "日": 365}[period], 6),
                                   "scope": scope, "base": base,
                                   "amount_formula": f"{base} * {value}/100 * accrual_{period}",
                                   "evidence_id": f"{clause.clause_id}-COST-{len(evidence)+1}"})
                seen.add(key)
            related = True
        fee = financing_charge(quote)
        penalty = bool(re.search(r"(?:支付|承担|计收).{0,18}违约金|违约金.{0,12}(?:为|按|计收)", text)) and not bool(re.search(r"(?:不再|不得|无需|不另|免除|不收取).{0,8}(?:支付|承担|计收)?违约金", text))
        if (fee or penalty) and not any(c["evidence_id"] == f"{clause.clause_id}-COST-{len(evidence)+1}" and c["kind"] in {"penalty", "financing_fee"} for c in components):
            components.append({"kind": "financing_fee" if fee else "penalty", "scope": "UNRESOLVED",
                               "annual_percent_estimate": None, "evidence_id": f"{clause.clause_id}-COST-{len(evidence)+1}"})
            related = True
        if related or re.search(r"合计|累计|不再.{0,8}利息|仅.{0,8}逾期利息|司法保护上限|LPR", text, re.I):
            evidence.append(row(clause, quote, len(evidence)+1))
    regular = [c for c in components if c["kind"] == "regular_interest"]
    references={(c['period'],c['percent']) for c in regular}
    for clause,quote,adjustment in relative_rates:
        period,value=next(iter(references)) if len(references)==1 else (None,None)
        derived=value*adjustment['multiplier'] if value is not None else None
        e=row(clause,quote,len(evidence)+1)
        evidence.append(e)
        components.append({'kind':'overdue_interest','charge_key':'overdue_interest',
                           'period':period,'percent':derived,
                           'annual_percent_estimate':round(derived*{'年':1,'月':12,'日':365}[period],6) if derived is not None else None,
                           'scope':'OVERDUE','base':'PRINCIPAL','evidence_id':e['evidence_id'],
                           'reference_evidence_ids':[c['evidence_id'] for c in regular],
                           'rate_adjustment':adjustment,'amount_formula':f"PRINCIPAL * CONTRACT_REGULAR_RATE * {adjustment['multiplier']} * accrual_period"})
    overdue = [c for c in components if c["kind"] == "overdue_interest"]
    extra = any(c["kind"] in {"penalty", "financing_fee"} for c in components)
    cumulative = bool(re.search(r"(?:逾期|利息|罚息)[^。；]{0,45}(?:另行|另加|同时|叠加|累计|并继续)[^。；]{0,25}(?:利息|利率|违约金|费用)", corpus))
    cumulative = cumulative or bool(re.search(r'(?:逾期利息|罚息)[^。；]{0,15}(?:借期|正常|原)利息[^。；]{0,8}(?:同时|一并|累计)计收', corpus))
    if re.search(r'(?:不得|不应|不)(?:同时|一并|累计)计收', corpus):
        cumulative = False
    replacement = bool(re.search(r"逾期[^。；]{0,40}(?:不再|停止)[^。；]{0,15}(?:借期|原|正常|借款)利息|逾期[^。；]{0,15}仅[^。；]{0,15}(?:逾期利息|罚息)|(?:借期|正常)利息[^。；]{0,20}(?:仅计至|计算至)[^。；]{0,12}到期", corpus))
    cap_pattern = r"(?:利息|利率|罚息)[^。；]{0,90}(?:合计|总计|总和|累计)[^。；]{0,30}(?:不超过|不得超过|为限)[^。；]{0,35}(?:合同成立时|成立时)[^。；]{0,20}(?:一年期|1年期)[^。；]{0,30}(?:四倍|4倍)"
    cap_evidence = [e["evidence_id"] for e in evidence if re.search(cap_pattern, compact(e["quote"]), re.I)
                    and (not extra or re.search(r"违约金.*(?:费用|收费)|全部融资成本", e["quote"]))]
    if not overdue and not extra:
        cap_evidence += [e['evidence_id'] for e in evidence if re.search(
            r'(?:利息|利率)[^。；]{0,25}(?:不超过|不得超过|为限)[^。；]{0,35}(?:合同成立时|成立时)[^。；]{0,20}(?:一年期|1年期)[^。；]{0,30}(?:四倍|4倍)', compact(e['quote']), re.I)]
    combined_cap = bool(cap_evidence)
    # Ordinary term interest and overdue interest are not automatically
    # simultaneous. Preserve ambiguity, but never convert it to a sum.
    limited_regular = all(c['scope']=='LOAN_TERM' for c in regular)
    replacement = replacement or bool(regular and overdue and limited_regular)
    ambiguous = bool(regular and overdue and not replacement and not cumulative)
    result = {"components": components, "evidence": evidence,
              "stacking": "CUMULATIVE" if cumulative else "REPLACEMENT" if replacement else "AMBIGUOUS" if ambiguous else "SINGLE",
              "regular_scope_explicit": limited_regular,
              "combined_contractual_cap": combined_cap, "cap_evidence_ids": cap_evidence,
              "conflicting_rates": any(len({(c.get('period'),c.get('percent')) for c in components if c['kind']==kind})>1 for kind in ('regular_interest','overdue_interest')),
              "conflicting_scope": cumulative and replacement,
              "unquantified_components": [c for c in components if c.get('annual_percent_estimate') is None]}
    from review_v2.lpr_protection import assess
    protection = assess(result, corpus)
    result.update(judicial_protection=protection,
                  lpr_verification=protection['reference']['status'],
                  calculation_status='NORMALIZED_BY_BASE_AND_PERIOD',
                  potential_annual_percent_estimate=None,
                  needs_check=protection['status']=='PENDING',
                  existing_clause_risk=protection['existing_clause_risk'],
                  reason=protection['reason'])
    return result


def external_assessment(node, clauses):
    hits = []
    for clause, quote in units(clauses):
        text = compact(quote)
        match = re.search(EXTERNAL_FACT_NODES[node], text)
        if match and not re.search(r"不得|禁止|不属于|不存在|并非|承诺|保证|未发现|无", text[max(0, match.start()-16):match.start()]):
            hits.append(row(clause, quote, len(hits)+1))
    return {"text_assessment": "RISK_INDICATOR_FOUND" if hits else "NO_RISK_INDICATOR_FOUND",
            "external_fact_status": "NOT_VERIFIED", "evidence": hits,
            "reason": "合同文本发现需核验的风险线索，外部事实尚未核实。" if hits else "合同文本未发现异常，相关实际事实需结合资金来源、历史放贷行为、实际用途等核验；不能据此确认相关风险事实不存在。"}
