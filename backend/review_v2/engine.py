"""独立的合同审查引擎（第二版）。"""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass
from typing import Any, Dict, List, Optional

from review_v2.clause_parser import parse_contract_clauses
from review_v2.contract_registry import (
    UnsupportedContractTypeError,
    get_checklist,
    get_contract_meta,
    supported_contract_display_names,
)
from review_v2.house_lease_checklist import ReviewCheckpoint
from review_v2.llm_semantic_reviewer import get_llm_review_status, judge_checkpoints_with_llm
from review_v2.semantic_reviewer import judge_checkpoint, matched_terms


NEGATION_WORDS = ("无", "没有", "未", "不包含", "不涉及", "并非", "不是")
VERDICT_WORDS = (
    "判决结果",
    "判决",
    "裁判结论",
    "驳回请求",
    "押金全额返还",
    "扣除维修费后返还余额",
    "承租方应赔偿",
    "出租方应赔偿",
)

REPORT_FORMAT_NOTICE = "本报告基于完整合同模板逐项审查，部分缺失项可能因合同格式简略所致，建议结合合同实际用途判断优先级。"
COVERAGE_NOT_APPLICABLE = "不适用"
ISSUE_NOT_APPLICABLE = "不适用"

CASE_DOCUMENT_HINTS = (
    "原告",
    "被告",
    "本院认为",
    "经审理查明",
    "审理查明",
    "诉称",
    "辩称",
    "案号",
    "民事判决书",
    "民事裁定书",
)


@dataclass
class ReviewItemResult:
    item_id: str
    node_id: str
    title: str
    risk_level: str
    status: str
    risk_point_description: str
    suggested_clause_example: str
    legal_basis_index: str
    legal_consequence_if_missing: str
    applicable_if: str
    matched_terms: List[str]
    coverage_status: str
    issue_type: str
    evidence_clauses: List[Dict[str, Any]]
    evidence_location: str
    reasoning_summary: str
    judge_source: str = "rule_fallback"
    llm_confidence: str = ""
    llm_raw_reason: str = ""
    fallback_reason: str = ""
    review_status: str = "待处理"
    reviewer_note: str = ""

    def to_public_dict(self) -> Dict[str, Any]:
        return asdict(self)


def _compact(text: str) -> str:
    return re.sub(r"\s+", "", text or "")


def _has_negated_word(text: str, word: str, window: int = 5) -> bool:
    for match in re.finditer(re.escape(word), text):
        prefix = text[max(0, match.start() - window):match.start()]
        if any(negation in prefix for negation in NEGATION_WORDS):
            return True
    return False


def _has_unnegated_word(text: str, word: str, window: int = 5) -> bool:
    for match in re.finditer(re.escape(word), text):
        prefix = text[max(0, match.start() - window):match.start()]
        if not any(negation in prefix for negation in NEGATION_WORDS):
            return True
    return False


def _matched_terms(text: str, terms: tuple[str, ...]) -> List[str]:
    return matched_terms(text, terms)


_SALE_APPLICABILITY_KEYWORDS: Dict[str, tuple[str, ...]] = {
    "sale_retention_title_clause": ("分期付款", "赊销", "所有权保留", "保留所有权", "付清全款前", "全款付清后", "未付清全部价款", "未付清全款"),
    "sale_retention_registration": ("分期付款", "赊销", "所有权保留", "保留所有权", "付清全款前", "全款付清后", "未付清全部价款", "未付清全款"),
    "sale_retention_retake": ("分期付款", "赊销", "所有权保留", "保留所有权", "付清全款前", "全款付清后", "未付清全部价款", "未付清全款"),
    "sale_retention_redemption": ("分期付款", "赊销", "所有权保留", "保留所有权", "付清全款前", "全款付清后", "未付清全部价款", "未付清全款"),
    "sale_installment_payment": ("分期付款", "分期支付", "分批付款", "每期", "首期", "尾期"),
    "sale_trial_use_period": ("试用", "试用期", "试运行", "试产", "免费试用", "先试后买"),
    "sale_trial_risk": ("试用", "试用期", "试运行", "试产", "免费试用", "先试后买"),
    "sale_sample_quality": ("样品", "样板", "封样", "凭样品", "样品确认", "按样交付"),
    "sale_risk_goods_in_transit": ("路货买卖", "在途", "在途货物", "运输途中", "已发运", "发运后转卖"),
}


