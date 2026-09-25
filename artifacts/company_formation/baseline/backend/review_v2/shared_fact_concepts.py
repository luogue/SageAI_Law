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

# Negation is evaluated within the actual supporting source, not the whole report.
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
