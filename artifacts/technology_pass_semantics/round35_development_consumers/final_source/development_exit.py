"""Event-bound atomic requirements for development delay and early exit."""
import re
from review_v2.obligation_detail_elements import _segments


EXIT_EVENT = r"解除|终止|提前退出|退出(?:项目|合作)|研发失败|开发失败"
DEFERRED = r"另行(?:协商|商定|约定)|后续(?:协商|商定|约定)|待(?:协商|商定|约定)|具体.{0,16}未(?:明确|约定)"
NO_ARRANGEMENT = r"未(?:明确|约定|规定)|尚无"
DENIED_DUTY = r"(?:无需|不必|无须|不予|不得|不)(?:向.{0,12})?(?:交付|移交|交接|返还|提供)|不得(?:解除|终止)"
# Handover objects are separate: a source-code clause cannot prove delivery of
# samples, research records or unfinished work as well.
DEVELOPMENT_EXIT_REQUIREMENTS = {
    "development_delay_liability": ("开发迟延的违约后果", r"(?:逾期|迟延|延期|延迟).{0,45}(?:研发|开发|里程碑|成果交付)|(?:研发|开发|里程碑|成果交付).{0,30}(?:逾期|迟延|延期|延迟)", r"违约责任|违约金|赔偿|承担.{0,15}(?:损失|责任)"),
    "payment_delay_liability": ("付款迟延的违约后果", r"(?:逾期|迟延|延期|延迟)(?:向.{1,12}?)?(?:付款|支付)(?!违约金|赔偿)|(?:付款|支付)(?:期限届满)?(?:逾期|迟延|延期|延迟)|未按(?:期|约定时间|约定期限)(?:付款|支付)(?!违约金|赔偿)", r"违约责任|违约金|赔偿|承担.{0,15}(?:损失|责任)"),
    "development_termination_mechanism": ("开发合同解除或终止机制", r"合同|开发|研发|合作|项目", r"(?:可以|有权|有权要求|可|应)(?:书面|通知另一方|通知对方|要求)?(?:解除|终止)|(?:解除|终止)(?:本)?合同.{0,10}(?:情形|条件)|合同(?:可以|可|应当|应)(?:解除|终止)"),
    "exit_research_material_handover": ("提前退出时研发资料交接", r"研发资料|研究资料|研究开发资料|开发文档|技术资料|研发记录", r"交接|移交|交付|返还|提供"),
    "exit_source_code_handover": ("提前退出时源代码交接", r"源代码|源程序", r"交接|移交|交付|返还|提供"),
    "exit_sample_handover": ("提前退出时样品交接", r"样品|样机|试制品", r"交接|移交|交付|返还|提供"),
    "exit_stage_result_handover": ("提前退出时阶段成果交接", r"阶段成果|阶段性成果|已(?:经)?完成(?:的)?(?:项目|开发|研发)?成果|未完成成果|未完成的成果", r"交接|移交|交付|返还|提供"),
    "exit_unfinished_result_ownership": ("提前退出时未完成成果归属", r"未完成.{0,8}(?:成果|模块|研发)|未完成部分", r"归.{0,25}(?:所有|享有)|权利归|成果归属|知识产权归|由.{0,20}享有"),
    "exit_development_cost_settlement": ("提前退出时开发费用结算", r"研发(?:费用|经费)|开发(?:费用|经费)|研究开发经费|已发生费用|已支付费用|未发生费用|研发费|开发费|费用|价款", r"结算|结清|退还|退回|退付|返还|扣除|调减|不予退还|继续支付"),
}


