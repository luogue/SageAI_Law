"""Runs only inside the separately named verification container on a fresh volume."""
import json,os,sys,time,sqlite3,importlib,hashlib
from pathlib import Path
import requests
assert os.environ.get('RELEASE_VERIFY_ONLY')=='true'
assert os.environ['DATABASE_URL']=='sqlite:////app/data/app.db'
sys.path.insert(0, '/app')
mode=sys.argv[1]
statefile=Path('/app/data/release-probe-state.json')
result={'mode':mode,'checks':{}}

def checks():
    with sqlite3.connect('/app/data/app.db') as db:
        return {p:db.execute('PRAGMA '+p).fetchall() for p in ['integrity_check','quick_check','foreign_key_check']}

if mode=='initialize':
    assert not Path('/app/data/app.db').exists(), 'Verification volume must be new'
    from storage.crud import init_db,create_user
    from storage.database import session_scope
    from storage.models import User
    from auth.utils import hash_password
    init_db()
    migrations=[]
    for name in ['migrate_db','004_add_file_hash_cache','005_add_country_code','006_add_security_enhancements','007_add_admin_table','008_add_raw_output']:
        module=importlib.import_module('migrations.'+name)
        import contextlib,io
        with contextlib.redirect_stdout(io.StringIO()):
            getattr(module,'migrate',getattr(module,'run',None))()
        migrations.append(name)
    user=create_user('19900000909',hash_password('Release-verify-2026!'))
    with session_scope() as db:
        account=db.get(User,user.id);account.status='normal';account.bonus_credits=50;db.commit()
    result['checks']={'migrations':migrations,'database':checks(),'user_id':user.id}
else:
    s=requests.Session();s.trust_env=False
    base='http://127.0.0.1:8000'
    def call(method,path,**kw):
        r=s.request(method,base+path,timeout=180,**kw)
        assert r.status_code==200,(path,r.status_code,r.text[:250])
        return r.json()
    login=call('POST','/auth/login',json={'phone':'19900000909','password':'Release-verify-2026!'})
    assert login['success'];s.headers['Authorization']='Bearer '+login['access_token']
    user_id=login['user_id'];assert call('GET','/auth/me')['user_id']==user_id
    result['checks']['login']='PASS'
    result['checks']['health']=call('GET','/health')
    if mode=='before_restart':
        cases={
            'house_lease':'房屋租赁合同。出租人甲方将房屋出租给承租人乙方居住使用，租期一年，月租金三千元，押金一个月租金。到期交还房屋并结清水电费。',
            'work_contract':'承揽合同。定作方甲方委托承揽方乙方加工一百套机械零件，按照图纸加工，价款十万元，交付后十日内验收，质量不合格应返工。',
            'transportation':'运输合同。托运人甲方委托承运人乙方将机械设备由北京运至上海，运费一万元，到货验收后付款，承运人负责货物安全并赔偿运输损失。',
            'investment':'投资协议。投资方甲方向融资方乙公司投资一百万元取得百分之十股权。双方约定资金用于生产经营，投资方享有知情权和利润分配权。',
            'shareholders':'股东协议。股东甲和股东乙共同出资设立有限责任公司，甲认缴六十万元，乙认缴四十万元。股东按出资比例行使表决权，利润按实缴比例分配。',
            'labor':'劳动合同。用人单位甲公司聘用劳动者乙担任工程师，劳动期限三年，每月工资一万元，每周工作四十小时。单位依法缴纳社会保险，双方依法解除劳动合同。'}
        result['checks']['v2_profiles']={}
        for typ,text in cases.items():
            data=call('POST','/review-v2/checklist',json={'contract_text':text,'contract_type':typ,'use_llm':False,
                'profile':{'user_identity':'个人租客','contract_scenario':'居住用途','risk_appetite':'激进','bargaining_position':'强势方','contract_type':'house_lease'}})
            assert data['success'];profile=data['profile'];assert profile['risk_appetite']=='激进'
            if typ!='house_lease':assert all(x not in json.dumps(profile,ensure_ascii=False) for x in ['个人租客','居住用途'])
            result['checks']['v2_profiles'][typ]={'status':'PASS','profile':profile,'response_keys':list(data)}
        from tasks import create_task,update_task,TaskStatus
        from storage.crud import create_record,get_user_by_id
        from storage.database import session_scope
        from storage.models import User
        task=create_task('退休人员返聘协议（发布验证）.docx',100,user_id)
        update_task(task.task_id,status=TaskStatus.PROCESSING,progress=35)
        assert call('GET','/api/task/'+task.task_id)['progress']==35
        markdown='# 发布验证报告\n\n独立数据库持久化检查。'
        record_id=create_record(user_id,task.filename,markdown,{})
        assert call('GET',f'/api/records/{record_id}')['report_markdown']==markdown
        before=get_user_by_id(user_id).bonus_credits
        try:
            with session_scope() as db:
                db.get(User,user_id).bonus_credits=9999;db.flush();raise RuntimeError('test rollback')
        except RuntimeError:pass
        assert get_user_by_id(user_id).bonus_credits==before
        state={'task_id':task.task_id,'record_id':record_id,'markdown':markdown}
        statefile.write_text(json.dumps(state,ensure_ascii=False))
        result['checks'].update(create_task='PASS',persist_status='PASS',save_read_report='PASS',rollback='PASS')
    else:
        state=json.loads(statefile.read_text());uid=state['task_id'];rid=state['record_id']
        detail=call('GET','/api/task/'+uid)
        assert any(t['task_id']==uid for t in call('GET','/api/tasks'))
        assert call('GET',f'/api/records/{rid}')['report_markdown']==state['markdown']
        if mode=='after_restart':
            assert detail['status']=='processing' and detail['progress']==35
            from tasks import update_task,TaskStatus
            update_task(uid,status=TaskStatus.COMPLETED,progress=100,result=state['markdown'],record_id=rid)
        else:assert detail['status']=='completed' and detail['result']==state['markdown']
        for path in [f'/api/task/{uid}/download',f'/api/download/{rid}']:
            for fmt in ['md','docx','pdf']:
                r=s.get(base+path,params={'format':fmt},timeout=60)
                assert r.status_code==200,(path,fmt,r.status_code,r.text[:200]);assert r.headers['content-disposition'].isascii()
        result['checks'].update(restart_restore='PASS',history_list_detail='PASS',exports='PASS')
    result['checks']['database']=checks()
result['status']='PASS'
print('PROBE_RESULT='+json.dumps(result,ensure_ascii=False))
