"""Source-bound contribution, control and protection facts shared by evaluators.

Predicates bind transaction, actor and action in an operative sentence. They do
not depend on document names, party names, particular amounts or dates.
"""
import re
from decimal import Decimal
from datetime import date

PARTY = r'[甲乙丙丁戊己庚辛壬癸]方'
CONTROL = r'一票否决权|最终决[定策]|单方决定|自行决定|直接决定|无[须需][^。；]{0,15}(?:股东会|其他股东同意)|由[甲乙丙丁戊己]方(?:决定|审批)'
RESERVED = r'任何表决|重大|借款|担保|资产(?:处置|处分)|投资|关联交易|增资|减资|经营事项'


def protection_polarity(text):
    """Four-way polarity for the exercise of information/inspection rights."""
    if not re.search(r'查阅|查询|查账', text) or not re.search(r'股东|账簿|凭证|财务|流水', text):
        return None
    common = dict(fact_type='information_right', action='inspect_financial_records',
                  beneficiary='shareholders', burdened_party='company')
    approval = re.search(r'(?:经|取得)([^，。；]{1,20})(?:同意|批准|审批)[^。；]{0,12}(?:方可|才能)|须[^。；]{0,15}(?:批准|同意)', text)
    if re.search(r'(?:不得|无权|禁止)[^。；]{0,15}(?:查阅|查询|查账)', text):
        return dict(common, polarity='ADVERSE', restriction='denied', condition='exclusion')
    if approval:
        return dict(common, polarity='RESTRICTIVE', restriction='approval_required', condition=approval.group(), actor=approval.group(1) if approval.lastindex else 'approver')
    if re.search(r'提前[^。；]{0,20}(?:通知|申请)', text):
        return dict(common, polarity='NEUTRAL', restriction='notice_procedure', condition='advance_notice')
    return dict(common, polarity='POSITIVE', restriction='', condition='')


def transaction_facts(text):
    result = []
    natural_parties = set(re.findall('(' + PARTY + r')[^\n：:]{0,15}[：:][^\n]{0,30}身份证', text))
    for match in re.finditer(r'[^。\n]+', text):
        s = match.group()
        base = dict(text=s, start=match.start(), end=match.end())
        if re.search(r'(?:作价|折价|估价|评估)[^。]{0,60}出资', s) or re.search(r'(?:以|用)[^。]{0,100}(?:权益|权利|产权|股权|债权|实物|设备|技术|土地|房屋)[^。]{0,50}出资', s):
            if not re.search(r'仅以现金|全部以货币', s):
                result.append(dict(base, fact_type='nonmonetary_contribution', actor='contributor', action='contribute_valued_property', polarity='AFFIRMED'))
        payment = re.search(r'认购|出资|投资款|认购款|筹备|临时账户', s)
        recipient = re.search(r'(?:汇入|支付至?|付给|转入)[^。；]{0,30}(?:' + PARTY + r'|发起人|股东|个人)[^。；]{0,15}(?:银行|账号|账户)?', s)
        holder = re.search(r'户名[：:]\s*([^；，。\n]+)', s)
        natural_holder = holder and bool(re.fullmatch(r'[\u4e00-\u9fff·]{2,12}', holder[1].strip())) and not re.search(r'公司|企业|银行|合作社', holder[1])
        known_person = recipient and any(p in recipient.group() for p in natural_parties)
        if payment and (natural_holder or known_person or re.search(r'个人[^。；]{0,8}(?:账户|银行)|股东账户|支付给发起人|临时账户', s)):
            result.append(dict(base, fact_type='personal_subscription_account', actor=holder[1] if holder else 'individual_recipient', action='receive_subscription_funds', polarity='AFFIRMED'))
        if re.search(CONTROL, s) and re.search(RESERVED, s) and not re.search(r'不得[^。；]{0,15}(?:自行决定|单方决定|一票否决)', s):
            result.append(dict(base, fact_type='unilateral_reserved_decision', actor='controlling_party', action='decide_reserved_matter', polarity='ADVERSE'))
        if (p := protection_polarity(s)):
            result.append(dict(base, **p))
        if re.search(r'公司(?:依法)?(?:回购|返还)|由公司[^。；]{0,30}(?:回购|返还|退还)', s):
            result.append(dict(base, fact_type='company_capital_return', actor='company', action='return_capital', polarity='AFFIRMED'))
        if re.search(r'(?:由)?' + PARTY + r'[^。；]{0,25}(?:第三方)?回购', s):
            result.append(dict(base, fact_type='shareholder_transfer_exit', actor='shareholder_or_third_party', action='purchase_equity', polarity='AFFIRMED'))
    return result


