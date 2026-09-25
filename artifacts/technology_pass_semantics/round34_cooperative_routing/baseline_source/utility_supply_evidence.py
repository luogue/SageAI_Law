"""Utility-supply evidence normalization for Review V2.

This layer prevents generic keyword hits from turning conflicted utility
clauses into PASS results.  It keeps the scope narrow: only utility-supply
nodes whose semantics need element-level checks are overridden here.
"""

from __future__ import annotations

import re
from typing import Dict, Iterable, List, Sequence, Tuple
from review_v2.evidence_compatibility import QUALITY_PATTERN


Element = Tuple[str, str, str]

# Domain declarations constrain both candidate retrieval and final evidence binding.
REQUIRED_EVIDENCE_DOMAINS = {
    "quality_evidence_record": {
        "quality_monitoring": "supply_quality_measurement",
        "quality_record_preservation": "supply_quality_measurement",
    },
}


def _compact(text: str) -> str:
    return re.sub(r"\s+", "", text or "")


def _sentences(text: str) -> List[str]:
    return [part for part in re.split(r"[。；;\n]", text or "") if part.strip()]


def _evidence(clause, node_id: str, keys: Sequence[str]) -> Dict[str, str]:
    return {
        "clause_id": clause.clause_id,
        "location": clause.location,
        "text": clause.text,
        "quote": clause.text,
        "source_type": "SOURCE_CLAUSE",
        "supported_elements": list(keys),
        "supports_element_ids": list(keys),
        "supporting_element_ids": list(keys),
        "element_ids": list(keys),
        "evidence_id": f"US-DIRECT-{node_id}-{clause.clause_id}",
        "evidence_claim_id": f"US-DIRECT-{node_id}-{clause.clause_id}",
        "support_type": "DIRECT",
        "relevance_score": 1.0,
        "selection_reason": "Utility-supply semantic evidence directly supports the resolved atomic element.",
        "sentence_index": 1,
        "document_id": "contract_package/main",
        "document_type": "CONTRACT_TEXT",
        "source_document_type": "CONTRACT_TEXT",
        "document_name": "合同正文",
        "section": clause.location,
        "evidence_type": "CONTRACT_TEXT",
        "raw_text": clause.text,
    }


def _find_supports(clauses, node_id: str, elements: Sequence[Element]) -> Tuple[set, List[Dict[str, str]]]:
    from review_v2.evidence_compatibility import evidence_compatible, evidence_domains
    covered = set()
    evidence = []
    domains = REQUIRED_EVIDENCE_DOMAINS.get(node_id, {})
    for clause in clauses:
        if domains:
            # A mixed clause may discuss several domains. Bind only the exact
            # supporting sentence, never borrow a neighbouring sentence's type.
            for index, sentence in enumerate(_sentences(clause.text)):
                keys = [key for key, _, pattern in elements if re.search(pattern, sentence)
                        and evidence_compatible(sentence, domains.get(key))
                        and not re.search(r"(?:不予|无需|不必|不进行|不保存|不提供)[^。；]{0,12}(?:监测|检测|记录|保存)", sentence)]
                if keys:
                    row = _evidence(clause, node_id, keys)
                    row.update(text=sentence, quote=sentence, raw_text=sentence,
                               sentence_index=index + 1, source_domains=sorted(evidence_domains(sentence)))
                    row["evidence_id"] += f"-S{index + 1}"
                    row["evidence_claim_id"] = row["evidence_id"]
                    evidence.append(row)
                    covered.update(keys)
            continue
        keys = [key for key, _, pattern in elements if re.search(pattern, clause.text)]
        if keys:
            covered.update(keys)
            evidence.append(_evidence(clause, node_id, keys))
    return covered, evidence


def _find_clauses(clauses, pattern: str) -> List[Dict[str, str]]:
    rows = []
    for clause in clauses:
        if re.search(pattern, clause.text):
            rows.append(_evidence(clause, "adverse", ["adverse_arrangement"]))
    return rows


