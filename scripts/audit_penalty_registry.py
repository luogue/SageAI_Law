"""Audit canonical penalty references in a serialized production response."""
import json
import sys
from pathlib import Path
from types import SimpleNamespace
from review_v2.contract_facts import ContractFact, ContractFactGraph
from review_v2.penalty_fact_binding import gate

path = Path(sys.argv[1])
report = json.loads(path.read_text(encoding='utf-8'))
registry = report['contract_facts']
graph = ContractFactGraph(facts={key: [ContractFact(**row) for row in rows]
                                 for key, rows in registry['facts'].items()})
items = [SimpleNamespace(**row) for row in report['items']]
findings = [SimpleNamespace(**row) for row in report['risk_findings']]
result = gate(items, findings, graph)
result['consumers'] = [{
    'rule_id': item.item_id, 'element_key': element['element_id'],
    'status': element['status'], 'fact_ids': element.get('canonical_fact_keys')
} for item in items for element in item.coverage_elements if element.get('canonical_fact_keys')]
result['release_quality_gate'] = report['release_quality_gate']['status']
path.with_name('canonical_penalty_audit.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps(result, ensure_ascii=False, indent=2))