def _development_delay_remedies(clauses):
    """Resolve event -> remedy links within an operative provision.

    An ensuing remedy may refer to the preceding development-delay condition.
    Keep the premise and consequence as separate original spans, never as a
    stitched quotation. A new, unrelated trigger ends that relation.
    """
    delay = r'迟延|逾期|延期|延迟|未按期'
    task = r'研发|开发|里程碑|成果交付'
    remedy = r'违约金|赔偿|承担.{0,20}(?:损失|责任)|(?:有权|可以|可)(?:解除|终止)'
    other_event = r'保密|泄密|侵权|不可抗力|付款|支付费用|支付价款'
    result = []
    previous_clause = None
    premises = []
    for clause, heading, quote in _segments(clauses):
        if clause.clause_id != previous_clause:
            premises = []
            previous_clause = clause.clause_id
        compact = re.sub(r'\s+', '', quote)
        if re.search(other_event, compact) or re.search(r'不承担.{0,18}(?:责任|损失)|无需.{0,12}赔偿', compact):
            premises = []
            continue
        project_stage = re.search(r'项目延期|开发进度|研发进度', heading) and re.search(r'阶段|核心功能|任务', compact)
        direct_event = re.search(delay, compact) and (re.search(task, compact + heading) or project_stage)
        reference = bool(premises and re.search(r'延期|延迟|迟延|逾期|因此|由此|上述|违约方|因.{0,12}违约造成', compact))
        if not direct_event and not reference:
            premises = []
            continue
        source = dict(clause_id=clause.clause_id, quote=quote, source_domain='DEVELOPMENT_EXIT',
                      deferred=bool(re.search(DEFERRED, compact)),
                      adverse=bool(re.search(DENIED_DUTY, compact)))
        if re.search(remedy, compact):
            context = [dict(clause_id=p['clause_id'], quote=p['quote'],
                            evidence_role='DEVELOPMENT_DELAY_TRIGGER') for p in premises]
            if context:
                source['domain_context_evidence'] = context
            for row in [*premises, source]:
                if not any(r['clause_id'] == row['clause_id'] and r['quote'] == row['quote'] for r in result):
                    result.append(row)
        if direct_event or reference:
            premises.append(source)
    return result


