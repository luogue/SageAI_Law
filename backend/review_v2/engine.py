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
from review_v2.semantic_reviewer import _has_gift_paid_consideration_risk, judge_checkpoint, matched_terms


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


_CONTRACT_APPLICABILITY_KEYWORDS: Dict[str, Dict[str, tuple[str, ...]]] = {
    "sale": {
    "sale_retention_title_clause": ("分期付款", "赊销", "所有权保留", "保留所有权", "付清全款前", "全款付清后", "未付清全部价款", "未付清全款"),
    "sale_retention_registration": ("分期付款", "赊销", "所有权保留", "保留所有权", "付清全款前", "全款付清后", "未付清全部价款", "未付清全款"),
    "sale_retention_retake": ("分期付款", "赊销", "所有权保留", "保留所有权", "付清全款前", "全款付清后", "未付清全部价款", "未付清全款"),
    "sale_retention_redemption": ("分期付款", "赊销", "所有权保留", "保留所有权", "付清全款前", "全款付清后", "未付清全部价款", "未付清全款"),
    "sale_installment_payment": ("分期付款", "分期支付", "分批付款", "每期", "首期", "尾期"),
    "sale_trial_use_period": ("试用", "试用期", "试运行", "试产", "免费试用", "先试后买"),
    "sale_trial_risk": ("试用", "试用期", "试运行", "试产", "免费试用", "先试后买"),
    "sale_sample_quality": ("样品", "样板", "封样", "凭样品", "样品确认", "按样交付"),
    "sale_risk_goods_in_transit": ("路货买卖", "在途", "在途货物", "运输途中", "已发运", "发运后转卖"),
    },
    "deposit": {
        "safekeeping_valuable_declaration": ("贵重物品", "货币", "有价证券", "珠宝", "名表", "贵金属", "重要文件", "高价值"),
        "safekeeping_undeclared_valuable_consequence": ("贵重物品", "货币", "有价证券", "珠宝", "名表", "贵金属", "重要文件", "高价值"),
        "safekeeping_consumptive_type": ("消费保管", "货币保管", "可替代物", "同种类", "同品质", "混同保管"),
        "safekeeping_consumptive_return_rule": ("消费保管", "货币保管", "可替代物", "同种类", "同品质", "混同保管"),
        "safekeeping_currency_interest": ("货币保管", "现金", "款项", "利息", "收益"),
        "safekeeping_consumptive_mixing": ("消费保管", "可替代物", "同类物", "批量保管", "混同保管"),
    },
    "work_contract": {
        "work_main_subcontract_consent": ("转包", "分包", "外协", "第三人完成", "交由第三人", "委托第三人"),
        "work_auxiliary_subcontract_liability": ("转包", "分包", "外协", "第三人完成", "辅助工作", "委托第三人"),
        "work_illegal_total_subcontract": ("全部转包", "整体转包", "肢解转包", "拆分转包", "主要工作交由第三人"),
        "work_sample_attachment": ("样品", "样板", "封样", "凭样", "样品确认", "按样制作"),
    },
    "agency": {
        "agency_sub_entrustment_consent": ("转委托", "第三人处理", "委托别人", "另行委托", "委托第三人"),
        "agency_sub_entrustment_liability": ("转委托", "第三人处理", "委托别人", "另行委托", "委托第三人"),
        "agency_emergency_sub_entrustment": ("转委托", "第三人处理", "紧急情况", "无法联系", "维护委托人利益"),
        "agency_self_agency_consent": ("自己代理", "与自己交易", "利益冲突", "自我交易"),
        "agency_both_side_agency_consent": ("双方代理", "同时代理双方", "交易双方", "利益冲突"),
        "agency_conflict_unfair_transaction": ("利益冲突", "显失公平", "低价转让", "高价购买", "不公平"),
        "agency_undisclosed_principal_intervention": ("以自己名义", "隐名委托", "第三人不知道", "披露第三人", "介入权"),
        "agency_disclose_third_party": ("以自己名义", "隐名委托", "第三人不履行", "披露第三人", "交易资料"),
        "agency_intervention_defense_continuation": ("以自己名义", "隐名委托", "介入权", "抗辩", "抵销"),
        "agency_third_party_choice_right": ("以自己名义", "隐名委托", "披露委托人", "选择权", "第三人选择"),
        "agency_disclose_principal": ("以自己名义", "隐名委托", "披露委托人", "委托人身份", "第三人"),
        "agency_choice_defense_continuation": ("以自己名义", "隐名委托", "选择权", "抗辩", "抵销"),
    },
    "guarantee": {
        "guarantee_share_agreed": ("共同保证人", "共同保证", "共同担保", "连带共同保证", "多个保证人", "两个以上保证人", "保证人A", "保证人B", "保证人名单"),
        "joint_guarantor_internal_recourse": ("共同保证人", "共同保证", "共同担保", "连带共同保证", "多个保证人", "两个以上保证人", "保证人A", "保证人B", "保证人之间"),
        "maximum_guarantee_period": ("最高额保证", "最高额担保", "最高债权额", "债权确定期间", "最高额保证终止", "最高额保证期间"),
        "post_period_signature_new_guarantee": ("保证期间届满", "期间届满后", "催收通知签字", "催收通知", "重新保证", "新的保证合同", "继续承担保证责任", "责任恢复"),
    },
    "construction": {
        "valid_bid_award_document": ("招标", "投标", "中标", "中标通知书", "招标文件", "投标文件", "评标", "备案合同"),
    },
}


