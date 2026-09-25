from pathlib import Path
import hashlib,json
root=Path(__file__).resolve().parent
manifest=json.loads((root/'manifest.json').read_text(encoding='utf8'))
errors=[name for name,row in manifest.items() if not (root/'files'/name).is_file() or hashlib.sha256((root/'files'/name).read_bytes()).hexdigest()!=row['sha256']]
assert not errors,errors
print(f"FROZEN snapshot verified: {len(manifest)} files")
