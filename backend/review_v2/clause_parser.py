"""Clause parser for contract review v2.

The parser keeps source text traceable by splitting uploaded contracts into
clauses and marking whether a clause is a formal contract term, usage
instruction, special notice, or appendix.
"""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass
from typing import Dict, List


SECTION_USAGE = "使用说明"
SECTION_SPECIAL_NOTICE = "特别提示"
SECTION_FORMAL = "正式合同条款"
SECTION_APPENDIX = "附件"


@dataclass(frozen=True)
class ParsedClause:
    clause_id: str
    location: str
    title: str
    text: str
    section_type: str
    level: int

    def to_public_dict(self) -> Dict[str, str | int]:
        return asdict(self)


ARTICLE_RE = re.compile(r"^第[一二三四五六七八九十百零〇\d]+条[\s　]*(.*)$")
SUBCLAUSE_RE = re.compile(r"^（[一二三四五六七八九十]+）")
NUMBERED_RE = re.compile(r"^\d+[\.．、]")
APPENDIX_RE = re.compile(r"^(附件|附表)[一二三四五六七八九十\d]*")


def _clean_lines(contract_text: str) -> List[str]:
    lines = []
    for raw_line in (contract_text or "").splitlines():
        line = raw_line.strip()
        if line:
            lines.append(line)
    return lines


def _section_type_for_line(line: str, current: str, formal_started: bool) -> str:
    if APPENDIX_RE.match(line):
        return SECTION_APPENDIX
    if formal_started:
        return current if current == SECTION_APPENDIX else SECTION_FORMAL
    if line == "使用说明":
        return SECTION_USAGE
    if line == "特别提示":
        return SECTION_SPECIAL_NOTICE
    return current


def _fallback_unstructured_clauses(lines: List[str]) -> List[ParsedClause]:
    raw_segments: List[str] = []
    for line in lines:
        parts = [part.strip() for part in re.split(r"(?<=[；;。])\s*", line) if part.strip()]
        raw_segments.extend(parts or [line])

    return [
        ParsedClause(
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
            ParsedClause(
                clause_id=f"C{len(clauses) + 1:04d}",
                location=current_location,
                title=current_title,
                text=text,
                section_type=current_section,
                level=current_level,
            )
        )
        current_lines = []

    for line in lines:
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

    if not seen_structural_marker and len(clauses) <= 2:
        return _fallback_unstructured_clauses(lines)

    return clauses


def formal_evidence_clauses(clauses: List[ParsedClause]) -> List[ParsedClause]:
    return [clause for clause in clauses if clause.section_type in {SECTION_FORMAL, SECTION_APPENDIX}]
