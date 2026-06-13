import sys
sys.path.insert(0, 'backend')
from auth.utils import create_access_token, verify_token

# 为用户ID 1创建token
token = create_access_token({'user_id': 1})
print(f"Token: {token}")

# 验证token
user_id = verify_token(token)
print(f"Verified user_id: {user_id}")