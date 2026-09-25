"""Body-level carriage purpose and downstream shipment scope."""
import re

def analyze(text):
    groups = {
        'carrier': r'承运人|承运方|负责运输|承担运输',
        'goods': r'货物(?:名称|数量|为|包括)|托运[^。\n]{0,25}(?:吨|件|箱)',
        'journey': r'起运地|目的地|从[^。\n]{1,25}运至',
        'price': r'运费|运输费用',
    }
    facts = {k:m.group() for k,p in groups.items() if (m:=re.search(p,text))}
    downstream = bool(re.search(r'(?:每票|每批|具体运输业务)[^。\n]{0,45}(?:另行|另签)[^。\n]{0,25}(?:合同|运单|运输单)',text))
    framework = downstream and bool(re.search(r'框架|长期运输合作|运输合作协议',text))
    return {'established':len(facts)==4, 'facts':facts, 'framework':framework}

SHIPMENT_ITEMS = {'T-01-02','T-01-03','T-02-01','T-02-02','T-02-03','T-03-01','T-03-04','T-08-01','T-08-02','T-12-02'}
