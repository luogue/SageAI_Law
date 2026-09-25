"""劳动用工专项清单；依据劳动合同法及2025年劳动争议解释（二）。"""
from review_v2.priority_checklist_helpers import required as R, forbidden as F, PROFILES

L = "《劳动合同法》"
IDENTITY = R("EMP", 1, "employment_identity", "用工主体与劳动者身份", ("用人单位", "劳动者", "身份证", "统一社会信用代码"), L + "第2条、第17条", [
    ("用人单位名称与住所", (r"(?:用人单位|劳务派遣单位)[）)]?\s*(?:名称|姓名)?\s*[：:]\s*[^\n，；。_]{2,60}(?:公司|企业|事务所)(?:(?!乙方|劳动者|用工单位).){0,300}(?:住所|地址|注册地|注册登记地|实际经营地)[：:]\s*[^\n，；。_]{3,60}",)),
    ("劳动者姓名与身份证明", (r"劳动者[）)]?\s*(?:名称|姓名)?\s*[：:]\s*[\u4e00-\u9fff·]{2,12}[^。；]{0,160}(?:居民身份证号码|身份证(?:号码)?|证件号码)[：:]?\s*[0-9Xx]{8,18}",)),
], risk="高")
TERM = R("EMP", 2, "employment_term", "合同期限", ("合同期限", "无固定期限", "工作任务"), L + "第12条至第15条、第17条", [
    ("期限类型", (r"(?:固定期限|无固定期限|以完成.{1,30}工作任务为期限)",)),
    ("生效或起始日期（按期限类型审查）", (r"(?:本合同|合同期限)(?:自|于)\d{4}年\d{1,2}月\d{1,2}日",)),
])
PROBATION = R("EMP", 3, "employment_probation", "试用期与试用工资", ("试用期", "试用工资"), L + "第19条、第20条", [
    ("试用期长度", (r"试用期(?:为|：|:)?\s*[一二三四五六七八九十\d]+个?月", r"试用期[：:]?\s*自?\d{4}[年/-]\d{1,2}[月/-]\d{1,2}日?起?至\d{4}[年/-]\d{1,2}[月/-]\d{1,2}日?")),
    ("试用期工资标准", (r"试用期(?:期间的|月)?(?:正常工作时间)?工资[^\n。；]{0,12}\d+(?:\.\d+)?\s*元", r"试用期.{0,30}(?:百分之八十|80%).{0,40}最低工资")),
], trigger=("试用期",))
WORK = R("EMP", 4, "employment_work", "工作内容和地点", ("岗位", "工作内容", "工作地点"), L + "第17条、第35条", [
    ("具体工作岗位或职责", (r"(?:工作岗位|工作内容|岗位)[为：:][^，。；_]{2,35}|安排(?:乙方|劳动者)在[^，。；_]{2,40}岗位|从事[^，。；_]{2,60}(?:开发|维护|测试|工作)",)),
    ("具体工作地点", (r"工作地点[为：:][^，。；_]{3,60}",)),
])
HOURS = R("EMP", 5, "employment_hours", "工时、休息与加班", ("工时", "休息", "加班"), "《劳动法》第36条、第38条、第41条、第44条", [
    ("工时制度及工作时间", (r"(?:标准工时|每天.{0,5}[八8]小时|每周.{0,5}40小时)", r"(?:综合计算工时|不定时工作制).{0,45}(?:审批|批准)")),
    ("休息休假安排", (r"(?:每周.{0,10}休息|(?:依法享有|依法享受).{0,15}(?:休假|年休假)|法定节假日.{0,10}休息)",)),
    ("加班报酬或依法调休", (r"加班.{0,40}(?:依法支付|加班工资|补休|调休)", r"依法安排[^。；\n]{0,20}(?:补休|调休)或支付加班工资", r"(?:支付|发放)加班工资")),
])
WAGE = R("EMP", 6, "employment_wage", "工资标准与支付", ("工资", "每月", "银行"), L + "第17条、第30条", [
    ("工资金额或可计算标准", (r"(?<!试用期)(?:月工资|月正常工作时间工资|基本工资|工资标准)[为：:]?\s*(?:人民币)?\d+(?:\.\d+)?\s*元",)),
    ("工资支付日期", (r"每月\d{1,2}日.{0,20}(?:发放|支付|银行)|工资.{0,20}每月\d{1,2}日",)),
    ("工资支付方式", (r"工资.{0,40}(?:银行转账|银行账户|现金支付)|(?:银行转账|银行账户|现金支付)[^。；]{0,40}工资",)),
], risk="高")
INSURANCE = R("EMP", 7, "employment_insurance", "社会保险缴纳", ("社会保险", "社保"), L + "第17条、第38条；《社会保险法》第58条、第60条", [
    ("用人单位依法办理参保并缴费", (r"(?:用人单位|甲方|甲乙双方).{0,80}(?:依法|按月).{0,15}(?:缴纳|缴付).{0,60}(?:社会保险|社保)", r"(?:社会保险|社保)缴纳主体[：:]\s*[^\n，；。_]{2,60}(?:公司|企业|事务所)")),
    ("个人应缴部分及代扣代缴", (r"(?:个人|劳动者|乙方).{0,15}(?:应缴|承担).{0,40}(?:代扣|代缴)|(?:代扣代缴).{0,45}(?:社会保险|社保).{0,15}个人缴费部分",)),
], risk="高", element_risk_levels=("高", "中"))
SAFETY = R("EMP", 8, "employment_safety", "劳动保护与职业危害", ("劳动保护", "职业危害", "防护"), L + "第17条、第32条", [
    ("劳动防护和安全培训", (r"(?:提供|配备).{0,60}(?:劳动保护|劳动防护用品|防护用品)|安全(?:生产)?(?:教育和)?培训",)),
    ("职业危害告知和健康保护", (r"职业(?:病)?危害.{0,35}(?:告知|防护|健康检查)",)),
])
SERVICE = R("EMP", 9, "employment_training_service", "专项培训服务期", ("专项培训", "服务期"), L + "第22条", [
    ("专项培训费用和凭证", (r"专项培训.{0,35}(?:\d+元|费用凭证|实际支出)",)),
    ("服务期与违约金按未履行部分分摊", (r"服务期.{0,20}[一二三四五六七八九十\d]+年",)),
    ("违约金不超过未履行服务期分摊培训费用", (r"违约金.{0,40}(?:不超过|不得超过).{0,35}(?:未履行|尚未履行).{0,25}培训费",)),
], trigger=("服务期", "专项培训"))
NC_SCOPE = R("NC", 1, "employment_noncompete_scope", "竞业人员及秘密接触范围", ("竞业限制", "商业秘密", "保密事项"), L + "第23条、第24条；劳动争议司法解释（二）第13条、第14条", [
    ("人员范围及实际接触秘密", (r"(?:劳动者|乙方).{0,40}(?:实际接触|知悉|掌握).{0,35}(?:商业秘密|保密事项)",)),
    ("明确约定竞业业务范围", (r"竞业(?:限制|禁止).{0,25}业务范围\s*(?:为|包括|限于|：|:)[^。；_]{3,80}", r"(?:不得|禁止).{0,20}(?:自营|经营|从事).{0,50}(?:竞争|同类|类似).{0,20}业务")),
    ("明确约定竞业地域范围", (r"竞业(?:限制|禁止).{0,25}(?:地域|地区|区域)范围\s*(?:为|包括|限于|：|:)[^。；_]{2,80}",)),
])
NC_TERM = R("NC", 2, "employment_noncompete_term", "离职竞业期限及补偿", ("竞业限制", "补偿", "离职"), L + "第23条、第24条；劳动争议司法解释（一）第36条至第39条", [
    ("离职竞业限制期限", (r"(?:离职|解除|终止).{0,40}竞业限制.{0,15}[一二三四五六七八九十\d]+个?(?:月|年)", r"竞业限制期限.{0,12}[一二三四五六七八九十\d]+个?(?:月|年)")),
    ("离职后按月经济补偿的金额或计算标准", (r"(?:离职|解除|终止).{0,100}(?:每月|按月).{0,30}(?:补偿.{0,12}\d+元|\d+元.{0,12}补偿|补偿.{0,20}\d+[%％])",)),
], trigger=("离职", "解除", "终止"), risk="高")
SECRET = R("NDA", 1, "employment_secret_scope", "保密信息范围及除外", ("保密信息", "商业秘密"), "《民法典》第501条、第509条；《劳动合同法》第23条", [
    ("明确受保护的信息内容", (r"(?:保密信息|商业秘密)(?:范围|内容)?(?:包括|为|：|:)[^。；_]{3,100}",)),
    ("公开信息、合法独立取得及法定披露除外", (r"(?:公开信息|已公开|独立开发|合法取得).{0,45}(?:除外|不属于|不受|不承担)|(?:不包括|除外).{0,40}(?:公开信息|独立开发)",)),
])
SECRET_DUTY = R("NDA", 2, "employment_secret_duty", "保密义务、期限和返还", ("保密义务", "披露", "返还", "销毁"), "《民法典》第509条；《劳动合同法》第23条", [
    ("限制使用披露及接触人员", (r"(?:不得|未经.{0,20}同意不得).{0,25}(?:披露|泄露|使用).{0,25}(?:保密信息|商业秘密)",)),
    ("保密期限或信息公开后的终止条件", (r"保密(?:义务)?期限.{0,25}(?:年|月|公开)|保密义务.{0,30}至.{0,30}公开",)),
    ("资料返还或销毁安排", (r"(?:终止|离职|要求).{0,45}(?:返还|销毁).{0,20}(?:资料|保密信息)",)),
])
EXIT = R("EMP", 10, "employment_exit", "解除终止条件和程序", ("解除", "终止", "通知"), L + "第36条至第44条", [
    ("解除终止事由或协商一致", (r"协商一致.{0,20}(?:解除|终止)|(?:解除|终止).{0,40}(?:法定条件|劳动合同法|法定事由)", r"(?:解除|终止)[^。；\n]{0,40}(?:按照|依照|根据|按)[^。；\n]{0,10}法律法规[^。；\n]{0,10}(?:执行|办理)", r"(?:派遣.{0,10}(?:届满|期满)|依法退回)[^。；]{0,100}(?:重新派遣|另行安排.{0,20}派遣|依法解除)")),
    ("解除通知方式或明确解除日期", (r"(?:解除|终止).{0,40}(?:书面通知|\d{4}年\d{1,2}月\d{1,2}日)|提前.{0,8}(?:三十|30)日.{0,8}书面通知",)),
])
COMPENSATION = R("EMP", 11, "employment_compensation", "经济补偿及结算", ("经济补偿", "工资结算"), L + "第46条、第47条、第50条", [
    ("经济补偿法定依据或明确计算口径", (r"经济补偿.{0,60}(?:第46条|第47条|第四十六条|第四十七条|\d+元|工作年限|月工资)|(?:甲方|用人单位)(?:应当|应|须)?依法(?:应当|应)?(?:向乙方|向劳动者)?支付经济补偿",)),
    ("解除终止后工资及补偿结算期限", (r"(?:解除|终止).{0,70}(?:\d+日内|当日).{0,35}(?:支付|结清)|(?:补偿|工资).{0,40}\d+日内.{0,20}(?:结清|支付)", r"经济补偿[^。；\n]{0,30}(?:办结|完成|办理完毕)工作交接(?:时|后当日)[^。；\n]{0,8}(?:支付|结清)")),
])
HANDOVER = R("ET", 1, "employment_handover", "离职证明、社保转移与交接", ("离职证明", "解除证明", "工作交接", "社保转移"), L + "第50条", [
    ("离职证明出具", (r"(?:出具|提供).{0,20}(?:离职证明|解除证明|解除劳动合同证明|终止劳动合同证明)",)),
    ("档案和社保关系转移", (r"(?:十五|15)日内.{0,45}(?:档案|社保|社会保险).{0,20}转移",)),
    ("交接事项及期限", (r"(?:交接|移交).{0,35}\d+日|\d+日内.{0,35}(?:工作交接|移交)",)),
])
DISPUTE = R("EMP", 12, "employment_dispute", "劳动争议处理", ("劳动争议", "劳动仲裁"), "《劳动争议调解仲裁法》第5条", [
    ("劳动争议依法申请劳动仲裁", (r"(?:劳动争议|劳动合同争议).{0,60}(?:劳动仲裁|劳动(?:人事)?争议仲裁委员会)", r"申请(?:调解或|调解、)?仲裁", r"劳动争议仲裁机构[：:]\s*[^。；\n]{2,50}劳动人事争议仲裁委员会")),
])
ILLEGAL_WAIVER = F("EMP", 13, "employment_illegal_waiver", "免除或放弃法定社会保险义务", ("放弃社保", "不缴纳社会保险"), L + "第26条、第38条；劳动争议司法解释（二）第19条", (
    r"(?:劳动者|乙方).{0,15}(?:自愿)?放弃.{0,8}(?:社保|社会保险)",
    r"(?:用人单位|甲方).{0,12}(?:无需|不予|不必|不).{0,5}缴纳.{0,5}(?:社会保险|社保)",
), "删除免除或放弃法定参保义务的约定，依法办理参保并缴费；已经存在缴费约定的，应消除冲突表述。")
ILLEGAL_EXIT = F("EMP", 16, "employment_arbitrary_exit", "用人单位任意解除且免予补偿", ("随时辞退", "随时解除", "无需补偿"), L + "第26条、第39条至第43条、第46条、第87条", (
    r"(?:用人单位|甲方).{0,20}(?:可以|可|有权).{0,8}随时(?:辞退|解除).{0,30}(?:无需|不予|不支付).{0,10}补偿",
), "删除任意解除和一概免予补偿的约定，按法定解除事由、程序及经济补偿或违法解除赔偿规则办理。")
PENALTY = F("EMP", 14, "employment_general_penalty", "违法约定劳动者违约金", ("辞职", "违约金", "保密违约金"), L + "第22条至第25条", (
    r"(?:辞职|辞退|普通培训|迟到|泄密|违反保密义务).{0,40}(?:应|须|需|必须|支付).{0,20}违约金",
), "劳动者违约金限于合法专项培训服务期和竞业限制；一般保密义务违反可依法按实际损失追责。")
NC_RISK = F("NC", 3, "employment_noncompete_adverse", "竞业范围或补偿明显不当", ("竞业限制", "补偿", "所有员工"), L + "第23条、第24条；劳动争议司法解释（二）第13条、第14条", (
    r"(?:所有员工|全体员工|任何员工).{0,40}(?:必须|均应|均须).{0,15}竞业限制",
    r"(?:离职|解除|终止).{0,60}竞业限制.{0,40}(?:无需支付|不支付|无偿).{0,10}(?:补偿|履行)",
    r"竞业限制.{0,25}(?:期限|为|长达)[：:]?(?:[3-9]|三|四|五|六|七|八|九|十)年",
), "按实际接触秘密确定人员及合理业务、地域范围；离职竞业最长两年，并依法处理按月补偿。在职竞业不套用离职补偿规则。")

