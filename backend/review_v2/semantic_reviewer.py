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


def _has_early_surrender_notice(text: str) -> bool:
    source = text or ""
    has_early = any(term in source for term in ("提前退租", "提前解除", "提前收回"))
    has_notice = any(term in source for term in ("书面通知", "提前通知", "通知"))
    return has_early and has_notice


def _has_termination_notice_delivery(text: str) -> bool:
    source = text or ""
    has_termination = any(term in source for term in ("解除通知", "解除合同", "解除本合同", "单方解除"))
    has_delivery = any(term in source for term in ("送达", "送达地址", "通知到达", "到达对方", "生效", "电子邮件", "微信", "短信", "通讯地址"))
    return has_termination and has_delivery


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


def _has_sale_delivery_transport_framework(text: str) -> bool:
    return any(
        term in (text or "")
        for term in (
            "运输方式",
            "负责运输",
            "由甲方负责运输",
            "由乙方负责运输",
            "承运人",
            "送货",
            "提货",
            "自提",
            "物流",
            "运输",
        )
    )


def _has_sale_delivery_signoff_terms(text: str) -> bool:
    return any(
        term in (text or "")
        for term in (
            "签收",
            "收货确认",
            "送货单",
            "签收单",
            "物流回执",
            "回单",
            "授权收货人",
            "收货人签字",
            "交接单",
        )
    )


def _has_sale_delivery_complete_terms(text: str) -> bool:
    return _has_sale_delivery_transport_framework(text) and _has_sale_delivery_signoff_terms(text)


def _has_gift_gratuitous_declaration(text: str) -> bool:
    source = compact(text or "")
    if any(term in source for term in ("无偿赠与", "无偿给与", "免费赠与", "不收取对价", "无需支付任何对价", "无需向甲方支付任何对价")):
        return True
    return bool(re.search(r"(无需|不需|不用|不必|无须).{0,10}(支付|给付|承担).{0,10}(对价|价款)", source))


def _has_gift_paid_consideration_risk(text: str) -> bool:
    if _has_gift_gratuitous_declaration(text):
        return False
    source = compact(text or "")
    return any(
        has_unnegated_word(source, term, window=8)
        for term in ("价款", "收益", "固定收益", "投资收益", "回购", "还款", "对价")
    )


def _has_any(text: str, terms: Sequence[str]) -> bool:
    return any(term in (text or "") for term in terms)


def _has_safekeeping_fee_nature(text: str) -> bool:
    source = text or ""
    return _has_any(source, ("有偿保管", "无偿保管", "免费保管", "保管费", "费用")) and _has_any(
        source, ("有偿", "无偿", "免费", "金额", "支付", "每月", "每日", "元")
    )


def _has_safekeeping_paid_fault_standard(text: str) -> bool:
    source = text or ""
    return _has_any(source, ("有偿保管", "保管费")) and _has_any(
        source, ("一般过失", "妥善保管", "注意义务", "保管不善", "赔偿责任")
    )


def _has_safekeeping_unpaid_fault_standard(text: str) -> bool:
    source = text or ""
    return _has_any(source, ("无偿保管", "免费保管")) and _has_any(source, ("故意", "重大过失", "不承担", "赔偿责任"))


def _has_safekeeping_transfer_terms(text: str) -> bool:
    source = text or ""
    return _has_any(source, ("转保管", "转交第三人", "第三人保管", "委托第三人")) and _has_any(
        source, ("书面同意", "不得", "责任", "赔偿", "追偿")
    )


def _has_safekeeping_consumptive_terms(text: str) -> bool:
    source = text or ""
    return _has_any(source, ("消费保管", "货币保管", "可替代物", "同种类", "同品质", "混同保管"))


def _has_work_subcontract_terms(text: str) -> bool:
    source = text or ""
    return _has_any(source, ("转包", "分包", "外协", "第三人完成", "交由第三人", "委托第三人")) and _has_any(
        source, ("书面同意", "不得", "责任", "成果负责", "解除")
    )


def _has_work_sample_terms(text: str) -> bool:
    source = text or ""
    return _has_any(source, ("样品", "样板", "封样", "凭样", "样品确认", "按样制作")) and _has_any(
        source, ("封存", "确认", "附件", "照片", "验收")
    )


def _has_work_material_inspection_notice(text: str) -> bool:
    source = text or ""
    return _has_any(source, ("材料", "来料", "定作人提供")) and _has_any(source, ("检验", "检查", "验收")) and _has_any(
        source, ("通知", "书面通知", "更换", "补齐", "补救")
    )


