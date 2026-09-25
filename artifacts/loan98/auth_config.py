from pathlib import Path
p=Path('scripts/run_loan98_acceptance.py');s=p.read_text(encoding='utf8').replace('from auth.utils import create_access_token',"from dotenv import load_dotenv\nload_dotenv(ROOT/'backend/.env')\nfrom auth.utils import create_access_token");p.write_text(s,encoding='utf8')
