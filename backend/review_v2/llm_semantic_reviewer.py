"""LLM-backed semantic reviewer for contract review v2.

The model only classifies coverage and selects evidence from recalled clauses.
Risk descriptions, suggested clauses, and legal basis remain checklist-owned so
the review report stays deterministic and traceable.
"""

from __future__ import annotations

import json
import os
import re
from dataclasses import replace
from typing import Any, Dict, List, Sequence

from review_v2.clause_parser import ParsedClause
from review_v2.contract_facts import ContractFactGraph
from review_v2.house_lease_checklist import ReviewCheckpoint
from review_v2.semantic_reviewer import (
    COVERAGE_MISSING,
    COVERAGE_PARTIAL,
    COVERAGE_PASS,
    COVERAGE_RISKY,
    ISSUE_CLAUSE_DEFECT,
    ISSUE_MISSING,
    ISSUE_PASS,
    ISSUE_RISKY,
    ISSUE_TEMPLATE_BLANK,
    ReviewJudgment,
    _has_concrete_advance_notice,
    _has_complete_term_expiry_settlement,
    _has_expropriation_terms,
    _has_early_surrender_notice,
    _has_loss_based_adjustment,
    _has_notice_delivery_terms,
    _has_sale_delivery_complete_terms,
    _has_sale_delivery_transport_framework,
    _has_termination_notice_delivery,
    _has_third_party_defect_terms,
    has_blank_value,
    has_specific_deposit_return_deadline,
    evidence_substantively_matches,
    judge_checkpoint,
    recall_candidate_clauses,
)


VALID_COVERAGE = {COVERAGE_PASS, COVERAGE_PARTIAL, COVERAGE_MISSING, COVERAGE_RISKY}
VALID_RISK_LEVELS = {"高", "中", "低"}
VALID_CONFIDENCE = {"high", "medium", "low"}
VERDICT_WORDS = (
    "判决结果",
    "判决",
    "裁判结论",
    "驳回请求",
    "押金全额返还",
    "扣除维修费后返还余额",
    "应赔偿",
    "应承担赔偿责任",
)

SPECIALIZED_PASS_REQUIREMENTS = {
    "lessor_death": (
        ("出租人死亡", "出租方死亡", "继承人", "受让人", "权利继受", "权利转移", "所有权变动", "房屋转让"),
        ("继续履行", "承继", "接收租金", "履行出租人义务", "维修义务", "通知义务"),
    ),
    "tenant_death_successor": (
        ("承租人死亡", "承租方死亡", "共同居住人", "共同经营人"),
        ("继续承租", "继续履行", "接替履行", "按原合同履行"),
    ),
    "tenant_death_settlement": (
        ("承租人死亡", "无人继续承租", "继承人", "遗产管理人"),
        ("交接", "结算", "遗留物", "押金", "费用"),
    ),
    "changed_circumstances": (
        ("情势变更", "无法预见", "非商业风险", "显失公平", "政策突变", "疫情", "封控"),
        ("协商", "减租", "延租", "变更", "解除"),
    ),
    "lease_before_sale": (
        ("房屋出售", "房屋转让", "所有权变动", "受让人", "新房主"),
        ("不影响", "继续履行", "承继", "押金交接", "义务"),
    ),
    "sale_notice_preemption": (
        ("出售", "转让", "优先购买权", "同等条件"),
        ("通知", "提前通知", "合理期限"),
    ),
    "expropriation_demolition": (
        ("征收", "拆迁", "腾退", "强制处置"),
        ("结算", "补偿", "押金", "租金", "终止"),
    ),
}


class LLMReviewError(Exception):
    """Raised when model output cannot be safely used."""


def llm_review_enabled() -> bool:
    return os.getenv("REVIEW_V2_LLM_ENABLED", "true").lower() in {"1", "true", "yes", "on"}


def _max_candidates() -> int:
    try:
        return max(1, min(12, int(os.getenv("REVIEW_V2_LLM_MAX_CANDIDATES", "4"))))
    except ValueError:
        return 4


def _max_retries() -> int:
    try:
        return max(1, min(3, int(os.getenv("REVIEW_V2_LLM_MAX_RETRIES", "1"))))
    except ValueError:
        return 1


