"""Symbolic interest expressions built exclusively from verified typed inputs."""
from decimal import Decimal
from review_v2.unified_facts.store import VerifiedFactStore,fail


def expression(rate,rate_unit,time_unit,day_basis,base):
    if rate is None or rate_unit not in {'DAY','MONTH','YEAR','ONCE'} or base=='UNKNOWN':
        return {'state':'UNKNOWN','reason':'利率、期间单位或计费基数不能确定'}
    if rate_unit=='ONCE':
        return {'state':'PRESENT','expression':f'{base} × {rate}%（一次性）','rate_value':str(rate),'rate_unit':rate_unit}
    if time_unit not in {'DAY','MONTH','YEAR'}:
        return {'state':'UNKNOWN','reason':'缺少明确计息时长单位'}
    labels={'DAY':'日','MONTH':'月','YEAR':'年'}
    term=f'{base} × {rate}%'
    divisor=None
    if rate_unit=='YEAR' and time_unit=='DAY':
        divisor={'ACT_360':'360','ACT_365':'365','ACT_ACT':'对应年度实际天数'}.get(day_basis)
        if divisor is None:
            return {'state':'UNKNOWN','reason':'未约定年转日计息基准，不能假定360或365'}
        term+=f' ÷ {divisor}'
    elif rate_unit!=time_unit:
        return {'state':'UNKNOWN','reason':'缺少该利率单位到计息单位的换算约定'}
    return {'state':'PRESENT','expression':term+f' × 实际计息{labels[time_unit]}数',
        'rate_value':str(rate),'rate_unit':rate_unit,'time_unit':time_unit,'day_count_divisor':divisor}


def build(store):
    if not isinstance(store,VerifiedFactStore):fail('VERIFIED_LOAN_STORE_REQUIRED')
    consumer='loan_formula_builder'
    keys=['loan.regular_rate','loan.regular_rate_period','loan.day_count_basis',
          'loan.cost_components','loan.compound']
    get=lambda k:store.scalar(k,consumer=consumer)
    rate=get(keys[0]);unit=get(keys[1]);basis=get(keys[2])
    charges=store.get('loan.cost_components',consumer=consumer)
    output=[]
    base_names={'PRINCIPAL':'原始借款总额','UNPAID_PRINCIPAL':'实际未偿本金',
                'UNPAID_INTEREST':'应付未付利息','UNKNOWN':'UNKNOWN'}
    for fact in charges:
        if fact['state']!='PRESENT':continue
        value=fact['normalized_value'];r=value['rate']
        percent=r.get('percent') if r['state']=='PRESENT' else None
        period=r.get('period')
        if r['state']=='PRESENT' and 'multiplier' in r and rate is not None:
            percent=rate*r['multiplier'];period=unit
        # Fixed-period charge is already expressed in that time unit. YEAR
        # charges use the expressly extracted contract accrual convention.
        # DAY/MONTH rates already define their own period. A YEAR rate is
        # converted to days only with an explicit verified day-count convention;
        # otherwise the expression remains pending, with no guessed denominator.
        time_unit=('DAY' if basis in {'ACT_360','ACT_365','ACT_ACT'} else None) if period=='YEAR' else period
        row=expression(percent,period,time_unit,basis,base_names[value['base']])
        related=[f for f in store.snapshot() if f['concept'] in keys[:3]]
        row.update(charge_key=value['charge_key'],kind=value['kind'],
            source_fact_ids=[fact['fact_id']]+[f['fact_id'] for f in related],
            evidence=fact['evidence']+[e for f in related for e in f['evidence']])
        output.append(row)
    if get('loan.compound') is True:
        output.append({'kind':'compound','state':'UNKNOWN',
            'reason':'复利需独立明确未付利息本金、适用利率及复利周期；不套用单利公式',
            'source_fact_ids':[f['fact_id'] for f in store.get('loan.compound',consumer=consumer)]})
    result={'source':'VERIFIED_FACTSTORE_DETERMINISTIC','formulas':output,
            'candidate_snapshot_hash':store.snapshot_hash,'no_default_day_basis':True}
    store.record_decision(consumer,'DETERMINISTIC_FORMULAS',result,keys)
    return result
