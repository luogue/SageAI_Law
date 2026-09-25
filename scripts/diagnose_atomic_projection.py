"""Print actual adapter inputs for a production-fixture regression."""
import json
import logging
from backend.test_database_bootstrap import install

install()
from tests.test_entrusted_development_production_closure import report, item
from review_v2 import engine

logging.disable(logging.CRITICAL)
original = engine._set_multi_element_state


def trace(review, elements, evidence):
    original(review, elements, evidence)
    if review.item_id == 'TC-10-02' and any(e['element_id'] == 'priority_license' for e in elements):
        print(json.dumps({'stage': 'adapter',
            'inputs': [e for e in elements if e['element_id'] == 'priority_license'],
            'sources': [{k: e.get(k) for k in ('clause_id', 'evidence_id', 'quote', 'text', 'raw_text')} for e in evidence],
            'outputs': [e for e in review.coverage_elements if e['element_id'] == 'priority_license']}, ensure_ascii=False))


engine._set_multi_element_state = trace
result = report.__wrapped__()
review = item(result, 'TC-10-02')
print(json.dumps({'stage': 'final', 'elements': review['coverage_elements']}, ensure_ascii=False))