def _has_work_assistance_urge_terms(text: str) -> bool:
    source = text or ""
    return _has_any(source, ("协助", "提供图纸", "提供资料", "确认方案", "提供场地")) and _has_any(
        source, ("催告", "合理期限", "逾期")
    ) and _has_any(source, ("顺延", "工期", "费用增加", "解除"))


def _has_work_arbitrary_termination_terms(text: str) -> bool:
    source = text or ""
    return _has_any(source, ("任意解除", "随时解除", "取消订单", "终止合同", "解除合同")) and _has_any(
        source, ("完成前", "工作完成前", "赔偿", "损失", "已投入", "结算")
    )


def _has_work_termination_notice_settlement(text: str) -> bool:
    source = text or ""
    return _has_any(source, ("解除通知", "解除合同", "终止合同")) and _has_any(
        source, ("通知", "送达", "收到通知")
    ) and _has_any(source, ("停止工作", "清点", "交接", "结算", "材料返还"))


def _has_agency_sub_entrustment_terms(text: str) -> bool:
    source = text or ""
    return _has_any(source, ("转委托", "第三人处理", "委托别人", "另行委托", "委托第三人")) and _has_any(
        source, ("同意", "追认", "紧急", "通知", "责任", "选任", "指示")
    )


def _has_agency_conflict_terms(text: str) -> bool:
    source = text or ""
    return _has_any(source, ("自己代理", "双方代理", "与自己交易", "同时代理双方", "利益冲突")) and _has_any(
        source, ("同意", "追认", "披露", "公平", "不得")
    )


def _has_agency_undisclosed_terms(text: str) -> bool:
    source = text or ""
    return _has_any(source, ("以自己名义", "隐名委托", "第三人不知道", "披露第三人", "披露委托人", "介入权", "选择权")) and _has_any(
        source, ("披露", "介入", "选择", "抗辩", "不得变更", "第三人")
    )


def _has_agency_arbitrary_termination_terms(text: str) -> bool:
    source = text or ""
    return _has_any(source, ("任意解除", "随时解除", "单方解除", "终止委托", "解除合同")) and _has_any(
        source, ("通知", "交接", "结算", "赔偿", "损失", "直接损失", "可得利益")
    )


_STRICT_EVIDENCE_NODE_IDS = {
    "safekeeping_fee_paid_or_unpaid",
    "safekeeping_paid_general_negligence",
    "safekeeping_unpaid_intent_gross",
    "safekeeping_no_transfer_to_third",
    "safekeeping_transfer_agreed_condition",
    "safekeeping_transfer_liability",
    "safekeeping_consumptive_type",
    "safekeeping_consumptive_return_rule",
    "safekeeping_currency_interest",
    "safekeeping_consumptive_mixing",
    "work_main_subcontract_consent",
    "work_auxiliary_subcontract_liability",
    "work_illegal_total_subcontract",
    "work_sample_attachment",
    "work_customer_material_inspection_notice",
    "work_assistance_urge_extension",
    "work_assistance_rescission",
    "work_customer_arbitrary_termination_before_completion",
    "work_arbitrary_termination_loss_scope",
    "work_arbitrary_termination_boundary",
    "work_termination_notice_settlement",
    "agency_sub_entrustment_consent",
    "agency_sub_entrustment_liability",
    "agency_emergency_sub_entrustment",
    "agency_self_agency_consent",
    "agency_both_side_agency_consent",
    "agency_conflict_unfair_transaction",
    "agency_undisclosed_principal_intervention",
    "agency_disclose_third_party",
    "agency_intervention_defense_continuation",
    "agency_third_party_choice_right",
    "agency_disclose_principal",
    "agency_choice_defense_continuation",
    "agency_arbitrary_termination",
    "agency_termination_compensation_scope",
    "agency_termination_handover",
}


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
    if checkpoint.node_id == "termination_notice":
        return _has_termination_notice_delivery(joined)
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
    if checkpoint.node_id == "sale_delivery_method":
        return _has_sale_delivery_complete_terms(joined)
    if checkpoint.node_id == "safekeeping_fee_paid_or_unpaid":
        return _has_safekeeping_fee_nature(joined)
    if checkpoint.node_id == "safekeeping_paid_general_negligence":
        return _has_safekeeping_paid_fault_standard(joined)
    if checkpoint.node_id == "safekeeping_unpaid_intent_gross":
        return _has_safekeeping_unpaid_fault_standard(joined)
    if checkpoint.node_id in (
        "safekeeping_no_transfer_to_third",
        "safekeeping_transfer_agreed_condition",
        "safekeeping_transfer_liability",
    ):
        return _has_safekeeping_transfer_terms(joined)
    if checkpoint.node_id in (
        "safekeeping_consumptive_type",
        "safekeeping_consumptive_return_rule",
        "safekeeping_currency_interest",
        "safekeeping_consumptive_mixing",
    ):
        return _has_safekeeping_consumptive_terms(joined)
    if checkpoint.node_id in (
        "work_main_subcontract_consent",
        "work_auxiliary_subcontract_liability",
        "work_illegal_total_subcontract",
    ):
        return _has_work_subcontract_terms(joined)
    if checkpoint.node_id == "work_sample_attachment":
        return _has_work_sample_terms(joined)
    if checkpoint.node_id == "work_customer_material_inspection_notice":
        return _has_work_material_inspection_notice(joined)
    if checkpoint.node_id in ("work_assistance_urge_extension", "work_assistance_rescission"):
        return _has_work_assistance_urge_terms(joined)
    if checkpoint.node_id in (
        "work_customer_arbitrary_termination_before_completion",
        "work_arbitrary_termination_loss_scope",
        "work_arbitrary_termination_boundary",
    ):
        return _has_work_arbitrary_termination_terms(joined)
    if checkpoint.node_id == "work_termination_notice_settlement":
        return _has_work_termination_notice_settlement(joined)
    if checkpoint.node_id in (
        "agency_sub_entrustment_consent",
        "agency_sub_entrustment_liability",
        "agency_emergency_sub_entrustment",
    ):
        return _has_agency_sub_entrustment_terms(joined)
    if checkpoint.node_id in (
        "agency_self_agency_consent",
        "agency_both_side_agency_consent",
        "agency_conflict_unfair_transaction",
    ):
        return _has_agency_conflict_terms(joined)
    if checkpoint.node_id in (
        "agency_undisclosed_principal_intervention",
        "agency_disclose_third_party",
        "agency_intervention_defense_continuation",
        "agency_third_party_choice_right",
        "agency_disclose_principal",
        "agency_choice_defense_continuation",
    ):
        return _has_agency_undisclosed_terms(joined)
    if checkpoint.node_id in (
        "agency_arbitrary_termination",
        "agency_termination_compensation_scope",
        "agency_termination_handover",
    ):
        return _has_agency_arbitrary_termination_terms(joined)
    return True


