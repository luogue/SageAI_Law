"""Read-only production discovery using existing deployment connection settings.

Never print credentials, full container environments, or business row contents.
"""
import json
import re
import shlex
from pathlib import Path
import paramiko

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent

def connect():
    config = (ROOT/'deploy_to_server.ps1').read_text(encoding='utf-8-sig')
    def value(name):
        return re.search(r'\[string\]\$'+name+r'\s*=\s*"([^"]*)"',config).group(1)
    client = paramiko.SSHClient()
    client.load_host_keys(str(Path.home()/'.ssh/known_hosts'))
    client.set_missing_host_key_policy(paramiko.RejectPolicy())
    client.connect(value('ServerIP'),username=value('ServerUser'),password=value('ServerPassword'),
                   allow_agent=False,look_for_keys=False,timeout=10,auth_timeout=10,banner_timeout=10)
    return client

def remote_python(client, code):
    command = 'python3 -c '+shlex.quote(code)
    _,stdout,stderr = client.exec_command(command,timeout=30)
    return {'command':command,'exit':stdout.channel.recv_exit_status(),
            'stdout':stdout.read().decode(errors='replace'),'stderr':stderr.read().decode(errors='replace')}

def main():
    result = {'PRODUCTION_DB_STATUS':'UNKNOWN','access_method':'Existing deployment settings; strict known_hosts; credentials not logged'}
    try:
        client = connect()
        result['access']='CONNECTED'
        code = '''import json,subprocess,os
def run(args):
 p=subprocess.run(args,capture_output=True,text=True);return {'exit':p.returncode,'stdout':p.stdout,'stderr':p.stderr}
r={'uname':run(['uname','-a']),'memory':run(['free','-m']),'disk':run(['df','-h','/opt/sageai']),
   'docker_version':run(['docker','version','--format','{{json .Server}}']),
   'containers':run(['docker','ps','--format','{{json .}}']),
   'git_commit':run(['git','-C','/opt/sageai','rev-parse','HEAD'])}
p=subprocess.run(['docker','inspect','sageai-backend'],capture_output=True,text=True)
if p.returncode==0:
 c=json.loads(p.stdout)[0];e=dict(x.split('=',1) for x in c['Config']['Env'] if '=' in x)
 r['backend']={'id':c['Id'],'image_id':c['Image'],'image_name':c['Config']['Image'],'created':c['Created'],
 'state':{k:c['State'].get(k) for k in ['Status','Running','StartedAt','Health']},'working_dir':c['Config']['WorkingDir'],
 'environment':{k:e.get(k) for k in ['DATABASE_URL','ENV','SAGE_DATA_DIR']},'mounts':c['Mounts'],
 'labels':{k:v for k,v in c['Config'].get('Labels',{}).items() if k.startswith('com.docker.compose.') or k.startswith('org.opencontainers.image.')},'command':c['Config']['Cmd']}
else:r['backend_inspect_error']=p.stderr
print(json.dumps(r,ensure_ascii=False))
'''
        probe=remote_python(client,code)
        result['discovery']=probe
        if probe['exit']==0:
            result['discovery_data']=json.loads(probe['stdout'])
        client.close()
    except Exception as error:
        result['access']='FAILED'
        result['error_type']=type(error).__name__
        # Credentials are never included in authentication exception output.
        result['error']=str(error)
    (OUT/'production-discovery.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k not in ('discovery',)},ensure_ascii=False,indent=2))

if __name__=='__main__':
    main()
