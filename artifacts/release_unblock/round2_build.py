"""One clean Vite production build, with resource-only npm configuration."""
import subprocess,time,json,os
from pathlib import Path
root=Path(__file__).resolve().parent
context=root/'context'
config=context/'frontend/.npmrc'
assert not config.exists(), 'Do not overwrite existing build configuration'
config.write_text('node-options=--max-old-space-size=768\n')
cmd=['docker','build','--memory=512m','--memory-swap=1536m','--cpu-period=100000',
     '--cpu-quota=50000','--cpu-shares=128','--force-rm','-f','Dockerfile.frontend',
     '-t','sageai-release-verify-20260909:frontend','.']
result={'status':'RUNNING','command':cmd,'started':time.time(),
        'resource_configuration':{'npm_node_options':'--max-old-space-size=768','physical_memory':'512m','memory_plus_swap':'1536m'},
        'checks_unchanged':'Original Dockerfile, npm run build, production Vite configuration, dependency lock and minification unchanged.',
        'resource_samples':[]}
def save(): (root/'round2-build-result.json').write_text(json.dumps(result,indent=2))
save()
with (root/'round2-build-frontend.log').open('wb') as log:
    p=subprocess.Popen(cmd,cwd=context,env=dict(os.environ,DOCKER_BUILDKIT='0'),stdout=log,stderr=subprocess.STDOUT)
    deadline=time.monotonic()+600
    while p.poll() is None:
        mem={l.split(':')[0]:l.split(':')[1].strip() for l in Path('/proc/meminfo').read_text().splitlines()}
        result['resource_samples'].append({'at':time.time(),'available':mem.get('MemAvailable'),'swap_free':mem.get('SwapFree')});save()
        if time.monotonic()>deadline:
            p.terminate();p.wait(timeout=30);result['error']='Verification build exceeded 600 seconds';break
        time.sleep(5)
    result['exit']=p.returncode;result['status']='PASS' if p.returncode==0 else 'FAIL'
result['finished']=time.time();save()
# The resource-only context configuration is retained alongside the evidence.
