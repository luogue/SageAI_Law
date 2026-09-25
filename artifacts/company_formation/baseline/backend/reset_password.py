"""密码重置脚本 - 用于重置指定用户的密码
使用方法：
  python reset_password.py <手机号> <新密码>
示例：
  python reset_password.py 15680793860 123456
"""
import sys
import bcrypt

# 添加父目录到 sys.path 以支持模块导入
import os
sys.path.insert(0, os.path.dirname(__file__))

from storage.database import get_db, SessionLocal
from storage.models import User


def reset_password(mobile: str, new_password: str):
    """直接操作数据库重置密码"""
    # 生成密码哈希
    salt = bcrypt.gensalt()
    password_hash = bcrypt.hashpw(new_password.encode('utf-8'), salt).decode('utf-8')
    
    db = SessionLocal()
    try:
        # 按手机号精确匹配
        user = db.query(User).filter(User.mobile == mobile).first()
        
        # 尝试模糊匹配（去掉区号）
        if not user:
            for u in db.query(User).all():
                digits_u = ''.join(filter(str.isdigit, u.mobile))
                digits_input = ''.join(filter(str.isdigit, mobile))
                if digits_u == digits_input or digits_input in digits_u or digits_u in digits_input:
                    user = u
                    print(f"模糊匹配到用户: {u.mobile}")
                    break
        
        if not user:
            print(f"【失败】未找到手机号对应的用户: {mobile}")
            return False
        
        user.password_hash = password_hash
        db.commit()
        print(f"【成功】用户 {user.mobile} (ID:{user.id}) 密码已重置为: {new_password}")
        return True
        
    except Exception as e:
        db.rollback()
        print(f"【失败】重置密码出错: {e}")
        return False
    finally:
        db.close()


if __name__ == "__main__":
    if len(sys.argv) >= 3:
        phone = sys.argv[1]
        pwd = sys.argv[2]
    else:
        # 默认：重置 15680793860 的密码为 123456
        phone = "15680793860"
        pwd = "123456"
        print(f"使用默认参数: 手机号={phone}, 密码={pwd}")
    
    reset_password(phone, pwd)
