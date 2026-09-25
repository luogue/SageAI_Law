"""Diagnostic only: restore this turn's shared logic in memory, never on disk.

Application-only branches and display entries cannot execute for the granted-
patent fixtures. The three shared behavioral changes are restored below before
running the exact same granted-patent suite to distinguish pre-existing failures.
"""
import inspect
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "backend"))
import review_v2.engine as engine
import pytest

source = inspect.getsource(engine._is_technology_checkpoint_applicable)
start = source.index('    if item_id == "TC-03-02":')
end = source.index('    if item_id in {"TC-03-01", "TC-03-03"}:', start)
source = source[:start] + source[end:]
source = source.replace('if item_id in {"TC-03-01", "TC-03-03"}:',
                        'if item_id in {"TC-03-01", "TC-03-02", "TC-03-03"}:')
exec(compile(source, "<pre-turn-applicability>", "exec"), engine.__dict__)


def previous_restriction(text):
    compact = engine._compact(text)
    return bool(
        any(term in compact for term in ("改进", "后续研发", "竞争性技术"))
        and re.search(
            r"(?:禁止|不得|无权|限制).{0,35}(?:自主)?(?:研发|研究|改进|使用竞争性技术)|"
            r"(?:必须|应当|应|须).{0,30}(?:无偿|免费).{0,20}(?:转让|移交|归属).{0,30}(?:改进|成果)|"
            r"(?:改进|后续研发).{0,40}(?:仅归|一律归|全部归).{0,16}(?:许可方|出让方|转让方)", compact)
        and not re.search(r"不得.{0,24}(?:限制|要求).{0,40}(?:自主改进|无偿转让)", compact)
    )


engine._has_affirmative_improvement_restriction = previous_restriction
source = inspect.getsource(engine._apply_technology_common_semantic_rules)
start = source.index("            attachment_schedule_clauses = [")
end = source.index("            closed_schedule_strength = (", start)
block = source[start:end]
block = block.replace("if (re.search(", "if re.search(")
addition = '''                ) or (
                    "附件" in _compact(clause.title)
                    and len(re.findall(r"《[^》]+》", clause.text)) >= 2
                    and any(term in clause.text for term in ("资料", "申请文件", "源代码", "设计", "技术"))
                ))'''
assert addition in block
block = block.replace(addition, "                )")
addition = ''' or any(
                    "附件" in _compact(clause.title) and len(re.findall(r"《[^》]+》", clause.text)) >= 2
                    for clause in attachment_schedule_clauses
                )'''
assert addition in block
block = block.replace(addition, "")
source = source[:start] + block + source[end:]
exec(compile(source, "<pre-turn-attachment-selection>", "exec"), engine.__dict__)
raise SystemExit(pytest.main(["tests/test_patent_right_transfer_contract_review.py", "-q", "--tb=short"]))
