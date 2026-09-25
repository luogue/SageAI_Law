"""Source-bound adapter to the existing coverage, finding and report pipeline."""
from copy import deepcopy
import re

from review_v2.priority_contract_types import PRIORITY_TYPES
from review_v2.priority_checklist_helpers import PROFILES, CONDITIONS, ADVERSE
from review_v2.lease_semantics import corpus_facts


def applicability(text, checkpoint, contract_type):
    if contract_type not in PRIORITY_TYPES:
        return None
    node = checkpoint.node_id
    if node == "security_company_authority":
        corporate = re.search(r"(?:抵押人|出质人)[^。；\n]{0,60}(?:公司|企业)", text)
        if not corporate:
            return False, "未识别公司作为抵押人或出质人，公司担保决议专项审查不触发；主体及处分权限仍独立核对。"
    if node.startswith("employment_noncompete") and contract_type != "non_compete":
        if not re.search(r"竞业限制|竞业禁止", text) or re.search(r"(?:不约定|不设置|不承担|不适用)竞业(?:限制|禁止)", text):
            return False, "未约定竞业限制，不要求新增该可选安排。"
    if node == "employment_general_penalty" and contract_type == "confidentiality" and not re.search(r"劳动者|用人单位|雇员|员工", text):
        return False, "未识别劳动用工关系，一般商业保密协议不适用劳动者违约金限制。"
    if node == "employment_noncompete_term":
        in_service_only = re.search(r"竞业限制.{0,20}(?:仅适用|仅限).{0,8}在职|仅在职期间.{0,15}竞业限制", text)
        if in_service_only:
            return False, "明确仅在职期间适用竞业限制，离职按月补偿及两年上限专项不适用。"
        return True, "核对离职竞业期限及补偿；未交代适用期间时不能直接按在职竞业豁免。"
    if node == "equity_capital_increase" and contract_type != "capital_increase" and not re.search(r"增资|新增注册资本|新增出资", text):
        return False, "未涉及新增资本认缴，不要求补写增资条款。"
    if node == "equity_transfer_restrictions" and contract_type == "shareholders" and not re.search(r"股权转让|对外转让|向股东以外", text):
        return False, "未约定股权转让安排，暂不触发转让程序审查。"
    terms = CONDITIONS.get(node, ())
    if terms:
        source = re.sub(r"(?:不约定|不设置|不适用|无)(?:试用期|服务期|专项培训|回购|业绩承诺|反稀释)", "", text)
        if not any(t in source for t in terms):
            return False, "未触发专项场景：" + "、".join(terms) + "。"
    return True, "专项清单及合同场景适用。"


def _number(value):
    if value.isdigit():
        return int(value)
    if value in {"两": 2, "十": 10}:
        return {"两": 2, "十": 10}[value]
    digits = {c: i for i, c in enumerate("零一二三四五六七八九")}
    if "十" in value:
        a, b = value.split("十", 1)
        return digits.get(a, 1) * 10 + digits.get(b, 0)
    return digits.get(value, 0)


def probation_risk(text):
    """Compare explicit terms/calendar dates, never infer risk from a topic."""
    from review_v2.employment_facts import probation_dates, add_months
    from review_v2.adverse_evidence import proposition_polarity
    from datetime import timedelta
    number = r"([\d一二两三四五六七八九十]+)"
    contract_dates, trial_dates = probation_dates(text)
    probation = re.search(r"试用期(?:为|：|:)?\s*" + number + r"个?月", text)
    if not trial_dates and not probation:
        return False
    trial_match = re.search(r"试用期\s*[：:]?\s*自?\d{4}[年/-]", text) if trial_dates else probation
    if trial_match:
        boundary = max(text.rfind(c, 0, trial_match.start()) for c in "。；;\n") + 1
        local = text[boundary:]
        if proposition_polarity(local, trial_match.start() - boundary, trial_match.end() - boundary) != "AFFIRMED":
            return False
    limit = 6
    term = re.search(r"(?:劳动)?合同期限(?:为|：|:)?\s*" + number + r"个?(月|年)", text)
    if contract_dates:
        start, end = contract_dates
        exclusive_end = end + timedelta(days=1)
        limit = (0 if exclusive_end < add_months(start, 3) else
                 1 if exclusive_end < add_months(start, 12) else
                 2 if exclusive_end < add_months(start, 36) else 6)
    elif term:
        duration = _number(term[1]) * (12 if term[2] == "年" else 1)
        limit = 0 if duration < 3 else 1 if duration < 12 else 2 if duration < 36 else 6
    elif "工作任务为期限" in text:
        limit = 0
    if trial_dates:
        return trial_dates[1] + timedelta(days=1) > add_months(trial_dates[0], limit)
    return _number(probation[1]) > limit


def adverse_evidence(node, clauses):
    from review_v2.adverse_evidence import direct_evidence
    positive, _ = direct_evidence(clauses, ADVERSE.get(node, ()), require_assertion=False)
    if node == "employment_probation_limit":
        corpus = "\n".join(c.text for c in clauses if c.section_type in {"正式合同条款", "附件"})
        if probation_risk(corpus):
            positive = [c.to_public_dict() for c in clauses if re.search(r"试用期|合同期限|自\d{4}年", c.text) and c.section_type in {"正式合同条款", "附件"}]
    return positive


