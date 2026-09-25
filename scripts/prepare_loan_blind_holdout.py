"""Generate sealed synthetic holdouts independently; never supplies regression failures."""
import concurrent.futures
import hashlib
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'backend')]
from backend.test_database_bootstrap import install
install()
from review_v2.deepseek_transport import request_json

OUT=ROOT/'artifacts/loan_blind_holdout'
SCENARIOS=['自然人之间无息短期借款，到期一次清偿', '自然人经营周转借款，月利率，分期还本',
    '企业设备采购借款，年利率，合同采用360日换算', '企业借款，按日利率，多个放款批次',
    '企业借款，年利率按实际年度天数计息，单利及逾期安排', '自然人借款，有明确复利条件和计算机制以及借据附件']

def generate(pair):
    index,scenario=pair
    body,raw=request_json('你是一位合同文书作者。输出JSON，不执行任何审查，不接收待测系统或失败样本。'
        '独立创作一份中文普通借款合同构造测试样本，约1200至2000字，采用自然的完整文书格式和具体虚构主体、金额、日期。'
        '不要写评价或答案提示。允许通常的起草缺口，但条款要自洽。不得复制既有合同。'
        'JSON字段text为合同全文，expected为你逐字文书明确的本金principal、currency、regular_rate（无息为null）、rate_period（无息为null）、compound布尔值。',
        {'scenario':scenario,'sample_number':index},stage='BLIND_DOCUMENT_AUTHORING')
    text=raw['text']
    if not isinstance(text,str) or len(text)<600:raise ValueError('holdout too short')
    path=OUT/f'blind-{index}.json'
    path.write_text(json.dumps(raw,ensure_ascii=False,indent=2),encoding='utf8')
    return {'id':f'blind-{index}','file':str(path),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
            'source_sha256':hashlib.sha256(text.encode()).hexdigest(),'source':'DEEPSEEK_SYNTHETIC_HOLDOUT','model':body.get('model')}

if __name__=='__main__':
    OUT.mkdir(parents=True,exist_ok=True)
    if (OUT/'manifest.json').exists():raise SystemExit('holdout already sealed; do not regenerate')
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        records=list(pool.map(generate,enumerate(SCENARIOS,1)))
    (OUT/'manifest.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf8')
    print('SEALED',len(records),'synthetic holdouts; content not displayed')