def _normalize_element_source_ids(item, evidence: Sequence[Dict[str, str]]) -> None:
    by_element: Dict[str, List[str]] = {}
    for row in evidence:
        for key in row.get("supported_elements") or row.get("supports_element_ids") or []:
            by_element.setdefault(key, []).append(row["clause_id"])
    for element in item.coverage_elements or []:
        key = element.get("element_id")
        if key in by_element and element.get("status") in {"COVERED", "PARTIALLY_COVERED", "ADVERSE", "CONFLICTING"}:
            element["source_clause_ids"] = list(dict.fromkeys(by_element[key]))
    item.decision_trace["coverage_elements"] = item.coverage_elements
    item.decision_trace["specialized_elements"] = [dict(row) for row in item.coverage_elements or []]


def _has_attachment_entity(text: str, terms: Iterable[str]) -> bool:
    term_alt = "|".join(re.escape(term) for term in terms)
    if not term_alt:
        return False
    return bool(re.search(
        rf"(?:附件[一二三四五六七八九十\d]*|本合同附件|附件清单|作为(?:本)?合同附件|详见附件)[^。；\n]{{0,160}}(?:{term_alt})"
        rf"|(?:{term_alt})[^。；\n]{{0,80}}(?:作为(?:本)?合同附件|列为附件|详见附件|附件[一二三四五六七八九十\d]*)",
        text,
    ))


def _adverse_patterns(node_id: str) -> Tuple[str, str]:
    if node_id in {"planned_interruption_notice", "temporary_interruption_notice", "no_notice_interruption_clause"}:
        return (
            r"(?:计划检修[^。；]{0,40}(?:仅|只)?提前24小时通知|临时检修[^。；]{0,80}(?:先停|停电后通知|事后通知)|未提前通知[^。；]{0,40}(?:免责|不承担赔偿|不承担责任))",
            "中断供应通知安排存在过短通知、先停后通知或未通知免责等削弱用户保护的约定。",
        )
    if node_id in {"suspension_after_demand_period", "suspension_procedure_compliance"}:
        return (
            r"(?:欠费[^。；]{0,40}(?:5|五)日[^。；]{0,40}(?:停电|停止供电|中止|停供)|欠费[^。；]{0,40}(?:直接|立即)[^。；]{0,20}(?:停电|停止供电|中止|停供)|(?:无需|无须|不经|不需要)[^。；]{0,15}(?:催告|通知|合理期限)[^。；]{0,40}(?:停电|停止供电|中止|停供|补缴)|(?:停电|停止供电|中止|停供)[^。；]{0,60}(?:无需|无须|不经|不需要)[^。；]{0,15}(?:催告|通知|合理期限))",
            "欠费中止供应被约定为无需催告、无需合理期限或无需通知即可实施。",
        )
    if node_id == "emergency_repair_time_limit":
        return (
            r"(?:不承诺[^。；]{0,20}(?:抢修完成时间|具体抢修|恢复时间)|抢修[^。；]{0,60}(?:不得|不得要求|不予)[^。；]{0,20}(?:赔偿|索赔))",
            "合同未承诺具体抢修完成时间或以免责条款削弱抢修迟延责任。",
        )
    if node_id in {"quality_nonconform_remedy", "safe_continuous_supply_obligation"}:
        return (
            r"(?:供电质量[^。；]{0,80}(?:赔偿|责任)[^。；]{0,20}(?:封顶|上限|不超过)[^。；]{0,30}(?:20%|百分之二十)|长期停电[^。；]{0,80}(?:仅退|只退)[^。；]{0,30}基本电费|排除其他赔偿)",
            "供应质量或持续供应责任被设置低额责任上限、仅退基本电费或排除其他赔偿。",
        )
    if node_id == "contract_change_or_termination":
        return (
            r"(?:不经济|不合理|增加(?:经营|运营|履约)?成本|增加(?:经营|运营|履约)?风险)[^。；]{0,80}(?:调整供电方式|调整容量|解除合同|提前[^。；]{0,10}解除)",
            "供应方因自身认为不经济、不合理、增加成本或风险即可单方调整或解除。",
        )
    return ("", "")