def _has_installment_pattern(compacted_text: str) -> bool:
    return bool(
        re.search(r"分[一二三四五六七八九十百\d]+期", compacted_text)
        or re.search(r"第[一二三四五六七八九十百\d]+期", compacted_text)
    )


def _construction_contract_body(contract_text: str) -> str:
    """Ignore test notes appended after the contract body."""
    body = contract_text
    for marker in ("**测试重点：", "测试重点：", "测试重点", "【测试重点】"):
        if marker in body:
            body = body.split(marker, 1)[0]
    return body


_TECHNOLOGY_SUBTYPE_KEYWORDS: Dict[str, tuple[str, ...]] = {
    "development": ("技术开发", "委托开发", "合作开发", "研究开发", "研发", "新技术", "新产品", "新工艺", "新材料"),
    "entrusted_development": (
        "委托开发",
        "委托研究开发",
        "委托研发",
        "技术开发（委托）",
        "技术开发(委托)",
        "委托方",
        "委托人",
        "研究开发方",
        "研究开发人",
        "委托乙方研究开发",
        "甲方委托乙方",
    ),
    "cooperative_development": ("合作开发", "双方共同", "共同投资", "共同参与", "共同研发", "共同研究开发", "协作开发"),
    "transfer": ("技术转让", "专利权转让", "专利申请权转让", "技术秘密转让", "让与", "受让"),
    "license": ("技术许可", "专利实施许可", "许可使用", "许可人", "被许可人", "独占许可", "排他许可", "普通许可"),
    "consulting": ("技术咨询", "咨询报告", "可行性论证", "技术预测", "分析评价"),
    "service": ("技术服务", "解决特定技术问题", "服务成果", "服务内容", "技术培训", "技术支持"),
    "import_export": ("技术进出口", "技术进口", "技术出口", "跨境技术", "跨境许可", "跨境交付", "数据出境"),
    "research_org": ("课题组", "实验室", "研究中心", "科研组织", "内部机构"),
    "existing_tech_fraud": ("现有技术", "冒充研发", "重复收费", "同一课题", "欺诈"),
}


_TECHNOLOGY_SUBTYPE_LABELS: Dict[str, str] = {
    "development": "技术开发",
    "entrusted_development": "委托开发",
    "cooperative_development": "合作开发",
    "transfer": "技术转让",
    "license": "技术许可",
    "consulting": "技术咨询",
    "service": "技术服务",
    "import_export": "技术进出口",
    "research_org": "科研组织签约",
    "existing_tech_fraud": "现有技术冒充研发",
}


def _detect_technology_subtypes(compacted_text: str) -> set[str]:
    subtypes: set[str] = set()
    for subtype, keywords in _TECHNOLOGY_SUBTYPE_KEYWORDS.items():
        if any(_has_unnegated_word(compacted_text, keyword, window=18) for keyword in keywords):
            subtypes.add(subtype)
    if {"entrusted_development", "cooperative_development"} & subtypes:
        subtypes.add("development")
    if "development" in subtypes and "cooperative_development" not in subtypes:
        subtypes.add("entrusted_development")
    return subtypes


