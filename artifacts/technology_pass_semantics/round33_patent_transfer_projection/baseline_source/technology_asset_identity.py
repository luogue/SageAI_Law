"""Operative transfer objects, distinct from confidential supporting materials."""
import re
from review_v2.clause_parser import parse_contract_clauses


def transfer_assets(text):
    facts = {key: [] for key in ('patent_identifier', 'patent_grant', 'patent_registration',
                                 'secret_transaction')}
    patterns = {
        'patent_identifier': r'专利(?:号|编号)[：:]?\s*(?:ZL|CN)\s*\d[\d.]+',
        'patent_grant': r'授权(?:公告)?(?:日|日期|号)|(?:已取得|已经|已获)授权|登记专利权人',
        'patent_registration': r'专利权(?:人)?(?:转让|变更)登记',
        # A secret itself must be the granted object. Returning/deleting
        # confidential material or delivering patent documents is not a grant.
        'secret_transaction': r'(?:将|就)(?:下列|本项|该)?(?:技术秘密|非专利技术|专有技术)(?:权利)?'
                              r'(?:整体|全部|一并)?(?:转让|许可)|'
                              r'(?:转让|许可)(?:给[^，。；]{1,15})?(?:下列|本项|该)?'
                              r'(?:技术秘密|非专利技术|专有技术)(?!资料|文件)',
    }
    for clause in parse_contract_clauses(text):
        for match in re.finditer(r'[^。；;\n]+[。；;]?', clause.text):
            quote = match[0].strip()
            for key, pattern in patterns.items():
                if re.search(pattern, quote, re.I):
                    facts[key].append(dict(clause_id=clause.clause_id, quote=quote))
    return facts
