"""Strict normalization of values, never keyword extraction or legal inference."""
from datetime import date
from decimal import Decimal, InvalidOperation
import re


def chinese_decimal(value):
    """Validate positional units before using the shared legacy converter.

    Refuse ambiguous strings such as 一二三 and 十百 instead of silently
    keeping the last digit or summing malformed units.
    """
    aliases = str.maketrans('〇两壹贰叁肆伍陆柒捌玖拾佰仟萬億', '零二一二三四五六七八九十百千万亿')
    text = value.translate(aliases)
    digits = '一二三四五六七八九'
    # This first version supports integer financial numerals up to 万 sections.
    # Larger/decimal Chinese forms remain explicitly unsupported, never guessed.
    small = rf'(?:[{digits}]千零?)?(?:[{digits}]百零?)?(?:[{digits}]?十)?[{digits}]?'
    if text == '零':
        return Decimal(0)
    parts = text.split('万')
    if len(parts) > 2 or any(not part for part in parts[:-1]):
        raise ValueError('INVALID_CHINESE_NUMBER')
    for index, part in enumerate(parts):
        if index and part.startswith('零'):
            part = part[1:]
        if part and (not re.fullmatch(small, part) or part.endswith('零')):
            raise ValueError('INVALID_CHINESE_NUMBER')
    from review_v2.fact_number_normalization import number
    return number(text)


def decimal(value):
    if isinstance(value, bool) or not isinstance(value, (str, int, float, Decimal)):
        raise ValueError('EXPECTED_FINITE_NUMBER')
    if isinstance(value, str):
        if not re.fullmatch(r'[+-]?(?:\d+(?:\.\d+)?|\d{1,3}(?:,\d{3})+(?:\.\d+)?)', value):
            # Chinese financial numerals are a defined, auditable input format.
            if not re.fullmatch(r'[零〇一二两三四五六七八九十百千万亿壹贰叁肆伍陆柒捌玖拾佰仟萬億]+', value):
                raise ValueError('INVALID_NUMBER_FORMAT')
            value = chinese_decimal(value)
        else:
            value = value.replace(',', '')
    try:
        result = Decimal(str(value))
    except InvalidOperation as exc:
        raise ValueError('INVALID_NUMBER') from exc
    if not result.is_finite():
        raise ValueError('EXPECTED_FINITE_NUMBER')
    return result


def shape(value, required, optional=()):
    if not isinstance(value, dict) or not set(required) <= value.keys() or not value.keys() <= set(required) | set(optional):
        raise ValueError('INVALID_VALUE_OBJECT_FIELDS')


def string(value):
    if not isinstance(value, str) or not value.strip():
        raise ValueError('EXPECTED_NONEMPTY_STRING')
    if value.strip().upper() in {'ABSENT', 'EXPLICIT_NONE', 'DEFERRED', 'NOT_APPLICABLE', 'UNCERTAIN', 'NULL', 'NONE'}:
        raise ValueError('STATE_IS_NOT_A_VALUE')
    return value


def duration(value):
    # Adapt only explicit magnitude/unit expressions, never infer a term from dates.
    if isinstance(value, str):
        match = re.fullmatch(r'([0-9零〇一二两三四五六七八九十百千万壹贰叁肆伍陆柒捌玖拾佰仟]+(?:\.\d+)?)\s*(个工作日|工作日|个月|月|天|日|年)', value.strip())
        if not match:
            raise ValueError('EXPECTED_EXPLICIT_DURATION')
        value = {'amount': match[1], 'unit': {'个工作日': 'WORKING_DAY', '工作日': 'WORKING_DAY',
            '个月': 'MONTH', '月': 'MONTH', '天': 'DAY', '日': 'DAY', '年': 'YEAR'}[match[2]]}
    shape(value, ('amount', 'unit'))
    if value['unit'] not in {'DAY', 'WORKING_DAY', 'MONTH', 'YEAR'}:
        raise ValueError('INVALID_DURATION_UNIT')
    amount = decimal(value['amount'])
    if amount < 0:
        raise ValueError('NEGATIVE_DURATION')
    return {'amount': amount, 'unit': value['unit']}


