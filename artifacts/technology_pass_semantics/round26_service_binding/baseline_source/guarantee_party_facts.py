"""One role-scoped guarantee party snapshot; signature templates are not identity."""
import re


def extract_guarantee_parties(text):
    rows = []
    header = re.compile(r'(?:^|[\n。；;])\s*(?:(?P<side>[甲乙丙丁]方)[（(]保证人[）)]|保证人[（(]?(?P<label>[一二三四AB12])?[）)]?)\s*[:：]\s*(?P<name>[^\n。；;]+)')
    for m in header.finditer(text):
        name=m['name'].strip()
        if name.startswith('指') or re.search(r'通信地址|联系方式',name):
            continue
        block=text[m.end():].split('\n',5)[:5]
        context=name+'\n'+'\n'.join(block)
        kind=('STATE_ORGAN' if re.search(r'政府|财政局|行政机关|机关法人|管委会',name) else
              'PUBLIC_NONPROFIT' if re.search(r'公益|非营利|公立|村委会|居委会',name) else
              'COMPANY' if re.search(r'公司|法人|合作社|合伙企业',name) else
              'NATURAL_PERSON' if re.search(r'身份证|自然人|个人',context) else 'UNKNOWN')
        names=re.split(r'[、与及]',name) if not re.search(r'公司|企业',name) else [name]
        for person in names:
            if person and not any(x['name']==person for x in rows):
                rows.append({'name':person,'side':m['side'] or m['label'] or '', 'party_type':kind, 'identity_quote':m.group().strip()})
    kinds={x['party_type'] for x in rows}
    joint=False
    for part in re.split(r'[。；;\n]', text):
        if '本合同' in part:
            part=part[part.rfind('本合同'):]
        if re.search(r'法律规定|民法典|例如|历史|原合同|旧合同|假如|如果|(?:不涉及|不存在|并非|不构成).{0,6}(?:共同|多个)', part):
            continue
        joint=joint or bool(re.search(r'共同(?:保证|担保)|(?:多个|两个以上|两名|两位)保证人', part))
    return {'guarantors':rows,'guarantor_count':len(rows),
            'guarantee_party_type':next(iter(kinds)) if len(kinds)==1 else 'MIXED' if kinds else 'UNKNOWN',
            'joint_guarantee':len(rows)>=2 or joint}


def signature_mismatches(text, parties):
    result=[]
    for party in parties['guarantors']:
        if not party['side']: continue
        pattern=rf'(?m)^\s*{re.escape(party["side"])}\s*[:：][^\n]*{re.escape(party["name"])}[^\n]*(?:\n[^\n]*)?'
        for m in re.finditer(pattern,text):
            block=m.group()
            corporate=bool(re.search(r'公章|法定代表人',block))
            personal=bool(re.search(r'签字|签名',block))
            if (party['party_type']=='NATURAL_PERSON' and corporate) or (party['party_type']=='COMPANY' and personal and not corporate and not re.search(r'授权|代表',block)):
                result.append({'party':party['name'],'quote':block,'reason':'主体身份与签署模板不一致，需核对实际签署主体及授权。'})
    return result
