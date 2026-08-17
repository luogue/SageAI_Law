"""Clause parser for contract review v2.

The parser keeps source text traceable by splitting uploaded contracts into
clauses and marking whether a clause is a formal contract term, usage
instruction, special notice, or appendix.
"""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional

from review_v2.template_parser import parse_option_groups


SECTION_USAGE = "使用说明"
SECTION_SPECIAL_NOTICE = "特别提示"
SECTION_FORMAL = "正式合同条款"
SECTION_APPENDIX = "附件"
SECTION_COMMENTARY = "说明评论"
SECTION_HISTORICAL_NOTE = "历史说明"

BLOCK_OPERATIVE = "OPERATIVE_CLAUSE"
BLOCK_PARTY_INFORMATION = "PARTY_INFORMATION"
BLOCK_SIGNATURE = "SIGNATURE_BLOCK"
BLOCK_TEMPLATE_GUIDANCE = "TEMPLATE_GUIDANCE"
BLOCK_TEMPLATE_INSTRUCTION = BLOCK_TEMPLATE_GUIDANCE
BLOCK_COMMENTARY = "COMMENTARY"
BLOCK_HISTORICAL_NOTE = "HISTORICAL_NOTE"
BLOCK_ANNEX = "ANNEX"


class DocumentBlockType(str):
    """Canonical block type with compatibility for the pre-6.4 template name."""

    def __eq__(self, other: object) -> bool:
        if str(self) == BLOCK_TEMPLATE_GUIDANCE and other == "TEMPLATE_INSTRUCTION":
            return True
        return str.__eq__(self, other)

    def __hash__(self) -> int:
        return str.__hash__(self)


@dataclass(frozen=True)
class ParsedClause:
    clause_id: str
    location: str
    title: str
    text: str
    section_type: str
    level: int
    raw_text: str = ""
    normalized_text: str = ""
    option_groups: List[Dict[str, Any]] = field(default_factory=list)
    source: str = "body"
    section_path: List[str] = field(default_factory=list)
    heading: str = ""
    clause_number: str = ""
    paragraph_index: int = 0
    block_type: str = BLOCK_OPERATIVE
    parties: List[str] = field(default_factory=list)
    dates: List[str] = field(default_factory=list)
    amounts: List[str] = field(default_factory=list)
    percentages: List[str] = field(default_factory=list)
    durations: List[str] = field(default_factory=list)
    cross_references: List[str] = field(default_factory=list)

    def to_public_dict(self) -> Dict[str, str | int]:
        return asdict(self)


@dataclass(frozen=True)
class DocumentIntegrity:
    source_length: int
    normalized_length: int
    paragraph_count: int
    clause_count: int
    heading_count: int
    first_clause: str
    last_clause: str
    parsed_character_ratio: float
    skipped_ranges: List[Dict[str, int]] = field(default_factory=list)
    truncated: bool = False

    def to_public_dict(self) -> Dict[str, Any]:
        return asdict(self)


def _clause_source(section_type: str, text: str = "") -> str:
    if section_type == SECTION_APPENDIX:
        return "appendix"
    if section_type == SECTION_USAGE:
        return "usage"
    if section_type == SECTION_SPECIAL_NOTICE:
        return "special_notice"
    compacted = re.sub(r"\s+", "", text or "")
    if re.search(r"(甲方|乙方|出租方|承租方).{0,16}(签字|签名|盖章)", compacted):
        return "signature"
    if text.startswith(("甲方（", "乙方（", "甲方(", "乙方(", "出租方", "承租方")):
        return "party_info"
    return "body"


def _block_type(section_type: str, source: str) -> str:
    if section_type in {SECTION_USAGE, SECTION_SPECIAL_NOTICE}:
        return DocumentBlockType(BLOCK_TEMPLATE_GUIDANCE)
    if section_type == SECTION_COMMENTARY:
        return BLOCK_COMMENTARY
    if section_type == SECTION_HISTORICAL_NOTE:
        return BLOCK_HISTORICAL_NOTE
    if section_type == SECTION_APPENDIX:
        return BLOCK_ANNEX
    if source == "signature":
        return BLOCK_SIGNATURE
    if source == "party_info":
        return BLOCK_PARTY_INFORMATION
    return BLOCK_OPERATIVE


def _normalize_clause_text(text: str) -> str:
    return re.sub(r"\s+", "", text or "")


