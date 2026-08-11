"""Template and checkbox parsing for contract review v2.

This module owns the interpretation of bracketed options and checkbox marks.
Fact extractors should consume this AST instead of re-parsing raw template
characters such as ``☑``, ``□`` and ``【】``.
"""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass
from typing import Any, Dict, List


BLANK_PLACEHOLDER_RE = re.compile(r"^[\s_＿—\-□【】（）()]*$")
CHECK_MARKS = {"☑", "☒", "√", "■", "✅"}
UNCHECK_MARKS = {"□", "☐", "○", "◇"}
OPTION_MARKS = CHECK_MARKS | UNCHECK_MARKS
OPTION_MARK_CLASS = "".join(re.escape(mark) for mark in sorted(OPTION_MARKS))


@dataclass(frozen=True)
class TemplateOption:
    label: str
    selected: bool
    blank: bool
    raw_text: str
    priority: int

    def to_public_dict(self) -> Dict[str, Any]:
        return {
            "text": "" if self.blank else self.label,
            "selected": self.selected,
            "blank": self.blank,
            "raw_text": self.raw_text,
            "priority": self.priority,
        }


@dataclass(frozen=True)
class OptionGroup:
    group_id: str
    type: str
    options: List[TemplateOption]
    raw_text: str

    def to_public_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["options"] = [option.to_public_dict() for option in self.options]
        return data


def is_blank_option_value(value: Any) -> bool:
    if value is None:
        return True
    if isinstance(value, bool):
        return False
    if isinstance(value, (int, float)):
        return False
    text = str(value).strip()
    if not text:
        return True
    if text in {"待填写", "未填写", "无", "暂无", "不详", "null", "None"}:
        return True
    if BLANK_PLACEHOLDER_RE.fullmatch(text):
        return True
    stripped = text.replace("_", "").replace("＿", "")
    if re.fullmatch(r".*[_＿]{3,}.*", text) and not re.search(r"[\u4e00-\u9fffA-Za-z0-9]", stripped):
        return True
    return False


def _option_priority(selected: bool, blank: bool, explicitly_unselected: bool) -> int:
    if selected and not blank:
        return 4
    if selected and blank:
        return 3
    if explicitly_unselected and not blank:
        return 2
    return 1


def parse_template_options(text: str) -> List[TemplateOption]:
    """Parse bracket/checkbox options and bind marks to the nearest option.

    Supported layouts include ``【A】☑【B】``, ``【A】【B】☑``, ``☑【A】【B】``,
    ``【A】□【B】☑`` and ``【每月5日前】☑【_____】``. A mark immediately after
    an option binds to the previous option; a mark immediately before an option
    binds to the following option. This mirrors common Chinese contract
    templates where the check mark is visually attached to the adjacent box.
    """

    source = text or ""
    pattern = re.compile(rf"([{OPTION_MARK_CLASS}]?)\s*【([^】]*)】\s*([{OPTION_MARK_CLASS}]?)")
    options: List[TemplateOption] = []
    occupied_spans: List[tuple[int, int]] = []
    for match in pattern.finditer(source):
        occupied_spans.append(match.span())
        before, label, after = match.groups()
        label = (label or "").strip()
        selected = before in CHECK_MARKS or after in CHECK_MARKS
        explicitly_unselected = before in UNCHECK_MARKS or after in UNCHECK_MARKS
        blank = is_blank_option_value(label)
        options.append(
            TemplateOption(
                label=label,
                selected=selected,
                blank=blank,
                raw_text=match.group(0),
                priority=_option_priority(selected, blank, explicitly_unselected),
            )
        )

    plain_pattern = re.compile(rf"([{OPTION_MARK_CLASS}])\s*([^{'【】' + OPTION_MARK_CLASS}。；;，,\n\r]+)")
    for match in plain_pattern.finditer(source):
        if any(start <= match.start() < end for start, end in occupied_spans):
            continue
        mark, label = match.groups()
        label = (label or "").strip()
        if not label:
            continue
        selected = mark in CHECK_MARKS
        explicitly_unselected = mark in UNCHECK_MARKS
        blank = is_blank_option_value(label)
        options.append(
            TemplateOption(
                label=label,
                selected=selected,
                blank=blank,
                raw_text=match.group(0),
                priority=_option_priority(selected, blank, explicitly_unselected),
            )
        )
    return options


def parse_option_groups(text: str) -> List[OptionGroup]:
    options = parse_template_options(text)
    if not options:
        return []
    return [
        OptionGroup(
            group_id="OG0001",
            type="choice_group",
            options=options,
            raw_text=text or "",
        )
    ]


def selected_non_blank_options(text: str) -> List[TemplateOption]:
    return [option for option in parse_template_options(text) if option.selected and not option.blank]