def evidence(node, clauses):
    rows = [c for c in clauses if c.section_type in {'正式合同条款', '附件'}]
    result = []
    from dataclasses import replace
    sentences = []
    for source in rows:
        for match in re.finditer(r'[^。]+[。]?', source.text):
            c = replace(source, text=match.group().strip())
            sentences.append(c)
    for c in sentences:
        reason = ''
        facts = transaction_facts(c.text)
        if node in {'formation_governance', 'formation_unilateral_control'}:
            controls = [f for f in facts if f['fact_type']=='unilateral_reserved_decision']
            restrictions = [f for f in facts if f['fact_type']=='information_right' and f['polarity'] in {'RESTRICTIVE','ADVERSE'}]
            if controls:
                reason = '单方否决或决定权覆盖重大经营事项，需与共同表决及法定保留事项协调；存在股东会不消除该控制权限制。'
            if restrictions and node == 'formation_governance':
                reason += '股东查账以另一股东同意为前提，属于知情权限制，不能作为充分保障知情权的正向证据。'
        if node == 'formation_profit_loss' and re.search(r'(?:净利润|利润)[^。]{0,40}(?:费用|支配)', c.text) and re.search(r'无[须需]提供[^。]{0,30}(?:凭证|发票)|自行支配', c.text):
            reason = '按利润提取股东费用并允许自行支配或免交支出凭证，存在关联利益输送与费用真实性、资金监督风险。'
        if node in {'common_general_breach','common_penalty_loss'} and re.search(PARTY+r'违反[^。]{0,40}(?:仅|只)', c.text) and re.search(r'直接[^。]{0,40}(?:书面证据|实际[^。]{0,10}损失)',c.text):
            reason = '一方责任被限定为有书面证据的直接实际损失，应与其他方违约金及继续赔偿责任比较，核对责任分配与救济限制。'
        if reason:
            row = dict(c.to_public_dict(), quote=c.text, original_excerpt=c.text, reason=reason, polarity='ADVERSE', semantic_facts=facts)
            if node in {'formation_governance','formation_unilateral_control'} and controls:
                from review_v2.company_governance_facts import risk_atom
                row['adverse_fact_atom'] = risk_atom('unilateral_reserved_decision',c,reason)
            elif node == 'formation_governance' and restrictions:
                row['adverse_fact_atom'] = dict(fact='restricted_information_right',scope='primary_company_governance',
                    actor='controlling_party',object='shareholder_information_right',legal_exposure='inspection_approval_dependency',
                    remedy='restore_independent_information_right',evidence_ids=[c.clause_id],title='股东知情权受单方审批限制',
                    summary=reason,recommendation='区分查阅不同财务材料的法定程序，不以另一股东自行同意作为统一查阅前提，保留法定监督和救济渠道')
            result.append(row)
    return result