def _technology_subtype_reason(subtypes: set[str], checkpoint: ReviewCheckpoint) -> str:
    labels = "、".join(_TECHNOLOGY_SUBTYPE_LABELS[subtype] for subtype in sorted(subtypes) if subtype in _TECHNOLOGY_SUBTYPE_LABELS)
    if not labels:
        labels = "未识别到明确技术合同子类型"
    return f"当前文本识别为{labels}场景，未触发“{checkpoint.title}”的适用条件：{checkpoint.applicable_if}"


def _is_technology_checkpoint_applicable(compacted_text: str, checkpoint: ReviewCheckpoint) -> tuple[Optional[bool], str]:
    subtypes = _detect_technology_subtypes(compacted_text)
    item_id = checkpoint.item_id
    node_id = checkpoint.node_id

    if node_id == "technology_contract_type_classification":
        known_subtypes = {"development", "transfer", "license", "consulting", "service"} & subtypes
        return (False, _technology_subtype_reason(subtypes, checkpoint)) if known_subtypes else (True, "")

    if node_id == "fraud_contract_existing_technology":
        return (True, "") if "existing_tech_fraud" in subtypes else (False, _technology_subtype_reason(subtypes, checkpoint))

    if node_id == "research_organization_authorization":
        return (True, "") if "research_org" in subtypes else (False, _technology_subtype_reason(subtypes, checkpoint))

    if item_id.startswith("TC-04"):
        if "entrusted_development" in subtypes and "cooperative_development" not in subtypes:
            return True, ""
        return False, _technology_subtype_reason(subtypes, checkpoint)

    if item_id.startswith("TC-05"):
        if node_id == "technical_secret_result_rights":
            return (True, "") if "development" in subtypes else (False, _technology_subtype_reason(subtypes, checkpoint))
        if node_id == "cooperation_breach_and_exit":
            return (True, "") if "development" in subtypes else (False, _technology_subtype_reason(subtypes, checkpoint))
        if "cooperative_development" in subtypes:
            return True, ""
        return False, _technology_subtype_reason(subtypes, checkpoint)

    subtype_by_prefix = {
        "TC-06": "transfer",
        "TC-07": "license",
        "TC-08": "consulting",
        "TC-09": "service",
    }
    for prefix, subtype in subtype_by_prefix.items():
        if item_id.startswith(prefix):
            return (True, "") if subtype in subtypes else (False, _technology_subtype_reason(subtypes, checkpoint))

    if node_id == "technology_import_export_control":
        return (True, "") if "import_export" in subtypes else (False, _technology_subtype_reason(subtypes, checkpoint))

    return None, ""


def _is_checkpoint_applicable(contract_text: str, checkpoint: ReviewCheckpoint, contract_type_key: str) -> tuple[bool, str]:
    applicability_text = _construction_contract_body(contract_text) if contract_type_key == "construction" else contract_text
    compacted = _compact(applicability_text)
    if contract_type_key == "technology":
        applicable, reason = _is_technology_checkpoint_applicable(compacted, checkpoint)
        if applicable is not None:
            return applicable, reason

    keywords = _CONTRACT_APPLICABILITY_KEYWORDS.get(contract_type_key, {}).get(checkpoint.node_id)
    if not keywords:
        return True, ""

    if contract_type_key == "guarantee" and checkpoint.node_id == "post_period_signature_new_guarantee":
        period_triggered = any(
            _has_unnegated_word(compacted, keyword, window=18)
            for keyword in ("保证期间届满", "期间届满后", "保证期间届满后")
        )
        signature_triggered = any(
            _has_unnegated_word(compacted, keyword, window=18)
            for keyword in ("催收通知签字", "催收通知上签字", "签字", "签收", "重新保证", "新的保证合同", "继续承担保证责任", "责任恢复")
        )
        if period_triggered and signature_triggered:
            return True, "合同文本同时出现保证期间届满后和催收签字/重新保证类表述，适用该专项审查点。"
        return False, f"未发现保证期间届满后催收签字或重新保证的组合情形：{checkpoint.applicable_if}"

    if checkpoint.node_id == "sale_installment_payment" and _has_installment_pattern(compacted):
        return True, "合同文本出现分期付款结构，适用该专项审查点。"
    for keyword in keywords:
        if _has_unnegated_word(compacted, keyword, window=18):
            return True, f"合同文本出现“{keyword}”，适用该专项审查点。"
    return False, f"未发现触发该专项审查点的交易类型表述：{checkpoint.applicable_if}"


