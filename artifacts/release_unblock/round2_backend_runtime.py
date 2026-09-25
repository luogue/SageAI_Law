"""Backend container checks only; never label this as full Docker acceptance."""
import subprocess,json,time
from pathlib import Path
root=Path(__file__).resolve().parent
prefix='sageai-release-verify-20260909-round2'
name=prefix+'-backend';volume=prefix+'-db';network=prefix+'-net';image='sageai-release-verify-20260909:backend'
r={'status':'RUNNING','scope':'Real backend Docker, two gunicorn workers, fresh volume; frontend unavailable. Six reviews use explicit rule mode. Persistence writes invoke real storage functions inside the container; reads/login/reviews/downloads use HTTP.','commands':[],'checks':{}}
def save():(root/'round2-backend-runtime.json').write_text(json.dumps(r,ensure_ascii=False,indent=2))
def run(cmd,timeout=120):
    p=subprocess.run(cmd,capture_output=True,text=True,timeout=timeout);r['commands'].append({'command':cmd,'exit':p.returncode,'stdout':p.stdout[-24000:],'stderr':p.stderr[-3000:]});save();assert p.returncode==0,p.stderr[-500:];return p.stdout
def health():
    for _ in range(60):
        v=json.loads(subprocess.run(['docker','inspect',name],capture_output=True,text=True).stdout)[0]
        assert v['State']['Status']=='running',v['State']
        if v['State'].get('Health',{}).get('Status')=='healthy':return v['State']['Health']
        time.sleep(2)
    raise RuntimeError('Health timeout')
env=['-e','ENV=production','-e','DATABASE_URL=sqlite:////app/data/app.db','-e','SAGE_DATA_DIR=/app/data','-e','LOG_DIR=/app/logs','-e','RELEASE_VERIFY_ONLY=true','-e','ENABLE_RATE_LIMIT=false','-e','REDIS_URL=redis://127.0.0.1:1/0','-e','JWT_SECRET_KEY=isolated-round2-verification-only']
limits=['--memory=384m','--memory-swap=512m','--cpus=.5','--cpu-shares=128']
try:
    run(['docker','network','create','--internal',network]);run(['docker','volume','create',volume])
    init=prefix+'-initialize'
    run(['docker','create','--name',init,'--network',network,*limits,*env,'-e','ALLOW_DATABASE_INITIALIZE=true','-v',volume+':/app/data','--entrypoint','python',image,'/tmp/probe.py','initialize'])
    run(['docker','cp',str(root/'round2_container_probe.py'),init+':/tmp/probe.py'])
    output=run(['docker','start','-a',init]);r['checks']['initialize']=json.loads(output.split('PROBE_RESULT=')[-1]);save();run(['docker','rm',init])
    run(['docker','run','-d','--name',name,'--network',network,'--network-alias','backend',*limits,*env,'-v',volume+':/app/data',image,'gunicorn','main:app','--workers','2','--worker-class','uvicorn.workers.UvicornWorker','--bind','0.0.0.0:8000','--timeout','180','--graceful-timeout','30'])
    run(['docker','cp',str(root/'round2_container_probe.py'),name+':/tmp/probe.py'])
    for mode in ['before_restart','after_restart','completed_restart']:
        if mode!='before_restart':run(['docker','restart','--timeout','30',name],60)
        r['checks'][mode+'_health']=health();save()
        output=run(['docker','exec',name,'python','/tmp/probe.py',mode],240)
        r['checks'][mode]=json.loads(output.split('PROBE_RESULT=')[-1]);save()
    r['status']='PASS_BACKEND_ONLY'
except Exception as e:r.update(status='FAIL',error=str(e))
finally:
    p=subprocess.run(['docker','logs','--tail','180',name],capture_output=True,text=True)
    (root/'round2-backend-runtime.log').write_text(p.stdout+p.stderr)
    # Release only this test container's load; retain its test volume and evidence.
    p=subprocess.run(['docker','stop','--timeout','30',name],capture_output=True,text=True,timeout=45)
    r['cleanup']={'stop_exit':p.returncode,'stdout':p.stdout,'stderr':p.stderr};r['finished']=time.time();save()
