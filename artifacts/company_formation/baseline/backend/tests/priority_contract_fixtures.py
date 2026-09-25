"""Hand-written contracts, independent of rule patterns; no external files/API.

Amounts, parties and identifiers are fictional. Each leaf has a normal,
materially incomplete and affirmative adverse version.
"""
EMPLOYMENT_ID = "用人单位：远山科技有限公司，住所：上海市长宁区长宁路88号。劳动者：张三，身份证：310101199001010011。"
LABOR = [EMPLOYMENT_ID,
    "本合同为固定期限，自2026年1月1日起至2028年12月31日。",
    "试用期为三个月，试用期月工资为8000元，不低于当地最低工资。",
    "工作岗位：软件工程师，工作内容：系统开发和维护，工作地点：上海市长宁区长宁路88号。",
    "实行标准工时，每天8小时，每周40小时，每周休息两日，依法享有年休假。加班依法支付加班工资。",
    "月工资为10000元，每月15日支付，工资通过银行转账支付。",
    "用人单位依法按月缴纳社会保险，劳动者个人应缴部分由用人单位代扣代缴。",
    "用人单位提供防护用品并组织安全培训，对职业危害如实告知并安排职业健康检查。",
    "双方协商一致可以解除本合同，解除应书面通知；其他解除终止依照劳动合同法法定条件办理。",
    "经济补偿按照劳动合同法第46条、第47条及工作年限和月工资计算，解除后5日内结清工资和经济补偿。",
    "劳动争议协商不成，依法向有管辖权的劳动争议仲裁委员会申请仲裁。",
    "本合同自双方签字盖章之日起生效。",
]
NC = [EMPLOYMENT_ID,
    "劳动者为高级技术人员，实际接触源代码等商业秘密，竞业限制范围为上海市工业控制软件开发业务，与所接触秘密范围相适应。",
    "离职后竞业限制期限为一年，用人单位每月支付经济补偿3000元。",
    "劳动争议协商不成，依法向有管辖权的劳动争议仲裁委员会申请仲裁。",
]
NDA = [
    "披露方：远山有限公司。接收方：海川有限公司。双方就保密信息合作交换订立本协议。",
    "保密信息包括未公开的产品设计图和技术参数，不包括公开信息、接收方原已知悉的信息、独立开发的信息、从合法第三人取得的信息以及依法院要求披露的信息。",
    "接收方不得泄露保密信息，仅限指定项目人员为合作目的使用。",
    "保密义务期限为五年，信息合法公开后该部分保密义务终止。",
    "协议终止后5日内返还或销毁资料，并提交书面销毁记录。",
    "违反保密义务的接收方应赔偿披露方因此发生的实际损失。",
]
TERMINATION = [EMPLOYMENT_ID,
    "由用人单位提出，经双方协商一致解除劳动合同，解除日期为2026年9月30日。",
    "经济补偿按劳动合同法第47条计算为30000元，解除后5日内支付补偿并结清工资。",
    "用人单位在解除当日出具解除劳动合同证明，并在15日内办理档案和社会保险关系转移。劳动者在5日内完成工作交接。",
    "劳动争议协商不成，依法向有管辖权的劳动争议仲裁委员会申请仲裁。",
]
SECURITY = [
    "债权人：海川银行，抵押权人及质权人均为债权人。抵押人及出质人：远山有限公司。",
    "主合同编号：JK-2026-1，债务人：星河有限公司，本金为100万元，债务履行期限：2028年12月31日。",
    "担保范围包括本金、利息、违约金和实现担保物权的合理费用。",
    "抵押人及出质人承诺对担保财产合法所有并享有处分权，无共有；应提交股东会授权决议供债权人核验。",
    "担保财产不存在在先担保、查封和冻结，双方通过登记查询核验受偿顺位。",
    "债务到期未清偿，债权人可依法拍卖、变卖或协议折价并优先受偿。超出债权部分返还担保人，不足部分由债务人继续清偿。",
    "抵押权在主债权诉讼时效期间内行使，质权应及时行使；主债权消灭后5日内办理注销或返还质物。",
    "本合同自双方签字盖章之日起生效。不可抗力致不能履行时应及时通知并提供证明，按影响依法免除相应责任。",
]
MORTGAGE = SECURITY + [
    "抵押财产为厂房，坐落：上海市长宁区长宁路88号，面积1000平方米，不动产权证：沪2026字第12345号。",
    "双方在签约后10日内到不动产登记机构办理抵押登记；取得登记证明后提交债权人核验。",
]
MOVABLE = SECURITY + [
    "质物为机床，数量10台，编号：J-001至J-010。质权人应妥善保管，因保管不善造成损毁应赔偿损失。",
    "签约后5日内将质物移交质权人占有，双方签署交付清单。",
]
EQUITY_PLEDGE = SECURITY + [
    "目标公司：星河有限公司，出质比例为20%，出质人认缴20万元，实缴20万元。",
    "双方在签约后10日内向市场监督管理登记机关办理股权出质登记，并提交出质登记通知书。",
]
RIGHTS = SECURITY + [
    "质押标的为应收账款，基础合同编号：XS-2026-88，付款义务人：海风有限公司，金额100万元，到期日2028年12月31日。",
    "双方应就应收账款办理质押登记，在签约后5日内通过动产融资统一登记公示系统取得登记证明。",
    "双方将质押及回款安排向付款义务人书面通知并取得确认，回款支付至指定账户专户。",
]
EQUITY = [
    "转让方：远山有限公司，投资方及受让方：海川有限公司，目标公司：星河有限公司。转让方持有20%股权，保证合法持有并具有处分权。",
    "该股权认缴20万元，实缴20万元，出资期限为2026年9月30日。全部实缴且不存在出资瑕疵；未缴出资由责任方承担，不影响法定责任。",
    "转让方保证股权无质押无冻结，财务及债务真实披露。陈述不实或隐瞒债务的应赔偿损失，受让方有权解除。",
    "本协议自双方签字盖章之日起生效。不可抗力造成无法履行时应通知并提供证明，按影响依法免责。",
]
TRANSFER = [
    "双方应核验公司章程转让限制，向其他股东书面通知股权数量、价格、支付方式及支付期限，其他股东享有优先购买权并在30日内行使；全体其他股东书面放弃优先购买权后办理交割。",
    "转让价款为100万元，签署后5日内支付至转让方银行账户。",
    "交割条件为审批及优先权处理完成，未满足则延期30日，仍未完成可解除并退款。目标公司更新股东名册并签发出资证明，修改公司章程；目标公司在交割后10日内办理变更登记。",
]
CAPITAL = [
    "投资款为100万元，签署后5日内支付至目标公司银行账户。新增注册资本20万元，计入资本公积80万元。",
    "投资方认缴新增出资的缴付期限为2026年9月30日，以货币出资。原股东依实缴比例优先认缴，全体股东一致同意本次认缴安排并书面放弃优先认缴权。",
    "投前估值为400万元，投后持股比例为20%，按投后注册资本计算。",
    TRANSFER[2],
]
GOVERNANCE = [
    "董事会由三名董事组成，投资方享有一席；股东会重大事项按公司法及章程规定表决。股东有权查阅财务报表和会计账簿。",
    "发生治理僵局且连续两次无法决议，双方协商30日；协商不成可通过独立评估定价转让股权退出，符合条件时依法请求法院解散公司。",
]