def _batch_size() -> int:
    try:
        return max(1, min(20, int(os.getenv("REVIEW_V2_LLM_BATCH_SIZE", "8"))))
    except ValueError:
        return 8


def _has_configured_model() -> bool:
    return any(
        os.getenv(key, "").strip()
        for key in ("DASHSCOPE_API_KEY", "ARK_API_KEY", "DEEPSEEK_API_KEY")
    )


def get_llm_review_status() -> Dict[str, Any]:
    enabled_by_env = llm_review_enabled()
    configured_models = []
    if os.getenv("DASHSCOPE_API_KEY", "").strip():
        configured_models.append("qwen")
    if os.getenv("ARK_API_KEY", "").strip():
        configured_models.append("doubao")
    if os.getenv("DEEPSEEK_API_KEY", "").strip():
        configured_models.append("deepseek")

    if not enabled_by_env:
        message = "服务器已关闭大模型语义复核，当前仅使用规则兜底。"
    elif not configured_models:
        message = "服务器未配置模型 API Key，当前仅使用规则兜底。"
    else:
        message = "AI语义审查已完成。"

    return {
        "enabled_by_env": enabled_by_env,
        "has_model_key": bool(configured_models),
        "available": enabled_by_env and bool(configured_models),
        "configured_models": configured_models,
        "priority": os.getenv("LLM_PRIORITY", "doubao,qwen,deepseek"),
        "message": message,
    }


def _fallback(rule_judgment: ReviewJudgment, reason: str) -> ReviewJudgment:
    return replace(
        rule_judgment,
        judge_source="rule_fallback",
        llm_confidence="",
        llm_raw_reason="",
        fallback_reason=reason,
    )


def _safe_text(text: str, limit: int = 900) -> str:
    cleaned = re.sub(r"\s+", " ", text or "").strip()
    return cleaned[:limit]


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


def _extract_json(raw_output: str) -> Dict[str, Any]:
    text = (raw_output or "").strip()
    if not text:
        raise LLMReviewError("模型返回为空")
    fence_match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
    if fence_match:
        text = fence_match.group(1)
    elif "{" in text and "}" in text:
        text = text[text.find("{"): text.rfind("}") + 1]
    try:
        result = json.loads(text)
    except json.JSONDecodeError as exc:
        raise LLMReviewError(f"模型返回不是合法 JSON: {exc}") from exc
    if not isinstance(result, dict):
        raise LLMReviewError("模型 JSON 顶层不是对象")
    return result


def _contains_verdict_language(*values: Any) -> bool:
    joined = "\n".join(str(value or "") for value in values)
    return any(word in joined for word in VERDICT_WORDS)


def _has_specialized_pass_evidence(checkpoint: ReviewCheckpoint, clauses: Sequence[ParsedClause]) -> bool:
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

    requirements = SPECIALIZED_PASS_REQUIREMENTS.get(checkpoint.node_id)
    if not requirements:
        return True
    return all(any(term in joined for term in group) for group in requirements)