def _set_atomic_item(item, elements: Sequence[Element], clauses, *, risk_level: str | None = None) -> None:
    from review_v2.engine import _set_item_missing, _set_item_partial, _set_item_pass, _set_multi_element_state

    covered, evidence = _find_supports(clauses, item.node_id, elements)
    specs = [
        {"element_id": key, "proposition": proposition, "terms": [proposition], "semantic_patterns": [pattern]}
        for key, proposition, pattern in elements
    ]
    item.decision_trace["semantic_requirements"] = specs
    item.decision_trace["required_evidence_domains"] = REQUIRED_EVIDENCE_DOMAINS.get(item.node_id, {})
    if len(covered) == len(elements):
        _set_item_pass(item, [], "已覆盖：" + "；".join(p for _, p, _ in elements) + "。", "上述要素均有对应原文支持。")
        item.suggested_clause_example = ""
    elif covered:
        missing = [p for key, p, _ in elements if key not in covered]
        reason = "尚需明确：" + "；".join(missing) + "。"
        _set_item_partial(item, [], risk_level or item.risk_level, reason, reason)
        item.suggested_clause_example = "建议补充明确" + "；".join(missing) + "。"
    else:
        reason = "尚需明确：" + "；".join(p for _, p, _ in elements) + "。"
        _set_item_missing(item, risk_level or item.risk_level, reason, reason, "utility_supply_atomic_evidence")
    item.evidence_clauses = evidence
    item.evidence_location = "；".join(dict.fromkeys(row["location"] for row in evidence))
    item.judge_source = "utility_supply_atomic_evidence"
    _set_multi_element_state(
        item,
        [
            {
                "element_id": key,
                "status": "COVERED" if key in covered else "MISSING",
                "proposition": proposition,
                "terms": [proposition],
                "semantic_patterns": [pattern],
                "bound_evidence_ids": [
                    row["evidence_id"] for row in evidence if key in row.get("supported_elements", [])
                ],
            }
            for key, proposition, pattern in elements
        ],
        evidence,
    )
    _normalize_element_source_ids(item, evidence)


def _set_adverse_if_found(item, clauses, *, assessment=None) -> bool:
    from review_v2.engine import _register_element_bound_core_claims, _set_multi_element_state

    pattern, reason = assessment if assessment else _adverse_patterns(item.node_id)
    if not pattern:
        return False
    evidence = _find_clauses(clauses, pattern)
    if not evidence:
        return False
    element_id = f"{item.node_id}_adverse_arrangement"
    for row in evidence:
        row["supported_elements"] = [element_id]
        row["supports_element_ids"] = [element_id]
        row["supporting_evidence"] = [{"clause_id": row["clause_id"], "quote": row["quote"]}]
    item.risk_level = item.risk_level if item.risk_level in {"高", "中"} else "高"
    item.status = "风险条款"
    item.coverage_status = "风险条款"
    item.issue_type = "风险条款"
    item.risk_status = "ADVERSE"
    item.reasoning_summary = reason
    item.risk_point_description = reason
    item.legal_consequence_if_missing = reason
    item.evidence_clauses = evidence
    item.evidence_location = "；".join(dict.fromkeys(row["location"] for row in evidence))
    item.suggested_clause_example = "建议删除或限制上述免责、无需通知、无需催告或单方调整/解除安排，并按法定程序设置通知、合理期限、抢修和赔偿规则。"
    item.judge_source = "utility_supply_adverse_evidence"
    _set_multi_element_state(item, [{
        "element_id": element_id,
        "status": "ADVERSE",
        "presence_status": "COVERED",
        "direction": "ADVERSE",
        "risk_relevant": True,
        "proposition": reason,
        "terms": [reason],
        "semantic_patterns": [pattern],
        "bound_evidence_ids": [row["evidence_id"] for row in evidence],
        "supporting_evidence": [
            {"clause_id": row["clause_id"], "quote": row["quote"], "proposition": reason}
            for row in evidence
        ],
    }], evidence)
    _normalize_element_source_ids(item, evidence)
    _register_element_bound_core_claims(item)
    return True


