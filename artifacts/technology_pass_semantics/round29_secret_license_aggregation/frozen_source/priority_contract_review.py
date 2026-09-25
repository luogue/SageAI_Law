"""Source-bound adapter to the existing coverage, finding and report pipeline."""
from copy import deepcopy
import re

from review_v2.priority_contract_types import PRIORITY_TYPES
from review_v2.priority_checklist_helpers import PROFILES, CONDITIONS, ADVERSE
from review_v2.lease_semantics import corpus_facts, supports


POSITIVE_RULE_ADVERSE_PATTERNS = {
    'security_exercise_period': (
        r'(?:抵押权人|债权人|贷款人)[^。；]{0,25}(?P<act>不得|无权|放弃)[^。；]{0,15}(?:行使|实现)抵押权',
        r'抵押权[^。；]{0,25}(?P<act>仅可|只能)[^。；]{0,25}(?:日|天|月)内行使',
        r'主债权诉讼时效[^。；]{0,15}(?P<act>缩短|不适用|排除)',
    ),
    'security_realization': (
        r'(?:抵押权人|债权人|贷款人)[^。；]{0,25}(?P<act>不得|无权|放弃)[^。；]{0,25}(?:优先受偿|拍卖|变卖|实现抵押权)',
        r'(?:超额|剩余|超过债权数额)[^。；]{0,25}(?P<act>归(?:债权人|贷款人|抵押权人)所有|不予返还|无需返还)',
    ),
    'employment_hours': (
        r'(?P<act>不再|不予|无需|不)(?:另行)?支付加班(?:工资|费|报酬)',
        r'(?:月工资|工资)[^。；\n]{0,20}(?P<act>已(?:经)?包含|包含|包括)[^。；\n]{0,15}加班(?:工资|费|报酬)',
        r'加班[^。；\n]{0,15}(?P<act>不支付|不予支付|无需支付|不计发)[^。；\n]{0,10}(?:任何报酬|报酬|工资|加班费)',
        r'(?:乙方|劳动者)[^。；\n]{0,10}(?P<act>放弃|不得主张|无权要求)[^。；\n]{0,10}(?:法定)?加班(?:工资|费|报酬)',
        r'(?:固定工资|月工资|基本工资)[^。；\n]{0,15}(?P<act>(?:当然)?包含(?:全部|所有|一切)加班(?:工资|费|报酬)?)',
        r'法定(?:节假日|休假日)[^。；\n]{0,15}加班[^。；\n]{0,10}(?P<act>仅(?:以|安排)?(?:调休|补休)|只(?:以|安排)?(?:调休|补休))',
        r'(?P<act>不支付|免付|不计发)(?:法定)?加班(?:工资|费|报酬)',
        r'(?:乙方|劳动者)[^。；\n]{0,12}(?P<act>每周七天均须工作|不得休息|无休息日)',
    ),
    'employment_insurance': (
        r'(?:甲方|用人单位)(?:(?!乙方|劳动者|[。；]).){0,20}(?P<act>不缴纳|不缴|少缴|不予缴纳|无需缴纳)[^。；\n]{0,15}(?:社会保险|社保)',
        r'(?:单位|用人单位|甲方)(?:应缴|应当缴纳|应承担|应缴纳)[^。；\n]{0,20}(?:社会保险|社保)[^。；\n]{0,20}(?P<act>由(?:乙方|劳动者|个人)(?:自行|全部)?承担)',
        r'(?:社会保险|社保)[^。；\n]{0,10}(?:单位|甲方|用人单位)(?:应缴|缴费|承担)部分[^。；\n]{0,10}(?P<act>由(?:乙方|劳动者|个人)(?:自行|全部)?承担)',
    ),
    # These predicates are narrow on purpose: ordinary labor contracts can rely
    # on statutory termination procedures, while a direct waiver/deprivation
    # must still surface as a real risk under the same checkpoint.
    "employment_exit": (
        r'(?:乙方|劳动者)[^。；\n]{0,15}(?P<act>不得|无权)[^。；\n]{0,8}(?:自行离职|自行辞职)',
        r"(?:用人单位|甲方).{0,20}(?:可以|可|有权).{0,8}(?:随时|任意|无理由)(?:辞退|解除|终止)",
        r"(?:劳动者|乙方)(?:(?!甲方|用人单位|[，。；]).){0,30}(?:不得|无权|放弃).{0,20}(?:依法)?(?:解除|终止|辞职|通知解除)",
    ),
    "employment_compensation": (
        r"(?:用人单位|甲方).{0,20}?(?P<act>无需|不予|不支付|免除).{0,15}经济补偿",
        r"(?:劳动者|乙方).{0,20}?(?P<act>放弃|不得主张|无权要求).{0,20}经济补偿",
        r"经济补偿.{0,25}?(?P<act>无需|不予|不支付|免除|放弃|不得主张)",
        r"经济补偿.{0,35}?(?P<act>一年后|六个月后|离职后[三四五六七八九十\d]+个?月后).{0,12}(?:支付|结算)",
        r'经济补偿[^。；\n]{0,15}(?P<act>低于法定标准|按法定标准的(?:[1-9]\d?|[一二三四五六七八九十]+)[%％折成]|仅按法定标准的(?:[1-9]\d?|[一二三四五六七八九十]+)[%％折成])',
        r'(?:甲方|用人单位)[^。；\n]{0,15}(?P<act>减免|免除|不支付|不予支付)[^。；\n]{0,12}(?:法定)?经济补偿',
        r'(?P<act>仅支付|只支付)[^。；\n]{0,8}法定经济补偿的(?:一半|半数|[1-9]\d?[%％])',
    ),
}