def _specialized_requirement_hint(checkpoint: ReviewCheckpoint) -> str:
    if checkpoint.node_id == "proper_party":
        return "；并且不能只出现出租人/承租人或原告/被告角色，必须有证件号、住所、联系方式或统一社会信用代码等可识别主体信息"
    if checkpoint.node_id == "deposit_return_deadline":
        return "；并且必须写明押金返还的具体天数、工作日或明确期限，不能只写“结清费用后返还”"
    if checkpoint.node_id == "utilities_fees":
        return "；并且必须具体写明水费、电费、燃气费、物业费、网络费等费用的承担或结清方式，不能只写“各项费用”"
    if checkpoint.node_id == "limitation_and_notice":
        return "；并且必须直接约定送达地址、通讯方式、催告留痕或联系方式变更后果，不能用提前解除通知条款替代"
    if checkpoint.node_id == "termination_notice":
        return "；并且必须区分提前退租通知和解除通知送达：提前退租通知用于启动解除程序，解除通知送达用于使解除行为生效；完整通过必须写明解除通知的送达方式、送达地址和通知到达后的生效时间"
    if checkpoint.node_id == "indefinite_lease":
        return "；并且必须直接约定期满后继续使用、出租人继续收租或未异议、双方未续签时转为不定期租赁及提前通知期限，不能用一般期满搬离交房条款替代"
    if checkpoint.node_id == "unauthorized_sublease":
        return "；并且必须直接约定转租、转借或交由他人使用的限制及后果，不能用一般解除条款替代"
    if checkpoint.node_id == "expropriation_demolition":
        return "；并且必须直接出现征收、拆迁、腾退或强制处置等场景，不能用一般合同终止条款替代"
    if checkpoint.node_id == "maintenance_duty":
        return "；并且必须区分出租人维修义务的范围，不能只写承租人使用不当时自行维修或赔偿"
    if checkpoint.node_id == "deposit_offset_order":
        return "；并且必须写明押金抵扣的先后顺序和款项类别，不能只泛称结清各项费用"
    if checkpoint.node_id == "third_party_tort":
        return "；并且必须直接约定第三方、邻居、楼上、物业原因等非合同相对方造成损害时的证据保全、协助追偿或责任方处理，不能用水电物业费承担条款替代"
    if checkpoint.node_id == "third_party_defect":
        return "；并且必须直接约定楼上住户、物业、公共管线或其他第三方原因影响使用时的通知、取证、维修、追偿或租金调整，不能用水电物业费承担条款替代"
    if checkpoint.node_id == "term_expiry_settlement":
        return "；押金条款中写明合同终止时结清费用可作为部分覆盖证据，但完整通过还必须同时约定租期届满或解除后的交房、查验和结算清单机制，不能用一般违约责任条款替代"
    if checkpoint.node_id == "early_surrender":
        return "；并且必须直接约定提前退租或提前解除、具体提前通知期限，以及按实际使用期间、未结费用或实际损失结算，不能把空白的提前通知天数或违约金标准视为通过"
    if checkpoint.node_id == "excessive_deduction":
        return "；并且必须直接约定扣款、违约金或赔偿以实际损失为基础，且明显过高时可调减或调整，不能把空白违约金标准视为通过"
    if checkpoint.node_id == "sale_delivery_method":
        return "；已有运输方式只能部分覆盖，完整通过必须同时写明交付或运输方式，以及签收单、送货单、物流回执、授权收货人等签收手续，不能仅凭“由甲方负责运输”判为通过"

    requirements = SPECIALIZED_PASS_REQUIREMENTS.get(checkpoint.node_id)
    if not requirements:
        return ""
    groups = ["、".join(group) for group in requirements]
    return "；且必须分别命中这些核心要素：" + " / ".join(groups)


def _validate_model_result(result: Dict[str, Any], candidates: Sequence[ParsedClause]) -> Dict[str, Any]:
    coverage_status = str(result.get("coverage_status", "")).strip()
    risk_level = str(result.get("risk_level", "")).strip()
    reasoning_summary = str(result.get("reasoning_summary", "")).strip()
    confidence = str(result.get("confidence", "medium")).strip().lower()
    evidence_ids = result.get("evidence_clause_ids", [])
    needs_human_review = bool(result.get("needs_manual_review_candidate", result.get("needs_human_review", False)))

    if coverage_status not in VALID_COVERAGE:
        raise LLMReviewError(f"模型 coverage_status 非法: {coverage_status}")
    if risk_level not in VALID_RISK_LEVELS:
        raise LLMReviewError(f"模型 risk_level 非法: {risk_level}")
    if confidence not in VALID_CONFIDENCE:
        confidence = "medium"
    if not isinstance(evidence_ids, list):
        raise LLMReviewError("模型 evidence_clause_ids 不是数组")
    if not reasoning_summary:
        raise LLMReviewError("模型 reasoning_summary 为空")
    if _contains_verdict_language(reasoning_summary):
        raise LLMReviewError("模型输出包含裁判式表述")

    candidate_ids = {clause.clause_id for clause in candidates}
    selected_ids = [str(item) for item in evidence_ids if str(item) in candidate_ids]
    if evidence_ids and len(selected_ids) != len(evidence_ids):
        raise LLMReviewError("模型引用了候选范围外的证据 ID")

    return {
        "coverage_status": coverage_status,
        "risk_level": risk_level,
        "reasoning_summary": reasoning_summary,
        "confidence": confidence,
        "evidence_clause_ids": selected_ids,
        "needs_human_review": needs_human_review,
    }


