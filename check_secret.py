import sys
sys.path.insert(0, 'backend')
import os
from dotenv import load_dotenv

load_dotenv()

print(f"JWT_SECRET_KEY from env: {os.getenv('JWT_SECRET_KEY', 'NOT SET')}")
print(f"Length: {len(os.getenv('JWT_SECRET_KEY', ''))}")

from auth.utils import SECRET_KEY as auth_secret_key
print(f"SECRET_KEY in auth/utils.py: {auth_secret_key}")
print(f"Length: {len(auth_secret_key)}")