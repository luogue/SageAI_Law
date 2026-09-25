from pathlib import Path
p=Path('backend/tests/test_business_overlays.py');s=p.read_text(encoding='utf8').replace("assert analyze('未完成应补足相应损失。')[0]['status']=='AMBIGUOUS'","assert analyze('未完成应补足相应损失。') == []  # ordinary loss is not business-performance shortfall") ;p.write_text(s,encoding='utf8')