PROBATION_LIMIT = F("EMP", 15, "employment_probation_limit", "试用期超过法定上限或重复约定", ("试用期", "再次约定试用期"), L + "第19条、第83条", (r"(?:双方|用人单位|甲方).{0,25}(?P<act>(?:再次|重新|重复)约定试用期)",), "根据劳动合同期限核对试用期上限，同一用人单位与同一劳动者只能约定一次试用期。")

# Salary context belongs to the amount proposition, not the whole document.
from review_v2.lease_semantics import requirement

# Alternate drafting forms use the same full-corpus evidence predicates in
# judgment, binding and absence audits; no institution or sample identifiers.
def _variants(node, index, *patterns):
    row = PROFILES[node][index]
    row['semantic_patterns'] = tuple(row['semantic_patterns']) + patterns

_variants('employment_identity', 0,
    r'甲方(?:[（(][^）)\n]{1,15}[）)])?[：:]\s*[^\n，；。_]{2,80}(?:(?!乙方)[\s\S]){0,200}(?:注册地址|经营地址|住所)[：:]\s*[^\n，；。_]{3,80}',
    r'甲方[：:]\s*[^\n，；。_]{2,60}(?:(?!乙方)[\s\S]){0,120}(?:住所|地址)[：:]\s*[^\n，；。_]{3,60}')