def _build_prompt(
    checkpoint: ReviewCheckpoint,
    candidates: Sequence[ParsedClause],
    rule_judgment: ReviewJudgment,
) -> str:
    candidate_payload = [
        {
            "clause_id": clause.clause_id,
            "location": clause.location,
            "section_type": clause.section_type,
            "text": _safe_text(clause.text),
        }
        for clause in candidates
    ]
    return f"""
你是合同风险审查专家。请只判断合同条款是否实质覆盖审查点，不要输出判决结果，不要判断谁胜诉，不要说任何一方应赔偿。reasoning_summary 禁止写“建议人工复核”“需要人工复核”等行动结论；是否复核只通过 needs_manual_review_candidate 结构化字段表达。

审查点：
- 编号：{checkpoint.item_id}
- 标题：{checkpoint.title}
- 类型：{checkpoint.kind}
- 语义问题：{checkpoint.semantic_question}
- 通过标准：{checkpoint.pass_criteria}{_specialized_requirement_hint(checkpoint)}
- 部分覆盖标准：{checkpoint.partial_criteria}
- 法律依据索引：{checkpoint.legal_basis}

候选原文条款 JSON：
{json.dumps(candidate_payload, ensure_ascii=False)}

规则初判：
{json.dumps({
    "coverage_status": rule_judgment.coverage_status,
    "risk_level": rule_judgment.risk_level,
    "reasoning_summary": rule_judgment.reasoning_summary,
}, ensure_ascii=False)}

请输出严格 JSON，不要输出 JSON 以外的文字：
{{
  "coverage_status": "通过|部分覆盖|缺失|风险条款",
  "risk_level": "高|中|低",
  "reasoning_summary": "一句话说明为什么该条款通过、部分覆盖、缺失或属于风险条款；只能写风险审查语言，不能写判决结果",
  "evidence_clause_ids": ["只能填候选原文条款中的 clause_id；没有证据时填空数组"],
  "confidence": "high|medium|low",
  "needs_manual_review_candidate": false,
  "manual_review_reason": null
}}
""".strip()


def _build_batch_prompt(entries: Sequence[Dict[str, Any]]) -> str:
    checkpoint_payload = []
    for entry in entries:
        checkpoint: ReviewCheckpoint = entry["checkpoint"]
        candidates: Sequence[ParsedClause] = entry["candidates"]
        rule_judgment: ReviewJudgment = entry["rule_judgment"]
        checkpoint_payload.append(
            {
                "item_id": checkpoint.item_id,
                "title": checkpoint.title,
                "kind": checkpoint.kind,
                "semantic_question": checkpoint.semantic_question,
                "pass_criteria": checkpoint.pass_criteria,
                "strict_pass_hint": _specialized_requirement_hint(checkpoint),
                "partial_criteria": checkpoint.partial_criteria,
                "legal_basis": checkpoint.legal_basis,
                "candidate_clauses": [
                    {
                        "clause_id": clause.clause_id,
                        "location": clause.location,
                        "section_type": clause.section_type,
                        "block_type": clause.block_type,
                        "text": _safe_text(clause.text),
                    }
                    for clause in candidates
                ],
                "rule_judgment": {
                    "coverage_status": rule_judgment.coverage_status,
                    "risk_level": rule_judgment.risk_level,
                    "reasoning_summary": rule_judgment.reasoning_summary,
                },
            }
        )

    return f"""
你是合同风险审查专家。请批量判断多个审查点是否被候选合同条款实质覆盖。

硬性要求：
- 只做合同审查，不要输出判决结果，不要判断谁胜诉，不要说任何一方应赔偿。
- 每个审查点必须返回一条 review。
- evidence_clause_ids 只能引用该审查点 candidate_clauses 中的 clause_id。
- reasoning_summary 只能写风险审查理由，不能写裁判结论。
- reasoning_summary 禁止写“建议人工复核”“需要人工复核”等行动结论；是否复核只通过 needs_manual_review_candidate 结构化字段表达。
- 不能用一般违约责任、通知送达、解除、继续履行等泛化条款替代专项审查点；只有候选条款直接覆盖该审查点的核心事实和处理安排，才能判为“通过”。

审查点和候选条款 JSON：
{json.dumps(checkpoint_payload, ensure_ascii=False)}

请输出严格 JSON，不要输出 JSON 以外的文字：
{{
  "reviews": [
    {{
      "item_id": "审查点编号",
      "coverage_status": "通过|部分覆盖|缺失|风险条款",
      "risk_level": "高|中|低",
      "reasoning_summary": "一句话说明为什么该条款通过、部分覆盖、缺失或属于风险条款",
      "evidence_clause_ids": ["只能填该审查点候选原文条款中的 clause_id；没有证据时填空数组"],
      "confidence": "high|medium|low",
      "needs_manual_review_candidate": false,
      "manual_review_reason": null
    }}
  ]
}}
""".strip()