def applicability(text, checkpoint, contract_type):
    from review_v2.employment_fact_store import current
    store = current()
    if store is not None and checkpoint.node_id.startswith(('employment_','confidentiality_','nda_','termination_')):
        return store.applicability(checkpoint.node_id)
    from review_v2.contract_effects import applicability as effect_applicability, RELATION_REQUIREMENTS
    if checkpoint.node_id in RELATION_REQUIREMENTS:
        from review_v2.clause_parser import parse_contract_clauses
        condition=effect_applicability(checkpoint.node_id,parse_contract_clauses(text))
        return condition['applicable'], condition['reason']
    if checkpoint.node_id.startswith('reg_'):
        from review_v2.business_overlays import checkpoints
        return checkpoint.item_id in {c.item_id for c in checkpoints(text)}, '正文存在对应监管业务；实际许可及有效状态须核验外部材料。'
    if checkpoint.node_id == 'common_shortfall_formula':
        from review_v2.settlement_formula import analyze
        return bool(analyze(text)), '存在补足、保底或最低收益金额安排。'
    if checkpoint.node_id in {'formation_nonmonetary', 'formation_fund_safety'}:
        from review_v2.shareholder_transaction_facts import transaction_facts
        kind = {'formation_nonmonetary':'nonmonetary_contribution','formation_fund_safety':'personal_subscription_account'}[checkpoint.node_id]
        matches = [f for f in transaction_facts(text) if f['fact_type']==kind]
        return bool(matches), '已识别出资财产或收款主体交易事实。' if matches else '未证明对应出资财产或个人收款事实，本项不适用。'
    if checkpoint.node_id == 'formation_no_shareholder_organ':
        from review_v2.company_governance_facts import organ_prerequisites
        facts = organ_prerequisites(text)
        return all(facts.values()), '有限责任公司、多股东、不设股东会机关三个前提均成立。' if all(facts.values()) else '未同时证明有限责任公司、多股东及不设股东会机关安排，不触发该不利条款检查。'
    if checkpoint.node_id.startswith('formation_') and checkpoint.node_id in ADVERSE:
        from review_v2.clause_parser import parse_contract_clauses
        present = bool(adverse_evidence(checkpoint.node_id, parse_contract_clauses(text)))
        return present, '发现本项直接不利安排，进入风险核验。' if present else '未发现本项直接不利安排，本项不启动缺失审查。'
    if checkpoint.node_id == 'common_dangling_obligation':
        from review_v2.clause_completeness import fragments
        return bool(fragments(text)), '存在未完成的义务或责任谓语，核对完整条款。'
    if checkpoint.node_id in {'common_internal_references', 'common_legal_references'}:
        from review_v2.contract_references import augment
        present = any(c.node_id == checkpoint.node_id for c in augment((), text))
        return present, '已识别显式引用，核对目标、层级与语义。' if present else '未出现本项显式引用，不适用。'
    if contract_type == 'employment_termination':
        from review_v2.employment_contract_checklist import TERMINATION_CHECKLIST
        if checkpoint.domain_owner == 'emp' and checkpoint.node_id not in {c.node_id for c in TERMINATION_CHECKLIST}:
            return False, '解除终止协议按专项清单审查，不适用普通在职劳动合同完整性要素。'
    from review_v2.termination_checklist import TERMINATION_ADDITIONS
    if checkpoint.node_id in {c.node_id for c in TERMINATION_ADDITIONS} or checkpoint.node_id == 'employment_handover':
        if contract_type != 'employment_termination':
            return False, '未处于劳动关系解除终止结算场景。'
    from review_v2.penalty_base import NODE as penalty_node, analyze as analyze_penalty
    if checkpoint.node_id == penalty_node:
        present = bool(analyze_penalty(text))
        return present, ('存在依赖金额基数的比例违约金约定。' if present else '未发现依赖金额基数的比例违约金约定，本项不适用。')
    if contract_type not in PRIORITY_TYPES:
        return None
    node = checkpoint.node_id
    from review_v2.employment_facts import operative_optional_arrangement
    if node == 'employment_probation':
        from review_v2.employment_facts import actual_probation, term_type
        if not actual_probation(text) and (re.search(r'(?:不约定|不设|不设置|无)试用期', text) or term_type(text) == 'TASK'):
            return False, '未建立实际试用期安排；明确不设试用期或任务期限合同不要求补充试用期要素。'
    if node == "employment_training_service" and not operative_optional_arrangement(text, r"服务期"):
        return False, "未识别已约定的专项培训服务期义务；另行签订协议的预备性表述不触发。"
    if node.startswith("employment_noncompete") and contract_type != "non_compete" and not operative_optional_arrangement(text, r"竞业限制|竞业禁止"):
        return False, "未识别当前生效的竞业限制义务；可以另行签订协议不等于已作出竞业约定。"
    if node == "security_company_authority":
        from review_v2.security_context import corporate_context
        if corporate_context(text)['own_debt']:
            return False, "为自身债务提供担保，不按公司对外担保决议缺失处理；代表权限仍应核验。"
        corporate = re.search(r"(?:抵押人|出质人)[^。；\n]{0,60}(?:公司|企业)", text)
        if not corporate:
            return False, "未识别公司作为抵押人或出质人，公司担保决议专项审查不触发；主体及处分权限仍独立核对。"
    if node.startswith("employment_noncompete") and contract_type != "non_compete":
        if not re.search(r"竞业限制|竞业禁止", text) or re.search(r"(?:不约定|不设置|不承担|不适用)竞业(?:限制|禁止)", text):
            return False, "未约定竞业限制，不要求新增该可选安排。"
    if node == "employment_general_penalty" and contract_type == "confidentiality":
        from review_v2.nda_semantics import scenario
        if scenario(text) != 'EMPLOYMENT_NDA':
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
    from review_v2.employment_facts import probation_dates, add_months, term_type
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
    if term_type(text) == 'INDEFINITE':
        limit = 6
    elif term_type(text) == 'TASK':
        limit = 0
    elif contract_dates:
        start, end = contract_dates
        exclusive_end = end + timedelta(days=1)
        limit = (0 if exclusive_end < add_months(start, 3) else
                 1 if exclusive_end < add_months(start, 12) else
                 2 if exclusive_end < add_months(start, 36) else 6)
    elif term:
        duration = _number(term[1]) * (12 if term[2] == "年" else 1)
        limit = 0 if duration < 3 else 1 if duration < 12 else 2 if duration < 36 else 6
    elif re.search(r"以完成.{0,30}工作任务为期限(?![。；]?\s*不适用)", text):
        limit = 0
    if trial_dates:
        return trial_dates[1] + timedelta(days=1) > add_months(trial_dates[0], limit)
    return _number(probation[1]) > limit


