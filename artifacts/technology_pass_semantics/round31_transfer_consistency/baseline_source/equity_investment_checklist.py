"""境内非上市股权交易的基础专项清单；特殊交易另作人工核验。"""
from dataclasses import replace
from review_v2.priority_checklist_helpers import required as R, forbidden as F, common_rows

C = "《公司法》"
AMOUNT = r'(?:人民币)?\s*(?:[\d,，]+(?:\.\d+)?|[零〇一二两三四五六七八九十百千万亿壹贰叁肆伍陆柒捌玖拾佰仟]+)\s*(?:万|亿)?元'
DATE = r'\d{4}\s*(?:年|[-/])\s*\d{1,2}\s*(?:月|[-/])\s*\d{1,2}\s*日?'
IDENTITY = R("EQT", 1, "equity_title", "交易主体及股权权属", ("目标公司", "转让方", "投资方", "股权"), C + "第15条、第55条、第56条、第86条", [
    ("转让方或投资方主体名称", (r'(?:^|\n)(?:转让方|投资方|甲方)\s*[：:]\s*[^\n，。；_（(]{2,60}',)),
    ("受让方或交易相对方主体名称", (r'(?:^|\n)(?:受让方|融资方|乙方)\s*[：:]\s*[^\n，。；_（(]{2,60}',)),
    ("目标公司名称", (r'目标公司\s*[：:]\s*[^\n，。；_]{2,70}', r'[\u4e00-\u9fff]{2,60}(?:有限责任公司|股份有限公司|有限公司)(?:的)?(?:股权|合法拥有)', r'(?:成为|在)[^。；\n]{2,60}(?:有限责任公司|股份有限公司|有限公司)(?:的股东|合法拥有|原享有)'),),
    ("持股或转让比例", (r'(?:持有|转让|认购|股权比例|注册资本)[^。；\n]{0,25}\d+(?:\.\d+)?\s*[%％]',)),
    ("合法权属或处分权声明", (r'合法(?:拥有|持有)[^。；\n]{0,15}股权',r'(?:拥有|享有)[^。；\n]{0,8}(?:完全)?(?:的)?处分权',r'股权[^。；\n]{0,30}(?:权属清晰|合法所有)'),),
], risk="高")
CONTRIBUTION = R("EQT", 2, "equity_contribution_liability", "认缴实缴及出资责任", ("认缴", "实缴", "出资期限", "未缴出资"), C + "第47条、第54条、第88条", [
    ("认缴出资金额", (r'认缴(?:出资|金额)?\s*(?:为|：|:)?\s*'+AMOUNT,)),
    ("实缴出资金额", (r'实缴(?:出资|金额)?\s*(?:为|：|:)?\s*'+AMOUNT,)),
    ("出资或缴付期限", (r'(?:出资期限|缴付期限)[^。；\n]{0,12}'+DATE,)),
    ("未缴出资责任的承担及法定责任保留", (r"(?:未缴出资|未届期出资|出资瑕疵).{0,60}(?:承担|责任).{0,45}(?:法定|不得对抗|不影响)", r"全部实缴.{0,20}不存在出资瑕疵")),
], risk="高")
RESTRICTIONS = R("EQT", 3, "equity_transfer_restrictions", "转让限制和其他股东权利", ("优先购买权", "其他股东", "章程"), C + "第84条、第85条", [
    ("公司章程转让限制核对", (r"(?:核对|核验|遵守).{0,30}章程.{0,25}转让限制",)),
    ("向其他股东通知同等条件或不触发外部转让", (r"其他股东.{0,50}(?:数量|比例).{0,30}价格.{0,30}(?:支付|期限)", r"股东之间内部转让")),
    ("优先购买权的依法行使或书面放弃", (r"优先购买权.{0,40}(?:三十|30)日|其他股东.{0,20}书面放弃.{0,15}优先购买权|股东之间内部转让",)),
    ("其他股东签署记载（不证明通知或放弃程序完成）", (r'其他股东(?:签署|签字|签章)\s*[：:]\s*(?:\n\s*)?[\u4e00-\u9fff·]{2,20}',)),
], risk="高", element_policies={3:{'risk_relevant':False,'recommendation_action':'OPTIONAL','residual_gap':'签署记载仅为相关证据，通知内容、同等条件和优先购买权程序仍分别核验'}})
PRICE = R("EQT", 4, "equity_price_payment", "交易价格及支付", ("转让价款", "投资款", "支付"), "《民法典》第510条、第511条、第509条", [
    ("价款或投资总额", (r'(?:股权转让款|转让价款|转让款|转让金|投资款|增资款|投资总额)\s*(?:为|：|:)?\s*'+AMOUNT,)),
    ("支付节点、条件或期限", (r"(?:交割|签署|生效).{0,20}\d+日内.{0,25}支付|支付.{0,30}"+DATE, DATE+r'\s*(?:前|之前|内)[^。；\n]{0,40}(?:支付|付清|付给|付款)',)),
], risk="高")
CLOSING = R("EQT", 5, "equity_closing_registration", "交割及名册工商变更", ("交割", "股东名册", "工商变更", "变更登记"), C + "第34条、第86条、第87条", [
    ("合同双方内部权益承接时间安排（不代表已完成名册及登记手续）", (DATE+r'\s*(?:起|日起)[^。；\n]{0,80}(?:成为[^。；\n]{0,60}股东|享有股东权利)',r'交割(?:日期|日|时间)[为：:]?\s*'+DATE)),
    ("交割条件及未满足的处理", (r"交割条件.{0,40}(?:满足|完成|具备).{0,60}(?:未满足|未完成).{0,30}(?:解除|延期|退款)",)),
    ("股东名册更新", (r"(?:更新|修改|记载).{0,15}股东名册",)),
    ("出资证明更新", (r'(?:更新|换发|出具|签发|注销)[^。；\n]{0,20}出资证明',)),
    ("办理变更登记的责任人与期限", (r"(?:目标公司|双方).{0,30}\d+日内.{0,20}(?:工商变更|变更登记)",)),
], risk="高", element_policies={0:{'risk_relevant':False,'recommendation_action':'OPTIONAL','residual_gap':'承接时间为独立事实；具备完整交割条件和登记安排时无需另设固定日期'}})
CLOSING = replace(CLOSING, legal_consequence_if_missing=(
    "合同双方内部约定的权益承接日期不能替代股东名册更新、出资证明更新及相关变更登记手续。"
    "受让人自记载于股东名册时起可以向公司主张行使股东权利；合同约定日期本身不证明上述手续已经完成。"
    "对尚未约定的手续，仍需明确办理责任人、办理期限及未及时办理的责任；必要时明确交割条件及未满足后的处理。"
))
GOVERNANCE = R("EQT", 6, "equity_governance", "公司治理和股东知情权", ("董事会", "表决权", "知情权", "财务报表"), C + "第57条、第59条、第66条、第67条", [
    ("董事席位或表决和重大事项决策", (r"(?:董事会|股东会).{0,50}(?:表决|席位|重大事项|决议)",)),
    ("财务信息和依法查阅的安排", (r"(?:股东|投资方).{0,25}(?:有权|可以).{0,20}(?:查阅|取得).{0,20}(?:财务|会计|账簿)",)),
])
CAPITAL = R("EQT", 7, "equity_capital_increase", "增资认缴和原股东优先权", ("增资", "新增注册资本", "资本公积", "优先认缴"), C + "第47条、第227条、第228条", [
    ("新增注册资本及资本公积拆分", (r"新增注册资本.{0,12}\d+万?元.{0,40}资本公积.{0,12}\d+万?元",)),
    ("认缴出资期限和方式", (r"(?:认缴|新增出资).{0,50}\d{4}年\d{1,2}月\d{1,2}日.{0,25}(?:货币|现金|银行转账|实物|知识产权)",)),
    ("原股东优先认缴或一致另约", (r"(?:原股东|全体股东).{0,50}(?:优先认缴|优先认购|一致同意).{0,45}(?:放弃|实缴比例|另行约定|认缴)",)),
], risk="高")
VALUATION = R("EQT", 8, "equity_valuation", "估值与投后比例", ("投前估值", "投后估值", "投后持股"), "《民法典》第143条、第465条、第509条", [
    ("投前或投后估值基准", (r"(?:投前估值|投后估值)[为：:]?\d+(?:\.\d+)?万?元",)),
    ("投资后持股比例及计算口径", (r"投后(?:持股)?比例[为：:]?\d+(?:\.\d+)?[%％].{0,50}(?:计算|完全摊薄|注册资本)",)),
])
PREFERENCES = R("EQT", 9, "equity_preferences", "优先权和反稀释", ("反稀释", "优先清算", "优先分红"), C + "第210条、第227条；《民法典》第465条、第509条", [
    ("优先权或反稀释的触发条件", (r"(?:反稀释|优先清算|优先分红).{0,60}(?:低于|发生|触发|条件)",)),
    ("计算范围、履行主体及公司法限制", (r"(?:反稀释|优先清算|优先分红).{0,100}(?:计算|比例|公式).{0,80}(?:公司法|法定程序|债权人)",)),
], trigger=("反稀释", "优先清算", "优先分红"))
BUYBACK = R("EQT", 10, "equity_buyback_performance", "回购及业绩承诺", ("回购", "业绩承诺", "对赌"), C + "第89条、第162条、第224条；《民法典》第143条、第509条", [
    ("回购或业绩承诺的触发条件与义务人", (r"(?:原股东|创始股东|目标公司).{0,65}(?:业绩未达|未上市|未实现|触发).{0,50}(?:回购|补偿)",)),
    ("价格或补偿计算及履行期限", (r"(?:回购|业绩补偿).{0,65}(?:本金|价格|计算|公式).{0,65}\d+日",)),
    ("目标公司承担时核验回购减资及资本维持", (r"(?:目标公司|公司回购).{0,80}(?:减资|法定程序|资本维持|债权人保护)|(?:回购义务人仅为|仅由).{0,20}(?:原股东|创始股东)",)),
], trigger=("回购", "业绩承诺", "对赌"), risk="高")
WARRANTY = R("EQT", 11, "equity_warranties_remedies", "陈述保证与违约救济", ("陈述保证", "债务", "赔偿"), "《民法典》第500条、第577条、第584条、第585条", [
    ("股权负担陈述保证", (r'(?:保证|承诺)[^。]{0,90}(?:无质押|无冻结|无权利负担|未设定[^。]{0,10}质押|没有设置[^。]{0,20}(?:抵押|质押|担保))',)),
    ("财务及债务披露保证", (r'(?:债务|财务)[^。；\n]{0,20}(?:披露|真实)',)),
    ("陈述不实的赔偿或退出救济", (r"(?:陈述不实|违反保证|隐瞒债务).{0,50}(?:赔偿|解除|退款)",)),
])
from review_v2.priority_checklist_helpers import PROFILES
PROFILES['equity_warranties_remedies'][2]['contextual_patterns'] = [{
    'context':r'保证|陈述|承诺',
    'predicate':r'否则[^。]{0,45}(?:责任|损失)[^。]{0,20}(?:甲方|转让方)[^。]{0,10}(?:承担|赔偿)'}]
