from pathlib import Path
p=Path('backend/review_v2/loan_facts.py');s=p.read_text(encoding='utf8');s=s.replace('if re.search(r"抵充|冲抵|清偿顺序|偿还顺序|扣款顺序",c.text)', 'if re.search(r"部分还款|还款.{0,12}不足|抵充|冲抵|清偿顺序|偿还顺序|扣款顺序",c.text)');p.write_text(s,encoding='utf8')
