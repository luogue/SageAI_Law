"""Upload only verified code fixes to the isolated build context and rerun Docker."""
import json,hashlib
from pathlib import Path
from production_probe import ROOT,OUT,connect,remote_python
REMOTE='/var/tmp/sageai-release-verify-20260909'
c=connect();s=c.open_sftp()
with s.open(REMOTE+'/build-result.json') as f:previous=json.loads(f.read())
assert previous['status']!='RUNNING'
for n in ['build-result.json','build-backend.log','build-frontend.log']:
    s.get(REMOTE+'/'+n,str(OUT/('initial-'+n)))
for name in ['backend/main.py','Dockerfile.frontend','.dockerignore','docker-compose.yml','backend/tests/test_download_headers.py']:
    s.put(str(ROOT/name),REMOTE+'/context/'+name)
for name in ['container_probe.py','docker_runtime_runner.py']:
    s.put(str(OUT/name),REMOTE+'/'+name)
runner=(OUT/'remote-build-runner.py').read_text()
runner=runner.replace("'--memory=512m','--memory-swap=1g'", "'--memory='+('512m' if service=='backend' else '1280m'),'--memory-swap=2g'")
runner += "\nif result['status']=='BUILT':\n subprocess.run(['python3',str(root/'docker_runtime_runner.py')],cwd=root,check=False)\n"
with s.open(REMOTE+'/build_runner_fixed.py','w') as f:f.write(runner)
(OUT/'remote-build-runner-fixed.py').write_text(runner)
manifest=json.loads((OUT/'build-source-manifest.json').read_text())
for entry in manifest['files']:entry['sha256']=hashlib.sha256((ROOT/entry['path']).read_bytes()).hexdigest()
manifest['fixes']=['Chinese download headers','IPv4 frontend healthcheck','compressed SQLite backup exclusion']
(OUT/'build-source-manifest-final.json').write_text(json.dumps(manifest,indent=2))
r=remote_python(c,f"""import subprocess,json
from pathlib import Path
root=Path({REMOTE!r})
with (root/'runner-fixed.log').open('wb') as log:
 p=subprocess.Popen(['python3',str(root/'build_runner_fixed.py')],cwd=root,stdout=log,stderr=subprocess.STDOUT,start_new_session=True)
print(json.dumps({{'pid':p.pid,'directory':str(root)}}))
""")
s.close();c.close();(OUT/'docker-rebuild-dispatch.json').write_text(json.dumps(r,indent=2));print(r['stdout'])
