from pathlib import Path
p=Path('backend/review_v2/engine.py');s=p.read_text(encoding='utf8').replace('if not complete and item.node_id in LOAN_ELEMENT_PROFILES:', 'if item.node_id in LOAN_ELEMENT_PROFILES and not complete:');p.write_text(s,encoding='utf8')
