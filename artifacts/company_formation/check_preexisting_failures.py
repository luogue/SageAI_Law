"""Isolated verification with this task's production changes removed."""
from pathlib import Path
import shutil
import subprocess
import os
root = Path(__file__).resolve().parents[2]
dest = Path(__file__).parent / 'baseline'
shutil.copytree(root / 'backend', dest / 'backend', dirs_exist_ok=True,
    ignore=shutil.ignore_patterns('.env*', '__pycache__', '*.db*', '*.log', 'uploads', '.pytest_cache', 'venv', '.venv'))

def edit(name, pairs):
    path = dest / 'backend' / 'review_v2' / name
    text = path.read_text(encoding='utf-8')
    for a,b in pairs:
        assert a in text, (name,a[:100])
        text=text.replace(a,b)
    path.write_text(text,encoding='utf-8')

edit('engine.py', [
    ("    from review_v2.priority_contract_types import PRIORITY_TYPES\n    if (checkpoint.node_id.startswith('sale_') and contract_type_key in PRIORITY_TYPES\n            and PRIORITY_TYPES[contract_type_key].family == 'EQUITY_INVESTMENT'):\n        return False, '股权出资关系不构成独立货物买卖；未选入独立买卖交易专项。'\n", ''),
    ('    from review_v2.transaction_scope import operative_text, trigger_matches\n    applicability_text = operative_text(applicability_text)\n', ''),
    (' and any(trigger_matches(compacted, keyword))', ''),
    ('        from review_v2.transaction_scope import trigger_matches\n        matched = [term for term in trigger_terms if term and any(trigger_matches(_compact(clause.text), term))]', '        matched = [term for term in trigger_terms if term and term in _compact(clause.text)]'),
    ('    "sale_risk_carrier_delivery": ("运输", "承运人", "物流", "送货", "发运"),\n', ''),
    (' and sale_item.coverage_status != COVERAGE_NOT_APPLICABLE and not has_installment_acceleration(review_text)', ' and not has_installment_acceleration(review_text)'),
    ('checklist if checklist is not None else get_checklist(contract_type_key)', 'get_checklist(contract_type_key)'),
])
edit('domain_selection.py', [
    ("    from review_v2.transaction_scope import operative_text\n    if family == 'SALE':\n        text = operative_text(text)\n", ''),
    ("(operative_text(clause.text) if family == 'SALE' else clause.text)", 'clause.text'),
    (" and not equity_primary", ''),
    ('        from review_v2.contract_registry import get_checklist_for_resolution\n        from types import SimpleNamespace\n        # Validate against the same resolved scenario used by execution.\n        domain = SimpleNamespace(**resolution.document_domain)\n        allowed = {row.item_id for row in get_checklist_for_resolution(resolved.lower(), domain)}',
     '        from review_v2.contract_registry import get_checklist\n        allowed = {row.item_id for row in get_checklist(resolved.lower())}'),
])
edit('domain_resolution.py',[("    from review_v2.transaction_scope import operative_text\n    if target == 'GOODS':\n        text = operative_text(text)\n",'')])
p=dest/'backend/review_v2/priority_contract_types.py'
s=p.read_text(encoding='utf-8'); start=s.index('    from review_v2.transaction_scope import company_formation'); end=s.index('    # A completed employment',start)
s=s[:start]+s[end:];p.write_text(s,encoding='utf-8')
# These failing legacy transactions never select formation. Its additive registry
# branch/modules are unreachable and therefore immaterial to the baseline.
env={**os.environ,'PYTHONIOENCODING':'utf-8','PYTHONPATH':str(dest/'backend')+';'+str(dest/'backend/tests')}
cases=['tests/test_sale_review_checklist.py::test_sale_cement_contract_practical_risk_level_corrections']
cases += [f'tests/test_priority_contract_review.py::test_each_type_end_to_end[{variant}-{kind}]' for variant in ('normal','risky') for kind in ('non_compete','equity_pledge','rights_pledge')]
cases += ['tests/test_priority_contract_review.py::test_specialized_nodes_do_not_change_legacy_checkpoints']
with (Path(__file__).parent/'baseline-failures.log').open('w',encoding='utf-8') as log:
    code=subprocess.call(['python','-m','pytest',*cases,'-q','--tb=short','--disable-warnings'],cwd=dest/'backend',env=env,stdout=log,stderr=subprocess.STDOUT)
print('baseline exit:',code)
