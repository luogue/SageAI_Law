"""Evidence-bound goods requirements, independent of document layout and party name.

Matchers operate on a sentence/field value, never an entire risk-topic packet.
The patterns are conjunctive within an atom; different atoms may have different
sources. Neither a schedule heading nor a related clause alone proves coverage.
"""
import re
import hashlib
from dataclasses import replace


def source_identity(clause_id, quote):
    return f"SOURCE-{clause_id}-{hashlib.sha256(quote.encode('utf-8')).hexdigest()[:12]}"


def atom(key, label, *patterns):
    return {"element_id": key, "proposition": label, "terms": [],
            "sale_patterns": list(patterns), "atomic": True}


DELIVERY = r"交付|交货|供货|送达|到货|发货"
TIME = r"\d+\s*(?:个工作日|日|天|年|月)|[一二三四五六七八九十]+(?:日|天)|订单.{0,12}(?:期限|日期)"
MONEY = r"\d[\d,.，]*\s*(?:%|％|‰|元)|[一二三四五六七八九十]+分之"
CLAIM = r"第三[方人].{0,16}(?:权利|索赔|侵权)|知识产权.{0,16}(?:纠纷|侵权)|权利瑕疵"
PROFILES = {
    "common_litigation_costs": [atom("enforcement_cost_allocation", "实现债权费用承担", r"律师费|诉讼费|实现债权费用", r"承担|支付")],
    "sale_payment_method_account": [
        atom("payment_method", "货款支付方式", r"银行转账|汇款|现金支付|转账支付"),
        atom("payment_account", "具体收款账户", r"银行账号|收款账号|账号|账户", r"\d{6,}")],
    "sale_warranty_period": [
        atom("goods_warranty_duration", "产品质保期限及起算点", r"质保期|保修期|质量保证期", r"\d+(?:个)?(?:月|年|日)"),
        atom("goods_warranty_responsibility", "质保期内质量补救责任", r"质保|保修|质量", r"(?:负责|承担|应当|应予|免费).{0,16}(?:维修|修理|更换)|(?:维修|修理|更换).{0,16}(?:承担|负责)")],
    "sale_inspection_period": [atom("goods_inspection_deadline", "到货后检验验收期限", r"(?:日|天)内(?:组织|完成|进行)?(?:验收|检验)|(?:检验|验收)期限[：:].{0,15}(?:日|天)")],
    "sale_subject_quantity_unit": [atom("goods_subject_quantity", "交付标的物数量和计量单位", r"(?:数量|总量)[：:]?\s*\d[\d,，]*(?:\.\d+)?\s*(?:套|台|件|吨|公斤|千克|米|个|箱)")],
    "common_effective_clause": [atom("contract_effective_condition", "本合同生效条件或日期", r"(?:本合同|合同生效日期).{0,35}(?:生效|\d{4}年)|本合同.{0,35}之日起生效")],
    "sale_quality_remedy": [
        atom("quality_objection_period", "质量异议提出期限或程序", r"质量|验收", r"异议|提出", r"日|天|期限|程序"),
        atom("quality_objection_form", "质量异议的书面通知或可留痕方式", r"质量|验收", r"异议", r"书面|电子邮件|异议单"),
        atom("quality_remedy_method", "质量问题的修理、更换等补救方式", r"质量|异议|问题|整改", r"修理|维修|更换|补发|重作|退货|减少价款|重新交付")],
    "sale_subject_legality": [atom("goods_lawful_source", "货物来源合法", r"货物|产品|设备", r"合法来源|来源合法|合法取得")],
    "sale_subject_quality_standard": [
        atom("goods_quality_standard", "货物质量适用标准", r"货物|产品|质量|验收", r"国家.{0,6}标准|行业标准|技术标准|质量标准|技术参数"),
        atom("goods_technical_parameters", "可识别的货物技术参数", r"\d+(?:\.\d+)?\s*(?:GHz|GB|TB|Hz|mm|W|英寸|核|线程)|分辨率.{0,15}\d",)],
    "sale_delivery_time": [atom("goods_delivery_deadline", "交货时间或期限", DELIVERY, TIME)],
    "sale_delivery_place": [atom("goods_delivery_place", "货物交付地点", r"交付地点|交货地点|收货地址|履约地点|服务地点|指定地点", r"[省市区县路街号仓库厂院]{1}.{3,}")],
    "sale_delivery_method": [
        atom("goods_transport_method", "货物交付或运输方式", r"货物|产品|设备|运输", r"公路|运输|送货|提货|自提|快递"),
        atom("goods_receipt_confirmation", "货物签收或交接确认", r"货物|设备|到货|交货|交付|送货单|交接|验收", r"签收|签字|签署.{0,12}(?:确认|验收)|确认单"),
        atom("goods_receipt_record", "交付签收或验收记录凭证", r"签收单|送货单|物流回执|验收记录|验收报告|交接单|验收单|验收文件")],
    "sale_delay_delivery_liability": [atom("goods_delay_liability", "迟延交货责任", r"逾期|迟延|延迟|未按.{0,16}(?:时间|期限)", DELIVERY, r"违约金|赔偿|解除")],
    "sale_risk_transfer_delivery": [atom("goods_risk_transfer", "货物毁损灭失风险转移节点", r"风险", r"转移|承担", DELIVERY)],
    "sale_risk_carrier_delivery": [atom("goods_transport_risk_allocation", "运输交付中的风险分配", r"风险", r"转移|承担", r"承运人|运输|送达|到货|签收")],
    "sale_payment_schedule": [
        atom("goods_payment_trigger", "价款支付触发条件或时间", r"支付|付款|预付款|尾款", r"生效后|签署后|签订后|到货|验收.{0,20}后|届满|日内|日前|材料后"),
        atom("goods_payment_ratio", "各付款节点的比例或金额", r"支付|付款|预付款|尾款", MONEY + r"|全部货款|全部价款|一次性付清")],
    "sale_invoice_tax": [
        atom("goods_invoice_obligation", "发票提供安排", r"发票", r"提供|提交|开具|开票|发票类型"),
        atom("goods_tax_allocation", "税费承担或含税价安排", r"含税|税费.{0,12}(?:承担|包含)|税金.{0,12}(?:承担|包含)")],
    "sale_quality_standard_basis": [atom("goods_quality_priority", "多项质量标准的适用顺序", r"标准", r"较高|从高|优先|顺序|先后|不一致.*适用")],
    "sale_breach_liability_general": [atom("goods_breach_liability", "违约责任安排", r"违约金|赔偿损失|赔偿.{0,16}经济损失", r"应|承担|支付|赔偿")],
    "sale_liquidated_damages_adjustment": [atom("goods_penalty_loss_relation", "违约金与损失赔偿的关系", r"违约金", r"赔偿|损失|调整|调减")],
    "sale_packaging_requirement": [
        atom("goods_packaging", "货物包装方式或标准", r"包装", r"标准|方式|应|防潮|防震|符合"),
        atom("goods_accompanying_documents", "随货资料交付", r"装箱清单|说明书|用户手册|合格证|保修凭证|软件许可证明", r"交付|提供|随货|随机")],
    "sale_right_defect_no_third_party": [atom("goods_rights_free", "货物无权利瑕疵保证", r"不存在.{0,8}权利瑕疵|无.{0,6}权利负担|不存在.{0,8}第三[方人]权利")],
    "sale_ip_compliance": [
        atom("goods_ip_authorization", "货物或软件合法授权", r"软件|操作系统|驱动|产品|知识产权", r"合法.{0,8}(?:授权|许可)|授权合法|合法有效授权|不侵犯.{0,10}知识产权"),
        atom("goods_ip_handling", "知识产权纠纷处理责任", CLAIM, r"负责处理|承担.{0,8}责任"),
        atom("goods_ip_costs", "知识产权侵权费用或赔偿承担", CLAIM, r"承担.{0,15}(?:费用|赔偿|全部责任)|赔偿损失")],
    "sale_right_defect_notice": [atom("goods_rights_disclosure", "权利瑕疵或第三方权利的披露义务", r"权利瑕疵|第三[方人]权利|权利负担", r"披露|书面告知|如实告知")],
    "sale_right_defect_remedy": [atom("goods_rights_remedy", "第三方权利主张的处理或赔偿措施", CLAIM, r"负责处理|赔偿|承担.{0,15}责任|排除妨碍")],
    "sale_technical_attachment": [atom("goods_specification_schedule", "技术规格或参数清单", r"\d+(?:\.\d+)?\s*(?:GHz|GB|TB|Hz|mm|W|英寸|核|线程)|分辨率.{0,15}\d|技术规格书.{0,12}(?:附件|交付|提供)")],
    "sale_attachment_priority": [
        atom("goods_document_composition", "合同文件组成及附件效力", r"组成合同|合同文件|组成部分|同等法律效力", r"附件|技术|文件|图纸|协议"),
        atom("goods_document_priority", "合同文件解释或冲突顺位", r"合同文件|附件|文件", r"顺序解释|优先顺序|解释顺序|冲突.{0,12}(?:优先|为准)|不一致.{0,12}(?:优先|为准)")],
}


