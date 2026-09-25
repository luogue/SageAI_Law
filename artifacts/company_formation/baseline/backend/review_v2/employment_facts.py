"""Source-bound employment dates and conditional occupational protection."""
import calendar
from datetime import date, timedelta
import re

from review_v2.element_resolution import conditional_element
from review_v2.lease_semantics import corpus_facts, requirement

DATE = r"(\d{4})[年/-](\d{1,2})[月/-](\d{1,2})日?"
RANGE = DATE + r"起?\s*(?:至|到)\s*" + DATE
START = r"(?:本合同|劳动合同|合同期限)(?:于|自|生效日期[为：:]?|起始日期[为：:]?)\s*" + DATE


def term_type(text):
    # Ignore inactive template alternatives and statutory explanations.
    active = re.sub(r'[^。；\n]*(?:不适用|未选择)[^。；\n]*', '', text)
    if re.search(r'(?:本合同为|合同类型[：:]|合同期限[为：:])\s*无固定期限|^无固定期限劳动合同', active):
        return 'INDEFINITE'
    if re.search(r'(?:本合同为|合同类型[：:]|(?:^|\n)\s*\d+[、.．])\s*以完成.{0,30}工作任务为期限', active):
        return 'TASK'
    if re.search(r'以完成[^。；\n]{3,120}为工作任务', active) and re.search(r'任务.{0,20}完成.{0,40}(?:终止|期限)', active):
        return 'TASK'
    return 'FIXED'


def actual_probation(text):
    """A denial does not create a probation; a separate concrete term prevails."""
    remaining = re.sub(r'[^。；\n]*(?:不约定|不设|不设置|无|不存在)试用期[^。；\n]*', '', text)
    return bool(probation_dates(remaining)[1] or re.search(
        r'试用期(?:为|：|:|自|至)\s*(?:\d|[一二两三四五六七八九十])|(?:乙方|劳动者)(?:应|须|必须).{0,12}试用', remaining))


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
    if not contract:
        contract = date_range(text, r"(?<!无)固定期限[。；：:]?\s*")
    if not contract:
        contract = date_range(text, r"本合同")
    if not contract and term_type(text) == 'FIXED':
        start_match = re.search(START, text)
        end_match = re.search(r'(?:终止日期|到期日期|合同至|期限至)[为：:]?\s*' + DATE, text)
        if start_match and end_match:
            try:
                start, end = date(*map(int, start_match.groups())), date(*map(int, end_match.groups()))
                if start <= end:
                    contract = (start, end)
            except ValueError:
                pass
    probation = date_range(text, "试用期")
    start = contract[0] if contract else None
    if start is None:
        match = re.search(START, text)
        if match:
            try:
                start = date(*map(int, match.groups()))
            except ValueError:
                pass
    if not probation and start:
        match = re.search(r"(?:其中\s*)?试用期(?:截止|结束)?(?:至|于)\s*" + DATE, text)
        if match:
            try:
                end = date(*map(int, match.groups()))
                if start <= end and (not contract or end <= contract[1]):
                    probation = (start, end)
            except ValueError:
                pass
    return contract, probation


def operative_optional_arrangement(text, topic):
    """Exclude deferred agreement paragraphs, preserving concrete duties elsewhere."""
    blocks = re.split(r"(?=第[一二三四五六七八九十百\d]+条)", text)
    substantive = []
    for block in blocks:
        if not re.search(topic, block):
            continue
        deferred = re.search(r"(?:可以|可)(?:另行|与.{1,12})?(?:签订|订立)|另行(?:协商后另行)?(?:签订|订立)|实际签署后", block)
        if deferred:
            # A separately imposed present duty still prevails over a reservation.
            explicit = re.search(r"(?:乙方|劳动者)(?:应|须|承诺|同意).{0,15}(?:服务|履行竞业|不得.{0,15}任职)|(?:服务期|竞业限制期限)[为：:]\s*[\d一二三四五六七八九十]+", block)
            if not explicit:
                continue
        for sentence in re.split(r"[。；\n]", block):
            if not re.search(topic, sentence):
                continue
            if re.search(r"(?:不约定|不设置|不适用|不承担)|除法律规定|不得.{0,30}违约金", sentence):
                continue
            if re.search(r"约定|承担|履行|遵守|应|须|同意|承诺|期限|范围|补偿|费用|[：:]", sentence):
                substantive.append(sentence)
    return bool(substantive)


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
    present = [row for row in present if not re.search(r"(?:如|若|可能).{0,30}(?:存在|产生|涉及|接触)职业(?:病)?危害", row['text'])]
    prerequisite = None if absent and present else False if absent else True if present else None
    return prerequisite, absent + present


def resolve_requirements(node, requirements, clauses):
    text = '\n'.join(c.text for c in clauses if c.section_type in {'正式合同条款', '附件'})
    if node == 'employment_identity':
        from review_v2.priority_contract_types import classify_priority_contract
        scenario = classify_priority_contract(text, clauses)
        if scenario and scenario[0] == 'employment_termination':
            requirements = [dict(row) for row in requirements]
            for row in requirements:
                if row['element_id'] == 'employment_identity_1':
                    row.update(risk_relevant=False, recommendation_action='OPTIONAL', gap_risk_level='低',
                        residual_gap='解除终止协议中住所属于可选联系信息完善，不作为核心签署障碍')
        return requirements, []
    if node == 'common_penalty_base_determinability':
        from review_v2.penalty_base import resolve
        return resolve(text), []
    if node in {'employment_secret_scope','employment_secret_duty','confidentiality_parties','confidentiality_remedies'}:
        from review_v2.nda_semantics import resolve
        return resolve(node, requirements, text), []
    if node.startswith(('security_', 'pledge_', 'mortgage_')):
        from review_v2.security_context import resolve
        return resolve(node, requirements, text), []
    if node == 'employment_term':
        kind = term_type(text)
        type_row = requirements[0]
        start = requirement('employment_term_start', '生效或起始日期', START,
            r'^\s*自' + RANGE,
            r'(?:本合同|合同期限)\s*[：:]?\s*自?' + RANGE,
            r'起始日期[为：:]?\s*' + DATE)
        if kind == 'INDEFINITE':
            return [type_row, start], []
        if kind == 'TASK':
            return [type_row, start,
                requirement('employment_term_task', '具体工作任务',
                    r'以完成\s*[^。；\n]{3,120}\s*为工作任务',
                    r'工作任务(?:包括|为(?!期限)|：|:)[^。；\n]{3,150}',
                    r'以完成(?!一定)[^。；\n]{2,50}工作任务为期限'),
                requirement('employment_term_task_end', '任务完成或验收作为终止节点',
                    r'(?:任务|项目|工作).{0,20}(?:完成|验收).{0,45}(?:终止|结束)',
                    r'实际劳动合同期限以.{0,30}工作任务实际完成时间为准')], []
        return [type_row, start, requirement('employment_term_end', '终止日期',
            r'^\s*自' + RANGE,
            r'(?:本合同|合同期限)\s*[：:]?\s*自?' + RANGE,
            r'(?:终止日期|到期日期|合同至|期限至)[为：:]?\s*' + DATE)], []
    if node == 'employment_probation':
        _, trial = probation_dates(text)
        if trial:
            requirements = [dict(r) for r in requirements]
            requirements[0]['semantic_patterns'] = (*requirements[0]['semantic_patterns'],
                r'(?:其中\s*)?试用期(?:截止|结束)?(?:至|于)\s*' + DATE)
        return requirements, []
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
