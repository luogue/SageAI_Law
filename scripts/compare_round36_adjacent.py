import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path

out=Path(__file__).resolve().parents[1]/'artifacts/technology_pass_semantics/round36_consulting_snapshot'
def rows(name):
    states,failures={},{}
    for c in ET.parse(out/name).iter('testcase'):
        key=c.attrib['classname']+'::'+c.attrib['name']
        failed=c.find('failure')
        if failed is None:failed=c.find('error')
        states[key]='FAIL' if failed is not None else 'SKIP' if c.find('skipped') is not None else 'PASS'
        if failed is not None:
            failures[key]=re.sub(r'0x[0-9A-Fa-f]+','0xADDR',failed.get('message',''))
    return states,failures
old,old_errors=rows('adjacent_baseline.xml')
new,new_errors=rows('adjacent.xml')
new_failures=[k for k,v in new.items() if v=='FAIL' and old.get(k)!='FAIL']
changed={k:[old.get(k),v] for k,v in new.items() if old.get(k)!=v}
assert old.keys()==new.keys(),'test inventory changed'
assert not new_failures,new_failures
assert all(old_errors[k]==v for k,v in new_errors.items()),'existing failure signature changed'
data={'total':len(new),'passed':list(new.values()).count('PASS'),'failed':len(new_errors),
      'newly_failing':new_failures,'changed':changed,'removed':[],'failure_signatures_equal':old_errors==new_errors,
      'existing_failed_tests':sorted(new_errors)}
(out/'adjacent_comparison.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({k:v for k,v in data.items() if k!='existing_failed_tests'},ensure_ascii=False))
