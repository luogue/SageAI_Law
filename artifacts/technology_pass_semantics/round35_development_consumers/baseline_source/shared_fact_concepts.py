"""Reusable source-bound concepts. Rule configuration selects concepts, never outcomes."""
from copy import deepcopy
from review_v2.lease_semantics import requirement, corpus_facts

CONCEPTS = {
 'accepted_handover': requirement('accepted_handover','接收方验收、接收或封存的交付机制',r'(?:移交|交付)[^。；]{0,30}(?:验收|接收|封存)[^。；]{0,20}(?:交付完成|接收完成)',r'(?:接收方|保管人|仓储方)[^。；]{0,25}(?:接收|占有|实际控制)[^。；]{0,15}(?:货物|物品|保管物)'),
 'custody_duty': requirement('custody_duty','接收方承担看管和管理义务',r'(?:应当|应|负责)[^。；]{0,15}(?:妥善保管|看管|保管和管理)',r'(?:保管人|仓储方)[^。；]{0,25}实际控制'),
 'custody_negligence_compensation': requirement('custody_negligence_compensation','保管不善导致毁损灭失的赔偿责任',r'(?:保管不善|未尽[^。；]{0,10}保管义务)[^。；]{0,35}(?:毁损|灭失|损坏)[^。；]{0,35}(?:应当|应|负责|承担)[^。；]{0,12}(?:赔偿|赔偿责任)'),
 'handover_receipt': requirement('handover_receipt','接收方出具交付接收凭证',r'(?:出具|签发|交付)[^。；]{0,30}(?:保管凭证|仓单|寄存单|接收凭证|交接单|签收单)'),
 'incidental_service_fees': requirement('incidental_service_fees','附加服务费用项目及计费安排',r'(?:装卸|清点|搬运|保险|附加服务)[^。；]{0,45}(?:费|费用)[^。；]{0,90}(?:[0-9]+元|一次性|承担|支付|收取)'),
 'overdue_service_fees': requirement('overdue_service_fees','逾期费用承担或计算方法',r'逾期[^。；]{0,60}(?:支付|承担)[^。；]{0,45}(?:费用|费|元)'),
 'expense_verification': requirement('expense_verification','额外费用的凭证或核验安排',r'(?:额外费用|其他费用|装卸费|搬运费|保险费|处置费用)[^。；]{0,40}(?:凭证|发票|核验|单据)',r'(?:提供|出具)[^。；]{0,15}(?:费用凭证|费用发票)'),
 'attachment_effect': requirement('attachment_effect','附件作为合同组成部分及效力',r'附件[^。；]{0,60}(?:同等(?:法律)?效力|组成部分)'),
 'document_precedence': requirement('document_precedence','正文附件冲突时的适用顺序',r'(?:附件|正文|合同文件)[^。；]{0,40}(?:冲突|不一致)[^。；]{0,45}(?:优先|为准|顺序)',r'(?:附件|正文|合同文件)[^。；]{0,30}(?:优先顺序|顺序适用|顺序解释)'),
 'lien_exclusion': requirement('lien_exclusion','明确排除或限制留置权',r'(?:不得|禁止)[^。；]{0,20}(?:留置|扣留)',r'(?:排除|放弃|限制)留置权'),
}
CONCEPTS['incidental_service_fees']['semantic_patterns']=[r'(?:装卸|清点|搬运|保险|附加服务)[^。]{0,45}(?:费|费用)[^。]{0,90}(?:[0-9]+元|一次性|承担|支付|收取)']
CONCEPTS['incidental_service_fees']['evidence_unit']='clause'
CONCEPTS['disposal_cost_allocation']=requirement('disposal_cost_allocation','处置费用承担或价款扣除安排',r'(?:处置所得|所得价款)[^。]{0,80}处置费用[^。]{0,40}(?:剩余|返还)',r'处置费用[^。；]{0,25}(?:由[^。；]{0,10}承担|扣除|抵扣)')
CONCEPTS.update({
 'remuneration_determinable': requirement('remuneration_determinable','报酬金额、计算方式或明确无偿安排',
    r'(?:保管费|服务费|仓储费|报酬)(?:计算方式|计算标准|标准|金额)?(?:为|是|按|按照|计算为|计为|：|:|\s){1,6}(?:每月|每年|每天|每日|每件|按月|按日)?(?:人民币)?[0-9]+(?:\.[0-9]+)?元',
    r'(?:本合同|本服务)(?:为|属于|系)(?:无偿|免费)',r'双方(?:明确)?约定(?:不收取|免收)(?:保管费|服务费|仓储费|报酬)'),
 'uncertain_remuneration_default': requirement('uncertain_remuneration_default','报酬无法确定时的处理后果',r'(?:费用|报酬|保管费)[^。；]{0,25}(?:不明|无法确定|未约定)[^。；]{0,40}(?:无偿|免费|补充协商)'),
 'unauthorized_delegation_control': requirement('unauthorized_delegation_control','未经同意委托第三人受到限制',
    r'未经[^。；]{0,20}同意[^。；]{0,35}(?:不得|禁止)[^。；]{0,25}(?:转交|委托)[^。；]{0,15}第三人',
    r'未经[^。；]{0,20}同意[^。；]{0,35}(?:转交|委托)[^。；]{0,15}第三人[^。；]{0,40}损失[^。；]{0,25}赔偿'),
 'unauthorized_delegation_liability': requirement('unauthorized_delegation_liability','未经授权交第三人履行造成损失的赔偿责任',
    r'未经[^。；]{0,20}同意[^。；]{0,35}(?:转交|委托)[^。；]{0,15}第三人[^。；]{0,40}损失[^。；]{0,25}(?:承担|赔偿)'),
 'authorized_delegation_liability': requirement('authorized_delegation_liability','经授权交第三人履行后的对外责任承担',
    r'(?<!未)经[^。；]{0,20}同意[^。；]{0,30}(?:转交|委托|转保管)[^。；]{0,45}(?:仍应|仍由|继续|连带)[^。；]{0,25}(?:承担|赔偿|负责)'),
 'gratuitous_fault_standard': requirement('gratuitous_fault_standard','无偿履行时故意或重大过失的责任标准',
    r'无偿[^。；]{0,35}证明[^。；]{0,12}没有故意或者重大过失[^。；]{0,15}不承担赔偿责任',
    r'无偿[^。；]{0,35}(?:故意|重大过失)[^。；]{0,30}(?:应当|应|承担)[^。；]{0,15}赔偿责任'),
})
CONCEPTS['remuneration_determinable']['excluded_patterns']=[r'例如|假设|拟定|待定|待协商|尚未确定']
CONCEPTS['unauthorized_delegation_liability']['excluded_patterns']=[r'(?:不承担|无需承担|免除)[^。；]{0,10}赔偿责任']
CONCEPTS['authorized_delegation_liability']['excluded_patterns']=[r'未经[^。；]{0,20}同意']
CONCEPTS['authorized_delegation_liability']['applicability_condition']={
 'description':'允许经同意交第三人履行的机制',
 'negative_patterns':[r'(?:不允许|禁止|不得)[^。；]{0,25}(?:转交|委托)[^。；]{0,15}第三人',
                      r'☐是☑否允许[^。；]{0,25}(?:转交|委托)[^。；]{0,15}第三人'],
 'positive_patterns':[r'(?<!不)允许[^。；]{0,25}(?:转交|委托)[^。；]{0,15}第三人',
                      r'(?<!未)经[^。；]{0,20}同意[^。；]{0,20}(?:可|可以)[^。；]{0,20}(?:转交|委托|转保管)',
                      r'(?<!未)经[^。；]{0,20}同意转保管'],
}
CONCEPTS['return_entrusted_property']=requirement('return_entrusted_property','接收方负有归还受托财物的义务',
 r'(?:应当|应|须|负责)[^。；]{0,15}(?:将|把)(?:保管物|寄存物|受托财物|物品)[^。；]{0,10}(?:归还|返还)',
 r'(?:应当|应|须|负责)(?:归还|返还)(?:保管物|寄存物|受托财物|原物)')
