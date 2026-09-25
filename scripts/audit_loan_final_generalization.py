"""Replays final certificates and deterministic formulas; never changes model output."""
import hashlib,json,sys,zipfile
from pathlib import Path
from decimal import Decimal
import xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'backend')]
from backend.test_database_bootstrap import install
install()
from review_v2.unified_facts.loan import schema
from review_v2.unified_facts.store import CandidateStore,commit
from review_v2.unified_facts.certificates import validate_response
from review_v2.unified_facts.loan_formulas import build
from review_v2.unified_facts.normalization import wire
from review_v2.clause_parser import parse_contract_clauses,strip_non_contract_tail
BASE=ROOT/'artifacts/loan_verified_acceptance'
ORIGINAL={'72':('150000','10.8','YEAR'),'98':('120000','4.2','YEAR'),
          '101':('1200000','7.2','YEAR'),'49':('300000','.8','MONTH'),
          '99':('680000','10.8','YEAR'),'104':('3200000','5.4','YEAR')}

def source_text(path):
    if path.suffix=='.json':return json.loads(path.read_text(encoding='utf8'))['text']
    with zipfile.ZipFile(path) as z:r=ET.fromstring(z.read('word/document.xml'))
    ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    return '\n'.join(''.join(t.text or '' for t in p.findall('.//w:t',ns)) for p in r.findall('.//w:p',ns))

