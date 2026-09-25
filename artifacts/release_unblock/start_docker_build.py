"""Build a source-only, isolated verification context on the accessible Docker host."""
import fnmatch
import hashlib
import io
import json
import os
import shlex
import tarfile
from datetime import datetime, timezone
from pathlib import Path
from production_probe import ROOT, OUT, connect, remote_python

RUN='sageai-release-verify-20260909'
REMOTE='/var/tmp/'+RUN

def main():
    archive=OUT/'build-context.tar.gz'
    files=[]
    deny_dirs={'node_modules','dist','__pycache__','.git','logs','data','.pytest_cache'}
    with tarfile.open(archive,'w:gz') as tar:
        for base in ('backend','frontend'):
            for directory,dirs,names in os.walk(ROOT/base):
                dirs[:]=[d for d in dirs if d not in deny_dirs]
                for name in names:
                    if name.startswith('.env') or any(fnmatch.fnmatch(name,p) for p in ('*.db','*.db-*','*.sqlite*','*.bak*','*.log','*.pyc','*.zip','*.gz')):continue
                    path=Path(directory)/name
                    if path.is_symlink():continue
                    rel=path.relative_to(ROOT).as_posix()
                    tar.add(path,arcname=rel)
                    files.append({'path':rel,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
        for name in ('Dockerfile.backend','Dockerfile.frontend','.dockerignore','nginx.conf'):
            tar.add(ROOT/name,arcname=name)
            files.append({'path':name,'sha256':hashlib.sha256((ROOT/name).read_bytes()).hexdigest()})
        # Dummy non-business canaries test actual Docker exclusions, not just filename patterns.
        for name in ('app.db','app.db-wal','app.db-shm','archive.sqlite','archive.sqlite.gz'):
            data=b'NON_BUSINESS_DATABASE_EXCLUSION_CANARY\n'
            info=tarfile.TarInfo('backend/release_exclusion_canary/'+name);info.size=len(data)
            tar.addfile(info,io.BytesIO(data))
    manifest={'run':RUN,'remote':REMOTE,'archive_sha256':hashlib.sha256(archive.read_bytes()).hexdigest(),'bytes':archive.stat().st_size,'files':files}
    (OUT/'build-source-manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
    runner='''import subprocess,json,os,time
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
'''
    (OUT/'remote-build-runner.py').write_text(runner,encoding='utf-8')
    client=connect();sftp=client.open_sftp()
    sftp.mkdir(REMOTE);sftp.put(str(archive),REMOTE+'/context.tar.gz')
    with sftp.open(REMOTE+'/build_runner.py','w') as f:f.write(runner)
    code=f'''import tarfile,subprocess,json,os
from pathlib import Path
root=Path({REMOTE!r});context=root/'context';context.mkdir()
with tarfile.open(root/'context.tar.gz') as archive:
 for member in archive.getmembers():
  if not (context/member.name).resolve().is_relative_to(context.resolve()):raise RuntimeError('Unsafe archive member')
 archive.extractall(context)
with (root/'runner.log').open('wb') as log:
 p=subprocess.Popen(['python3',str(root/'build_runner.py')],cwd=root,stdout=log,stderr=subprocess.STDOUT,start_new_session=True)
print(json.dumps({{'pid':p.pid,'workdir':str(root),'context_bytes':(root/'context.tar.gz').stat().st_size}}))
'''
    result=remote_python(client,code);sftp.close();client.close()
    (OUT/'docker-build-dispatch.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(result['stdout'])

if __name__=='__main__':main()