def _has_installment_pattern(compacted_text: str) -> bool:
    return bool(
        re.search(r"分[一二三四五六七八九十百\d]+期", compacted_text)
        or re.search(r"第[一二三四五六七八九十百\d]+期", compacted_text)
    )


def _is_checkpoint_applicable(contract_text: str, checkpoint: ReviewCheckpoint, contract_type_key: str) -> tuple[bool, str]:
    if contract_type_key != "sale":
        return True, ""
    keywords = _SALE_APPLICABILITY_KEYWORDS.get(checkpoint.node_id)
    if not keywords:
        return True, ""

    compacted = _compact(contract_text)
    if checkpoint.node_id == "sale_installment_payment" and _has_installment_pattern(compacted):
        return True, "合同文本出现分期付款结构，适用该专项审查点。"
    for keyword in keywords:
        if _has_unnegated_word(compacted, keyword, window=6):
            return True, f"合同文本出现“{keyword}”，适用该专项审查点。"
    return False, f"未发现触发该专项审查点的交易类型表述：{checkpoint.applicable_if}"


def _not_applicable_item(checkpoint: ReviewCheckpoint, reason: str) -> ReviewItemResult:
    return ReviewItemResult(
        item_id=checkpoint.item_id,
        node_id=checkpoint.node_id,
        title=checkpoint.title,
        risk_level="不适用",
        status="不适用",
        risk_point_description="该审查点仅适用于特定买卖交易类型，当前合同文本未触发对应适用条件。",
        suggested_clause_example=checkpoint.suggested_clause,
        legal_basis_index=checkpoint.legal_basis,
        legal_consequence_if_missing=checkpoint.legal_consequence_if_missing,
        applicable_if=checkpoint.applicable_if,
        matched_terms=[],
        coverage_status=COVERAGE_NOT_APPLICABLE,
        issue_type=ISSUE_NOT_APPLICABLE,
        evidence_clauses=[],
        evidence_location="",
        reasoning_summary=reason,
        judge_source="applicability_filter",
    )


def _is_case_document_excerpt(text: str) -> bool:
    compacted = _compact(text)
    if "原告" in compacted and "被告" in compacted and ("租赁合同" in compacted or "房屋租赁合同" in compacted):
        return True
    hit_count = sum(1 for hint in CASE_DOCUMENT_HINTS if hint in compacted)
    return hit_count >= 2 and ("合同" in compacted or "租赁" in compacted)


def _apply_source_exemptions(item: ReviewItemResult, contract_text: str) -> ReviewItemResult:
    if item.item_id != "HL-002" or not _is_case_document_excerpt(contract_text):
        return item
    if item.coverage_status == "通过":
        item.risk_level = "低"
        return item

    item.risk_level = "低"
    item.status = "已覆盖"
    item.coverage_status = "通过"
    item.issue_type = "通过"
    item.risk_point_description = (
        "输入文本呈现为案件文书摘录，通常只会保留出租人、承租人的诉讼身份或角色摘要，"
        "不能按完整签约合同要求其载明证件号、住所和联系方式。正式合同原文仍建议补全主体身份信息。"
    )
    item.reasoning_summary = (
        "检测到文本具有案件文书摘录特征，本项按来源豁免处理：只要能够识别出租人与承租人的角色，"
        "不因摘录中缺少证件号、住所、联系方式而认定为条款缺陷。"
    )
    focused_evidence = [
        clause
        for clause in item.evidence_clauses
        if ("原告" in clause.get("text", "") and "被告" in clause.get("text", ""))
        or ("出租人" in clause.get("text", "") and "承租人" in clause.get("text", ""))
    ]
    if focused_evidence:
        item.evidence_clauses = focused_evidence[:1]
        item.evidence_location = item.evidence_clauses[0].get("location", "")
    item.fallback_reason = "案件文书摘录来源豁免"
    return item


