"""修改管理员密码为 a.144iLil123"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from storage.database import engine, Base
from storage.models import Admin
from storage.crud import get_admin_by_username
from auth.utils import hash_password, verify_password
from sqlalchemy.orm import sessionmaker

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

# 获取管理员
admin = get_admin_by_username('admin')
if admin:
    # 修改密码为 a.144iLil123
    admin.password_hash = hash_password('a.144iLil123')
    db.commit()
    print("密码已修改为: a.144iLil123")

    # 验证新密码
    if verify_password('a.144iLil123', admin.password_hash):
        print("密码验证成功! ✅")
    else:
        print("密码验证失败! ❌")
else:
    print("管理员账号不存在!")

db.close()
print("\n现在可以使用 admin/a.144iLil123 登录了!")