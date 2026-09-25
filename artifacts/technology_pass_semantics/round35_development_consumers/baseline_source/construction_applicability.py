"""Shared construction tender trigger facts."""
import re

TENDER_TERMS = ('招标','投标','中标','中标通知书','招标文件','投标文件','评标','备案合同')
def tender_fact(text):
    body=str(text or '')
    if re.search(r'(?:不涉及|未进行|无需|不需要|不属于).{0,12}(?:招标|投标)',body):
        return {'status':'NOT_TRIGGERED','triggered':False,'evidence':[],'reason':'合同明确不涉及招投标场景。'}
    hits=[term for term in TENDER_TERMS if term in body]
    return {'status':'TRIGGERED' if hits else 'NOT_TRIGGERED','triggered':bool(hits),'evidence':hits,
            'reason':'合同存在招投标/中标事实。' if hits else '未发现招标、投标、中标或备案合同事实。'}

def applies(text):
    return tender_fact(text)['triggered']
