"""Text-bound financing costs. Annualizations are estimates, not verified LPR.

No current LPR is substituted for the rate at contract formation. A contractual
ceiling is distinguished from external verification of the applicable ceiling.

Legal reference: SPC private lending interpretation, articles 28–29 (2020
December revision), https://www.court.gov.cn/zixun/xiangqing/282621.html.
"""
import re

from review_v2.loan_facts import compact, units, financing_charge


EXTERNAL_FACT_NODES = {
    "loan_relending_bank_loan_invalid": r"套取.{0,12}(?:金融机构|银行).{0,12}(?:转贷|转借)|(?:银行|金融机构)贷款.{0,12}(?:转贷|转借)",
    "loan_professional_lender_invalid": r"职业放贷|经常性.{0,15}(?:放贷|发放贷款)|向不特定.{0,12}(?:放贷|出借)",
    "loan_illegal_purpose_known_invalid": r"明知.{0,20}(?:违法|犯罪)|借款用于.{0,12}(?:赌博|走私|贩毒)",
}
COST_NODES = {"loan_interest_lpr_cap", "loan_overdue_interest"}
COLLECTION_NODES = {"loan_collection_ack_limitation_interruption", "loan_collection_record_attachment"}


def row(clause, quote, index):
    return {"clause_id": clause.clause_id, "text": quote, "quote": quote,
            "location": clause.location, "section_type": clause.section_type,
            "block_type": clause.block_type, "source_type": "CONTRACT_TEXT",
            "evidence_id": f"{clause.clause_id}-COST-{index}",
            "entailment_status": "SUPPORTS", "semantic_score": 1.0}


