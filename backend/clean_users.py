"""清理用户数据 - 保留指定用户并重置密码"""
from storage.models import User, Record, Feedback, BonusLog, RewardLog, InviteReward, FileHashCache
from storage.database import get_db
from auth.utils import hash_password

def main():
    db = next(get_db())
    target_mobile = '15680793860'
    
    # 获取目标用户
    target_user = db.query(User).filter(User.mobile == target_mobile).first()
    if not target_user:
        print(f"错误：未找到用户 {target_mobile}")
        return
    
    target_user_id = target_user.id
    print(f"保留用户: ID={target_user_id}, Mobile={target_mobile}")
    
    # 获取需要删除的用户ID列表
    users_to_delete = db.query(User).filter(User.mobile != target_mobile).all()
    user_ids_to_delete = [u.id for u in users_to_delete]
    
    print(f"\n待删除用户列表:")
    for u in users_to_delete:
        print(f"  ID={u.id}, Mobile={u.mobile}")
    
    # 删除相关记录（按外键依赖顺序）
    print("\n删除相关记录...")
    
    # 删除 Record
    record_count = db.query(Record).filter(Record.user_id.in_(user_ids_to_delete)).delete(synchronize_session=False)
    print(f"  删除 Record: {record_count} 条")
    
    # 删除 Feedback
    feedback_count = db.query(Feedback).filter(Feedback.user_id.in_(user_ids_to_delete)).delete(synchronize_session=False)
    print(f"  删除 Feedback: {feedback_count} 条")
    
    # 删除 BonusLog
    bonuslog_count = db.query(BonusLog).filter(BonusLog.user_id.in_(user_ids_to_delete)).delete(synchronize_session=False)
    print(f"  删除 BonusLog: {bonuslog_count} 条")
    
    # 删除 RewardLog
    rewardlog_count = db.query(RewardLog).filter(RewardLog.user_id.in_(user_ids_to_delete)).delete(synchronize_session=False)
    print(f"  删除 RewardLog: {rewardlog_count} 条")
    
    # 删除 InviteReward (被邀请人)
    invitereward_invitee_count = db.query(InviteReward).filter(InviteReward.invitee_id.in_(user_ids_to_delete)).delete(synchronize_session=False)
    print(f"  删除 InviteReward (被邀请人): {invitereward_invitee_count} 条")
    
    # 删除 InviteReward (邀请人)
    invitereward_inviter_count = db.query(InviteReward).filter(InviteReward.inviter_id.in_(user_ids_to_delete)).delete(synchronize_session=False)
    print(f"  删除 InviteReward (邀请人): {invitereward_inviter_count} 条")
    
    # 删除 FileHashCache
    filehashcache_count = db.query(FileHashCache).filter(FileHashCache.user_id.in_(user_ids_to_delete)).delete(synchronize_session=False)
    print(f"  删除 FileHashCache: {filehashcache_count} 条")
    
    # 删除用户
    user_count = db.query(User).filter(User.id.in_(user_ids_to_delete)).delete(synchronize_session=False)
    print(f"  删除 User: {user_count} 条")
    
    # 提交事务
    db.commit()
    print(f"\n已成功删除 {user_count} 个用户及相关记录")
    
    # 重置目标用户密码
    target_user.password_hash = hash_password('a.144iLil123')
    db.commit()
    print("Admin密码已重置为: a.144iLil123")
    
    # 验证结果
    remaining_users = db.query(User).all()
    print(f"\n剩余用户:")
    for u in remaining_users:
        print(f"  ID={u.id}, Mobile={u.mobile}")

if __name__ == "__main__":
    main()
