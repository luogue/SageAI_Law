"""Exit settlement requirements; never loaded for ordinary ongoing employment."""
from review_v2.priority_checklist_helpers import required as R, forbidden as F, PROFILES
from dataclasses import replace

L = '《劳动合同法》第26条、第30条、第46条、第47条、第50条；《工资支付暂行规定》第9条、第15条、第16条'
SETTLEMENT = R('ET', 2, 'termination_settlement', '离职劳动报酬结算', ('工资','奖金','年休假'), L, [
    ('工资及奖金等应付报酬清单或核对安排', (r'(?:工资|劳动报酬)[^。]{0,100}(?:\d+元|结清|结算)',)),
    ('未休年休假工资结算或核对', (r'未休(?:年休假|年假)[^。]{0,30}(?:工资|结算)|不存在其他未支付[^。]{0,80}未休',)),
])
CALCULATION = R('ET', 3, 'termination_compensation_calculation', '补偿或赔偿金计算明细', ('经济补偿','赔偿金','工作年限'), L, [
    ('补偿或赔偿金额及依据', (r'(?:经济补偿|赔偿|应支付)[^。]{0,120}\d+(?:\.\d+)?元',)),
    ('计入补偿的工作年限', (r'(?:连续工作|工作年限)[^。]{0,20}\d+年',)),
    ('补偿计算工资基数', (r'(?:前|过去)(?:十二|12)个月平均工资[^。]{0,20}\d+元',)),
], trigger=('经济补偿','赔偿金'))
WITHHOLD = F('ET', 4, 'termination_payment_withholding', '到期报酬与交接挂钩或单方暂缓支付', ('交接','暂缓支付','劳动报酬'), L, (
    r'(?:工资|劳动报酬|上述款项)[^。；\n]{0,90}(?:完成|办结)[^。；\n]{0,20}交接[^。；\n]{0,30}(?:支付|结算)',
    r'(?:甲方|用人单位)[^。；\n]{0,20}(?:有权|可以|可)(?:暂缓|延迟|暂停)支付[^。；\n]{0,30}(?:工资|劳动报酬)',
), '到期劳动报酬与经济补偿分开结算，不能以未完成交接为由当然扣留工资；经济补偿按法定交接结算规则处理。')
DEDUCTION = F('ET', 5, 'termination_direct_deduction', '工资补偿单方直接扣款', ('扣除','培训费用','损失'), L, (
    r'(?:甲方|用人单位)[^。；\n]{0,60}(?:直接|自行|单方)扣除[^。；\n]{0,90}(?:财物|培训|损失|借款)',
), '分别核实债务依据、损失责任和金额，依法处理工资扣减限额及争议程序，不以概括授权直接扣除全部工资或补偿。')
WAIVER = F('ET', 6, 'termination_remedy_waiver', '概括排除劳动争议救济及撤销权', ('放弃','仲裁','诉讼','撤销'), L+'；劳动争议司法解释（一）第35条', (
    r'(?:乙方|劳动者)[^。；\n]{0,80}放弃[^。；\n]{0,100}(?:仲裁|诉讼|投诉|举报)',
    r'(?:双方|乙方|劳动者)[^。；\n]{0,15}不得以任何理由[^。；\n]{0,20}(?:撤销|仲裁|诉讼)',
), '区分已核实款项的有效结算与概括放弃救济；保留法定仲裁、诉讼及符合条件时撤销协议的权利，不直接否定全部结算协议。')
STOPPAGE = R('ET', 7, 'termination_insurance_stoppage', '社保及公积金停缴衔接', ('社保','社会保险','公积金','停缴'), L+'；《社会保险法》第58条、第60条', [
    ('社保停缴时点或办理安排', (r'(?:社会保险|社保)[^。；]{0,30}(?:停缴|转移|办理)',)),
    ('公积金停缴或封存安排', (r'(?:公积金)[^。；]{0,30}(?:停缴|封存|转移|办理)',)),
    ('最后缴费月份及实际缴费衔接', ()),
], element_policies={2: {'requirement_kind':'EXTERNAL_VERIFICATION',
    'verification_instruction':'核验解除当月社保、公积金实际缴费及停缴生效时点；停缴月份约定不等于已依法足额缴费，不以文本推定实际欠缴。', 'verification_priority':'MEDIUM'}})
SECRECY = R('ET', 8, 'termination_secrecy', '离职后保密义务范围', ('保密','商业秘密'), '《劳动合同法》第23条', [
    ('受保护秘密的范围', (r'(?:商业秘密|技术资料|客户信息|经营数据)',)),
    ('离职后保密义务及期限', (r'(?:解除|终止|离职)后[^。]{0,30}保密义务',r'保密期限[^。]{0,20}(?:年|永久|公开)'),),
], trigger=('保密',))
TERMINATION_ADDITIONS = (SETTLEMENT, CALCULATION, WITHHOLD, DEDUCTION, WAIVER, STOPPAGE, SECRECY)
TERMINATION_ADDITIONS = tuple(replace(c, applicable_if='劳动关系解除或终止结算协议场景适用。'+ (c.applicable_if if c.applicable_if != '始终适用' else '')) for c in TERMINATION_ADDITIONS)
for element in PROFILES['termination_insurance_stoppage'][:2]:
    element['preserve_full_quote'] = True
