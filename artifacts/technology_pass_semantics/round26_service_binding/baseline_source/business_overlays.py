"""Additive business regulation packs; never replace the primary registry."""
import re
from review_v2.priority_checklist_helpers import required as R

def external(number,node,title,instruction,law):
    return R('REG',number,node,title,('核验',),law,[(title,(r'(?!)',))],
        element_policies={0:{'requirement_kind':'EXTERNAL_VERIFICATION','verification_instruction':instruction,'verification_priority':'MEDIUM'}})

ROAD_LAW='《道路危险货物运输管理规定》《道路运输从业人员管理规定》'
PACKS={
 'DANGEROUS_ROAD_TRANSPORT':(r'(?:危险品|危险货物|危化品)[^。\n]{0,16}运输',(
  external(1,'reg_carrier_license','经营及实际承运主体许可核验','核验经营主体和实际承运人的道路危险货物运输许可、许可范围及有效状态。',ROAD_LAW),
  external(2,'reg_vehicle_documents','实际车辆准入及证件核验','核验实际投入车辆清单、道路运输证、检验有效期及适运范围；合同要求有证不等于证件真实有效。',ROAD_LAW),
  external(3,'reg_personnel','驾驶及押运人员资格核验','核验驾驶、押运及装卸管理人员对应从业资格、有效状态及与货物类别的匹配。',ROAD_LAW),
  external(4,'reg_insurance','实际投保及保障范围核验','核验保险单、缴费及承保状态、被保险人、保险期间、责任范围和除外责任。',ROAD_LAW),
  external(5,'reg_safety_management','安全管理及事故报告体系核验','核验安全管理人员、操作制度、应急预案、事故报告流程及演练记录；与合同安全义务分开审查。',ROAD_LAW))),
 'FOOD_OPERATION':(r'(?:食品|餐饮)[^。\n]{0,15}(?:经营|加盟|生产)|(?:经营|加盟)[^。\n]{0,15}(?:食品|餐饮)',(
  external(6,'reg_food_permission','食品经营准入材料核验','核验实际经营项目及对应食品生产经营许可或备案；按业务类别确认许可、备案或豁免条件。','《食品安全法》第35条'),)),
}

def relevance(text):
    """Separate the transaction's performance from incidental use of funds."""
    body='\n'.join(text.splitlines()[1:]) if '\n' in text else text
    result = {}
    for key, (pattern, _) in PACKS.items():
        hits = []
        for sentence in re.split(r'[。；\n]', body):
            if not re.search(pattern, sentence) or re.search(r'不涉及|不经营|不从事', sentence):
                continue
            background = bool(re.search(r'(?:借款|贷款|融资|资金)[^。；]{0,30}(?:用途|用于)|借款用途', sentence))
            dependency = bool(re.search(r'(?:须|应|必须)[^。；]{0,20}(?:取得|提供|持有)[^。；]{0,20}(?:许可|备案)|以[^。；]{0,20}许可[^。；]{0,10}为(?:前提|条件)', sentence))
            hits.append({'quote':sentence, 'regulatory_relevance_level': 'performance_dependency' if dependency else 'background_reference' if background else 'direct_subject'})
        if hits:
            level = next((h['regulatory_relevance_level'] for h in hits if h['regulatory_relevance_level'] != 'background_reference'), 'background_reference')
            result[key] = {'regulatory_relevance_level':level, 'evidence':hits,
                           'applicable':level != 'background_reference'}
    return result

def active(text):
    return [key for key, fact in relevance(text).items() if fact['applicable']]

def checkpoints(text):
    return tuple(c for k in active(text) for c in PACKS[k][1])

def augment(checklist,text):
    ids={c.item_id for c in checklist}
    return tuple(checklist)+tuple(c for c in checkpoints(text) if c.item_id not in ids)