def judge(checkpoint, clauses):
    """Initial judgments also use exact evidence, including when LLM is enabled."""
    from review_v2.semantic_reviewer import ReviewJudgment
    if checkpoint.node_id not in ADVERSE and checkpoint.node_id not in PROFILES:
        return None
    if checkpoint.node_id in ADVERSE:
        evidence = adverse_evidence(checkpoint.node_id, clauses)
        state = "风险条款" if evidence else "通过"
        reason = checkpoint.risk_point_present if evidence else "全文未发现该项禁止性风险约定；防范和否定表述不作为风险证据。"
    else:
        from review_v2.employment_facts import resolve_requirements
        elements, conditions = resolve_requirements(checkpoint.node_id, PROFILES[checkpoint.node_id], clauses)
        facts = corpus_facts(clauses, elements)
        evidence = [row for element in elements for row in facts[element["element_id"]]]
        missing = [e["proposition"] for e in elements if not facts[e["element_id"]]]
        state = "通过" if not missing else "部分覆盖" if evidence else "缺失"
        reason = ("合同原文覆盖全部专项要素。" if not missing else "未找到明确约定：" + "、".join(missing) + "。")
        if any(row['prerequisite_status'] == 'FALSE' for row in conditions):
            reason += "原文明确岗位无职业危害，职业危害专项要素不适用；一般劳动保护仍独立审查。"
        if any(row['prerequisite_status'] == 'UNKNOWN' for row in conditions):
            reason += "岗位职业危害情况待核实，未将条件不明的专项义务判为合同缺失。"
    return ReviewJudgment(
        coverage_status=state, risk_level="低" if state == "通过" else checkpoint.risk_level,
        status=state, risk_point_description=reason, evidence_clauses=evidence,
        evidence_location="；".join(dict.fromkeys(r.get("location", "") for r in evidence)),
        reasoning_summary=reason, matched_terms=[t for t in checkpoint.terms if any(t in r.get("text", "") for r in evidence)],
        issue_type={"通过": "通过", "部分覆盖": "条款缺陷", "缺失": "完全缺失", "风险条款": "风险条款"}[state],
    )


def apply(items, clauses, checklist):
    by_node = {row.node_id: row for row in checklist}
    for item in items:
        if item.coverage_status == "不适用":
            continue
        checkpoint = by_node[item.node_id]
        judgment = judge(checkpoint, clauses)
        if judgment is None:
            continue
        for name in ("coverage_status", "risk_level", "status", "risk_point_description", "evidence_clauses", "evidence_location", "reasoning_summary", "matched_terms", "issue_type"):
            setattr(item, name, deepcopy(getattr(judgment, name)))
        item.judge_source = "rule_fallback"
        item.fallback_reason = "专项原文要素核验"
        item.needs_manual_review = False
        if item.node_id in PROFILES:
            from review_v2.employment_facts import resolve_requirements
            elements, conditions = resolve_requirements(item.node_id, PROFILES[item.node_id], clauses)
            item.decision_trace["semantic_requirements"] = deepcopy(elements)
            item.decision_trace["priority_conditional_elements"] = deepcopy(conditions)
        elif item.node_id in ADVERSE and judgment.coverage_status == "风险条款":
            # Predicate/calculation verification already established the adverse
            # fact. Bind that exact source span to an element before the shared
            # evidence layer; generic topic similarity must not erase the fact.
            element_id = item.node_id + "_adverse"
            item.decision_trace["semantic_requirements"] = [{
                "element_id": element_id, "proposition": checkpoint.title,
                "semantic_patterns": tuple(re.escape(row["text"]) for row in judgment.evidence_clauses),
            }]
            item.decision_trace["priority_adverse_verification"] = {
                "method": "DIRECT_PREDICATE_OR_DATE_CALCULATION",
                "predicate_patterns": list(ADVERSE[item.node_id]),
                "source_clause_ids": [row["clause_id"] for row in judgment.evidence_clauses],
            }
            for row in item.evidence_clauses:
                row["supports_element_ids"] = [element_id]
        elif item.node_id in ADVERSE:
            item.decision_trace.pop("semantic_requirements", None)
        item.decision_trace["priority_specialized_evaluation"] = True
        group = {
            "employment_probation_limit": "employment_probation",
            "employment_illegal_waiver": "employment_insurance",
            "security_publicity_waiver": "security_publicity",
            "mortgage_publicity": "security_publicity",
            "pledge_movable_delivery": "security_publicity",
            "pledge_equity_registration": "security_publicity",
            "pledge_rights_publicity": "security_publicity",
        }.get(item.node_id, item.node_id)
        item.decision_trace["finding_parent_group"] = group
        item.decision_trace["underlying_risk_identity"] = {"fact": group, "scope": "primary_contract", "remedy": "verify_and_complete_" + group}
        item.decision_trace.pop("element_evidence_truth", None)
    return items