PROFILES: Dict[str, Sequence[Element]] = {
    "quality_evidence_record": (
        ("quality_monitoring", "供应质量参数检测或监测安排", QUALITY_PATTERN),
        ("quality_record_preservation", "供应质量检测记录保存或提供核验", rf"(?=[^。；\n]*(?:(?:保存|保留|留存|提供|核验)[^。；]{{0,35}}(?:数据|记录|报告)|(?:检测|监测|检验)(?:数据|记录|报告))){QUALITY_PATTERN}"),
    ),
    "temporary_supply_measures": (
        ("temporary_supply_plan", "重要用户临时供应或备用保障方案", r"(?:提供|配备|启用|安排|制定|保障)[^。；]{0,40}(?:临时供电|临时供应|应急供水|备用电源|备用设备|应急保障方案)|(?:临时供电|备用电源|应急保障方案)[^。；]{0,25}(?:提供|启用|配备|制定)"),
    ),
    "critical_user_termination_limit": (
        ("critical_user_cutoff_procedure", "重要用户停供或解除专门程序", r"重要(?:电力)?用户[^。；]{0,50}(?:停电|停供|中止|解除)[^。；]{0,50}(?:报送|审批|备案|预案|主管部门)"),
        ("critical_user_transition", "重要用户停供前必要过渡保障", r"(?:停电|停供|中止|解除)[^。；]{0,40}(?:过渡措施|应急保障|备用电源|临时供应)"),
    ),
    "safe_economical_planned_use": (
        ("safe_use", "安全使用公共供应资源", r"(?:安全用电|安全用水|安全用气|安全用热|安全使用|按照国家有关规定[^。；]{0,20}安全[^。；]{0,10}(?:用电|用水|用气|用热)|不得[^。；]{0,60}(?:危害|影响|破坏)[^。；]{0,30}(?:电网|供电安全|公共安全|供应安全))"),
        ("economical_use", "节约使用公共供应资源", r"(?:节约用电|节约用水|节约用气|节约用热|节约使用|合理节约[^。；]{0,20}(?:电|水|气|热力|能源))"),
        ("planned_use", "按计划或核定用途使用公共供应资源", r"(?:计划用电|计划用水|计划用气|计划用热|按计划使用|按照核定用途|不得超计划|不得超容量|不得超负荷)"),
    ),
    "illegal_use_prohibition": (
        ("unauthorized_facility_change", "禁止擅自改动供用设施", r"(?:不得|禁止|严禁)[^。；]{0,50}(?:擅自|私自)[^。；]{0,30}(?:改动|改装|拆除|移动)[^。；]{0,30}(?:设施|线路|管线|设备)"),
        ("grid_safety_harm", "禁止危害电网或公共供应安全", r"(?:不得|禁止|严禁)[^。；]{0,50}(?:危害|影响|破坏)[^。；]{0,30}(?:电网|供电安全|公共安全|供应安全)"),
        ("meter_tampering", "禁止破坏或绕越计量装置", r"(?:不得|禁止|严禁)[^。；]{0,50}(?:破坏|绕越|绕表|私接)[^。；]{0,30}(?:计量|电表|水表|气表|热量表)"),
        ("electricity_theft", "禁止窃用或盗用公共供应资源", r"(?:不得|禁止|严禁)[^。；]{0,50}(?:窃电|偷电|窃用|盗用)"),
    ),
    "billing_standard_method": (
        ("metering_basis", "计量依据或计量结果作为计费基础", r"(?:(?:按|依据|根据|以)[^。；]{0,50}(?:计量|抄表|表计|电表|水表|气表|热量表|计量装置)[^。；]{0,60}(?:计费|收费|结算|计算|确定费用|作为[^。；]{0,12}(?:结算|计费|收费)依据)|(?:计量|抄表|表计|电表|水表|气表|热量表|计量装置)[^。；]{0,50}(?:记录|显示|结果|数据|数量)[^。；]{0,50}(?:作为[^。；]{0,12}(?:结算|计费|收费)依据|结算|计费|收费|计算)|按实际[^。；]{0,10}(?:抄表数|计量数量|计量结果)[^。；]{0,20}(?:结算|计费|收费)|(?:结算依据|计费依据|收费依据))"),
        ("price_standard", "电价、收费标准或单价规则", r"(?:电价|水价|气价|热价|收费标准|单价|价格)[^。；]{0,80}(?:元|政府|批准|公示|目录|执行)"),
        ("billing_cycle", "账单周期或抄表周期", r"(?:账单周期|计费周期|抄表周期|每月|按月)[^。；]{0,50}(?:账单|抄表|计费|结算)"),
        ("payment_deadline", "付款期限", r"(?:付款期限|缴费期限|支付期限|应于|应在)[^。；]{0,30}(?:日|工作日|天|日前|内)"),
    ),
    "emergency_repair_time_limit": (
        ("repair_response_time", "抢修响应时间", r"(?:抢修|报修|故障)[^。；]{0,40}(?:\d+|[一二三四五六七八九十]+)[^。；]{0,8}(?:小时|分钟|日|天)[^。；]{0,20}(?:响应|到场|处置|恢复)"),
        ("estimated_restoration_notice", "告知预计恢复时间", r"(?:抢修|报修|故障|停电|断供)[^。；]{0,80}(?:预计恢复|恢复时间|预计[^。；]{0,8}恢复)"),
    ),
}


