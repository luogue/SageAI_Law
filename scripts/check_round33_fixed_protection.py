"""Control model variability with identical baseline/final model responses."""
from pathlib import Path
import sys,json,hashlib
root=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(root/'backend'),str(root)]
from dotenv import load_dotenv
load_dotenv(root/'backend/.env')
out=root/'artifacts/technology_pass_semantics/round33_patent_transfer_projection'
mode,name,round_name,role=sys.argv[1:]
import review_v2
if mode=='baseline':review_v2.__path__.insert(0,str(out/'baseline_source'))
import reasoning.llm_client as client
original=client.call_llm
record=[] if mode=='baseline' else json.loads((out/f'{name}_model_responses.json').read_text(encoding='utf8'))
index=0
def controlled(prompt,*args,**kwargs):
 global index
 fingerprint=hashlib.sha256(prompt.encode()).hexdigest()
 if mode=='baseline':
  response=original(prompt,*args,**kwargs)
  record.append({'prompt_sha256':fingerprint,'response':response})
 else:
  assert record[index]['prompt_sha256']==fingerprint,'Prompt changed; replay is not comparable'
  response=record[index]['response']
 index+=1
 return response
client.call_llm=controlled
from review_v2.engine import review_contract_v2
from review_v2.user_profile import UserRiskProfile
text=(out.parent/round_name/'input/original.txt').read_text(encoding='utf8')
r=review_contract_v2(text,'technology',use_llm=True,profile=UserRiskProfile(user_identity=role))
(out/f'{name}_fixed_{mode}.json').write_text(json.dumps(r,ensure_ascii=False),encoding='utf8')
if mode=='baseline':(out/f'{name}_model_responses.json').write_text(json.dumps(record,ensure_ascii=False),encoding='utf8')
assert index==len(record)
print(mode,name,index,r['release_quality_gate']['status'],sorted(i['risk_group'] for i in r['risk_themes']))