def _status_for(checkpoint: ReviewCheckpoint, coverage_status: str) -> str:
    if coverage_status == COVERAGE_PASS:
        return "未发现明显风险条款" if checkpoint.kind == "forbidden" else "已覆盖"
    if coverage_status == COVERAGE_PARTIAL:
        return "部分覆盖，需补充填写"
    if coverage_status == COVERAGE_RISKY:
        return "发现风险条款"
    return "缺失或不明确"


def _risk_description_for(checkpoint: ReviewCheckpoint, coverage_status: str) -> str:
    if coverage_status == COVERAGE_PASS:
        return checkpoint.risk_point_missing if checkpoint.kind == "forbidden" else checkpoint.risk_point_present
    if coverage_status == COVERAGE_PARTIAL:
        return f"合同已出现“{checkpoint.title}”相关条款，但尚未完整覆盖该审查点，签署前需要补充或细化。"
    return checkpoint.risk_point_present if checkpoint.kind == "forbidden" and coverage_status == COVERAGE_RISKY else checkpoint.risk_point_missing


def _issue_type_for(coverage_status: str, clauses: Sequence[ParsedClause]) -> str:
    if coverage_status in {COVERAGE_PASS, COVERAGE_PARTIAL} and any(has_blank_value(clause.text) for clause in clauses):
        return ISSUE_TEMPLATE_BLANK
    if coverage_status == COVERAGE_PASS:
        return ISSUE_PASS
    if coverage_status == COVERAGE_RISKY:
        return ISSUE_RISKY
    if coverage_status == COVERAGE_MISSING:
        return ISSUE_MISSING
    return ISSUE_CLAUSE_DEFECT


def _risk_level_for(checkpoint: ReviewCheckpoint, coverage_status: str) -> str:
    if coverage_status == COVERAGE_PASS:
        return "低"
    if checkpoint.node_id == "deposit_return_deadline" and coverage_status == COVERAGE_PARTIAL:
        return "中"
    return checkpoint.risk_level