def _make_clause(
    *,
    clause_id: str,
    location: str,
    title: str,
    text: str,
    section_type: str,
    level: int,
    paragraph_index: int = 0,
) -> ParsedClause:
    normalized = _normalize_clause_text(text)
    source = _clause_source(section_type, text)
    first_line = text.splitlines()[0] if text else ""
    article = ARTICLE_RE.match(first_line)
    return ParsedClause(
        clause_id=clause_id,
        location=location,
        title=title,
        text=text,
        section_type=section_type,
        level=level,
        raw_text=text,
        normalized_text=normalized,
        option_groups=[group.to_public_dict() for group in parse_option_groups(text)],
        source=source,
        section_path=[value for value in (section_type, location) if value],
        heading=title,
        clause_number=article.group(0).split(maxsplit=1)[0] if article else "",
        paragraph_index=paragraph_index,
        block_type=_block_type(section_type, source),
        parties=list(dict.fromkeys(re.findall(r"甲方|乙方|出卖人|买受人|买方|卖方|供货单位|购货单位", text))),
        dates=re.findall(r"(?:20\d{2})[年/.-]\d{1,2}[月/.-]\d{1,2}日?", text),
        amounts=re.findall(r"(?:人民币)?\s*[\d,]+(?:\.\d+)?\s*元", text),
        percentages=re.findall(r"(?:\d+(?:\.\d+)?\s*[%％]|百分之[一二三四五六七八九十百]+|万分之[一二三四五六七八九十百]+)", text),
        durations=re.findall(r"(?:\d+|[一二三四五六七八九十]+)\s*(?:个)?\s*(?:工作日|日|天|个月|月|年)", text),
        cross_references=re.findall(r"第[一二三四五六七八九十百零〇\d]+条", text),
    )


ARTICLE_RE = re.compile(r"^第[一二三四五六七八九十百零〇\d]+条[\s　]*(.*)$")
CHINESE_HEADING_RE = re.compile(r"^[一二三四五六七八九十百零〇]+、\s*(.*)$")
SUBCLAUSE_RE = re.compile(r"^（[一二三四五六七八九十]+）")
NUMBERED_RE = re.compile(r"^\d+[\.．、]")
APPENDIX_RE = re.compile(r"^(附件|附表)[一二三四五六七八九十\d]*")
PARTY_RE = re.compile(r"^(甲方|乙方)[（(].*")
NON_CONTRACT_META_MARKERS = (
    "测试重点",
    "测试说明",
    "审查要求",
    "用户提问",
    "修正动作",
    "验证标准",
    "应被判定为",
    "应被识别为",
    "当前状态",
    "问题发现",
    "任务目标",
)


def _is_non_contract_meta_line(line: str) -> bool:
    compacted = re.sub(r"\s+", "", line)
    return any(marker in compacted for marker in NON_CONTRACT_META_MARKERS)


def _is_signature_boundary_line(line: str) -> bool:
    compacted = re.sub(r"\s+", "", line)
    if "（以下无正文）" in compacted or "(以下无正文)" in compacted:
        return True
    if compacted in {"签字", "签名", "盖章", "签字盖章", "签名盖章"}:
        return True
    if re.match(r"^(甲方|乙方|出卖人|买受人|法定代表人|委托代理人|授权代表).{0,8}(签字|签名|盖章)[:：]?$", compacted):
        return True
    if re.match(r"^(签署日期|签订日期|日期)[:：]?[年月日\d_\-/.]*$", compacted):
        return True
    return False


def strip_non_contract_tail(contract_text: str) -> str:
    """Remove test notes or analysis text appended outside the contract body."""
    kept: List[str] = []
    in_signature_tail = False

    for raw_line in (contract_text or "").splitlines():
        line = raw_line.strip()
        if not line:
            if not in_signature_tail:
                kept.append(raw_line)
            continue
        if _is_non_contract_meta_line(line):
            break
        if in_signature_tail:
            if APPENDIX_RE.match(line):
                in_signature_tail = False
                kept.append(raw_line)
            continue
        if _is_signature_boundary_line(line):
            in_signature_tail = True
            continue
        kept.append(raw_line)

    return "\n".join(kept).strip()