def adverse_evidence(node, clauses):
    from review_v2.employment_fact_store import current
    store = current()
    if store is not None and node.startswith(('employment_','confidentiality_','nda_','termination_')):
        return store.adverse(node)
    from review_v2.contract_effects import CHECKPOINTS as effect_checkpoints, evidence as effect_evidence
    if node in {c.node_id for c in effect_checkpoints}:
        return effect_evidence(node,clauses)
    if node == 'formation_deadline_legality':
        from review_v2.formation_rule_semantics import deadline_evidence
        return deadline_evidence(clauses)
    if node == 'formation_unilateral_control':
        from review_v2.shareholder_transaction_facts import evidence
        extra = evidence(node, clauses)
        if extra:
            return extra
    if node == 'formation_no_shareholder_organ':
        from review_v2.company_governance_facts import governance_evidence
        return governance_evidence(node, clauses)
    if node in {"equity_transaction_structure", "equity_contribution_warranty_alignment", "equity_invalid_cross_reference"}:
        from review_v2.equity_transaction_facts import structure_evidence
        return structure_evidence(node, clauses)
    from review_v2.adverse_evidence import direct_evidence
    positive, _ = direct_evidence(clauses, ADVERSE.get(node, ()), require_assertion=False)
    if node == 'formation_unilateral_control':
        from review_v2.company_governance_facts import governance_evidence
        modeled = {r['clause_id']: r.get('adverse_fact_atom') for r in governance_evidence(node, clauses)}
        for row in positive:
            if modeled.get(row.get('clause_id')):
                row['adverse_fact_atom'] = deepcopy(modeled[row['clause_id']])
    if node == 'employment_noncompete_adverse':
        for c in clauses:
            if c.section_type in {'正式合同条款','附件'} and re.search(r'(?:解除|终止|离职)', c.text) and re.search(r'竞业', c.text):
                extra, _ = direct_evidence([c], (r'(?:甲方|用人单位)[^。；]{0,12}(?:无需|不必|不予|不)[^。；]{0,50}支付[^。；]{0,10}经济补偿',), require_assertion=False)
                # Cessation of both future duties after releasing the covenant
                # is not uncompensated performance of a surviving covenant.
                if re.search(r'(?:协议|竞业限制)(?:解除|终止)后', c.text) and re.search(r'(?:无需|不再|不必)[^。；]{0,12}履行[^。；]{0,15}竞业', c.text):
                    extra = []
                positive.extend(extra)
    if node == 'employment_general_penalty':
        # Resolve the governing article, then bind BOTH the penalty and the
        # ordinary duty it covers. Amount alone is never an adverse predicate.
        parent = None
        groups = {}
        for s in clauses:
            if re.match(r'^(?:\d+[、.]|第[一二三四五六七八九十\d]+条)', s.text):
                parent = s.clause_id
            groups[s.clause_id] = parent
        for c in clauses:
            if c.section_type not in {'正式合同条款','附件'} or not re.search(r'违反本条[^。；]{0,30}违约金', c.text):
                continue
            if re.search(r'仅(?:就|因|对|限于)?[^。；]{0,15}(?:竞业限制|专项培训服务期)[^。；]{0,30}违约金', c.text):
                continue
            parent = groups.get(c.clause_id)
            siblings = [s for s in clauses if groups.get(s.clause_id) == parent and s.section_type in {'正式合同条款','附件'}]
            duties = [s for s in siblings if s.clause_id != c.clause_id and re.search(
                r'(?:乙方|劳动者)[^。；]{0,100}(?:保密义务|应[^。；]{0,30}(?:办理|完成|配合)[^。；]{0,15}(?:交接|离职)|不得[^。；]{0,15}辞职)', s.text)]
            if parent and duties:
                reason = '“违反本条”将违约金概括绑定至同条一般保密、交接或离职义务，超出仅对竞业限制或法定专项培训服务期约定违约金的范围；风险依据是义务作用域，而非违约金金额。'
                pair_ids = [c.clause_id] + [s.clause_id for s in duties]
                positive.append({**c.to_public_dict(), 'reason':reason,
                    'binding_role':'PENALTY_CLAUSE', 'scope_parent_clause_id':parent, 'scope_evidence_ids':pair_ids})
                positive.extend({**s.to_public_dict(), 'reason':reason,
                    'binding_role':'COVERED_ORDINARY_OBLIGATION', 'scope_parent_clause_id':parent,
                    'scope_evidence_ids':pair_ids} for s in duties)
    if node in {'employment_illegal_waiver', 'employment_ip_ownership'}:
        from review_v2.employment_rights import rights_evidence
        positive.extend(rights_evidence(node, clauses))
    if node == "employment_probation_limit":
        corpus = "\n".join(c.text for c in clauses if c.section_type in {"正式合同条款", "附件"})
        if probation_risk(corpus):
            from review_v2.employment_facts import probation_dates
            positive = []
            for c in clauses:
                if c.section_type not in {"正式合同条款", "附件"}:
                    continue
                for sentence in re.split(r'(?<=[。；])|\n', c.text):
                    term, trial = probation_dates(sentence)
                    if term or trial or re.search(r'(?:合同期限|试用期)(?:为|：|:)\s*[一二两三四五六七八九十\d]+个?(?:年|月)|(?:再次|重新|重复)约定试用期', sentence):
                        positive.append({**c.to_public_dict(), 'text':sentence, 'quote':sentence})
    return positive


