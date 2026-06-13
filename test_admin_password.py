"""测试管理员密码验证"""
import sys
sys.path.insert(0, './backend')

from storage.crud import get_admin_by_username
from auth.utils import verify_password, hash_password

# 检查数据库中的管理员
admin = get_admin_by_username('admin')
print(f"数据库中管理员存在: {admin is not None}")

if admin:
    print(f"管理员用户名: {admin.username}")
    print(f"密码哈希: {admin.password_hash}")

    # 测试密码验证
    test_passwords = ['admin', 'a.144iLil123', 'admin123']
    for pwd in test_passwords:
        result = verify_password(pwd, admin.password_hash)
        print(f"密码 '{pwd}' 验证结果: {result}")

    # 测试新密码哈希
    new_hash = hash_password('a.144iLil123')
    print(f"\n新密码 'a.144iLil123' 的哈希: {new_hash}")
    print(f"新哈希验证: {verify_password('a.144iLil123', new_hash)}")
else:
    print("数据库中没有管理员账号")
    print("\n创建测试管理员...")
    from storage.crud import create_admin
    create_admin('admin', hash_password('a.144iLil123'))
    print("管理员创建成功")