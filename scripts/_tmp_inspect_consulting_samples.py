"""临时排查脚本：列出技术咨询样本标题，对比 Round41-45 fixtures 已用样本。"""
import sys
from pathlib import Path

ROOT = Path(r"F:/ai/Sage")

def docx_text(path: Path) -> str:
    try:
        from docx import Document
    except ImportError:
        return "(python-docx 不可用)"
    try:
        doc = Document(str(path))
        return "\n".join(p.text.strip() for p in doc.paragraphs if p.text.strip())
    except Exception as e:
        return f"(读取失败: {e})"

def head(text: str, n: int = 3) -> str:
    lines = [l for l in text.splitlines() if l.strip()]
    return " | ".join(lines[:n])

print("=" * 70)
print("A. test_data 中技术咨询类样本（候选新合同）")
print("=" * 70)
candidates = [
    "16 技术咨询合同.docx",
    "22 技术咨询.docx",
    "33 技术咨询服务合同.docx",
    "17 技术服务.docx",
    "23 技术服务.docx",
    "24 技术服务.docx",
    "32 技术服务.docx",
    "34 技术服务.docx",
]
for name in candidates:
    p = ROOT / "test_data" / name
    if p.exists():
        t = docx_text(p)
        print(f"\n[{name}]  size={p.stat().st_size}")
        print(f"   head: {head(t)}")
    else:
        print(f"\n[{name}] 不存在")

print("\n" + "=" * 70)
print("B. Round41-45 fixtures 标题（已用样本）")
print("=" * 70)
fx_dir = ROOT / "backend" / "tests" / "fixtures"
for fx in sorted(fx_dir.glob("round4*_consulting*.txt")) + sorted(fx_dir.glob("round36_consulting.txt")):
    t = fx.read_text(encoding="utf-8")
    print(f"\n[{fx.name}]  size={fx.stat().st_size}")
    print(f"   head: {head(t)}")

print("\n" + "=" * 70)
print("C. artifacts round44/45 input.txt 标题")
print("=" * 70)
for rd in ["round44_consulting_projection", "round45_consulting_projection"]:
    p = ROOT / "artifacts" / "technology_pass_semantics" / rd / "input.txt"
    if p.exists():
        t = p.read_text(encoding="utf-8")
        print(f"\n[{rd}/input.txt]  size={p.stat().st_size}")
        print(f"   head: {head(t)}")
