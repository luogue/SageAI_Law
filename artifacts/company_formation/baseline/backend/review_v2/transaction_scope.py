"""Source-bound transaction purpose and operative conditional facts.

Business registrations and document annotations are not performance promises.
Keep the original text for evidence; this view is only for trigger evaluation.
"""
import re


def operative_text(text):
    text = re.sub(r'[【\[][^】\]\n]*(?:用途|说明|提示|声明)[^】\]\n]*[】\]]', '', text)
    return re.sub(r'(?:经营范围|经营项目|主营业务)\s*[：:][^。\n]*', '', text)


def company_formation(text):
    source = operative_text(text)
    purpose = re.search(r'(?:共同|联合|合资|合作)(?:投资|出资)?(?:设立|成立|组建)[^。；\n]{0,65}(?:公司|企业)', source)
    groups = {
        'capital': r'注册资本|认缴(?:出资)?额',
        'contribution': r'出资额|出资方式|现金出资|以[^。\n]{0,30}出资',
        'ownership': r'股权|持股|股份比例',
        'governance': r'股东会|执行董事|董事会|监事|表决',
        'returns': r'利润分配|盈亏|分红|亏损',
    }
    hits = {key: m[0] for key, pattern in groups.items() if (m := re.search(pattern, source))}
    return {'established': bool(purpose and len(hits) >= 3),
            'purpose': purpose[0] if purpose else '', 'signals': hits}


def trigger_matches(text, term):
    source = operative_text(text)
    # Chinese substrings are not words: 测试用途 != 试用, 抽样品检 != 凭样品买卖.
    pattern = r'(?<!测)试用(?!途)' if term == '试用' else re.escape(term)
    for match in re.finditer(pattern, source):
        prefix = re.split(r'[。；，\n]', source[:match.start()])[-1][-18:]
        if re.search(r'(?:不涉及|不适用|不设|不约定|无需|没有|无|取消)[^，。；]{0,8}$', prefix):
            continue
        yield match
