"""Deterministic non-compete proportionality, using verified obligations only.
Guidance (not statutory invalidity thresholds): 人社厅发〔2025〕40号, arts 13–14.
"""
from decimal import Decimal
from review_v2.employment_fact_store import number
from review_v2.fact_validation import FactExtractionError

GUIDANCE = '《企业实施竞业限制合规指引》第十三、十四条（合理性参考，不直接认定无效）'

def assess(store):
    keys=('non_compete.duration_months','non_compete.compensation','non_compete.compensation_floor','non_compete.salary_base')
    groups={k:store.get(k) for k in keys}
    penalties=[f for f in store.get('penalties.obligations') if f['normalized_value'].get('scope')=='NON_COMPETE' and f['normalized_value'].get('imposed') is True]
    used=[f for fs in groups.values() for f in fs]+penalties
    def unique(key):
        vals=[f['normalized_value'] for f in groups[key]]
        return vals[0] if vals and all(v==vals[0] for v in vals) else None
    def money(v):
        return Decimal(str(v['amount'])) if isinstance(v,dict) and v.get('amount') is not None and v.get('unit')=='CNY/MONTH' else None
    duration=unique(keys[0]);comp=unique(keys[1]);floor=money(unique(keys[2]));base=money(unique(keys[3]))
    formula=(comp or {}).get('formula',{});ratio=formula.get('percent');monthly=money(comp)
    checks=[];risk=[]
    if ratio is not None and formula.get('kind')=='PERCENT_OF_BASE':
        if base is not None and unique(keys[3]).get('base')==formula.get('base'):
            monthly=base*number(ratio)/100
        else: base=None
    if monthly is not None and floor is not None: monthly=max(monthly,floor)
    total=monthly*Decimal(str(duration)) if monthly is not None and duration is not None else None
    lower=floor*Decimal(str(duration)) if floor is not None and duration is not None else None
    effective=monthly/base*100 if monthly is not None and base else None
    reference=50 if duration is not None and duration>12 else 30
    if ratio is not None and number(ratio)<reference and (effective is None or effective<reference):
        checks.append(f'竞业期限{duration:g}个月、补偿比例{number(ratio):g}%，需结合保底金额、工资基数和限制就业程度核验补偿合理性；指引对该期限建议参考{reference}%，不据此直接认定违法或无效。' if duration is not None else '竞业期限不明，需结合补偿比例核验限制与补偿是否相称。')
    amounts=[]
    for f in penalties:
        v=f['normalized_value']
        try: amount=number(v['amount_text'])
        except (KeyError,ValueError,TypeError,FactExtractionError): amount=None
        if amount is not None and (not amount.is_finite() or amount<0): amount=None
        if amount is None:
            checks.append('竞业违约金采用非固定金额或公式，需核验其计算依据及与补偿总额的比例。');continue
        if amount not in amounts: amounts.append(amount)
        if total is None:
            missing = []
            if duration is None: missing.append('竞业期限')
            if ratio is not None and base is None: missing.append('与补偿公式同口径的工资基数')
            if comp is None or (monthly is None and ratio is None): missing.append('完整补偿计算标准')
            message = f'竞业违约金{amount:g}元；尚需核验'+ '、'.join(missing or ['补偿计算依据']) + '，无法确定补偿总额及准确倍数，需结合损失、秘密价值等核验是否明显过高。'
            if lower is not None and lower>0:
                message += f'按保底标准计算，全期补偿下限为{lower:g}元（非实际总额），该违约金不超过此下限的{amount/lower:.2f}倍，不能仅据金额认定过高。'
            checks.append(message)
        elif total>0 and amount>total*5:
            risk.append(f'竞业违约金{amount:g}元为约定补偿总额{total:g}元的{amount/total:.2f}倍，超过合规指引一般不宜超过5倍的参考，存在明显比例失衡风险；仍需结合损失、秘密价值等判断，不当然无效。')
    if len(groups[keys[1]])>1 or len(groups[keys[0]])>1 or len(groups[keys[3]])>1:
        checks.append('存在多项期限或计酬口径，需核对是否为同一竞业安排，不能直接合计。')
    snapshot={'noncompete_duration_months':duration,'compensation_ratio':ratio,'compensation_floor_amount':float(floor) if floor is not None else None,'employee_salary_base':float(base) if base is not None else None,'estimated_total_compensation':float(total) if total is not None else None,'total_lower_bound':float(lower) if lower is not None else None,'noncompete_penalty_amounts':[float(a) for a in amounts], 'source_fact_ids':list(dict.fromkeys(f['fact_id'] for f in used)),'basis':GUIDANCE,'checks':checks,'risks':risk}
    return snapshot,used