for index in (0, 2):
    # The denial of encumbrances and its "otherwise" remedy are interpreted
    # in the warranty context; publish the source intact rather than detaching
    # a short remedy fragment from the statement it qualifies.
    PROFILES['equity_warranties_remedies'][index]['preserve_full_quote'] = True

# Atomic transaction facts: asset contributions and capital tables are not cash
# payments. Keep predicates source-bound, with parent headings only supplying role.
PROFILES['equity_title'][2]['semantic_patterns'] += (
    r'标的公司[：:]\s*[^，。；\n]{2,70}',
    r'(?:对|持有)[^，。；\n]{2,60}(?:有限公司|有限责任公司)(?:的增资|[0-9.]+%股权)',)
for idx, verb in ((0,'认缴'),(1,'实缴')):
    PROFILES['equity_contribution_liability'][idx]['semantic_patterns'] += (verb+r'(?:注册资本|资本|出资额)\s*'+AMOUNT,)
_ASSET_PERFORMANCE = r'(?:甲方|乙方|投资方|出资方)[^。；\n]{0,15}(?:于|在)[^。；\n]{0,12}(?:\d+|[一二两三四五六七八九十]+)(?:个工作日|日|天)内[^。；\n]{0,30}(?:房产|不动产|土地使用权|知识产权|设备|资产)[^。；\n]{0,20}(?:变更至|过户至|转移至|交付给)[^。；\n]{0,20}(?:公司|企业)'
PROFILES['equity_contribution_liability'][2]['semantic_patterns'] += (_ASSET_PERFORMANCE,)
PROFILES['equity_price_payment'][0]['semantic_patterns'] += (
    r'(?:作价|出资作价)(?:确定)?(?:为)?\s*'+AMOUNT+r'[^。；\n]{0,50}(?:投入|出资|增资)',
    r'(?:本次|实际)出资作价(?:确定)?为\s*'+AMOUNT,)