_variants('employment_identity', 1,
    r'乙方(?:[（(][^）)\n]{1,15}[）)])?[：:]\s*[\u4e00-\u9fff·]{2,12}(?:(?!甲方)[\s\S]){0,180}(?:居民身份证号码|身份证号码)[：:]\s*[0-9Xx]{18}',
    r'乙方[：:]?\s*[\u4e00-\u9fff·]{2,12}[\s\S]{0,180}(?:居民身份证号码|身份证号码|证件号码)[：:]\s*[0-9Xx]{8,18}')
PROFILES['employment_identity'][1]['evidence_unit'] = 'clause'
_variants('employment_identity', 1,
    r'乙方(?:[（(][^）)\n]{1,15}[）)])?\s*[：:]\s*[\u4e00-\u9fff·]{2,12}(?:(?!甲方)[\s\S]){0,180}身份证号(?:码)?\s*[：:]\s*[0-9Xx*＊]{15,18}')
PROFILES['employment_identity'][0]['proposition'] = '用人单位住所'
PROFILES['employment_identity'].append(requirement('employment_identity_name', '用人单位名称',
    r'甲方(?:[（(][^）)\n]{1,20}[）)])?\s*[：:]\s*[^\n，；。_]{2,60}', r'甲方\s*(?:名称|为|系)\s*[：:]?\s*[^\n，；。_]{2,60}(?:大学|学院|医院|公司|研究所|中心)',
    r'(?:用人单位|劳务派遣单位)[）)]?\s*(?:名称)?\s*[：:]\s*[^\n，；。_]{2,60}'))