def _clean_lines(contract_text: str) -> List[str]:
    lines = []
    for raw_line in strip_non_contract_tail(contract_text).splitlines():
        normalized = raw_line.strip()
        if not normalized:
            continue
        normalized = re.sub(r"\s+(?=第[一二三四五六七八九十百零〇\d]+条)", "\n", normalized)
        normalized = re.sub(r"(?<!^)(?=第[一二三四五六七八九十百零〇\d]+条)", "\n", normalized)
        normalized = re.sub(r"\s+#+\s*(?=[一二三四五六七八九十百零〇]+、|附件|补充条款|甲方[（(]|乙方[（(])", "\n", normalized)
        normalized = re.sub(r"(?<!^)(?<![一二三四五六七八九十百零〇附件])(?=[一二三四五六七八九十百零〇]+、)", "\n", normalized)
        normalized = re.sub(r"(?<!^)(?=（[一二三四五六七八九十]+）)", "\n", normalized)
        normalized = re.sub(r"(?<!^)(?<!\d)(?=\d+[\.．、](?!\d))", "\n", normalized)
        normalized = re.sub(r"(?<!^)(?=本合同双方当事人[:：])", "\n", normalized)
        normalized = re.sub(r"(?<!^)(?=出租方[（(])", "\n", normalized)
        normalized = re.sub(r"(?<!^)(?=承租方[（(])", "\n", normalized)
        for line in normalized.splitlines():
            line = re.sub(r"^#+\s*", "", line.strip())
            if line:
                lines.append(line)
    return lines


def _section_type_for_line(line: str, current: str, formal_started: bool) -> str:
    if APPENDIX_RE.match(line):
        return SECTION_APPENDIX
    compacted = re.sub(r"[：:\s]", "", line)
    if compacted in {"使用说明", "填写说明"}:
        return SECTION_USAGE
    if compacted in {"特别提示", "范本附注"}:
        return SECTION_SPECIAL_NOTICE
    if compacted in {"编制说明", "条文说明", "注释", "评论"}:
        return SECTION_COMMENTARY
    if compacted in {"历史沿革", "修订记录", "历史说明"}:
        return SECTION_HISTORICAL_NOTE
    if formal_started:
        return current if current in {SECTION_APPENDIX, SECTION_USAGE, SECTION_SPECIAL_NOTICE, SECTION_COMMENTARY, SECTION_HISTORICAL_NOTE} else SECTION_FORMAL
    return current


def _fallback_unstructured_clauses(lines: List[str]) -> List[ParsedClause]:
    raw_segments: List[str] = []
    for line in lines:
        parts = [part.strip() for part in re.split(r"(?<=[；;。])\s*", line) if part.strip()]
        raw_segments.extend(parts or [line])

    return [
        _make_clause(
            clause_id=f"C{index + 1:04d}",
            location=f"第{index + 1}段",
            title=segment[:40],
            text=segment,
            section_type=SECTION_FORMAL,
            level=0,
        )
        for index, segment in enumerate(raw_segments)
    ]


