"""诊断 delivery_form 过滤块真实内容。"""
from pathlib import Path

P = Path(r"F:/ai/Sage/backend/review_v2/consulting_element_facts.py")
src = P.read_text(encoding="utf-8")
lines = src.splitlines()

print("=== 含 '书面报告' 的行 ===")
for i, line in enumerate(lines, 1):
    if "书面报告" in line:
        print(i, repr(line))

print("\n=== 含 'delivery_form' 的行 ===")
for i, line in enumerate(lines, 1):
    if "delivery_form" in line:
        print(i, repr(line[:150]))

print("\n=== 400-420 行 ===")
for i in range(399, min(421, len(lines))):
    print(i + 1, repr(lines[i][:160]))
