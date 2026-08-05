"""审查引擎第二版 API。

该路由独立于裁判引擎和旧版 LLM 合同审查主流程。
"""

from __future__ import annotations

import html
import io
import os
from datetime import datetime
from typing import Any, Dict, List
from urllib.parse import quote

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from fastapi.responses import StreamingResponse
from docx import Document as DocxDocument
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.shared import Pt
from pydantic import BaseModel, Field
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from auth.routes import get_current_user
from layers.input_layer import InputLayer
from review_v2.engine import COVERAGE_NOT_APPLICABLE, ISSUE_NOT_APPLICABLE, REPORT_FORMAT_NOTICE, review_contract_v2
from review_v2.llm_semantic_reviewer import get_llm_review_status
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
    has_blank_value,
)


router = APIRouter(prefix="/review-v2", tags=["contract_review_v2"])
input_layer = InputLayer()


class ReviewV2Input(BaseModel):
    contract_text: str = Field(..., min_length=1, description="合同文本")
    contract_type: str = Field("house_lease", description="合同类型，当前支持 house_lease、sale、gift、deposit、work_contract、transportation、agency、loan、service、guarantee、finance_lease、warehouse、construction、technology、commission_agency、utility_supply、brokerage")
    include_low_risk: bool = Field(True, description="是否返回低风险/已覆盖检查点")
    use_llm: bool = Field(True, description="是否启用大模型语义复核")


class ReviewV2Result(BaseModel):
    success: bool
    contract_type: str
    contract_type_name: str
    message: str
    items: List[Dict[str, Any]] = Field(default_factory=list)
    all_items_count: int = 0
    summary: Dict[str, int] = Field(default_factory=dict)
    coverage_summary: Dict[str, int] = Field(default_factory=dict)
    issue_type_summary: Dict[str, int] = Field(default_factory=dict)
    judge_source_summary: Dict[str, int] = Field(default_factory=dict)
    llm_enabled: bool = True
    llm_status: Dict[str, Any] = Field(default_factory=dict)
    global_fallback_reason: str = ""
    report_notice: str = ""
    result: str = ""
    filename: str = ""
    extracted_text_length: int = 0
    clause_count: int = 0
    formal_clause_count: int = 0


class ReviewV2PdfInput(BaseModel):
    filename: str = "合同审查报告"
    contract_type_name: str = "房屋租赁合同"
    summary: Dict[str, int] = Field(default_factory=dict)
    coverage_summary: Dict[str, int] = Field(default_factory=dict)
    issue_type_summary: Dict[str, int] = Field(default_factory=dict)
    judge_source_summary: Dict[str, int] = Field(default_factory=dict)
    llm_status: Dict[str, Any] = Field(default_factory=dict)
    global_fallback_reason: str = ""
    report_notice: str = ""
    items: List[Dict[str, Any]] = Field(default_factory=list)


class ReviewV2LlmStatus(BaseModel):
    enabled_by_env: bool
    has_model_key: bool
    available: bool
    configured_models: List[str] = Field(default_factory=list)
    priority: str = ""
    message: str = ""


def _register_cjk_font() -> str:
    candidates = [
        r"C:\Windows\Fonts\msyh.ttc",
        r"C:\Windows\Fonts\simhei.ttf",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
    ]
    for path in candidates:
        if os.path.exists(path):
            try:
                pdfmetrics.registerFont(TTFont("SageCJK", path))
                return "SageCJK"
            except Exception:
                continue
    return "Helvetica"


def _p(text: Any) -> str:
    return html.escape(str(text or "")).replace("\n", "<br/>")


def _item_evidence_text(item: Dict[str, Any]) -> str:
    return "\n".join(
        str(evidence.get("text") or "")
        for evidence in (item.get("evidence_clauses") or [])
        if isinstance(evidence, dict)
    )


def _item_issue_type(item: Dict[str, Any]) -> str:
    issue_type = str(item.get("issue_type") or "").strip()
    if issue_type:
        return issue_type

    coverage_status = str(item.get("coverage_status") or "").strip()
    evidence_text = _item_evidence_text(item)
    if coverage_status in {COVERAGE_PASS, COVERAGE_PARTIAL} and has_blank_value(evidence_text):
        return ISSUE_TEMPLATE_BLANK
    if coverage_status == COVERAGE_PASS:
        return ISSUE_PASS
    if coverage_status == COVERAGE_RISKY:
        return ISSUE_RISKY
    if coverage_status == COVERAGE_MISSING:
        return ISSUE_MISSING
    return ISSUE_CLAUSE_DEFECT


