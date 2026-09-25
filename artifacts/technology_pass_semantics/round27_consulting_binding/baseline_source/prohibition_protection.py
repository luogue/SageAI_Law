"""Positive protection requirements; conditional prohibitions are not permissions."""
from review_v2.construction_coverage import element

def requirements(action, label):
    prohibition = rf'(?:不得|禁止|严禁|不允许)[^。；\n]{{0,60}}(?:{action})'
    return [
        element('action_restriction', f'存在{label}限制', prohibition),
        {**element('unconditional_prohibition', f'{label}限制不附同意或批准条件', prohibition),
         'excluded_context_patterns': [r'未经|除非|除.{0,20}外|经.{0,25}(?:同意|批准|许可)']},
    ]
