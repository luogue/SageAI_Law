import json
from pathlib import Path
for name in ('local_client.json','local_provider.json'):
 r=json.loads((Path('artifacts/technology_pass_semantics/round27_consulting_binding')/name).read_text(encoding='utf8'))
 print(name,json.dumps(r['release_quality_gate']['failures'],ensure_ascii=False,indent=2))