def supports(element, text):
    text = re.sub(r"\s+", "", text)
    if any(re.search(p, text) for p in element.get('negative_patterns', [])):
        return False
    if element['element_id'] == 'quality_remedy_method' and re.search(r"不得.{0,12}更换(?:材料|供应商)|更换材料型号", text):
        return False
    if element['element_id'] == 'goods_receipt_record':
        if re.search(r"(?:无需|不必|不予|未)(?:签署|签收|出具|形成|提供|留存).{0,8}(?:单|文件|记录|报告)", text):
            return False
        if '验收文件' in text and not re.search(r"签署|签字|出具|形成|留存|提供|提交", text):
            return False
    if element['element_id'].startswith('goods_payment_') and re.search(r"违约金|赔偿|损失", text):
        # A quality-retention payment condition can mention unresolved claims;
        # payment *of* damages/penalties is not a purchase-price instalment.
        if not re.search(r"预付款|尾款|质保期|质量保证期|合同总价|支付合同总金额", text) or re.search(r"支付违约金|支付赔偿", text):
            return False
    return bool(element.get("sale_patterns")) and all(re.search(p, text, re.I) for p in element["sale_patterns"])


def source_units(clauses):
    """Keep original excerpts. Attach a standalone field label to its value only."""
    for clause in clauses:
        lines = clause.text.splitlines()
        label = ""
        for line in lines:
            if re.fullmatch(r"[^。；;：:]{2,40}[：:]", line.strip()):
                label = line.strip()
                continue
            for sentence in re.split(r"(?<=[。；;])", line):
                if sentence.strip():
                    source = replace(clause, location=label.rstrip('：:')) if label in {'合同生效日期：', '合同生效日期:'} else clause
                    yield source, (label + "\n" if label else "") + sentence.strip()
                    label = ""