def normalize_term(value):
    # A calendar interval is not a measured duration. Preserve both endpoints;
    # no inclusive-day/month convention or missing year is invented.
    if isinstance(value, str):
        token = r'(\d{4})[年-](\d{1,2})[月-](\d{1,2})日?'
        match = re.fullmatch(r'(?:自|从)?' + token + r'\s*(?:至|到)\s*' + token + r'(?:止)?', value.strip())
        if match:
            values = [int(part) for part in match.groups()]
            value = {'start_date': date(*values[:3]).isoformat(), 'end_date': date(*values[3:]).isoformat()}
    if isinstance(value, dict) and ('start_date' in value or 'end_date' in value):
        shape(value, ('start_date', 'end_date'))
        dates = {}
        for key in ('start_date', 'end_date'):
            if not isinstance(value[key], str) or not re.fullmatch(r'\d{4}-\d{2}-\d{2}', value[key]):
                raise ValueError('EXPECTED_ISO_DATE')
            dates[key] = date.fromisoformat(value[key]).isoformat()
        if dates['end_date'] < dates['start_date']:
            raise ValueError('REVERSED_TERM_INTERVAL')
        return dates
    return duration(value)


def accrual_scope(window):
    """Pure projection of source events, not an interest-priority legal rule."""
    shape(window, ('start_event', 'end_event'))
    if window['start_event'] not in {'FUNDING', 'OVERDUE', 'BREACH', 'UNKNOWN'}:
        raise ValueError('INVALID_ACCRUAL_START_EVENT')
    if window['end_event'] not in {'MATURITY', 'PRINCIPAL_REPAID', 'INTEREST_PAID', 'UNKNOWN'}:
        raise ValueError('INVALID_ACCRUAL_END_EVENT')
    if window['start_event'] == 'OVERDUE':
        return 'OVERDUE'
    if window['start_event'] == 'FUNDING' and window['end_event'] == 'PRINCIPAL_REPAID':
        return 'UNTIL_REPAYMENT'
    if window['end_event'] == 'MATURITY' and window['start_event'] in {'FUNDING', 'UNKNOWN'}:
        return 'LOAN_TERM'
    return 'UNKNOWN'