ATTACHMENT_PROFILES: Dict[str, Tuple[Sequence[str], str]] = {
    "user_address_capacity_attachment": (
        ("供电地址", "用电地址", "用水地址", "用气地址", "供热地址", "地址及容量", "容量表", "容量", "接入点"),
        "用户供应地址、容量及用途附件",
    ),
    "metering_billing_attachment": (
        ("计量装置资料", "检定证书", "收费标准", "价格文件", "抄表规则", "账单样式"),
        "计量计费资料、收费标准或价格文件附件",
    ),
    "boundary_facility_diagram_attachment": (
        ("产权分界确认书", "设施图", "管线图", "线路图", "计量装置位置图", "设备清单", "维护责任划分表"),
        "产权分界、供用设施图或维护责任附件",
    ),
    "notice_repair_record_attachment": (
        ("检修公告", "临时中断通知", "欠费催告", "抢修工单", "报修记录", "恢复供应通知", "费用结算记录"),
        "通知、催告、抢修或恢复供应记录附件",
    ),
}


def _apply_attachment_rule(item, clauses, full_text: str) -> None:
    from review_v2.engine import _set_item_missing, _set_item_partial, _set_item_pass, _set_multi_element_state

    terms, proposition = ATTACHMENT_PROFILES[item.node_id]
    entities = [c for c in clauses if _has_attachment_entity(c.text, terms)]
    has_attachment = bool(entities)
    related = [c for c in clauses if any(term in c.text for term in terms)]
    if item.node_id == "user_address_capacity_attachment":
        related = [c for c in related if re.search(r"地址|容量表|容量[^。；\n]{0,12}\d+\s*(?:kVA|kW|千伏安|千瓦|立方米|吨)", c.text, re.I)]
    evidence = [_evidence(c, item.node_id, ["attachment_entity" if has_attachment else "body_related_arrangement"]) for c in (entities if has_attachment else related)]
    item.decision_trace["semantic_requirements"] = [
        {
            "element_id": "attachment_entity",
            "proposition": proposition,
            "terms": list(terms),
            "semantic_patterns": [
                rf"(?:附件|附件清单|作为(?:本)?合同附件|详见附件)[^。；\n]{{0,160}}(?:{'|'.join(re.escape(term) for term in terms)})"
            ],
        },
    ]
    if has_attachment:
        _set_item_pass(item, [], proposition + "已作为附件或附件清单列明。", proposition + "已有可识别附件实体。")
        item.suggested_clause_example = ""
        status = "COVERED"
    elif related:
        reason = "正文已有相关事项，但未检测到对应附件标题、附件正文、附件清单或明确附件实体。"
        _set_item_partial(item, [], item.risk_level, reason, reason)
        item.suggested_clause_example = "建议将相关资料以附件、附件清单或可核验记录形式固定。"
        status = "MISSING"
    else:
        reason = "未检测到对应附件标题、附件正文、附件清单或明确附件实体。"
        _set_item_missing(item, item.risk_level, reason, reason, "utility_supply_attachment_entity")
        status = "MISSING"
    item.evidence_clauses = evidence
    item.evidence_location = "；".join(dict.fromkeys(row["location"] for row in evidence))
    item.judge_source = "utility_supply_attachment_entity"
    elements = [{
        "element_id": "attachment_entity",
        "status": status,
        "proposition": proposition,
        "terms": list(terms),
        "semantic_patterns": [rf"(?:附件|附件清单|作为(?:本)?合同附件|详见附件)[^。；\n]{{0,160}}(?:{'|'.join(re.escape(term) for term in terms)})"],
        "bound_evidence_ids": [row["evidence_id"] for row in evidence] if has_attachment else [],
    }]
    if related and not has_attachment:
        elements.append({
            "element_id": "body_related_arrangement", "status": "COVERED",
            "proposition": "正文列有相关地址、容量或资料事项（不代表附件存在）",
            "terms": list(terms), "semantic_patterns": ["|".join(re.escape(t) for t in terms)],
            "bound_evidence_ids": [row["evidence_id"] for row in evidence],
        })
    _set_multi_element_state(item, elements, evidence)
    _normalize_element_source_ids(item, evidence)