PROFILES['equity_price_payment'][1]['semantic_patterns'] += (_ASSET_PERFORMANCE,)
PROFILES['equity_price_payment'][1]['proposition'] = '价款支付或出资履行的节点、条件或期限'
PROFILES['equity_closing_registration'][4]['semantic_patterns'] += (
    r'(?:甲乙双方|双方|目标公司)[^。；\n]{0,15}\d+日内[^。；\n]{0,60}(?:市场监督管理|登记机关)[^。；\n]{0,60}(?:变更手续|变更登记)',)
# A filing deadline is evidence of a procedural arrangement, not proof that
# registration must be completed on that day.
PROFILES['equity_closing_registration'][4]['proposition'] = '变更登记办理主体及申报或办理期限安排'
PROFILES['equity_valuation'][1]['semantic_patterns'] += (
    r'(?:甲方|乙方|投资方|股东)[^。；\n]{0,15}持有目标公司\d+(?:\.\d+)?[%％]股权',)
PROFILES['equity_valuation'][1]['semantic_patterns'] = PROFILES['equity_valuation'][1]['semantic_patterns'][:-1]
PROFILES['equity_valuation'][1]['contextual_patterns'] = [{'context':r'增资.*后.*(?:注册资本|股本)|投后', 'predicate':r'(?:甲方|乙方|投资方|股东)[^。；\n]{0,15}持有目标公司\d+(?:\.\d+)?[%％]股权'}]
PROFILES['equity_capital_increase'][1]['semantic_patterns'] += (_ASSET_PERFORMANCE,)
PROFILES['equity_warranties_remedies'][0]['contextual_patterns'] = [{
    'context': r'声明|保证|承诺',
    'predicate': r'(?:股权|房产所有权|土地使用权|出资资产)[^。；\n]{0,30}不存在任何(?:抵押|质押|担保)'}]
