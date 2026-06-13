"""创建管理员账号"""
import sys
import os

# 切换到backend目录
os.chdir('backend')
sys.path.insert(0, '.')

from storage.database import engine, Base
from storage.models import Admin
from storage.crud import create_admin, get_admin_by_username
from auth.utils import hash_password

# 创建所有表
print("创建数据库表...")
Base.metadata.create_all(bind=engine)
print("数据库表创建成功")

# 检查管理员
admin = get_admin_by_username('admin')
if admin:
    print(f"管理员已存在: {admin.username}")
else:
    print("创建管理员账号...")
    create_admin('admin', hash_password('a.144iLil123'))
    print("管理员创建成功!")
    print("  用户名: admin")
    print("  密码: a.144iLil123")