"""Reusable source facts for tabular breach tariffs, independent of consumers."""
import re

EVENTS = {'delay': r'(?:工期|竣工|完工|交付|交货)(?:延期|延误|延迟|逾期)|(?:逾期|延误|延迟)(?:竣工|完工|交付|交货)'}
RATE = r'(?P<amount>[\d,，]+(?:\.\d+)?)\s*元\s*[/／]\s*(?P<unit>天|日|月|次)'

def facts(text):
    rows=[]
    for m in re.finditer(r'(?P<event>[^。；;\n：:]{2,35})\s*[：:]\s*'+RATE,text):
        before=text[:m.start()]
        header=re.split(r'\n\s*(?:第[一二三四五六七八九十\d]+条|[一二三四五六七八九十]+、)',before)[-1]
        if not re.search(r'违约责任|违约金|赔偿标准|罚款标准',header):
            continue
        if re.search(r'例如|假设|示例',header[-40:]+m.group()):
            continue
        concept=next((k for k,p in EVENTS.items() if re.search(p,m['event'])), 'other_breach')
        rows.append({'concept':concept,'event':m['event'].strip(), 'quote':m.group(),
                     'start':m.start(),'end':m.end(),'amount':m['amount'].replace(',','').replace('，',''),
                     'unit':m['unit'],'context':'BREACH_TARIFF'})
    return rows

def supports(text, concept):
    return any(f['concept']==concept for f in facts(text))