def inspection_period_context(clauses):
    """Collect inputs to a reasonableness assessment, not a 'reasonable' word.

    An objection deadline after acceptance is not an arrival-to-test deadline;
    warranty duration alone does not establish that full testing is feasible.
    Keep those anchors in their source sentences for human evaluation.
    """
    result = {"periods": [], "acceptance_method": [], "latent_defects": []}
    for clause, quote in source_units(clauses):
        compact = re.sub(r"\s+", "", quote)
        categories = []
        # Bind the clock to inspecting/objecting, not a payment or a seller's
        # repair obligation that merely follows acceptance/receipt of objection.
        period_action = (r"(?:日|天)内(?:组织|完成|进行)?(?:验收|检验)"
                         r"|(?:验收|检验)后.{0,24}(?:日|天)内.{0,24}(?:提出|通知)"
                         r"|(?:检验|异议)期限[：:].{0,12}(?:日|天)"
                         r"|(?:当场|即时)(?:验收|检验)")
        if re.search(period_action, compact):
            categories.append("periods")
        if re.search(r"验收|检验", compact) and re.search(r"安装|调试|测试|试运行|抽样|外观|数量|性能", compact):
            categories.append("acceptance_method")
        if re.search(r"隐蔽瑕疵|潜在缺陷|质保|质量保证期|保修", compact):
            categories.append("latent_defects")
        for category in categories:
            if not any(row['quote'] == quote for row in result[category]):
                result[category].append({"quote": quote, "text": quote, "clause_id": clause.clause_id,
                                         "evidence_id": source_identity(clause.clause_id, quote),
                                         "location": clause.location, "source_type": "SOURCE_CLAUSE"})
    return result