def positive_rule_adverse_evidence(node, clauses):
    from review_v2.employment_fact_store import current
    store = current()
    if store is not None and node.startswith(('employment_','confidentiality_','nda_','termination_')):
        return store.adverse(node)
    if node == 'formation_transfer_exit':
        from review_v2.formation_rule_semantics import transfer_evidence
        return transfer_evidence(clauses)
    from review_v2.shareholder_transaction_facts import evidence, consistency
    if node == 'formation_parties_capital':
        return consistency(clauses)
    extra = evidence(node, clauses)
    if extra and node not in {'formation_governance','formation_capital_increase','equity_governance'}:
        return extra
    if node in {'formation_governance', 'formation_capital_increase', 'equity_governance'}:
        from review_v2.company_governance_facts import governance_evidence
        return extra + governance_evidence('formation_governance' if node == 'equity_governance' else node, clauses)
    if node in {'common_internal_references', 'common_legal_references'}:
        from review_v2.contract_references import adverse
        return adverse(node, clauses)
    from review_v2.adverse_evidence import direct_evidence
    patterns = POSITIVE_RULE_ADVERSE_PATTERNS.get(node, ())
    if node == 'employment_wage':
        # Reuse the existing earned-pay withholding detector in ordinary labor
        # contracts too; its applicability does not depend on document title.
        from review_v2.termination_checklist import WITHHOLD
        patterns = ADVERSE[WITHHOLD.node_id]
    if node == 'employment_handover':
        rows=[]
        for c in clauses:
            if c.section_type not in {'正式合同条款','附件'}:
                continue
            for m in re.finditer(r'(?:解除|终止)[^。；]{0,25}?(\d+|[一二两三四五六七八九十]+)(?:日|天)内[^。；]{0,35}(?:档案|社会保险|社保)[^。；]{0,20}转移', c.text):
                if _number(m[1]) > 15:
                    rows.append({**c.to_public_dict(), 'text':m.group(), 'quote':m.group(), 'reason':'约定转移期限超过解除或终止后十五日的法定期限。'})
        return rows
    if node == 'employment_noncompete_term':
        return [row for row in adverse_evidence('employment_noncompete_adverse', clauses)
                if re.search(r'(?:无需|不予|不支付|无偿)[^。；]{0,60}(?:补偿|履行)', row['text'])]
    if not patterns:
        return []
    # These predicates already state the affected statutory payment. A numeric
    # reduction/deferral remains an assertion even when the sentence omits 甲方.
    positive, _ = direct_evidence(clauses, patterns, require_assertion=node not in {'employment_insurance', 'employment_compensation', 'employment_hours', 'security_realization', 'security_exercise_period'})
    if node == 'employment_hours':
        # A bounded allowance with a statutory shortfall settlement is not an
        # unlimited waiver; retain independently adverse payment terms.
        positive = [row for row in positive if not (
            re.search(r'包含(?:全部|所有|一切)加班', row.get('text', ''))
            and re.search(r'(?:不足|差额)[^。；]{0,15}(?:依法补足|另行支付|补齐)', row.get('text', ''))
            and not re.search(r'放弃|不支付|免付', row.get('text', '')))]
    if node == 'employment_insurance':
        # Reuse the existing waiver rule's predicates without changing EMP-13.
        waiver, _ = direct_evidence(clauses, ADVERSE['employment_illegal_waiver'], require_assertion=False)
        positive.extend(waiver)
    if node == 'employment_compensation':
        positive = [row for row in positive if not re.search(r'竞业(?:限制|禁止)', row.get('text',''))]
    if node == 'employment_exit':
        from review_v2.employment_exit import exit_adverse_evidence
        positive.extend(exit_adverse_evidence(clauses))
    return positive


