"""精确模拟 arrangement_matches 内部判定，定位 C0042 拦截点。"""
import io
import re
import sys
from pathlib import Path

ROOT = Path(r"F:/ai/Sage")
sys.path.insert(0, str(ROOT / "backend"))
sys.path.insert(0, str(ROOT))

from review_v2.proposition_scope import (
    scoped_propositions, arrangement_matches,
    _GAP, _UNRESOLVED, _INDEPENDENT,
)
from review_v2.consulting_element_facts import FAMILIES

OUT = ROOT / "scripts" / "_tmp_debug2.out.txt"
buf = io.StringIO()


def w(s=""):
    buf.write(s + "\n")


TEXT = ("7.2如果咨询方在其控制的范围内在任何时候、以任何原因向委托方提供本合同附件一中的"
        "工作范围内的服务不能令人满意，委托方可将不满意之处通知咨询方，并给咨询方30天的期限改正或弥补。")

defect_pat = dict((r[0], r[2]) for r in FAMILIES["consulting_remedy"])["defect_trigger"]
corr_pat = dict((r[0], r[2]) for r in FAMILIES["consulting_remedy"])["correction_period"]

for name, pattern in [("defect_trigger", defect_pat), ("correction_period", corr_pat)]:
    w("=" * 66)
    w(f"{name}")
    w("=" * 66)
    w(f"text: {TEXT}")
    w(f"\nscoped_propositions:")
    for row in scoped_propositions(TEXT):
        w(f"  quote={row['quote'][:80]}...")
        w(f"     polarity={row['polarity']} inherited_missing={row['inherited_missing']} "
          f"condition={row['condition'][:40] if row['condition'] else None}")
    w(f"\n逐 match 判定:")
    for m in re.finditer(pattern, TEXT, re.I):
        w(f"  match={m[0][:60]!r} start={m.start()} end={m.end()}")
        # 模拟 arrangement_matches 内部
        for row in scoped_propositions(TEXT):
            quote = row["quote"]
            if row["inherited_missing"]:
                w(f"     -> quote 被 inherited_missing 跳过")
                continue
            if re.fullmatch(r"第[一二三四五六七八九十百\d]+条[^，,。；;：:\n]{0,40}", quote):
                w(f"     -> quote 被 fullmatch 跳过")
                continue
            for match in re.finditer(pattern, quote, re.I):
                independent = [x.start() for x in _INDEPENDENT.finditer(quote) if x.start() <= match.start()]
                begin = independent[-1] if independent else 0
                boundaries = [x.end() + begin for x in re.finditer(r"[，,]", quote[begin:match.start()])]
                prefix = quote[boundaries[-1] if boundaries else begin:match.start()]
                gap = _GAP.search(quote, begin) or _UNRESOLVED.search(quote, begin)
                w(f"     inner match={match[0][:50]!r}")
                w(f"       prefix={prefix[-40:]!r}")
                w(f"       gap={gap[0] if gap else None}")
                q = quote[begin:match.end()]
                w(f"       是否/能否检查={bool(re.search(r'是否|能否|要不要|何时|如何', q))}")
                w(f"       gap拦截={bool(gap and (gap.start() < match.end()))}")
                w(f"       negation拦截={bool(re.search(r'(?:不(?:应当|应|得|能|再|会|必|须)?|无需|无须|未|没有|并非|未曾|不曾|否认)[^，,。；;]{0,6}$', prefix))}")
    w(f"\n  最终 arrangement_matches 数量 = {len(list(arrangement_matches(pattern, TEXT)))}")
    w("")

OUT.write_text(buf.getvalue(), encoding="utf-8")
print("written", OUT)
