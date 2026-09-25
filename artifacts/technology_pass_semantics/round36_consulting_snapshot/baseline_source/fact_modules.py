"""Request-local schema selection; excluded modules are not absence claims."""
from contextvars import ContextVar
from review_v2.fact_module_registry import REGISTRY
AGREEMENT = ContextVar('fact_agreement', default=None)

def select(concepts, roots, agreement):
 return list(REGISTRY.select(agreement, concepts, roots))