def parse_contract_clauses(contract_text: str) -> List[ParsedClause]:
    """Parse contract text into traceable clauses.

    If the contract does not contain recognizable formal-clause markers, the
    whole text is treated as formal terms so ordinary short test strings still
    review correctly.
    """

    lines = _clean_lines(contract_text)
    if not lines:
        return []

    clauses: List[ParsedClause] = []
    current_lines: List[str] = []
    current_location = "全文"
    current_title = "全文"
    current_section = SECTION_USAGE if "使用说明" in lines[:6] else SECTION_FORMAL
    current_level = 0
    article_location = ""
    formal_started = current_section == SECTION_FORMAL
    seen_structural_marker = False

    def flush() -> None:
        nonlocal current_lines, current_location, current_title, current_section, current_level
        text = "\n".join(current_lines).strip()
        if not text:
            current_lines = []
            return
        clauses.append(
            _make_clause(
                clause_id=f"C{len(clauses) + 1:04d}",
                location=current_location,
                title=current_title,
                text=text,
                section_type=current_section,
                level=current_level,
                paragraph_index=len(clauses),
            )
        )
        current_lines = []

    for line in lines:
        if re.sub(r"\s+", "", line).startswith(("订立合同双方", "合同双方当事人", "甲乙双方经")):
            formal_started = True
            if current_section != SECTION_FORMAL:
                flush()
            current_section = SECTION_FORMAL
            current_location = "合同主体"
            current_title = "合同主体"
            current_level = 1
        if line.startswith("甲方（出租人）") or line.startswith("甲方(出租人)"):
            formal_started = True
            if current_section != SECTION_FORMAL:
                flush()
            current_section = SECTION_FORMAL
            current_location = "当事人信息"
            current_title = "当事人信息"
            current_level = 1

        next_section = _section_type_for_line(line, current_section, formal_started)
        if next_section != current_section:
            flush()
            current_section = next_section
            current_location = next_section
            current_title = line
            current_level = 0
            current_lines = [line]
            continue

        article_match = ARTICLE_RE.match(line)
        chinese_heading_match = CHINESE_HEADING_RE.match(line)
        party_match = PARTY_RE.match(line)
        if APPENDIX_RE.match(line):
            flush()
            seen_structural_marker = True
            current_section = SECTION_APPENDIX
            article_location = line
            current_location = line
            current_title = line
            current_level = 1
            current_lines = [line]
            continue
        if party_match and current_section in {SECTION_FORMAL, SECTION_APPENDIX}:
            flush()
            seen_structural_marker = True
            current_location = line[:40]
            current_title = line[:40]
            current_level = 1
            current_section = SECTION_FORMAL
            formal_started = True
            current_lines = [line]
            continue
        if article_match:
            flush()
            seen_structural_marker = True
            article_location = line.split(maxsplit=1)[0]
            current_location = line
            current_title = article_match.group(1).strip() or line
            current_level = 1
            current_section = SECTION_FORMAL
            formal_started = True
            current_lines = [line]
            continue
        if chinese_heading_match and current_section in {SECTION_FORMAL, SECTION_APPENDIX}:
            flush()
            seen_structural_marker = True
            article_location = line.split("、", 1)[0] + "、"
            current_location = line
            current_title = chinese_heading_match.group(1).strip() or line
            current_level = 1
            current_section = SECTION_FORMAL
            formal_started = True
            current_lines = [line]
            continue
        if SUBCLAUSE_RE.match(line) and current_section in {SECTION_FORMAL, SECTION_APPENDIX}:
            flush()
            seen_structural_marker = True
            marker = SUBCLAUSE_RE.match(line).group(0)
            current_location = f"{article_location}{marker}" if article_location else marker
            current_title = line[:40]
            current_level = 2
            current_lines = [line]
            continue
        if NUMBERED_RE.match(line) and current_section in {SECTION_FORMAL, SECTION_APPENDIX}:
            flush()
            seen_structural_marker = True
            marker = NUMBERED_RE.match(line).group(0).rstrip(".．、")
            current_location = f"{article_location}第{marker}项" if article_location else f"第{marker}项"
            current_title = line[:40]
            current_level = 3
            current_lines = [line]
            continue

        current_lines.append(line)

    flush()

    if (
        not seen_structural_marker
        and len(clauses) <= 2
        and all(clause.section_type == SECTION_FORMAL for clause in clauses)
    ):
        return _fallback_unstructured_clauses(lines)

    return clauses


def formal_evidence_clauses(clauses: List[ParsedClause]) -> List[ParsedClause]:
    allowed = {BLOCK_OPERATIVE, BLOCK_ANNEX, BLOCK_PARTY_INFORMATION, BLOCK_SIGNATURE}
    return [clause for clause in clauses if clause.block_type in allowed]


def document_integrity(contract_text: str, clauses: Optional[List[ParsedClause]] = None) -> DocumentIntegrity:
    source = contract_text or ""
    parsed = clauses if clauses is not None else parse_contract_clauses(source)
    normalized_source = _normalize_clause_text(strip_non_contract_tail(source))
    normalized_parsed = "".join(clause.normalized_text for clause in parsed)
    ratio = min(1.0, len(normalized_parsed) / len(normalized_source)) if normalized_source else 1.0
    skipped = [] if ratio >= 0.95 else [{"start": len(normalized_parsed), "end": len(normalized_source)}]
    return DocumentIntegrity(
        source_length=len(source),
        normalized_length=len(normalized_source),
        paragraph_count=len([line for line in source.splitlines() if line.strip()]),
        clause_count=len(parsed),
        heading_count=sum(1 for clause in parsed if clause.level <= 1),
        first_clause=parsed[0].clause_id if parsed else "",
        last_clause=parsed[-1].clause_id if parsed else "",
        parsed_character_ratio=round(ratio, 4),
        skipped_ranges=skipped,
        truncated=bool(skipped),
    )
