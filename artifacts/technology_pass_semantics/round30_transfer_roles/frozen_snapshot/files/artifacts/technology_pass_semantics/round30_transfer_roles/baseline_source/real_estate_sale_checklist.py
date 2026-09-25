"""Material review pack for real-estate sale contracts."""

from __future__ import annotations

from typing import Tuple

from review_v2.house_lease_checklist import ReviewCheckpoint


def _review(item_id: str, node_id: str, title: str, risk: str, terms: Tuple[str, ...], group: str, applicable_if: str = "房地产买卖合同", applicability_triggers: Tuple[str, ...] = (), claim_requirements: Tuple[str, ...] = ()) -> ReviewCheckpoint:
    risk_point = f"合同未充分明确{title}，可能影响房产权属转移、价款安全或违约救济。"
    return ReviewCheckpoint(
        item_id=item_id, node_id=node_id, title=title, kind="required", risk_level=risk,
        terms=terms, risk_point_missing=risk_point,
        risk_point_present=f"合同已约定{title}，仍应核对登记材料、金额、期限及附件的一致性。",
        suggested_clause=f"双方应明确约定{title}的具体内容、办理期限、证明文件、协作义务和未完成时的责任。",
        legal_basis="《中华人民共和国民法典》合同编、物权编及不动产登记相关规则",
        legal_consequence_if_missing=risk_point,
        semantic_question=f"合同是否以明确、可执行且有证据支持的方式约定了{title}？",
        evidence_scope="正式合同条款、不动产权属资料及合同附件",
        pass_criteria=f"存在关于{title}的明确约定，关键主体、金额、日期或证明文件完整。",
        partial_criteria=f"提及{title}但关键主体、金额、日期、条件、责任或附件不完整。",
        applicable_if=applicable_if,
        allowed_families=("SALE",), allowed_subject_matters=("REAL_ESTATE",),
        domain_owner="sale/real_estate", material_group=group,
        applicability_triggers=applicability_triggers, claim_requirements=claim_requirements,
    )