PROFILES['equity_warranties_remedies'][0]['proposition'] = '股权或出资资产负担陈述保证'
PROFILES['equity_warranties_remedies'][2]['contextual_patterns'] += [{
    'context': r'终止|解除|补偿|赔偿|违约',
    'predicate':r'(?:声明|保证|承诺)[^。；\n]{0,30}(?:不真实|不实)|违反其声明[^。；\n]{0,160}(?:补偿|赔偿)'}]

EXIT = R("EQT", 12, "equity_exit", "退出及僵局机制", ("退出", "僵局", "共同出售"), "《民法典》第465条、第509条；《公司法》第231条", [
    ("退出或治理僵局触发事由", (r"(?:僵局|退出).{0,40}(?:无法决议|未能|触发|条件|协商不成)",)),
    ("退出程序与定价或依法解散救济", (r"(?:退出|僵局).{0,80}(?:评估|定价|转让|依法解散|法院)",)),
])
INVALID = F("EQT", 13, "equity_mandatory_rights_waiver", "排除股东法定权利或资本约束", ("无需通知", "不享有优先购买权", "不经减资", "出资责任"), C + "第57条、第84条、第88条、第224条", (
    r"(?:对外转让|向股东以外).{0,45}(?:无需通知|无须通知).{0,12}其他股东",
    r"(?:目标公司|公司).{0,35}(?:回购|返还投资款).{0,35}(?:无需|不经).{0,15}(?:减资|法定程序|债权人通知)",
    r"(?:受让方|转让方).{0,20}(?:一律|全部|永久)免除.{0,15}(?:法定出资责任|出资责任)",
    r"(?:股东|投资方).{0,20}(?:永久放弃|不得行使).{0,15}(?:知情权|查阅权)",
), "保留股东依法行使的权利及法定出资责任；内部责任分配不得对抗法定责任，公司回购与减资应核验法定条件和程序。")

STRUCTURE = tuple(F('EQT', n, node, title, (title,), '《民法典》第466条、第509条', (), suggestion) for n,node,title,suggestion in (
    (14,'equity_transaction_structure','增资与股权转让交易结构冲突','区分新增出资与存量股权转让，明确对价、收款主体及股权来源。'),
    (15,'equity_contribution_warranty_alignment','出资主体及资产保证对象不一致','逐项核对实际出资人与资产对象，使声明保证与出资义务一致。'),
    (16,'equity_invalid_cross_reference','条款交叉引用目标未定义','核对交叉引用的条款编号及对应义务，修正不存在的引用。'),
))
STRUCTURE = tuple(replace(r, legal_consequence_if_missing=r.risk_point_present) for r in STRUCTURE)
BASE = (IDENTITY, CONTRIBUTION, WARRANTY, INVALID)
EQUITY_TRANSFER_CHECKLIST = BASE + (RESTRICTIONS, PRICE, CLOSING) + common_rows()
CAPITAL_INCREASE_CHECKLIST = BASE + STRUCTURE + (CAPITAL, PRICE, CLOSING, VALUATION, GOVERNANCE, PREFERENCES, BUYBACK, EXIT) + common_rows()
INVESTMENT_CHECKLIST = BASE + (PRICE, CLOSING, VALUATION, GOVERNANCE, CAPITAL, PREFERENCES, BUYBACK, EXIT) + common_rows()
SHAREHOLDERS_CHECKLIST = BASE + (GOVERNANCE, RESTRICTIONS, PREFERENCES, BUYBACK, EXIT) + common_rows()