def _assess_checkpoint(contract_text: str, checkpoint: ReviewCheckpoint) -> ReviewItemResult:
    clauses = parse_contract_clauses(contract_text)
    judgment = judge_checkpoint(checkpoint, clauses)
    return ReviewItemResult(
        item_id=checkpoint.item_id,
        node_id=checkpoint.node_id,
        title=checkpoint.title,
        risk_level=judgment.risk_level,
        status=judgment.status,
        risk_point_description=judgment.risk_point_description,
        suggested_clause_example=checkpoint.suggested_clause,
        legal_basis_index=checkpoint.legal_basis,
        legal_consequence_if_missing=checkpoint.legal_consequence_if_missing,
        applicable_if=checkpoint.applicable_if,
        matched_terms=judgment.matched_terms,
        coverage_status=judgment.coverage_status,
        issue_type=judgment.issue_type,
        evidence_clauses=judgment.evidence_clauses,
        evidence_location=judgment.evidence_location,
        reasoning_summary=judgment.reasoning_summary,
        judge_source=judgment.judge_source,
        llm_confidence=judgment.llm_confidence,
        llm_raw_reason=judgment.llm_raw_reason,
        fallback_reason=judgment.fallback_reason,
    )


def _risk_summary(items: List[ReviewItemResult]) -> Dict[str, int]:
    return {
        "高": sum(1 for item in items if item.risk_level == "高"),
        "中": sum(1 for item in items if item.risk_level == "中"),
        "低": sum(1 for item in items if item.risk_level == "低"),
    }


def _coverage_summary(items: List[ReviewItemResult]) -> Dict[str, int]:
    summary: Dict[str, int] = {}
    for item in items:
        summary[item.coverage_status] = summary.get(item.coverage_status, 0) + 1
    return summary


def _judge_source_summary(items: List[ReviewItemResult]) -> Dict[str, int]:
    summary: Dict[str, int] = {}
    for item in items:
        summary[item.judge_source] = summary.get(item.judge_source, 0) + 1
    return summary


def _issue_type_summary(items: List[ReviewItemResult]) -> Dict[str, int]:
    summary: Dict[str, int] = {}
    for item in items:
        summary[item.issue_type] = summary.get(item.issue_type, 0) + 1
    return summary


def _sanitize_review_report(report: str) -> str:
    sanitized = report
    for word in VERDICT_WORDS:
        sanitized = sanitized.replace(word, "审查建议")
    return sanitized


def _format_markdown(contract_type_name: str, items: List[ReviewItemResult]) -> str:
    summary = _risk_summary(items)
    lines = [
        f"# {contract_type_name}审查清单（第二版）",
        "",
        f"- 审查点数量：{len(items)}",
        f"- 高风险：{summary['高']} 项",
        f"- 中风险：{summary['中']} 项",
        f"- 低风险：{summary['低']} 项",
        f"- 不适用：{sum(1 for item in items if item.coverage_status == COVERAGE_NOT_APPLICABLE)} 项",
        "",
        f"说明：{REPORT_FORMAT_NOTICE}",
        "",
        "说明：本引擎只输出条款完备性检查、风险等级和修改建议，不输出纠纷裁判结果。",
        "",
    ]
    for index, item in enumerate(items, start=1):
        lines.extend(
            [
                f"## {index}. {item.title}（{item.item_id}）",
                f"- 风险等级：{item.risk_level}",
                f"- 状态：{item.status}",
                f"- 覆盖状态：{item.coverage_status}",
                f"- 问题类型：{item.issue_type}",
                f"- 判定来源：{'大模型' if item.judge_source == 'llm' else '适用条件过滤' if item.judge_source == 'applicability_filter' else '规则兜底'}",
                f"- 模型置信度：{item.llm_confidence or '无'}",
                f"- 回退原因：{item.fallback_reason or '无'}",
                f"- 原文位置：{item.evidence_location or '未召回正式条款'}",
                f"- 系统判断：{item.reasoning_summary}",
                f"- 【风险点描述】：{item.risk_point_description}",
                f"- 【缺失的法律后果】：{item.legal_consequence_if_missing}",
                f"- 【建议条款示例】：{item.suggested_clause_example}",
                f"- 【法律依据索引】：{item.legal_basis_index}",
                f"- 【适用条件】：{item.applicable_if}",
                "",
            ]
        )
    return _sanitize_review_report("\n".join(lines))


