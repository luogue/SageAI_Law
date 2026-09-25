from pathlib import Path
import subprocess,sys,concurrent.futures
root=Path('artifacts/employment-adapter')
def run(p):
 out=root/'matrix'/p.stem;out.mkdir(parents=True,exist_ok=True)
 with (out/'run.log').open('w',encoding='utf8') as f:
  proc=subprocess.run([sys.executable,'scripts/run_employment_fact_acceptance.py',str(p),'--output',str(out)],stdout=f,stderr=subprocess.STDOUT)
 return p.stem,proc.returncode
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
 for result in pool.map(run, sorted((root/'fixtures').glob('*.docx'))): print(result,flush=True)
