"""Start/restart a distinct loopback instance on a COPY of the chosen candidate."""
import hashlib
import json
import os
import secrets
import socket
import sqlite3
import subprocess
import sys
import tempfile
import time
from pathlib import Path
import requests

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'artifacts/db_recovery'
CANDIDATE = OUT / 'candidates_latest/logical.db'
SERVER = Path(__file__).with_name('isolated_server.py')


def main():
    work = Path(tempfile.mkdtemp(prefix='sageai-test-recovery-'))
    database = work / 'app.db'
    database.write_bytes(CANDIDATE.read_bytes())
    (work / 'logs').mkdir()
    with socket.socket() as sock:
        sock.bind(('127.0.0.1', 0))
        port = sock.getsockname()[1]
    secret = secrets.token_hex(32)
    env = dict(os.environ, ENV='test', SAGE_TEST_ROOT=str(work), SAGE_DATA_DIR=str(work),
               DATABASE_URL='sqlite:///' + database.as_posix(), LOG_DIR=str(work/'logs'),
               REDIS_URL='redis://127.0.0.1:1/0', PROBE_SECRET=secret, PROBE_PORT=str(port),
               ENABLE_RATE_LIMIT='false', PYTHONIOENCODING='utf-8')
    base = f'http://127.0.0.1:{port}'
    session = requests.Session()
    session.trust_env = False
    session.headers['X-Probe-Secret'] = secret
    result = {'candidate':str(CANDIDATE), 'candidate_sha256':hashlib.sha256(CANDIDATE.read_bytes()).hexdigest(),
              'instance_db':str(database), 'port':port, 'checks':{},
              'scope':'Real app/router/ORM; synthetic-account password login; existing account accessed with a signed test token; V2 rule mode use_llm=false; rate limit disabled only for isolated batch probes'}
    processes = []
    def start(number):
        log = (OUT / f'instance-{number}.log').open('wb')
        proc = subprocess.Popen([sys.executable, str(SERVER)], cwd=work, env=env, stdout=log, stderr=subprocess.STDOUT, creationflags=subprocess.CREATE_NO_WINDOW)
        processes.append((proc, log))
        for _ in range(120):
            if proc.poll() is not None:
                raise RuntimeError(f'Instance {number} exited: inspect instance log')
            try:
                response = session.get(base+'/health', timeout=2)
                if response.status_code == 200:
                    result['checks'][f'startup_{number}'] = response.json()
                    return proc
            except requests.RequestException:
                pass
            time.sleep(.25)
        raise RuntimeError('Instance startup timeout')
    def call(method, path, **kwargs):
        response = session.request(method, base+path, timeout=120, **kwargs)
        if response.status_code != 200:
            raise RuntimeError(f'{path}: HTTP {response.status_code}: {response.text[:200]}')
        return response.json()
    def stop(proc):
        call('POST', '/__probe/shutdown')
        proc.wait(timeout=20)
    try:
        proc = start(1)
        seed = call('POST', '/__probe/seed')
        login = call('POST', '/auth/login', json={'phone':'19900000001','password':'Isolated-acceptance-2026!'})
        assert login['success']
        user_id = login['user_id']
        session.headers['Authorization'] = 'Bearer '+login['access_token']
        assert call('GET','/auth/me')['user_id'] == user_id
        result['checks']['login_account'] = 'PASS: real password verification and /auth/me'
        new_task = call('POST','/__probe/task', json={'user_id':user_id})['task_id']
        call('POST','/__probe/task', json={'task_id':new_task, 'changes':{'status':'processing','progress':35,'metadata':{'acceptance':True}}})
        assert call('GET','/api/task/'+new_task)['progress'] == 35
        result['checks']['create_and_persist_task'] = 'PASS'
        session.headers['Authorization'] = 'Bearer '+seed['existing_account_token']
        history = call('GET','/api/tasks')
        assert len(history) == 33, len(history)
        for task in history:
            detail = call('GET','/api/task/'+task['task_id'])
            assert detail['task_id'] == task['task_id'] and detail['result'] == task['result']
        result['checks']['history_list_and_all_33_details'] = 'PASS'
        missing_report = session.get(base+'/api/records/1', timeout=10)
        assert missing_report.status_code == 404
        result['checks']['preexisting_report_1_missing'] = {'status':'DATA_GAP', 'http_status':404, 'affected_task_links':14}
        session.headers['Authorization'] = 'Bearer '+login['access_token']
        cases = {
            'house_lease':'房屋租赁合同。出租人甲方将房屋出租给承租人乙方居住使用，租期一年，月租金三千元，押金一个月租金。到期交还房屋并结清水电费。',
            'work_contract':'承揽合同。定作方甲方委托承揽方乙方加工一百套机械零件，按照图纸加工，价款十万元，交付后十日内验收，质量不合格应返工。',
            'transportation':'运输合同。托运人甲方委托承运人乙方将机械设备由北京运至上海，运费一万元，到货验收后付款，承运人负责货物安全并赔偿运输损失。',
            'investment':'投资协议。投资方甲方向融资方乙公司投资一百万元取得百分之十股权。双方约定资金用于生产经营，投资方享有知情权和利润分配权。',
            'shareholders':'股东协议。股东甲和股东乙共同出资设立有限责任公司，甲认缴六十万元，乙认缴四十万元。股东按出资比例行使表决权，利润按实缴比例分配。',
            'labor':'劳动合同。用人单位甲公司聘用劳动者乙担任工程师，劳动期限三年，每月工资一万元，每周工作四十小时。单位依法缴纳社会保险，双方依法解除劳动合同。',
        }
        result['checks']['v2_profiles'] = {}
        for typ, contract in cases.items():
            response = call('POST','/review-v2/checklist', json={'contract_text':contract, 'contract_type':typ, 'use_llm':False,
                'profile':{'user_identity':'个人租客','contract_scenario':'居住用途','risk_appetite':'激进','bargaining_position':'强势方','contract_type':'house_lease'}})
            assert response['success']
            profile = response['profile']
            assert profile['risk_appetite'] == '激进'
            if typ != 'house_lease':
                assert '个人租客' not in json.dumps(profile, ensure_ascii=False) and '居住用途' not in json.dumps(profile, ensure_ascii=False)
            result['checks']['v2_profiles'][typ] = {'status':'PASS','profile':profile}
        from docx import Document
        from io import BytesIO
        document = Document()
        document.add_paragraph(cases['work_contract'])
        content = BytesIO()
        document.save(content)
        uploaded = call('POST','/review-v2/file',
            files={'file':('isolated-contract.docx',content.getvalue(),'application/vnd.openxmlformats-officedocument.wordprocessingml.document')},
            data={'contract_type':'work_contract','use_llm':'false','profile_json':json.dumps({'risk_appetite':'激进'})})
        assert uploaded['success'] and uploaded['profile']['contract_type']=='work_contract'
        result['checks']['v2_docx_upload'] = 'PASS: real input extraction and review'
        saved = call('POST','/__probe/report', json={'user_id':user_id,'markdown':'# Independent acceptance report\nDatabase roundtrip verified.'})['record_id']
        report = call('GET',f'/api/records/{saved}')
        assert 'Database roundtrip verified.' in report['report_markdown']
        assert call('POST','/__probe/rollback',json={'user_id':user_id})['rolled_back']
        result['checks']['new_report_save_read'] = 'PASS'
        result['checks']['exception_rollback'] = 'PASS'
        stop(proc)
        proc = start(2)
        detail = call('GET','/api/task/'+new_task)
        assert detail['status'] == 'processing' and detail['progress'] == 35
        assert any(t['task_id']==new_task for t in call('GET','/api/tasks'))
        assert call('GET',f'/api/records/{saved}')['report_markdown'] == report['report_markdown']
        call('POST','/__probe/task',json={'task_id':new_task,'changes':{'status':'completed','progress':100,'result':'durable result','record_id':saved}})
        result['checks']['restart_restore_pending_and_report'] = 'PASS'
        stop(proc)
        proc = start(3)
        assert call('GET','/api/task/'+new_task)['result'] == 'durable result'
        result['checks']['restart_restore_completed'] = 'PASS'
        stop(proc)
        result['business_regression'] = 'PASS_WITH_SCOPE_LIMITS'
    except Exception as error:
        result['business_regression'] = 'FAILED'
        result['error'] = str(error)
    finally:
        for proc, log in processes:
            if proc.poll() is None:
                try:
                    stop(proc)
                except Exception:
                    proc.terminate()  # Only our isolated test process, never the running service.
                    proc.wait(timeout=10)
            log.close()
        db = sqlite3.connect(database.as_uri()+'?mode=ro&immutable=1',uri=True)
        result['final_checks'] = {name:db.execute('PRAGMA '+name).fetchall() for name in ('integrity_check','quick_check','foreign_key_check')}
        db.close()
        result['candidate_unchanged'] = hashlib.sha256(CANDIDATE.read_bytes()).hexdigest() == result['candidate_sha256']
        (OUT/'business-regression.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__ == '__main__':
    main()
