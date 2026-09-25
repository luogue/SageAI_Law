"""Explicit modules and parent-dependent concept selection."""
from dataclasses import dataclass
from types import MappingProxyType


# One semantic contract is sent to BOTH extractor and verifier. These describe
# literal contractual facts, not legal priority or enforceability decisions.
CHARGE_SCOPE = {
    'LOAN_TERM': '原文明确限定正常借期内或明确终止于到期日。',
    'OVERDUE': '原文起点为逾期/到期未偿，终点可为实际清偿。',
    'UNTIL_REPAYMENT': '原文起点为实际放款/到账，终点为相应本金实际归还，未在该安排中限定到期日。',
    'UNKNOWN': '原文未明确足够的起止信息，不能仅从收费名称或另有逾期条款推定。',
}
CHARGE_SCOPE_POLICY = (
    'scope描述该收费条款明示的起止边界。另有逾期利率不等于明示停止普通利息；'
    '是否替代、叠加或择一是独立关系事实，不得用法律常识推断来改写scope。'
    '明确相互矛盾的安排分别保留；同一事实的同义表述不是遗漏。'
    '已有起点和终点且覆盖对应原文时，不得再以推断的优先适用关系报告计息范围遗漏。'
)
CHARGE_BASE = {
    'PRINCIPAL': '明确以原始全部借款金额/借款总额为基数。',
    'UNPAID_PRINCIPAL': '尚未清偿的本金余额，含正常本金余额、实际占用未还本金、逾期本金；余额不是最初总额。',
    'UNPAID_INTEREST': '应付未付利息金额。',
    'UNKNOWN': '没有明确基数。仅说执行利率加成/倍数不能证明本金基数，利率基准不等于计费基数。',
}


@dataclass(frozen=True)
class Concept:
    key: str
    kind: str
    description: str
    enum: tuple[str, ...] = ()
    multiple: bool = False

    def public(self):
        result = {'kind': self.kind, 'description': self.description, 'multiple': self.multiple,
                **({'enum': list(self.enum)} if self.enum else {})}
        if self.kind in {'boolean', 'string', 'enum'}:
            result['value_schema'] = {'type': 'boolean' if self.kind == 'boolean' else 'string',
                                     **({'enum': list(self.enum)} if self.enum else {})}
        def obj(properties):
            return {'type': 'object', 'properties': properties, 'required': list(properties), 'additionalProperties': False}
        def enum(*values):
            return {'type': 'string', 'enum': list(values)}
        number = {'oneOf': [{'type': 'number'}, {'type': 'string', 'description': '精确十进制数值，无单位或状态占位'}]}
        iso_date = {'type': 'string', 'format': 'date', 'description': '明确的完整YYYY-MM-DD日期'}
        if self.kind == 'number':
            result['value_schema'] = number
        if self.kind == 'date':
            result['value_schema'] = iso_date
        if self.kind in {'duration', 'term'}:
            magnitude = obj({'amount': number, 'unit': enum('DAY', 'WORKING_DAY', 'MONTH', 'YEAR')})
            result['value_schema'] = magnitude if self.kind == 'duration' else {'oneOf': [magnitude,
                obj({'start_date': iso_date, 'end_date': iso_date})]}
            result['verification_policy'] = ('明确长度与日期区间都是期限事实，但不得由日期差推定一年、几个月或天数。'
                'term仅有日期区间时直接保存端点；duration仅接受原文明确的数值单位，不把可计算视为原文明示。')
        if self.kind == 'loan_charge':
            def obj(properties):
                return {'type': 'object', 'properties': properties, 'required': list(properties), 'additionalProperties': False}
            def enum(*values):
                return {'type': 'string', 'enum': list(values)}
            number = {'oneOf': [{'type': 'number'}, {'type': 'string', 'description': '精确十进制数值，无单位或状态占位'}]}
            result['value_schema'] = obj({
                'kind': enum('regular_interest', 'overdue_interest', 'penalty', 'financing_fee'),
                'charge_key': {'type': 'string'},
                'base_expression': {'type':['string','null'], 'description':'原文直接指明本收费基数的逐字连续短语，未明说填null。代码据此归一base，不由模型输出base枚举。'},
                'accrual_window': obj({
                    'start_event': enum('FUNDING', 'OVERDUE', 'BREACH', 'UNKNOWN'),
                    'end_event': enum('MATURITY', 'PRINCIPAL_REPAID', 'INTEREST_PAID', 'UNKNOWN')}),
                'rate': {'oneOf': [obj({'state': enum('PRESENT'), 'percent': number,
                    'period': enum('DAY', 'MONTH', 'YEAR', 'ONCE')}),
                    obj({'state': enum('PRESENT'), 'multiplier': number, 'reference': enum('REGULAR_RATE')}),
                    obj({'state': enum('UNKNOWN', 'DEFERRED')})]},
            })
            result['value_schema']['properties']['accrual_window']['description'] = (
                '仅提取本收费条款明示起止事件：FUNDING=资金实际放款/到账；OVERDUE=到期未付起；BREACH=其他违约起；'
                'MATURITY=明确到期日停止；PRINCIPAL_REPAID=相应本金实际归还；INTEREST_PAID=欠息实际支付。'
                '未明说的边界用UNKNOWN；不得仅因另有逾期条款就填MATURITY。scope由代码投影，不由模型输出。')
            result['base_definitions'] = CHARGE_BASE
            result['scope_definitions'] = CHARGE_SCOPE
            result['verification_policy'] = CHARGE_SCOPE_POLICY + '核验直接事实accrual_window的原文起止事件；scope是代码确定性投影。基数按base_definitions逐项核验，不推定。'
        if self.multiple:
            result['collection_protocol'] = (
                'value_schema描述一个成员。推荐每个成员一条observation，分别附证据；'
                '也可PRESENT value=[成员,...]并附覆盖所有成员的证据。成员各自独立核验。'
                '无成员须明确ABSENT/EXPLICIT_NONE/UNKNOWN等状态，不可PRESENT空集合。'
                '状态记录不携带value；ABSENT空数组可兼容，但仍须通过全文无遗漏核验。')
        return result