def _apply_parameters(item, clauses, full_text):
    """Resolve existence, source-bound parameters, conditions, then coverage.

    Electricity standards must never be applied to water/gas/heat by title alone.
    Article 100's agreed-departure proviso is retained in the risk explanation.
    """
    from review_v2.parameter_validation import extract_parameters, compare
    from review_v2.engine import _set_item_partial, _set_multi_element_state

    restoring = item.node_id == "restoration_commitment"
    if item.node_id not in {"restoration_commitment", "overdue_fee_liquidated_damage"}:
        return False
    if not re.search(r"供电|用电|电费", full_text):
        return False
    topic = r"恢复供电" if restoring else r"违约金|滞纳金"
    selected = [(c, s) for c in clauses for s in _sentences(c.text)
                if re.search(topic, s) and (restoring or re.search(r"逾期|滞纳|(?:欠费|电费)[^。；]{0,60}(?:计算|标准|承担|支付违约金)", s))]
    if not selected:
        return False
    checks, problems, unresolved = [], [], []
    is_other = bool(re.search(r"非居民|工业|生产用电|厂区|工厂", full_text))
    is_resident = not is_other and bool(re.search(r"居民用户|居民用电|生活用电", full_text))
    for clause, sentence in selected:
        values = [p for p in extract_parameters(sentence) if p["kind"] == ("duration" if restoring else "ratio")]
        for value in values:
            value["clause_id"] = clause.clause_id
        if restoring:
            # The 24-hour obligation concerns elimination of the interruption cause.
            triggered = bool(re.search(r"欠费|缴|付清|原因消除|消除原因", sentence))
            if not triggered:
                unresolved.append("复电承诺适用的停供原因及消除条件")
                continue
            if re.search(r"原则上|视情况|酌情|不承诺|尽可能", sentence):
                problems.append("复电承诺使用酌情或原则性措辞，未形成确定的恢复时限")
            for value in values:
                outcome = compare(value, 24)
                checks.append(dict(parameter=value, maximum=24, unit="hours", result=outcome))
                if outcome == "ADVERSE":
                    problems.append("约定复电期限超过停供原因消除后24小时的标准")
                elif outcome != "COVERED":
                    unresolved.append("工作日表述与24小时复电期限的衔接")
            if not values:
                unresolved.append("明确的复电时限")
        else:
            for value in values:
                # Resolve conditions at the parameter span, not from another rate's clause.
                context = sentence[max(0, value["start"] - 55):value["start"]]
                year_matches = list(re.finditer(r"跨(?:日历年|年度|年)|往年|当年|本年", context))
                year = "cross_year" if year_matches and re.search(r"跨|往", year_matches[-1].group()) else "current_year"
                daily = bool(re.search(r"每日|每天|每逾期一日|按日|日计", sentence))
                maximum = .001 if is_resident else (.003 if year == "cross_year" else .002) if is_other else None
                outcome = compare(value, maximum, condition=daily and (is_resident or is_other))
                checks.append(dict(parameter=value, maximum=maximum, user_category="non_resident" if is_other else "resident" if is_resident else "unknown", arrears_year=year,
                                   year_condition_explicit=bool(year_matches), daily=daily, result=outcome))
                if outcome == "ADVERSE":
                    problems.append("欠费违约金比例高于对应用户类别或当年欠费的通常标准，存在加重用户负担及适用条件争议；应结合第100条另有约定条款、第102条责任限度核验")
                elif outcome != "COVERED":
                    unresolved.append("用户类别、欠费年度及按日计算的适用条件")
            if not values:
                unresolved.append("欠费违约金计算比例")
            if not re.search(r"逾期|到期次日", sentence):
                unresolved.append("违约金自逾期起算的时间")
    direct_pattern = "|".join(re.escape(s) for _, s in selected)
    trace = dict(checks=checks, unresolved=list(dict.fromkeys(unresolved)), problems=list(dict.fromkeys(problems)),
                 legal_basis="《供电营业规则》（2024）第72条" if restoring else "《供电营业规则》（2024）第100、102条",
                 source_url="https://www.moj.gov.cn/pub/sfbgw/flfggz/flfggzbmgz/202410/t20241031_508786.html")
    if problems:
        _set_adverse_if_found(item, clauses, assessment=(direct_pattern, "；".join(dict.fromkeys(problems)) + "。"))
        item.suggested_clause_example = ("建议明确停供原因消除后24小时内恢复供电，删除削弱时限的酌情表述。" if restoring else "建议按用户类别区分当年及跨年度欠费，明确计算比例、起止日，并核验另行约定与责任限度及过高违约金调整规则的衔接。")
    else:
        _set_atomic_item(item, (("parameterized_obligation", "恢复供应承诺" if restoring else "欠费违约金计算安排", direct_pattern),), clauses)
        if unresolved:
            reason = "已有相关义务安排；尚需核验或明确：" + "；".join(dict.fromkeys(unresolved)) + "。"
            _set_item_partial(item, [], "中", reason, reason)
            item.suggested_clause_example = "建议核验或明确" + "；".join(dict.fromkeys(unresolved)) + "。"
            # Preserve the positive source; incomplete parameters do not erase existence.
            item.evidence_clauses = [_evidence(c, item.node_id, ["parameterized_obligation"]) for c, _ in selected]
            item.evidence_location = "；".join(dict.fromkeys(c.location for c, _ in selected))
            elements = [dict(row) for row in item.coverage_elements]
            for index, requirement in enumerate(dict.fromkeys(unresolved)):
                elements.append(dict(element_id=f"parameter_condition_{index}", proposition=requirement,
                                     status="MISSING", terms=[requirement], bound_evidence_ids=[]))
            _set_multi_element_state(item, elements, item.evidence_clauses)
            _normalize_element_source_ids(item, item.evidence_clauses)
        else:
            item.reasoning_summary = "已识别义务及参数，并完成当前适用条件下的期限或比例校验。"
    item.decision_trace["parameter_validation"] = trace
    item.legal_basis_index = trace["legal_basis"] + ("；《民法典》第654条" if restoring else "；《民法典》第585条、第654条")
    return True


