"""Rule-based semantic review for contract review v2.

This module intentionally exposes a stable judge_checkpoint() interface so a
model-backed reviewer can be introduced later without changing API consumers.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import List, Sequence

from review_v2.clause_parser import ParsedClause, formal_evidence_clauses
from review_v2.house_lease_checklist import ReviewCheckpoint


COVERAGE_PASS = "通过"
COVERAGE_PARTIAL = "部分覆盖"
COVERAGE_MISSING = "缺失"
COVERAGE_RISKY = "风险条款"
ISSUE_PASS = "通过"
ISSUE_TEMPLATE_BLANK = "模板空白"
ISSUE_CLAUSE_DEFECT = "条款缺陷"
ISSUE_MISSING = "完全缺失"
ISSUE_RISKY = "风险条款"

NEGATION_WORDS = ("无", "没有", "未", "不包含", "不涉及", "并非", "不是")
GENERIC_TITLE_WORDS = (
    "条款",
    "处理",
    "规则",
    "机制",
    "责任",
    "合同",
    "房屋",
    "租赁",
    "出租人",
    "承租人",
    "风险",
)

BLANK_PATTERNS = (
    re.compile(r"[_＿]{2,}"),
    re.compile(r"□\s*是\s*□\s*否"),
    re.compile(r"□[^。\n；;]{0,16}□"),
    re.compile(r"(人民币|押金|租金|金额|月租金)[^。\n]{0,12}[ 　]{2,}(元|日|天|月|年)"),
    re.compile(r"提前[ 　]{2,}(日|天|个工作日|工作日)"),
    re.compile(r"按照[ 　]{2,}的标准"),
    re.compile(r"(违约金|赔偿金|扣款)[^。\n；;]{0,16}[ 　]{2,}(元|%|％|的标准)"),
    re.compile(r"[ 　]{2,}年[ 　]{1,}月[ 　]{1,}日"),
    re.compile(r"(期限|时间|日期|天数|金额|标准)[：:][ 　]*(。|；|;|$)"),
)


@dataclass(frozen=True)
class ReviewJudgment:
    coverage_status: str
    risk_level: str
    status: str
    risk_point_description: str
    evidence_clauses: List[dict]
    evidence_location: str
    reasoning_summary: str
    matched_terms: List[str]
    issue_type: str
    judge_source: str = "rule_fallback"
    llm_confidence: str = ""
    llm_raw_reason: str = ""
    fallback_reason: str = ""


def compact(text: str) -> str:
    return re.sub(r"\s+", "", text or "")


def has_unnegated_word(text: str, word: str, window: int = 5) -> bool:
    for match in re.finditer(re.escape(word), text):
        prefix = text[max(0, match.start() - window):match.start()]
        if not any(negation in prefix for negation in NEGATION_WORDS):
            return True
    return False


def matched_terms(text: str, terms: Sequence[str]) -> List[str]:
    source = compact(text)
    return [term for term in terms if term and term in source and has_unnegated_word(source, term)]


def has_blank_value(text: str) -> bool:
    return any(pattern.search(text or "") for pattern in BLANK_PATTERNS)


def has_specific_deposit_return_deadline(text: str) -> bool:
    deadline_pattern = re.compile(
        r"(?:\d+|[一二三四五六七八九十]+)\s*(?:个)?\s*(?:工作日|日|天|小时)\s*(?:内|以内|前)?"
    )
    refund_terms = ("退还", "返还", "退回")
    normalized = text or ""
    sentence_parts = re.split(r"[。；;！!\n]", normalized)
    for part in sentence_parts:
        if "押金" not in part or not any(term in part for term in refund_terms):
            continue
        if deadline_pattern.search(part):
            return True
    compacted = compact(normalized)
    for refund_term in refund_terms:
        for match in re.finditer(refund_term, compacted):
            window = compacted[max(0, match.start() - 28): match.end() + 28]
            if "押金" in window and deadline_pattern.search(window):
                return True
    return False


def _has_concrete_advance_notice(text: str) -> bool:
    return bool(
        re.search(r"提前\s*(?:\d+|[一二三四五六七八九十]+)\s*(?:个)?\s*(?:工作日|日|天|月)\s*(?:书面)?通知", text or "")
    )


def _has_loss_based_adjustment(text: str) -> bool:
    source = text or ""
    has_loss_basis = any(term in source for term in ("实际损失", "实际发生", "合理损失", "合理费用", "造成损失"))
    has_adjustment = any(term in source for term in ("过高", "调减", "调整", "协商调整", "法院调整"))
    return has_loss_basis and has_adjustment


def _title_terms(title: str) -> List[str]:
    chunks = re.split(r"[、和与及/（）()：:，,。\s]+", title or "")
    terms: List[str] = []
    for chunk in chunks:
        chunk = chunk.strip()
        if len(chunk) >= 2 and chunk not in GENERIC_TITLE_WORDS:
            terms.append(chunk)
    return terms


def _has_notice_delivery_terms(text: str) -> bool:
    return any(
        term in (text or "")
        for term in (
            "送达",
            "通讯地址",
            "通信地址",
            "联系地址",
            "电子邮件",
            "邮箱",
            "微信",
            "短信",
            "催告",
            "留痕",
            "联系方式",
            "联系电话",
            "地址变更",
            "变更联系方式",
        )
    )


def _is_only_advance_notice(text: str) -> bool:
    source = text or ""
    return "提前" in source and "通知" in source and not _has_notice_delivery_terms(source)


def _has_expropriation_terms(text: str) -> bool:
    return any(term in (text or "") for term in ("征收", "拆迁", "腾退", "强制处置"))


def _has_third_party_defect_terms(text: str) -> bool:
    source = text or ""
    has_actor = any(term in source for term in ("第三方", "第三人", "邻居", "楼上", "物业原因", "公共管线", "楼上住户"))
    has_effect = any(term in source for term in ("漏水", "停水", "噪声", "影响使用", "损坏", "维修", "报修", "追偿", "协助", "保全证据"))
    return has_actor and has_effect


def _is_fee_only_clause(text: str) -> bool:
    source = text or ""
    has_fee = any(term in source for term in ("水费", "电费", "燃气费", "物业费", "网络费", "水电"))
    has_payment = any(term in source for term in ("承担", "支付", "缴纳", "结清"))
    has_third_party_context = any(term in source for term in ("第三方", "第三人", "邻居", "楼上", "侵权", "追偿", "保全证据", "影响使用", "漏水", "噪声"))
    return has_fee and has_payment and not has_third_party_context


def _has_term_expiry_settlement_terms(text: str) -> bool:
    source = text or ""
    has_deposit_settlement = "押金" in source and any(term in source for term in ("合同终止", "租期届满", "退租", "结清费用", "结算", "返还"))
    has_handover = any(term in source for term in ("交还房屋", "退还房屋", "查验", "结算清单", "交接"))
    return has_deposit_settlement or has_handover


def _has_complete_term_expiry_settlement(text: str) -> bool:
    source = text or ""
    has_expiry = any(term in source for term in ("租期届满", "合同终止", "退租", "合同解除"))
    has_handover = any(term in source for term in ("交还房屋", "退还房屋", "查验", "交接"))
    has_settlement = any(term in source for term in ("结算清单", "结清费用", "押金", "租金", "费用"))
    return has_expiry and has_handover and has_settlement


def recall_candidate_clauses(
    checkpoint: ReviewCheckpoint,
    clauses: Sequence[ParsedClause],
    *,
    max_candidates: int = 4,
) -> tuple[List[ParsedClause], List[str]]:
    evidence_pool = formal_evidence_clauses(list(clauses))
    scored: List[tuple[int, int, ParsedClause, List[str]]] = []
    all_matched_terms: List[str] = []
    title_terms = _title_terms(checkpoint.title)

    for index, clause in enumerate(evidence_pool):
        terms = matched_terms(clause.text, checkpoint.terms)
        title_hits = matched_terms(clause.text, title_terms)
        score = len(terms) * 4 + len(title_hits) * 2
        if checkpoint.node_id in ("deposit_return_deadline", "deposit_amount", "deposit_offset_order") and "押金" in clause.text:
            score += 2
        if checkpoint.node_id == "deposit_offset_order":
            if "押金" in clause.text:
                score += 4
            elif not any(term in clause.text for term in ("抵扣", "扣除", "扣款")):
                score = 0
        if checkpoint.node_id in ("use_restriction",) and "用途" in clause.text:
            score += 2
        if checkpoint.node_id == "third_party_tort":
            has_third_party = any(term in clause.text for term in ("第三方", "第三人", "邻居", "楼上", "路人"))
            has_property_cause = "物业" in clause.text and any(term in clause.text for term in ("原因", "造成", "损坏", "侵权", "责任"))
            if not (has_third_party or has_property_cause):
                score = 0
        if checkpoint.node_id == "limitation_and_notice":
            if not _has_notice_delivery_terms(clause.text) or _is_only_advance_notice(clause.text):
                score = 0
        if checkpoint.node_id == "third_party_defect":
            if _is_fee_only_clause(clause.text) or not _has_third_party_defect_terms(clause.text):
                score = 0
        if checkpoint.node_id == "expropriation_demolition":
            if not _has_expropriation_terms(clause.text):
                score = 0
        if checkpoint.node_id == "term_expiry_settlement":
            if _has_term_expiry_settlement_terms(clause.text):
                score += 6
            else:
                score = 0
        if checkpoint.node_id == "unauthorized_sublease" and not any(
            term in clause.text for term in ("转租", "转借", "交由他人", "他人长期使用", "次承租")
        ):
            score = 0
        if checkpoint.node_id in ("pre_delivery_defect", "handover_evidence") and "交割单" in clause.text:
            score += 2
        if checkpoint.node_id in ("tenant_fault_damage", "damage_definition") and ("毁损" in clause.text or "赔偿" in clause.text):
            score += 2
        if score:
            all_matched_terms.extend(terms or title_hits)
            scored.append((score, index, clause, terms or title_hits))

    scored.sort(key=lambda item: (-item[0], item[1]))
    candidates = [item[2] for item in scored[:max_candidates]]
    unique_terms = list(dict.fromkeys(all_matched_terms))
    return candidates, unique_terms


def _public_evidence(clauses: Sequence[ParsedClause]) -> List[dict]:
    result = []
    for clause in clauses:
        text = clause.text.strip()
        if len(text) > 420:
            text = text[:420].rstrip() + "..."
        result.append(
            {
                "clause_id": clause.clause_id,
                "location": clause.location,
                "title": clause.title,
                "text": text,
                "section_type": clause.section_type,
            }
        )
    return result


def _locations(clauses: Sequence[ParsedClause]) -> str:
    return "；".join(dict.fromkeys(clause.location for clause in clauses if clause.location))


def _has_strict_pass_evidence(checkpoint: ReviewCheckpoint, clauses: Sequence[ParsedClause]) -> bool:
    joined = "\n".join(clause.text for clause in clauses)
    if checkpoint.node_id == "proper_party":
        has_party_roles = any(term in joined for term in ("出租人", "甲方", "承租人", "乙方"))
        has_identity_details = any(
            term in joined
            for term in ("身份证", "证件号", "统一社会信用代码", "营业执照", "住所", "住址", "联系电话", "联系方式", "邮箱")
        )
        return has_party_roles and has_identity_details
    if checkpoint.node_id == "deposit_return_deadline":
        has_deposit_return = "押金" in joined and any(term in joined for term in ("退还", "返还", "退回"))
        has_specific_deadline = has_specific_deposit_return_deadline(joined)
        return has_deposit_return and has_specific_deadline
    if checkpoint.node_id == "utilities_fees":
        has_specific_fee = any(term in joined for term in ("水费", "电费", "燃气费", "物业费", "网络费", "水电", "水、电", "水、电、燃气"))
        has_settlement = any(term in joined for term in ("承担", "结清", "结算", "缴纳"))
        return has_specific_fee and has_settlement
    if checkpoint.node_id == "indefinite_lease":
        has_holdover = any(term in joined for term in ("继续居住", "继续使用", "继续承租", "期满后继续"))
        has_lessor_acceptance = any(term in joined for term in ("继续收租", "继续收取租金", "未提出异议", "没有提出异议"))
        has_indefinite = any(term in joined for term in ("不定期租赁", "不定期", "未续签", "未签订新的租赁合同"))
        has_notice = any(term in joined for term in ("提前", "通知", "三十日", "30日", "一个月"))
        return has_holdover and has_lessor_acceptance and has_indefinite and has_notice
    if checkpoint.node_id == "unauthorized_sublease":
        has_sublease = any(term in joined for term in ("转租", "转借", "交由他人", "他人长期使用", "次承租"))
        has_consequence = any(term in joined for term in ("书面同意", "未经同意", "不得", "解除", "纠正"))
        return has_sublease and has_consequence
    if checkpoint.node_id == "expropriation_demolition":
        return _has_expropriation_terms(joined)
    if checkpoint.node_id == "limitation_and_notice":
        return _has_notice_delivery_terms(joined)
    if checkpoint.node_id == "third_party_defect":
        has_handling = any(term in joined for term in ("协助维修", "报修", "追偿", "保全证据", "租金调整", "减租", "责任方"))
        return _has_third_party_defect_terms(joined) and has_handling
    if checkpoint.node_id == "term_expiry_settlement":
        return _has_complete_term_expiry_settlement(joined)
    if checkpoint.node_id == "maintenance_duty":
        has_lessor_repair = "出租人" in joined and any(term in joined for term in ("维修", "修复", "负责", "承担"))
        has_scope = any(term in joined for term in ("自然老化", "非承租人原因", "主体", "管线", "附属设施", "正常使用"))
        return has_lessor_repair and has_scope
    if checkpoint.node_id == "deposit_offset_order":
        has_order = any(term in joined for term in ("顺序", "先", "依次", "按"))
        has_categories = sum(1 for term in ("租金", "水电", "费用", "维修费", "损坏", "其他款项") if term in joined) >= 2
        return "押金" in joined and has_order and has_categories
    if checkpoint.node_id == "third_party_tort":
        has_third_party = any(term in joined for term in ("第三方", "第三人", "邻居", "楼上", "路人", "物业原因"))
        has_tort_handling = any(term in joined for term in ("侵权", "保全证据", "协助追偿", "责任方", "不得当然归责"))
        return has_third_party and has_tort_handling
    if checkpoint.node_id == "early_surrender":
        has_early_surrender = any(term in joined for term in ("提前退租", "提前解除", "提前收回"))
        has_notice = _has_concrete_advance_notice(joined)
        has_settlement_or_loss_basis = any(term in joined for term in ("实际使用", "实际损失", "合理空置", "结算", "未结费用"))
        return has_early_surrender and has_notice and has_settlement_or_loss_basis
    if checkpoint.node_id == "excessive_deduction":
        return _has_loss_based_adjustment(joined)
    return True


def judge_checkpoint(checkpoint: ReviewCheckpoint, clauses: Sequence[ParsedClause]) -> ReviewJudgment:
    candidates, terms = recall_candidate_clauses(checkpoint, clauses)
    evidence = _public_evidence(candidates)
    evidence_location = _locations(candidates)

    if checkpoint.kind == "forbidden":
        if candidates:
            return ReviewJudgment(
                coverage_status=COVERAGE_RISKY,
                risk_level=checkpoint.risk_level,
                status="发现风险条款",
                risk_point_description=checkpoint.risk_point_present,
                evidence_clauses=evidence,
                evidence_location=evidence_location,
                reasoning_summary="正式合同条款中出现了该审查点列明的明显不利或过宽表述，需要人工复核并修改。",
                matched_terms=terms,
                issue_type=ISSUE_RISKY,
            )
        return ReviewJudgment(
            coverage_status=COVERAGE_PASS,
            risk_level="低",
            status="未发现明显风险条款",
            risk_point_description=checkpoint.risk_point_missing,
            evidence_clauses=[],
            evidence_location="",
            reasoning_summary="正式合同条款和附件中未召回该类明显风险表述。",
            matched_terms=[],
            issue_type=ISSUE_PASS,
        )

    if not candidates:
        return ReviewJudgment(
            coverage_status=COVERAGE_MISSING,
            risk_level=checkpoint.risk_level,
            status="缺失或不明确",
            risk_point_description=checkpoint.risk_point_missing,
            evidence_clauses=[],
            evidence_location="",
            reasoning_summary="未在正式合同条款或附件中找到能覆盖该审查点的有效约定。",
            matched_terms=[],
            issue_type=ISSUE_MISSING,
        )

    blank_clauses = [clause for clause in candidates if has_blank_value(clause.text)]
    if blank_clauses:
        return ReviewJudgment(
            coverage_status=COVERAGE_PARTIAL,
            risk_level=checkpoint.risk_level,
            status="部分覆盖，需补充填写",
            risk_point_description=f"合同已出现“{checkpoint.title}”相关条款，但存在空白项、未勾选选项或关键数值未填写，签署前需要补全。",
            evidence_clauses=evidence,
            evidence_location=evidence_location,
            reasoning_summary="召回到相关正式条款，但条款中仍有空白或未选择内容，不能视为完整覆盖。",
            matched_terms=terms,
            issue_type=ISSUE_TEMPLATE_BLANK,
        )

    if not _has_strict_pass_evidence(checkpoint, candidates):
        return ReviewJudgment(
            coverage_status=COVERAGE_PARTIAL,
            risk_level=checkpoint.risk_level,
            status="部分覆盖，需补充细化",
            risk_point_description=f"合同已出现“{checkpoint.title}”相关条款，但表述过于概括，尚未完整覆盖该审查点。",
            evidence_clauses=evidence,
            evidence_location=evidence_location,
            reasoning_summary="召回条款只有一般性表述，缺少该审查点要求的关键主体信息、具体期限或费用类别，不能视为完整通过。",
            matched_terms=terms,
            issue_type=ISSUE_CLAUSE_DEFECT,
        )

    return ReviewJudgment(
        coverage_status=COVERAGE_PASS,
        risk_level="低",
        status="已覆盖",
        risk_point_description=checkpoint.risk_point_present,
        evidence_clauses=evidence,
        evidence_location=evidence_location,
        reasoning_summary="正式合同条款或附件中已召回能够覆盖该审查点的实质约定，未发现明显空白项。",
        matched_terms=terms,
        issue_type=ISSUE_PASS,
    )