def review_contract_v2(
    contract_text: str,
    contract_type: Optional[str] = "house_lease",
    *,
    include_low_risk: bool = True,
    use_llm: bool = True,
) -> Dict[str, Any]:
    """按第二版审查清单审查合同。

    当前原型仅实现房屋租赁合同；新增合同类型时应新增清单配置，再接入
    合同类型映射，不复用裁判结论。
    """

    normalized_type = (contract_type or "house_lease").strip().lower()
    try:
        type_meta = get_contract_meta(contract_type)
    except UnsupportedContractTypeError:
        type_meta = None
    llm_status = get_llm_review_status()
    if not use_llm:
        global_fallback_reason = "本次审查未启用大模型语义复核，使用规则判定"
    elif not llm_status.get("available"):
        global_fallback_reason = llm_status.get("message", "")
    else:
        global_fallback_reason = ""

    if not type_meta:
        return {
            "success": False,
            "contract_type": normalized_type,
            "contract_type_name": "未支持的合同类型",
            "message": f"审查第二版当前支持{'、'.join(supported_contract_display_names())}；其他合同类型应按同一审查清单结构迁移。",
            "items": [],
            "summary": {"高": 0, "中": 0, "低": 0},
            "coverage_summary": {},
            "issue_type_summary": {},
            "judge_source_summary": {},
            "llm_enabled": use_llm,
            "llm_status": llm_status,
            "global_fallback_reason": global_fallback_reason,
            "report_notice": REPORT_FORMAT_NOTICE,
            "result": "",
        }

    checklist = get_checklist(type_meta.key)
    clauses = parse_contract_clauses(contract_text)
    applicable_checkpoints = []
    not_applicable_items: Dict[str, ReviewItemResult] = {}
    for checkpoint in checklist:
        is_applicable, applicability_reason = _is_checkpoint_applicable(contract_text, checkpoint, type_meta.key.value)
        if is_applicable:
            applicable_checkpoints.append(checkpoint)
        else:
            not_applicable_items[checkpoint.item_id] = _not_applicable_item(checkpoint, applicability_reason)

    judgments = judge_checkpoints_with_llm(tuple(applicable_checkpoints), clauses, use_llm=use_llm)
    items = []
    for checkpoint in checklist:
        if checkpoint.item_id in not_applicable_items:
            items.append(not_applicable_items[checkpoint.item_id])
            continue
        judgment = judgments[checkpoint.item_id]
        item = ReviewItemResult(
            item_id=checkpoint.item_id,
            node_id=checkpoint.node_id,
            title=checkpoint.title,
            risk_level=judgment.risk_level,
            status=judgment.status,
            risk_point_description=judgment.risk_point_description,
            suggested_clause_example=checkpoint.suggested_clause,
            legal_basis_index=checkpoint.legal_basis,
            legal_consequence_if_missing=checkpoint.legal_consequence_if_missing,
            applicable_if=checkpoint.applicable_if,
            matched_terms=judgment.matched_terms,
            coverage_status=judgment.coverage_status,
            issue_type=judgment.issue_type,
            evidence_clauses=judgment.evidence_clauses,
            evidence_location=judgment.evidence_location,
            reasoning_summary=judgment.reasoning_summary,
            judge_source=judgment.judge_source,
            llm_confidence=judgment.llm_confidence,
            llm_raw_reason=judgment.llm_raw_reason,
            fallback_reason=judgment.fallback_reason,
        )
        items.append(_apply_source_exemptions(item, contract_text))
    visible_items = items if include_low_risk else [item for item in items if item.risk_level in {"高", "中"}]
    contract_type_name = type_meta.display_name
    result = _format_markdown(contract_type_name, visible_items)
    return {
        "success": True,
        "contract_type": type_meta.response_key,
        "contract_type_name": contract_type_name,
        "message": f"审查第二版已完成{contract_type_name}{len(items)}项核心检查。",
        "items": [item.to_public_dict() for item in visible_items],
        "all_items_count": len(items),
        "summary": _risk_summary(items),
        "coverage_summary": _coverage_summary(items),
        "issue_type_summary": _issue_type_summary(items),
        "judge_source_summary": _judge_source_summary(items),
        "llm_enabled": use_llm,
        "llm_status": llm_status,
        "global_fallback_reason": global_fallback_reason,
        "report_notice": REPORT_FORMAT_NOTICE,
        "clause_count": len(clauses),
        "formal_clause_count": sum(1 for clause in clauses if clause.section_type in {"正式合同条款", "附件"}),
        "result": result,
    }