def _item_legal_consequence(item: Dict[str, Any]) -> str:
    return (
        str(item.get("legal_consequence_if_missing") or "").strip()
        or str(item.get("risk_point_description") or "").strip()
        or "未补全该审查点会增加合同履行和争议处理的不确定性，建议签署前补充明确约定。"
    )


def _issue_type_summary_from_items(items: List[Dict[str, Any]]) -> Dict[str, int]:
    summary = {
        ISSUE_PASS: 0,
        ISSUE_TEMPLATE_BLANK: 0,
        ISSUE_CLAUSE_DEFECT: 0,
        ISSUE_MISSING: 0,
        ISSUE_RISKY: 0,
        ISSUE_NOT_APPLICABLE: 0,
    }
    for item in items:
        issue_type = _item_issue_type(item)
        summary[issue_type] = summary.get(issue_type, 0) + 1
    return summary


def _build_pdf(payload: ReviewV2PdfInput) -> bytes:
    font_name = _register_cjk_font()
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=1.6 * cm,
        leftMargin=1.6 * cm,
        topMargin=1.6 * cm,
        bottomMargin=1.6 * cm,
    )

    styles = getSampleStyleSheet()
    base = ParagraphStyle(
        "SageBase",
        parent=styles["Normal"],
        fontName=font_name,
        fontSize=9,
        leading=14,
        alignment=TA_LEFT,
    )
    title = ParagraphStyle(
        "SageTitle",
        parent=base,
        fontSize=18,
        leading=24,
        spaceAfter=12,
    )
    heading = ParagraphStyle(
        "SageHeading",
        parent=base,
        fontSize=12,
        leading=18,
        spaceBefore=10,
        spaceAfter=6,
    )

    summary = payload.summary or {}
    coverage_summary = payload.coverage_summary or {}
    issue_type_summary = _issue_type_summary_from_items(payload.items)
    judge_source_summary = payload.judge_source_summary or {}
    story = [
        Paragraph("合同审查报告（第二版）", title),
        Paragraph(f"合同类型：{_p(payload.contract_type_name)}", base),
        Paragraph(f"文件名称：{_p(payload.filename)}", base),
        Paragraph(f"模型状态：{_p((payload.llm_status or {}).get('message') or '未记录')}", base),
        Paragraph(f"报告提示：{_p(payload.report_notice or REPORT_FORMAT_NOTICE)}", base),
        Paragraph(f"全局回退原因：{_p(payload.global_fallback_reason or '无')}", base),
        Paragraph(f"导出时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", base),
        Spacer(1, 10),
        Table(
            [
                ["高风险", "中风险", "低风险", "不适用", "审查项总数"],
                [
                    str(summary.get("高", 0)),
                    str(summary.get("中", 0)),
                    str(summary.get("低", 0)),
                    str(coverage_summary.get(COVERAGE_NOT_APPLICABLE, 0)),
                    str(len(payload.items)),
                ],
            ],
            colWidths=[3.2 * cm, 3.2 * cm, 3.2 * cm, 3.2 * cm, 3.2 * cm],
            style=TableStyle(
                [
                    ("FONTNAME", (0, 0), (-1, -1), font_name),
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#f3f6fb")),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#1f2937")),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#d8dee9")),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("TOPPADDING", (0, 0), (-1, -1), 8),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ]
            ),
        ),
        Spacer(1, 12),
    ]

    if coverage_summary:
        story.extend(
            [
                Paragraph("覆盖状态统计", heading),
                Table(
                    [
                        ["通过", "部分覆盖", "缺失", "风险条款", "不适用"],
                        [
                            str(coverage_summary.get("通过", 0)),
                            str(coverage_summary.get("部分覆盖", 0)),
                            str(coverage_summary.get("缺失", 0)),
                            str(coverage_summary.get("风险条款", 0)),
                            str(coverage_summary.get(COVERAGE_NOT_APPLICABLE, 0)),
                        ],
                    ],
                    colWidths=[3.2 * cm, 3.2 * cm, 3.2 * cm, 3.2 * cm, 3.2 * cm],
                    style=TableStyle(
                        [
                            ("FONTNAME", (0, 0), (-1, -1), font_name),
                            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#f3f6fb")),
                            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#d8dee9")),
                            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                            ("TOPPADDING", (0, 0), (-1, -1), 8),
                            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                        ]
                    ),
                ),
                Spacer(1, 12),
            ]
        )

    if judge_source_summary:
        story.extend(
            [
                Paragraph("判定来源统计", heading),
                Table(
                    [
                        ["大模型判定", "规则兜底"],
                        [
                            str(judge_source_summary.get("llm", 0)),
                            str(judge_source_summary.get("rule_fallback", 0)),
                        ],
                    ],
                    colWidths=[8 * cm, 8 * cm],
                    style=TableStyle(
                        [
                            ("FONTNAME", (0, 0), (-1, -1), font_name),
                            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#f3f6fb")),
                            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#d8dee9")),
                            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                            ("TOPPADDING", (0, 0), (-1, -1), 8),
                            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                        ]
                    ),
                ),
                Spacer(1, 12),
            ]
        )

    if issue_type_summary:
        story.extend(
            [
                Paragraph("问题类型统计", heading),
                Table(
                    [
                        ["通过", "模板空白", "条款缺陷", "完全缺失", "风险条款", "不适用"],
                        [
                            str(issue_type_summary.get("通过", 0)),
                            str(issue_type_summary.get("模板空白", 0)),
                            str(issue_type_summary.get("条款缺陷", 0)),
                            str(issue_type_summary.get("完全缺失", 0)),
                            str(issue_type_summary.get("风险条款", 0)),
                            str(issue_type_summary.get(ISSUE_NOT_APPLICABLE, 0)),
                        ],
                    ],
                    colWidths=[2.65 * cm, 2.65 * cm, 2.65 * cm, 2.65 * cm, 2.65 * cm, 2.65 * cm],
                    style=TableStyle(
                        [
                            ("FONTNAME", (0, 0), (-1, -1), font_name),
                            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#f3f6fb")),
                            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#d8dee9")),
                            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                            ("TOPPADDING", (0, 0), (-1, -1), 8),
                            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                        ]
                    ),
                ),
                Spacer(1, 12),
            ]
        )

    for index, item in enumerate(payload.items, start=1):
        issue_type = _item_issue_type(item)
        legal_consequence = _item_legal_consequence(item)
        story.extend(
            [
                Paragraph(f"{index}. {_p(item.get('title'))}（{_p(item.get('item_id'))}）", heading),
                Paragraph(
                    f"风险等级：{_p(item.get('risk_level'))}　"
                    f"覆盖状态：{_p(item.get('coverage_status'))}　"
                    f"问题类型：{_p(issue_type)}　"
                    f"复核状态：{_p(item.get('review_status') or '待处理')}",
                    base,
                ),
                Paragraph(
                    f"判定来源：{_p('大模型' if item.get('judge_source') == 'llm' else '规则兜底')}　"
                    f"模型置信度：{_p(item.get('llm_confidence') or '无')}",
                    base,
                ),
                Paragraph(f"回退原因：{_p(item.get('fallback_reason') or '无')}", base),
                Paragraph(f"原文位置：{_p(item.get('evidence_location') or '未召回正式条款')}", base),
                Paragraph(f"系统判断：{_p(item.get('reasoning_summary'))}", base),
                Paragraph(f"【风险点描述】：{_p(item.get('risk_point_description'))}", base),
                Paragraph(f"【缺失的法律后果】：{_p(legal_consequence)}", base),
                Paragraph(f"【建议条款示例】：{_p(item.get('suggested_clause_example'))}", base),
                Paragraph(f"【法律依据索引】：{_p(item.get('legal_basis_index'))}", base),
                Paragraph("命中原文：", base),
                *[
                    Paragraph(
                        f"{_p(evidence.get('location'))}：{_p(evidence.get('text'))}",
                        base,
                    )
                    for evidence in (item.get("evidence_clauses") or [])[:3]
                ],
                Paragraph(f"人工备注：{_p(item.get('reviewer_note'))}", base),
                Spacer(1, 8),
            ]
        )

    doc.build(story)
    return buffer.getvalue()


def _set_docx_run_font(run, *, bold: bool = False, size: int = 10) -> None:
    run.bold = bold
    run.font.name = "Microsoft YaHei"
    run.font.size = Pt(size)
    try:
        run._element.rPr.rFonts.set(qn("w:eastAsia"), "Microsoft YaHei")
    except Exception:
        pass


def _add_docx_line(doc: DocxDocument, label: str, value: Any = "", *, bold_label: bool = True) -> None:
    paragraph = doc.add_paragraph()
    label_run = paragraph.add_run(label)
    _set_docx_run_font(label_run, bold=bold_label)
    if value not in (None, ""):
        value_run = paragraph.add_run(str(value))
        _set_docx_run_font(value_run)


def _add_docx_table(doc: DocxDocument, headers: List[str], values: List[Any]) -> None:
    table = doc.add_table(rows=2, cols=len(headers))
    table.style = "Table Grid"
    for index, header in enumerate(headers):
        table.cell(0, index).text = header
        table.cell(1, index).text = str(values[index])


def _build_docx(payload: ReviewV2PdfInput) -> bytes:
    doc = DocxDocument()
    normal = doc.styles["Normal"]
    normal.font.name = "Microsoft YaHei"
    normal.font.size = Pt(10)

    title = doc.add_heading("合同审查报告（第二版）", level=1)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER

    _add_docx_line(doc, "合同类型：", payload.contract_type_name)
    _add_docx_line(doc, "文件名称：", payload.filename)
    _add_docx_line(doc, "模型状态：", (payload.llm_status or {}).get("message") or "未记录")
    _add_docx_line(doc, "报告提示：", payload.report_notice or REPORT_FORMAT_NOTICE)
    _add_docx_line(doc, "全局回退原因：", payload.global_fallback_reason or "无")
    _add_docx_line(doc, "导出时间：", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    summary = payload.summary or {}
    coverage_summary = payload.coverage_summary or {}
    _add_docx_table(
        doc,
        ["高风险", "中风险", "低风险", "不适用", "审查项总数"],
        [summary.get("高", 0), summary.get("中", 0), summary.get("低", 0), coverage_summary.get(COVERAGE_NOT_APPLICABLE, 0), len(payload.items)],
    )

    if coverage_summary:
        doc.add_heading("覆盖状态统计", level=2)
        _add_docx_table(
            doc,
            ["通过", "部分覆盖", "缺失", "风险条款", "不适用"],
            [
                coverage_summary.get("通过", 0),
                coverage_summary.get("部分覆盖", 0),
                coverage_summary.get("缺失", 0),
                coverage_summary.get("风险条款", 0),
                coverage_summary.get(COVERAGE_NOT_APPLICABLE, 0),
            ],
        )

    issue_type_summary = _issue_type_summary_from_items(payload.items)
    if issue_type_summary:
        doc.add_heading("问题类型统计", level=2)
        _add_docx_table(
            doc,
            ["通过", "模板空白", "条款缺陷", "完全缺失", "风险条款", "不适用"],
            [
                issue_type_summary.get("通过", 0),
                issue_type_summary.get("模板空白", 0),
                issue_type_summary.get("条款缺陷", 0),
                issue_type_summary.get("完全缺失", 0),
                issue_type_summary.get("风险条款", 0),
                issue_type_summary.get(ISSUE_NOT_APPLICABLE, 0),
            ],
        )

    for index, item in enumerate(payload.items, start=1):
        doc.add_heading(f"{index}. {item.get('title')}（{item.get('item_id')}）", level=2)
        issue_type = _item_issue_type(item)
        legal_consequence = _item_legal_consequence(item)
        source = "大模型判定" if item.get("judge_source") == "llm" else "规则兜底"

        _add_docx_line(
            doc,
            "基本信息：",
            f"风险等级：{item.get('risk_level') or ''}；覆盖状态：{item.get('coverage_status') or ''}；"
            f"问题类型：{issue_type}；复核状态：{item.get('review_status') or '待处理'}",
        )
        _add_docx_line(doc, "判定来源：", f"{source}；模型置信度：{item.get('llm_confidence') or '无'}")
        _add_docx_line(doc, "回退原因：", item.get("fallback_reason") or "无")
        _add_docx_line(doc, "原文位置：", item.get("evidence_location") or "未召回正式条款")
        _add_docx_line(doc, "系统判断：", item.get("reasoning_summary") or "")
        _add_docx_line(doc, "【风险点描述】：", item.get("risk_point_description") or "")
        _add_docx_line(doc, "【缺失的法律后果】：", legal_consequence)
        _add_docx_line(doc, "【建议条款示例】：", item.get("suggested_clause_example") or "")
        _add_docx_line(doc, "【法律依据索引】：", item.get("legal_basis_index") or "")

        evidences = item.get("evidence_clauses") or []
        _add_docx_line(doc, "命中原文：")
        if evidences:
            for evidence in evidences[:3]:
                _add_docx_line(doc, "", f"{evidence.get('location') or ''}：{evidence.get('text') or ''}", bold_label=False)
        else:
            _add_docx_line(doc, "", "无正式条款证据", bold_label=False)
        _add_docx_line(doc, "人工备注：", item.get("reviewer_note") or "")

    buffer = io.BytesIO()
    doc.save(buffer)
    return buffer.getvalue()


@router.get("/llm-status", response_model=ReviewV2LlmStatus, summary="合同审查第二版：大模型语义复核状态")
async def review_v2_llm_status(
    current_user: dict = Depends(get_current_user),
):
    """返回审查第二版当前是否可以调用大模型语义复核。"""

    return get_llm_review_status()


@router.post("/checklist", response_model=ReviewV2Result, summary="合同审查第二版：清单式审查")
async def review_v2_checklist(
    payload: ReviewV2Input,
    current_user: dict = Depends(get_current_user),
):
    """按文本运行独立审查引擎，供调试和后续批量迁移使用。"""

    return review_contract_v2(
        payload.contract_text,
        payload.contract_type,
        include_low_risk=payload.include_low_risk,
        use_llm=payload.use_llm,
    )


@router.post("/file", response_model=ReviewV2Result, summary="合同审查第二版：文件上传审查")
async def review_v2_file(
    file: UploadFile = File(...),
    contract_type: str = Form("house_lease"),
    include_low_risk: bool = Form(True),
    use_llm: bool = Form(True),
    current_user: dict = Depends(get_current_user),
):
    """接收 Word/PDF 合同文件，抽取文本后运行清单式审查。"""

    filename = file.filename or ""
    if not filename.lower().endswith((".doc", ".docx", ".pdf")):
        raise HTTPException(status_code=400, detail="审查第二版当前支持 .doc、.docx 和 .pdf 文件")

    try:
        contract_text = input_layer.extract_text_from_file(file)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"合同文本读取失败：{exc}") from exc

    result = review_contract_v2(
        contract_text,
        contract_type,
        include_low_risk=include_low_risk,
        use_llm=use_llm,
    )
    result["filename"] = filename
    result["extracted_text_length"] = len(contract_text)
    return result


@router.post("/export-pdf", summary="合同审查第二版：导出 PDF 报告")
async def review_v2_export_pdf(
    payload: ReviewV2PdfInput,
    current_user: dict = Depends(get_current_user),
):
    """将当前结构化审查报告导出为 PDF。"""

    content = _build_pdf(payload)
    base_name = (payload.filename or "合同审查报告").rsplit(".", 1)[0]
    download_name = f"{base_name}_审查第二版报告.pdf"
    encoded_name = quote(download_name)
    return StreamingResponse(
        io.BytesIO(content),
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename*=UTF-8''{encoded_name}"},
    )


@router.post("/export-docx", summary="合同审查第二版：导出 DOCX 报告")
async def review_v2_export_docx(
    payload: ReviewV2PdfInput,
    current_user: dict = Depends(get_current_user),
):
    """将当前结构化审查报告导出为 Word 文档。"""

    content = _build_docx(payload)
    base_name = (payload.filename or "合同审查报告").rsplit(".", 1)[0]
    download_name = f"{base_name}_审查第二版报告.docx"
    encoded_name = quote(download_name)
    return StreamingResponse(
        io.BytesIO(content),
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={"Content-Disposition": f"attachment; filename*=UTF-8''{encoded_name}"},
    )
