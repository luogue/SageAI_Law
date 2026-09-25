from pathlib import Path
p=Path('backend/review_v2/shareholder_transaction_facts.py');s=p.read_text(encoding='utf-8')
s=s.replace("    for c in rows:\n        reason = ''", "    from copy import copy\n    sentences = []\n    for source in rows:\n        for match in re.finditer(r'[^。]+[。]?', source.text):\n            c = copy(source)\n            c.text = match.group().strip()\n            sentences.append(c)\n    for c in sentences:\n        reason = ''",1)
s=s.replace("        if m:=re.search('('+PARTY+r')认缴出资额", "        for m in re.finditer('('+PARTY+r')认缴出资额")
s=s.replace("dates.append((date(*map(int,ds[0])),date(*map(int,ds[1])),c))", "dates.extend((date(*map(int,ds[j])),date(*map(int,ds[j+1])),c) for j in range(0,len(ds)-1,2))")
s=s.replace("            if base is c or '租赁合同' not in base.text:continue", "            if (base_start,base_end)==(start,end) or '租赁合同' not in base.text:continue")
p.write_text(s,encoding='utf-8')