def consistency(clauses):
    """Compare a cap-table snapshot and explicitly dependent date ranges."""
    rows = [c for c in clauses if c.section_type in {'正式合同条款','附件'}]
    capital = []
    table = []
    signers = set()
    dates = []
    for c in rows:
        s=c.text
        signers.update(re.findall('('+PARTY+r')[^：:\n]{0,16}[：:][^\n]{1,20}',s))
        if m:=re.search(r'注册资本[^。\n]{0,12}?(\d+(?:\.\d+)?)万元',s):capital.append((Decimal(m[1]),c))
        for m in re.finditer('('+PARTY+r')认缴出资额[^\d]{0,5}(\d+(?:\.\d+)?)万元[^。\n]{0,30}持股比例[^\d]{0,5}(\d+(?:\.\d+)?)[%％]',s):
            table.append((m[1],Decimal(m[2]),Decimal(m[3]),c))
        ds=re.findall(r'(\d{4})年(\d{1,2})月(\d{1,2})日',s)
        if len(ds)>=2 and re.search(r'期限',s):
            try: dates.extend((date(*map(int,ds[j])),date(*map(int,ds[j+1])),c) for j in range(0,len(ds)-1,2))
            except ValueError: pass
    out=[]
    def add(kind,reason,sources):
        out.extend(dict(c.to_public_dict(),quote=c.text,reason=reason,polarity='ADVERSE',fact_type=kind) for c in sources)
    if len(table)>1 and len({r[0] for r in table})==len(table):
        percent=sum(r[2] for r in table)
        amount=sum(r[1] for r in table)
        if percent!=100:add('equity_total',f'同一股权结构持股比例合计为{percent}%，不等于100%。',[r[3] for r in table])
        if capital and amount!=capital[0][0]:add('capital_total',f'各股东认缴合计{amount}万元，与注册资本{capital[0][0]}万元不一致。',[capital[0][1]]+[r[3] for r in table])
        for party,_,_,c in table:
            if party not in signers:add('shareholder_party_mismatch',f'{party}出现在股权结构中，但未识别其签约身份或签署，需补充主体加入及认缴安排。',[c])
    for start,end,c in dates:
        if '合作期限' not in c.text:continue
        if not re.search(r'不得超出|不得超过', '\n'.join(r.text for r in rows)):continue
        for base_start,base_end,base in dates:
            if (base_start,base_end)==(start,end) or '租赁合同' not in base.text:continue
            if end>base_end:add('dependent_term_conflict',f'合作期限终止日{end}超过基础租赁期限终止日{base_end}，与不得超出基础租赁期限的约定冲突。',[c,base])
    return out


def attach_source_assertions(items, clauses):
    """Persist pre-assembly source truth for independent final-state checks."""
    text = '\n'.join(c.text for c in clauses if c.section_type in {'正式合同条款','附件'})
    facts = transaction_facts(text)
    mapping = {'formation_nonmonetary':'nonmonetary_contribution',
               'formation_fund_safety':'personal_subscription_account',
               'formation_unilateral_control':'unilateral_reserved_decision'}
    from review_v2.priority_checklist_helpers import PROFILES
    from review_v2.employment_facts import resolve_requirements
    from review_v2.lease_semantics import corpus_facts
    for item in items:
        if item.node_id in mapping:
            item.decision_trace['source_trigger_facts'] = [f for f in facts if f['fact_type']==mapping[item.node_id]]
        if item.node_id in PROFILES and (item.node_id.startswith('formation_') or item.node_id == 'common_contract_termination'):
            requirements,_ = resolve_requirements(item.node_id,PROFILES[item.node_id],clauses)
            item.decision_trace['source_requirement_facts'] = corpus_facts(clauses,requirements)


def source_consistency_failures(items):
    failures=[]
    for item in items:
        trace=item.decision_trace or {}
        if trace.get('source_trigger_facts') and (item.coverage_status=='不适用' or (item.applicability or {}).get('status')=='NOT_APPLICABLE'):
            failures.append(dict(requirement='SOURCE_FACT_APPLICABILITY_CONFLICT',root_cause=item.item_id, evidence=trace['source_trigger_facts']))
        for audit in trace.get('element_absence_searches',[]):
            if audit.get('result')=='NOT_FOUND' and trace.get('source_requirement_facts',{}).get(audit.get('element_id')):
                failures.append(dict(requirement='SOURCE_FACT_SEARCH_AUDIT_CONFLICT',root_cause=item.item_id,element_id=audit['element_id']))
        for requirement in trace.get('semantic_requirements',[]):
            if requirement.get('polarity_policy')!='PROTECTIVE_RIGHT':continue
            for row in item.evidence_clauses:
                bound=row.get('supports_element_ids') or row.get('supporting_element_ids') or []
                fact=protection_polarity(row.get('text','')) or {}
                if requirement['element_id'] in bound and fact.get('polarity') in {'RESTRICTIVE','ADVERSE','NEUTRAL'}:
                    failures.append(dict(requirement='RESTRICTIVE_EVIDENCE_AS_POSITIVE_COVERAGE',root_cause=item.item_id, evidence_id=row.get('clause_id')))
    return failures