def judge(checkpoint, clauses, shared_facts=None):
    """Initial judgments also use exact evidence, including when LLM is enabled."""
    from review_v2.semantic_reviewer import ReviewJudgment
    if checkpoint.node_id not in ADVERSE and checkpoint.node_id not in PROFILES:
        return None
    risk_level = checkpoint.risk_level
    if checkpoint.node_id in ADVERSE:
        evidence = adverse_evidence(checkpoint.node_id, clauses)
        from review_v2.employment_fact_store import current
        pending = current().pending_reason(checkpoint.node_id) if current() is not None else ''
        if not evidence and pending:
            return ReviewJudgment(coverage_status='INSUFFICIENT_CONTEXT',risk_level='低',status='待核验',
                risk_point_description=pending,evidence_clauses=[],evidence_location='',
                reasoning_summary=pending,matched_terms=[],issue_type='待核验')
        state = "风险条款" if evidence else "通过"
        reason = checkpoint.risk_point_present if evidence else "全文未发现该项禁止性风险约定；防范和否定表述不作为风险证据。"
        if checkpoint.node_id == 'formation_deadline_legality' and evidence:
            reason = '；'.join(dict.fromkeys(r['reason'] for r in evidence))
        if checkpoint.node_id == 'employment_general_penalty' and evidence:
            scope_reasons = list(dict.fromkeys(row['reason'] for row in evidence if row.get('scope_evidence_ids')))
            if scope_reasons:
                reason = '；'.join(scope_reasons)
        if evidence and any(row.get('legal_effects') for row in evidence):
            from review_v2.employment_rights import EFFECT_REASONS
            reason = EFFECT_REASONS[checkpoint.node_id]
        if not evidence and current() is not None:
            evidence = current().negative_support(checkpoint.node_id)
            if evidence:
                reason = '原文已明确允许依法通知终止；全文核验未发现提前等待、离职违约金、最低履行期间或批准等终止限制。'
    else:
        adverse = positive_rule_adverse_evidence(checkpoint.node_id, clauses)
        if adverse:
            state = "风险条款"
            evidence = adverse
            lead = '发现影响本项安排准确性或可执行性的直接约定。' if checkpoint.node_id in {'formation_governance', 'formation_capital_increase', 'common_internal_references', 'common_legal_references'} else '发现与本项法定保护相冲突的直接不利约定。'
            reason = lead + '；'.join(dict.fromkeys(row['reason'] for row in adverse if row.get('reason')))
            # This judgment binds the adverse facts below. Positive coverage
            # is evaluated independently; do not inject an unbound positive
            # quotation into the adverse narrative.
            return ReviewJudgment(
                coverage_status=state, risk_level=risk_level,
                status=state, risk_point_description=reason, evidence_clauses=evidence,
                evidence_location="；".join(dict.fromkeys(r.get("location", "") for r in evidence)),
                reasoning_summary=reason, matched_terms=[t for t in checkpoint.terms if any(t in r.get("text", "") for r in evidence)],
                issue_type="风险条款",
            )
        from review_v2.employment_fact_store import current
        from review_v2.employment_facts import resolve_requirements
        elements, conditions = resolve_requirements(checkpoint.node_id, PROFILES[checkpoint.node_id], clauses)
        from review_v2.requirement_kinds import partition, notes
        elements, kind_assessments = partition(elements)
        facts = ({e["element_id"]: deepcopy(shared_facts[e["element_id"]]) for e in elements}
                 if shared_facts is not None and all(e["element_id"] in shared_facts for e in elements)
                 else corpus_facts(clauses, elements))
        facts = {e['element_id']: [r for r in facts[e['element_id']] if supports(e, r)] for e in elements}
        # Economic compensation is context-specific.  Do not let a
        # non-compete/training/overtime compensation sentence satisfy the
        # post-termination statutory settlement rule merely by sharing the
        # token “经济补偿”.  The specialized NC rule consumes those facts.
        from review_v2.employment_fact_store import current
        if checkpoint.node_id == 'employment_compensation' and current() is None:
            for key, rows in facts.items():
                facts[key] = [r for r in rows if not re.search(
                    r'竞业(?:限制|禁止)|专项培训|加班', str(r.get('text') or ''))]
        evidence = [row for element in elements for row in facts[element["element_id"]]]
        missing_elements = [e for e in elements if not facts[e["element_id"]]]
        actionable_missing = [e for e in missing_elements if e.get("risk_relevant") is not False]
        optional_missing = [e for e in missing_elements if e.get("risk_relevant") is False]
        missing = [e["proposition"] for e in actionable_missing]
        # A compensation sentence from a non-compete/training context is not
        # applicable evidence for EMP-11.  After semantic filtering, force
        # the verdict to reflect the remaining valid evidence; never retain a
        # stale covered/pass state from an earlier semantic hit.
        if checkpoint.node_id == 'employment_compensation' and not evidence:
            actionable_missing = list(elements)
            optional_missing = []
            missing = [e["proposition"] for e in actionable_missing]
        if actionable_missing and any("gap_risk_level" in e for e in elements):
            risk_level = max((e.get("gap_risk_level", checkpoint.risk_level)
                              for e in actionable_missing),
                             key={"低": 0, "中": 1, "高": 2}.__getitem__)
        state = "通过" if not actionable_missing else "部分覆盖" if evidence else "缺失"
        if not actionable_missing and optional_missing:
            reason = "合同原文覆盖本项核心法定义务；可选完善项未单独作为实际风险：" + "、".join(e["proposition"] for e in optional_missing) + "。"
        else:
            reason = ("合同原文已覆盖本项合同声明及材料提交安排；外部事实仍待核验。" if not missing and any(a["status"]=="PENDING_VERIFICATION" for a in kind_assessments) else "合同原文覆盖全部专项要素。" if not missing else "未找到明确约定：" + "、".join(missing) + "。")
        if any(row['prerequisite_status'] == 'FALSE' for row in conditions):
            reason += "未触发的专项要素不参与缺失计算；其余适用要素独立审查。"
        if any(row['prerequisite_status'] == 'UNKNOWN' for row in conditions):
            reason += "专项要素的适用前提待核实，未将条件不明的义务判为合同缺失。"
        if kind_assessments:
            reason += notes(kind_assessments)
    if checkpoint.node_id == 'formation_fund_safety':
        from review_v2.formation_rule_semantics import account_context
        reason = account_context('\n'.join(c.text for c in clauses))['conclusion'] + reason
    return ReviewJudgment(
        coverage_status=state, risk_level="低" if state == "通过" else risk_level,
        status=state, risk_point_description=reason, evidence_clauses=evidence,
        evidence_location="；".join(dict.fromkeys(r.get("location", "") for r in evidence)),
        reasoning_summary=reason, matched_terms=[t for t in checkpoint.terms if any(t in r.get("text", "") for r in evidence)],
        issue_type={"通过": "通过", "部分覆盖": "条款缺陷", "缺失": "完全缺失", "风险条款": "风险条款"}[state],
    )


