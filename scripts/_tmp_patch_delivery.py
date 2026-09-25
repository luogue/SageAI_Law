"""精确修补 delivery_form 过滤正则（加入 Incoterm / 邮寄渠道）。"""
from pathlib import Path

P = Path(r"F:/ai/Sage/backend/review_v2/consulting_element_facts.py")
src = P.read_text(encoding="utf-8")

old = "|书面报告', source['quote'], re.I,"
new = "|书面报告|CIF|FOB|C&F|CFR|FCA|航空邮寄|挂号邮寄|快递', source['quote'], re.I,"

print("old found count:", src.count(old))
if src.count(old) == 1:
    P.write_text(src.replace(old, new), encoding="utf-8")
    print("patched OK")
    # 回读验证
    again = P.read_text(encoding="utf-8")
    print("verify CIF in filter:", "|书面报告|CIF|FOB" in again)
else:
    # 回退：尝试按行定位
    print("未唯一匹配，按行检查：")
    for i, line in enumerate(src.splitlines(), 1):
        if "书面报告" in line and "source['quote']" in line:
            print(i, repr(line))