def analyze_costs(clauses):
    components, evidence, seen = [], [], set()
    source = list(units(clauses))
    corpus = "".join(compact(q) for _, q in source)
    # Period belongs to the nearby rate, not to the whole document.
    rate_re = re.compile(r"(?:(年|月|日)利率|每(?:逾期)?一?(日|天)|按(日|月|年)|月息|年息)[^。；;\n%％‰]{0,24}?(\d+(?:\.\d+)?)\s*([%％‰])")
    for clause, quote in source:
        text = compact(quote)
        related = False
        for match in rate_re.finditer(text):
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
            key = (kind, charge_key, period, value)
            if key not in seen:
                components.append({"kind": kind, "period": period, "percent": value,
                                   "charge_key": charge_key,
                                   "annual_percent_estimate": round(value * {"年": 1, "月": 12, "日": 365}[period], 6),
                                   "scope": "OVERDUE" if overdue else "FROM_DISBURSEMENT_UNTIL_UNSPECIFIED_END",
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
    overdue = [c for c in components if c["kind"] == "overdue_interest"]
    extra = any(c["kind"] in {"penalty", "financing_fee"} for c in components)
    cumulative = bool(re.search(r"(?:逾期|利息|罚息)[^。；]{0,45}(?:另行|另加|同时|叠加|累计|并继续)[^。；]{0,25}(?:利息|利率|违约金|费用)", corpus))
    replacement = bool(re.search(r"逾期[^。；]{0,40}(?:不再|停止)[^。；]{0,15}(?:借期|原|正常|借款)利息|逾期[^。；]{0,15}仅[^。；]{0,15}(?:逾期利息|罚息)|(?:借期|正常)利息[^。；]{0,20}(?:仅计至|计算至)[^。；]{0,12}到期", corpus))
    cap_pattern = r"(?:利息|利率|罚息)[^。；]{0,90}(?:合计|总计|总和|累计)[^。；]{0,30}(?:不超过|不得超过|为限)[^。；]{0,35}(?:合同成立时|成立时)[^。；]{0,20}(?:一年期|1年期)[^。；]{0,30}(?:四倍|4倍)"
    cap_evidence = [e["evidence_id"] for e in evidence if re.search(cap_pattern, compact(e["quote"]), re.I)
                    and (not extra or re.search(r"违约金.*(?:费用|收费)|全部融资成本", e["quote"]))]
    combined_cap = bool(cap_evidence)
    limited_regular = bool(re.search(r"借期内|到期前|借款期限内", corpus))
    # A combined ceiling bounds the amount; it does not decide which charges
    # accrue together. Scope ambiguity and amount compliance are separate.
    ambiguous = bool(regular and overdue and not replacement and not cumulative)
    unknown_extra = extra and not combined_cap
    conflicting_rates = any(len({(c.get("period"), c.get("percent")) for c in components if c["kind"] == kind}) > 1
                            for kind in ("regular_interest", "overdue_interest"))
    conflicting_scope = cumulative and replacement
    needs_check = ambiguous or unknown_extra or conflicting_rates or conflicting_scope or (bool(overdue) and not combined_cap)
    selected = (overdue if replacement and not cumulative else regular + overdue) + [c for c in components if c["kind"] in {"penalty", "financing_fee"}]
    # Different main/annex versions of the same rate are alternatives, never
    # two simultaneous charges. Keep the inconsistency as a separate risk.
    estimate = round(sum(max((c["annual_percent_estimate"] or 0) for c in selected if c.get("charge_key", c["kind"]) == key)
                         for key in {c.get("charge_key", c["kind"]) for c in selected}), 6)
    lpr_match = re.search(r"(?:合同成立时|成立时)[^。；]{0,12}(?:一年期|1年期)[^。；]{0,25}(?:LPR|贷款市场报价利率)(?:为|是|[:：])?(\d+(?:\.\d+)?)[%％]", corpus, re.I)
    declared_cap = float(lpr_match.group(1)) * 4 if lpr_match else None
    exceeds_declared_cap = declared_cap is not None and estimate > declared_cap
    needs_check = needs_check or exceeds_declared_cap
    reasons = []
    # Economic exposure warning, not a substitute for the verified legal cap:
    # a year's simple overdue charge reaches/exceeds the outstanding principal.
    high_cost_exposure=any(c['scope']=='OVERDUE' and (c.get('annual_percent_estimate') or 0)>=100 for c in components)
    for c in components:
        if c.get('percent') is not None and c['scope']=='OVERDUE':
            reasons.append(f"合同已有每{c['period']}{c['percent']:g}%的逾期责任约定，按单利折算年化约{c['annual_percent_estimate']:g}%；应审查该现有责任的司法保护范围，而非仅补写限额条款")
    if ambiguous:
        reasons.append("借期利率与逾期利率的时间范围或累计计收关系未明确，逾期期间可能叠加")
    if unknown_extra:
        reasons.append("违约金或融资性费用需要纳入同期间、同本金口径的合计成本")
    if conflicting_rates or conflicting_scope:
        reasons.append("正文与附件或不同条款的利率、替代计息及累计计收安排存在冲突")
    if cumulative:
        reasons.append("条款存在同时或另行计收安排，应合并核算逾期期间的融资成本")
    if exceeds_declared_cap:
        reasons.append("约定成本的年化估算高于合同声明的成立时一年期LPR四倍，数值约定与限额存在冲突；声明的LPR本身仍需核验")
    if needs_check:
        reasons.append("尚未以合同成立时一年期LPR四倍核验全部逾期融资成本；单项利率兜底不等于合计限额")
    return {"components": components, "evidence": evidence, "stacking": "CUMULATIVE" if cumulative else "REPLACEMENT" if replacement else "AMBIGUOUS" if ambiguous else "SINGLE_OR_CAPPED",
            "regular_scope_explicit": limited_regular, "combined_contractual_cap": combined_cap, "cap_evidence_ids": cap_evidence,
            "conflicting_rates": conflicting_rates, "conflicting_scope": conflicting_scope,
            "declared_lpr_cap_percent": declared_cap, "exceeds_declared_cap": exceeds_declared_cap,
            "lpr_verification": "NOT_EXTERNALLY_VERIFIED", "annualization_basis": "simple; monthly x12; daily x365; excludes unquantified fees",
            "calculation_status": "ESTIMATE_ONLY_REQUIRES_SAME_PERIOD_AND_PRINCIPAL", "unquantified_components": [c for c in components if c["annual_percent_estimate"] is None],
            "potential_annual_percent_estimate": estimate, "needs_check": needs_check,
            "existing_clause_risk": high_cost_exposure or exceeds_declared_cap,
            "reason": "；".join(reasons) + ("。" if reasons else "")}


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
