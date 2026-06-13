import sys
sys.path.insert(0, 'backend')
from auth.utils import create_access_token

# 为用户ID 1创建token
token = create_access_token({'user_id': 1})
print(token)