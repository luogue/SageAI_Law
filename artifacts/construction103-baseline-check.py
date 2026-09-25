"""Isolated counterfactual: undo this turn's changed predicates/search/quotes only."""
import sys,ast,json
from pathlib import Path
sys.path.insert(0,str(Path.cwd()/'backend'))
from docx import Document
import review_v2.engine as engine
import review_v2.construction_coverage as c
import review_v2.penalty_base as p
old_document=r'(?:组成本?合同的(?:各个)?文件|本?合同(?:的)?组成文件|合同文件的组成|合同文件包括|本?合同(?:包括|包含)以下文件)'
# Only the changed requirements are restored; untouched requirements stay identical.
changes={
 'scope': [r'(?:承包范围|工程范围|施工范围)(?:，包括以下)?[：:].{2,180}'],
 'acceptance':[r'(?:承包人|发包人|监理人).{0,40}(?:应|须).{0,35}(?:组织|申请|提交|通知).{0,50}竣工验收'],
 'deposit_return':[r'(?:期满|届满|\d+日内).{0,60}(?:返还|退还).{0,20}(?:质量保证金|质保金)',r'(?:质量保证金|质保金)(?:应|须|于|在|的返还期限).{0,60}(?:期|日).{0,40}(?:返还|退还)'],
 'pricing':[r'(?:合同价格|合同价款|工程价款|合同总价).{0,100}(?:固定|总价|单价|计价|清单)',r'本合同采用.{0,30}(?:总价|单价|清单计价).{0,20}(?:合同|形式|方式)'],
 'settlement_payment':[r'(?:结算|审核).{0,100}(?:付款|支付|应付|结清).{0,50}(?:日内|期限|节点)'],
 'pricing_attachment':[r'(?:工程量清单|报价清单|预算书|计价表).{0,100}(?:附件|合同文件|组成|确认)|(?:附件|合同文件|组成).{0,160}(?:工程量清单|报价清单|预算书|计价表)'],
}
for node,reqs in c.PROFILES.items():
 for e in reqs:
  if e['element_id'] in changes:
   e['construction_patterns']=tuple(x.replace('.{',r'[^。\n]{') for x in changes[e['element_id']])
  else:
   e['construction_patterns']=tuple(x.replace(c.DOCUMENT,old_document).replace('标准.{0,8}规范|技术(?:标准及)?要求|技术标准|技术规范','标准.{0,8}规范|技术要求|技术规范') for x in e['construction_patterns'])
new_extract=c.extract
def old_extract(*args,**kwargs):
 rows=new_extract(*args,**kwargs)
 for row in rows:row.pop('quote',None)
 return rows
c.extract=old_extract;engine.extract_construction_coverage=old_extract
source=Path('backend/review_v2/engine.py').read_text(encoding='utf8')
node=next(n for n in ast.parse(source).body if isinstance(n,ast.FunctionDef) and n.name=='_search_final_element')
function=ast.get_source_segment(source,node).replace('item.decision_trace.get("construction_required_elements", CONSTRUCTION_COVERAGE_PROFILES.get(item.node_id, []))','item.decision_trace.get("construction_required_elements", [])')
exec(function,engine.__dict__)
source=Path('backend/review_v2/penalty_base.py').read_text(encoding='utf8')
node=next(n for n in ast.parse(source).body if isinstance(n,ast.FunctionDef) and n.name=='analyze')
function=ast.get_source_segment(source,node)
a=function.index("        if re.fullmatch(r'(?:本)?合同(?:暂定|最终|结算)?")
b=function.index('        if base in LOAN_BASE_ALIASES:',a)
exec(function[:a]+function[b:],p.__dict__)
p.source_pattern=p.re.escape
text='\n'.join(x.text for x in Document('test_data/50 建设工程.docx').paragraphs if x.text.strip())
r=engine.review_contract_v2(text,'construction',use_llm=False)
Path('artifacts/construction103-legacy-baseline.json').write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf8')
print('count',len(r['items']))
for i in r['items']:
 if i['item_id'] in ['CE-12-03','CE-13-03']:print(i['item_id'],i['coverage_status'])
print('manual',r['coverage_summary'].get('待核验'))
print('legacy replacement target present','- 待核验：6 项' in r['result'])
