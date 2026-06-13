"""创建管理员表和账号"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from storage.database import engine, Base
from storage.models import Admin
from storage.crud import get_admin_by_username, create_admin
from auth.utils import hash_password

# 创建所有表
print("创建数据库表...")
Base.metadata.create_all(bind=engine)
print("数据库表创建完成")

# 检查管理员
admin = get_admin_by_username('admin')
if admin:
    print(f"管理员已存在: {admin.username}")
    # 测试密码验证
    from auth.utils import verify_password
    test_passwords = ['admin', 'a.144iLil123', 'admin123']
    for pwd in test_passwords:
        result = verify_password(pwd, admin.password_hash)
        print(f"  密码 '{pwd}' 验证: {result}")
else:
    print("创建管理员账号...")
    create_admin('admin', hash_password('a.144iLil123'))
    print("管理员创建成功!")
    print("  用户名: admin")
    print("  密码: a.144iLil123")