def termination_element_context(text, transaction_structure=None):
    """Prerequisites concern the remedy/transaction, not the sale label alone."""
    sentences = re.split(r"[。；;\n]", re.sub(r"[ \t]+", "", text))
    ongoing = transaction_structure == "FRAMEWORK_SUPPLY" or any(
        re.search(r"框架(?:供货|采购|协议)|持续交易|长期合作|订单制采购|按订单(?:供货|采购)|分批下单", s)
        and not re.search(r"不(?:采用|属于)|非框架|[□☐]\s*框架", s) for s in sentences)
    cure = any("解除" in s and re.search(r"催告|限期.{0,8}(?:履行|补救|整改)|补救期|宽限期", s) for s in sentences)
    return {"ongoing_transaction": ongoing, "cure_based_termination": cure}


def extract(node, clauses, profiles=None):
    evidence = []
    requirements = (PROFILES if profiles is None else profiles).get(node, [])
    for clause, quote in source_units(clauses):
        if node == "sale_subject_quantity_unit" and re.search(r"原材料|预计使用数量", clause.text):
            continue
        keys = [row["element_id"] for row in requirements if supports(row, quote)]
        if not keys:
            continue
        evidence.append({"evidence_id": source_identity(clause.clause_id, quote),
                         "clause_id": clause.clause_id, "location": clause.location,
                         "text": quote, "quote": quote, "original_excerpt": quote,
                         "raw_text": clause.text, "source_type": "SOURCE_CLAUSE",
                         "entailment_status": "SUPPORTS", "source_domain": "GOODS_SALE",
                         "supported_elements": keys, "element_ids": keys})
    return evidence


def has_title_retention(text):
    for sentence in re.split(r"[。；;\n]", re.sub(r"\s+", "", text)):
        if re.search(r"不(?:设立|采用|适用|保留).{0,6}所有权|无所有权保留", sentence):
            continue
        if re.search(r"所有权保留|保留.{0,8}所有权|付清.{0,18}所有权.{0,8}(?:归|转移)|所有权.{0,12}付清", sentence):
            return True
    return False


def has_installment_acceleration(text):
    """A payment percentage alone is not an acceleration/termination remedy."""
    for sentence in re.split(r"[。；;\n]", text):
        sentence = re.sub(r"\s+", "", sentence)
        default = re.search(r"(?:逾期|迟延|未按.{0,5})(?:付款|支付)|(?:欠付|未付|未支付).{0,10}(?:价款|货款)|(?:价款|货款).{0,10}(?:逾期|未付)", sentence)
        remedy = re.search(r"五分之一|提前到期|取回|解除合同|(?:支付|偿还).{0,10}全部价款|(?:全部|剩余|未到期).{0,8}价款.{0,12}(?:到期|支付)", sentence)
        if default and remedy:
            return True
    return False
