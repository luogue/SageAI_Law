"""检查管理员密码"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from storage.database import engine, Base
from storage.models import Admin
from storage.crud import get_admin_by_username
from auth.utils import verify_password, hash_password

# 获取管理员
admin = get_admin_by_username('admin')
if admin:
    print(f"管理员存在: {admin.username}")
    print(f"密码哈希: {admin.password_hash}")

    # 测试密码验证
    test_passwords = ['admin', 'a.144iLil123', 'admin123']
    for pwd in test_passwords:
        result = verify_password(pwd, admin.password_hash)
        print(f"密码 '{pwd}' 验证: {result}")

    # 重新生成正确的哈希
    correct_hash = hash_password('a.144iLil123')
    print(f"\n正确的哈希: {correct_hash}")
    print(f"当前哈希: {admin.password_hash}")
    print(f"是否匹配: {admin.password_hash == correct_hash}")
else:
    print("管理员账号不存在!")