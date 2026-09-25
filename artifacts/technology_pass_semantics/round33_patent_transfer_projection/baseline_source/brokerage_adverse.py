"""Independent adverse-content assessment; screening thresholds are not legal caps."""
from copy import deepcopy
import re

from review_v2.lease_semantics import corpus_facts, requirement, evidence_identity


def number(raw):
    raw = raw.replace(',', '').replace('，', '')
    try:
        return float(raw)
    except ValueError:
        digits = dict(zip('零一二三四五六七八九', range(10)))
        if raw == '两':
            return 2
        if '十' in raw:
            a, b = raw.split('十', 1)
            return digits.get(a, 1) * 10 + digits.get(b, 0)
        return digits.get(raw, 0)


N = r'[\d.,，一二两三四五六七八九十]+'


def daily_rate(text):
    if not re.search(r'(?:每日|日息|按日).{0,65}违约金', text):
        return None
    m = re.search(r'(?:千分之|万分之|百分之)(' + N + ')|(' + N + r')(‰|%|‱)', text)
    if not m:
        return None
    divisor = (1000 if m[0].startswith('千分之') else 10000 if m[0].startswith('万分之') else 100) if m[1] else {'‰': 1000, '%': 100, '‱': 10000}[m[3]]
    return number(m[1] or m[2]) / divisor


def money_amount(text):
    m = re.search(r'(?:人民币)?\s*(' + N + r')\s*(万)?元', text)
    if not m:
        return None
    value = number(m[1])
    return value * 10000 if m[2] else value


def percent_value(text):
    m = re.search(r'(' + N + r')\s*%', text)
    if m:
        return number(m[1]) / 100
    m = re.search(r'百分之(' + N + r')', text)
    if m:
        return number(m[1]) / 100
    return None


def remuneration_rate(text):
    candidates = []
    for pattern in (
        r'(' + N + r')\s*%.{0,25}(?:支付|作为|计为).{0,12}(?:中介报酬|佣金|服务费用)',
        r'(?:按照|按).{0,45}(' + N + r')\s*%.{0,35}(?:中介报酬|佣金|服务费用)',
        r'(?:中介报酬|佣金|服务费用).{0,30}(?:按|按照|费率|比例).{0,20}(' + N + r')\s*%',
    ):
        for match in re.finditer(pattern, text):
            value = number(match[1]) / 100
            if 0 < value <= 0.3:
                candidates.append(value)
    return candidates[0] if candidates else None