def evidence_substantively_matches(checkpoint: ReviewCheckpoint, clauses: Sequence[ParsedClause]) -> bool:
    """Return whether cited evidence matches the checkpoint's legal scenario.

    This is intentionally stricter than keyword recall. It prevents a clause with
    surface terms such as "通知", "物业费" or "合同终止" from being treated as
    evidence for a different legal requirement.
    """

    if not clauses:
        return False
    joined = "\n".join(clause.text for clause in clauses)
    if checkpoint.node_id == "limitation_and_notice":
        return _has_notice_delivery_terms(joined) and not all(_is_only_advance_notice(clause.text) for clause in clauses)
    if checkpoint.node_id == "third_party_defect":
        return _has_third_party_defect_terms(joined) and not all(_is_fee_only_clause(clause.text) for clause in clauses)
    if checkpoint.node_id == "expropriation_demolition":
        return _has_expropriation_terms(joined)
    if checkpoint.node_id == "third_party_tort":
        has_third_party = any(term in joined for term in ("第三方", "第三人", "邻居", "楼上", "路人", "物业原因"))
        has_tort_handling = any(term in joined for term in ("侵权", "保全证据", "协助追偿", "责任方", "不得当然归责"))
        return has_third_party and has_tort_handling
    if checkpoint.node_id in _STRICT_EVIDENCE_NODE_IDS:
        return _has_strict_pass_evidence(checkpoint, clauses)
    return True


