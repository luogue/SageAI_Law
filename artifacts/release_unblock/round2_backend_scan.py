"""Scan final backend rootfs AND every image layer for database payloads."""
import subprocess,json,tarfile,re,gzip,io,hashlib
from pathlib import Path
root=Path(__file__).resolve().parent
image='sageai-release-verify-20260909:backend'
name='sageai-release-verify-20260909-round2-scan'
result={'status':'FAIL','image':image,'commands':[],'scans':[]}
pattern=re.compile(r'\.(?:db|sqlite3?)(?:-(?:wal|shm|journal)|\.(?:gz|bz2|xz|zip|bak))?$|\.bak(?:\.\d+)?$',re.I)
def scan(archive,label):
    count=0;found=[]
    for m in archive:
        if not m.isfile():continue
        count+=1;n=m.name.lstrip('./');f=archive.extractfile(m);head=f.read(16)
        reason=[]
        if pattern.search(n):reason.append('database/backup filename')
        if head==b'SQLite format 3\x00':reason.append('SQLite signature')
        if n.startswith(('app/data/','app/backups/','app/artifacts/db_recovery/','app/artifacts/release_unblock/','app/logs/')):reason.append('business/evidence data directory contains file')
        if reason:found.append({'file':n,'size':m.size,'reason':reason})
    result['scans'].append({'scope':label,'files_checked':count,'findings':found})
def run(cmd):
    p=subprocess.run(cmd,capture_output=True,text=True);result['commands'].append({'command':cmd,'exit':p.returncode});assert p.returncode==0,p.stderr;return p.stdout
try:
    v=json.loads(run(['docker','image','inspect',image]))[0];result['image_id']=v['Id'];result['layers']=v['RootFS']['Layers']
    run(['docker','create','--name',name,'--network','none','--entrypoint','true',image])
    p=subprocess.Popen(['docker','export',name],stdout=subprocess.PIPE)
    with tarfile.open(fileobj=p.stdout,mode='r|') as t:scan(t,'final root filesystem')
    assert p.wait()==0;run(['docker','rm','-v',name])
    archive=root/'round2-backend-image.tar'
    run(['docker','image','save','-o',str(archive),image])
    with tarfile.open(archive) as outer:
        # Docker 29 OCI archives and legacy layer.tar archives are both supported.
        for m in outer:
            if not m.isfile():continue
            f=outer.extractfile(m)
            try:
                with tarfile.open(fileobj=f,mode='r|*') as layer:scan(layer,'layer '+m.name)
            except tarfile.ReadError:pass
    result['status']='PASS' if all(not x['findings'] for x in result['scans']) else 'FAIL'
except Exception as e:result['error']=str(e)
(root/'round2-backend-scan.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result))
