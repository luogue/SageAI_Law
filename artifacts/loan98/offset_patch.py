from pathlib import Path
p=Path('backend/review_v2/loan_facts.py');s=p.read_text(encoding='utf8').replace('r"抵充|冲抵|清偿顺序|偿还顺序"','r"抵充|冲抵|清偿顺序|偿还顺序|扣款顺序"')
s=s.replace('    else:\n        source=units(clauses)','    elif node == "loan_repayment_offset_order":\n        source=((c,c.text) for c in formal_evidence_clauses(list(clauses)) if re.search(r"抵充|冲抵|清偿顺序|偿还顺序|扣款顺序",c.text))\n    else:\n        source=units(clauses)')
s=s.replace('    if element.get("element_id") == "loan_agreed_rate":', '''    if element.get('element_id') == 'loan_early_application' and re.search(r'无需[^。；]{0,10}(?:申请|同意)|不得申请',compact(text)):
        return False
    if element.get("element_id") == "loan_agreed_rate":''')
p.write_text(s,encoding='utf8')