REAL_ESTATE_SALE_REVIEW_CHECKLIST: Tuple[ReviewCheckpoint, ...] = (
    _review("RE-01-01", "real_estate_seller_identity", "出卖人身份与处分主体", "高", ("出卖人", "卖售人", "甲方", "身份证号码"), "TITLE"),
    _review("RE-01-02", "real_estate_buyer_identity", "买受人身份与登记主体", "高", ("买受人", "乙方", "身份证号码"), "TITLE"),
    _review("RE-01-03", "real_estate_registered_owner", "登记权利人与出卖人一致性", "高", ("登记权利人", "合法登记权利人", "不动产权证"), "TITLE"),
    _review("RE-01-04", "real_estate_coownership", "共有情况与共有人同意", "高", ("共有情况", "共同共有", "按份共有", "共有人同意"), "TITLE"),
    _review("RE-01-05", "real_estate_spouse_consent", "配偶知情及出售同意", "高", ("配偶", "同意出售", "婚姻关系", "无异议"), "TITLE", "出卖人有配偶或合同披露婚姻关系"),
    _review("RE-01-06", "real_estate_agent_authority", "代理签约和过户授权", "高", ("委托代理人", "授权委托书", "代理签署", "代办过户"), "TITLE", "存在代理签约或代办登记安排", ("agent.exists",)),
    _review("RE-01-07", "real_estate_certificate", "不动产权证号与权属资料", "高", ("不动产权", "房地产权证号", "权属资料", "产权证"), "TITLE"),
    _review("RE-01-08", "real_estate_disposition_restriction", "查封、限售及处分限制", "高", ("司法查封", "限制处分", "限售", "产权争议"), "ENCUMBRANCE"),
    _review("RE-02-01", "real_estate_mortgage_status", "抵押状态及债权余额", "高", ("存在抵押", "抵押权人", "剩余贷款本金", "抵押情况"), "ENCUMBRANCE"),
    _review("RE-02-02", "real_estate_mortgage_release", "还贷及抵押注销期限", "高", ("抵押注销", "结清抵押贷款", "注销证明", "完成还贷"), "ENCUMBRANCE", "房地产存在抵押或贷款余额"),
    _review("RE-02-03", "real_estate_mortgage_payment_protection", "解押失败时的停付和解约保护", "高", ("暂停支付", "尚未支付的房款", "有权解除合同", "抵押登记仍未注销"), "ENCUMBRANCE", "房地产存在抵押或贷款余额"),
    _review("RE-02-04", "real_estate_third_party_rights", "第三方权利负担披露", "高", ("第三方权利", "权利负担", "相邻关系", "占用"), "ENCUMBRANCE", claim_requirements=("property.mortgage.disclosed", "property.judicial_seizure.disclosed", "property.ownership_dispute.disclosed", "property.coownership.disclosed", "property.lease.disclosed", "seller.encumbrance_warranty.exists")),
    _review("RE-02-05", "real_estate_existing_lease", "现有租赁及空置交付状态", "中", ("租赁情况", "无租赁", "出租情况", "空置状态"), "ENCUMBRANCE"),
    _review("RE-03-01", "real_estate_property_identity", "房屋坐落、类型与范围", "高", ("房地产坐落", "房屋类型", "四至范围", "平面图"), "PROPERTY"),
    _review("RE-03-02", "real_estate_area_usage", "建筑面积与房屋用途", "高", ("建筑面积", "平方米", "房屋用途", "居住"), "PROPERTY"),
    _review("RE-03-03", "real_estate_land_use_right", "土地权属、用途和使用期限", "高", ("土地使用权", "土地用途", "出让", "使用年限"), "LAND_USE"),
    _review("RE-03-04", "real_estate_accessories", "装修、设备及附属物范围", "中", ("设备及装饰", "附属设施", "随房屋", "附件二"), "PROPERTY"),
    _review("RE-04-01", "real_estate_total_price", "房地产转让总价款", "高", ("房地产转让价款", "房地产总价", "房价款", "人民币"), "PRICE"),
    _review("RE-04-02", "real_estate_deposit_downpayment", "定金与首期房款", "高", ("定金", "首期房款", "首付款", "累计已支付"), "PAYMENT"),
    _review("RE-04-03", "real_estate_purchase_financing", "住房贷款及贷款不足处理", "高", ("住房贷款", "贷款金额", "补足差额", "放款条件"), "PAYMENT"),
    _review("RE-04-04", "real_estate_balance_holdback", "尾款与交割保证款", "高", ("尾款", "剩余", "保证款", "户口迁出"), "PAYMENT"),
    _review("RE-04-05", "real_estate_payment_account", "付款节点与资金监管账户", "高", ("付款协议", "收款账户", "资金监管账户", "支付期限"), "PAYMENT"),
    _review("RE-05-01", "real_estate_transfer_deadline", "转移登记申请期限", "高", ("转移登记", "过户手续", "房地产过户", "权利转移日期"), "REGISTRATION"),
    _review("RE-05-02", "real_estate_registration_cooperation", "登记机构与双方协作义务", "高", ("房地产交易中心", "登记机构", "积极给予协助", "提供相关材料"), "REGISTRATION"),
    _review("RE-05-03", "real_estate_advance_notice_registration", "预告登记触发与期限", "中", ("预告登记", "第一期房款", "工作日内", "配合办理"), "REGISTRATION"),
    _review("RE-05-04", "real_estate_registration_failure", "登记失败的责任和退出机制", "高", ("不予登记", "无法办理过户", "解除合同", "实际损失"), "REGISTRATION"),
    _review("RE-06-01", "real_estate_delivery_deadline", "腾空和交房期限", "高", ("腾空", "交房通知", "验收交接", "交付房屋"), "DELIVERY"),
    _review("RE-06-02", "real_estate_inspection", "交房查验范围与期限", "中", ("查验", "验收交接", "装修", "水、电、燃气"), "DELIVERY"),
    _review("RE-06-03", "real_estate_possession_handover", "钥匙、占有及交接凭证", "高", ("钥匙", "转移占有", "交接书", "实际交付"), "DELIVERY"),
    _review("RE-06-04", "real_estate_risk_transfer", "房屋毁损灭失风险转移", "高", ("毁损、灭失风险", "实际交付前", "风险由", "转移占有"), "RISK_TRANSFER"),
    _review("RE-06-05", "real_estate_property_fee_settlement", "物业水电燃气等费用结清", "中", ("物业", "水、电、燃气", "费用结清", "交割"), "DELIVERY"),
    _review("RE-07-01", "real_estate_condition_disclosure", "房屋现状及重大瑕疵披露", "高", ("房地产现状", "现场查看", "结构性损坏", "隐瞒重大质量问题"), "PROPERTY"),
    _review("RE-07-02", "real_estate_defect_remedy", "权利瑕疵和物理瑕疵责任", "高", ("权利瑕疵", "质量问题", "故意隐瞒", "承担责任"), "PROPERTY"),
    _review("RE-08-01", "real_estate_household_registration", "户口人数、迁出期限及保证款", "高", ("户口迁移", "登记户口", "迁出手续", "保证款"), "HOUSEHOLD_REGISTRATION", "住宅房地产买卖"),
    _review("RE-09-01", "real_estate_maintenance_fund", "维修资金账户变更及欠缴情形", "中", ("维修资金", "维修基金", "户名变更", "欠缴"), "MAINTENANCE_FUND", "住宅房地产买卖"),
    _review("RE-10-01", "real_estate_specific_breach", "解押、过户、交房及户口违约责任", "高", ("逾期", "违约责任", "解除合同", "已支付房款"), "BREACH"),
)
