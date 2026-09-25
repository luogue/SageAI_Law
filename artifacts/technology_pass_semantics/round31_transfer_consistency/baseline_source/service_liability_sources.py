"""Source facts for a service cap; beneficiary orientation is a separate decision."""
import re
from review_v2.obligation_detail_elements import _segments
from review_v2.technology_service_analysis import analyze_technical_service_core_facts


def elements(clauses):
    facts = analyze_technical_service_core_facts('\n'.join(c.text for c in clauses))['liability']
    party = facts['service_provider_party']
    specs = (
        ('provider_liability_cap', '服务方累计赔偿责任上限', rf'{re.escape(party)}[^。；]{{0,30}}(?:承担的)?(?:全部|累计)?赔偿责任[^。；]{{0,35}}(?:最高不超过|不超过)[^。；]{{0,45}}(?:已经|实际)?支付[^。；]{{0,25}}(?:技术服务费用|服务费用|服务费)'),
        ('broad_loss_exclusion', '服务方排除赔偿的损失项目', rf'(?:利润损失|业务中断|第三方索赔|间接损失).{{0,100}}{re.escape(party)}.{{0,15}}(?:不承担责任|不予赔偿|免责|不负责)|{re.escape(party)}.{{0,20}}不承担.{{0,100}}(?:利润损失|业务中断|第三方索赔|间接损失)'),
        ('high_operational_exposure', '生产系统及数据库实际操作', r'(?:可|应|负责).{0,35}(?:访问|处理|调整|优化).{0,45}(?:生产数据库|参数|SQL|数据)'),
    )
    result = []
    for key,label,pattern in specs:
        rows = [dict(clause_id=c.clause_id, quote=q, location=c.location, actor=party)
                for c,_,q in _segments(clauses) if party and re.search(pattern, re.sub(r'\s+', '',q),re.I)]
        result.append(dict(element_id=key, source_fact_key='service_liability.'+key,
                           required_fact=label, proposition=label, status='COVERED' if rows else 'MISSING',
                           supporting_evidence=rows, search_targets=[label], residual_gap='' if rows else label))
    return result
