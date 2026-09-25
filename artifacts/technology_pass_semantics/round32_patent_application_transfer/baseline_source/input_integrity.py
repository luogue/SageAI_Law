"""Input lineage diagnostics shared by the upload route and review engine.

The review pipeline must never silently replace a full contract with a field
summary, a truncated normalization result, or another request's text.  This
module keeps the checks independent from contract classification and rules.
"""

from __future__ import annotations

import hashlib
import re
from typing import Any, Dict, Iterable, Mapping, Optional


CRITICAL_CONTRACT_ANCHORS = (
    "专利技术",
    "许可方",
    "接受方",
    "非独占",
    "提成费",
    "专利资料",
    "中国国际经济贸易仲裁委员会",
    "不可抗力",
    "专利失效",
    "专利费用",
    "侵权",
)


def _sha256(text: str) -> str:
    return hashlib.sha256((text or "").encode("utf-8")).hexdigest()


def text_stage_snapshot(text: str, *, used: bool = True) -> Dict[str, Any]:
    value = text or ""
    nonempty_paragraphs = [
        paragraph.strip()
        for paragraph in re.split(r"(?:\r?\n\s*)+", value)
        if paragraph.strip()
    ]
    return {
        "character_count": len(value),
        "non_whitespace_character_count": len("".join(value.split())),
        "nonempty_paragraph_count": len(nonempty_paragraphs),
        "sha256": _sha256(value),
        "head_preview": value[:300],
        "tail_preview": value[-300:] if value else "",
        "used_by_stage": used,
    }


def _anchor_presence(text: str, anchors: Iterable[str]) -> Dict[str, bool]:
    return {anchor: anchor in (text or "") for anchor in anchors}