def _judgment_from_model_result(
    checkpoint: ReviewCheckpoint,
    candidates: Sequence[ParsedClause],
    terms: Sequence[str],
    model_result: Dict[str, Any],
) -> ReviewJudgment:
    selected_ids = set(model_result["evidence_clause_ids"])
    selected_clauses = [clause for clause in candidates if clause.clause_id in selected_ids]
    if model_result["coverage_status"] != COVERAGE_MISSING and not selected_clauses:
        selected_clauses = list(candidates)

    reasoning_summary = model_result["reasoning_summary"]
    coverage_status = model_result["coverage_status"]
    confidence = model_result["confidence"]

    if coverage_status == COVERAGE_PASS and any(has_blank_value(clause.text) for clause in selected_clauses):
        coverage_status = COVERAGE_PARTIAL
        confidence = "low"
        reasoning_summary = (
            f"命中条款存在空白、未勾选或关键金额、期限未填写，属于“{checkpoint.title}”的模板空白，"
            "不能视为完整通过。建议签署前补全具体内容。"
        )

    if coverage_status == COVERAGE_PASS and not _has_specialized_pass_evidence(checkpoint, selected_clauses):
        coverage_status = COVERAGE_PARTIAL
        confidence = "low"
        if checkpoint.node_id == "sale_delivery_method" and _has_sale_delivery_transport_framework("\n".join(clause.text for clause in selected_clauses)):
            reasoning_summary = (
                "合同已约定运输方式，但未写明签收手续、授权收货人或送货单、签收单、物流回执等交付凭证，"
                "属于模板框架已写但关键手续未补全。"
            )
        elif checkpoint.node_id == "termination_notice" and _has_early_surrender_notice("\n".join(clause.text for clause in selected_clauses)):
            reasoning_summary = (
                "合同约定了提前退租的书面通知，但未约定解除通知的送达方式、送达地址和生效时间。"
                "二者法律功能不同，前者启动解除程序，后者使解除行为生效。"
            )
        else:
            reasoning_summary = (
                f"候选条款仅包含一般性表述，未直接覆盖“{checkpoint.title}”的核心事实和处理安排，"
                "不能视为完整通过。建议签署前补充更具体的约定。"
            )

    if coverage_status in {COVERAGE_PASS, COVERAGE_PARTIAL} and not evidence_substantively_matches(checkpoint, selected_clauses):
        coverage_status = COVERAGE_MISSING
        confidence = "low"
        selected_clauses = []
        reasoning_summary = "未在正式合同条款中找到能覆盖该审查点的有效约定。"

    selected_text = "\n".join(clause.text for clause in selected_clauses)
    if checkpoint.node_id == "indefinite_lease" and coverage_status == COVERAGE_MISSING:
        reasoning_summary = (
            "根据《民法典》第734条，租赁期满后双方未续签合同但继续履行租约的，原合同继续有效，"
            "租赁期限转为不定期；出租人解除合同需提前合理期限通知。对简化版居住租赁合同而言，"
            "该条款属于建议性补充条款，并非必须条款。"
        )
    if checkpoint.node_id == "termination_notice" and coverage_status == COVERAGE_PARTIAL and _has_early_surrender_notice(selected_text) and not _has_termination_notice_delivery(selected_text):
        reasoning_summary = (
            "合同约定了提前退租的书面通知，但未约定解除通知的送达方式、送达地址和生效时间。"
            "二者法律功能不同，前者启动解除程序，后者使解除行为生效。"
        )
    if checkpoint.node_id == "early_surrender" and coverage_status == COVERAGE_PARTIAL and any(has_blank_value(clause.text) for clause in selected_clauses):
        reasoning_summary = (
            "提前退租条款已被召回，但通知期限或违约金比例存在模板空白；违约金还应与实际损失、"
            "合理空置损失或未结费用挂钩，避免固定高额约定被调减。"
        )

    return ReviewJudgment(
        coverage_status=coverage_status,
        risk_level=_risk_level_for(checkpoint, coverage_status),
        status=_status_for(checkpoint, coverage_status),
        risk_point_description=_risk_description_for(checkpoint, coverage_status),
        evidence_clauses=_public_evidence(selected_clauses),
        evidence_location=_locations(selected_clauses),
        reasoning_summary=reasoning_summary,
        matched_terms=list(terms),
        issue_type=(
            ISSUE_TEMPLATE_BLANK
            if checkpoint.node_id == "sale_delivery_method"
            and coverage_status == COVERAGE_PARTIAL
            and _has_sale_delivery_transport_framework("\n".join(clause.text for clause in selected_clauses))
            and not _has_sale_delivery_complete_terms("\n".join(clause.text for clause in selected_clauses))
            else _issue_type_for(coverage_status, selected_clauses)
        ),
        judge_source="llm",
        llm_confidence=confidence,
        llm_raw_reason=model_result["reasoning_summary"],
        fallback_reason="",
    )


