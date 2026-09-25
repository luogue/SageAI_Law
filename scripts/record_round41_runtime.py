"""Record the bounded live server and the exact source used for acceptance."""
import sys,json,hashlib
from pathlib import Path
from datetime import datetime,timezone
root=Path(__file__).resolve().parents[1]
out=root/'artifacts/technology_pass_semantics/round41_consulting_components'
data={'process_id':int(sys.argv[1]),'logical_cpu_limit':1,'priority':'Idle',
      'recorded_at':datetime.now(timezone.utc).isoformat(),
      'source_hashes':{str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest()
                       for p in (root/'backend/review_v2').glob('*.py')}}
(out/'runtime.json').write_text(json.dumps(data,indent=2),encoding='utf8')
print('Recorded single-CPU server',data['process_id'])





