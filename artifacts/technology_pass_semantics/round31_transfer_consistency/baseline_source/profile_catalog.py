"""Contract-scoped profile options shared with the UI through /profile-options.

Roles describe a party's legal position, never company size or risk appetite.
The first role is the visible initial selection; unknown types stay neutral.
"""

NEUTRAL_IDENTITY = "合同当事人"
NEUTRAL_SCENARIO = "一般合同"

# type: (roles, scenarios). Keep rental usage exclusively in house_lease.
PROFILE_OPTIONS = {
    "house_lease": (("承租人", "出租人"), ("居住用途", "商业经营", "投资/转租")),
    "sale": (("买方", "卖方"), ("商品买卖", "设备买卖", "房地产买卖", "商业经营")),
    "work_contract": (("定作方", "承揽方"), ("承揽加工", "定作", "修理")),
    "transportation": (("托运人", "承运人", "收货人"), ("货物运输", "危险品运输", "多式联运")),
    "equity_transfer": (("转让方", "受让方"), ("股权转让",)),
    "investment": (("投资方", "融资方"), ("股权投资",)),
    "capital_increase": (("投资方", "融资方", "原股东"), ("增资扩股",)),
    "shareholders": (("股东", "公司"), ("公司治理", "共同出资设立公司")),
    "labor": (("劳动者", "用人单位"), ("劳动用工",)),
    "non_compete": (("劳动者", "用人单位"), ("竞业限制",)),
    "employment_termination": (("劳动者", "用人单位"), ("劳动关系解除/终止",)),
    "confidentiality": (("信息披露方", "信息接收方"), ("保密信息披露",)),
    "mortgage": (("抵押人", "抵押权人"), ("抵押担保",)),
    "movable_pledge": (("出质人", "质权人"), ("动产质押",)),
    "equity_pledge": (("出质人", "质权人"), ("股权质押",)),
    "rights_pledge": (("出质人", "质权人"), ("权利质押",)),
    "gift": (("赠与人", "受赠人"), ("财产赠与",)),
    "deposit": (("寄存人", "保管人"), ("保管",)),
    "agency": (("委托人", "受托人"), ("委托事务",)),
    "loan": (("借款人", "贷款人"), ("借款融资",)),
    "service": (("服务接受方", "服务提供方"), ("服务履行",)),
    "guarantee": (("保证人", "债权人"), ("保证担保",)),
    "finance_lease": (("承租人", "出租人"), ("融资租赁",)),
    "warehouse": (("存货人", "保管人"), ("仓储保管",)),
    "construction": (("发包人", "承包人"), ("建设工程",)),
    "technology": (("甲方", "乙方"), ("技术交易",)),
    "commission_agency": (("委托人", "行纪人"), ("行纪交易",)),
    "utility_supply": (("用能人", "供能人"), ("电水气热供应",)),
    "brokerage": (("委托人", "中介人"), ("中介服务",)),
    "operating_cooperation": (("合同当事人",), ("承包经营及业务合作",)),
}

# Legacy API callers use legal synonyms or party-qualified labels. Normalize
# within a type so, for example, an explicit seller is never reset to buyer.
ROLE_ALIASES = {
    "house_lease": {"承租方": "承租人", "出租方": "出租人", "房东": "出租人", "租客": "承租人"},
    "sale": {"买受人": "买方", "采购人": "买方", "采购方": "买方", "需方": "买方",
             "出卖人": "卖方", "供应商": "卖方", "供方": "卖方"},
    "work_contract": {"定作人": "定作方", "承揽人": "承揽方"},
    "transportation": {"托运方": "托运人", "承运方": "承运人"},
    "investment": {"目标公司": "融资方"},
    "capital_increase": {"目标公司": "融资方"},
    "labor": {"员工": "劳动者", "雇主": "用人单位"},
}


def profile_options(contract_type):
    key = "house_lease" if contract_type == "lease" else contract_type
    roles, scenarios = PROFILE_OPTIONS.get(key, ((NEUTRAL_IDENTITY,), (NEUTRAL_SCENARIO,)))
    return {"identities": list(dict.fromkeys((*roles, NEUTRAL_IDENTITY))), "scenarios": list(scenarios)}


def profile_catalog():
    return {key: profile_options(key) for key in PROFILE_OPTIONS}