def judge_checkpoint_with_llm(
    checkpoint: ReviewCheckpoint,
    clauses: Sequence[ParsedClause],
    *,
    use_llm: bool = True,
    fact_graph: ContractFactGraph | None = None,
) -> ReviewJudgment:
    rule_judgment = judge_checkpoint(checkpoint, clauses, fact_graph=fact_graph)
    if not use_llm:
        return _fallback(rule_judgment, "本次审查未启用大模型语义复核，使用规则判定")
    if not llm_review_enabled():
        return _fallback(rule_judgment, "REVIEW_V2_LLM_ENABLED 已关闭，使用规则判定")
    if not _has_configured_model():
        return _fallback(rule_judgment, "未配置可用模型 API Key，使用规则判定")

    candidates, terms = recall_candidate_clauses(checkpoint, clauses, fact_graph=fact_graph, max_candidates=_max_candidates())
    if not candidates:
        return _fallback(rule_judgment, "未召回候选正式条款，使用规则判定")

    try:
        from reasoning.llm_client import call_llm

        prompt = _build_prompt(checkpoint, candidates, rule_judgment)
        raw_output = call_llm(prompt, response_format="json", max_retries=_max_retries())
        model_result = _validate_model_result(_extract_json(raw_output), candidates)
    except Exception as exc:
        return _fallback(rule_judgment, f"模型判定不可用，已回退规则判定：{exc}")

    return _judgment_from_model_result(checkpoint, candidates, terms, model_result)


def judge_checkpoints_with_llm(
    checkpoints: Sequence[ReviewCheckpoint],
    clauses: Sequence[ParsedClause],
    *,
    use_llm: bool = True,
    fact_graph: ContractFactGraph | None = None,
) -> Dict[str, ReviewJudgment]:
    rule_entries: List[Dict[str, Any]] = []
    results: Dict[str, ReviewJudgment] = {}

    for checkpoint in checkpoints:
        rule_judgment = judge_checkpoint(checkpoint, clauses, fact_graph=fact_graph)
        if not use_llm:
            results[checkpoint.item_id] = _fallback(rule_judgment, "本次审查未启用大模型语义复核，使用规则判定")
            continue
        if not llm_review_enabled():
            results[checkpoint.item_id] = _fallback(rule_judgment, "REVIEW_V2_LLM_ENABLED 已关闭，使用规则判定")
            continue
        if not _has_configured_model():
            results[checkpoint.item_id] = _fallback(rule_judgment, "未配置可用模型 API Key，使用规则判定")
            continue

        candidates, terms = recall_candidate_clauses(checkpoint, clauses, fact_graph=fact_graph, max_candidates=_max_candidates())
        if not candidates:
            results[checkpoint.item_id] = _fallback(rule_judgment, "未召回候选正式条款，使用规则判定")
            continue

        rule_entries.append(
            {
                "checkpoint": checkpoint,
                "rule_judgment": rule_judgment,
                "candidates": candidates,
                "terms": terms,
            }
        )

    if not rule_entries:
        return results

    try:
        from reasoning.llm_client import call_llm
    except Exception as exc:
        for entry in rule_entries:
            checkpoint = entry["checkpoint"]
            results[checkpoint.item_id] = _fallback(entry["rule_judgment"], f"模型判定不可用，已回退规则判定：{exc}")
        return results

    for start in range(0, len(rule_entries), _batch_size()):
        batch = rule_entries[start:start + _batch_size()]
        try:
            raw_output = call_llm(_build_batch_prompt(batch), response_format="json", max_retries=_max_retries())
            parsed = _extract_json(raw_output)
            reviews = parsed.get("reviews")
            if not isinstance(reviews, list):
                raise LLMReviewError("批量模型返回缺少 reviews 数组")
        except Exception as exc:
            for entry in batch:
                checkpoint = entry["checkpoint"]
                results[checkpoint.item_id] = _fallback(entry["rule_judgment"], f"批量模型判定不可用，已回退规则判定：{exc}")
            continue

        reviews_by_id = {
            str(review.get("item_id")): review
            for review in reviews
            if isinstance(review, dict) and review.get("item_id")
        }
        for entry in batch:
            checkpoint = entry["checkpoint"]
            review = reviews_by_id.get(checkpoint.item_id)
            if not review:
                results[checkpoint.item_id] = _fallback(entry["rule_judgment"], "批量模型未返回该审查点，使用规则判定")
                continue
            try:
                model_result = _validate_model_result(review, entry["candidates"])
                results[checkpoint.item_id] = _judgment_from_model_result(
                    checkpoint,
                    entry["candidates"],
                    entry["terms"],
                    model_result,
                )
            except Exception as exc:
                results[checkpoint.item_id] = _fallback(entry["rule_judgment"], f"批量模型该项输出不可用，已回退规则判定：{exc}")

    return results
