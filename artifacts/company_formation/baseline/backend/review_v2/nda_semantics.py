"""NDA scenario and source-verifiable requirements, shared across NDA variants."""
import re
from copy import deepcopy
from review_v2.lease_semantics import requirement


def scenario(text):
    employment = re.search(r'(?:双方|甲乙双方).{0,25}(?:建立|存在|订立|签订).{0,12}(?:劳动关系|劳动合同)|(?:乙方|接受方|接收方).{0,15}(?:为|系|是|担任).{0,25}(?:员工|雇员|劳动者)|(?:员工|劳动者)保密协议|(?:本协议|本合同).{0,10}适用于.{0,10}(?:雇员|员工|劳动者)', text)
    return 'EMPLOYMENT_NDA' if employment else 'INSTITUTIONAL_NDA'


def resolve(node, requirements, text):
    rows=deepcopy(requirements)
    if node=='employment_secret_scope':
        rows[0]['contextual_patterns']=[{'context':r'保密信息','predicate':r'(?:^|\n)指[^。]{10,}'}]
        rows[0]['preferred_patterns']=[r'(?:^|\n)指[^。]{10,}']
        rows[0]['evidence_unit']='clause'
        exceptions = [
            ('public', '合法公开或进入公共领域的信息除外', r'公开|公共领域'),
            ('prior', '接受方原已知悉或持有的信息除外', r'原已知悉|原已拥有|(?:披露.{0,15}之前|披露前|原先).{0,20}(?:拥有|持有|知悉)'),
            ('independent', '独立开发取得的信息除外', r'独立开发|独立研发|自行研发|自行开发'),
            ('third_party', '从无保密义务第三方合法取得的信息除外', r'(?:第三方|第三人).{0,35}(?:合法|不受|无保密)|(?:合法|无保密).{0,25}(?:第三方|第三人)'),
            ('mandatory', '依法强制披露的信息除外', r'(?:政府机关|法庭|法院|监管机构|法律).{0,25}(?:要求|规定).{0,15}披露'),
        ]
        rows=rows[:1]
        for key,label,predicate in exceptions:
            row=requirement('nda_exception_'+key,label,
                r'(?:不包括|除外|不属于|无需保密)[\s\S]{0,700}(?:'+predicate+r')',
                r'(?:'+predicate+r')[^。]{0,60}(?:除外|不属于|无需保密)')
            row.update(evidence_unit='clause', contextual_patterns=[{'context':r'不包括|除外|不属于','predicate':predicate}])
            rows.append(row)
    if node=='confidentiality_parties':
        rows=[
            requirement('confidentiality_parties_1','协议第一方主体可识别',r'(?:^|[。；\n])\s*(?:甲方|披露方|信息提供方|用人单位)(?:[（(][^）)]{1,20}[）)])?\s*[：:]\s*[^。；\n_]{2,80}'),
            requirement('confidentiality_parties_2','协议第二方主体可识别',r'(?:^|[。；\n])\s*(?:乙方|接受方|接收方|劳动者)(?:[（(][^）)]{1,20}[）)])?\s*[：:]\s*[^。；\n_]{2,80}'),
            requirement('confidentiality_information_flow','披露与接受信息的角色或双向流向',
                r'披露方\s*[：:][^。]{2,80}[。；].{0,10}(?:接受方|接收方)\s*[：:][^。]{2,80}',
                r'(?:披露方|信息提供方).{0,50}(?:是指|指|为).{0,100}(?:接受方|接收方)',
                r'(?:双方|一方).{0,50}(?:向对方|向另一方).{0,20}披露',
                r'(?:甲方|公司).{0,30}(?:向|提供给)(?:乙方|员工|劳动者).{0,30}(?:保密信息|商业秘密)')]
        rows[-1]['evidence_unit']='clause'
    if node=='confidentiality_remedies':
        rows[0].update(evidence_unit='clause', semantic_patterns=[
            r'(?:违反[^。；]{0,20}保密|泄露[^。；]{0,15}(?:信息|秘密)|未经授权披露)[^。]{0,100}(?:赔偿|补偿|停止披露|停止侵害|消除影响|违约金|救济|补救)',
            r'(?:下述|下列|以下)违约[^：:。]{0,180}(?:赔偿|违约金)[^：:。]{0,80}[：:][\s\S]{0,300}(?:违反[^。；]{0,20}保密义务|未经[^。；]{0,30}披露[^。；]{0,20}保密信息)',
            r'(?:披露方|守约方)[^。]{0,25}有权[^。]{0,35}(?:违反保密|泄露秘密)[^。]{0,30}(?:救济|补救)'],
            contextual_patterns=[{'context':r'保密违约责任|违反保密义务的责任|泄密责任',
                'predicate':r'(?:损害赔偿|赔偿|补偿).{0,60}(?:损失|损害)|停止侵害|停止披露'}],
            excluded_patterns=[r'(?:无需|不必|免于|不承担).{0,8}(?:赔偿|补偿|损害赔偿)'])
    return rows


def apply_scenario(items, clauses):
    text='\n'.join(c.text for c in clauses)
    variant=scenario(text)
    for item in items:
        if item.item_id.startswith('NDA-'):
            item.decision_trace['nda_scenario']={'variant':variant,'selection_basis':'EXPLICIT_EMPLOYMENT_RELATIONSHIP' if variant=='EMPLOYMENT_NDA' else 'NO_ESTABLISHED_EMPLOYMENT_RELATIONSHIP'}
            if variant=='INSTITUTIONAL_NDA':
                item.legal_basis_index='《民法典》第501条、第509条、第577条'
                item.legal_consequence_if_missing='相关约定不明确时，协议双方对保密信息使用、保护及违约救济的履行可能产生争议。'
