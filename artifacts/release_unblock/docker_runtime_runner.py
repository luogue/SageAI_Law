"""Independent Docker acceptance; never address production containers or volumes."""
import json,subprocess,time,os,tarfile,io,re
from pathlib import Path
ROOT=Path(__file__).resolve().parent
PREFIX='sageai-release-verify-20260909'
BACK=PREFIX+'-backend';FRONT=PREFIX+'-frontend';NET=PREFIX+'-net';VOL=PREFIX+'-fresh-db'
result={'status':'RUNNING','commands':[],'checks':{}}
def save(): (ROOT/'runtime-result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
def run(args,timeout=120,input=None,check=True):
    p=subprocess.run(args,input=input,capture_output=True,text=True,timeout=timeout)
    result['commands'].append({'command':args,'exit':p.returncode,'stdout':p.stdout[-16000:],'stderr':p.stderr[-4000:]});save()
    if check and p.returncode:raise RuntimeError(str(args[:6])+' failed: '+p.stderr[-500:])
    return p
def health(name):
    for attempt in range(60):
        p=subprocess.run(['docker','inspect',name],capture_output=True,text=True)
        c=json.loads(p.stdout)[0]
        if c['State']['Status']!='running':raise RuntimeError(name+' not running')
        h=c['State'].get('Health',{}).get('Status')
        if h=='healthy':return {'state':h,'image':c['Image'],'mounts':c['Mounts'],'command':c['Config']['Cmd']}
        if h=='unhealthy':raise RuntimeError(name+' unhealthy: '+str(c['State'].get('Health')))
        time.sleep(2)
    raise RuntimeError(name+' health timeout')
def probe(mode):
    p=run(['docker','exec',BACK,'python','/tmp/container_probe.py',mode],timeout=360)
    data=json.loads(p.stdout.split('PROBE_RESULT=')[-1]);assert data['status']=='PASS';return data
try:
    # Inspect final root filesystems without starting either application.
    result['checks']['images']={}
    for service in ['backend','frontend']:
        image=PREFIX+':'+service;name=PREFIX+'-inspect-'+service
        run(['docker','create','--name',name,'--network','none','--entrypoint','true',image])
        found=[];count=0
        p=subprocess.Popen(['docker','export',name],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        with tarfile.open(fileobj=p.stdout,mode='r|') as tar:
            for member in tar:
                if not member.isfile():continue
                count+=1;n=member.name.lower()
                if re.search(r'(?:\.db|\.sqlite3?)(?:$|[-.])',n) or '.bak' in Path(n).name:found.append(n)
                # Signature check catches renamed uncompressed SQLite databases.
                f=tar.extractfile(member)
                if f.read(16)==b'SQLite format 3\x00' and n not in found:found.append(n)
        assert p.wait(timeout=30)==0
        run(['docker','rm','-v',name])
        result['checks']['images'][service]={'files_checked':count,'database_files':found}
        assert not found,found
    run(['docker','network','create','--internal',NET])
    run(['docker','volume','create',VOL])
    env=['-e','ENV=production','-e','DATABASE_URL=sqlite:////app/data/app.db','-e','SAGE_DATA_DIR=/app/data','-e','LOG_DIR=/app/logs','-e','RELEASE_VERIFY_ONLY=true','-e','ENABLE_RATE_LIMIT=false','-e','REDIS_URL=redis://127.0.0.1:1/0','-e','JWT_SECRET_KEY=isolated-release-probe-no-business-tokens']
    limits=['--memory=768m','--memory-swap=1536m','--cpus=.5','--cpu-shares=128']
    init=PREFIX+'-initialize'
    run(['docker','create','--name',init,'--network',NET,*limits,*env,'-e','ALLOW_DATABASE_INITIALIZE=true','-v',VOL+':/app/data','--entrypoint','python',PREFIX+':backend','/tmp/container_probe.py','initialize'])
    run(['docker','cp',str(ROOT/'container_probe.py'),init+':/tmp/container_probe.py'])
    p=run(['docker','start','-a',init],timeout=120)
    result['checks']['initialize']=json.loads(p.stdout.split('PROBE_RESULT=')[-1]);save()
    assert result['checks']['initialize']['status']=='PASS'
    run(['docker','rm',init])
    run(['docker','run','-d','--name',BACK,'--network',NET,'--network-alias','backend',*limits,*env,'-v',VOL+':/app/data',PREFIX+':backend'])
    run(['docker','cp',str(ROOT/'container_probe.py'),BACK+':/tmp/container_probe.py'])
    result['checks']['backend_startup']=health(BACK);save()
    run(['docker','run','-d','--name',FRONT,'--network',NET,'--memory=64m','--cpus=.1',PREFIX+':frontend'])
    result['checks']['frontend_startup']=health(FRONT);save()
    result['checks']['frontend_http']=run(['docker','exec',FRONT,'wget','-q','-O','/dev/null','http://127.0.0.1/']).returncode
    result['checks']['before_restart']=probe('before_restart');save()
    run(['docker','restart','-t','30',BACK],timeout=60)
    result['checks']['first_restart_health']=health(BACK)
    result['checks']['after_restart']=probe('after_restart');save()
    run(['docker','restart','-t','30',BACK],timeout=60)
    result['checks']['second_restart_health']=health(BACK)
    result['checks']['completed_restart']=probe('completed_restart');save()
    result['status']='PASS'
except Exception as e:
    result.update(status='FAILED',error=str(e))
finally:
    for name in [BACK,FRONT]:
        p=subprocess.run(['docker','logs','--tail','150',name],capture_output=True,text=True)
        (ROOT/(name+'.log')).write_text(p.stdout+p.stderr)
    result['finished']=time.time();save()