def build_input_integrity_diagnostics(
    *,
    extracted_text: str,
    normalized_text: str,
    classifier_input: str,
    rule_engine_input: str,
    clause_extraction_input: Optional[str] = None,
    search_audit_input: Optional[str] = None,
    clause_extraction_output: Optional[str] = None,
    source_diagnostics: Optional[Mapping[str, Any]] = None,
    downstream_used: bool = True,
) -> Dict[str, Any]:
    """Build a single trace for every text-bearing review stage.

    ``source_diagnostics`` may contain the private ``source_visible_text`` key
    produced by :class:`InputLayer`.  It is used for comparisons but is removed
    from the public/loggable diagnostics; only its length, hash and previews are
    exposed.
    """

    source = dict(source_diagnostics or {})
    source_visible_text = str(source.pop("source_visible_text", "") or "")
    clause_input = rule_engine_input if clause_extraction_input is None else clause_extraction_input
    audit_input = rule_engine_input if search_audit_input is None else search_audit_input
    stages = {
        "source_document": text_stage_snapshot(
            source_visible_text or extracted_text,
            used=True,
        ),
        "extracted_full_text": text_stage_snapshot(extracted_text, used=True),
        "normalized_full_text": text_stage_snapshot(normalized_text, used=True),
        "classifier_input": text_stage_snapshot(classifier_input, used=downstream_used),
        "clause_extraction_input": text_stage_snapshot(clause_input, used=downstream_used),
        "rule_engine_input": text_stage_snapshot(rule_engine_input, used=downstream_used),
        "search_audit_input": text_stage_snapshot(audit_input, used=downstream_used),
    }
    if clause_extraction_output is not None:
        stages["clause_extraction_output"] = text_stage_snapshot(
            clause_extraction_output,
            used=downstream_used,
        )
    stage_texts = {
        "source_document": source_visible_text or extracted_text,
        "extracted_full_text": extracted_text,
        "normalized_full_text": normalized_text,
        "classifier_input": classifier_input,
        "clause_extraction_input": clause_input,
        "rule_engine_input": rule_engine_input,
        "search_audit_input": audit_input,
    }
    if clause_extraction_output is not None:
        stage_texts["clause_extraction_output"] = clause_extraction_output
    anchor_matrix: Dict[str, Dict[str, bool]] = {
        anchor: {
            stage: anchor in text
            for stage, text in stage_texts.items()
        }
        for anchor in CRITICAL_CONTRACT_ANCHORS
    }

    failures = []
    for anchor, presence in anchor_matrix.items():
        if presence["source_document"] and not presence["extracted_full_text"]:
            failures.append({
                "code": "SOURCE_TO_EXTRACTION_ANCHOR_LOSS",
                "anchor": anchor,
                "stage": "document_extraction",
                "message": f"源文档存在锚点“{anchor}”，但提取后的完整文本中不存在。",
            })
        if presence["extracted_full_text"] and not presence["normalized_full_text"]:
            failures.append({
                "code": "NORMALIZATION_ANCHOR_LOSS",
                "anchor": anchor,
                "stage": "normalization",
                "message": f"提取文本存在锚点“{anchor}”，但归一化文本中不存在。",
            })
        downstream_anchor_checks = (
            ("classifier_input", "CLASSIFIER_INPUT_ANCHOR_LOSS", "classification", "分类器"),
            ("clause_extraction_input", "CLAUSE_EXTRACTION_INPUT_ANCHOR_LOSS", "clause_extraction", "条款抽取器"),
            ("rule_engine_input", "RULE_ENGINE_INPUT_ANCHOR_LOSS", "rule_engine", "规则引擎"),
            ("search_audit_input", "SEARCH_AUDIT_INPUT_ANCHOR_LOSS", "search_audit", "SEARCH_AUDIT"),
        )
        for stage_name, code, failure_stage, label in downstream_anchor_checks:
            if presence["extracted_full_text"] and not presence[stage_name]:
                failures.append({
                    "code": code,
                    "anchor": anchor,
                    "stage": failure_stage,
                    "message": f"提取文本存在锚点“{anchor}”，但{label}输入中不存在。",
                })

    def _compact_length(value: str) -> int:
        return len("".join((value or "").split()))

    def _retention(child: str, parent: str) -> float:
        parent_length = _compact_length(parent)
        if not parent_length:
            return 1.0
        return round(_compact_length(child) / parent_length, 6)

    # Anchor checks explain losses for known regression documents.  These
    # length/hash checks catch the same class of corruption for every contract,
    # including documents whose vocabulary is not present in the anchor list.
    source_basis = source_visible_text or extracted_text
    source_to_extracted_retention = _retention(extracted_text, source_basis)
    extracted_to_normalized_retention = _retention(normalized_text, extracted_text)
    if (
        source_visible_text
        and _compact_length(source_visible_text) >= 500
        and _compact_length(source_visible_text) - _compact_length(extracted_text) >= 300
        and source_to_extracted_retention < 0.8
    ):
        failures.append({
            "code": "DOCUMENT_EXTRACTION_TEXT_LOSS",
            "anchor": "",
            "stage": "document_extraction",
            "message": "源文档可见文本在文件解析阶段明显缩短，疑似表格、文本框、页眉页脚或嵌入正文未被完整提取。",
        })
    if (
        source_diagnostics
        and _compact_length(extracted_text) >= 800
        and _compact_length(extracted_text) - _compact_length(normalized_text) >= 500
        and extracted_to_normalized_retention < 0.65
    ):
        failures.append({
            "code": "NORMALIZATION_TEXT_LOSS",
            "anchor": "",
            "stage": "normalization",
            "message": "文件解析文本在 normalize/full_text 阶段明显缩短，疑似清洗或尾部识别错误。",
        })

    exact_downstream_stages = (
        ("classifier_input", classifier_input, "CLASSIFIER_INPUT_TEXT_MISMATCH", "classification"),
        ("clause_extraction_input", clause_input, "CLAUSE_EXTRACTION_INPUT_TEXT_MISMATCH", "clause_extraction"),
        ("rule_engine_input", rule_engine_input, "RULE_ENGINE_INPUT_TEXT_MISMATCH", "rule_engine"),
        ("search_audit_input", audit_input, "SEARCH_AUDIT_INPUT_TEXT_MISMATCH", "search_audit"),
    )
    for stage_name, value, code, failure_stage in exact_downstream_stages:
        if _sha256(value) != _sha256(normalized_text):
            failures.append({
                "code": code,
                "anchor": "",
                "stage": failure_stage,
                "message": f"{stage_name} 未使用同一份 normalized/full_text，疑似被摘要、结构化字段或错误 fallback 替换。",
            })

    clause_output_retention = None
    if clause_extraction_output is not None:
        clause_output_retention = _retention(clause_extraction_output, clause_input)
        if (
            _compact_length(clause_input) >= 1000
            and _compact_length(clause_input) - _compact_length(clause_extraction_output) >= 700
            and clause_output_retention < 0.5
        ):
            failures.append({
                "code": "CLAUSE_EXTRACTION_OUTPUT_TEXT_LOSS",
                "anchor": "",
                "stage": "clause_extraction",
                "message": "条款抽取结果仅保留了少量输入正文，疑似条款切分或文档结构识别发生大段漏读。",
            })

    completeness = dict(source.get("completeness") or {})
    if completeness.get("status") == "INCOMPLETE_INPUT":
        failures.append({
            "code": "SOURCE_DOCUMENT_FIELD_SUMMARY",
            "anchor": "",
            "stage": "document_source",
            "message": str(completeness.get("message") or "上传文件源包仅包含字段摘要或不完整正文。"),
        })
    elif completeness.get("status") == "EXTRACTION_SUSPECTED":
        failures.append({
            "code": "SOURCE_DOCUMENT_EXTRACTION_SUSPECTED",
            "anchor": "",
            "stage": "document_extraction",
            "message": str(completeness.get("message") or "源文件包含尚未成功提取的正文载体。"),
        })

    extracted_hash = stages["extracted_full_text"]["sha256"]
    normalized_hash = stages["normalized_full_text"]["sha256"]
    classifier_hash = stages["classifier_input"]["sha256"]
    clause_input_hash = stages["clause_extraction_input"]["sha256"]
    rule_hash = stages["rule_engine_input"]["sha256"]
    audit_hash = stages["search_audit_input"]["sha256"]
    return {
        "status": "BLOCKED" if failures else "PASS",
        "failure_count": len(failures),
        "failures": failures,
        "stages": stages,
        "anchor_matrix": anchor_matrix,
        "source_diagnostics": source,
        "lineage": {
            "source_to_extracted_retention": source_to_extracted_retention,
            "extracted_to_normalized_retention": extracted_to_normalized_retention,
            "clause_extraction_output_retention": clause_output_retention,
            "extracted_to_normalized_same_hash": extracted_hash == normalized_hash,
            "classifier_rule_same_hash": classifier_hash == rule_hash,
            "normalized_classifier_same_hash": normalized_hash == classifier_hash,
            "normalized_clause_extraction_same_hash": normalized_hash == clause_input_hash,
            "normalized_rule_engine_same_hash": normalized_hash == rule_hash,
            "normalized_search_audit_same_hash": normalized_hash == audit_hash,
            "single_full_text_source": (
                classifier_hash
                == clause_input_hash
                == rule_hash
                == audit_hash
                == normalized_hash
            ),
        },
    }