def audit(prefix,hashes):
    runs=sorted(BASE.glob('20*-'+prefix))
    if not runs:
        provider_path=BASE/'provider-availability.json'
        provider=json.loads(provider_path.read_text(encoding='utf8')) if provider_path.exists() else {}
        reason='NOT_RUN_PROVIDER_BLOCKED:INSUFFICIENT_BALANCE' if provider.get('http_status')==402 else 'NOT_RUN'
        return {'contract':prefix,'status':'BLOCKED','pipeline':'NOT_RUN','errors':[reason],
                'source':'SEALED_DEEPSEEK_SYNTHETIC' if prefix.startswith('blind-') else 'EXISTING_DOCX'}
    folder=runs[-1]/prefix
    if not (folder/'result.json').exists():return {'contract':prefix,'status':'BLOCKED','errors':['RUNNING_OR_INTERRUPTED']}
    record=json.loads((folder/'result.json').read_text(encoding='utf8'))
    errors=[]
    if record['code_sha256']!=hashes:errors.append('CODE_SNAPSHOT_CHANGED')
    if record['status']!='PASS':errors.append(record.get('error','PIPELINE_BLOCKED'))
    else:
        try:
            report=json.loads((folder/'report.json').read_text(encoding='utf8'))
            debug=report['structured_fact_debug']
            source=strip_non_contract_tail(source_text(Path(record['file'])))
            s=schema();clauses=parse_contract_clauses(source)
            packet=debug['raw_extraction']
            c=CandidateStore(source,clauses,s,debug['active_concepts'],packet,snapshot_id=debug['candidate_snapshot_id'])
            store=commit(c,debug['verification'])
            if store.snapshot_hash!=debug['candidate_snapshot_hash']:raise ValueError('REPORT_SNAPSHOT_MISMATCH')
            certs=debug['final_verification_batches']
            checked=set()
            for cert in certs:
                scope=cert['searched_concepts']
                subpacket={**packet,'searched_concepts':scope,
                    'observations':[r for r in packet['observations'] if r['concept'] in scope]}
                sub=CandidateStore(source,clauses,s,scope,subpacket,snapshot_id=cert['candidate_snapshot_id'])
                validate_response(sub,cert);commit(sub,cert)
                if checked.intersection(scope):raise ValueError('REUSED_BATCH_CERTIFICATE')
                checked.update(scope)
            if checked!=set(c.active):raise ValueError('UNCERTIFIED_CONCEPTS')
            if wire(build(store))!=report['deterministic_interest_formulas']:raise ValueError('FORMULA_NOT_FROM_VERIFIED_STORE')
            if 'loan.interest_formula' in c.active:raise ValueError('MODEL_FORMULA_STILL_ACTIVE')
            if report['fact_migration']['mode']!='VERIFIED_FACTS' or report['all_items_count']!=48:
                raise ValueError('LEGACY_OR_RULE_COVERAGE_DRIFT')
            if report['statistics_consistency_gate']['status']!='REPORT_READY':raise ValueError('STATISTICS_GATE')
            if prefix in ORIGINAL:
                principal,rate,period=ORIGINAL[prefix];currency='CNY'
            else:
                path=Path(record['file']);sealed=json.loads((path.parent/'manifest.json').read_text(encoding='utf8'))
                expected_hash=next(v['sha256'] for v in sealed if v['id']==prefix)
                if hashlib.sha256(path.read_bytes()).hexdigest()!=expected_hash:raise ValueError('BLIND_SAMPLE_CHANGED')
                exp=json.loads(path.read_text(encoding='utf8'))['expected']
                principal,rate,period,currency=exp['principal'],exp['regular_rate'],exp['rate_period'],exp['currency']
            get=lambda k:store.scalar(k,consumer='independent_acceptance')
            money=get('loan.principal')
            if not money or money['amount']!=Decimal(str(principal)) or money['currency']!=currency:raise ValueError('PRINCIPAL_MISMATCH')
            if rate is not None and (get('loan.regular_rate')!=Decimal(str(rate)) or get('loan.regular_rate_period')!=period):
                raise ValueError('REGULAR_RATE_MISMATCH')
            if rate is None and get('loan.regular_rate') not in (None,Decimal(0)):
                raise ValueError('INTEREST_INVENTED_IN_INTEREST_FREE_CONTRACT')
            if prefix not in ORIGINAL and (get('loan.compound') is True)!=exp['compound']:
                raise ValueError('COMPOUND_SEMANTIC_MISMATCH')
            if prefix in {'101','99'}:
                regular=[f for f in store.get('loan.cost_components',consumer='acceptance')
                    if f['state']=='PRESENT' and f['normalized_value']['kind']=='regular_interest']
                if not regular or any(f['normalized_value']['scope']!='UNTIL_REPAYMENT' for f in regular):raise ValueError('SCOPE_DRIFT')
            if prefix in {'98','101','99','104'}:
                if get('loan.day_count_basis')!=('ACT_360' if prefix=='98' else 'ACT_365'):raise ValueError('DAY_BASIS_MISSING')
            return {'contract':prefix,'status':'PASS','pipeline':'PASS','semantic_acceptance':'PASS',
                    'certificate_snapshot':'PASS','accepted_verifier_evidence':'PASS','source':record['sample_origin'],
                    'artifact_directory':str(folder),'calls':record['calls']}
        except Exception as exc:errors.append(type(exc).__name__+': '+str(exc))
    return {'contract':prefix,'status':'BLOCKED','pipeline':record['status'],'errors':errors,
            'source':record['sample_origin'],'artifact_directory':str(folder),'calls':record['calls']}

if __name__=='__main__':
    hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
        for p in sorted((ROOT/'backend/review_v2/unified_facts').glob('*.py'))}
    prefixes=list(ORIGINAL)+[f'blind-{i}' for i in range(1,7)]
    if '--original-only' in sys.argv:prefixes=list(ORIGINAL)
    rows=[audit(p,hashes) for p in prefixes]
    tests=ET.parse(BASE/'automated.xml').getroot().find('testsuite')
    test_result={k:int(tests.get(k,0)) for k in ('tests','failures','errors','skipped')}
    passed=len(rows)==12 and all(r['status']=='PASS' for r in rows) and not test_result['failures'] and not test_result['errors']
    result={'status':'PASS' if passed else 'BLOCKED','automatic_tests':test_result,'contracts':rows,'code_sha256':hashes,
            'blind_origin':'SEALED_DEEPSEEK_SYNTHETIC; NOT NEW REAL BUSINESS DOCUMENTS'}
    target=BASE/('original-audit.json' if '--original-only' in sys.argv else 'final-generalization.json')
    target.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8')
    print(json.dumps(result,ensure_ascii=False))
    raise SystemExit(0 if all(r['status']=='PASS' for r in rows) else 1)
