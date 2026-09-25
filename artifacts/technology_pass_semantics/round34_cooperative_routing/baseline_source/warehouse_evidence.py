"""Scope-sensitive warehouse evidence; intake inspection is not depositor access."""
import re

# Bind numbers to the storage-price field, never to area, loading charges or
# another amount elsewhere in the candidate clause. Reuse this in final search.
FEE_VALUE_PATTERN = (
    r'(?:仓储费|仓库租金|月租金|每平方米|每吨|每立方米)'
    r'(?:为|是|按|每|吨|件|立方米|平方[米]?|日|天|月|年|计算|计收|收取|人民币|单价|[:：=￥¥]|\s){0,20}'
    r'(?:\d[\d,，]*(?:\.\d+)?|[壹贰叁肆伍陆柒捌玖拾佰仟万]+)\s*元'
)

PROFILES = {
    'inspection_sampling_right': ('depositor_inspection_sampling', '存货人或仓单持有人检查仓储物及提取样品的权利', ['检查仓储物', '取样', '提取样品']),
    'partial_damage_return': ('partial_damage_disposition', '部分毁损灭失时未损部分处置及损失承担', ['部分毁损', '部分灭失', '未毁损部分', '未损部分']),
    'value_depreciation_liability': ('depreciation_compensation', '仓储物价值减损的赔偿安排', ['价值减损', '贬值', '货值下降', '减损价值']),
}


def supports(node, text):
    text = re.sub(r'\s+', '', text)
    if node == 'inspection_sampling_right':
        return bool(re.search(r'(?:存货人|仓单持有人|甲方).{0,25}(?:有权|可以|可|要求).{0,25}(?:检查|查验)', text)
                    and re.search(r'取样|提取样品|抽样', text)
                    and not re.search(r'不得.{0,15}(?:检查|取样)', text))
    if node == 'partial_damage_return':
        return bool(re.search(r'部分毁损|部分灭失|未毁损部分|未损部分', text)
                    and re.search(r'返还|继续保管|处置', text) and re.search(r'赔偿|损失承担', text))
    return bool(re.search(r'价值减损|贬值|货值下降|减损价值', text) and re.search(r'赔偿|补偿', text))


def apply(items, clauses):
    from review_v2.engine import _set_item_pass, _set_item_missing
    for item in items:
        if item.node_id == 'storage_fee_amount':
            apply_fee(item, clauses)
            continue
        if item.node_id not in PROFILES:
            continue
        key, proposition, terms = PROFILES[item.node_id]
        item.decision_trace['warehouse_scope_elements'] = [dict(element_id=key, proposition=proposition, terms=terms)]
        sources = []
        for clause in clauses:
            if supports(item.node_id, clause.text):
                sources.append(dict(clause_id=clause.clause_id, location=clause.location,
                    text=clause.text, quote=clause.text, source_type='SOURCE_CLAUSE',
                    supported_elements=[key], evidence_id=f'WH-SCOPE-{key}-{clause.clause_id}'))
        if sources:
            _set_item_pass(item, [], proposition + '已有直接合同条款。', proposition + '已有直接合同条款。')
            item.evidence_clauses = sources
            item.evidence_location = '；'.join(dict.fromkeys(e['location'] for e in sources))
            item.suggested_clause_example = ''
        else:
            _set_item_missing(item, item.risk_level, '全文未找到直接约定：' + proposition + '。',
                              '尚未明确：' + proposition + '；入库检查或一般损失赔偿不证明该专项安排。', 'warehouse_scope_evidence')
            item.evidence_clauses = []
            item.evidence_location = ''
        item.judge_source = 'warehouse_scope_evidence'
    return items


def apply_fee(item, clauses):
    from review_v2.engine import _set_item_pass, _set_item_partial
    terms = ['仓储费', '仓库租金', '月租金', '租金', '每平方米']
    candidates = [c for c in clauses if re.search(r'仓储费|仓库租金|月租金|租金|每平方米', c.text)
                  and re.search(r'元|计费|包库|按月|按日|收费', c.text)]
    if not candidates:
        return
    amount = [c for c in candidates if re.search(FEE_VALUE_PATTERN, c.text)]
    item.decision_trace['warehouse_scope_elements'] = [
        dict(element_id='storage_fee_arrangement', proposition='仓储费计费安排', terms=terms,
             semantic_patterns=[r'(?:仓储费|仓库租金|月租金|租金|每平方米).{0,100}(?:元|计费|包库|按月|按日|收费)']),
        dict(element_id='storage_fee_value', proposition='仓储费具体金额或单价', terms=['具体金额', '具体单价'],
             semantic_patterns=[FEE_VALUE_PATTERN]),
    ]
    item.decision_trace['semantic_requirements'] = item.decision_trace['warehouse_scope_elements']
    sources = [dict(clause_id=c.clause_id, location=c.location, text=c.text, quote=c.text,
                    source_type='SOURCE_CLAUSE', evidence_id=f'WH-FEE-{c.clause_id}',
                    supported_elements=['storage_fee_arrangement'] + (['storage_fee_value'] if c in amount else []))
               for c in candidates]
    if amount:
        _set_item_pass(item, [], '仓储费计费安排及具体金额或单价已有明确约定。', '仓库租金属于本仓储合同的计费安排。')
        item.suggested_clause_example = ''
    else:
        reason = '已约定仓储费计费安排，但具体金额或单价尚未填写或确定。'
        _set_item_partial(item, [], '中', reason, reason)
        item.suggested_clause_example = '建议填写或明确仓储费的具体金额或单价。'
    item.evidence_clauses = sources
    item.evidence_location = '；'.join(dict.fromkeys(c.location for c in candidates))
    item.judge_source = 'warehouse_fee_evidence'
