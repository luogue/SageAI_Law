"""迁移脚本007 - 添加管理员账号表"""
import sys
sys.path.insert(0, '.')

from storage.models import Admin
from storage.crud import init_db, create_admin, get_admin_by_username
from auth.utils import hash_password


def run():
    print("初始化数据库表...")
    init_db()
    
    # 检查是否已有管理员
    existing_admin = get_admin_by_username("admin")
    if existing_admin:
        print("管理员账号已存在，跳过创建")
        return
    
    # 创建管理员
    print("创建管理员账号: admin")
    create_admin("admin", hash_password("a.144iLil123"))
    print("管理员账号创建成功!")
    print("用户名: admin")
    print("密码: a.144iLil123")


if __name__ == "__main__":
    run()