def scan(clauses):
    findings = []
    full_text = '\n'.join(str(getattr(c, 'text', '') or '') for c in clauses)
    remuneration_ratio = None
    remuneration_ratio = remuneration_rate(full_text)
    patterns = {
        'daily_penalty': r'(?:逾期|延迟).{0,100}(?:每日|按日).{0,70}违约金',
        'cumulative_bypass': r'(?:绕开|绕过|跳单).{0,100}(?:除|除应).{0,30}(?:全部|全额).{0,15}报酬.{0,35}(?:还应|另行|再).{0,70}违约金',
        'exclusive_fixed_penalty': r'违反.{0,35}独家.{0,100}(?:人民币|支付).{0,25}元违约金',
        'tail_period': r'(?:提供|介绍).{0,45}(?:之日起|后)\s*' + N + r'个?月内.{0,160}(?:报酬|佣金)',
        'extended_affiliates': r'(?:关联公司|关联企业).{0,60}任何形式商业合作.{0,70}(?:报酬|佣金)',
        'unapproved_expenses': r'(?:单笔|每笔).{0,35}(?:费用|支出).{0,40}(?:无需|不必|无须).{0,25}(?:书面同意|书面批准)',
    }
    ownership = {
        'daily_penalty': ('principal_pay_remuneration', '逾期报酬违约金负担', '建议结合可证明损失、宽限期和累计上限调整日违约金；筛查结果不等于司法调减结论。'),
        'cumulative_bypass': ('bypass_remuneration_liability', '跳单报酬与违约金叠加', '建议区分应付报酬与损失赔偿，约定违约金与报酬的关系及合理累计责任上限。'),
        'exclusive_fixed_penalty': ('exclusive_bypass_consequence', '独家委托定额违约责任', '建议结合剩余独家期限、实际服务投入及损失确定违约责任，避免不区分违约程度的固定负担。'),
        'tail_period': ('post_contract_obligation', '尾随报酬的期限与因果边界', '建议限定尾随期限、已确认客户名单及成交与中介服务的实质因果关系。'),
        'extended_affiliates': ('post_contract_obligation', '尾随报酬的期限与因果边界', '建议限定关联主体、交易类型及实际使用中介信息的证明条件，避免所有商业合作均计酬。'),
        'unapproved_expenses': ('expense_scope_and_cap', '无需事先批准的费用负担', '建议明确累计费用预算、必要性证明及超预算书面审批，防止拆分支出绕过审批。'),
    }
    for kind, pattern in patterns.items():
        spec = requirement('broker_adverse_' + kind, ownership[kind][1], pattern)
        rows = corpus_facts(clauses, [spec])[spec['element_id']]
        for row in rows:
            text = row['text']
            # Prohibitions of the adverse arrangement are not affirmative risks.
            if re.search(r'(?:不得|禁止|不允许).{0,12}(?:按每日|另行|无需|无须)', text):
                continue
            assessment = {'basis': '合同经济负担及责任边界筛查，不作为法定上限或当然无效判断'}
            level = '中'
            if kind == 'daily_penalty':
                rate = daily_rate(text)
                if rate is None or rate * 365 <= 1:
                    continue
                assessment.update(daily_rate=rate, simple_annualized_rate=round(rate * 365, 6), screening_threshold='一年简单累计超过计费基数')
                level = '高'
            if kind == 'cumulative_bypass':
                assessment.update(penalty_ratio_to_remuneration=percent_value(text), cumulative_with_remuneration=True)
                level = '高'
            if kind == 'exclusive_fixed_penalty':
                assessment.update(fixed_amount=money_amount(text))
            if kind == 'tail_period':
                m = re.search('(' + N + ')个?月内', text)
                if not m or number(m[1]) <= 12:
                    continue
                assessment.update(months=number(m[1]), screening_threshold='跨年度尾随报酬需核验因果及期限边界')
                rate = percent_value(text)
                assessment.update(remuneration_ratio=rate if rate is not None else remuneration_ratio)
            if kind == 'extended_affiliates':
                rate = percent_value(text)
                assessment.update(remuneration_ratio=rate if rate is not None else remuneration_ratio)
            if kind == 'unapproved_expenses':
                assessment.update(no_preapproval_single_expense_threshold=money_amount(text))
            node, title, suggestion = ownership[kind]
            findings.append({'kind': kind, 'node_id': node, 'title': title, 'level': level,
                             'assessment': assessment, 'recommendation': suggestion,
                             'requirement': spec, 'evidence': evidence_identity(row)})
    return {'status': 'COMPLETE', 'method': 'INDEPENDENT_CONTENT_PREDICATES_AND_NUMERIC_ASSESSMENT',
            'searched_clause_ids': [c.clause_id for c in clauses], 'findings': findings}


def bind(item, scan_result):
    hits = [f for f in scan_result['findings'] if f['node_id'] == item.node_id]
    if not hits:
        return
    item.coverage_status = item.status = item.issue_type = '风险条款'
    item.coverage_presence = 'PRESENT'
    item.risk_status = 'ADVERSE'
    item.risk_level = '高' if any(f['level'] == '高' for f in hits) else '中'
    item.economic_impact = 'high' if item.risk_level == '高' else 'medium'
    item.economic_impact_detail = {
        'level': item.economic_impact,
        'assessment_source': 'BROKERAGE_ADVERSE_CLAUSE_SCAN',
        'basis': '合同条款载明明确金额、比例、日费率、期限或计费范围，实际损失另需结合履行事实确认。',
        'exposures': [deepcopy(f['assessment']) for f in hits],
    }
    item.risk_group = 'broker_' + hits[0]['kind']
    item.risk_point_description = item.reasoning_summary = '；'.join(dict.fromkeys(f['title'] + '：' + f['recommendation'] for f in hits))
    item.legal_consequence_if_missing = '已有条款形成实际经济负担或过宽责任范围，应结合损失和交易因果关系核验并调整。'
    item.suggested_clause_example = '；'.join(dict.fromkeys(f['recommendation'] for f in hits))
    item.action_suggestion = item.suggested_clause_example
    item.evidence_clauses = list({f['evidence']['evidence_id']: deepcopy(f['evidence']) for f in hits}.values())
    item.evidence_location = '；'.join(dict.fromkeys(e['location'] for e in item.evidence_clauses))
    item.decision_trace.update(semantic_requirements=[deepcopy(f['requirement']) for f in hits],
        review_mode='ABSENCE_REQUIRED', review_polarity='NEGATIVE_CLAUSE_CHECK',
        review_nature='CONTRACTUAL_REQUIREMENT',
        negative_check_basis={'method': scan_result['method'], 'finding_kinds': [f['kind'] for f in hits]},
        finding_parent_group=item.risk_group,
        underlying_risk_identity={'fact': item.risk_group, 'scope': 'primary_contract', 'remedy': 'adjust_' + item.risk_group})
    for row in item.evidence_clauses:
        row.update(entailment_status='SUPPORTS', evidence_semantics='ACTUAL_RISK_CLAUSE', affirmative_risk_evidence=True)