def normalize(spec, value):
    kind = spec.kind
    if value is None:
        raise ValueError('NULL_IS_NOT_A_PRESENT_VALUE')
    if kind == 'string':
        return string(value)
    if kind == 'boolean':
        if type(value) is not bool:
            raise ValueError('EXPECTED_BOOLEAN')
        return value
    if kind == 'enum':
        if type(value) is not str or value not in spec.enum:
            raise ValueError('INVALID_ENUM')
        return value
    if kind == 'number':
        return decimal(value)
    if kind == 'date':
        if not isinstance(value, str) or not re.fullmatch(r'\d{4}-\d{2}-\d{2}', value):
            raise ValueError('EXPECTED_ISO_DATE')
        return date.fromisoformat(value).isoformat()
    if kind == 'money':
        shape(value, ('amount', 'currency'), ('role',))
        if value['currency'] not in {'CNY', 'USD', 'EUR', 'HKD', 'JPY', 'GBP'}:
            raise ValueError('UNSUPPORTED_CURRENCY')
        return {'amount': decimal(value['amount']), 'currency': value['currency'],
                **({'role': string(value['role'])} if 'role' in value else {})}
    if kind == 'duration':
        return duration(value)
    if kind == 'term':
        return normalize_term(value)
    if kind == 'party':
        shape(value, ('name', 'role', 'kind'))
        if value['kind'] not in {'NATURAL', 'ENTERPRISE', 'FINANCIAL', 'GOVERNMENT', 'OTHER_ORGANIZATION'}:
            raise ValueError('INVALID_PARTY_KIND')
        return {**value, 'name': string(value['name']), 'role': string(value['role'])}
    if kind == 'loan_charge':
        if isinstance(value,dict) and 'base_expression' in value and 'base' not in value:
            value={**value,'base':'UNKNOWN'}
        if isinstance(value, dict) and 'accrual_window' in value:
            shape(value, ('kind', 'charge_key', 'base', 'accrual_window', 'rate'), ('scope','base_expression'))
            projected = accrual_scope(value['accrual_window'])
            if 'scope' in value and value['scope'] != projected:
                raise ValueError('SCOPE_CONFLICTS_WITH_EXPLICIT_EVENTS')
            value = {**value, 'scope': projected}
        else:
            # Old normalized observations remain readable; fresh model schema
            # emits source events. This is a shape adapter, never a raw-text path.
            shape(value, ('kind', 'charge_key', 'base', 'scope', 'rate'), ('base_expression',))
        if value.get('base_expression') is not None:
            from review_v2.unified_facts.ontology import principal_basis
            value={**value,'base':principal_basis(value['base_expression'])}
        elif 'base_expression' in value:
            value={**value,'base':'UNKNOWN'}
        if value['kind'] not in {'regular_interest', 'overdue_interest', 'penalty', 'financing_fee'}:
            raise ValueError('INVALID_CHARGE_KIND')
        if value['base'] not in {'PRINCIPAL', 'UNPAID_PRINCIPAL', 'UNPAID_INTEREST', 'UNKNOWN'}:
            raise ValueError('INVALID_CHARGE_BASE')
        if value['scope'] not in {'LOAN_TERM', 'OVERDUE', 'UNTIL_REPAYMENT', 'UNKNOWN'}:
            raise ValueError('INVALID_CHARGE_SCOPE')
        if value['kind'] == 'overdue_interest' and value['scope'] not in {'OVERDUE', 'UNKNOWN'}:
            raise ValueError('OVERDUE_RATE_REQUIRES_OVERDUE_OR_UNKNOWN_SCOPE')
        rate = value['rate']
        if not isinstance(rate, dict):
            raise ValueError('INVALID_CHARGE_RATE')
        state = rate.get('state')
        if state in {'UNKNOWN', 'DEFERRED'}:
            shape(rate, ('state',))
            normalized_rate = dict(rate)
        elif state == 'PRESENT':
            if 'multiplier' in rate:
                shape(rate, ('state', 'multiplier', 'reference'))
                if rate['reference'] != 'REGULAR_RATE':
                    raise ValueError('INVALID_RATE_REFERENCE')
                normalized_rate = {**rate, 'multiplier': decimal(rate['multiplier'])}
            else:
                shape(rate, ('state', 'percent', 'period'))
                if rate['period'] not in {'DAY', 'MONTH', 'YEAR', 'ONCE'}:
                    raise ValueError('INVALID_RATE_PERIOD')
                normalized_rate = {**rate, 'percent': decimal(rate['percent'])}
            if any(v < 0 for v in normalized_rate.values() if isinstance(v, Decimal)):
                raise ValueError('NEGATIVE_CHARGE_RATE')
        else:
            raise ValueError('INVALID_RATE_STATE')
        return {**value, 'charge_key': string(value['charge_key']), 'rate': normalized_rate}
    if kind == 'formula':
        shape(value, ('operator', 'operands'))
        if value['operator'] not in {'MULTIPLY', 'ADD', 'SUBTRACT', 'DIVIDE', 'MIN', 'MAX'}:
            raise ValueError('INVALID_FORMULA_OPERATOR')
        terms = value['operands']
        if not isinstance(terms, list) or len(terms) < 2 or len(terms) > 16:
            raise ValueError('INVALID_FORMULA_OPERANDS')
        normalized = []
        for term in terms:
            if isinstance(term, dict) and set(term) == {'number'}:
                normalized.append({'number': decimal(term['number'])})
            elif isinstance(term, dict) and set(term) == {'reference'}:
                if term['reference'] not in {'PRINCIPAL', 'UNPAID_PRINCIPAL', 'UNPAID_INTEREST', 'RATE', 'DAYS', 'MONTHS', 'YEARS', 'ACTUAL_LOSS', 'CONTRACT_AMOUNT'}:
                    raise ValueError('INVALID_FORMULA_REFERENCE')
                normalized.append(dict(term))
            else:
                raise ValueError('INVALID_FORMULA_TERM')
        return {'operator': value['operator'], 'operands': normalized}
    raise ValueError('UNREGISTERED_VALUE_TYPE:' + kind)


def wire(value):
    """Lossless JSON representation; Decimal never becomes a binary float."""
    if isinstance(value, Decimal):
        return format(value, 'f')
    if isinstance(value, dict):
        return {k: wire(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [wire(v) for v in value]
    return value