def document(title, paragraphs):
    return title + "\n" + "\n".join(f"第{i}条 {p}" for i, p in enumerate(paragraphs, 1))


NORMAL = {
    "labor": document("劳动合同", LABOR),
    "non_compete": document("竞业限制协议", NC),
    "confidentiality": document("保密协议", NDA),
    "employment_termination": document("劳动关系解除协议", TERMINATION),
    "mortgage": document("抵押合同", MORTGAGE),
    "movable_pledge": document("动产质押合同", MOVABLE),
    "equity_pledge": document("股权质押合同", EQUITY_PLEDGE),
    "rights_pledge": document("应收账款质押合同", RIGHTS),
    "equity_transfer": document("股权转让协议", EQUITY + TRANSFER),
    "capital_increase": document("增资扩股协议", EQUITY + CAPITAL + GOVERNANCE),
    "investment": document("投资协议", EQUITY + CAPITAL + GOVERNANCE),
    "shareholders": document("股东协议", EQUITY + GOVERNANCE),
}
CRITICAL_NODES = {
    "labor": "employment_wage", "non_compete": "employment_noncompete_scope",
    "confidentiality": "employment_secret_scope", "employment_termination": "employment_compensation",
    "mortgage": "security_main_debt", "movable_pledge": "pledge_movable_delivery",
    "equity_pledge": "pledge_equity_registration", "rights_pledge": "pledge_rights_publicity",
    "equity_transfer": "equity_closing_registration", "capital_increase": "equity_capital_increase",
    "investment": "equity_valuation", "shareholders": "equity_governance",
}
ADVERSE_CLAUSES = {
    "labor": ("用人单位不缴纳社会保险，劳动者自愿放弃社保。", "employment_illegal_waiver"),
    "non_compete": ("离职后竞业限制期限为五年。", "employment_noncompete_adverse"),
    "confidentiality": ("本协议同时适用于用人单位雇员，劳动者违反保密义务应支付违约金50000元。", "employment_general_penalty"),
    "employment_termination": ("劳动者自愿放弃社会保险。", "employment_illegal_waiver"),
    "mortgage": ("如债务到期未清偿，抵押财产直接归债权人所有。", "security_forfeiture"),
    "movable_pledge": ("债务人不履行到期债务，质物直接归质权人所有。", "security_forfeiture"),
    "equity_pledge": ("债务人不履行到期债务，股权直接归质权人所有。", "security_forfeiture"),
    "rights_pledge": ("债务人不履行到期债务，应收账款直接归质权人所有。", "security_forfeiture"),
    "equity_transfer": ("对外转让股权无需通知其他股东。", "equity_mandatory_rights_waiver"),
    "capital_increase": ("目标公司回购股权不经减资法定程序。", "equity_mandatory_rights_waiver"),
    "investment": ("目标公司回购股权无需履行减资程序。", "equity_mandatory_rights_waiver"),
    "shareholders": ("股东永久放弃知情权。", "equity_mandatory_rights_waiver"),
}
MISSING = {key: value.splitlines()[0] + "\n第一条 本协议经双方协商签署，具体履行安排另行协商。" for key, value in NORMAL.items()}
RISKY = {key: value + "\n第99条 " + ADVERSE_CLAUSES[key][0] for key, value in NORMAL.items()}
