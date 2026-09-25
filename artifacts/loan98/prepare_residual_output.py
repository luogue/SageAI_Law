from pathlib import Path
s=Path('artifacts/loan98/save_diff.py').read_text(encoding='utf8').replace("root/'before.json'","root/'residual-before.json'").replace("root/'after.json'","root/'residual-after.json'").replace("root/'diff.md'","root/'residual-diff.md'").replace("root/'diff.json'","root/'residual-diff.json'").replace("root/'report.md'","root/'residual-report.md'").replace("root/'acceptance.json'","root/'residual-acceptance.json'")
Path('artifacts/loan98/save_residual_diff.py').write_text(s,encoding='utf8')
