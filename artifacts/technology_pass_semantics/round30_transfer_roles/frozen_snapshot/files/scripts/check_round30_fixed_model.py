"""Diagnostic only: capture live semantic outputs, then replay unchanged outputs on prior source."""
from pathlib import Path
import sys,json,hashlib
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'artifacts/technology_pass_semantics/round30_transfer_roles'
mode=sys.argv[1]
kind=sys.argv[2] if len(sys.argv)>2 else 'license'
party=sys.argv[3] if len(sys.argv)>3 else '乙方/被许可方'
label=kind+('_provider' if party.startswith('甲') else '')
location={'license':'round29_secret_license_aggregation','transfer':'round28_secret_transfer_binding'}[kind]
import review_v2
if mode=='baseline':review_v2.__path__.insert(0,str(OUT/'baseline_source'))
from dotenv import load_dotenv
load_dotenv(ROOT/'backend/.env')
import reasoning.llm_client as client
original=client.call_llm
path=OUT/f'{label}_fixed_model_outputs.json'
record=[] if mode=='capture' else json.loads(path.read_text(encoding='utf8'))
index=0
def controlled(prompt,*args,**kwargs):
 global index
 if mode=='capture':
  value=original(prompt,*args,**kwargs);record.append({'prompt_sha256':hashlib.sha256(prompt.encode()).hexdigest(),'response':value});path.write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf8')
 else:
  row=record[index];assert hashlib.sha256(prompt.encode()).hexdigest()==row['prompt_sha256'],'Prompt changed; same-output control invalid';value=row['response']
 index+=1
 return value
client.call_llm=controlled
from review_v2.engine import review_contract_v2
from review_v2.user_profile import UserRiskProfile
text=(ROOT/'artifacts/technology_pass_semantics'/location/'input/original.txt').read_text(encoding='utf8')
r=review_contract_v2(text,'technology',use_llm=True,profile=UserRiskProfile(user_identity=party))
(OUT/f'{label}_fixed_model_{mode}.json').write_text(json.dumps(r,ensure_ascii=False),encoding='utf8')
print(mode,index,r['release_quality_gate']['status'],sorted(i['risk_group'] for i in r['risk_themes']))