@dataclass(frozen=True)
class Module:
    name: str
    concepts: tuple[Concept, ...]
    # All parent facts must be explicitly verified PRESENT with this value.
    requires: tuple[tuple[str, object], ...] = ()


class Schema:
    version = 'contract-facts-1.0'

    def __init__(self, family, root_modules, modules):
        self.family = family
        self.root_modules = tuple(root_modules)
        self.modules = tuple(modules)
        all_modules = self.root_modules + self.modules
        keys = [c.key for m in all_modules for c in m.concepts]
        if len(keys) != len(set(keys)):
            raise ValueError('DUPLICATE_FACT_CONCEPT')
        self.concepts = MappingProxyType({c.key: c for m in all_modules for c in m.concepts})
        roots = set(self.root_keys)
        if any(key not in roots for m in self.modules for key, _ in m.requires):
            raise ValueError('MODULE_PARENT_MUST_BE_A_ROOT_FACT')

    @property
    def root_keys(self):
        return tuple(c.key for m in self.root_modules for c in m.concepts)

    def active_modules(self, roots):
        def present(key, value):
            rows = [f for f in roots if f['concept'] == key]
            return bool(rows) and all(f.get('state') == 'PRESENT'
                and f.get('verified') is True and f.get('assertion') == 'EXPLICIT'
                and f.get('confidence', 0) >= .75 and f.get('normalized_value') == value
                for f in rows)
        return self.root_modules + tuple(m for m in self.modules
            if all(present(key, value) for key, value in m.requires))

    def select(self, roots):
        return tuple(c.key for m in self.active_modules(roots) for c in m.concepts)

    def public(self, active):
        if not set(active) <= set(self.concepts):
            raise ValueError('UNKNOWN_ACTIVE_CONCEPT')
        return {key: self.concepts[key].public() for key in active}


COMMON = Module('common', (
    Concept('common.parties', 'party', '合同主体名称、角色及主体性质，分别提取各主体，不猜测身份。', multiple=True),
    Concept('common.signing_date', 'date', '实际填写的合同签署日期，不能用其他日期代替。'),
    Concept('common.effective_date', 'date', '明确的生效日期；生效条件另存，不计算或补日期。'),
    Concept('common.effective_condition', 'string', '合同生效条件的具体约定。'),
    Concept('common.term', 'term', '合同期限：明确长度用amount/unit；仅明确起止日期用start_date/end_date。不得由日期差推算长度或补足不明年份。'),
    Concept('common.amounts', 'money', '合同金额；须保留币种和语义角色，不能把不同用途金额合并。', multiple=True),
    Concept('common.liability', 'string', '当前合同责任分配、责任触发条件和责任承担方式。', multiple=True),
    Concept('common.dispute_method', 'enum', '约定的争议解决方式。', ('LITIGATION', 'ARBITRATION', 'NEGOTIATION', 'MEDIATION'), multiple=True),
    Concept('common.dispute_institution', 'string', '约定的法院、仲裁机构或可确定的管辖连接点。'),
))
