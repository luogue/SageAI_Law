"""Opt-in runtime evidence diagnostics. Does not adjudicate or rewrite reports."""
import os,json,hashlib,subprocess,inspect
from dataclasses import asdict
from review_v2.security_property_checklist import RIGHTS_PLEDGE_CHECKLIST
from review_v2.priority_checklist_helpers import PROFILES
from review_v2.security_context import resolve
from review_v2.clause_parser import parse_contract_clauses
from review_v2.lease_semantics import corpus_facts,supports

def snapshot(text,contract_type):
 clauses=parse_contract_clauses(text);rules=[]
 for rule in RIGHTS_PLEDGE_CHECKLIST:
  if rule.item_id not in {'RPL-01-01','RPL-02-01','SEC-03-01'}:continue
  specs=resolve(rule.node_id,PROFILES[rule.node_id],text)
  facts=corpus_facts(clauses,specs)
  candidates=[c.to_public_dict() for c in clauses if '应收账款质押登记' in c.text]
  definition={'rule':asdict(rule),'requirements':specs}
  rules.append({**definition,'fingerprint':hashlib.sha256(json.dumps(definition,ensure_ascii=False,sort_keys=True).encode()).hexdigest(),
   'pre_render_elements':[{'element_id':s['element_id'],'label':s['proposition'],'status':'FOUND' if facts[s['element_id']] else 'NOT_FOUND','accepted':facts[s['element_id']], 'candidate_supports':[{'clause_id':c['clause_id'],'text':c['text'],'supports':supports(s,c)} for c in candidates]} for s in specs]})
 return {'pid':os.getpid(),'cwd':os.getcwd(),'git_commit':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),
  'contract_type':contract_type,'contract_sha256':hashlib.sha256(text.encode()).hexdigest(),'rules':rules,
  'module_file':inspect.getsourcefile(resolve),'module_sha256':hashlib.sha256(open(inspect.getsourcefile(resolve),'rb').read()).hexdigest(),
  'corpus':text,'chunks':[c.to_public_dict() for c in clauses],'cache':'No result cache in review-v2/file; new process imports fresh rule objects'}
