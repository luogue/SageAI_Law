"""Sentence-bound brokerage concepts reused by independent requirement owners.

No review IDs or document strings: each binding still runs supports() against
original evidence. Composite rules retain their separate required elements.
"""
GAP = r'[^。；;\n]{0,140}'
FEE = r'(?:中介(?:服务)?费(?:用)?|居间费|中介报酬|报酬|佣金)'
BROKER = r'(?:乙方|中介人|居间人)'
CLIENT = r'(?:甲方|委托人|委托方)'
COUNTERPART = r'(?:第三方|第三人|购买方|客户|交易对象|交易对方)'
INTRO = r'(?:中介引荐|引荐|推介|介绍)'
SIGN = r'(?:签订|订立|签署|签约)'

CONCEPTS = {
    'no_service_obstruction': {
        'patterns': [rf'{CLIENT}不得(?:无故|恶意)?(?:拒绝|拖延|拒绝、拖延){GAP}{BROKER}{GAP}(?:中介服务|居间服务|履行){GAP}(?:协助|配合)',
                     rf'{CLIENT}不得(?:无故|恶意)?(?:拒绝|拖延|阻碍|妨碍){GAP}(?:中介|居间)(?:服务|履行)'],
        'excluded': [r'(?:有权|可以|允许)(?:无故)?(?:拒绝|拖延|阻碍|妨碍)'],
    },
    'defined_brokerage_object': {
        'patterns': [rf'{BROKER}(?:接受{CLIENT}委托[，,]?)?为(?:本项目|该项目|本标的|标的公司|指定项目){GAP}(?:中介引荐|提供中介服务|提供居间服务)',
                     rf'(?:中介|居间)服务(?:仅限于|限于|针对)[^。；;\n]{{2,80}}(?:项目|公司|股权|资产|交易)'],
        'excluded': [r'(?:项目|标的|服务范围)(?:尚未|未予|未)(?:确定|明确)',
                     r'(?:不提供|无需提供)(?:中介|居间)服务'],
    },
    'undertaken_mediation_work': {
        'patterns': [rf'{BROKER}(?:接受{CLIENT}委托|负责|应当){GAP}(?:引荐|介绍|组织磋商){GAP}促成{GAP}{SIGN}',
                     rf'{BROKER}(?:负责|应当|应|须)(?:尽力|积极|勤勉)?促成{GAP}{SIGN}'],
        'excluded': [r'(?:如果|若|仅当|未能|未必|不负责|无需|不得).{0,30}促成',
                     r'(?:以|作为)(?:服务)?目标'],
    },
    'introduce_counterparty': {
        'patterns': [rf'{BROKER}{GAP}{INTRO}{COUNTERPART}',
                     rf'{BROKER}{GAP}提供(?:交易|订约|订立合同的)机会'],
        'excluded': [rf'(?:无需|不负责|不提供|不承担|不得){GAP}{INTRO}',
                     r'(?:无需|不负责|不得)提供(?:交易|订约)机会'],
    },
    'mediate_contract': {
        'patterns': [rf'{BROKER}{GAP}(?:促成|撮合){GAP}{SIGN}',
                     rf'{BROKER}{GAP}(?:负责|应当|提供)(?:撮合交易|媒介服务)'],
        'excluded': [r'(?:不负责|无需|不得|未能)(?:促成|撮合)',
                     r'(?:不负责|无需|不得)提供媒介服务'],
    },
    'success_triggers_payment': {
        'patterns': [rf'{BROKER}{GAP}中介(?:获得)?成功{GAP}{CLIENT}{GAP}(?:支付|给付){FEE}',
                     rf'(?:中介|居间)成功(?:后|时|的){GAP}{CLIENT}{GAP}(?:支付|给付){FEE}'],
        'excluded': [rf'(?:无需|不必|不应|不得|不)(?:支付|给付){FEE}',
                     r'(?:未成功|不成功|未获得成功)'],
    },
    'principal_pays_broker': {
        'patterns': [rf'{CLIENT}{GAP}向{BROKER}支付{FEE}',
                     rf'{FEE}由{CLIENT}(?:承担|支付|负担)',
                     rf'{BROKER}(?:有权|可以|可)向{CLIENT}收取{FEE}'],
        'excluded': [rf'{CLIENT}(?:无需|无须|不必|不得){GAP}支付{FEE}',
                     rf'{BROKER}(?:无权|不得)向{CLIENT}收取{FEE}'],
    },
    'signed_referral_record': {
        'patterns': [rf'{BROKER}{GAP}(?:报备确认单|客户确认单|客户名单){GAP}{CLIENT}{GAP}(?:签字|盖章|签署|确认)'],
        'excluded': [r'(?:未经|无需|不经)甲方.{0,15}(?:签字|盖章|确认)'],
    },
    'introduced_party_transaction': {
        'patterns': [rf'{CLIENT}{GAP}与{BROKER}(?:所)?(?:推介|介绍|引荐){GAP}{COUNTERPART}{GAP}{SIGN}'],
        'excluded': [rf'(?:未利用|并非|不是){GAP}{BROKER}{GAP}(?:推介|介绍|引荐)'],
    },
    'anti_evasion_payment': {
        'patterns': [rf'{CLIENT}不得私下{GAP}{COUNTERPART}{GAP}规避{GAP}(?:支付|给付){GAP}{FEE}',
                     rf'{CLIENT}{GAP}与{BROKER}(?:所)?(?:推介|介绍|引荐){GAP}{COUNTERPART}{GAP}{SIGN}{GAP}{CLIENT}{GAP}支付{FEE}'],
        'excluded': [rf'(?:无需|不必|免于)支付{FEE}'],
    },
}

# Ownership is explicit; evidence is not copied from a rule's PASS verdict.
BINDINGS = {
    'broker_no_obstruction': ('no_service_obstruction',),
    'broker_service_area': ('defined_brokerage_object',),
    'broker_diligence': ('undertaken_mediation_work',),
    'broker_nature': ('introduce_counterparty', 'mediate_contract'),
    'broker_no_agency': ('introduce_counterparty', 'mediate_contract'),
    'broker_report_scope': ('introduce_counterparty',),
    'broker_media_scope': ('mediate_contract',),
    'broker_commission_trigger': ('success_triggers_payment',),
    'broker_commission_allocation': ('principal_pays_broker',),
    'broker_principal_payment': ('principal_pays_broker',),
    'broker_service_received': ('signed_referral_record',),
    'broker_service_records': ('signed_referral_record',),
    'broker_proof_materials': ('signed_referral_record',),
    'broker_opportunity_used': ('introduced_party_transaction',),
    'broker_bypass_contract': ('anti_evasion_payment',),
}


def attach_concepts(profiles):
    for elements in profiles.values():
        for element in elements:
            names = BINDINGS.get(element['element_id'], ())
            if not names:
                continue
            element['semantic_concepts'] = list(names)
            element['semantic_patterns'] = list(element['semantic_patterns']) + [
                p for name in names for p in CONCEPTS[name]['patterns']]
            element['excluded_patterns'] = list(element.get('excluded_patterns', [])) + [
                p for name in names for p in CONCEPTS[name]['excluded']]
