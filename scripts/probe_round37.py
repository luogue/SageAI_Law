import sys,json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(root/'backend'),str(root)]
from review_v2.engine import review_contract_v2
import review_v2.engine as engine
original_project=engine._project_atomic_requirement_state
def traced_project(item,family,*args,**kwargs):
    if item.item_id=='TC-12-02':
        print('PROJECT_INPUT',family,item.coverage_status,item.coverage_presence,item.applicability,kwargs.get('allow_empty'))
    return original_project(item,family,*args,**kwargs)
engine._project_atomic_requirement_state=traced_project
from review_v2.user_profile import UserRiskProfile
out=root/'artifacts/technology_pass_semantics/round37_export_blockers'
r=review_contract_v2((out/'input/original.txt').read_text(encoding='utf8'),'technology',use_llm=False,profile=UserRiskProfile(user_identity='甲方'))
(out/'probe.json').write_text(json.dumps(r,ensure_ascii=False),encoding='utf8')
print(json.dumps({'status':r['release_quality_gate']['status'],'failures':r['release_quality_gate']['failures']},ensure_ascii=False))