for _identity_element, _gap_level in zip(PROFILES['employment_identity'], ('中', '高', '高')):
    _identity_element['gap_risk_level'] = _gap_level
_variants('employment_probation', 0,
    r'本合同自\d{4}年\d{1,2}月\d{1,2}日起?至\d{4}年\d{1,2}月\d{1,2}日止?，其中试用期至\d{4}年\d{1,2}月\d{1,2}日')
_variants('employment_probation', 1,
    r'试用期(?:期间的|月)?(?:基本)?工资(?:标准)?(?:为|：|:)?\s*(?:人民币)?\s*\d+(?:\.\d+)?\s*元')
_variants('employment_work', 0, r'(?:担任|从事)[^。；\n]{2,60}岗位',
    r'(?:负责|参与|承担)[^。；\n]{2,80}(?:研发|开发|测试|维护|研究|设计|整理|编写)')
_variants('employment_hours', 1, r'(?:休假制度|享受|享有)[^。；\n]{0,40}(?:法定节假日|公休日|带薪年假)')
PROFILES['employment_hours'][2].update({
    'risk_relevant': False,
    'recommendation_action': 'OPTIONAL',
    'residual_gap': '法定加班报酬规则无需在合同中重复列明；明确不利约定仍独立审查',
})
_variants('employment_wage', 1, r'每月[一二三四五六七八九十\d]{1,3}日(?:前|内)?[^。；\n]{0,30}支付[^。；\n]{0,20}工资')
_variants('employment_wage', 1, r'每月\s*[一二三四五六七八九十\d]{1,3}\s*日\s*(?:前|内)?[^。；\n]{0,40}支付[^。；\n]{0,25}工资')
_variants('employment_wage', 0, r'(?:月工资标准|月工资|工资标准)\s*(?:为|：|:)\s*(?:税前|税后)?\s*(?:人民币)?\s*\d+(?:\.\d+)?\s*元(?:/月)?')
_variants('employment_wage', 2, r'以货币形式支付[^。；\n]{0,20}工资')
_variants('employment_insurance', 0,
    r'(?:甲乙双方|用人单位|甲方)(?:按|按照)[^。；\n]{0,35}规定参加社会保险')
