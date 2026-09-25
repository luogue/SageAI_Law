"""Construction rule semantics, independent of document names and examples."""
from __future__ import annotations

import re
from review_v2.adverse_evidence import direct_evidence

ADVERSE_PREDICATES = {
    "affiliation_qualification_lending": (r"挂靠", r"(?:借用|出借)资质"),
    "tender_illegal_invalid": (r"规避招标|串通投标|虚假招标|中标无效", r"(?:必须|应当)招标.{0,16}(?:未|不)招标"),
    "prohibit_total_subcontract": (r"转包|整体转让施工",),
    "no_re_subcontract": (r"再分包|二次分包|层层分包",),
    "black_white_contract_check": (
        r"(?:签订|签署|订立|另行|补充协议).{0,60}?(?P<act>(?:背离|相背离|不一致).{0,40}(?:实质|中标|合同))",
        r"(?:签订|签署|订立|另行|补充协议).{0,60}(?:实质|中标|合同).{0,40}?(?P<act>背离|不一致)",
        r"(?:以|按).{0,20}(?:另行协议|补充协议).{0,20}(?:取代|替代|结算).{0,20}中标合同",
        r"(?:签订|采用|订立).{0,12}(?:黑白合同|阴阳合同)",
    ),
    "priority_no_waiver_worker_interest": (
        r"放弃.{0,16}优先(?:受偿)?权", r"(?:不得|不应|不能|无权|禁止)主张.{0,16}优先(?:受偿)?权",
        r"优先受偿权.{0,12}(?:予以放弃|不予行使|不再行使)",
    ),
}

LEGAL_NODES = {
    "invalid_contract_price_compensation", "priority_payment_right", "priority_claim_18_months",
    "priority_scope_quality_condition", "direct_sue_employer_limit", "subrogation_claim",
    "planning_obtained_before_suit",
}
EXTERNAL_NODES = {"contractor_qualification_match", "mandatory_tender_review", "planning_permit_obtained",
                  "actual_constructor_identification", "affiliation_qualification_lending", "tender_illegal_invalid"}


def nature_evidence(clauses):
    profiles = (
        ("EPC设计-采购-施工总承包", r"设计[\s—–－-]*采购[\s—–－-]*施工.{0,20}总承包|EPC.{0,12}(?:总承包|合同)"),
        ("建设工程施工劳务分包合同", r"(?:建设工程|工程|施工)(?:施工)?劳务分包合同|建筑劳务分包合同"),
        ("建设工程总承包", r"(?:工程总承包|总承包合同)"),
        ("建设工程施工合同", r"(?:建设工程施工合同|工程施工合同|施工合同)"),
        ("建设工程设计合同", r"(?:工程设计合同|建设工程设计)"),
        ("建设工程勘察合同", r"(?:工程勘察合同|建设工程勘察)"),
    )
    for name, pattern in profiles:
        positive, _ = direct_evidence(clauses, (pattern,), require_assertion=False)
        # A template citation is not a statement about this contract's nature.
        positive = [row for row in positive if not re.search(r"示范文本|编制|借鉴|参考", row["text"])]
        if positive:
            return name, [{**r, 'nature_pattern': pattern} for r in positive[:3]]
    return "", []


EMPLOYER_ELEMENTS = {
    "site": r"施工场地|施工现场|现场条件|现场移交",
    "funds": r"资金|工程款|合同价款|支付担保|支付保证",
    "documents": r"图纸|技术资料|基础资料|基础数据|现场障碍资料",
    "materials": r"(?:材料|设备)(?!运行条件|资料|清单|说明)|工程物资|甲供(?:材料|设备)",
}


def employer_coverage(clauses):
    covered = {}
    for element, pattern in EMPLOYER_ELEMENTS.items():
        rows, _ = direct_evidence(clauses, (
            rf"(?:发包人|甲方)(?:(?!承包人|乙方|，|,).){{0,40}}(?:应|须|负责|承诺)(?:(?!承包人|乙方).){{0,50}}(?:提供|移交|交付|支付|提交)(?:(?!承包人|乙方).){{0,40}}(?:{pattern})",
            rf"(?:发包人|甲方)(?:应|须)?(?:提供|移交|交付|支付)(?!的).{{0,16}}(?:{pattern})",
            rf"(?:由)?(?:发包人|甲方)(?:提供|供应|负责采购)的(?:{pattern})(?:为|包括|包含|如下)[：:]?[^，。；]{{2,}}",
        ))
        rows = [r for r in rows if not re.search(r"(?:如|若|如果)(?:由)?发包人.{0,12}提供", r["text"])]
        if rows:
            covered[element] = rows[:3]
    return covered


def evidence_failures(items):
    failures = []
    for item in items:
        if item.node_id not in ADVERSE_PREDICATES or item.coverage_status != "风险条款":
            continue
        from types import SimpleNamespace
        rows = item.evidence_clauses or []
        clauses = [SimpleNamespace(text=r.get("text", ""), clause_id=r.get("clause_id", ""),
                   location=r.get("location", ""), title=r.get("title", ""),
                   section_type=r.get("section_type", "正式合同条款"), block_type=r.get("block_type", "OPERATIVE_CLAUSE")) for r in rows]
        positive, _ = direct_evidence(clauses, ADVERSE_PREDICATES[item.node_id])
        source_rows = (item.decision_trace or {}).get("direct_adverse_evidence", {}).get("positive", [])
        source_bound = all(any(r.get("clause_id") == s.get("clause_id") and
                               re.sub(r"\s+", "", r.get("text", "")) == re.sub(r"\s+", "", s.get("text", ""))
                               for s in source_rows) for r in rows)
        if not rows or not source_bound or len({r["clause_id"] for r in positive}) != len({r.get("clause_id") for r in rows}):
            failures.append({"requirement": "DIRECT_AFFIRMATIVE_RISK_EVIDENCE", "failure_stage": "Final Evidence Projection",
                             "root_cause": f"{item.item_id}: 风险条款缺少语义一致的正向直接证据。", "current_status": "FAIL"})
    return failures