def apply(items, clauses):
    full_text = "\n".join(c.text for c in clauses)
    for item in items:
        # Post-processing must respect the already resolved pre-retrieval gate.
        if item.coverage_status in {"INSUFFICIENT_CONTEXT", "不适用", "NOT_APPLICABLE"}:
            continue
        if item.node_id == "mandatory_contracting_obligation":
            reason = "当前已进入具体供用合同签署及审查阶段，强制缔约属于外部法定义务提示；未在合同中重复第648条本身不构成重大合同缺失。"
            item.risk_level = "低"
            item.status = "法律提示"
            item.coverage_status = "法律提示"
            item.issue_type = "法律提示"
            item.reasoning_summary = reason
            item.risk_point_description = reason
            item.legal_consequence_if_missing = ""
            item.evidence_clauses = []
            item.evidence_location = ""
            item.suggested_clause_example = ""
            item.judge_source = "utility_supply_applicability"
            continue
        if _apply_parameters(item, clauses, full_text):
            continue
        if _set_adverse_if_found(item, clauses):
            continue
        if item.node_id in PROFILES:
            _set_atomic_item(item, PROFILES[item.node_id], clauses)
            continue
        if item.node_id in ATTACHMENT_PROFILES:
            _apply_attachment_rule(item, clauses, full_text)
            continue
    return items


def _item_value(item, key: str, default=None):
    if isinstance(item, dict):
        return item.get(key, default)
    return getattr(item, key, default)


def _element_statuses(item) -> Dict[str, str]:
    rows = _item_value(item, "coverage_elements", []) or []
    return {
        str(row.get("element_id") or ""): str(row.get("status") or "").upper()
        for row in rows
        if isinstance(row, dict) and row.get("element_id")
    }


