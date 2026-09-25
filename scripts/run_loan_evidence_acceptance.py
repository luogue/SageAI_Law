import asyncio,io,json
from pathlib import Path
from routers.review_v2 import review_v2_file

async def main():
    path=Path('test_data/72 无抵押借款.docx')
    class Upload:
        filename=path.name
        file=io.BytesIO(path.read_bytes())
    r=await review_v2_file(file=Upload(),contract_type='loan',include_low_risk=True,use_llm=False,profile_json='{}',current_user={'id':'regression'})
    out=Path('artifacts/loan_evidence_acceptance'); out.mkdir(parents=True,exist_ok=True)
    (out/'report.json').write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8')
    (out/'report.md').write_text(r['result'],encoding='utf-8')
    for i in r['items']:
        if i['item_id'] in ['L-03-02','L-03-04','L-05-01','L-06-02','L-12-03','L-12-04','L-04-02','L-05-02']:
            print(i['item_id'],i['coverage_status'],i.get('evidence_location'),i.get('reasoning_summary'))
    print(r['release_quality_gate']['status'],r['release_quality_gate']['failures'])
asyncio.run(main())