_variants('employment_compensation', 1,
    r'经济补偿[^。；\n]{0,30}工作交接(?:结束|完成|办结)后[^。；\n]{0,8}支付')

PROFILES['employment_wage'][0]['excluded_scenario_patterns'] = (r'试用期(?!满|结束|届满)',)
from review_v2.noncompete_semantics import TERM_PATTERNS, DEFINED_TERM
PROFILES['employment_noncompete_term'][0]['semantic_patterns'] = TERM_PATTERNS
PROFILES['employment_noncompete_term'][0]['contextual_patterns'] = [
    {'context':r'竞业(?:限制|禁止)期', 'predicate':DEFINED_TERM}]
_variants('employment_noncompete_term', 1,
    r'经济补偿(?:金)?(?:为|：|:)[^。；\n]{0,80}(?:每月|按月)\s*(?:人民币)?\s*[\d,，]+(?:\.\d+)?\s*元',
    r'(?:离职后|竞业限制期间)[^。；\n]{0,40}(?:每月|按月)[^。；\n]{0,20}(?:支付)?(?:经济)?补偿(?:金)?\s*(?:为|：|:)?\s*(?:人民币)?\s*[\d,，]+\s*元')

# Ordinary labor contracts may satisfy these topics by incorporating statutory
# termination/settlement rules.  Missing bespoke notice delivery or settlement
# deadline language is a drafting refinement, not a standalone actual risk,
# unless a direct adverse clause deprives statutory rights.
PROFILES['employment_exit'][1].update({
    'risk_relevant': False,
    'recommendation_action': 'OPTIONAL',
    'residual_gap': '可选完善解除通知方式或未来解除日期确认机制',
})
PROFILES['employment_compensation'][1].update({
    'risk_relevant': False,
    'recommendation_action': 'OPTIONAL',
    'residual_gap': '可选完善解除终止后工资及经济补偿结算期限',
})
PROFILES['employment_insurance'][1].update({
    'risk_relevant': False,
    'recommendation_action': 'OPTIONAL',
    'residual_gap': '法定个人缴费及代扣代缴机制无需在普通劳动合同中重复列明',
})
# A source-bound normal compensation settlement is an alternative to spelling
# out the statutory formula. Adverse overrides are checked before coverage.
_variants('employment_compensation', 0,
    r'依法(?:需要|应当|应)?[^。；\n]{0,20}支付经济补偿[^。；\n]{0,15}(?:甲方|用人单位)(?:按照|依照|按)法律规定支付',
    r'经济补偿[^。；\n]{0,30}(?:办结|完成|办理完毕)工作交接(?:时|后当日)[^。；\n]{0,8}(?:支付|结清)',
    r'经济补偿[^。；\n]{0,30}工作交接(?:结束|完成|办结)后[^。；\n]{0,8}支付')
