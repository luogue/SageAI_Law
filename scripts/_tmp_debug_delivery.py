"""调试 33 的 delivery_form 匹配。"""
import io
import re
import sys
from pathlib import Path

ROOT = Path(r"F:/ai/Sage")
sys.path.insert(0, str(ROOT / "backend"))
sys.path.insert(0, str(ROOT))

from review_v2.clause_parser import parse_contract_clauses
from review_v2.obligation_detail_elements import _segments
from review_v2.proposition_scope import arrangement_matches, scoped_propositions, _GAP, _UNRESOLVED, _INDEPENDENT
from review_v2.consulting_element_facts import FAMILIES

OUT = ROOT / "scripts" / "_tmp_debug_delivery.out.txt"
buf = io.StringIO()


def w(s=""):
    buf.write(s + "\n")


TEXT = (ROOT / "backend" / "tests" / "fixtures" / "round46_consulting_generalization.txt").read_text(encoding="utf-8")
clauses = parse_contract_clauses(TEXT)
pat = dict((r[0], r[2]) for r in FAMILIES["consulting_quality"])["delivery_form"]
w("delivery_form pattern:")
w("  " + pat[:500])

w("\n含 CIF/邮寄 的 segments:")
for clause, heading, quote in _segments(clauses):
    text = re.sub(r"\s+", "", quote)
    if not re.search(r"CIF|邮寄", text):
        continue
    w(f"\nclause={clause.clause_id} block={getattr(clause,'block_type','')}")
    w(f"  title={getattr(clause,'title','')[:60]}")
    w(f"  text={text[:120]}")
    w(f"  直接正则分支3={bool(re.search(r'(?:报告|文件|成果)[^。；]{0,30}(?:以|按|采用)[^。；]{0,25}(?:CIF|FOB|C&F|CFR|FCA|航空邮寄|挂号邮寄|快递)[^。；]{0,30}(?:交付|提交)', text))}")
    w(f"  完整pattern finditer={[m[0][:60] for m in re.finditer(pat, text, re.I)]}")
    w(f"  arrangement_matches={len(list(arrangement_matches(pat, text)))}")
    for row in scoped_propositions(text):
        q = row["quote"]
        w(f"    scoped: {q[:70]!r} polarity={row['polarity']} inherited={row['inherited_missing']}")
        for match in re.finditer(pat, q, re.I):
            begin = 0
            boundaries = [m.end() for m in re.finditer(r"[，,]", q[:match.start()])]
            prefix = q[boundaries[-1] if boundaries else begin:match.start()]
            w(f"      match={match[0][:50]!r} prefix={prefix[-30:]!r}")
            w(f"        疑问词拦截={bool(re.search(r'是否|能否|要不要|(?<!任)何时|如何', q[begin:match.end()]))}")
            w(f"        negation拦截={bool(re.search(r'(?:不(?:应当|应|得|能|再|会|必|须)?|无需|无须|未|没有|并非|未曾|不曾|否认)[^，,。；;]{0,6}$', prefix))}")

OUT.write_text(buf.getvalue(), encoding="utf-8")
print("written", OUT)
