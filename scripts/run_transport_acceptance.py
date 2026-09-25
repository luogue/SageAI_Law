import asyncio, io, json, sys
from pathlib import Path
from routers.review_v2 import review_v2_file

async def main():
    path=Path(sys.argv[2] if len(sys.argv)>2 else 'test_data/78 运输合同.docx')
    class Upload:
        filename=path.name
        file=io.BytesIO(path.read_bytes())
    result=await review_v2_file(file=Upload(),contract_type='transportation',include_low_risk=True,use_llm=False,profile_json='{}',current_user={'id':'regression'})
    out=Path('artifacts/transport_acceptance'); out.mkdir(parents=True,exist_ok=True)
    name=sys.argv[1] if len(sys.argv)>1 else 'after'
    (out/(name+'.json')).write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    (out/(name+'.md')).write_text(result['result'],encoding='utf-8')
    print(result['release_quality_gate'])
asyncio.run(main())
