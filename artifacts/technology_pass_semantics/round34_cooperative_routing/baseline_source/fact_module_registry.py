"""Contract-family registration, with no default family or all-domain schema."""
from dataclasses import dataclass
from typing import Callable


class UnknownFactFamily(ValueError):
    pass


@dataclass(frozen=True)
class FactFamily:
    name: str
    contract_types: tuple[str, ...]
    selector: Callable
    pipeline: str
    migration_status: str


class FactModuleRegistry:
    def __init__(self):
        self._families = {}

    def register(self, family):
        if not family.contract_types or any(key in self._families for key in family.contract_types):
            raise ValueError('DUPLICATE_OR_EMPTY_FACT_FAMILY')
        for key in family.contract_types:
            self._families[key] = family

    def family(self, contract_type):
        try:
            return self._families[contract_type]
        except KeyError:
            raise UnknownFactFamily(f'UNREGISTERED_FACT_FAMILY:{contract_type}') from None

    def select(self, contract_type, concepts, roots):
        keys = tuple(self.family(contract_type).selector(concepts, roots, contract_type))
        if len(keys) != len(set(keys)) or not set(keys) <= set(concepts):
            raise ValueError('INVALID_ACTIVE_CONCEPT_SCOPE')
        return keys


REGISTRY = FactModuleRegistry()


def _employment_selector(concepts, roots, agreement):
    from review_v2.fact_dependencies import ROOTS, eligible
    prefixes = {
        'confidentiality': ('nda.', 'identity.', 'penalties.', 'worker.', 'ip.', 'non_compete.'),
        'non_compete': ('identity.', 'penalties.', 'worker.', 'non_compete.'),
        'employment_termination': ('identity.','penalties.','worker.','non_compete.','termination.','economic_compensation.','exit_settlement.','salary.','social_insurance.','dispute.'),
    }
    if agreement == 'labor':
        keys = [key for key in concepts if not key.startswith(('nda.','exit_settlement.'))]
    else:
        keys = [key for key in concepts if key.startswith(prefixes[agreement]) or key in ROOTS]
    forms = {f.get('normalized_value', f.get('value')) for f in roots
             if f['concept'] == 'contract.employment_form'}
    keys = [key for key in keys if not key.startswith('part_time.') or 'PART_TIME' in forms]
    if 'DISPATCH' in forms:
        keys += [key for key in concepts if key.startswith('dispatch.')]
    # Legacy personnel remains readable for stored fixtures, not re-extracted
    # alongside the independent scope/eligibility concepts.
    keys = [key for key in keys if key != 'non_compete.personnel']
    return dict.fromkeys(eligible(keys, roots))


REGISTRY.register(FactFamily('employment', ('labor', 'non_compete', 'confidentiality', 'employment_termination'),
    _employment_selector, 'employment_fact_pipeline', 'ACTIVE'))


def _loan_selector(concepts, roots, agreement):
    from review_v2.unified_facts.loan import schema
    return schema().select(roots)


REGISTRY.register(FactFamily('credit', ('loan',), _loan_selector,
    'unified_facts.loan_pipeline', 'ACTIVE'))