def judge_checkpoint(checkpoint: ReviewCheckpoint, clauses: Sequence[ParsedClause]) -> ReviewJudgment:
    candidates, terms = recall_candidate_clauses(checkpoint, clauses)
    evidence = _public_evidence(candidates)
    evidence_location = _locations(candidates)

    if checkpoint.kind == "forbidden":
        if checkpoint.node_id == "gift_nature_confusing_consideration" and not _has_gift_paid_consideration_risk("\n".join(clause.text for clause in clauses)):
            return ReviewJudgment(
                coverage_status=COVERAGE_PASS,
                risk_level="低",
                status="未发现明显风险条款",
                risk_point_description=checkpoint.risk_point_missing,
                evidence_clauses=[],
                evidence_location="",
                reasoning_summary="合同已明确无偿赠与，且未发现未被排除的价款、收益、回购、还款或其他实质有偿对价安排。",
                matched_terms=[],
                issue_type=ISSUE_PASS,
            )
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
        if checkpoint.node_id == "indefinite_lease":
            return ReviewJudgment(
                coverage_status=COVERAGE_MISSING,
                risk_level=checkpoint.risk_level,
                status="缺失或不明确",
                risk_point_description=checkpoint.risk_point_missing,
                evidence_clauses=[],
                evidence_location="",
                reasoning_summary=(
                    "根据《民法典》第734条，租赁期满后双方未续签合同但继续履行租约的，原合同继续有效，"
                    "租赁期限转为不定期；出租人解除合同需提前合理期限通知。对简化版居住租赁合同而言，"
                    "该条款属于建议性补充条款，并非必须条款。"
                ),
                matched_terms=[],
                issue_type=ISSUE_MISSING,
            )
        return ReviewJudgment(
            coverage_status=COVERAGE_MISSING,
            risk_level=checkpoint.risk_level,
            status="缺失或不明确",
            risk_point_description=checkpoint.risk_point_missing,
            evidence_clauses=[],
            evidence_location="",
            reasoning_summary="未在正式合同条款中找到能覆盖该审查点的有效约定。",
            matched_terms=[],
            issue_type=ISSUE_MISSING,
        )

    joined_candidates = "\n".join(clause.text for clause in candidates)
    if checkpoint.node_id in _STRICT_EVIDENCE_NODE_IDS and not _has_strict_pass_evidence(checkpoint, candidates):
        return ReviewJudgment(
            coverage_status=COVERAGE_MISSING,
            risk_level=checkpoint.risk_level,
            status="缺失或不明确",
            risk_point_description=checkpoint.risk_point_missing,
            evidence_clauses=[],
            evidence_location="",
            reasoning_summary="召回条款与该审查点只有表面词语关联，未实质覆盖对应法律要求，因此不作为有效证据。",
            matched_terms=[],
            issue_type=ISSUE_MISSING,
        )

    if checkpoint.node_id == "termination_notice" and _has_early_surrender_notice(joined_candidates) and not _has_termination_notice_delivery(joined_candidates):
        return ReviewJudgment(
            coverage_status=COVERAGE_PARTIAL,
            risk_level=checkpoint.risk_level,
            status="部分覆盖，需补充细化",
            risk_point_description=f"合同已出现“{checkpoint.title}”相关条款，但提前退租通知不能替代解除通知送达制度。",
            evidence_clauses=evidence,
            evidence_location=evidence_location,
            reasoning_summary=(
                "合同约定了提前退租的书面通知，但未约定解除通知的送达方式、送达地址和生效时间。"
                "二者法律功能不同，前者启动解除程序，后者使解除行为生效。"
            ),
            matched_terms=terms,
            issue_type=ISSUE_TEMPLATE_BLANK if any(has_blank_value(clause.text) for clause in candidates) else ISSUE_CLAUSE_DEFECT,
        )

    blank_clauses = [clause for clause in candidates if has_blank_value(clause.text)]
    if blank_clauses:
        if checkpoint.node_id == "early_surrender":
            return ReviewJudgment(
                coverage_status=COVERAGE_PARTIAL,
                risk_level=checkpoint.risk_level,
                status="部分覆盖，需补充填写",
                risk_point_description=(
                    "合同已出现提前退租安排，但违约金比例或通知期限仍为空白，签约前必须填写具体比例；"
                    "同时应明确违约金以实际损失为基础，否则存在被调减的风险。"
                ),
                evidence_clauses=evidence,
                evidence_location=evidence_location,
                reasoning_summary=(
                    "提前退租条款已被召回，但通知期限或违约金比例存在模板空白；违约金还应与实际损失、"
                    "合理空置损失或未结费用挂钩，避免固定高额约定被调减。"
                ),
                matched_terms=terms,
                issue_type=ISSUE_TEMPLATE_BLANK,
            )
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

    if checkpoint.node_id == "sale_delivery_method" and _has_sale_delivery_transport_framework(joined_candidates) and not _has_sale_delivery_complete_terms(joined_candidates):
        return ReviewJudgment(
            coverage_status=COVERAGE_PARTIAL,
            risk_level=checkpoint.risk_level,
            status="部分覆盖，需补充填写",
            risk_point_description=f"合同已出现“{checkpoint.title}”相关安排，但仅有运输方式框架，签收手续、收货确认或有效交付凭证仍不完整。",
            evidence_clauses=evidence,
            evidence_location=evidence_location,
            reasoning_summary="合同已约定运输方式，但未写明签收手续、授权收货人或送货单、签收单、物流回执等交付凭证，属于模板框架已写但关键手续未补全。",
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
