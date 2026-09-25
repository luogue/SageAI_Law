"""Separate a service allowance from an express price-inclusion agreement."""
import re
from review_v2.obligation_detail_elements import _segments

_SERVICE_FEE = r'(?:技术)?(?:服务|支持|指导|培训)(?:(?:和|及|与|、)(?:技术)?(?:服务|支持|指导|培训))*(?:费|费用)'
_MONEY = r'(?:人民币)?\d[\d,.]*元'


def elements(clauses):
    spans = [(c, q, re.sub(r'\s+', '', q)) for c, _, q in _segments(clauses)]
    def rows(pattern):
        return [dict(clause_id=c.clause_id, quote=q, location=c.location)
                for c, q, text in spans if re.search(pattern, text)]
    explicit = rows(rf'{_SERVICE_FEE}.{{0,30}}(?:包含|不另行|{_MONEY})|(?:转让费|许可费|合同总价).{{0,20}}包含.{{0,20}}(?:服务|培训)|(?:技术服务|技术支持).{{0,20}}不另行收费')
    allowance = rows(r'(?:现场)?技术服务.{0,24}(?:不超过|限于|累计不超过)\d+(?:个)?(?:工作日|日|天|小时|次)')
    extra = rows(r'(?:超过|超出).{0,36}(?:服务|工作量|工时).{0,24}(?:另行协商收费|另行收费|另行计费|协商计费)')
    included = rows(rf'{_SERVICE_FEE}.{{0,25}}包含.{{0,15}}(?:转让费|许可费|(?:转让|合同)?价款|总价)|(?:转让费|许可费|合同总价).{{0,20}}包含.{{0,20}}(?:服务|培训)')
    # A component introduced by "其中" refers to the preceding total in the
    # same operative price provision, not to every price anywhere in a theme.
    components = [(c, q) for c, q, t in spans if re.search(rf'其中{_SERVICE_FEE}[：:]?{_MONEY}', t)]
    for clause, quote in components:
        totals = [dict(clause_id=c.clause_id, quote=q, location=c.location)
                  for c, q, t in spans if c.clause_id == clause.clause_id
                  and clause.text.index(q) < clause.text.index(quote)
                  and re.search(rf'(?:使用费总额|许可费总额|转让费总额|合同总价|合同总额)[：:]?{_MONEY}', t)]
        if len(totals) == 1:
            included += totals + [dict(clause_id=clause.clause_id, quote=quote, location=clause.location,
                                      domain_context_evidence=[{**totals[0], 'evidence_role': 'PRICE_COMPONENT_TOTAL'}])]
    schedule = rows(r'(?:技术服务费|额外服务费).{0,35}(?:支付|结算).{0,25}(?:日内|完成后|按月|确认后)|(?:日内|完成后|按月|确认后).{0,20}支付.{0,15}技术服务费')
    if included:
        # Keep each payment node as an independent source; inclusion supplies
        # the explicit link from service component to total-price instalments.
        payments = rows(r'(?:分期支付|第一期|第二期|第三期).{0,80}(?:支付|元)|(?:日内|完成后).{0,20}支付(?:合同总额|剩余).{0,12}%')
        if payments:
            schedule += included + payments
    specs = [
        ('service_fee_amount', '约定工作量范围内的技术服务费用', explicit or (allowance + extra if allowance and extra else []), 'PARTIALLY_COVERED' if not explicit and allowance and extra else 'COVERED', '约定工作量内费用是否另收或包含于主价款'),
        ('service_payment_schedule', '技术服务费用的支付安排', schedule, 'COVERED', '技术服务费用与主价款付款安排的对应关系'),
        ('extra_service_pricing_standard', '额外技术服务收费标准', rows(r'(?:超出|超过|额外).{0,80}(?:每人日|每小时|单价|费率)[：:]?\d'), 'COVERED', '额外技术服务收费标准'),
        ('extra_service_billing_method', '额外服务计价和工作量确认', rows(r'工时确认单|工作量确认|按实际工时|按人日|按小时'), 'COVERED', '额外服务计价和工作量确认'),
        ('extra_service_payment_node', '额外服务付款节点', rows(r'(?:额外|超出|超过).{0,60}(?:支付|付款|结算).{0,30}(?:日内|完成后|确认后|按月|按季)'), 'COVERED', '额外服务付款节点'),
    ]
    return [dict(element_id=k, source_fact_key='ancillary_fee.'+k, required_fact=label,
                 proposition=label, search_targets=[gap], status=status if evidence else 'MISSING',
                 supporting_evidence=evidence, residual_gap=gap if not evidence or status=='PARTIALLY_COVERED' else '')
            for k,label,evidence,status,gap in specs if not k.startswith('extra_') or extra]