CONCEPTS['return_entrusted_property']['excluded_patterns']=[r'(?:不|无需|不必)(?:应当|应)?(?:返还|归还)']
CONCEPTS['return_property_fruits']=requirement('return_property_fruits','返还受托财物产生的孳息或收益',
 r'(?:应当|应|须)[^。；]{0,20}(?:返还|归还|交还|交付)[^。；]{0,25}(?:孳息|收益|利息|分红|果实)',
 r'(?:孳息|收益|利息|分红|果实)[^。；]{0,20}(?:应|须|归)[^。；]{0,20}(?:寄存人|委托人|甲方|返还|归还)')
CONCEPTS['return_property_fruits']['excluded_patterns']=[r'(?:不|无需)(?:返还|归还|交付)']
CONCEPTS['return_property_fruits']['applicability_condition']={
 'description':'受托财物存在产生孳息或财产收益的场景', 'on_absence':'NOT_TRIGGERED',
 'positive_patterns':[
  r'(?:保管物|寄存物|受托财物|所保管的财产)[^。；]{0,45}(?:孳息|收益|利息|租金|分红|果实|牲畜|奶牛|母牛|母羊|果树)',
  r'(?:保管|寄存|看管)(?:的)?(?:牲畜|奶牛|母牛|母羊|果树)',
  r'(?:保管期间|寄存期间)[^。；]{0,30}(?:产生|取得|获得)[^。；]{0,20}(?:孳息|收益|利息|租金|分红|果实)',
  r'(?:孳息|收益|利息|分红|果实)[^。；]{0,20}(?:返还|归还|交还)(?:寄存人|委托人|甲方)',
 ],
 'negative_patterns':[r'(?:保管物|寄存物)[^。；]{0,20}(?:不产生|不存在)(?:孳息|收益|利息)'],
}
CONCEPTS['depositor_packaging_duty']=requirement('depositor_packaging_duty','交付方承担必要包装责任',
 r'(?:甲方|寄存人|存货人|交付方|委托人)[^。；]{0,12}(?:应当|应|须|负责)[^。；]{0,35}(?:完成|提供|进行|采用)[^。；]{0,12}(?:包装|封装)',
 r'(?:包装|封装)[^。；]{0,10}由(?:甲方|寄存人|存货人|交付方|委托人)(?:负责|承担)')