PROFILES['employment_compensation'][0]['proposition'] = '经济补偿依法处理、计算依据或正常结算安排'
# Statutory contract content is not made optional by an untriggered hazard
# condition or by statutory remedies being available outside the contract.
PROFILES['employment_safety'][0]['statutory_required_term'] = True

from dataclasses import replace
IP_OWNERSHIP = replace(F('EMP-IP', 1, 'employment_ip_ownership', '劳动成果与知识产权归属',
    ('职务成果', '非职务发明', '著作权', '署名权', '科研成果'),
    '《专利法》第6条、第16条；《著作权法》第10条、第18条；《劳动合同法》第26条', (),
    '按职务发明、职务作品和非职务成果分别界定权利，保留依法享有的署名等人身权；经费和奖励按各自法律性质处理，不仅以在职期间作为全部权利归单位的依据。'), item_id='EMP-IP-01')
LABOR_CHECKLIST = (IDENTITY, TERM, PROBATION, PROBATION_LIMIT, WORK, HOURS, WAGE, INSURANCE, SAFETY, SERVICE, EXIT, COMPENSATION, DISPUTE, ILLEGAL_WAIVER, ILLEGAL_EXIT, PENALTY, NC_SCOPE, NC_TERM, NC_RISK, IP_OWNERSHIP)
NON_COMPETE_CHECKLIST = (IDENTITY, NC_SCOPE, NC_TERM, NC_RISK, DISPUTE, PENALTY)
NDA_IDENTITY = R("NDA", 3, "confidentiality_parties", "保密双方及信息流向", ("披露方", "接收方", "用人单位", "劳动者"), "《民法典》第143条、第509条；《劳动合同法》第23条", [
    ("信息提供方或用人单位可识别", (r"(?:披露方|用人单位)[：:][^。；_]{2,60}",)),
    ("信息接收方或劳动者可识别", (r"(?:接收方|劳动者)[：:][^。；_]{2,60}",)),
])
NDA_REMEDY = R("NDA", 4, "confidentiality_remedies", "保密违约救济", ("保密义务", "赔偿", "停止侵害"), "《民法典》第577条、第584条；《劳动合同法》第25条、第90条", [
    ("保密违反的停止侵害或损失赔偿", (r"(?:违反保密义务|泄露保密信息|泄露商业秘密).{0,65}(?:赔偿|停止侵害|消除影响)",)),
])
CONFIDENTIALITY_CHECKLIST = (NDA_IDENTITY, SECRET, SECRET_DUTY, NDA_REMEDY, PENALTY, NC_SCOPE, NC_TERM, NC_RISK)
TERMINATION_CHECKLIST = (IDENTITY, EXIT, COMPENSATION, HANDOVER, DISPUTE, ILLEGAL_WAIVER, ILLEGAL_EXIT, PENALTY, NC_SCOPE, NC_TERM, NC_RISK)
from review_v2.termination_checklist import TERMINATION_ADDITIONS
TERMINATION_CHECKLIST += TERMINATION_ADDITIONS
