"""Compare identical recorded model output on the Round32 baseline/final source."""
from pathlib import Path
import sys,json,hashlib
root=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(root/'backend'),str(root)]
out=root/'artifacts/technology_pass_semantics/round32_patent_application_transfer'
prior=out.parent/'round31_transfer_consistency'
mode=sys.argv[1]
import review_v2
if mode=='baseline':review_v2.__path__.insert(0,str(out/'baseline_source'))
import reasoning.llm_client as client
record=json.loads((prior/'transfer_fixed_model_outputs.json').read_text(encoding='utf8'))
index=0
def controlled(prompt,*args,**kwargs):
 global index
 row=record[index]
 assert hashlib.sha256(prompt.encode()).hexdigest()==row['prompt_sha256'],'Changed prompt invalidates fixed-output control'
 index+=1
 return row['response']
client.call_llm=controlled
from review_v2.engine import review_contract_v2
from review_v2.user_profile import UserRiskProfile
r=review_contract_v2((prior/'input/original.txt').read_text(encoding='utf8'),'technology',use_llm=True,
 profile=UserRiskProfile(user_identity='乙方/让与方'))
assert index==len(record)
(out/f'fixed_model_{mode}.json').write_text(json.dumps(r,ensure_ascii=False),encoding='utf8')
print(mode,index,r['release_quality_gate']['status'],sorted(i['risk_group'] for i in r['risk_themes']))
