"""Evidence-based screening, not automatic judicial proportionality findings."""
import re
from review_v2.noncompete_semantics import temporal_roles

GUIDANCE = '《企业实施竞业限制合规指引》：超过1年月补偿一般不宜低于离职前12个月平均工资50%；属于合规审查基准，不自动认定无效。'
EXIT_LAW = '《劳动争议司法解释（一）》第39条：竞业履行期间单位请求解除，劳动者请求额外支付三个月竞业经济补偿的，人民法院应予支持。'


def number(raw):
    if raw.isdigit():
        return float(raw)
    digits = dict(zip('零一二三四五六七八九', range(10)))
    if raw == '两':
        return 2
    if '十' in raw:
        a, b = raw.split('十', 1)
        return digits.get(a, 1) * 10 + digits.get(b, 0)
    return digits.get(raw)


def assess(clauses):
    rows = []
    for clause in clauses:
        if clause.section_type not in {'正式合同条款', '附件'}:
            continue
        for m in re.finditer(r'[^。；\n]+', clause.text):
            rows.append(dict(clause_id=clause.clause_id, location=clause.location,
                text=m.group(), quote=m.group(), source_start=m.start(), source_end=m.end(), source_type='CONTRACT_TEXT'))
    def find(pattern):
        return [r for r in rows if re.search(pattern, r['text'])]
    checks = []
    def add(key, message, evidence, **facts):
        checks.append(dict(key=key, status='REVIEW_REQUIRED', message=message, evidence=evidence, **facts))
    broad = find(r'竞业.{0,40}(?:地域|地区|区域).{0,25}(?:全国|全球|全世界|世界各地|所有国家)')
    if broad:
        global_scope = any(re.search(r'全球|全世界|世界各地|所有国家', r['text']) for r in broad)
        geography = r'(?:全球|世界各地|各国)' if global_scope else r'(?:全国|各省|全球)'
        business = find(r'(?:甲方|公司|用人单位).{0,30}(?:实际经营|业务覆盖|经营地域|业务遍及|经营覆盖).{0,12}' + geography)
        secrets = find(r'(?:乙方|劳动者).{0,20}(?:实际接触|掌握|知悉).{0,25}' + geography + r'.{0,25}(?:商业秘密|核心秘密)')
        reason = find(r'(?:由于|基于|鉴于).{0,65}(?:秘密|业务).{0,50}(?:全国|全球).{0,20}(?:必要|保护|限制)')
        add('broad_geography', '竞业地域约定较宽（' + ('全球' if global_scope else '全国') + '范围）；'
            + ('已有相应经营地域及秘密接触陈述，仍需核验真实性、必要性和岗位关联。' if business and secrets else
               '缺少相应实际经营地域或秘密接触范围的支持事实，需结合劳动者岗位核验必要性和合理性。'),
            broad + business + secrets + reason, supporting_business=bool(business), supporting_secrets=bool(secrets), justification=bool(reason))
    durations = []
    for r in temporal_roles(clauses):
        if r['role'] != 'NONCOMPETE_DURATION':
            continue
        m = re.fullmatch(r'([一二两三四五六七八九十\d]+)\s*个?\s*(月|年|日|天)', r['expression'])
        value = number(m[1]) if m else None
        if value is not None:
            durations.append((value * (12 if m[2]=='年' else 1 if m[2]=='月' else 1/30), r))
    compensation = find(r'(?:补偿|补助).{0,120}(?:平均工资|月工资).{0,20}\d+(?:\.\d+)?\s*[%％]')
    ratios = []
    for row in compensation:
        m = re.search(r'(?:平均工资|月工资).{0,20}?(\d+(?:\.\d+)?)\s*[%％]', row['text'])
        if m:
            ratios.append((float(m[1]), row))
    months = max((v for v, _ in durations), default=None)
    ratio = min((v for v, _ in ratios), default=None)
    if ratio is not None and ((months is not None and months>12 and ratio<50) or ratio<30):
        add('duration_compensation', f'竞业期限为{months:g}个月，月补偿比例为{ratio:g}%；需核验补偿水平是否与期限及限制强度匹配。' if months is not None else
            f'月补偿比例为{ratio:g}%，需核验补偿水平与限制强度及当地适用标准。',
            [r for _, r in durations] + [r for _, r in ratios], duration_months=months, compensation_percent=ratio, legal_basis=GUIDANCE)
    # An absolute amount alone does not establish a wage ratio or a local minimum.
    if not ratios and find(r'(?:每月|按月).{0,25}(?:补偿|补助).{0,20}\d+元'):
        add('compensation_baseline', '已有补偿金额，但缺少可核对的工资比例或当地标准，需核验金额合理性。',
            find(r'(?:每月|按月).{0,25}(?:补偿|补助).{0,20}\d+元'))
    termination = find(r'(?:甲方|用人单位).{0,100}(?:提前|单方).{0,60}(?:解除|终止)(?:本协议|竞业限制|协议)')
    termination = [r for r in termination if not re.search(r'不得|无权|协商一致|(?:乙方|劳动者)(?:有权|可|可以).{0,12}(?:解除|终止)', r['text'])]
    extra = find(r'(?:解除|终止).{0,60}(?:额外|另行).{0,15}(?:三|3)个月.{0,20}(?:补偿|补助)')
    if termination and not extra:
        add('early_termination_compensation', '协议允许单位提前解除，但未明确额外补偿责任。须区分已履行期间正常补偿、解除后的未来普通补偿与额外补偿；履行期间单位解除时应核对劳动者请求额外三个月补偿的权利，通知期不能替代该责任。',
            termination, legal_basis=EXIT_LAW, nature='LEGAL_NOTICE_NOT_AUTOMATIC_ILLEGALITY')
    return dict(checks=checks, duration_months=months, compensation_percent=ratio,
                early_termination_evidence=termination, extra_compensation_evidence=extra)