def development_exit_elements(clauses):
    """Classify presence without substituting normal delivery for exit duties."""
    facts = {key: [] for key in DEVELOPMENT_EXIT_REQUIREMENTS}
    # Colon-led conditions govern their following consequence. Keep an exact
    # contiguous span; a different liability event cannot donate its remedy.
    from review_v2.proposition_scope import arrangement_matches
    label, trigger, consequence = DEVELOPMENT_EXIT_REQUIREMENTS['payment_delay_liability']
    for clause, _, quote in _segments(clauses):
        if re.search(trigger, re.sub(r'\s+', '', quote)) and re.search(consequence, quote):
            if not re.search(r'未(?:明确|约定)|尚未|无需支付违约金|不承担', quote):
                facts['payment_delay_liability'].append(dict(clause_id=clause.clause_id, quote=quote,
                    source_domain='DEVELOPMENT_EXIT', deferred=False, adverse=False))
    development_context = any(re.search(r"技术开发|委托开发|研发|研究开发", c.text) for c in clauses)
    # A defined software-only delivery scope does not entail a physical sample.
    # A mention of hardware/samples anywhere keeps the requirement active.
    from review_v2.obligation_detail_elements import _delivery_sources
    outputs = [obj for _, obj, _ in _delivery_sources(clauses)]
    # Software deliverables may be part of an embodied system. Physical
    # integration/validation prevents a software-only applicability inference.
    physical_integration = any(re.search(
        r'(?:机器人|生产线|机械|机床|实物|样件).{0,16}(?:集成|调试|试运行|验证|抓取)'
        r'|(?:集成|调试|试运行|验证).{0,16}(?:机器人|生产线|机械|机床|实物|样件)', c.text)
        for c in clauses)
    software_only = bool(outputs and any(re.search(r'源代码|软件|可执行|数据库|API', q) for q in outputs)
                         and not physical_integration
                         and not any(re.search(r'样品|样机|试制品|硬件|设备研发|设备开发|开发设备', c.text) for c in clauses))
    for clause in clauses:
        heading = " ".join(getattr(clause, "heading_path", None) or [])
        title = getattr(clause, "title", "") or ""
        context = heading + " " + title
        for sentence in re.split(r"[。；;\n]", clause.text):
            sentence = sentence.strip()
            compact = re.sub(r"\s+", "", sentence)
            if not compact:
                continue
            for key, (_, subject, action) in DEVELOPMENT_EXIT_REQUIREMENTS.items():
                exit_bound = bool(re.search(EXIT_EVENT, context + compact))
                if key.startswith("exit_") and not exit_bound:
                    continue
                if key.startswith("exit_") and re.search(r"正常履行|正常交付|项目完成时|验收合格后", compact):
                    # A heading covering both routine performance and exit
                    # cannot convert routine delivery into an exit obligation.
                    if not re.search(EXIT_EVENT, compact):
                        continue
                operative = re.sub(r"已(?:经)?(?:交付|移交|交接|提供|返还)", "", compact)
                development_delivery = (key == "development_delay_liability"
                                        and (re.search(r"研发|开发|技术|成果", context) or development_context)
                                        and re.search(r"(?:迟延|逾期|延期|延迟)交付|交付(?:迟延|逾期|延期|延迟)|未按.{0,12}(?:时间|期限).{0,12}(?:完成|交付).{0,12}(?:交付|成果)|未按期.{0,8}交付", compact))
                from review_v2.technology_fact_ontology import mentions_document
                canonical_document = (key == 'exit_research_material_handover'
                                      and mentions_document('generic_technical_documentation', compact, context))
                completed_artifact = (key == 'exit_stage_result_handover'
                                      and bool(re.search(r'已(?:经)?完成的', compact))
                                      and (mentions_document('source_and_executable_delivery', compact, context)
                                           or mentions_document('generic_technical_documentation', compact, context)))
                generic_project_materials = (key == "exit_research_material_handover" and development_context
                                             and bool(re.search(r"(?:项目|研发|开发)成果.{0,8}相关资料|项目资料|项目数据", compact)))
                if not (re.search(subject, compact) or development_delivery or generic_project_materials or canonical_document or completed_artifact) or not re.search(action, operative):
                    continue
                deferred = bool(re.search(DEFERRED, compact)) or generic_project_materials or completed_artifact
                if re.search(NO_ARRANGEMENT, compact) and not deferred:
                    continue
                # Cost settlement is presence, not a mandatory refund rule.
                # In contrast an express denial of a handover/exit right is
                # retained as contrary evidence, never converted to absence.
                adverse = key != "exit_development_cost_settlement" and bool(re.search(DENIED_DUTY, compact))
                facts[key].append({"clause_id": clause.clause_id, "quote": sentence,
                                   "source_domain": "DEVELOPMENT_EXIT", "deferred": deferred, "adverse": adverse})
    # Canonical delay consequences include termination and damages, not only a
    # numeric penalty. Existing single-sentence predicates keep their sources.
    for source in _development_delay_remedies(clauses):
        if not any(row['clause_id'] == source['clause_id'] and
                   row['quote'].rstrip('。；;') == source['quote'].rstrip('。；;')
                   for row in facts['development_delay_liability']):
            facts['development_delay_liability'].append(source)
    elements = []
    from review_v2.proposition_scope import scoped_propositions
    termination_gaps = []
    for clause in clauses:
        for proposition in scoped_propositions(clause.text):
            q = proposition['quote']
            if (proposition['polarity'] == 'MISSING'
                    and re.search(r'暂停|无法继续|履行受阻', q)
                    and re.search(r'解除|终止', q)):
                party = re.search(r'([甲乙丙]方|委托方|开发方)[^，,。；]{0,35}(?:是否|能否|有权|享有)[^，,。；]{0,12}(?:解除|终止)', q)
                if party:
                    termination_gaps.append(dict(clause_id=clause.clause_id, quote=q,
                        required_fact=party[1]+'在履行受阻或长期暂停时的解除权'))
    for key, (label, subject, action) in DEVELOPMENT_EXIT_REQUIREMENTS.items():
        sources = facts[key]
        adverse = [row for row in sources if row["adverse"]]
        direct = [row for row in sources if not row["deferred"] and not row["adverse"]]
        supporting = adverse or direct or sources
        status = "ADVERSE" if adverse else "COVERED" if direct else "PARTIALLY_COVERED" if sources else "MISSING"
        if key == 'exit_sample_handover' and not sources and software_only:
            status = 'NOT_APPLICABLE'
        residual = ({
            "exit_development_cost_settlement": "提前退出时开发费用结算的计算方式",
            "exit_research_material_handover": "提前退出时研发资料交接的具体范围",
            "exit_stage_result_handover": "除已列明代码和文档外其他已完成阶段成果的交接范围",
        }.get(key, label) if status == "PARTIALLY_COVERED" else label)
        if key == 'development_termination_mechanism' and direct and not adverse and termination_gaps:
            status = 'PARTIALLY_COVERED'
            residual = '、'.join(dict.fromkeys(g['required_fact'] for g in termination_gaps))
        elements.append({
            "element_id": key, "source_fact_key": key, "required_fact": label,
            "status": status, "risk_relevant": status != 'NOT_APPLICABLE',
            "proposition": ("；".join(row["quote"] for row in adverse) if adverse else label + ("已有明确约定" if direct else "已有原则安排，但具体内容仍待确定" if sources else "")),
            "residual_gap": residual if status == "PARTIALLY_COVERED" else "",
            "search_targets": [] if status == 'NOT_APPLICABLE' else [residual], "query_patterns": [subject, action],
            **({'conditional_element': True, 'prerequisite_status': 'FALSE',
                'prerequisite_fact': '已明确的软件交付范围内无实物样品/样机交付对象'}
               if status == 'NOT_APPLICABLE' else {}),
            "bound_evidence_ids": list(dict.fromkeys(row["clause_id"] for row in supporting)),
            "supporting_evidence": supporting,
            **({'explicit_absence_evidence': termination_gaps}
               if key == 'development_termination_mechanism' and termination_gaps else {}),
        })
    return elements
