import sys
sys.path.insert(0, 'backend')
import os
from dotenv import load_dotenv

load_dotenv()

print(f"JWT_SECRET_KEY from env: '{os.getenv('JWT_SECRET_KEY', 'NOT SET')}'")
print(f"Length: {len(os.getenv('JWT_SECRET_KEY', ''))}")

# 模拟后端环境
os.environ['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your-secret-key-here')

from auth.utils import create_access_token, verify_token

# 为用户ID 1创建token
token = create_access_token({'user_id': 1})
print(f"Token: {token}")

# 验证token
user_id = verify_token(token)
print(f"Verified user_id: {user_id}")