import subprocess,json,os,time
from pathlib import Path
root=Path(__file__).resolve().parent
result={'commands':[],'status':'RUNNING','started':time.time()}
def save(): (root/'build-result.json').write_text(json.dumps(result,indent=2))
save()
for service in ('backend','frontend'):
 cmd=['docker','build','--memory=512m','--memory-swap=1g','--cpu-period=100000','--cpu-quota=50000','--cpu-shares=128','--force-rm','-f','Dockerfile.'+service,'-t','sageai-release-verify-20260909:'+service,'.']
 result['commands'].append({'service':service,'command':cmd,'environment':{'DOCKER_BUILDKIT':'0'}});save()
 with (root/('build-'+service+'.log')).open('wb') as output:
  try: p=subprocess.run(cmd,cwd=root/'context',env=dict(os.environ,DOCKER_BUILDKIT='0'),stdout=output,stderr=subprocess.STDOUT,timeout=1800);code=p.returncode
  except subprocess.TimeoutExpired:code=124
 result['commands'][-1]['exit']=code;save()
 if code: result['status']='FAILED';break
else:result['status']='BUILT'
result['finished']=time.time();save()