def log_input_integrity(
    logger: Any,
    diagnostics: Mapping[str, Any],
    *,
    trace_id: str = "",
    filename: str = "",
) -> None:
    """Write length/hash/head/tail evidence for every pipeline stage."""

    for stage, snapshot in (diagnostics.get("stages") or {}).items():
        logger.warning(
            "[REVIEW_INPUT_INTEGRITY] trace_id=%s filename=%s stage=%s used=%s "
            "chars=%s compact_chars=%s paragraphs=%s sha256=%s head=%r tail=%r",
            trace_id,
            filename,
            stage,
            snapshot.get("used_by_stage"),
            snapshot.get("character_count"),
            snapshot.get("non_whitespace_character_count"),
            snapshot.get("nonempty_paragraph_count"),
            snapshot.get("sha256"),
            snapshot.get("head_preview"),
            snapshot.get("tail_preview"),
        )
    logger.warning(
        "[REVIEW_INPUT_INTEGRITY_GATE] trace_id=%s filename=%s status=%s "
        "failures=%s anchors=%s lineage=%s",
        trace_id,
        filename,
        diagnostics.get("status"),
        diagnostics.get("failures") or [],
        diagnostics.get("anchor_matrix") or {},
        diagnostics.get("lineage") or {},
    )


def input_integrity_user_message(diagnostics: Mapping[str, Any]) -> str:
    """Return a stage-specific message without guessing that every failure is an upload defect."""

    codes = {
        str(row.get("code") or "")
        for row in diagnostics.get("failures") or []
    }
    if "SOURCE_DOCUMENT_FIELD_SUMMARY" in codes:
        return (
            "已核验本次上传文件的源文档内容：仅检测到字段摘要/填空页，源包中未发现连续合同正文；"
            "已停止生成报告。请确认所选文件本身包含完整条款和附件。"
        )
    if "SOURCE_DOCUMENT_EXTRACTION_SUSPECTED" in codes or "DOCUMENT_EXTRACTION_TEXT_LOSS" in codes:
        return (
            "源文件包含未被完整提取的正文载体，文件解析/OCR阶段疑似发生文本丢失；"
            "已停止生成报告，请转换为可提取文字的 DOCX 或 PDF 后重试。"
        )
    if "NORMALIZATION_TEXT_LOSS" in codes:
        return "完整正文在 normalize/full_text 阶段明显缩短，已按输入链路异常停止生成报告。"
    if any("INPUT_TEXT_MISMATCH" in code or "INPUT_ANCHOR_LOSS" in code for code in codes):
        return "完整正文在分类、条款抽取、规则引擎或 SEARCH_AUDIT 输入阶段发生不一致，已停止生成报告。"
    return "合同输入链路完整性校验未通过，已停止生成报告。"