def consistency_gate(items, clauses=None) -> Dict[str, object]:
    """Utility-supply consistency gate for shared evidence/coverage drift.

    The gate is intentionally narrow and domain-generic: it checks that utility
    rules do not treat the same interruption disclaimer as both ADVERSE and
    PASS, and that positive atomic evidence already found in one utility rule is
    not ignored by a sibling rule that reviews the same factual family.
    """

    by_node = {_item_value(item, "node_id", ""): item for item in items}
    failures: List[Dict[str, object]] = []

    for node, item in by_node.items():
        trace = _item_value(item, "decision_trace", {}) or {}
        validation = trace.get("parameter_validation", {})
        if _item_value(item, "coverage_status") == "通过" and (
            validation.get("unresolved") or validation.get("problems")
            or any(c["result"] != "COVERED" for c in validation.get("checks", []))
        ):
            failures.append(dict(requirement="PARAMETER_COMPLIANCE", current_status="FAIL",
                                 root_cause="参数或适用条件尚未通过校验，不能输出PASS。", source_rules=[node]))
        if node in ATTACHMENT_PROFILES and _item_value(item, "coverage_status") == "通过" and clauses:
            text = "\n".join(_item_value(c, "text", "") for c in clauses)
            if not _has_attachment_entity(text, ATTACHMENT_PROFILES[node][0]):
                failures.append(dict(requirement="ATTACHMENT_EXISTENCE", current_status="FAIL",
                                     root_cause="附件通过结果缺乏附件实体证据。", source_rules=[node]))

    interruption_nodes = ["planned_interruption_notice", "temporary_interruption_notice"]
    interruption_risk = [
        node for node in interruption_nodes
        if _item_value(by_node.get(node, {}), "coverage_status") == "风险条款"
    ]
    no_notice = by_node.get("no_notice_interruption_clause")
    if interruption_risk and no_notice and _item_value(no_notice, "coverage_status") == "通过":
        failures.append({
            "requirement": "UTILITY_INTERRUPTION_CONSISTENCY",
            "failure_stage": "Utility Supply Cross-rule Consistency",
            "root_cause": "同一中断供应通知/免责事实已被相邻规则识别为风险，但免除通知义务规则仍判通过。",
            "current_status": "FAIL",
            "source_rules": interruption_risk + ["no_notice_interruption_clause"],
        })

    illegal = by_node.get("illegal_use_prohibition")
    safe = by_node.get("safe_economical_planned_use")
    illegal_elements = _element_statuses(illegal) if illegal else {}
    has_safety_evidence = any(
        illegal_elements.get(key) == "COVERED"
        for key in ("unauthorized_facility_change", "grid_safety_harm")
    )
    if has_safety_evidence and safe and _item_value(safe, "coverage_status") == "缺失":
        failures.append({
            "requirement": "UTILITY_SAFE_USE_SHARED_EVIDENCE",
            "failure_stage": "Utility Supply Cross-rule Consistency",
            "root_cause": "第九条等安全使用证据已被违规使用规则消费，但安全节约计划使用规则仍判完全缺失。",
            "current_status": "FAIL",
            "source_rules": ["illegal_use_prohibition", "safe_economical_planned_use"],
        })

    billing = by_node.get("billing_standard_method")
    if billing:
        billing_elements = _element_statuses(billing)
        full_text = "\n".join(_item_value(c, "text", "") if isinstance(c, dict) else getattr(c, "text", "") for c in (clauses or []))
        metering_pattern = dict((key, pattern) for key, _, pattern in PROFILES["billing_standard_method"]).get("metering_basis", "")
        if (
            billing_elements.get("metering_basis") == "MISSING"
            and metering_pattern
            and re.search(metering_pattern, full_text)
        ):
            failures.append({
                "requirement": "UTILITY_BILLING_METERING_FALSE_ABSENCE",
                "failure_stage": "Utility Supply Cross-rule Consistency",
                "root_cause": "全文存在计量结果作为结算/计费依据的正向事实，但 US-10-02 仍将该 element 判为缺失。",
                "current_status": "FAIL",
                "source_rules": ["billing_standard_method"],
            })

    return {
        "status": "REPORT_READY" if not failures else "BLOCKED",
        "failures": failures,
        "gate_results": {"UTILITY_SUPPLY_CONSISTENCY_GATE": "PASS" if not failures else "FAIL"},
        "failure_count": len(failures),
    }