CONCEPTS['depositor_delivery_assistance']=requirement('depositor_delivery_assistance','交付方承担交付协助义务',
 r'(?:甲方|寄存人|存货人|交付方|委托人)[^。；]{0,12}(?:应当|应|须|负责)[^。；]{0,45}(?:协助|配合)[^。；]{0,15}(?:交付|移交|验收|入库|清点)',
 r'(?:甲方|寄存人|存货人|交付方|委托人)[^。；]{0,12}(?:应当|应|须)[^。；]{0,20}提供[^。；]{0,15}(?:交付资料|入库资料|交接资料)')
for _key in ('depositor_packaging_duty','depositor_delivery_assistance'):
 CONCEPTS[_key]['excluded_patterns']=[r'(?:无需|不必|不承担)[^。；]{0,15}(?:包装|协助|配合)']

# Negation is evaluated within the actual supporting source, not the whole report.
CONCEPTS.update({
 'movement_records': requirement('movement_records','建立或保存财物出入、交接流转记录',
    r'(?:应当|应|须|负责)[^。；]{0,15}(?:建立|保存|留存|提供)[^。；]{0,20}(?:出入库|入出库|出入|交接|进出)[^。；]{0,8}(?:记录|台账)',
    r'(?:出入库|入出库|交接)(?:记录|台账)[^。；]{0,15}(?:应当|应|须)[^。；]{0,12}(?:保存|留存|提供)'),
 'retained_visual_records': requirement('retained_visual_records','保存可核验的照片、视频或监控资料',
    r'(?:保存|保留|留存|提供)[^。；]{0,30}(?:视频监控资料|监控录像|监控资料|照片|视频)[^。；]{0,20}(?:记录|资料|日|天|年|备查)',
    r'(?:照片|视频|监控)(?:记录|资料|录像)[^。；]{0,20}(?:应当|应|须)[^。；]{0,12}(?:保存|留存|保留)'),
 'signed_handover_record': requirement('signed_handover_record','交接凭证具备双方签认机制',
    r'(?:双方签名|双方签字|双方签章|双方盖章)[^。；]{0,25}(?:保管凭证|交接单|签收单|交接记录|接收凭证)',
    r'(?:保管凭证|交接单|签收单|交接记录|接收凭证)[^。；]{0,25}(?:双方签名|双方签字|双方签章|双方盖章)'),
 'retrieval_workflow': requirement('retrieval_workflow','约定领取、返还时的办理条件或协作步骤',
    r'(?:领取|取回)[^。；]{0,35}(?:支付|结清)[^。；]{0,25}(?:后|时)[^。；]{0,25}(?:归还|返还)',
    r'(?:领取|取回)[^。；]{0,35}(?:应|须)[^。；]{0,25}(?:提前|出示|提交|签署)[^。；]{0,25}(?:通知|凭证|证明|确认单)'),
 'acceptance_record': requirement('acceptance_record','验收或封存状态形成交接记录或凭证',
    r'(?:验收|封存)[^。]{0,100}(?:出具|签发|记录|登记)[^。]{0,25}(?:凭证|单据|记录|清单)',
    r'(?:出具|签发)[^。；]{0,25}(?:验收单|封存记录|验收记录|状态记录)'),
})
for _key in ('movement_records','retained_visual_records','signed_handover_record','retrieval_workflow','acceptance_record'):
 CONCEPTS[_key]['excluded_patterns']=[r'(?:无需|不必|不予|不得)(?:建立|保存|保留|留存|提供|出具|签署)',r'(?:记录|台账|凭证)(?:尚未|未)(?:建立|保存|提供)']
CONCEPTS['acceptance_record']['evidence_unit']='clause'
CONCEPTS['custody_negligence_compensation']['excluded_patterns']=[r'(?:不承担|无需承担|免除)[^。；]{0,10}赔偿责任']
CONCEPTS['handover_receipt']['excluded_patterns']=[r'(?:不|无需|不必)出具']

def requirements(keys):
 return [deepcopy(CONCEPTS[k]) for k in keys]

def register(node,keys):
 from review_v2.priority_checklist_helpers import PROFILES
 PROFILES[node]=requirements(keys)

def pool(clauses,keys):
 """A single concept is evaluated once per request and is reusable by consumers."""
 return corpus_facts(clauses,requirements(tuple(dict.fromkeys(keys))))
