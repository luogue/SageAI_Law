"""Source-bound employment dates and conditional occupational protection."""
import calendar
from datetime import date, timedelta
import re

from review_v2.element_resolution import conditional_element
from review_v2.lease_semantics import corpus_facts, requirement

DATE = r"(\d{4})[年/-](\d{1,2})[月/-](\d{1,2})日?"
RANGE = DATE + r"起?\s*(?:至|到)\s*" + DATE


def date_range(text, label):
    match = re.search(label + r"\s*[：:]?\s*自?" + RANGE, text)
    if not match:
        return None
    try:
        start, end = date(*map(int, match.groups()[:3])), date(*map(int, match.groups()[3:]))
        return (start, end) if start <= end else None
    except ValueError:
        return None


def add_months(start, months):
    year, month = divmod(start.year * 12 + start.month - 1 + months, 12)
    return date(year, month + 1, min(start.day, calendar.monthrange(year, month + 1)[1]))


def probation_dates(text):
    contract = date_range(text, r"(?:劳动)?合同期限")
    probation = date_range(text, "试用期")
    return contract, probation


def safety_condition(clauses):
    absent = corpus_facts(clauses, [requirement("hazard_absent", "岗位无职业危害",
        r"(?:本岗位|该岗位)?(?:不属于存在|不存在|不涉及|无)职业(?:病)?危害(?:因素)?",
        r"职业(?:病)?危害[：:]\s*(?:无|不涉及)")])["hazard_absent"]
    present = corpus_facts(clauses, [requirement("hazard_present", "岗位存在职业危害",
        r"(?<!不)(?<!不属于)(?:存在|接触|涉及)职业(?:病)?危害",
        r"(?:对|将)职业(?:病)?危害.{0,15}(?:如实)?告知",
        r"职业(?:病)?危害(?:因素)?[：:]\s*(?:粉尘|噪声|有毒|辐射|化学)")])["hazard_present"]
    # A denial containing “不属于存在” must not also establish the trigger.
    present = [row for row in present if not any(row['text'] == other['text'] for other in absent)]
    prerequisite = None if absent and present else False if absent else True if present else None
    return prerequisite, absent + present


def resolve_requirements(node, requirements, clauses):
    if node != "employment_safety":
        return requirements, []
    prerequisite, sources = safety_condition(clauses)
    health = requirements[1]
    facts = corpus_facts(clauses, [health])[health['element_id']]
    condition = conditional_element(health['element_id'], health['proposition'], prerequisite, facts,
        prerequisite_fact="工作岗位存在职业病危害因素",
        verification_instruction="核实岗位是否存在职业病危害因素，再确定告知和职业健康保护义务。")
    condition['prerequisite_evidence'] = sources
    condition['source_clause_ids'] = [r['clause_id'] for r in sources]
    if prerequisite is True:
        condition['proposition'] = health['proposition']
        return requirements, [condition]
    return [row for row in requirements if row['element_id'] != health['element_id']], [condition]


def project_conditions(item):
    """Retain condition decisions alongside normal element evidence projections."""
    conditions = item.decision_trace.get('priority_conditional_elements', [])
    for condition in conditions:
        existing = next((row for row in item.coverage_elements if row['element_id'] == condition['element_id']), None)
        if existing is not None:
            existing.update({key: condition[key] for key in (
                'conditional_element', 'prerequisite_status', 'prerequisite_fact',
                'prerequisite_evidence', 'risk_relevant', 'verification_instruction')})
        else:
            item.coverage_elements.append(dict(condition))
