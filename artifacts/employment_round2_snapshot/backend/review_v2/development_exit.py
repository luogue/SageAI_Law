"""Event-bound atomic requirements for development delay and early exit."""
import re


EXIT_EVENT = r"解除|终止|提前退出|退出(?:项目|合作)|研发失败|开发失败"
DEFERRED = r"另行(?:协商|商定|约定)|后续(?:协商|商定|约定)|待(?:协商|商定|约定)|具体.{0,16}未(?:明确|约定)"
NO_ARRANGEMENT = r"未(?:明确|约定|规定)|尚无"
DENIED_DUTY = r"(?:无需|不必|无须|不予|不得|不)(?:向.{0,12})?(?:交付|移交|交接|返还|提供)|不得(?:解除|终止)"
# Handover objects are separate: a source-code clause cannot prove delivery of
# samples, research records or unfinished work as well.
DEVELOPMENT_EXIT_REQUIREMENTS = {
    "development_delay_liability": ("开发迟延的违约后果", r"(?:逾期|迟延|延期|延迟).{0,45}(?:研发|开发|里程碑|成果交付)|(?:研发|开发|里程碑|成果交付).{0,30}(?:逾期|迟延|延期|延迟)", r"违约责任|违约金|赔偿|承担.{0,15}(?:损失|责任)"),
    "payment_delay_liability": ("付款迟延的违约后果", r"(?:逾期|迟延|延期|延迟).{0,12}(?:付款|支付)|(?:付款|支付).{0,16}(?:逾期|迟延|延期|延迟)", r"违约责任|违约金|赔偿|承担.{0,15}(?:损失|责任)"),
    "development_termination_mechanism": ("开发合同解除或终止机制", r"合同|开发|研发|合作|项目", r"(?:可以|有权|有权要求|可|应)(?:书面|通知另一方|通知对方|要求)?(?:解除|终止)|(?:解除|终止)(?:本)?合同.{0,10}(?:情形|条件)|合同(?:可以|可)?(?:解除|终止)"),
    "exit_research_material_handover": ("提前退出时研发资料交接", r"研发资料|研究资料|研究开发资料|开发文档|技术资料|研发记录", r"交接|移交|交付|返还|提供"),
    "exit_source_code_handover": ("提前退出时源代码交接", r"源代码|源程序", r"交接|移交|交付|返还|提供"),
    "exit_sample_handover": ("提前退出时样品交接", r"样品|样机|试制品", r"交接|移交|交付|返还|提供"),
    "exit_stage_result_handover": ("提前退出时阶段成果交接", r"阶段成果|阶段性成果|已完成成果|已完成的成果|未完成成果|未完成的成果", r"交接|移交|交付|返还|提供"),
    "exit_unfinished_result_ownership": ("提前退出时未完成成果归属", r"未完成.{0,8}(?:成果|模块|研发)|未完成部分", r"归.{0,25}(?:所有|享有)|权利归|成果归属|知识产权归|由.{0,20}享有"),
    "exit_development_cost_settlement": ("提前退出时开发费用结算", r"研发(?:费用|经费)|开发(?:费用|经费)|研究开发经费|已发生费用|已支付费用|未发生费用|研发费|开发费|费用|价款", r"结算|结清|退还|退回|退付|返还|扣除|调减|不予退还|继续支付"),
}


def development_exit_elements(clauses):
    """Classify presence without substituting normal delivery for exit duties."""
    facts = {key: [] for key in DEVELOPMENT_EXIT_REQUIREMENTS}
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
                if not re.search(subject, compact) or not re.search(action, operative):
                    continue
                deferred = bool(re.search(DEFERRED, compact))
                if re.search(NO_ARRANGEMENT, compact) and not deferred:
                    continue
                # Cost settlement is presence, not a mandatory refund rule.
                # In contrast an express denial of a handover/exit right is
                # retained as contrary evidence, never converted to absence.
                adverse = key != "exit_development_cost_settlement" and bool(re.search(DENIED_DUTY, compact))
                facts[key].append({"clause_id": clause.clause_id, "quote": sentence,
                                   "source_domain": "DEVELOPMENT_EXIT", "deferred": deferred, "adverse": adverse})
    elements = []
    for key, (label, subject, action) in DEVELOPMENT_EXIT_REQUIREMENTS.items():
        sources = facts[key]
        adverse = [row for row in sources if row["adverse"]]
        direct = [row for row in sources if not row["deferred"] and not row["adverse"]]
        supporting = adverse or direct or sources
        status = "ADVERSE" if adverse else "COVERED" if direct else "PARTIALLY_COVERED" if sources else "MISSING"
        elements.append({
            "element_id": key, "source_fact_key": key, "required_fact": label,
            "status": status, "risk_relevant": True,
            "proposition": ("；".join(row["quote"] for row in adverse) if adverse else label + ("已有明确约定" if direct else "已有原则安排，但具体内容仍待确定" if sources else "")),
            "search_targets": [label], "query_patterns": [subject, action],
            "bound_evidence_ids": list(dict.fromkeys(row["clause_id"] for row in supporting)),
            "supporting_evidence": supporting,
        })
    return elements