def apply(items, clauses, checklist, shared_facts=None):
    from review_v2.shareholder_transaction_facts import attach_source_assertions
    attach_source_assertions(items, clauses)
    from review_v2.formation_rule_semantics import deadline_assessment, transfer_assessment, account_context
    formation_text = '\n'.join(c.text for c in clauses)
    for review in items:
        if review.node_id in {'formation_contributions','formation_deadline_legality'}:
            review.decision_trace['contribution_deadline_assessment'] = deadline_assessment(formation_text)
        if review.node_id == 'formation_transfer_exit':
            review.decision_trace['transfer_mechanism_assessment'] = transfer_assessment(formation_text)
        if review.node_id == 'formation_fund_safety':
            review.decision_trace['fund_receiver_context'] = account_context(formation_text)
            for fact in review.decision_trace['fund_receiver_context']['evidence']:
                sources = [c for c in clauses if fact['text'] in c.text]
                fact['source_clause_ids'] = [c.clause_id for c in sources]
                fact['source_locations'] = [c.location for c in sources]
    from review_v2.nda_semantics import apply_scenario
    apply_scenario(items, clauses)
    by_node = {row.node_id: row for row in checklist}
    from review_v2.penalty_base import CHECKPOINT
    by_node[CHECKPOINT.node_id] = CHECKPOINT
    from review_v2.contract_references import CHECKPOINTS
    by_node.update({c.node_id: c for c in CHECKPOINTS})
    for item in items:
        if item.coverage_status == "不适用":
            continue
        checkpoint = by_node[item.node_id]
        if item.node_id in {'operation_multiple_penalty','operation_prospective_penalty'}:
            from review_v2.settlement_formula import penalty_expressions
            item.decision_trace['penalty_expression_analysis'] = penalty_expressions('\n'.join(c.text for c in clauses))
        if item.node_id == 'common_shortfall_formula':
            from review_v2.settlement_formula import analyze
            item.decision_trace['settlement_formula_analysis'] = analyze('\n'.join(c.text for c in clauses))
        if item.node_id in {'common_internal_references', 'common_legal_references'}:
            from review_v2.contract_references import analyze as analyze_references
            item.decision_trace['reference_integrity_audit'] = [
                {**{k: v for k, v in row.items() if k != 'source'}, 'source_clause_id': row['source'].clause_id}
                for row in analyze_references(clauses)[item.node_id]]
        if item.node_id == 'common_penalty_base_determinability':
            from review_v2.penalty_base import analyze
            item.decision_trace['penalty_base_analysis'] = analyze('\n'.join(c.text for c in clauses))
        judgment = judge(checkpoint, clauses, shared_facts=shared_facts)
        if judgment is None:
            continue
        for name in ("coverage_status", "risk_level", "status", "risk_point_description", "evidence_clauses", "evidence_location", "reasoning_summary", "matched_terms", "issue_type"):
            setattr(item, name, deepcopy(getattr(judgment, name)))
        item.judge_source = "rule_fallback"
        item.fallback_reason = "专项原文要素核验"
        item.needs_manual_review = False
        if item.node_id == 'employment_ip_ownership':
            item.decision_trace['optional_without_specific_exposure'] = judgment.coverage_status == '缺失'
            if judgment.coverage_status == '缺失':
                item.legal_consequence_if_missing = '合同未明确约定劳动成果及知识产权归属，可选完善；法定权利仍依法确定，不据此认定权利被剥夺。'
        from review_v2.employment_risk_semantics import project_item
        project_item(item)
        item.decision_trace['adverse_fact_atoms'] = [deepcopy(row['adverse_fact_atom']) for row in judgment.evidence_clauses if row.get('adverse_fact_atom')]
        if item.node_id in PROFILES and judgment.coverage_status == "风险条款":
            if item.node_id in {'employment_insurance', 'employment_compensation'}:
                core = PROFILES[item.node_id][0]
                item.decision_trace['priority_core_obligation_context'] = corpus_facts(clauses, [core])[core['element_id']]
            if item.node_id == 'employment_exit':
                item.action_suggestion = '修改单独扩张用人单位解除权的约定，保留法定事由及前置程序；违纪解除须核验合法制定并公示的制度、严重程度及事实证据，不删除保护劳动者的限制解除条款。'
            elif item.node_id == 'employment_compensation':
                item.action_suggestion = item.suggested_clause_example if item.decision_trace.get('risk_semantic_contract') else '删除免除、减少或违法拖延经济补偿的约定，按法定情形和结算规则支付。'
            element_id = item.node_id + "_adverse"
            item.coverage_elements = [{
                "review_id": item.item_id,
                "element_id": element_id,
                "claim_id": f"{item.item_id}-{element_id}",
                "proposition": item.title + "存在直接不利约定。",
                "status": "ADVERSE",
                "risk_relevant": True,
                "direction": "LEGALITY_RISK",
                "recommendation_action": item.decision_trace.get("risk_semantic_contract", {}).get("recommendation_action"),
                "presence_status": "COVERED",
                "arrangement_status": "ADVERSE",
                "evidence_ids": [
                    str(row.get("evidence_id") or row.get("clause_id") or "")
                    for row in item.evidence_clauses
                    if row.get("evidence_id") or row.get("clause_id")
                ],
                "supporting_evidence_ids": [
                    str(row.get("evidence_id") or row.get("clause_id") or "")
                    for row in item.evidence_clauses
                    if row.get("evidence_id") or row.get("clause_id")
                ],
                "source_clause_ids": [
                    str(row.get("clause_id") or "")
                    for row in item.evidence_clauses
                    if row.get("clause_id")
                ],
                "supporting_evidence": [
                    {"clause_id": row.get("clause_id"), "quote": row.get("text") or row.get("quote") or ""}
                    for row in item.evidence_clauses
                ],
            }]
            item.decision_trace['semantic_requirements'] = [{
                'element_id': element_id, 'proposition': item.title + '存在直接不利约定',
                'semantic_patterns': tuple(re.escape(row['text']) for row in item.evidence_clauses),
                'evidence_unit': 'clause',
            }]
            item.decision_trace["priority_positive_adverse_verification"] = {
                "method": "DIRECT_ADVERSE_PREDICATE",
                "predicate_patterns": list(POSITIVE_RULE_ADVERSE_PATTERNS.get(item.node_id, ())),
                "source_clause_ids": [row["clause_id"] for row in item.evidence_clauses if row.get("clause_id")],
            }
            for row in item.evidence_clauses:
                row["supports_element_ids"] = [element_id]
                row["supporting_element_ids"] = [element_id]
        elif item.node_id in PROFILES:
            from review_v2.employment_facts import resolve_requirements
            elements, conditions = resolve_requirements(item.node_id, PROFILES[item.node_id], clauses)
            from review_v2.requirement_kinds import partition, notes
            elements, kind_assessments = partition(elements)
            item.decision_trace['requirement_kind_assessments'] = kind_assessments
            if kind_assessments:
                item.legal_consequence_if_missing = notes(kind_assessments)
            external = [a for a in kind_assessments if a['status']=='PENDING_VERIFICATION']
            if external:
                item.needs_manual_review = True
                item.action_suggestion = '；'.join(a['verification_instruction'] for a in external)
                item.suggested_clause_example = ''
                if item.coverage_status == '通过':
                    item.coverage_status = item.status = 'INSUFFICIENT_CONTEXT'
                    item.issue_type = '待核验'
            item.decision_trace["semantic_requirements"] = deepcopy(elements)
            item.decision_trace["priority_conditional_elements"] = deepcopy(conditions)
            if any("gap_risk_level" in e for e in elements):
                facts = corpus_facts(clauses, elements)
                item.decision_trace["element_severity_assessment"] = {
                    "basis": "MAXIMUM_ACTUAL_UNCOVERED_ELEMENT_SEVERITY",
                    "theme_default_level": checkpoint.risk_level,
                    "selected_level": judgment.risk_level,
                    "elements": [{"element_id": e["element_id"],
                                  "status": "COVERED" if facts[e["element_id"]] else "MISSING",
                                  "gap_risk_level": e.get("gap_risk_level", checkpoint.risk_level),
                                  "source_clause_ids": [r["clause_id"] for r in facts[e["element_id"]]]}
                                 for e in elements],
                }
        elif item.node_id in ADVERSE and judgment.coverage_status == "风险条款":
            # Predicate/calculation verification already established the adverse
            # fact. Bind that exact source span to an element before the shared
            # evidence layer; generic topic similarity must not erase the fact.
            element_id = item.node_id + "_adverse"
            item.decision_trace["semantic_requirements"] = [{
                "element_id": element_id, "proposition": checkpoint.title,
                "preserve_full_quote": any(row.get("scope_evidence_ids") for row in judgment.evidence_clauses),
                "semantic_patterns": tuple(re.escape(row["text"]) for row in judgment.evidence_clauses),
            }]
            item.decision_trace["priority_adverse_verification"] = {
                "method": "SCOPED_LEGAL_EFFECT_ANALYSIS" if any(row.get('legal_effects') for row in judgment.evidence_clauses) else "DIRECT_PREDICATE_OR_DATE_CALCULATION",
                "predicate_patterns": list(ADVERSE[item.node_id]),
                "source_clause_ids": [row["clause_id"] for row in judgment.evidence_clauses],
                'legal_effects': sorted({effect for row in judgment.evidence_clauses for effect in row.get('legal_effects', [])}),
            }
            for row in item.evidence_clauses:
                row["supports_element_ids"] = [element_id]
        elif item.node_id in ADVERSE:
            item.decision_trace.pop("semantic_requirements", None)
        item.decision_trace["priority_specialized_evaluation"] = True
        from review_v2.employment_fact_store import current
        if current() is not None and item.node_id.startswith(('employment_','confidentiality_','nda_','termination_')):
            negative_audit = current().negative_search_audit(item.node_id)
            if negative_audit:
                item.decision_trace['verified_negative_search'] = negative_audit
            from review_v2.dispatch_assessment import assessment
            legal_assessment = assessment(current(), item.node_id)
            if legal_assessment:
                item.decision_trace['specialized_legality'] = {
                    **legal_assessment,
                    'input_fact_ids': sorted({f['fact_id'] for c in legal_assessment['concepts'] for f in current().get(c, positive=False)}),
                    'evidence': current().evidence(
                        [f for c in legal_assessment['concepts'] for f in current().get(c, positive=False)],
                        item.node_id + '_legal_assessment'),
                }
            item.judge_source = 'structured_facts'
            item.fallback_reason = ''
            item.decision_trace['fact_pipeline'] = {'schema_version':'employment-facts-1.0', 'provider':'deepseek',
                'source_sha256':current().hash, 'fact_ids': sorted({e['structured_fact_id'] for e in item.evidence_clauses if e.get('structured_fact_id')})}
            if judgment.coverage_status == 'INSUFFICIENT_CONTEXT':
                item.needs_manual_review = True
                item.action_suggestion = judgment.reasoning_summary
        if item.node_id == 'employment_exit' and current() is None:
            from review_v2.employment_exit import classify_exit_clauses
            item.decision_trace['employment_exit_classification'] = classify_exit_clauses(clauses)
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
    from review_v2.noncompete_semantics import attach_prerequisites, temporal_roles
    attach_prerequisites(items, clauses)
    for item in items:
        if item.node_id == 'employment_noncompete_term' and item.coverage_status != '不适用':
            item.decision_trace['temporal_role_analysis'] = temporal_roles(clauses)
    return items