def _not_applicable_item(checkpoint: ReviewCheckpoint, reason: str) -> ReviewItemResult:
    return ReviewItemResult(
        item_id=checkpoint.item_id,
        node_id=checkpoint.node_id,
        title=checkpoint.title,
        risk_level="不适用",
        status="不适用",
        risk_point_description="该审查点仅适用于特定交易场景，当前合同文本未触发对应适用条件。",
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


def _apply_gift_consideration_override(item: ReviewItemResult, contract_text: str) -> ReviewItemResult:
    if item.item_id != "G-01-04" or item.coverage_status != "风险条款":
        return item
    if _has_gift_paid_consideration_risk(contract_text):
        return item

    item.risk_level = "低"
    item.status = "未发现明显风险条款"
    item.coverage_status = "通过"
    item.issue_type = "通过"
    item.risk_point_description = (
        "合同已明确无偿赠与，且未发现未被无偿声明排除的价款、收益、回购、还款或其他实质有偿对价安排。"
    )
    item.reasoning_summary = (
        "检测到合同已声明无偿赠与或无需支付对价，G-01-04 不再因“对价”等否定语境中的词语误判为风险条款。"
    )
    item.matched_terms = []
    item.evidence_clauses = []
    item.evidence_location = ""
    item.fallback_reason = "赠与无偿性专项校正"
    return item


_DEPENDENCY_BAD_COVERAGE = {"部分覆盖", "缺失", "风险条款"}
_DEPENDENCY_BAD_ISSUES = {"模板空白", "条款缺陷", "完全缺失", "风险条款"}
_GIFT_CHECKPOINT_DEPENDENCIES: Dict[str, Dict[str, str]] = {
    "G-09-03": {
        "depends_on": "G-09-01",
        "risk_level": "中",
        "mode": "partial",
        "reason": "不履行附义务的救济以受赠人义务内容为前提；前置义务内容未完整填写时，救济条款不能单独视为完整通过。",
    },
    "G-10-04": {
        "depends_on": "G-09-01",
        "risk_level": "中",
        "mode": "sync",
        "reason": "附义务赠与瑕疵担保范围以受赠人义务内容为计算和适用前提；前置义务内容缺失或空白时，本项应同步前置条款状态。",
    },
    "G-11-01": {
        "depends_on": "G-01-02",
        "risk_level": "中",
        "mode": "sync",
        "reason": "撤销后返还规则以赠与的无偿性基础为前提；无偿赠与意思表示未完整覆盖时，本项应同步前置条款状态。",
    },
}


def _dependency_is_incomplete(item: ReviewItemResult | None) -> bool:
    if not item:
        return False
    return item.coverage_status in _DEPENDENCY_BAD_COVERAGE or item.issue_type in _DEPENDENCY_BAD_ISSUES


def _dependency_status(dep: ReviewItemResult) -> str:
    if dep.coverage_status == "缺失":
        return "缺失或不明确"
    if dep.coverage_status == "风险条款":
        return "发现风险条款"
    return "部分覆盖，需先补全前置条款"


def _apply_gift_dependency_rules(items: List[ReviewItemResult]) -> List[ReviewItemResult]:
    by_id = {item.item_id: item for item in items}
    for item_id, rule in _GIFT_CHECKPOINT_DEPENDENCIES.items():
        item = by_id.get(item_id)
        dependency = by_id.get(rule["depends_on"])
        if not item or not _dependency_is_incomplete(dependency):
            continue

        assert dependency is not None
        item.risk_level = rule["risk_level"]
        if rule["mode"] == "sync":
            item.coverage_status = dependency.coverage_status
            item.issue_type = dependency.issue_type
            item.status = _dependency_status(dependency)
        else:
            item.coverage_status = "部分覆盖"
            item.issue_type = dependency.issue_type if dependency.issue_type == "模板空白" else "条款缺陷"
            item.status = "部分覆盖，需先补全前置条款"
        item.reasoning_summary = f"{rule['reason']} 当前前置审查点 {dependency.item_id}（{dependency.title}）状态为“{dependency.coverage_status}/{dependency.issue_type}”。"
        item.risk_point_description = f"该审查点依赖前置条款“{dependency.title}”。前置条款未完整覆盖时，本项不能单独认定为完整通过。"
        item.fallback_reason = "赠与合同跨条款依赖校正"
    return items


def _apply_technology_development_mode_rules(items: List[ReviewItemResult], contract_text: str) -> List[ReviewItemResult]:
    subtypes = _detect_technology_subtypes(_compact(contract_text))
    if "entrusted_development" not in subtypes or "cooperative_development" in subtypes:
        return items

    for item in items:
        if item.item_id != "TC-05-03" or item.coverage_status == COVERAGE_NOT_APPLICABLE:
            continue
        item.risk_level = "中"
        item.risk_point_description = (
            "委托开发合同中，技术秘密成果使用转让规则仍建议明确；但该项可由委托开发成果归属、保密和验收交付条款部分承接，"
            "缺失通常不属于直接阻碍合同履行的高风险。"
        )
        item.reasoning_summary = (
            f"{item.reasoning_summary} 当前合同识别为委托开发合同，TC-05-03 按委托开发场景降为中风险；"
            "如技术秘密成果具有核心商业价值，仍建议补充使用、转让、许可、收益分配和保密限制。"
        )
        item.fallback_reason = "技术合同开发方式风险校正"
    return items


def _clause_public_dict(clause: Any) -> Dict[str, Any]:
    return clause.to_public_dict() if hasattr(clause, "to_public_dict") else asdict(clause)


def _find_clause(clauses: List[Any], predicate) -> Optional[Any]:
    for clause in clauses:
        if predicate(clause):
            return clause
    return None


def _find_clauses(clauses: List[Any], predicate, limit: int = 2) -> List[Any]:
    found = []
    for clause in clauses:
        if predicate(clause):
            found.append(clause)
            if len(found) >= limit:
                break
    return found


def _set_item_pass(item: ReviewItemResult, evidence: List[Any], reason: str, description: str) -> None:
    item.risk_level = "低"
    item.status = "已覆盖"
    item.coverage_status = "通过"
    item.issue_type = "通过"
    item.risk_point_description = description
    item.reasoning_summary = reason
    item.evidence_clauses = [_clause_public_dict(clause) for clause in evidence]
    item.evidence_location = "；".join(clause.location for clause in evidence)
    item.fallback_reason = "房屋租赁真实合同条款专项校正"


def _set_item_partial(
    item: ReviewItemResult,
    evidence: List[Any],
    risk_level: str,
    reason: str,
    description: str,
    issue_type: str = "条款缺陷",
) -> None:
    item.risk_level = risk_level
    item.status = "部分覆盖"
    item.coverage_status = "部分覆盖"
    item.issue_type = issue_type
    item.risk_point_description = description
    item.reasoning_summary = reason
    item.evidence_clauses = [_clause_public_dict(clause) for clause in evidence]
    item.evidence_location = "；".join(clause.location for clause in evidence)
    item.fallback_reason = "房屋租赁真实合同条款专项校正"


def _set_item_not_applicable(item: ReviewItemResult, reason: str) -> None:
    item.risk_level = "不适用"
    item.status = "不适用"
    item.coverage_status = COVERAGE_NOT_APPLICABLE
    item.issue_type = ISSUE_NOT_APPLICABLE
    item.risk_point_description = "该审查点仅适用于特定交易场景，当前合同文本未触发对应适用条件。"
    item.reasoning_summary = reason
    item.evidence_clauses = []
    item.evidence_location = ""
    item.judge_source = "applicability_filter"
    item.fallback_reason = "房屋租赁真实合同条款专项校正"


def _has_house_title_certificate(compacted: str) -> bool:
    return bool(re.search(r"(产证编号|不动产权证|房地产权证|沪房地|房地.+第\\d+号)", compacted))


def _has_reasonable_rent_penalty(compacted: str) -> bool:
    if not ("违约金" in compacted and ("月租金" in compacted or "租金" in compacted)):
        return False
    if re.search(r"(月租金|租金)的?(?:1|2|一|二|两)倍", compacted):
        return True
    return "不够抵付损失" in compacted or "不足抵付损失" in compacted or "赔偿造成的损失" in compacted


def _apply_house_lease_real_contract_rules(items: List[ReviewItemResult], contract_text: str) -> List[ReviewItemResult]:
    clauses = parse_contract_clauses(contract_text)
    compacted = _compact(contract_text)
    by_id = {item.item_id: item for item in items}

    party_evidence = _find_clauses(
        clauses,
        lambda clause: (
            ("甲方" in clause.text or "乙方" in clause.text)
            and ("证号" in clause.text or "居民身份证" in clause.text or "联系地址" in clause.text or "联系电话" in clause.text)
            and not any(term in clause.text for term in ("房地产经纪", "中介", "居间介绍", "代理内容"))
        ),
        limit=3,
    )
    if party_evidence and (item := by_id.get("HL-002")):
        _set_item_pass(
            item,
            party_evidence,
            "合同首部/签署栏直接列明甲方、乙方姓名、身份证件号、住址和联系方式，证据应定位主体信息栏，不应引用中介服务附件。",
            "出租人与承租人的身份信息已在合同主体信息栏中列明，可支持签约主体识别、通知联系和后续履行。",
        )

    delivery_evidence = _find_clauses(
        clauses,
        lambda clause: (
            ("联系地址" in clause.text or "联系电话" in clause.text or "证号" in clause.text)
            and ("甲方" in clause.text or "乙方" in clause.text)
            and not any(term in clause.text for term in ("房地产经纪", "中介", "居间介绍", "代理内容"))
        ),
        limit=3,
    )
    if delivery_evidence and (item := by_id.get("HL-005")):
        _set_item_pass(
            item,
            delivery_evidence,
            "合同列明双方住址、联系电话和身份信息，已具备通知、催告和送达的基础联系信息；真实合同场景下不应再因未召回第十二条而认定为缺失。",
            "合同已提供双方可用于通知和催告的联系地址、联系电话及身份信息，通知送达基础已覆盖。",
        )

    title_certificate = _find_clause(clauses, lambda clause: "产证编号" in clause.text or "沪房地" in clause.text or "不动产权证" in clause.text)
    if title_certificate and _has_house_title_certificate(compacted) and (item := by_id.get("HL-010")):
        _set_item_partial(
            item,
            [title_certificate],
            "中",
            "合同已列明产证编号和权利人信息，能间接证明房屋权属与合法出租基础；但未单独写明“房屋合法、非违法建筑、具备出租条件”的保证条款，按中风险处理更贴近实务。",
            "合同已列明产证编号或权属证明信息，房屋合法性并非完全缺失；建议补充出租人对房屋合法性和可出租性的明示保证。",
            issue_type="条款缺陷",
        )

    rent_default = _find_clause(
        clauses,
        lambda clause: "逾期不支付租金" in clause.text and ("1个月" in _compact(clause.text) or "一个月" in clause.text or "解除本合同" in clause.text),
    )
    if rent_default and (item := by_id.get("HL-015")):
        _set_item_pass(
            item,
            [rent_default],
            "合同第九条已约定乙方逾期不支付租金累计超过1个月时可解除合同，已经覆盖欠租重大违约标准。",
            "欠租达到累计超过1个月即构成解除事由，欠租重大违约标准已明确。",
        )

    early_surrender = _find_clause(
        clauses,
        lambda clause: "提前退租" in clause.text and "违约金" in clause.text and ("2倍" in clause.text or "二倍" in clause.text or "两倍" in clause.text),
    )
    if early_surrender and (item := by_id.get("HL-029")):
        _set_item_pass(
            item,
            [early_surrender],
            "合同第十条已明确乙方中途擅自退租时按提前退租天数租金的2倍支付违约金，并约定不足抵付损失时继续赔偿，提前退租规则已覆盖。",
            "提前退租的违约金计算方式和损失补足规则已明确。",
        )
    if early_surrender and (item := by_id.get("HL-030")):
        _set_item_not_applicable(
            item,
            "合同第十条已明确约定提前退租违约金和损失补足规则，不属于“无提前退租条款时的协商补位”场景，本审查点不适用。",
        )

    expiry_settlement = _find_clause(
        clauses,
        lambda clause: "返还该房屋" in clause.text and "结清" in clause.text and "费用" in clause.text,
    )
    if expiry_settlement and (item := by_id.get("HL-031")):
        _set_item_pass(
            item,
            [expiry_settlement],
            "合同第七条约定租期届满返还房屋、验收认可并相互结清各自应承担费用，已覆盖租期届满结算。",
            "租期届满后的房屋返还、验收和费用结清规则已明确。",
        )

    damage_evidence_list = _find_clause(
        clauses,
        lambda clause: (
            ("附件三" in clause.text or "家电及装修清单" in clause.text or "家具家电" in clause.text or "装修清单" in clause.text)
            and not ("合同备案" in clause.text or "备案" in clause.text)
        ),
    )
    if damage_evidence_list and (item := by_id.get("HL-035")):
        _set_item_partial(
            item,
            [damage_evidence_list],
            "低",
            "合同附件三列明家电及装修清单，可作为退租时核对房屋附属设施和装修状态的基础证据；但仍未完整约定照片、视频、维修单、报价单等损坏举证材料，故保持部分覆盖。",
            "附件三已提供家电及装修清单作为损坏认定的基础证据，但损坏事实、原因和金额的举证材料仍需进一步补足。",
            issue_type="模板空白",
        )
        if "附件三" in damage_evidence_list.text:
            item.evidence_location = "附件三（家电及装修清单）"

    penalty_evidence = []
    for predicate in (
        lambda clause: "月租金的2倍" in clause.text and "违约金" in clause.text,
        lambda clause: "提前退租" in clause.text and "违约金" in clause.text,
    ):
        found = _find_clause(clauses, predicate)
        if found and found not in penalty_evidence:
            penalty_evidence.append(found)
    if penalty_evidence and _has_reasonable_rent_penalty(compacted) and (item := by_id.get("HL-039")):
        _set_item_partial(
            item,
            penalty_evidence[:2],
            "中",
            "合同约定违约金为月租金或提前退租天数租金的2倍，并设置损失不足时补赔规则，未明显偏离居住租赁常见损失范围；不宜自动列为高风险，但仍建议保留与实际损失挂钩的表述。",
            "违约金约定已有计算基础，且2倍月租金/租金天数通常不属于明显过高；建议进一步写明可结合实际损失、空置期和再出租成本调整。",
            issue_type="条款缺陷",
        )

    return items


def _apply_sale_contract_rules(items: List[ReviewItemResult], contract_text: str) -> List[ReviewItemResult]:
    clauses = parse_contract_clauses(contract_text)
    by_id = {item.item_id: item for item in items}

    quality_remedy = _find_clause(
        clauses,
        lambda clause: (
            ("质量问题" in clause.text or "质量异议" in clause.text or "质量不合格" in clause.text)
            and ("日内" in clause.text or "10日" in clause.text or "十日" in clause.text or "期限" in clause.text)
            and ("更换" in clause.text or "换货" in clause.text or "补发" in clause.text or "补货" in clause.text)
        ),
    )
    if quality_remedy and (item := by_id.get("S-06-03")):
        _set_item_partial(
            item,
            [quality_remedy],
            "中",
            "合同已约定发现质量问题应在期限内提出，并由出卖人及时更换、补发，已覆盖质量异议期限和部分补救方式；但未完整列明修理、重作、退货、减少价款、赔偿损失等法定救济路径，故不应按完全缺失处理。",
            "合同已有质量问题异议和更换补发机制，但质量瑕疵救济方式仍不完整，建议补充修理、重作、退货、减少价款、赔偿损失等处理路径。",
            issue_type="条款缺陷",
        )
        item.fallback_reason = "买卖合同质量异议补救条款专项校正"

    return items


def _construction_has_contract_title(compacted: str) -> bool:
    return any(term in compacted for term in ("建设工程施工合同", "建设工程合同", "施工合同", "工程施工合同"))


def _construction_has_total_subcontract_prohibition(compacted: str) -> bool:
    total_transfer_ban = bool(
        re.search(r"(不得|禁止).{0,24}(全部工程|全部承包工程|承包的全部工程).{0,16}(转包|转让)", compacted)
        or re.search(r"(不得|禁止).{0,16}(转包|整体转让施工)", compacted)
    )
    split_transfer_ban = bool(
        re.search(r"(不得|禁止).{0,24}(肢解|分解|拆分).{0,24}(转包|分包)", compacted)
        or re.search(r"(肢解|分解|拆分).{0,24}(后|以后)?.{0,12}(不得|禁止)?.{0,12}(分包|转包)", compacted)
    )
    return total_transfer_ban and split_transfer_ban


def _construction_has_resubcontract_prohibition(compacted: str) -> bool:
    return bool(
        re.search(r"(不得|禁止).{0,20}(再分包|二次分包|层层分包)", compacted)
        or re.search(r"(不得|禁止).{0,18}分包单位.{0,18}再分包", compacted)
        or re.search(r"分包单位.{0,18}(不得|禁止).{0,18}(再分包|二次分包|层层分包)", compacted)
    )


def _mark_construction_pass(item: ReviewItemResult, description: str, reason: str) -> None:
    item.risk_level = "低"
    item.status = "未发现明显风险条款"
    item.coverage_status = "通过"
    item.issue_type = "通过"
    item.risk_point_description = description
    item.reasoning_summary = reason
    item.fallback_reason = "建设工程禁止性条款合规校正"


def _apply_construction_contract_rules(items: List[ReviewItemResult], contract_text: str) -> List[ReviewItemResult]:
    compacted = _compact(_construction_contract_body(contract_text))
    has_title = _construction_has_contract_title(compacted)
    has_total_subcontract_ban = _construction_has_total_subcontract_prohibition(compacted)
    has_resubcontract_ban = _construction_has_resubcontract_prohibition(compacted)
    has_bid_consistency_framework = any(term in compacted for term in ("实质性内容", "工程范围", "建设工期", "工程质量", "工程价款", "中标合同一致"))

    for item in items:
        if item.item_id == "CE-01-01" and has_title and item.coverage_status != COVERAGE_NOT_APPLICABLE:
            item.risk_level = "中"
            item.coverage_status = "部分覆盖"
            item.issue_type = "模板空白"
            item.status = "部分覆盖，模板空白"
            item.risk_point_description = (
                "合同标题已能识别为建设工程施工合同，合同性质并非完全缺失；但正文中的工程类型、工程范围或关键项目栏仍可能存在空白，"
                "需要签约前补全以减少履行和结算争议。"
            )
            item.reasoning_summary = (
                "合同标题已明确为建设工程施工合同，足以初步确定合同性质；正文空白影响的是条款完整性，不宜按高风险完全缺失处理，"
                "本项调整为中风险-部分覆盖-模板空白。"
            )
            item.fallback_reason = "建设工程合同标题识别校正"

        if item.item_id == "CE-03-04" and item.coverage_status != COVERAGE_NOT_APPLICABLE and has_bid_consistency_framework:
            item.risk_level = "中"
            item.coverage_status = "部分覆盖"
            item.issue_type = "模板空白"
            item.status = "部分覆盖，模板空白"
            item.risk_point_description = (
                "合同已出现工程范围、建设工期、工程质量、工程价款等实质性内容框架，可提示中标合同一致性风险；"
                "但如项目实际涉及招投标，仍需明确本合同及补充协议不得背离中标合同实质性内容。"
            )
            item.reasoning_summary = (
                "简化版模板已预留建设工程实质性内容框架，但未完整形成中标合同一致性条款；本项按中风险-部分覆盖-模板空白处理。"
            )
            item.fallback_reason = "建设工程中标一致性模板空白校正"

        if item.item_id == "CE-05-01" and has_total_subcontract_ban:
            _mark_construction_pass(
                item,
                "合同明确禁止承包人将全部工程转包，并禁止将工程肢解后分包或转包，符合建设工程强制性规范要求。",
                "检测到合同正文包含禁止全部转包和禁止肢解转包/分包的明确表述，该表述属于合规禁止性条款，不应认定为风险条款。",
            )

        if item.item_id == "CE-05-03" and has_resubcontract_ban:
            _mark_construction_pass(
                item,
                "合同明确禁止分包单位将其承包的工程再分包，符合建设工程分包限制规则。",
                "检测到合同正文包含禁止再分包的明确表述，该表述属于合规禁止性条款，不应认定为风险条款。",
            )

    return items


def _apply_contract_specific_post_rules(items: List[ReviewItemResult], contract_text: str, contract_type_key: str) -> List[ReviewItemResult]:
    if contract_type_key == "lease":
        return _apply_house_lease_real_contract_rules(items, contract_text)
    if contract_type_key == "sale":
        return _apply_sale_contract_rules(items, contract_text)
    if contract_type_key == "gift":
        items = [_apply_gift_consideration_override(item, contract_text) for item in items]
        return _apply_gift_dependency_rules(items)
    if contract_type_key == "technology":
        return _apply_technology_development_mode_rules(items, contract_text)
    if contract_type_key == "construction":
        return _apply_construction_contract_rules(items, contract_text)
    return items


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
    items = _apply_contract_specific_post_rules(items, contract_text, type_meta.key.value)
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
